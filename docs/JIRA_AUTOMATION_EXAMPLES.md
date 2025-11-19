# Example Jira Automation Configuration

This document provides example configurations for setting up Jira automation rules that trigger the GitHub Copilot agent workflow with full project context.

---

## 🎯 Overview

For each target repository, you'll create a Jira automation rule that:
1. Triggers when a specific label is added to a Jira issue
2. Sends a webhook to the `jira-github-codingagent` repository
3. Includes the Jira issue details as payload

---

## 📋 Automation Rule Template

### Basic Configuration

**Name:** Auto-Assign to GitHub Copilot - [Project Name]

**Trigger:** Issue labeled with `Auto-Copilot-[ProjectName]`

**Condition:** (Optional) Add conditions like:
- Issue type = Story, Task, or Bug
- Project = Specific project key

**Action:** Send web request

---

## 🔧 Webhook Configuration

### For Enhanced Workflow (with Project Context)

Use this configuration to get full project context synced:

```
URL: https://api.github.com/repos/Karthi-Knackforge/jira-github-codingagent/dispatches

Method: POST

Headers:
  Authorization: Bearer YOUR_GITHUB_TOKEN
  Accept: application/vnd.github+json
  X-GitHub-Api-Version: 2022-11-28
  Content-Type: application/json

HTTP Body (Custom Data):
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

### For Basic Workflow (without Context Sync)

Use this if you don't need documentation synced:

```
URL: https://api.github.com/repos/Karthi-Knackforge/jira-github-codingagent/dispatches

Method: POST

Headers:
  Authorization: Bearer YOUR_GITHUB_TOKEN
  Accept: application/vnd.github+json
  X-GitHub-Api-Version: 2022-11-28
  Content-Type: application/json

HTTP Body (Custom Data):
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

## 🏷️ Label Naming Convention

Use descriptive labels that map to your repositories:

| Jira Label | Target Repository | Description |
|------------|-------------------|-------------|
| `Auto-Copilot-CMS` | cms-project | Content Management System |
| `Auto-Copilot-API` | api-project | Backend API |
| `Auto-Copilot-Frontend` | frontend-app | React Frontend |
| `Auto-Copilot-Mobile` | mobile-app | Mobile Application |
| `Auto-Copilot-Admin` | admin-dashboard | Admin Dashboard |
| `Auto-Copilot-Docs` | documentation | Documentation Site |

---

## 📝 Example Configurations

### Example 1: CMS Project (Full Stack)

```yaml
Name: Auto-Copilot CMS
Trigger: Label = Auto-Copilot-CMS
Condition: Project = CGCI AND Issue Type IN (Story, Task, Bug)

Webhook:
  event_type: jira-to-copilot-with-context
  target_owner: Karthi-Knackforge
  target_repo: cms-project
```

**What happens:**
1. Branch `jira/cgci-123` created in `cms-project`
2. All docs synced to branch (Laravel + React standards)
3. Issue created with context reference
4. Copilot assigned with instructions to read docs

---

### Example 2: API Only Project

```yaml
Name: Auto-Copilot API
Trigger: Label = Auto-Copilot-API
Condition: Project = API AND Issue Type IN (Story, Task, Bug)

Webhook:
  event_type: jira-to-copilot-with-context
  target_owner: Karthi-Knackforge
  target_repo: api-project
```

**What happens:**
1. Branch `jira/api-456` created in `api-project`
2. Only relevant docs synced (architecture, Laravel standards)
3. Issue created with API-specific context
4. Copilot assigned with backend-focused instructions

---

### Example 3: Frontend Only Project

```yaml
Name: Auto-Copilot Frontend
Trigger: Label = Auto-Copilot-Frontend
Condition: Project = FE AND Issue Type IN (Story, Task, Bug)

Webhook:
  event_type: jira-to-copilot-with-context
  target_owner: Karthi-Knackforge
  target_repo: frontend-app
```

**What happens:**
1. Branch `jira/fe-789` created in `frontend-app`
2. Only frontend docs synced (React standards, component patterns)
3. Issue created with frontend-specific context
4. Copilot assigned with React-focused instructions

---

## 🔒 Security Considerations

### GitHub Token Requirements

Your GitHub Personal Access Token needs:
- `repo` scope (full control of private repositories)
- `workflow` scope (update GitHub Actions workflows)

