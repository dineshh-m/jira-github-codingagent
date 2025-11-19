#!/usr/bin/env python3
"""
Assign GitHub issue to Copilot coding agent with context instructions.

This script:
1. Assigns the issue to @copilot (or copilot-swe-agent)
2. Adds a comment with specific instructions about the context branch
3. Uses GitHub's official API to trigger Copilot agent
"""

import os
import sys
from typing import Optional, Dict, Any
import requests

# Configuration from environment variables
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
TARGET_REPO_OWNER = os.environ.get("TARGET_REPO_OWNER")
TARGET_REPO_NAME = os.environ.get("TARGET_REPO_NAME")
ISSUE_NUMBER = os.environ.get("ISSUE_NUMBER")
CONTEXT_BRANCH = os.environ.get("CONTEXT_BRANCH")

# GitHub API configuration
GITHUB_API_BASE = "https://api.github.com"


def check_required_env_vars():
    """Validate that all required environment variables are set."""
    required_vars = {
        "GITHUB_TOKEN": GITHUB_TOKEN,
        "TARGET_REPO_OWNER": TARGET_REPO_OWNER,
        "TARGET_REPO_NAME": TARGET_REPO_NAME,
        "ISSUE_NUMBER": ISSUE_NUMBER,
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


def assign_copilot_to_issue() -> bool:
    """
    Assign GitHub Copilot coding agent to the issue.
    
    Tries multiple methods:
    1. GitHub's official assign_copilot_to_issue API
    2. GraphQL mutation with copilot-swe-agent
    3. REST API with Copilot username
    
    Returns:
        True if successful, False otherwise
    """
    issue_num = int(ISSUE_NUMBER)
    
    print(f"🤖 Assigning Copilot to issue #{issue_num}...")
    
    # Method 1: Try official GitHub Copilot assignment API (if available)
    try:
        assign_url = f"{GITHUB_API_BASE}/repos/{TARGET_REPO_OWNER}/{TARGET_REPO_NAME}/issues/{issue_num}/assignees"
        
        # Try with copilot-swe-agent first (official agent username)
        response = requests.post(
            assign_url,
            headers=get_github_headers(),
            json={"assignees": ["copilot-swe-agent"]},
            timeout=10
        )
        
        if response.status_code == 201:
            print("✅ Assigned via copilot-swe-agent")
            return True
        
        # Fallback to "Copilot" username
        response = requests.post(
            assign_url,
            headers=get_github_headers(),
            json={"assignees": ["Copilot"]},
            timeout=10
        )
        
        if response.status_code == 201:
            print("✅ Assigned via Copilot username")
            return True
        
        print(f"⚠️  Assignment returned status {response.status_code}")
        
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Error assigning Copilot: {e}")
    
    # Method 2: Try GraphQL approach
    try:
        print("🔄 Trying GraphQL assignment method...")
        copilot_id = get_copilot_agent_id()
        
        if copilot_id:
            issue_node_id = get_issue_node_id(issue_num)
            
            if issue_node_id:
                if assign_via_graphql(issue_node_id, copilot_id):
                    print("✅ Assigned via GraphQL")
                    return True
    
    except Exception as e:
        print(f"⚠️  GraphQL assignment failed: {e}")
    
    print("⚠️  Automatic assignment unsuccessful")
    print("💡 Copilot may need to be manually assigned or mentioned in a comment")
    return False


def get_copilot_agent_id() -> Optional[str]:
    """Get the Copilot coding agent's GraphQL node ID."""
    graphql_url = f"{GITHUB_API_BASE}/graphql"
    
    query = """
    query($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) {
        suggestedActors(capabilities: [CAN_BE_ASSIGNED], first: 100) {
          nodes {
            login
            __typename
            ... on Bot {
              id
            }
          }
        }
      }
    }
    """
    
    variables = {
        "owner": TARGET_REPO_OWNER,
        "name": TARGET_REPO_NAME
    }
    
    try:
        response = requests.post(
            graphql_url,
            headers=get_github_headers(),
            json={"query": query, "variables": variables},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            actors = data.get("data", {}).get("repository", {}).get("suggestedActors", {}).get("nodes", [])
            
            for actor in actors:
                if actor.get("login") == "copilot-swe-agent":
                    return actor.get("id")
        
    except Exception as e:
        print(f"⚠️  Error getting Copilot ID: {e}")
    
    return None


def get_issue_node_id(issue_num: int) -> Optional[str]:
    """Get the issue's GraphQL node ID."""
    url = f"{GITHUB_API_BASE}/repos/{TARGET_REPO_OWNER}/{TARGET_REPO_NAME}/issues/{issue_num}"
    
    try:
        response = requests.get(url, headers=get_github_headers(), timeout=10)
        
        if response.status_code == 200:
            issue_data = response.json()
            return issue_data.get("node_id")
    
    except Exception as e:
        print(f"⚠️  Error getting issue node ID: {e}")
    
    return None


def assign_via_graphql(issue_node_id: str, copilot_id: str) -> bool:
    """Assign Copilot using GraphQL mutation."""
    graphql_url = f"{GITHUB_API_BASE}/graphql"
    
    mutation = """
    mutation($issueId: ID!, $assigneeIds: [ID!]!) {
      addAssigneesToAssignable(input: {assignableId: $issueId, assigneeIds: $assigneeIds}) {
        assignable {
          ... on Issue {
            number
            assignees(first: 10) {
              nodes {
                login
              }
            }
          }
        }
      }
    }
    """
    
    variables = {
        "issueId": issue_node_id,
        "assigneeIds": [copilot_id]
    }
    
    try:
        response = requests.post(
            graphql_url,
            headers=get_github_headers(),
            json={"query": mutation, "variables": variables},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if "errors" not in result:
                return True
    
    except Exception as e:
        print(f"⚠️  GraphQL mutation error: {e}")
    
    return False


def add_copilot_instructions_comment() -> bool:
    """
    Add a comment to the issue with clear instructions for Copilot.
    
    This ensures Copilot knows about the context branch and documentation.
    
    Returns:
        True if successful, False otherwise
    """
    issue_num = int(ISSUE_NUMBER)
    
    print(f"💬 Adding instructions comment to issue #{issue_num}...")
    
    comment_body = f"""## 🤖 @copilot - Implementation Instructions

Hi @copilot! Please work on this issue following these steps:

### 1️⃣ Switch to Context Branch
```bash
git checkout {CONTEXT_BRANCH}
```

### 2️⃣ Read Project Documentation
Before implementing, please review the project standards in the `docs/` directory:

**Architecture & Standards:**
- `docs/architecture/overview.md` - System architecture, tech stack, patterns
- `docs/api-standards/naming-conventions.md` - Naming conventions for APIs, URLs, fields
- `docs/api-standards/crud-api-spec.md` - CRUD API specification with examples

**Laravel Backend:**
- `docs/laravel/core-patterns.md` - MVC patterns, controllers, models
- `docs/laravel/database-access-layer.md` - Eloquent ORM, queries, migrations
- `docs/laravel/error-handling.md` - Error handling patterns
- `docs/laravel/unit-testing-standards.md` - PHPUnit testing patterns

**React Frontend:**
- `docs/react/component-structure.md` - Component organization and patterns
- `docs/react/state-management.md` - React Query, Context API, state patterns
- `docs/react/api-consumption.md` - Service layer, Axios configuration
- `docs/react/testing-library-patterns.md` - React Testing Library patterns

### 3️⃣ Implementation Guidelines
- ✅ Follow the established patterns from the documentation
- ✅ Adhere to naming conventions
- ✅ Use the specified error handling approach
- ✅ Write tests following the testing standards
- ✅ Make all changes on the `{CONTEXT_BRANCH}` branch

### 4️⃣ Create Pull Request
Once implementation is complete, create a PR from `{CONTEXT_BRANCH}` to the default branch.

---

**Note:** All project coding standards are defined in the documentation above. Please ensure your implementation strictly follows these patterns.
"""
    
    comment_url = f"{GITHUB_API_BASE}/repos/{TARGET_REPO_OWNER}/{TARGET_REPO_NAME}/issues/{issue_num}/comments"
    
    try:
        response = requests.post(
            comment_url,
            headers=get_github_headers(),
            json={"body": comment_body},
            timeout=10
        )
        response.raise_for_status()
        
        print("✅ Instructions comment added successfully")
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error adding comment: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text[:200]}")
        return False


def main():
    """Main execution flow."""
    print("🚀 Starting Copilot assignment with context...")
    print(f"📍 Target Repository: {TARGET_REPO_OWNER}/{TARGET_REPO_NAME}")
    print(f"🎫 Issue Number: #{ISSUE_NUMBER}")
    print(f"🌿 Context Branch: {CONTEXT_BRANCH}")
    
    # Validate environment variables
    check_required_env_vars()
    
    # Try to assign Copilot to the issue
    assignment_successful = assign_copilot_to_issue()
    
    # Add instructions comment (whether assignment succeeded or not)
    comment_added = add_copilot_instructions_comment()
    
    if assignment_successful and comment_added:
        print(f"\n✅ Successfully assigned @copilot to issue #{ISSUE_NUMBER}")
        print(f"📚 Instructions added with full project context")
        print(f"🌿 Copilot will work on branch: {CONTEXT_BRANCH}")
    elif comment_added:
        print(f"\n⚠️  Issue created with instructions, but automatic assignment may have failed")
        print(f"💡 Please manually assign @copilot to issue #{ISSUE_NUMBER}")
        print(f"🔗 URL: https://github.com/{TARGET_REPO_OWNER}/{TARGET_REPO_NAME}/issues/{ISSUE_NUMBER}")
    else:
        print(f"\n❌ Failed to complete setup")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
