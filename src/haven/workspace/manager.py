"""Workspace manager for notes and tasks"""
from typing import List, Dict, Optional
from datetime import datetime
from ..memory import MemoryManager


class WorkspaceManager:
    """
    Workspace manager - Notion-like features for notes and tasks
    """
    
    def __init__(self, memory_manager: MemoryManager, username: str = "default"):
        """Initialize workspace manager"""
        self.memory = memory_manager
        self.username = username
    
    # Notes Management
    def create_note(self, title: str, content: str, tags: str = "") -> int:
        """Create a new note"""
        return self.memory.create_note(self.username, title, content, tags)
    
    def list_notes(self, search: Optional[str] = None) -> List[Dict]:
        """List all notes"""
        return self.memory.get_notes(self.username, search)
    
    def get_note(self, note_id: int) -> Optional[Dict]:
        """Get a specific note"""
        notes = self.memory.get_notes(self.username)
        for note in notes:
            if note["id"] == note_id:
                return note
        return None
    
    def update_note(self, note_id: int, title: str, content: str, tags: str = "") -> bool:
        """Update an existing note"""
        try:
            self.memory.update_note(self.username, note_id, title, content, tags)
            return True
        except Exception:
            return False
    
    def delete_note(self, note_id: int) -> bool:
        """Delete a note"""
        try:
            self.memory.delete_note(self.username, note_id)
            return True
        except Exception:
            return False
    
    def search_notes(self, query: str) -> List[Dict]:
        """Search notes by title or content"""
        return self.memory.get_notes(self.username, search=query)
    
    # Tasks Management
    def create_task(
        self, 
        title: str, 
        description: str = "", 
        priority: str = "medium",
        due_date: Optional[datetime] = None
    ) -> int:
        """Create a new task"""
        return self.memory.create_task(
            self.username, 
            title, 
            description, 
            priority, 
            due_date
        )
    
    def list_tasks(self, show_completed: bool = False) -> List[Dict]:
        """List tasks"""
        if show_completed:
            return self.memory.get_tasks(self.username)
        else:
            return self.memory.get_tasks(self.username, completed=False)
    
    def get_task(self, task_id: int) -> Optional[Dict]:
        """Get a specific task"""
        tasks = self.memory.get_tasks(self.username)
        for task in tasks:
            if task["id"] == task_id:
                return task
        return None
    
    def toggle_task(self, task_id: int) -> bool:
        """Toggle task completion status"""
        try:
            self.memory.toggle_task(self.username, task_id)
            return True
        except Exception:
            return False
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        try:
            self.memory.delete_task(self.username, task_id)
            return True
        except Exception:
            return False
    
    def get_pending_tasks(self) -> List[Dict]:
        """Get all pending tasks"""
        return self.memory.get_tasks(self.username, completed=False)
    
    def get_completed_tasks(self) -> List[Dict]:
        """Get all completed tasks"""
        return self.memory.get_tasks(self.username, completed=True)
    
    def get_tasks_by_priority(self, priority: str) -> List[Dict]:
        """Get tasks filtered by priority"""
        all_tasks = self.memory.get_tasks(self.username, completed=False)
        return [task for task in all_tasks if task["priority"] == priority]
    
    # Workspace Statistics
    def get_stats(self) -> Dict:
        """Get workspace statistics"""
        notes = self.list_notes()
        all_tasks = self.memory.get_tasks(self.username)
        pending_tasks = [t for t in all_tasks if not t["completed"]]
        completed_tasks = [t for t in all_tasks if t["completed"]]
        
        return {
            "total_notes": len(notes),
            "total_tasks": len(all_tasks),
            "pending_tasks": len(pending_tasks),
            "completed_tasks": len(completed_tasks),
            "completion_rate": (
                len(completed_tasks) / len(all_tasks) * 100
                if all_tasks else 0
            ),
        }
    
    # Bulk Operations
    def export_workspace(self) -> Dict:
        """Export entire workspace data"""
        return {
            "notes": self.list_notes(),
            "tasks": self.memory.get_tasks(self.username),
            "stats": self.get_stats(),
            "exported_at": datetime.utcnow().isoformat(),
        }
    
    def clear_completed_tasks(self) -> int:
        """Delete all completed tasks"""
        completed = self.get_completed_tasks()
        count = 0
        for task in completed:
            if self.delete_task(task["id"]):
                count += 1
        return count
