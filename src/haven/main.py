"""Main Haven application"""
import sys
import asyncio
from typing import Optional
from .ui import TerminalUI
from .core import AIEngine, DEFAULT_SYSTEM_PROMPT
from .memory import MemoryManager
from .consent import ConsentManager
from .integrations import GitHubService, AzureService
from .workspace import WorkspaceManager
from .config import settings


class HavenApp:
    """Main Haven application"""
    
    def __init__(self, username: str = "default"):
        """Initialize Haven application"""
        self.username = username
        self.ui = TerminalUI()
        self.memory = MemoryManager()
        self.consent = ConsentManager(callback=self._consent_callback)
        self.workspace = WorkspaceManager(self.memory, username)
        
        # Initialize AI engine (may fail if no API key)
        try:
            self.ai = AIEngine()
        except ValueError as e:
            self.ai = None
            self.ui.print_warning(str(e))
        
        # Initialize integrations (may fail if no credentials)
        try:
            self.github = GitHubService(self.consent)
        except ValueError:
            self.github = None
        
        try:
            self.azure = AzureService(self.consent)
        except ValueError:
            self.azure = None
        
        # Load user language preference
        lang = self.memory.get_preference(username, "language")
        if lang:
            self.ui.set_language(lang)
            settings.language = lang
    
    def _consent_callback(self, warning: str, language: str) -> bool:
        """Callback for consent manager"""
        self.ui.print_warning(warning)
        confirm_text = "هل تريد المتابعة؟" if language == "ar" else "Do you want to continue?"
        return self.ui.confirm(confirm_text, default=False)
    
    async def chat(self):
        """Start chat session"""
        if not self.ai:
            error_msg = "AI engine not initialized. Please configure API keys." if self.ui.current_language == "en" else "محرك الذكاء الاصطناعي غير مهيأ. يرجى تكوين مفاتيح API."
            self.ui.print_error(error_msg)
            return
        
        chat_msg = "بدء المحادثة. اكتب 'exit' للخروج." if self.ui.current_language == "ar" else "Starting chat. Type 'exit' to quit."
        self.ui.print_info(chat_msg)
        
        # Load conversation history
        messages = self.memory.get_conversation_history(self.username, limit=10)
        
        while True:
            # Get user input
            prompt_text = "أنت" if self.ui.current_language == "ar" else "You"
            user_input = self.ui.prompt(f"\n👤 {prompt_text}")
            
            if not user_input.strip():
                continue
            
            if user_input.lower() in ["exit", "خروج", "quit"]:
                break
            
            # Detect language
            language = self.ai.detect_language(user_input)
            
            # Add to conversation
            messages.append({"role": "user", "content": user_input})
            self.memory.add_conversation(self.username, "user", user_input, language)
            
            # Generate response
            try:
                with self.ui.show_loading():
                    response = await self.ai.generate_response(messages, DEFAULT_SYSTEM_PROMPT)
                
                messages.append({"role": "assistant", "content": response})
                self.memory.add_conversation(self.username, "assistant", response, language)
                
                # Display response
                self.ui.print_chat_message("assistant", response)
                
            except Exception as e:
                error_msg = f"Error generating response: {str(e)}"
                self.ui.print_error(error_msg)
    
    def show_help(self):
        """Show help message"""
        self.ui.print_help()
    
    def clear_screen(self):
        """Clear the screen"""
        self.ui.clear()
    
    def change_language(self, lang: str):
        """Change interface language"""
        if lang in ["ar", "en"]:
            self.ui.set_language(lang)
            self.memory.set_preference(self.username, "language", lang)
            success_msg = f"Language changed to {lang}"
            self.ui.print_success(success_msg)
        else:
            error_msg = "Invalid language. Use 'ar' or 'en'."
            self.ui.print_error(error_msg)
    
    def show_history(self):
        """Show conversation history"""
        history = self.memory.get_conversation_history(self.username, limit=20)
        
        if not history:
            msg = "لا يوجد سجل محادثات." if self.ui.current_language == "ar" else "No conversation history."
            self.ui.print_info(msg)
            return
        
        title = "سجل المحادثات" if self.ui.current_language == "ar" else "Conversation History"
        self.ui.print_panel(f"### {title}", markdown=False)
        
        for msg in history[-10:]:  # Show last 10 messages
            self.ui.print_chat_message(msg["role"], msg["content"])
    
    def manage_notes(self):
        """Manage notes"""
        while True:
            self.ui.print_panel(
                "### Notes Menu\n1. List notes\n2. Create note\n3. Delete note\n4. Back",
                title="📝 Notes"
            )
            
            choice = self.ui.prompt("Choice")
            
            if choice == "1":
                notes = self.workspace.list_notes()
                if not notes:
                    self.ui.print_info("No notes found.")
                else:
                    for note in notes:
                        self.ui.print_panel(
                            f"{note['content'][:100]}...",
                            title=f"#{note['id']} - {note['title']}"
                        )
            
            elif choice == "2":
                title = self.ui.prompt("Note title")
                content = self.ui.prompt("Note content")
                tags = self.ui.prompt("Tags (comma-separated)", default="")
                note_id = self.workspace.create_note(title, content, tags)
                self.ui.print_success(f"Note created with ID: {note_id}")
            
            elif choice == "3":
                note_id = int(self.ui.prompt("Note ID to delete"))
                if self.workspace.delete_note(note_id):
                    self.ui.print_success("Note deleted")
                else:
                    self.ui.print_error("Failed to delete note")
            
            else:
                break
    
    def manage_tasks(self):
        """Manage tasks"""
        while True:
            self.ui.print_panel(
                "### Tasks Menu\n1. List tasks\n2. Create task\n3. Toggle task\n4. Delete task\n5. Back",
                title="✅ Tasks"
            )
            
            choice = self.ui.prompt("Choice")
            
            if choice == "1":
                tasks = self.workspace.list_tasks()
                if not tasks:
                    self.ui.print_info("No tasks found.")
                else:
                    for task in tasks:
                        status = "✅" if task['completed'] else "⬜"
                        self.ui.print_message(
                            f"{status} #{task['id']} - {task['title']} [{task['priority']}]"
                        )
            
            elif choice == "2":
                title = self.ui.prompt("Task title")
                description = self.ui.prompt("Description", default="")
                priority = self.ui.prompt("Priority (low/medium/high)", default="medium")
                task_id = self.workspace.create_task(title, description, priority)
                self.ui.print_success(f"Task created with ID: {task_id}")
            
            elif choice == "3":
                task_id = int(self.ui.prompt("Task ID to toggle"))
                if self.workspace.toggle_task(task_id):
                    self.ui.print_success("Task toggled")
                else:
                    self.ui.print_error("Failed to toggle task")
            
            elif choice == "4":
                task_id = int(self.ui.prompt("Task ID to delete"))
                if self.workspace.delete_task(task_id):
                    self.ui.print_success("Task deleted")
                else:
                    self.ui.print_error("Failed to delete task")
            
            else:
                break
    
    def show_preferences(self):
        """Show user preferences"""
        prefs = self.memory.get_all_preferences(self.username)
        
        if not prefs:
            msg = "لا توجد تفضيلات." if self.ui.current_language == "ar" else "No preferences found."
            self.ui.print_info(msg)
            return
        
        title = "التفضيلات" if self.ui.current_language == "ar" else "Preferences"
        self.ui.print_table(
            ["Key", "Value"],
            [[k, v] for k, v in prefs.items()],
            title=title
        )
    
    def github_menu(self):
        """GitHub integration menu"""
        if not self.github:
            self.ui.print_error("GitHub not configured. Please set GITHUB_TOKEN in .env")
            return
        
        self.ui.print_panel(
            "### GitHub Menu\n1. List repositories\n2. User info\n3. Back",
            title="🐙 GitHub"
        )
        
        choice = self.ui.prompt("Choice")
        
        if choice == "1":
            repos = self.github.list_repositories()
            for repo in repos:
                self.ui.print_message(f"⭐ {repo['full_name']} - {repo['description']}")
        
        elif choice == "2":
            info = self.github.get_user_info()
            self.ui.print_panel(
                f"**Name:** {info['name']}\n**Login:** {info['login']}\n**Repos:** {info['public_repos']}",
                title="User Info"
            )
    
    def azure_menu(self):
        """Azure integration menu"""
        if not self.azure:
            self.ui.print_error("Azure not configured. Please set Azure credentials in .env")
            return
        
        self.ui.print_panel(
            "### Azure Menu\n1. List resource groups\n2. Subscription info\n3. Back",
            title="☁️  Azure"
        )
        
        choice = self.ui.prompt("Choice")
        
        if choice == "1":
            groups = self.azure.list_resource_groups()
            for group in groups:
                if "error" not in group:
                    self.ui.print_message(f"📦 {group['name']} - {group['location']}")
        
        elif choice == "2":
            info = self.azure.get_subscription_info()
            if "error" not in info:
                self.ui.print_panel(
                    f"**Name:** {info['display_name']}\n**ID:** {info['subscription_id']}\n**State:** {info['state']}",
                    title="Subscription Info"
                )
    
    async def run(self):
        """Main application loop"""
        self.ui.clear()
        self.ui.print_welcome()
        
        while True:
            try:
                command = self.ui.prompt("\n⚡ Haven").strip().lower()
                
                if not command:
                    continue
                
                # Parse command
                parts = command.split()
                cmd = parts[0]
                args = parts[1:] if len(parts) > 1 else []
                
                # Command routing
                if cmd in ["exit", "خروج", "quit"]:
                    bye_msg = "وداعاً! 👋" if self.ui.current_language == "ar" else "Goodbye! 👋"
                    self.ui.print_success(bye_msg)
                    break
                
                elif cmd in ["help", "مساعدة"]:
                    self.show_help()
                
                elif cmd in ["clear", "مسح"]:
                    self.clear_screen()
                    self.ui.print_welcome()
                
                elif cmd == "language":
                    if args:
                        self.change_language(args[0])
                    else:
                        self.ui.print_error("Usage: language <ar|en>")
                
                elif cmd in ["chat", "محادثة"]:
                    await self.chat()
                
                elif cmd in ["history", "سجل"]:
                    self.show_history()
                
                elif cmd in ["notes", "ملاحظات"]:
                    self.manage_notes()
                
                elif cmd in ["tasks", "مهام"]:
                    self.manage_tasks()
                
                elif cmd in ["preferences", "تفضيلات"]:
                    self.show_preferences()
                
                elif cmd == "github":
                    self.github_menu()
                
                elif cmd == "azure":
                    self.azure_menu()
                
                else:
                    # Try to interpret as chat message if AI is available
                    if self.ai:
                        messages = [{"role": "user", "content": command}]
                        with self.ui.show_loading():
                            response = await self.ai.generate_response(messages, DEFAULT_SYSTEM_PROMPT)
                        self.ui.print_chat_message("assistant", response)
                    else:
                        unknown_msg = "أمر غير معروف. اكتب 'help' للمساعدة." if self.ui.current_language == "ar" else "Unknown command. Type 'help' for help."
                        self.ui.print_error(unknown_msg)
            
            except KeyboardInterrupt:
                self.ui.print_message("\n")
                if self.ui.confirm("Exit Haven?", default=False):
                    break
            except Exception as e:
                self.ui.print_error(f"Error: {str(e)}")


def main():
    """Main entry point"""
    app = HavenApp()
    asyncio.run(app.run())


if __name__ == "__main__":
    main()
