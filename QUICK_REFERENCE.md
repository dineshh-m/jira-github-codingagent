# Quick Reference Guide

## 🚀 Quick Start

### For Enhanced Workflow (Recommended)

1. **Configure GitHub Secret**
   ```
   Repository: jira-github-codingagent
   Secret Name: GB_TOKEN
   Value: Your GitHub Personal Access Token (with repo + workflow scopes)
   ```

2. **Create Jira Automation Rule**
   - Trigger: Issue labeled with `Auto-Copilot-[ProjectName]`
   - Action: Send web request to GitHub
   - Event Type: `jira-to-copilot-with-context`

3. **Test It**
   - Add label to Jira issue
   - Wait 1-2 minutes
   - Check GitHub for: branch creation, docs sync, issue creation, Copilot assignment

---

## 📋 Workflow Comparison

| Feature | Basic Workflow | Enhanced Workflow |
|---------|----------------|-------------------|
| **Workflow File** | `jira-to-github-issue.yml` | `jira-to-copilot-with-context.yml` |
| **Event Type** | `jira-to-github-issue` | `jira-to-copilot-with-context` |
| **Creates Branch** | ❌ No | ✅ Yes (`jira/{key}`) |
| **Syncs Docs** | ❌ No | ✅ Yes (all `docs/*.md`) |
| **Creates Issue** | ✅ Yes | ✅ Yes (with context reference) |
| **Assigns Copilot** | ✅ Yes | ✅ Yes (with instructions) |
| **Project Context** | ❌ No | ✅ Yes (full docs available) |
| **Use Case** | Simple issue creation | Full-featured with standards |

---

## 🔧 Configuration Examples

### Jira Webhook (Enhanced)

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

### Jira Webhook (Basic)

```json
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

---

## 📁 What Gets Synced (Enhanced Workflow)

All files from `docs/` directory in agent repo → Target repo branch

```
docs/
├── architecture/
│   └── overview.md                    → System architecture
├── api-standards/
│   ├── naming-conventions.md          → Naming rules
│   └── crud-api-spec.md               → API patterns
├── laravel/
│   ├── core-patterns.md               → MVC patterns
│   ├── database-access-layer.md       → Eloquent ORM
│   ├── error-handling.md              → Error handling
│   └── unit-testing-standards.md      → PHPUnit tests
└── react/
    ├── component-structure.md         → Components
    ├── state-management.md            → State patterns
    ├── api-consumption.md             → API service layer
    └── testing-library-patterns.md    → React tests
```

---

## 🏷️ Labels Created

### Enhanced Workflow
- `jira-sync` - Synced from Jira
- `copilot-ready` - Ready for Copilot agent
- `has-context` - Project documentation available
- `priority-{level}` - Priority from Jira (e.g., `priority-high`)

### Basic Workflow
- `jira-sync` - Synced from Jira
- `copilot-agent` - Assigned to Copilot
- `priority-{level}` - Priority from Jira

---

## 🌿 Branch Naming

| Jira Issue | Branch Created |
|------------|----------------|
| CGCI-123 | `jira/cgci-123` |
| API-456 | `jira/api-456` |
| FE-789 | `jira/fe-789` |

---

## 🔍 Verification Checklist

After triggering the workflow:

### Enhanced Workflow
- [ ] GitHub Actions workflow ran successfully in `jira-github-codingagent`
- [ ] New branch `jira/{key}` created in target repository
- [ ] `docs/` directory synced to branch with all markdown files
- [ ] GitHub issue created with title `[JIRA-KEY] Summary`
- [ ] Issue has labels: `copilot-ready`, `has-context`, `priority-{level}`
- [ ] Issue assigned to `@copilot` or `copilot-swe-agent`
- [ ] Comment added with instructions to read docs
- [ ] Comment includes list of documentation files
- [ ] Comment references the context branch

### Basic Workflow
- [ ] GitHub Actions workflow ran successfully in `jira-github-codingagent`
- [ ] GitHub issue created in target repository
- [ ] Issue has labels: `jira-sync`, `copilot-agent`, `priority-{level}`
- [ ] Issue assigned to `@copilot`

---

## 🛠️ Common Commands

### Test Webhook Manually

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
      "description": "Test description",
      "url": "https://your-jira.atlassian.net/browse/TEST-1",
      "priority": "Medium",
      "issue_type": "Task"
    }
  }'
```

