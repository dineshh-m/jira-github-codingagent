# Jira to GitHub Copilot Agent Integration

This workflow automatically creates GitHub issues from Jira tickets and assigns them to GitHub Copilot coding agent for autonomous implementation.

## 🔧 Setup Instructions

### 1. Configure GitHub Repository Secrets

Go to your **cms-project** repository **Settings → Secrets and variables → Actions** and verify:

- `GB_TOKEN` - Already available by default (no action needed)

### 2. Configure Jira Automation

Create a new automation rule in Jira:

**Trigger:** Issue labeled with `Auto-Copilot`

**Action:** Send web request

```
URL: https://api.github.com/repos/Karthi-Knackforge/cms-project/dispatches
Method: POST
Headers:
  Authorization: Bearer KEY
  Accept: application/vnd.github+json
  X-GitHub-Api-Version: 2022-11-28

Body (Custom data - JSON):
{
  "event_type": "jira-to-github-issue",
  "client_payload": {
    "jira_key": "{{issue.key}}",
    "summary": "{{issue.summary}}",
    "description": "{{issue.description}}",
    "url": "{{issue.url}}",
    "priority": "{{issue.priority.name}}",
    "issue_type": "{{issue.type.name}}"
  }
}
```

### 3. Enable GitHub Actions

Ensure Actions are enabled in your **cms-project** repository:
- Go to **Settings → Actions → General**
- Allow all actions and reusable workflows

## 🎯 How It Works

1. **Jira Trigger**: When you add the `Auto-Copilot` label to a Jira issue
2. **Webhook**: Jira sends a `repository_dispatch` event to GitHub
3. **Deduplication**: Script checks if an issue already exists for this Jira key
4. **Issue Creation**: If new, creates a GitHub issue with:
   - Structured format optimized for Copilot understanding
   - Requirements and Acceptance Criteria sections
   - Link back to original Jira ticket
   - Automatic labels: `jira-sync`, `copilot-agent`, `priority-{level}`
5. **Copilot Assignment**: Issue is automatically assigned to `@github` (GitHub Copilot coding agent)
6. **Autonomous Work**: Copilot coding agent:
   - Analyzes the requirements
   - Creates a development branch (copilot/*)
   - Implements the solution
   - Runs tests and validation
   - Opens a pull request for review

## 📊 Monitoring

- **Workflow runs**: Check `.github/workflows` action runs for execution logs
- **Job summaries**: Each run creates a summary with status and links
- **Issue comments**: Track Copilot's progress in the created issue
- **Pull requests**: Review Copilot's implementation in the PR it creates

## 🚨 Error Handling

If the workflow fails:
- Check the Actions tab for detailed error logs
- An automation-failure issue will be created automatically
- Review the job summary for quick diagnostics

## 🔒 Security Notes

- Copilot can only push to `copilot/*` branches
- All PRs require human review before merge
- CI/CD workflows need approval before running
- Commits are co-authored for traceability

## 📝 Issue Format Example

```markdown
## 📋 Requirements

Implement user authentication with OAuth2 support...

## ✅ Acceptance Criteria

- [ ] Implementation matches the requirements described above
- [ ] Code follows project conventions and best practices
- [ ] Tests are added/updated to cover changes
- [ ] Documentation is updated if needed

## 🔗 Jira Reference

**Jira Issue:** [CGCI-123](https://knackforge-team-xpf6pae3.atlassian.net/browse/CGCI-123)
**Priority:** High
**Type:** Story

---

*This issue was automatically created from Jira and assigned to GitHub Copilot coding agent for implementation.*
```

## 🎓 Learn More

- [GitHub Copilot Coding Agent Documentation](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)
- [Repository Dispatch Events](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)
- [Jira Automation](https://support.atlassian.com/cloud-automation/docs/jira-automation-triggers/)

## 📋 Jira Automation Configuration Details

### Smart Values Available

You can use these Jira smart values in your webhook:

- `{{issue.key}}` - Issue key (e.g., CGCI-123)
- `{{issue.summary}}` - Issue title
- `{{issue.description}}` - Issue description
- `{{issue.url}}` - Direct link to Jira issue
- `{{issue.priority.name}}` - Priority level
- `{{issue.type.name}}` - Issue type (Story, Bug, Task, etc.)
- `{{issue.assignee.displayName}}` - Assignee name
- `{{issue.reporter.displayName}}` - Reporter name

### Webhook Configuration Steps

1. Go to **Project settings → Automation** in your Jira project
2. Click **Create rule**
3. Set trigger: **Issue → Labeled**
4. Add condition: **Label equals "Auto-Copilot"**
5. Add action: **Send web request**
6. Configure as shown in Setup Instructions above
7. Name your rule: "Sync to GitHub Copilot"
8. Turn it ON

## 🧪 Testing

To test the integration:

1. Create or open a Jira issue in your CGCI project
2. Add the label `Auto-Copilot` to the issue
3. Wait 1-2 minutes for processing
4. Check GitHub Actions tab in cms-project repository
5. Verify new issue was created and assigned to @github
6. Watch for Copilot to start working on a PR

## 🐛 Troubleshooting

### Workflow not triggering?
- Verify the webhook URL is correct
- Check GitHub token has proper permissions
- Ensure repository_dispatch is enabled

### Issue not created?
- Check workflow logs in Actions tab
- Verify all Jira smart values are populated
- Check Python script output for errors

### Copilot not assigned?
- Ensure you have Copilot Pro/Business/Enterprise
- Verify @github user assignment in issue
- Check if Copilot is enabled for the repository
