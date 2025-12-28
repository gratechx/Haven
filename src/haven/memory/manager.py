"""Memory manager for storing and retrieving user data"""
from typing import List, Optional, Dict
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ..config import settings
from .models import Base, User, UserPreference, Conversation, Note, Task


class MemoryManager:
    """Manages user memory, preferences, and conversation history"""
    
    def __init__(self, database_url: Optional[str] = None):
        """Initialize memory manager with database connection"""
        self.database_url = database_url or settings.database_url
        self.engine = create_engine(self.database_url, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Create tables
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self) -> Session:
        """Get database session"""
        return self.SessionLocal()
    
    # User Management
    def get_or_create_user(self, username: str = "default") -> User:
        """Get existing user or create new one"""
        with self.get_session() as session:
            user = session.query(User).filter(User.username == username).first()
            if not user:
                user = User(username=username)
                session.add(user)
                session.commit()
                session.refresh(user)
            return user
    
    # Preferences
    def set_preference(self, username: str, key: str, value: str):
        """Set user preference"""
        with self.get_session() as session:
            user = self.get_or_create_user(username)
            pref = session.query(UserPreference).filter(
                UserPreference.user_id == user.id,
                UserPreference.key == key
            ).first()
            
            if pref:
                pref.value = value
                pref.updated_at = datetime.utcnow()
            else:
                pref = UserPreference(user_id=user.id, key=key, value=value)
                session.add(pref)
            
            session.commit()
    
    def get_preference(self, username: str, key: str) -> Optional[str]:
        """Get user preference"""
        with self.get_session() as session:
            user = self.get_or_create_user(username)
            pref = session.query(UserPreference).filter(
                UserPreference.user_id == user.id,
                UserPreference.key == key
            ).first()
            return pref.value if pref else None
    
    def get_all_preferences(self, username: str) -> Dict[str, str]:
        """Get all user preferences"""
        with self.get_session() as session:
            user = self.get_or_create_user(username)
            prefs = session.query(UserPreference).filter(
                UserPreference.user_id == user.id
            ).all()
            return {pref.key: pref.value for pref in prefs}
    
    # Conversation History
    def add_conversation(self, username: str, role: str, content: str, language: str = "ar"):
        """Add conversation message to history"""
        with self.get_session() as session:
            user = self.get_or_create_user(username)
            conversation = Conversation(
                user_id=user.id,
                role=role,
                content=content,
                language=language
            )
            session.add(conversation)
            session.commit()
    
    def get_conversation_history(
        self, 
        username: str, 
        limit: int = 50
    ) -> List[Dict[str, str]]:
        """Get recent conversation history"""
        with self.get_session() as session:
            user = self.get_or_create_user(username)
            conversations = session.query(Conversation).filter(
                Conversation.user_id == user.id
            ).order_by(Conversation.created_at.desc()).limit(limit).all()
            
            # Return in chronological order
            return [
                {"role": conv.role, "content": conv.content}
                for conv in reversed(conversations)
            ]
    
    def clear_conversation_history(self, username: str):
        """Clear conversation history for user"""
        with self.get_session() as session:
            user = self.get_or_create_user(username)
            session.query(Conversation).filter(
                Conversation.user_id == user.id
            ).delete()
            session.commit()
    
    # Notes Management
    def create_note(self, username: str, title: str, content: str, tags: str = "") -> int:
        """Create a new note"""
        with self.get_session() as session:
            user = self.get_or_create_user(username)
            note = Note(
                user_id=user.id,
                title=title,
                content=content,
                tags=tags
            )
            session.add(note)
            session.commit()
            session.refresh(note)
            return note.id
    
    def get_notes(self, username: str, search: Optional[str] = None) -> List[Dict]:
        """Get all notes, optionally filtered by search term"""
        with self.get_session() as session:
            user = self.get_or_create_user(username)
            query = session.query(Note).filter(Note.user_id == user.id)
            
            if search:
                query = query.filter(
                    (Note.title.contains(search)) | (Note.content.contains(search))
                )
            
            notes = query.order_by(Note.updated_at.desc()).all()
            return [
                {
                    "id": note.id,
                    "title": note.title,
                    "content": note.content,
                    "tags": note.tags,
                    "created_at": note.created_at,
                    "updated_at": note.updated_at
                }
                for note in notes
            ]
    
    def update_note(self, username: str, note_id: int, title: str, content: str, tags: str = ""):
        """Update an existing note"""
        with self.get_session() as session:
            user = self.get_or_create_user(username)
            note = session.query(Note).filter(
                Note.id == note_id,
                Note.user_id == user.id
            ).first()
            
            if note:
                note.title = title
                note.content = content
                note.tags = tags
                note.updated_at = datetime.utcnow()
                session.commit()
    
    def delete_note(self, username: str, note_id: int):
        """Delete a note"""
        with self.get_session() as session:
            user = self.get_or_create_user(username)
            session.query(Note).filter(
                Note.id == note_id,
                Note.user_id == user.id
            ).delete()
            session.commit()
    
    # Task Management
    def create_task(
        self, 
        username: str, 
        title: str, 
        description: str = "", 
        priority: str = "medium",
        due_date: Optional[datetime] = None
    ) -> int:
        """Create a new task"""
        with self.get_session() as session:
            user = self.get_or_create_user(username)
            task = Task(
                user_id=user.id,
                title=title,
                description=description,
                priority=priority,
                due_date=due_date
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            return task.id
    
    def get_tasks(
        self, 
        username: str, 
        completed: Optional[bool] = None
    ) -> List[Dict]:
        """Get all tasks, optionally filtered by completion status"""
        with self.get_session() as session:
            user = self.get_or_create_user(username)
            query = session.query(Task).filter(Task.user_id == user.id)
            
            if completed is not None:
                query = query.filter(Task.completed == completed)
            
            tasks = query.order_by(Task.created_at.desc()).all()
            return [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority,
                    "due_date": task.due_date,
                    "created_at": task.created_at,
                    "updated_at": task.updated_at
                }
                for task in tasks
            ]
    
    def toggle_task(self, username: str, task_id: int):
        """Toggle task completion status"""
        with self.get_session() as session:
            user = self.get_or_create_user(username)
            task = session.query(Task).filter(
                Task.id == task_id,
                Task.user_id == user.id
            ).first()
            
            if task:
                task.completed = not task.completed
                task.updated_at = datetime.utcnow()
                session.commit()
    
    def delete_task(self, username: str, task_id: int):
        """Delete a task"""
        with self.get_session() as session:
            user = self.get_or_create_user(username)
            session.query(Task).filter(
                Task.id == task_id,
                Task.user_id == user.id
            ).delete()
            session.commit()
