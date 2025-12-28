# Haven 🌟
## رفيقك الذكي الشخصي | Your Personal AI Companion

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Philosophy**: "The human commands, the AI serves" | "الإنسان يأمر، الذكاء الاصطناعي يخدم"

Haven is an AI companion app with Arabic-first interface, providing gentle warnings, full transparency, and human-centric design.

## ✨ Features

### 🧠 Core AI Engine
- **Arabic Language Support**: Native understanding of Arabic language
- **Multi-provider**: Support for OpenAI and Anthropic Claude
- **Context-aware**: Remembers conversation context

### 💾 Memory System
- **User Preferences**: Remembers your preferences and settings
- **Conversation History**: Persistent chat history
- **Smart Recall**: Retrieves relevant past conversations

### 🔗 Integrations
- **GitHub**: Repository management, issues, PRs
- **Azure**: Cloud resource management
- Extensible architecture for more integrations

### 🔒 Consent System
- **Always Asks First**: No dangerous actions without explicit consent
- **Risk Levels**: Safe, Low, Medium, High, Critical
- **Calm Warnings**: Human-friendly, not panic-inducing
- **Transparent**: Always clear about what will happen

### 💻 Terminal Interface
- **Rich UI**: Beautiful terminal interface with Rich library
- **Arabic Support**: Full RTL support in terminal
- **Interactive**: Intuitive command-based interface
- **Multilingual**: Switch between Arabic and English

### 📝 Workspace (Notion Alternative)
- **Notes**: Create, edit, search, and organize notes
- **Tasks**: Todo lists with priorities and due dates
- **Tags**: Organize content with tags
- **Search**: Full-text search across all content

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/gratechx/Haven.git
cd Haven
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys and credentials
```

4. **Install Haven**
```bash
pip install -e .
```

### Configuration

Edit `.env` file with your credentials:

```bash
# AI Provider (choose one)
AI_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
# OR
# AI_PROVIDER=anthropic
# ANTHROPIC_API_KEY=your_anthropic_api_key_here

# GitHub Integration (optional)
GITHUB_TOKEN=your_github_token_here

# Azure Integration (optional)
AZURE_SUBSCRIPTION_ID=your_subscription_id_here
AZURE_TENANT_ID=your_tenant_id_here
AZURE_CLIENT_ID=your_client_id_here
AZURE_CLIENT_SECRET=your_client_secret_here

# Application Settings
DATABASE_URL=sqlite:///./haven.db
LOG_LEVEL=INFO
LANGUAGE=ar  # ar for Arabic, en for English
```

### Running Haven

```bash
haven
# OR
python -m haven.main
```

## 📖 Usage

### Commands

#### General Commands
- `help` or `مساعدة` - Show help message
- `clear` or `مسح` - Clear screen
- `exit` or `خروج` - Exit Haven
- `language <ar|en>` - Change language

#### Conversation
- `chat` or `محادثة` - Start chat session
- `history` or `سجل` - View conversation history
- Type any message to get AI response

#### Workspace
- `notes` or `ملاحظات` - Manage notes
  - List, create, edit, delete notes
  - Search notes
  - Tag organization
- `tasks` or `مهام` - Manage tasks
  - Create todo items
  - Set priorities (low/medium/high)
  - Mark as complete
  - Delete tasks

#### Integrations
- `github` - GitHub operations
  - List repositories
  - View user info
  - Create issues (coming soon)
- `azure` - Azure operations
  - List resource groups
  - View subscription info
  - Manage resources (coming soon)

#### Preferences
- `preferences` or `تفضيلات` - View saved preferences

### Examples

**Arabic Conversation:**
```
⚡ Haven: مرحباً، كيف يمكنني مساعدتك؟
👤 أنت: ما هي أفضل ممارسات البرمجة؟
🤖 Haven: [AI provides response in Arabic]
```

**English Conversation:**
```
⚡ Haven: chat
👤 You: What are the best coding practices?
🤖 Haven: [AI provides response in English]
```

**Creating a Note:**
```
⚡ Haven: notes
📝 Notes Menu
1. List notes
2. Create note
3. Delete note
4. Back

Choice: 2
Note title: Meeting Notes
Note content: Discussed project timeline and deliverables
Tags: work, meeting
✅ Success: Note created with ID: 1
```

**Managing Tasks:**
```
⚡ Haven: tasks
✅ Tasks Menu
1. List tasks
2. Create task
3. Toggle task
4. Delete task
5. Back

Choice: 2
Task title: Review pull request
Description: Check PR #123
Priority (low/medium/high): high
✅ Success: Task created with ID: 1
```

## 🏗️ Architecture

```
src/haven/
├── core/           # AI engine
├── memory/         # Database and memory management
├── consent/        # Consent system for dangerous actions
├── integrations/   # GitHub, Azure, etc.
├── ui/             # Terminal interface
├── workspace/      # Notes and tasks
├── config.py       # Configuration management
└── main.py         # Main application
```

## 🔐 Security & Privacy

- **Consent First**: Always asks before dangerous operations
- **Local Storage**: Data stored locally in SQLite
- **API Keys**: Stored in `.env` (never committed)
- **Transparent**: Clear about what data is accessed
- **Risk Assessment**: Every action is risk-assessed

### Risk Levels

- 🟢 **SAFE**: No consent needed
- 🔵 **LOW**: Quick confirmation
- 🟡 **MEDIUM**: Clear warning
- 🟠 **HIGH**: Explicit consent required
- 🔴 **CRITICAL**: Multiple confirmations

## 🌍 Language Support

Haven supports both Arabic and English:

- **Arabic-first**: Default language is Arabic
- **Auto-detection**: Detects language from input
- **Consistent**: Responds in the same language
- **Switchable**: Change language anytime with `language` command

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- UI powered by [Rich](https://rich.readthedocs.io/)
- AI by [OpenAI](https://openai.com/) and [Anthropic](https://anthropic.com/)

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Remember**: "The human commands, the AI serves" | "الإنسان يأمر، الذكاء الاصطناعي يخدم"
