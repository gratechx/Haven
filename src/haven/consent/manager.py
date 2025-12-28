"""Consent system for dangerous actions"""
from enum import Enum
from typing import Optional, Callable, Any
from dataclasses import dataclass


class ActionRisk(Enum):
    """Risk levels for actions"""
    SAFE = "safe"  # No risk, proceed without asking
    LOW = "low"  # Minimal risk, quick confirmation
    MEDIUM = "medium"  # Moderate risk, clear warning
    HIGH = "high"  # High risk, explicit consent required
    CRITICAL = "critical"  # Critical risk, multiple confirmations


@dataclass
class Action:
    """Represents an action that may require consent"""
    name: str
    description: str
    risk_level: ActionRisk
    warning_ar: str  # Arabic warning
    warning_en: str  # English warning
    
    def get_warning(self, language: str = "ar") -> str:
        """Get warning in specified language"""
        return self.warning_ar if language == "ar" else self.warning_en


class ConsentManager:
    """
    Manages consent for potentially dangerous actions.
    Philosophy: Always ask before dangerous actions, use calm warnings.
    """
    
    # Predefined risky actions
    ACTIONS = {
        # GitHub actions
        "github_delete_repo": Action(
            name="github_delete_repo",
            description="Delete a GitHub repository",
            risk_level=ActionRisk.CRITICAL,
            warning_ar="⚠️ تحذير: هذا الإجراء سيحذف المستودع بشكل دائم. لا يمكن التراجع عن هذا الإجراء.",
            warning_en="⚠️ Warning: This will permanently delete the repository. This action cannot be undone."
        ),
        "github_force_push": Action(
            name="github_force_push",
            description="Force push to GitHub repository",
            risk_level=ActionRisk.HIGH,
            warning_ar="⚠️ تنبيه: الدفع القسري قد يحذف تاريخ الكود. يُنصح بأخذ نسخة احتياطية أولاً.",
            warning_en="⚠️ Notice: Force pushing may delete code history. Consider backing up first."
        ),
        "github_make_public": Action(
            name="github_make_public",
            description="Make repository public",
            risk_level=ActionRisk.MEDIUM,
            warning_ar="ℹ️ ملاحظة: سيصبح المستودع مرئياً للجميع. تأكد من عدم وجود بيانات حساسة.",
            warning_en="ℹ️ Note: The repository will be visible to everyone. Ensure no sensitive data is present."
        ),
        
        # Azure actions
        "azure_delete_resource": Action(
            name="azure_delete_resource",
            description="Delete Azure resource",
            risk_level=ActionRisk.HIGH,
            warning_ar="⚠️ تحذير: سيتم حذف المورد من Azure. قد يؤثر هذا على الخدمات المرتبطة.",
            warning_en="⚠️ Warning: This will delete the resource from Azure. This may affect connected services."
        ),
        "azure_modify_permissions": Action(
            name="azure_modify_permissions",
            description="Modify Azure resource permissions",
            risk_level=ActionRisk.MEDIUM,
            warning_ar="ℹ️ تنبيه: سيتم تعديل صلاحيات الوصول. تأكد من أنك تعرف ما تفعل.",
            warning_en="ℹ️ Notice: Access permissions will be modified. Make sure you know what you're doing."
        ),
        
        # File system actions
        "delete_file": Action(
            name="delete_file",
            description="Delete a file",
            risk_level=ActionRisk.LOW,
            warning_ar="ℹ️ سيتم حذف الملف. هل تريد المتابعة؟",
            warning_en="ℹ️ The file will be deleted. Do you want to continue?"
        ),
        "clear_history": Action(
            name="clear_history",
            description="Clear conversation history",
            risk_level=ActionRisk.LOW,
            warning_ar="ℹ️ سيتم حذف سجل المحادثات. لا يمكن استرجاعه.",
            warning_en="ℹ️ Conversation history will be cleared. This cannot be recovered."
        ),
    }
    
    def __init__(self, callback: Optional[Callable[[str, str], bool]] = None):
        """
        Initialize consent manager
        
        Args:
            callback: Function to call for user consent (prompt, language) -> bool
        """
        self.callback = callback
        self.auto_approve_safe = True  # Auto-approve safe actions
    
    def requires_consent(self, action_name: str) -> bool:
        """Check if action requires consent"""
        action = self.ACTIONS.get(action_name)
        if not action:
            return False  # Unknown actions are considered safe
        
        if self.auto_approve_safe and action.risk_level == ActionRisk.SAFE:
            return False
        
        return True
    
    def get_action_risk(self, action_name: str) -> ActionRisk:
        """Get risk level for an action"""
        action = self.ACTIONS.get(action_name)
        return action.risk_level if action else ActionRisk.SAFE
    
    def get_warning(self, action_name: str, language: str = "ar") -> str:
        """Get warning message for an action"""
        action = self.ACTIONS.get(action_name)
        if not action:
            return ""
        return action.get_warning(language)
    
    def request_consent(self, action_name: str, language: str = "ar") -> bool:
        """
        Request user consent for an action
        
        Args:
            action_name: Name of the action
            language: Language for warnings (ar/en)
            
        Returns:
            True if user consents, False otherwise
        """
        if not self.requires_consent(action_name):
            return True  # No consent needed
        
        warning = self.get_warning(action_name, language)
        
        if not self.callback:
            # No callback, default to denying
            return False
        
        # Get consent via callback
        return self.callback(warning, language)
    
    def register_action(self, action: Action):
        """Register a new action that may require consent"""
        self.ACTIONS[action.name] = action


# Helper function to create calm, non-panic warnings
def create_calm_warning(
    action: str,
    risk_level: ActionRisk,
    details_ar: str,
    details_en: str
) -> tuple[str, str]:
    """
    Create calm, helpful warning messages
    
    Returns:
        Tuple of (arabic_warning, english_warning)
    """
    icons = {
        ActionRisk.SAFE: "✓",
        ActionRisk.LOW: "ℹ️",
        ActionRisk.MEDIUM: "⚠️",
        ActionRisk.HIGH: "⚠️",
        ActionRisk.CRITICAL: "🛑"
    }
    
    icon = icons[risk_level]
    
    warning_ar = f"{icon} {details_ar}"
    warning_en = f"{icon} {details_en}"
    
    return warning_ar, warning_en
