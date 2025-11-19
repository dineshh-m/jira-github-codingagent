#!/usr/bin/env python3
"""
Create GitHub issue with enhanced context for Copilot agent.

This script creates a GitHub issue that references:
- Jira ticket details
- The context branch with project documentation
- Instructions for Copilot to read the project context
"""

import os
import sys
from typing import Optional, Dict, Any
import requests

# Configuration from environment variables
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
TARGET_REPO_OWNER = os.environ.get("TARGET_REPO_OWNER")
TARGET_REPO_NAME = os.environ.get("TARGET_REPO_NAME")
JIRA_ISSUE_KEY = os.environ.get("JIRA_ISSUE_KEY")
JIRA_SUMMARY = os.environ.get("JIRA_SUMMARY", "")
JIRA_DESCRIPTION = os.environ.get("JIRA_DESCRIPTION", "")
JIRA_ISSUE_URL = os.environ.get("JIRA_ISSUE_URL", "")
JIRA_PRIORITY = os.environ.get("JIRA_PRIORITY", "Medium")
JIRA_ISSUE_TYPE = os.environ.get("JIRA_ISSUE_TYPE", "Task")
CONTEXT_BRANCH = os.environ.get("CONTEXT_BRANCH", "")

# GitHub API configuration
GITHUB_API_BASE = "https://api.github.com"


