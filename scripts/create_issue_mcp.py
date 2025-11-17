#!/usr/bin/env python3
"""
Create GitHub issue from Jira ticket via MCP GitHub server and assign to Copilot.
Prevents duplicate issues by checking for existing Jira key references.
Uses MCP to connect to target repositories from this centralized agent repo.
"""

import os
import sys
import json
from typing import Optional, Dict, Any

# Configuration from environment variables
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
TARGET_REPO_OWNER = os.environ.get("TARGET_REPO_OWNER", "Karthi-Knackforge")
TARGET_REPO_NAME = os.environ.get("TARGET_REPO_NAME", "cms-project")
JIRA_ISSUE_KEY = os.environ.get("JIRA_ISSUE_KEY")
JIRA_SUMMARY = os.environ.get("JIRA_SUMMARY", "")
JIRA_DESCRIPTION = os.environ.get("JIRA_DESCRIPTION", "")
JIRA_ISSUE_URL = os.environ.get("JIRA_ISSUE_URL", "")
JIRA_PRIORITY = os.environ.get("JIRA_PRIORITY", "Medium")
JIRA_ISSUE_TYPE = os.environ.get("JIRA_ISSUE_TYPE", "Task")

# GitHub Copilot coding agent username
GITHUB_COPILOT_USERNAME = "github"


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


def create_copilot_optimized_issue_body() -> str:
    """
    Create a structured issue body optimized for GitHub Copilot coding agent.
    
    Uses clear sections that help Copilot understand:
    - What needs to be done (Requirements)
    - How to verify completion (Acceptance Criteria)
    - Where to find more info (Jira Link)
    """
    # Clean and format the description
    description = JIRA_DESCRIPTION.strip() if JIRA_DESCRIPTION else "No description provided."
    
    # Build structured issue body
    issue_body = f"""## 📋 Requirements

{description}

## ✅ Acceptance Criteria

- [ ] Implementation matches the requirements described above
- [ ] Code follows project conventions and best practices
- [ ] Tests are added/updated to cover changes
- [ ] Documentation is updated if needed

## 🔗 Jira Reference

**Jira Issue:** [{JIRA_ISSUE_KEY}]({JIRA_ISSUE_URL})
**Priority:** {JIRA_PRIORITY}
**Type:** {JIRA_ISSUE_TYPE}

---

*This issue was automatically created from Jira and assigned to GitHub Copilot coding agent for implementation.*
"""
    
    return issue_body


def search_existing_issue_via_mcp(jira_key: str) -> Optional[Dict[str, Any]]:
    """
    Search for existing GitHub issues containing the Jira key via MCP.
    Uses the MCP GitHub search_issues tool.
    
    Returns the first matching issue or None if not found.
    """
    print(f"🔍 Searching for existing issues with key: {jira_key} in {TARGET_REPO_OWNER}/{TARGET_REPO_NAME}")
    
    # MCP GitHub search query
    search_query = f"repo:{TARGET_REPO_OWNER}/{TARGET_REPO_NAME} {jira_key} in:title,body is:issue"
    
    # Call MCP GitHub search tool
    try:
        # Import MCP client
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
        
        # Connect to MCP GitHub server
        server_params = StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-github"],
            env={
                **os.environ,
                "GITHUB_PERSONAL_ACCESS_TOKEN": GITHUB_TOKEN,
            }
        )
        
        async def search_issues():
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    # Call search_issues tool
                    result = await session.call_tool(
                        "search_issues",
                        arguments={
                            "query": search_query,
                            "perPage": 1
                        }
                    )
                    
                    return result
        
        # Run async search
        import asyncio
        result = asyncio.run(search_issues())
        
        # Parse result
        if result and result.content:
            content = result.content[0].text if result.content else "{}"
            data = json.loads(content)
            
            if data.get("total_count", 0) > 0 and data.get("items"):
                return data["items"][0]
        
        return None
    
    except Exception as e:
        print(f"⚠️  Warning: MCP search failed, falling back to direct API: {e}")
        # Fallback to direct API if MCP fails
        import requests
        
        search_url = "https://api.github.com/search/issues"
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        params = {"q": search_query, "per_page": 1}
        
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data.get("total_count", 0) > 0:
            return data["items"][0]
        
        return None


