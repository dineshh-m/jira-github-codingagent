# Jira to GitHub Copilot Agent 🤖

Automated workflow to create GitHub issues from Jira tickets and assign them to GitHub Copilot with **full project context**.

## ✅ What's Implemented

Your **centralized agent repository** with **full project context** is ready:

```
Jira Ticket → Agent Repo → Branch + Docs Sync → GitHub Issue → Copilot Agent
```

### 🎯 Two Workflows Available

| Feature | Basic Workflow | Enhanced Workflow ⭐ |
|---------|----------------|---------------------|
| **Creates GitHub Issue** | ✅ | ✅ |
| **Assigns to Copilot** | ✅ | ✅ |
| **Creates Context Branch** | ❌ | ✅ |
| **Syncs Project Docs** | ❌ | ✅ |
| **Provides Standards** | ❌ | ✅ |
| **Copilot Instructions** | Basic | Detailed |

## 🚀 Quick Start

### 1. Configure GitHub Secret
```
Repository: jira-github-codingagent
Settings → Secrets → Actions
Secret: GB_TOKEN = <Your GitHub PAT with repo + workflow scopes>
```

### 2. Create Jira Automation Rule
**Trigger:** Issue labeled with `Auto-Copilot-[ProjectName]`  
**Action:** Send webhook to GitHub

**Enhanced Workflow (Recommended):**
```json
{
  "event_type": "jira-to-copilot-with-context",
  "client_payload": {
    "target_owner": "Karthi-Knackforge",
    "target_repo": "cms-project",
    "jira_key": "{{issue.key}}",
    "summary": "{{issue.summary}}",
    "description": "{{issue.description}}",
    "url": "{{issue.url}}",
    "priority": "{{issue.priority.name}}",
    "issue_type": "{{issue.type.name}}"
  }
}
```

### 3. Test It
1. Add label `Auto-Copilot-CMS` to a Jira issue
2. Wait 1-2 minutes
3. Check target repository for:
   - New branch: `jira/cgci-123`
   - Synced docs in branch
   - New GitHub issue assigned to @copilot
   - Comment with implementation instructions

## 📚 Documentation

- **[Quick Reference Guide](QUICK_REFERENCE.md)** - Command reference and checklist
- **[Enhanced Workflow Guide](docs/COPILOT_WITH_CONTEXT.md)** - Full setup and architecture
- **[Jira Automation Examples](docs/JIRA_AUTOMATION_EXAMPLES.md)** - Configuration templates
- **[Setup Guide](SETUP.md)** - Basic workflow setup

## 📁 Project Structure

```
jira-github-codingagent/
├── .github/
│   └── workflows/
│       ├── jira-to-github-issue.yml              # Basic workflow
│       └── jira-to-copilot-with-context.yml      # Enhanced workflow ⭐
├── scripts/
│   ├── create_issue_mcp.py                       # Basic issue creation
│   ├── sync_context_to_branch.py                 # Branch + docs sync ⭐
│   ├── create_issue_with_context.py              # Issue with context ⭐
│   └── assign_to_copilot.py                      # Copilot assignment ⭐
├── docs/
│   ├── architecture/overview.md                  # System architecture
│   ├── api-standards/                            # API conventions
│   ├── laravel/                                  # Laravel patterns
│   ├── react/                                    # React patterns
│   ├── COPILOT_WITH_CONTEXT.md                  # Enhanced workflow docs
│   └── JIRA_AUTOMATION_EXAMPLES.md              # Jira configuration
├── README.md                                      # This file
├── QUICK_REFERENCE.md                            # Quick reference guide
├── SETUP.md                                      # Basic setup
└── requirements.txt                              # Python dependencies
```

## 🎯 What Gets Synced

When using the **enhanced workflow**, all project documentation is synced to the target branch:

```
docs/
├── architecture/overview.md          → System architecture
├── api-standards/
│   ├── naming-conventions.md        → Naming rules
│   └── crud-api-spec.md             → API patterns
├── laravel/
│   ├── core-patterns.md             → MVC patterns
│   ├── database-access-layer.md     → Eloquent ORM
│   ├── error-handling.md            → Error handling
│   └── unit-testing-standards.md    → PHPUnit tests
└── react/
    ├── component-structure.md       → Components
    ├── state-management.md          → State patterns
    ├── api-consumption.md           → API layer
    └── testing-library-patterns.md  → React tests
```

## 🔄 How It Works (Enhanced Workflow)

```
┌─────────────┐
│ Jira Ticket │ Label: Auto-Copilot-CMS
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│  Jira Automation Rule           │ Webhook to GitHub
└──────┬──────────────────────────┘
       │
       ▼
┌────────────────────────────────────────────────────────┐
│  jira-github-codingagent (Agent Repository)            │
│                                                         │
│  GitHub Actions Workflow Executes:                     │
│                                                         │
│  1️⃣ sync_context_to_branch.py                         │
│     ├─ Create branch: jira/cgci-123                    │
│     └─ Push docs/* → target repo                       │
│                                                         │
│  2️⃣ create_issue_with_context.py                      │
│     ├─ Create issue with context reference             │
│     └─ Add labels: copilot-ready, has-context          │
│                                                         │
│  3️⃣ assign_to_copilot.py                              │
│     ├─ Assign @copilot to issue                        │
│     └─ Add comment with instructions                   │
└──────┬─────────────────────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────────────────────────┐
│  Target Repository (cms-project)                       │
│                                                         │
│  ├─ Branch: jira/cgci-123                              │
│  │   └─ docs/ (full project standards)                 │
│  │                                                      │
│  ├─ Issue #123: [CGCI-123] Feature X                   │
│  │   ├─ Assigned: @copilot                             │
│  │   ├─ Labels: copilot-ready, has-context             │
│  │   └─ References branch: jira/cgci-123               │
│  │                                                      │
│  └─ Comment: "Read docs/ and follow patterns..."       │
└──────┬─────────────────────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────────────────────────┐
│  GitHub Copilot Agent                                  │
│                                                         │
│  1. Switches to branch jira/cgci-123                   │
│  2. Reads project documentation in docs/               │
│  3. Implements following established patterns          │
│  4. Creates PR: jira/cgci-123 → main                   │
└────────────────────────────────────────────────────────┘
```

