"""Core AI engine with Arabic language support"""
from typing import List, Dict, Optional
from enum import Enum
import openai
import anthropic
from .config import settings


class AIProvider(Enum):
    """Supported AI providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class AIEngine:
    """Core AI engine that understands Arabic and English"""
    
    def __init__(self):
        self.provider = AIProvider(settings.ai_provider)
        self._setup_client()
    
    def _setup_client(self):
        """Setup the appropriate AI client"""
        if self.provider == AIProvider.OPENAI:
            if not settings.openai_api_key:
                raise ValueError("OpenAI API key not configured")
            self.client = openai.OpenAI(api_key=settings.openai_api_key)
        elif self.provider == AIProvider.ANTHROPIC:
            if not settings.anthropic_api_key:
                raise ValueError("Anthropic API key not configured")
            self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    
    async def generate_response(
        self, 
        messages: List[Dict[str, str]], 
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate AI response with Arabic support
        
        Args:
            messages: Conversation history
            system_prompt: Optional system prompt
            
        Returns:
            AI-generated response
        """
        if self.provider == AIProvider.OPENAI:
            return await self._generate_openai(messages, system_prompt)
        elif self.provider == AIProvider.ANTHROPIC:
            return await self._generate_anthropic(messages, system_prompt)
    
    async def _generate_openai(
        self, 
        messages: List[Dict[str, str]], 
        system_prompt: Optional[str]
    ) -> str:
        """Generate response using OpenAI"""
        formatted_messages = []
        
        if system_prompt:
            formatted_messages.append({"role": "system", "content": system_prompt})
        
        formatted_messages.extend(messages)
        
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=formatted_messages,
            temperature=0.7,
        )
        
        return response.choices[0].message.content
    
    async def _generate_anthropic(
        self, 
        messages: List[Dict[str, str]], 
        system_prompt: Optional[str]
    ) -> str:
        """Generate response using Anthropic Claude"""
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            system=system_prompt or "",
            messages=messages,
        )
        
        return response.content[0].text
    
    def detect_language(self, text: str) -> str:
        """
        Detect if text is Arabic or English
        
        Args:
            text: Input text
            
        Returns:
            'ar' for Arabic, 'en' for English
        """
        # Simple detection: check for Arabic Unicode range
        arabic_chars = sum(1 for char in text if '\u0600' <= char <= '\u06FF')
        if arabic_chars > len(text) * 0.3:  # More than 30% Arabic characters
            return 'ar'
        return 'en'


# Default system prompt with Arabic support
DEFAULT_SYSTEM_PROMPT = """أنت Haven، مساعد ذكي ودود يخدم المستخدم.

You are Haven, a friendly and helpful AI assistant serving the user.

Philosophy: "The human commands, the AI serves"

Core principles:
- Always be respectful and serve the human's needs
- Support both Arabic and English naturally
- Ask for consent before any dangerous actions
- Provide calm, helpful warnings (not panic-inducing)
- Be transparent about capabilities and limitations
- Remember user preferences and context

You have access to:
- GitHub integration for repository management
- Azure integration for cloud resources
- Workspace for notes and tasks
- Memory system to remember user preferences

Always respond in the same language the user uses, or in Arabic by default.
"""
