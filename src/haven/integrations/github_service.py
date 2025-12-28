"""GitHub integration service"""
from typing import Optional, List, Dict
from github import Github, GithubException
from ..config import settings
from ..consent import ConsentManager


class GitHubService:
    """GitHub integration for repository management"""
    
    def __init__(self, consent_manager: Optional[ConsentManager] = None):
        """Initialize GitHub service"""
        if not settings.github_token:
            raise ValueError("GitHub token not configured")
        
        self.client = Github(settings.github_token)
        self.consent = consent_manager
        self.user = self.client.get_user()
    
    def get_user_info(self) -> Dict:
        """Get authenticated user information"""
        return {
            "login": self.user.login,
            "name": self.user.name,
            "email": self.user.email,
            "bio": self.user.bio,
            "public_repos": self.user.public_repos,
        }
    
    def list_repositories(self, limit: int = 10) -> List[Dict]:
        """List user repositories"""
        repos = self.user.get_repos()[:limit]
        return [
            {
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "private": repo.private,
                "url": repo.html_url,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
            }
            for repo in repos
        ]
    
    def get_repository(self, repo_name: str) -> Dict:
        """Get repository details"""
        try:
            repo = self.client.get_repo(repo_name)
            return {
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "private": repo.private,
                "url": repo.html_url,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "language": repo.language,
                "created_at": repo.created_at,
                "updated_at": repo.updated_at,
            }
        except GithubException as e:
            return {"error": str(e)}
    
    def create_repository(
        self, 
        name: str, 
        description: str = "", 
        private: bool = True
    ) -> Dict:
        """Create a new repository"""
        try:
            repo = self.user.create_repo(
                name=name,
                description=description,
                private=private
            )
            return {
                "success": True,
                "name": repo.name,
                "url": repo.html_url,
            }
        except GithubException as e:
            return {"success": False, "error": str(e)}
    
    def delete_repository(self, repo_name: str, language: str = "ar") -> Dict:
        """Delete a repository (requires consent)"""
        # Check consent
        if self.consent and not self.consent.request_consent("github_delete_repo", language):
            return {
                "success": False,
                "error": "User denied consent" if language == "en" else "رفض المستخدم الموافقة"
            }
        
        try:
            repo = self.client.get_repo(repo_name)
            repo.delete()
            return {"success": True}
        except GithubException as e:
            return {"success": False, "error": str(e)}
    
    def create_issue(
        self, 
        repo_name: str, 
        title: str, 
        body: str = ""
    ) -> Dict:
        """Create an issue in a repository"""
        try:
            repo = self.client.get_repo(repo_name)
            issue = repo.create_issue(title=title, body=body)
            return {
                "success": True,
                "number": issue.number,
                "url": issue.html_url,
            }
        except GithubException as e:
            return {"success": False, "error": str(e)}
    
    def list_issues(self, repo_name: str, state: str = "open") -> List[Dict]:
        """List issues in a repository"""
        try:
            repo = self.client.get_repo(repo_name)
            issues = repo.get_issues(state=state)[:20]
            return [
                {
                    "number": issue.number,
                    "title": issue.title,
                    "state": issue.state,
                    "url": issue.html_url,
                    "created_at": issue.created_at,
                }
                for issue in issues
            ]
        except GithubException as e:
            return [{"error": str(e)}]
