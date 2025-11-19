# Jira to GitHub Copilot with Full Project Context

## 🎯 Overview

This enhanced workflow automatically:
1. **Creates a branch** in the target repository named after the Jira issue (e.g., `jira/cgci-123`)
2. **Syncs project documentation** from this agent repo's `docs/` directory to that branch
3. **Creates a GitHub issue** with clear instructions referencing the context branch
4. **Assigns to Copilot** with explicit instructions to read the project documentation

This ensures GitHub Copilot has **full project context** including architecture, coding standards, API conventions, and testing patterns before implementing any changes.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          Jira Ticket                            │
│                   (with Auto-Copilot label)                     │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ Automation Rule triggers
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│               jira-github-codingagent Repository                │
│                    (Centralized Agent Repo)                     │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  GitHub Actions Workflow                                 │   │
│  │  (jira-to-copilot-with-context.yml)                      │   │
│  │                                                          │   │
│  │  Step 1: sync_context_to_branch.py                       │   │
│  │    ├─ Create branch: jira/cgci-123                       │   │
│  │    └─ Push docs/* to target repo branch                  │   │
│  │                                                          │   │
│  │  Step 2: create_issue_with_context.py                    │   │
│  │    ├─ Create issue with context reference                │   │
│  │    └─ Add labels: copilot-ready, has-context             │   │
│  │                                                          │   │
│  │  Step 3: assign_to_copilot.py                            │   │
│  │    ├─ Assign @copilot to issue                           │   │
│  │    └─ Add comment with explicit instructions             │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  📁 docs/                                                       │
│    ├─ architecture/overview.md                                  │
│    ├─ api-standards/naming-conventions.md                       │
│    ├─ api-standards/crud-api-spec.md                            │
│    ├─ laravel/core-patterns.md                                  │
│    ├─ laravel/database-access-layer.md                          │
│    ├─ laravel/error-handling.md                                 │
│    ├─ laravel/unit-testing-standards.md                         │
│    ├─ react/component-structure.md                              │
│    ├─ react/state-management.md                                 │
│    ├─ react/api-consumption.md                                  │
│    └─ react/testing-library-patterns.md                         │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ Creates issue in...
                            │
┌───────────────────────────▼──────────────────────────────────────┐
│                      Target Repository                           │
│                      (cms-project, etc.)                         │
│                                                                  │
│  Branch: jira/cgci-123                                           │
│    └─ docs/ (synced from agent repo)                             │
│       ├─ architecture/                                           │
│       ├─ api-standards/                                          │
│       ├─ laravel/                                                │
│       └─ react/                                                  │
│                                                                  │
│  Issue #123: [CGCI-123] Implement feature X                    │
│    Assigned to: @copilot                                         │
│    Branch: jira/cgci-123                                         │
│    Labels: copilot-ready, has-context                            │
│                                                                  │
│  Comment: Instructions to read docs/ and follow patterns         │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                            │ Copilot reads docs
                            │ and implements
                            │
┌───────────────────────────▼──────────────────────────────────────┐
│                    Pull Request Created                          │
│              From: jira/cgci-123 → main                          │
│          With: Implementation following patterns                 │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Setup Instructions

### 1. Configure GitHub Secret

In the `jira-github-codingagent` repository:
- Go to **Settings → Secrets and variables → Actions**
- Add secret: `GB_TOKEN` = Your GitHub Personal Access Token
- Required scopes: `repo`, `workflow`

### 2. Create Jira Automation Rules

For each target repository, create a Jira automation rule:

#### Example: CMS Project

**Trigger:** Issue labeled with `Auto-Copilot-CMS`

**Action:** Send web request

```json
URL: https://api.github.com/repos/Karthi-Knackforge/jira-github-codingagent/dispatches
Method: POST
Headers:
  Authorization: Bearer YOUR_GITHUB_TOKEN
  Accept: application/vnd.github+json
  X-GitHub-Api-Version: 2022-11-28

Body:
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

#### Add More Repositories

Create additional rules for different projects:
- `Auto-Copilot-API` → `"target_repo": "api-project"`
- `Auto-Copilot-Frontend` → `"target_repo": "frontend-app"`
- `Auto-Copilot-Mobile` → `"target_repo": "mobile-app"`

---

## 📋 What Gets Synced

When a Jira issue is labeled, the workflow automatically copies these documentation files to the target repository's context branch:

### Architecture Documentation
- `docs/architecture/overview.md` - System architecture, tech stack, design patterns

### API Standards
- `docs/api-standards/naming-conventions.md` - Naming rules for APIs, URLs, fields, components
- `docs/api-standards/crud-api-spec.md` - Standard CRUD API patterns with examples

### Laravel Backend Standards
- `docs/laravel/core-patterns.md` - MVC patterns, controllers, models, relationships
- `docs/laravel/database-access-layer.md` - Eloquent ORM usage, queries, migrations
- `docs/laravel/error-handling.md` - Error handling patterns and HTTP status codes
- `docs/laravel/unit-testing-standards.md` - PHPUnit testing patterns and examples

### React Frontend Standards
- `docs/react/component-structure.md` - Component organization and patterns
- `docs/react/state-management.md` - React Query, Context API, local state patterns
- `docs/react/api-consumption.md` - Service layer, Axios configuration, error handling
- `docs/react/testing-library-patterns.md` - React Testing Library patterns and examples

---

## 🔄 Workflow Steps

### Step 1: Branch Creation & Context Sync
**Script:** `scripts/sync_context_to_branch.py`

- Creates branch named `jira/{jira-key}` (e.g., `jira/cgci-123`)
- Copies all `docs/**/*.md` files to the branch
- Maintains directory structure (`docs/architecture/`, `docs/laravel/`, etc.)
- Updates or creates files as needed

### Step 2: Issue Creation
**Script:** `scripts/create_issue_with_context.py`

- Creates GitHub issue with title: `[JIRA-KEY] Summary`
- Includes Jira requirements and acceptance criteria
- References the context branch explicitly
- Adds instructions to read documentation
- Applies labels: `copilot-ready`, `has-context`, `priority-{level}`

### Step 3: Copilot Assignment
**Script:** `scripts/assign_to_copilot.py`

- Assigns issue to `@copilot` or `copilot-swe-agent`
- Adds a detailed comment with:
  - Instructions to switch to context branch
  - List of documentation files to review
  - Implementation guidelines
  - Standards to follow

---

## 🧪 Testing the Workflow

1. **Create or open a Jira issue** in your project
2. **Add label** (e.g., `Auto-Copilot-CMS`)
3. **Wait 1-2 minutes** for automation to trigger
4. **Verify in GitHub:**
   - Actions tab: Check workflow run in `jira-github-codingagent` repo
   - Target repo: Verify new branch `jira/cgci-###` exists
   - Target repo: Check `docs/` directory in the new branch
   - Target repo: Verify issue was created with proper labels
   - Target repo: Check issue is assigned to @copilot
   - Target repo: Review comment with instructions
