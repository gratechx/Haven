# Haven Architecture Overview

## System Design

```
┌─────────────────────────────────────────────────────────────┐
│                      Haven Application                      │
└─────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            │                 │                 │
      ┌─────▼─────┐    ┌─────▼─────┐    ┌─────▼─────┐
      │  Terminal  │    │    Core   │    │   Memory  │
      │     UI     │    │ AI Engine │    │  Manager  │
      └───────────┘    └───────────┘    └───────────┘
            │                 │                 │
            │                 │          ┌──────▼──────┐
            │                 │          │   SQLite    │
            │                 │          │  Database   │
            │                 │          └─────────────┘
            │                 │
      ┌─────▼─────────────────▼──────────┐
      │         Consent Manager          │
      └──────────────────────────────────┘
            │
      ┌─────▼──────────┬─────────────────┐
      │                │                 │
┌─────▼─────┐   ┌─────▼─────┐   ┌──────▼──────┐
│  GitHub   │   │   Azure   │   │  Workspace  │
│  Service  │   │  Service  │   │   Manager   │
└───────────┘   └───────────┘   └─────────────┘
```

## Core Components

### 1. Terminal UI (`src/haven/ui/`)
- Rich-based terminal interface
- Arabic and English support
- Interactive prompts and menus
- Beautiful formatted output

**Key Features:**
- Panels, tables, and formatted text
- Color-coded messages (success, error, warning, info)
- Chat message display
- Loading indicators

### 2. Core AI Engine (`src/haven/core/`)
- Multi-provider support (OpenAI, Anthropic)
- Arabic language detection
- Context-aware responses
- Conversation management

**Key Features:**
- Automatic language detection
- System prompt management
- Message history handling
- Error handling for API failures

### 3. Memory Manager (`src/haven/memory/`)
- SQLite database backend
- User preferences storage
- Conversation history
- Notes and tasks persistence

**Database Models:**
- `User`: User accounts
- `UserPreference`: Key-value preferences
- `Conversation`: Chat history
- `Note`: Workspace notes
- `Task`: Todo items

### 4. Consent Manager (`src/haven/consent/`)
- Risk assessment system
- Human-friendly warnings
- Multi-level consent flow
- Action classification

**Risk Levels:**
- SAFE: Auto-approve
- LOW: Quick confirmation
- MEDIUM: Clear warning
- HIGH: Explicit consent
- CRITICAL: Multiple confirmations

### 5. Integrations (`src/haven/integrations/`)

#### GitHub Service
- Repository management
- Issue tracking
- User information
- Consent-protected operations

#### Azure Service
- Resource group management
- Subscription information
- Resource listing
- Consent-protected operations

### 6. Workspace Manager (`src/haven/workspace/`)
- Notes management (Notion-like)
- Task tracking with priorities
- Search functionality
- Statistics and analytics

## Data Flow

### Chat Flow
```
User Input → Language Detection → AI Engine → Response Generation
    ↓                                              ↓
Memory Storage ← Conversation History ← Response Storage
```

### Dangerous Action Flow
```
User Command → Action Detection → Risk Assessment
                    ↓
            Consent Required?
                    ↓
        ┌───────────┴───────────┐
       Yes                      No
        ↓                        ↓
Show Warning              Execute Action
        ↓
  User Confirms?
        ↓
   ┌────┴────┐
  Yes       No
   ↓         ↓
Execute   Cancel
Action
```

## Configuration

### Environment Variables
- `AI_PROVIDER`: openai or anthropic
- `OPENAI_API_KEY`: OpenAI API key
- `ANTHROPIC_API_KEY`: Anthropic API key
- `GITHUB_TOKEN`: GitHub personal access token
- `AZURE_*`: Azure credentials
- `DATABASE_URL`: SQLite database path
- `LANGUAGE`: Default language (ar/en)

### User Preferences (Stored in DB)
- Language preference
- Custom settings
- User-specific configurations

## Security Considerations

1. **API Key Storage**: Keys stored in `.env` file (not committed)
2. **Consent System**: Always asks before dangerous operations
3. **Risk Assessment**: Every action classified by risk level
4. **Calm Warnings**: Human-friendly, not panic-inducing
5. **Transparency**: Clear about what will happen
6. **Local Storage**: Data stored locally in SQLite

## Extensibility

### Adding New Integrations
1. Create service class in `src/haven/integrations/`
2. Implement consent checks for dangerous actions
3. Register actions in ConsentManager
4. Add UI commands in main application

### Adding New Languages
1. Update language detection in AI engine
2. Add language-specific warnings in ConsentManager
3. Update UI messages
4. Update system prompts

### Adding New Features
1. Define data models in `src/haven/memory/models.py`
2. Add manager methods in appropriate manager
3. Create UI commands
4. Add tests

## Philosophy: "The Human Commands, the AI Serves"

This architecture enforces the core philosophy:

1. **Human Authority**: User must approve dangerous actions
2. **AI Service**: AI provides suggestions and automation
3. **Transparency**: Always clear about capabilities and limitations
4. **Safety First**: Consent system prevents accidents
5. **User Respect**: Calm warnings, not panic
6. **Arabic First**: Native support for Arabic language

## Performance Considerations

- **Database**: SQLite for simplicity, can scale to PostgreSQL
- **API Calls**: Cached conversations reduce API usage
- **Memory**: Conversation history limited to recent messages
- **Async**: Async/await for non-blocking operations

## Future Enhancements

1. **More Integrations**: GitLab, AWS, Jira, etc.
2. **Advanced Search**: Full-text search with ranking
3. **Export/Import**: Workspace data backup
4. **Plugins**: Plugin system for extensions
5. **Web UI**: Optional web interface
6. **Voice Input**: Arabic voice recognition
7. **Collaboration**: Multi-user support
8. **Encryption**: Database encryption for sensitive data