def create_github_issue_via_mcp() -> Dict[str, Any]:
    """
    Create a new GitHub issue via MCP GitHub server.
    Uses the mcp_github_github_issue_write tool with method='create'.
    
    Returns:
        Dict containing the created issue data
    """
    # Create issue title with Jira key
    title = f"[{JIRA_ISSUE_KEY}] {JIRA_SUMMARY}"
    body = create_copilot_optimized_issue_body()
    
    print(f"📝 Creating issue in {TARGET_REPO_OWNER}/{TARGET_REPO_NAME}")
    print(f"   Title: {title}")
    
    try:
        # Import MCP client
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
        
        # Connect to MCP GitHub server
        server_params = StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-github"],
            env={
                **os.environ,
                "GITHUB_PERSONAL_ACCESS_TOKEN": GITHUB_TOKEN,
            }
        )
        
        async def create_issue():
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    # Call issue_write tool to create issue
                    result = await session.call_tool(
                        "github_issue_write",
                        arguments={
                            "method": "create",
                            "owner": TARGET_REPO_OWNER,
                            "repo": TARGET_REPO_NAME,
                            "title": title,
                            "body": body,
                            "labels": ["jira-sync", "copilot-agent", f"priority-{JIRA_PRIORITY.lower()}"],
                            "assignees": [GITHUB_COPILOT_USERNAME],
                        }
                    )
                    
                    return result
        
        # Run async creation
        import asyncio
        result = asyncio.run(create_issue())
        
        # Parse result
        if result and result.content:
            content = result.content[0].text if result.content else "{}"
            issue = json.loads(content)
            return issue
        
        raise Exception("MCP returned no content")
    
    except Exception as e:
        print(f"⚠️  Warning: MCP creation failed, falling back to direct API: {e}")
        # Fallback to direct API if MCP fails
        import requests
        
        create_url = f"https://api.github.com/repos/{TARGET_REPO_OWNER}/{TARGET_REPO_NAME}/issues"
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        issue_data = {
            "title": title,
            "body": body,
            "labels": ["jira-sync", "copilot-agent", f"priority-{JIRA_PRIORITY.lower()}"],
            "assignees": [GITHUB_COPILOT_USERNAME],
        }
        
        response = requests.post(create_url, headers=headers, json=issue_data)
        response.raise_for_status()
        
        return response.json()


def main():
    """Main execution flow."""
    print("🚀 Starting Jira to GitHub Issue workflow via MCP...")
    print(f"📍 Target Repository: {TARGET_REPO_OWNER}/{TARGET_REPO_NAME}")
    print(f"📝 Jira Issue: {JIRA_ISSUE_KEY}")
    
    # Validate environment variables
    check_required_env_vars()
    
    # Check for existing issue with this Jira key
    existing_issue = search_existing_issue_via_mcp(JIRA_ISSUE_KEY)
    
    if existing_issue:
        issue_number = existing_issue.get("number")
        issue_url = existing_issue.get("html_url")
        print(f"ℹ️  Issue already exists: #{issue_number}")
        print(f"🔗 URL: {issue_url}")
        print(f"✅ Skipping creation - no duplicate will be created")
        return
    
    # Create new issue via MCP
    print(f"✨ No existing issue found, creating new issue...")
    issue = create_github_issue_via_mcp()
    
    issue_number = issue.get("number")
    issue_url = issue.get("html_url")
    
    print(f"✅ Successfully created issue #{issue_number}")
    print(f"🔗 URL: {issue_url}")
    print(f"🤖 Assigned to: @{GITHUB_COPILOT_USERNAME} (GitHub Copilot coding agent)")
    print(f"🏷️  Labels: {', '.join(issue.get('labels', []))}")
    
    # Output for GitHub Actions summary
    print(f"\n::notice title=Issue Created::Created issue #{issue_number} in {TARGET_REPO_OWNER}/{TARGET_REPO_NAME}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