## 💡 Benefits

### ✅ Full Project Context
Copilot has access to all coding standards, patterns, and architectural decisions.

### ✅ Consistent Implementation
All implementations follow documented patterns ensuring consistency.

### ✅ Isolated Work
Each Jira issue gets its own branch with documentation.

### ✅ Zero Manual Steps
Entire process is automated from Jira label to Copilot assignment.

### ✅ Multi-Repo Support
Single agent repository serves multiple target repositories.

### ✅ Traceable
Branch names match Jira keys for easy tracking.

## 🧪 Testing

Test the webhook manually:

```bash
curl -X POST \
  https://api.github.com/repos/Karthi-Knackforge/jira-github-codingagent/dispatches \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -d '{
    "event_type": "jira-to-copilot-with-context",
    "client_payload": {
      "target_owner": "Karthi-Knackforge",
      "target_repo": "cms-project",
      "jira_key": "TEST-1",
      "summary": "Test Issue",
      "description": "This is a test",
      "url": "https://your-jira.atlassian.net/browse/TEST-1",
      "priority": "Medium",
      "issue_type": "Task"
    }
  }'
```

## 🛠️ Requirements

- Python 3.11+
- GitHub Personal Access Token with `repo` and `workflow` scopes
- GitHub Copilot enabled for organization/repositories
- Jira with automation rules capability

Install dependencies:
```bash
pip install -r requirements.txt
```

## 🔧 Customization

### Add New Documentation
Place markdown files in `docs/` directory. They will automatically sync to target branches.

### Change Branch Naming
Edit `sync_context_to_branch.py`:
```python
branch_name = f"jira/{JIRA_ISSUE_KEY.lower()}"
```

### Customize Issue Template
Edit `create_issue_with_context.py`:
```python
def create_copilot_optimized_issue_body():
    # Customize template here
```

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## 📞 Support

- **Documentation:** See `docs/` directory
- **Issues:** Open a GitHub issue
- **Questions:** Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

---

**Built with ❤️ for automated development workflows**

## 🚀 Next Steps

### 1. Configure GitHub Secret

In this repo (`jira-github-codingagent`):
- Go to **Settings → Secrets and variables → Actions**
- Add secret: `GB_TOKEN` = Your GitHub Personal Access Token
- Required scopes: `repo`, `workflow`

### 2. Create Jira Automation Rules

For each target repository, create a Jira automation rule:

#### Example: CMS Project

**Trigger:** Issue labeled with `Auto-Copilot-CMS`

**Action:** Send web request
```
URL: https://api.github.com/repos/Karthi-Knackforge/jira-github-codingagent/dispatches
Method: POST
Headers:
  Authorization: Bearer YOUR_GITHUB_TOKEN
  Accept: application/vnd.github+json
  X-GitHub-Api-Version: 2022-11-28

Body:
{
  "event_type": "jira-to-github-issue",
  "client_payload": {
    "target_owner": "Karthi-Knackforge",
    "target_repo": "cms-project",
    "jira_key": "{{issue.key}}",
    "summary": "{{issue.summary}}",
    "description": "{{issue.description}}",
    "url": "{{issue.url}}",
    "priority": "{{issue.priority.name}}",
    "issue_type": "{{issue.type.name}}"
  }
}
```

#### Add More Repos

Create additional rules with different labels:
- `Auto-Copilot-API` → `"target_repo": "api-project"`
- `Auto-Copilot-Frontend` → `"target_repo": "frontend-app"`
- `Auto-Copilot-Mobile` → `"target_repo": "mobile-app"`

## 🧪 Test It

1. Create/open a Jira issue in your CGCI project
2. Add label `Auto-Copilot-CMS`
3. Wait 1-2 minutes
4. Check:
   - GitHub Actions in `jira-github-codingagent` repo (workflow logs)
   - New issue in `cms-project` repo
   - Issue assigned to `@github`
5. Watch Copilot create a PR!

## 🏗️ Architecture Benefits

✅ **Centralized Logic**: All orchestration in one repo
✅ **Multi-Repo Support**: Route to any target repo via label
✅ **MCP Abstraction**: Clean API interface via Model Context Protocol
✅ **No Duplication**: Single workflow serves all repos
✅ **Easy Extension**: Add new repos by creating new Jira rules

## 📁 Key Files

- `.github/workflows/jira-to-github-issue.yml` - GitHub Actions workflow
- `scripts/create_issue_mcp.py` - MCP-based issue creation script
- `requirements.txt` - Python dependencies (requests, mcp)
- `.github/workflows/README.md` - Detailed documentation

## 🔧 How MCP Works

The script:
1. Connects to MCP GitHub server via `npx @modelcontextprotocol/server-github`
2. Uses `search_issues` tool to check for duplicates
3. Uses `github_issue_write` tool to create issue
4. Assigns to `@github` (Copilot coding agent)
5. Falls back to direct GitHub API if MCP fails

## 📚 Learn More

- [GitHub Copilot Coding Agent](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Repository Dispatch Events](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)