def check_required_env_vars():
    """Validate that all required environment variables are set."""
    required_vars = {
        "GITHUB_TOKEN": GITHUB_TOKEN,
        "TARGET_REPO_OWNER": TARGET_REPO_OWNER,
        "TARGET_REPO_NAME": TARGET_REPO_NAME,
        "JIRA_ISSUE_KEY": JIRA_ISSUE_KEY,
        "CONTEXT_BRANCH": CONTEXT_BRANCH,
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


def search_existing_issue(jira_key: str) -> Optional[Dict[str, Any]]:
    """
    Search for existing OPEN GitHub issues containing the Jira key.
    Returns the first matching OPEN issue or None if not found.
    """
    print(f"🔍 Searching for existing OPEN issues with key: {jira_key}")
    
    search_url = f"{GITHUB_API_BASE}/search/issues"
    search_query = f"repo:{TARGET_REPO_OWNER}/{TARGET_REPO_NAME} {jira_key} in:title,body type:issue state:open"
    
    params = {"q": search_query, "per_page": 1}
    
    try:
        response = requests.get(search_url, headers=get_github_headers(), params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("total_count", 0) > 0:
            issue = data["items"][0]
            print(f"   Found open issue: #{issue.get('number')}")
            return issue
        
        print("   No open issues found")
        return None
    
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Warning: Failed to search for existing issues: {e}")
        return None


def create_copilot_optimized_issue_body() -> str:
    """
    Create a structured issue body optimized for GitHub Copilot coding agent.
    
    Includes:
    - Clear instructions to work on the context branch
    - References to project documentation
    - Jira ticket requirements
    - Acceptance criteria
    """
    description = JIRA_DESCRIPTION.strip() if JIRA_DESCRIPTION else "No description provided."
    
    issue_body = f"""## 🤖 Instructions for @copilot

**IMPORTANT:** This issue has full project context available. Please:

1. **Switch to branch:** `{CONTEXT_BRANCH}`
2. **Read the project documentation** in the `docs/` directory:
   - `docs/architecture/overview.md` - System architecture and tech stack
   - `docs/api-standards/` - API naming conventions and CRUD specifications
   - `docs/laravel/` - Laravel patterns, database access, error handling, testing
   - `docs/react/` - React component structure, state management, API consumption, testing
3. **Follow the established patterns** defined in the documentation
4. **Implement the requirements** described below

---

## 📋 Requirements

{description}

## ✅ Acceptance Criteria

- [ ] Implementation follows patterns defined in project documentation
- [ ] Code adheres to naming conventions and API standards from `docs/api-standards/`
- [ ] Laravel code follows patterns from `docs/laravel/core-patterns.md`
- [ ] React components follow structure from `docs/react/component-structure.md`
- [ ] Tests are added following `docs/laravel/unit-testing-standards.md` or `docs/react/testing-library-patterns.md`
- [ ] Error handling follows `docs/laravel/error-handling.md`
- [ ] All changes are made on branch `{CONTEXT_BRANCH}`

## 🔗 Jira Reference

**Jira Issue:** [{JIRA_ISSUE_KEY}]({JIRA_ISSUE_URL})  
**Priority:** {JIRA_PRIORITY}  
**Type:** {JIRA_ISSUE_TYPE}

## 📚 Project Context

This repository follows strict coding standards. All patterns, conventions, and architectural decisions are documented in the `docs/` directory of the **`{CONTEXT_BRANCH}`** branch.

**Before implementing, please read:**
- Architecture overview for system understanding
- API standards for endpoint and naming conventions  
- Laravel patterns for backend implementation
- React patterns for frontend implementation
- Testing standards for test coverage

---

*This issue was automatically created from Jira with full project context.*
"""
    
    return issue_body


def create_github_issue() -> Dict[str, Any]:
    """
    Create a new GitHub issue with context branch reference.
    
    Returns:
        Dict containing the created issue data
    """
    title = f"[{JIRA_ISSUE_KEY}] {JIRA_SUMMARY}"
    body = create_copilot_optimized_issue_body()
    label_names = [
        "jira-sync",
        "copilot-ready",
        f"priority-{JIRA_PRIORITY.lower()}",
        "has-context"
    ]
    
    print(f"📝 Creating issue in {TARGET_REPO_OWNER}/{TARGET_REPO_NAME}")
    print(f"   Title: {title}")
    print(f"   Context Branch: {CONTEXT_BRANCH}")
    
    create_url = f"{GITHUB_API_BASE}/repos/{TARGET_REPO_OWNER}/{TARGET_REPO_NAME}/issues"
    
    issue_data = {
        "title": title,
        "body": body,
        "labels": label_names,
    }
    
    try:
        response = requests.post(
            create_url,
            headers=get_github_headers(),
            json=issue_data,
            timeout=10
        )
        response.raise_for_status()
        
        issue = response.json()
        print(f"✅ Issue #{issue['number']} created successfully")
        return issue
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error creating GitHub issue: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        sys.exit(1)


def set_github_env(name: str, value: str):
    """Set environment variable for subsequent GitHub Actions steps."""
    github_env = os.environ.get('GITHUB_ENV')
    if github_env:
        with open(github_env, 'a') as f:
            f.write(f"{name}={value}\n")
        print(f"🔧 Set environment variable: {name}={value}")


def main():
    """Main execution flow."""
    print("🚀 Starting issue creation with context...")
    print(f"📍 Target Repository: {TARGET_REPO_OWNER}/{TARGET_REPO_NAME}")
    print(f"📝 Jira Issue: {JIRA_ISSUE_KEY}")
    print(f"🌿 Context Branch: {CONTEXT_BRANCH}")
    
    # Validate environment variables
    check_required_env_vars()
    
    # Check for existing OPEN issue with this Jira key
    existing_issue = search_existing_issue(JIRA_ISSUE_KEY)
    
    if existing_issue:
        issue_number = existing_issue.get("number")
        issue_url = existing_issue.get("html_url")
        print(f"ℹ️  Open issue already exists: #{issue_number}")
        print(f"🔗 URL: {issue_url}")
        print("✅ Skipping creation - will use existing issue")
        
        # Set issue number for next step
        set_github_env("ISSUE_NUMBER", str(issue_number))
        return
    
    # Create new issue
    print("✨ No existing issue found, creating new issue...")
    issue = create_github_issue()
    
    issue_number = issue.get("number")
    issue_url = issue.get("html_url")
    
    print(f"\n✅ Successfully created issue #{issue_number}")
    print(f"🔗 URL: {issue_url}")
    print(f"🌿 Context available on branch: {CONTEXT_BRANCH}")
    
    # Set issue number for next step (Copilot assignment)
    set_github_env("ISSUE_NUMBER", str(issue_number))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
