"""
Haven - Your Personal AI Companion
Quick start guide
"""

# Installation
pip install -r requirements.txt
pip install -e .

# Configuration
cp .env.example .env
# Edit .env with your API keys

# Run
haven
# OR
python -m haven.main

# First time setup
1. Configure at least one AI provider (OpenAI or Anthropic)
2. Optionally configure GitHub and Azure credentials
3. Run `haven` to start

# Basic Commands
- help: Show help
- chat: Start conversation
- notes: Manage notes
- tasks: Manage tasks
- exit: Quit

# Language
- Default: Arabic
- Change: `language en` or `language ar`

# Philosophy
"The human commands, the AI serves"
الإنسان يأمر، الذكاء الاصطناعي يخدم
