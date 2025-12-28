"""Rich terminal UI for Haven"""
from typing import Optional, Callable
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich.table import Table
from rich import box
from rich.text import Text


class TerminalUI:
    """Rich terminal interface with Arabic support"""
    
    def __init__(self):
        """Initialize terminal UI"""
        self.console = Console()
        self.current_language = "ar"
    
    def set_language(self, language: str):
        """Set UI language"""
        self.current_language = language
    
    def clear(self):
        """Clear the console"""
        self.console.clear()
    
    def print_welcome(self):
        """Print welcome message"""
        welcome_ar = """
# مرحباً بك في Haven 🌟
## رفيقك الذكي الشخصي

**الفلسفة**: "الإنسان يأمر، الذكاء الاصطناعي يخدم"

### المزايا المتاحة:
- 💬 محادثة ذكية بالعربية والإنجليزية
- 🧠 ذاكرة لتذكر تفضيلاتك
- 🐙 تكامل مع GitHub
- ☁️  تكامل مع Azure
- 📝 مساحة عمل للملاحظات والمهام
- 🔒 نظام موافقة للإجراءات الحساسة

اكتب `help` أو `مساعدة` للحصول على قائمة الأوامر.
"""
        
        welcome_en = """
# Welcome to Haven 🌟
## Your Personal AI Companion

**Philosophy**: "The human commands, the AI serves"

### Available Features:
- 💬 Smart conversation in Arabic and English
- 🧠 Memory to remember your preferences
- 🐙 GitHub integration
- ☁️  Azure integration
- 📝 Workspace for notes and tasks
- 🔒 Consent system for sensitive actions

Type `help` for a list of commands.
"""
        
        content = welcome_ar if self.current_language == "ar" else welcome_en
        self.console.print(Panel(Markdown(content), border_style="green"))
    
    def print_message(self, message: str, style: str = ""):
        """Print a message"""
        self.console.print(message, style=style)
    
    def print_panel(
        self, 
        content: str, 
        title: str = "", 
        style: str = "blue",
        markdown: bool = True
    ):
        """Print content in a panel"""
        if markdown:
            content = Markdown(content)
        self.console.print(Panel(content, title=title, border_style=style))
    
    def print_error(self, message: str):
        """Print error message"""
        error_prefix = "❌ خطأ:" if self.current_language == "ar" else "❌ Error:"
        self.console.print(f"{error_prefix} {message}", style="red")
    
    def print_success(self, message: str):
        """Print success message"""
        success_prefix = "✅ نجح:" if self.current_language == "ar" else "✅ Success:"
        self.console.print(f"{success_prefix} {message}", style="green")
    
    def print_warning(self, message: str):
        """Print warning message (calm, not panic)"""
        self.console.print(Panel(message, border_style="yellow", title="⚠️"))
    
    def print_info(self, message: str):
        """Print info message"""
        self.console.print(f"ℹ️  {message}", style="cyan")
    
    def prompt(self, message: str, default: str = "") -> str:
        """Prompt user for input"""
        return Prompt.ask(message, default=default)
    
    def confirm(self, message: str, default: bool = False) -> bool:
        """Ask user for confirmation"""
        return Confirm.ask(message, default=default)
    
    def print_chat_message(self, role: str, content: str):
        """Print a chat message"""
        if role == "user":
            prefix = "👤 أنت" if self.current_language == "ar" else "👤 You"
            style = "cyan"
        else:
            prefix = "🤖 Haven"
            style = "green"
        
        self.console.print(f"\n{prefix}:", style=f"bold {style}")
        self.console.print(content)
    
    def print_table(self, headers: list, rows: list, title: str = ""):
        """Print data in a table"""
        table = Table(title=title, box=box.ROUNDED)
        
        for header in headers:
            table.add_column(header, style="cyan")
        
        for row in rows:
            table.add_row(*[str(cell) for cell in row])
        
        self.console.print(table)
    
    def print_help(self):
        """Print help message"""
        help_ar = """
## الأوامر المتاحة:

### أوامر عامة:
- `help` أو `مساعدة` - عرض هذه الرسالة
- `clear` أو `مسح` - مسح الشاشة
- `exit` أو `خروج` - الخروج من البرنامج
- `language <ar|en>` - تغيير اللغة

### المحادثة:
- `chat` أو `محادثة` - بدء محادثة جديدة
- `history` أو `سجل` - عرض سجل المحادثات

### مساحة العمل:
- `notes` أو `ملاحظات` - إدارة الملاحظات
- `tasks` أو `مهام` - إدارة المهام

### التكاملات:
- `github` - أوامر GitHub
- `azure` - أوامر Azure

### التفضيلات:
- `preferences` أو `تفضيلات` - إدارة التفضيلات
"""
        
        help_en = """
## Available Commands:

### General:
- `help` - Show this message
- `clear` - Clear screen
- `exit` - Exit the program
- `language <ar|en>` - Change language

### Conversation:
- `chat` - Start a new conversation
- `history` - View conversation history

### Workspace:
- `notes` - Manage notes
- `tasks` - Manage tasks

### Integrations:
- `github` - GitHub commands
- `azure` - Azure commands

### Preferences:
- `preferences` - Manage preferences
"""
        
        content = help_ar if self.current_language == "ar" else help_en
        self.console.print(Panel(Markdown(content), title="Help", border_style="blue"))
    
    def show_loading(self, message: str = ""):
        """Show loading indicator"""
        loading_msg = message or ("جاري المعالجة..." if self.current_language == "ar" else "Processing...")
        return self.console.status(loading_msg, spinner="dots")
