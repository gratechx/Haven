"""Azure integration service"""
from typing import Optional, List, Dict
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from ..config import settings
from ..consent import ConsentManager


class AzureService:
    """Azure integration for cloud resource management"""
    
    def __init__(self, consent_manager: Optional[ConsentManager] = None):
        """Initialize Azure service"""
        if not all([
            settings.azure_tenant_id,
            settings.azure_client_id,
            settings.azure_client_secret,
            settings.azure_subscription_id
        ]):
            raise ValueError("Azure credentials not fully configured")
        
        self.credential = ClientSecretCredential(
            tenant_id=settings.azure_tenant_id,
            client_id=settings.azure_client_id,
            client_secret=settings.azure_client_secret
        )
        
        self.subscription_id = settings.azure_subscription_id
        self.consent = consent_manager
        
        self.resource_client = ResourceManagementClient(
            self.credential,
            self.subscription_id
        )
    
    def list_resource_groups(self) -> List[Dict]:
        """List resource groups"""
        try:
            groups = self.resource_client.resource_groups.list()
            return [
                {
                    "name": group.name,
                    "location": group.location,
                    "tags": group.tags or {},
                }
                for group in groups
            ]
        except Exception as e:
            return [{"error": str(e)}]
    
    def list_resources(self, resource_group: Optional[str] = None) -> List[Dict]:
        """List resources in a resource group or subscription"""
        try:
            if resource_group:
                resources = self.resource_client.resources.list_by_resource_group(
                    resource_group
                )
            else:
                resources = self.resource_client.resources.list()
            
            return [
                {
                    "name": resource.name,
                    "type": resource.type,
                    "location": resource.location,
                    "resource_group": resource_group or "N/A",
                }
                for resource in list(resources)[:50]  # Limit to 50
            ]
        except Exception as e:
            return [{"error": str(e)}]
    
    def create_resource_group(
        self, 
        name: str, 
        location: str = "eastus"
    ) -> Dict:
        """Create a resource group"""
        try:
            result = self.resource_client.resource_groups.create_or_update(
                name,
                {"location": location}
            )
            return {
                "success": True,
                "name": result.name,
                "location": result.location,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def delete_resource_group(self, name: str, language: str = "ar") -> Dict:
        """Delete a resource group (requires consent)"""
        # Check consent
        if self.consent and not self.consent.request_consent("azure_delete_resource", language):
            return {
                "success": False,
                "error": "User denied consent" if language == "en" else "رفض المستخدم الموافقة"
            }
        
        try:
            # This is async operation in Azure
            poller = self.resource_client.resource_groups.begin_delete(name)
            return {
                "success": True,
                "message": "Deletion started" if language == "en" else "بدأ الحذف"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_subscription_info(self) -> Dict:
        """Get subscription information"""
        try:
            from azure.mgmt.subscription import SubscriptionClient
            sub_client = SubscriptionClient(self.credential)
            sub = sub_client.subscriptions.get(self.subscription_id)
            return {
                "subscription_id": sub.subscription_id,
                "display_name": sub.display_name,
                "state": sub.state,
            }
        except Exception as e:
            return {"error": str(e)}
