"""Tests for Haven application"""
import pytest
from haven.memory import MemoryManager
from haven.workspace import WorkspaceManager
from haven.consent import ConsentManager, ActionRisk


@pytest.fixture
def memory_manager():
    """Create a test memory manager"""
    return MemoryManager("sqlite:///:memory:")


@pytest.fixture
def workspace_manager(memory_manager):
    """Create a test workspace manager"""
    return WorkspaceManager(memory_manager, "test_user")


class TestMemoryManager:
    """Test memory management"""
    
    def test_create_user(self, memory_manager):
        """Test user creation"""
        user = memory_manager.get_or_create_user("test_user")
        assert user is not None
        assert user.username == "test_user"
    
    def test_preferences(self, memory_manager):
        """Test user preferences"""
        memory_manager.set_preference("test_user", "language", "ar")
        pref = memory_manager.get_preference("test_user", "language")
        assert pref == "ar"
    
    def test_conversation_history(self, memory_manager):
        """Test conversation history"""
        memory_manager.add_conversation("test_user", "user", "Hello", "en")
        memory_manager.add_conversation("test_user", "assistant", "Hi there", "en")
        
        history = memory_manager.get_conversation_history("test_user")
        assert len(history) == 2
        assert history[0]["role"] == "user"
        assert history[1]["role"] == "assistant"


class TestWorkspaceManager:
    """Test workspace management"""
    
    def test_create_note(self, workspace_manager):
        """Test note creation"""
        note_id = workspace_manager.create_note("Test Note", "Content", "tag1,tag2")
        assert note_id > 0
        
        notes = workspace_manager.list_notes()
        assert len(notes) == 1
        assert notes[0]["title"] == "Test Note"
    
    def test_create_task(self, workspace_manager):
        """Test task creation"""
        task_id = workspace_manager.create_task("Test Task", "Description", "high")
        assert task_id > 0
        
        tasks = workspace_manager.list_tasks()
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Test Task"
        assert tasks[0]["priority"] == "high"
        assert not tasks[0]["completed"]
    
    def test_toggle_task(self, workspace_manager):
        """Test task completion toggle"""
        task_id = workspace_manager.create_task("Test Task", "Description")
        workspace_manager.toggle_task(task_id)
        
        tasks = workspace_manager.list_tasks(show_completed=True)
        assert tasks[0]["completed"]
    
    def test_workspace_stats(self, workspace_manager):
        """Test workspace statistics"""
        workspace_manager.create_note("Note 1", "Content 1")
        workspace_manager.create_note("Note 2", "Content 2")
        workspace_manager.create_task("Task 1", "Desc 1")
        task_id = workspace_manager.create_task("Task 2", "Desc 2")
        workspace_manager.toggle_task(task_id)
        
        stats = workspace_manager.get_stats()
        assert stats["total_notes"] == 2
        assert stats["total_tasks"] == 2
        assert stats["pending_tasks"] == 1
        assert stats["completed_tasks"] == 1


class TestConsentManager:
    """Test consent system"""
    
    def test_action_risk_levels(self):
        """Test action risk assessment"""
        consent = ConsentManager()
        
        # Safe actions don't require consent
        assert not consent.requires_consent("unknown_action")
        
        # Critical actions require consent
        assert consent.requires_consent("github_delete_repo")
        assert consent.get_action_risk("github_delete_repo") == ActionRisk.CRITICAL
    
    def test_consent_callback(self):
        """Test consent callback"""
        approved = False
        
        def callback(warning, language):
            return approved
        
        consent = ConsentManager(callback=callback)
        
        # Denied by default
        assert not consent.request_consent("github_delete_repo", "ar")
        
        # Approved when callback returns True
        approved = True
        assert consent.request_consent("github_delete_repo", "ar")
    
    def test_warnings(self):
        """Test warning messages"""
        consent = ConsentManager()
        
        warning_ar = consent.get_warning("github_delete_repo", "ar")
        warning_en = consent.get_warning("github_delete_repo", "en")
        
        assert "تحذير" in warning_ar
        assert "Warning" in warning_en


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