### Check Workflow Runs

```bash
# View recent workflow runs
gh run list -R Karthi-Knackforge/jira-github-codingagent

# View specific run logs
gh run view RUN_ID -R Karthi-Knackforge/jira-github-codingagent
```

### Check Branch in Target Repo

```bash
# List branches matching pattern
gh api /repos/Karthi-Knackforge/cms-project/branches | jq '.[].name | select(startswith("jira/"))'

# View branch contents
gh api /repos/Karthi-Knackforge/cms-project/contents/docs?ref=jira/cgci-123
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Workflow not triggering | Check `event_type` matches workflow file |
| 401 Unauthorized | Verify GitHub token is valid and has correct scopes |
| Branch not created | Check `GB_TOKEN` secret in agent repo |
| Docs not syncing | Verify `docs/` directory exists in agent repo |
| Copilot not assigned | Check Copilot is enabled for organization/repo |
| No comment added | Check script logs for errors |

---

## 📚 Documentation Links

- [Full Enhanced Workflow Guide](docs/COPILOT_WITH_CONTEXT.md)
- [Jira Automation Examples](docs/JIRA_AUTOMATION_EXAMPLES.md)
- [GitHub Copilot Docs](https://docs.github.com/en/copilot)
- [Repository Dispatch Events](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)

---

## 🎯 Recommended Labels for Different Projects

| Project Type | Jira Label | Target Repo | Docs Synced |
|--------------|------------|-------------|-------------|
| Full Stack | `Auto-Copilot-CMS` | cms-project | All docs |
| Backend API | `Auto-Copilot-API` | api-project | Architecture, Laravel |
| Frontend | `Auto-Copilot-Frontend` | frontend-app | Architecture, React |
| Mobile | `Auto-Copilot-Mobile` | mobile-app | Architecture, API standards |
| Microservice | `Auto-Copilot-Service-[Name]` | service-name | Architecture, relevant tech |

---

## 💡 Tips & Best Practices

### For Better Copilot Results
1. Write detailed Jira descriptions with clear requirements
2. Include acceptance criteria in Jira description
3. Link to design documents or mockups
4. Specify technical constraints or preferences
5. Mention specific files or components to modify

### For Documentation
1. Keep `docs/` directory up-to-date in agent repo
2. Use consistent markdown formatting
3. Include code examples in standards
4. Document exceptions to patterns
5. Update docs when patterns change

### For Team Adoption
1. Start with one project to test
2. Train team on label usage
3. Document your specific workflow
4. Monitor Copilot's implementations
5. Iterate on documentation based on results

---

## 📞 Getting Help

1. **Check Logs**: GitHub Actions logs show detailed execution
2. **Review Scripts**: Python scripts have detailed print statements
3. **Test Manually**: Use curl to test webhook independently
4. **Verify Access**: Ensure tokens and permissions are correct
5. **Read Docs**: Full documentation in `docs/` directory

---

## 🔄 Workflow Diagram (Enhanced)

```
Jira Issue
    ↓ (label: Auto-Copilot-CMS)
Jira Automation Rule
    ↓ (webhook trigger)
jira-github-codingagent Repository
    ↓ (GitHub Actions)
    ├─ Step 1: sync_context_to_branch.py
    │   ├─ Create branch: jira/cgci-123
    │   └─ Sync docs/* → target repo
    ├─ Step 2: create_issue_with_context.py
    │   ├─ Create issue with context reference
    │   └─ Add labels: copilot-ready, has-context
    └─ Step 3: assign_to_copilot.py
        ├─ Assign @copilot to issue
        └─ Add comment with instructions
    ↓
Target Repository (cms-project)
    ├─ Branch: jira/cgci-123
    │   └─ docs/ (full project context)
    ├─ Issue #123: [CGCI-123] Feature X
    │   ├─ Assigned: @copilot
    │   └─ Labels: copilot-ready, has-context
    └─ Comment: Read docs and implement
    ↓
Copilot Agent Works
    ├─ Reads docs/ on branch
    ├─ Implements following patterns
    └─ Creates PR: jira/cgci-123 → main
```
