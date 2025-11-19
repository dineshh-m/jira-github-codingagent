#!/usr/bin/env python3
"""
Create a branch in the target repository and sync project context documentation.

This script:
1. Creates a new branch named after the Jira issue key
2. Pushes all docs from this agent repo's docs/ directory to the target branch
3. Sets environment variables for subsequent workflow steps

This ensures GitHub Copilot has full project context when working on the issue.
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import requests

# Configuration from environment variables
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
TARGET_REPO_OWNER = os.environ.get("TARGET_REPO_OWNER")
TARGET_REPO_NAME = os.environ.get("TARGET_REPO_NAME")
JIRA_ISSUE_KEY = os.environ.get("JIRA_ISSUE_KEY")
AGENT_REPO_PATH = os.environ.get("AGENT_REPO_PATH", ".")

# GitHub API configuration
GITHUB_API_BASE = "https://api.github.com"


def check_required_env_vars():
    """Validate that all required environment variables are set."""
    required_vars = {
        "GITHUB_TOKEN": GITHUB_TOKEN,
        "TARGET_REPO_OWNER": TARGET_REPO_OWNER,
        "TARGET_REPO_NAME": TARGET_REPO_NAME,
        "JIRA_ISSUE_KEY": JIRA_ISSUE_KEY,
    }
    
    missing = [var for var, value in required_vars.items() if not value]
    
    if missing:
        print(f"❌ Error: Missing required environment variables: {', '.join(missing)}")
        sys.exit(1)


def get_github_headers() -> Dict[str, str]:
    """Return headers for GitHub API requests."""
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def get_default_branch() -> str:
    """Get the default branch of the target repository."""
    url = f"{GITHUB_API_BASE}/repos/{TARGET_REPO_OWNER}/{TARGET_REPO_NAME}"
    
    try:
        response = requests.get(url, headers=get_github_headers(), timeout=10)
        response.raise_for_status()
        
        repo_data = response.json()
        default_branch = repo_data.get("default_branch", "main")
        print(f"✅ Default branch: {default_branch}")
        return default_branch
    
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Error fetching default branch: {e}")
        print("📍 Falling back to 'main'")
        return "main"


def get_branch_sha(branch_name: str) -> Optional[str]:
    """Get the SHA of the latest commit on a branch."""
    url = f"{GITHUB_API_BASE}/repos/{TARGET_REPO_OWNER}/{TARGET_REPO_NAME}/git/refs/heads/{branch_name}"
    
    try:
        response = requests.get(url, headers=get_github_headers(), timeout=10)
        response.raise_for_status()
        
        ref_data = response.json()
        sha = ref_data.get("object", {}).get("sha")
        return sha
    
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Branch {branch_name} not found or error: {e}")
        return None


def create_branch(branch_name: str, base_branch: str) -> bool:
    """
    Create a new branch in the target repository.
    
    Args:
        branch_name: Name of the new branch
        base_branch: Base branch to create from
        
    Returns:
        True if successful, False otherwise
    """
    print(f"🌿 Creating branch '{branch_name}' from '{base_branch}'...")
    
    # Check if branch already exists
    existing_sha = get_branch_sha(branch_name)
    if existing_sha:
        print(f"ℹ️  Branch '{branch_name}' already exists")
        return True
    
    # Get SHA of base branch
    base_sha = get_branch_sha(base_branch)
    if not base_sha:
        print(f"❌ Error: Could not get SHA for base branch '{base_branch}'")
        return False
    
    # Create new branch
    url = f"{GITHUB_API_BASE}/repos/{TARGET_REPO_OWNER}/{TARGET_REPO_NAME}/git/refs"
    
    data = {
        "ref": f"refs/heads/{branch_name}",
        "sha": base_sha
    }
    
    try:
        response = requests.post(url, headers=get_github_headers(), json=data, timeout=10)
        response.raise_for_status()
        
        print(f"✅ Branch '{branch_name}' created successfully")
        return True
    
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 422:
            print(f"ℹ️  Branch '{branch_name}' already exists (422 response)")
            return True
        else:
            print(f"❌ Error creating branch: {e}")
            print(f"Response: {e.response.text if hasattr(e, 'response') else 'N/A'}")
            return False
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error creating branch: {e}")
        return False


def get_file_content_from_repo(file_path: str, branch: str) -> Optional[Dict[str, Any]]:
    """Get file content and metadata from target repository."""
    url = f"{GITHUB_API_BASE}/repos/{TARGET_REPO_OWNER}/{TARGET_REPO_NAME}/contents/{file_path}"
    params = {"ref": branch}
    
    try:
        response = requests.get(url, headers=get_github_headers(), params=params, timeout=10)
        
        if response.status_code == 404:
            return None
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException:
        return None


def push_file_to_branch(local_file_path: Path, remote_path: str, branch_name: str) -> bool:
    """
    Push a single file from local path to the target repository branch.
    
    Args:
        local_file_path: Path to local file
        remote_path: Destination path in repository
        branch_name: Target branch name
        
    Returns:
        True if successful, False otherwise
    """
    # Read local file content
    try:
        with open(local_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file {local_file_path}: {e}")
        return False
    
    # Check if file exists in target repo to get SHA
    existing_file = get_file_content_from_repo(remote_path, branch_name)
    sha = existing_file.get("sha") if existing_file else None
    
    # Prepare API request
    url = f"{GITHUB_API_BASE}/repos/{TARGET_REPO_OWNER}/{TARGET_REPO_NAME}/contents/{remote_path}"
    
    import base64
    content_base64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    
    data = {
        "message": f"Sync project context: {remote_path} for {JIRA_ISSUE_KEY}",
        "content": content_base64,
        "branch": branch_name
    }
    
    if sha:
        data["sha"] = sha
        action = "Updating"
    else:
        action = "Creating"
    
    # Push file
    try:
        response = requests.put(url, headers=get_github_headers(), json=data, timeout=10)
        response.raise_for_status()
        
        print(f"   ✅ {action} {remote_path}")
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error pushing {remote_path}: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Response: {e.response.text[:200]}")
        return False


def sync_docs_to_branch(branch_name: str) -> int:
    """
    Sync all documentation files from agent repo to target repo branch.
    
    Args:
        branch_name: Target branch to sync to
        
    Returns:
        Number of files successfully synced
    """
    print(f"📁 Syncing documentation to branch '{branch_name}'...")
    
    docs_dir = Path(AGENT_REPO_PATH) / "docs"
    
    if not docs_dir.exists():
        print(f"❌ Error: docs directory not found at {docs_dir}")
        return 0
    
    # Find all markdown files recursively
    md_files = list(docs_dir.rglob("*.md"))
    
    if not md_files:
        print("⚠️  No markdown files found in docs directory")
        return 0
    
    print(f"📄 Found {len(md_files)} documentation files to sync")
    
    success_count = 0
    
    for local_file in md_files:
        # Calculate relative path from docs directory
        relative_path = local_file.relative_to(docs_dir)
        
        # Remote path maintains docs/ prefix
        remote_path = f"docs/{relative_path}".replace(os.sep, '/')
        
        if push_file_to_branch(local_file, remote_path, branch_name):
            success_count += 1
    
    print(f"✅ Successfully synced {success_count}/{len(md_files)} files")
    return success_count


def set_github_env(name: str, value: str):
    """Set environment variable for subsequent GitHub Actions steps."""
    github_env = os.environ.get('GITHUB_ENV')
    if github_env:
        with open(github_env, 'a') as f:
            f.write(f"{name}={value}\n")
        print(f"🔧 Set environment variable: {name}={value}")


def main():
    """Main execution flow."""
    print("🚀 Starting context sync workflow...")
    print(f"📍 Target Repository: {TARGET_REPO_OWNER}/{TARGET_REPO_NAME}")
    print(f"📝 Jira Issue: {JIRA_ISSUE_KEY}")
    
    # Validate environment variables
    check_required_env_vars()
    
    # Determine branch name
    # Use Jira key to create a safe branch name
    branch_name = f"jira/{JIRA_ISSUE_KEY.lower()}"
    print(f"🌿 Target branch: {branch_name}")
    
    # Get default branch
    default_branch = get_default_branch()
    
    # Create branch
    if not create_branch(branch_name, default_branch):
        print("❌ Failed to create branch")
        sys.exit(1)
    
    # Sync documentation files
    synced_count = sync_docs_to_branch(branch_name)
    
    if synced_count == 0:
        print("❌ No files were synced")
        sys.exit(1)
    
    # Set environment variable for subsequent steps
    set_github_env("CONTEXT_BRANCH", branch_name)
    
    print(f"\n✅ Successfully synced {synced_count} context files to branch '{branch_name}'")
    print(f"🎯 Next: Create issue and assign to Copilot with branch context")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