5. **Watch Copilot work:**
   - Copilot will read the documentation
   - Implement following the patterns
   - Create a PR from the context branch

---

## 📁 Key Files

### Workflow
- `.github/workflows/jira-to-copilot-with-context.yml` - Main GitHub Actions workflow

### Scripts
- `scripts/sync_context_to_branch.py` - Branch creation and documentation sync
- `scripts/create_issue_with_context.py` - Issue creation with context references
- `scripts/assign_to_copilot.py` - Copilot assignment with instructions

### Documentation (Synced to Target Repos)
- `docs/architecture/` - Architecture and system design
- `docs/api-standards/` - API naming and CRUD patterns
- `docs/laravel/` - Laravel backend patterns and testing
- `docs/react/` - React frontend patterns and testing

---

## 💡 Benefits

### ✅ Full Project Context
Copilot has access to all coding standards, patterns, and architectural decisions documented in your project.

### ✅ Consistent Implementation
All implementations follow the same patterns defined in documentation, ensuring consistency across the codebase.

### ✅ Isolated Work
Each Jira issue gets its own branch with documentation, keeping work isolated and organized.

### ✅ No Manual Steps
Entire process is automated from Jira label to Copilot assignment.

### ✅ Multi-Repo Support
Single agent repository can serve multiple target repositories with different tech stacks.

### ✅ Traceable
Branch names match Jira keys, making it easy to track which branch corresponds to which ticket.

---

## 🛠️ Customization

### Adding New Documentation
To add new project context:
1. Add markdown files to `docs/` directory in this agent repo
2. Organize in logical subdirectories
3. Files will automatically sync to target branches

### Changing Branch Naming
Edit `sync_context_to_branch.py`:
```python
branch_name = f"jira/{JIRA_ISSUE_KEY.lower()}"
# Change to your preferred pattern
```

### Customizing Issue Template
Edit `create_issue_with_context.py`:
```python
def create_copilot_optimized_issue_body():
    # Customize the issue body template
```

### Adding More Labels
Edit `create_issue_with_context.py`:
```python
label_names = [
    "jira-sync",
    "copilot-ready",
    f"priority-{JIRA_PRIORITY.lower()}",
    "has-context",
    # Add your custom labels here
]
```

---

## 🔍 Troubleshooting

### Issue: Branch Creation Fails
**Solution:** Check that `GB_TOKEN` has `repo` scope and access to target repository.

### Issue: Docs Not Syncing
**Solution:** Verify `docs/` directory exists in agent repo and contains `.md` files.

### Issue: Copilot Not Assigned
**Solution:** 
- Ensure GitHub Copilot is enabled for the organization/repository
- Check that `copilot-swe-agent` has access to the repository
- Instructions comment will still be added for manual assignment

### Issue: Workflow Not Triggering
**Solution:**
- Verify Jira automation rule is using correct `event_type`: `jira-to-copilot-with-context`
- Check GitHub Actions are enabled in the repository
- Verify `GB_TOKEN` secret is configured

---

## 📚 References

- [GitHub Copilot Coding Agent](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)
- [Assigning Tasks to Copilot](https://docs.github.com/en/copilot/using-github-copilot/using-copilot-coding-agent-to-work-on-tasks/about-assigning-tasks-to-copilot)
- [Repository Dispatch Events](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)
- [GitHub Actions Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

---

## 🎉 Next Steps

1. ✅ Configure `GB_TOKEN` secret
2. ✅ Set up Jira automation rules for your repositories
3. ✅ Customize documentation in `docs/` directory
4. ✅ Test with a sample Jira issue
5. ✅ Monitor Copilot's implementation
6. ✅ Review and merge the PRs created by Copilot