### Token Storage

**In Jira:**
- Store token in automation rule webhook headers
- Use Jira's built-in secrets management if available
- Rotate tokens periodically

**In GitHub:**
- Add token as repository secret: `GB_TOKEN`
- Settings → Secrets and variables → Actions
- Never commit tokens to code

---

## 🧪 Testing Your Configuration

### Step 1: Test Webhook

Before creating the automation rule, test the webhook manually:

```bash
curl -X POST \
  https://api.github.com/repos/Karthi-Knackforge/jira-github-codingagent/dispatches \
  -H "Authorization: Bearer YOUR_GITHUB_TOKEN" \
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

Expected result: HTTP 204 No Content

### Step 2: Verify Workflow Triggered

1. Go to `jira-github-codingagent` repository
2. Navigate to **Actions** tab
3. Look for workflow run with "jira-to-copilot-with-context" event
4. Check workflow logs for success

### Step 3: Verify Target Repository

1. Go to target repository (e.g., `cms-project`)
2. Check **Branches** - should see new branch `jira/test-1`
3. Check branch contents - should see `docs/` directory
4. Check **Issues** - should see new issue assigned to @copilot

### Step 4: Create Actual Jira Rule

Once manual test succeeds:
1. Create the automation rule in Jira
2. Test with a real Jira issue
3. Add the label and observe the automation

---

## 🔧 Troubleshooting

### Webhook Returns 401 Unauthorized
- Check GitHub token is valid
- Verify token has `repo` and `workflow` scopes
- Ensure token is not expired

### Webhook Returns 404 Not Found
- Verify repository owner and name are correct
- Check repository exists and token has access
- Ensure URL format is correct

### Workflow Doesn't Trigger
- Check `event_type` matches workflow configuration
- Verify workflow file is in `.github/workflows/` directory
- Ensure workflow is enabled in repository settings

### Branch Creation Fails
- Check `GB_TOKEN` secret is configured in agent repository
- Verify token has write access to target repository
- Check target repository exists and is accessible

### Docs Not Syncing
- Verify `docs/` directory exists in agent repository
- Check markdown files exist in docs subdirectories
- Review workflow logs for sync errors

### Copilot Not Responding
- Verify GitHub Copilot is enabled for the organization
- Check `copilot-swe-agent` has access to repository
- Ensure issue is properly assigned
- Review comment instructions were added

---

## 📚 Jira Smart Values Reference

Use these Jira smart values in your webhook body:

| Smart Value | Description | Example |
|-------------|-------------|---------|
| `{{issue.key}}` | Issue key | CGCI-123 |
| `{{issue.summary}}` | Issue title | Implement user login |
| `{{issue.description}}` | Issue description | Full description text |
| `{{issue.url}}` | Issue URL | https://jira.../browse/CGCI-123 |
| `{{issue.priority.name}}` | Priority level | High, Medium, Low |
| `{{issue.type.name}}` | Issue type | Story, Task, Bug |
| `{{issue.assignee.displayName}}` | Assignee name | John Doe |
| `{{issue.reporter.emailAddress}}` | Reporter email | john@example.com |
| `{{issue.created}}` | Creation date | 2024-01-15 |
| `{{issue.labels}}` | All labels | label1, label2 |

---

## 🎯 Best Practices

### Label Organization
- Use consistent naming: `Auto-Copilot-[ProjectName]`
- Document label meanings for team
- Create label guide in Jira

### Issue Description Quality
- Write clear, actionable requirements
- Include acceptance criteria
- Link to design documents or mockups
- Copilot works better with detailed descriptions

### Priority Mapping
- Use Jira priorities consistently
- Map to GitHub labels for visibility
- Consider different urgency levels

### Testing Strategy
1. Test webhook manually first
2. Test with a single Jira issue
3. Monitor GitHub Actions logs
4. Verify target repository changes
5. Roll out to team gradually

---

## 📞 Support

If you encounter issues:

1. Check GitHub Actions logs in `jira-github-codingagent` repository
2. Review target repository for branch and issue creation
3. Verify Jira automation rule execution logs
4. Check webhook response codes in Jira

For detailed troubleshooting, see [COPILOT_WITH_CONTEXT.md](COPILOT_WITH_CONTEXT.md).
