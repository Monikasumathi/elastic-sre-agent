# Agent Setup Guide

## Step 1: Create the Agent

1. Go to Kibana → **AI Agent** (or search "Agent" in global search)
2. Click **Create Agent**
3. Configure:
   - **Agent ID**: `sre-agent`
   - **Display Name**: `SRE Agent`
   - **Description**: AI agent that detects production outages, finds the bad commit, and creates fixes automatically

## Step 2: Add System Instructions

Paste this in the **Custom Instructions** field:

```
You are an SRE (Site Reliability Engineering) Agent for TechCorp Industries. Your job is to help engineers quickly identify and fix production incidents.

WORKFLOW:
1. DETECT - When asked about service health, use investigate_errors to find error spikes
2. ANALYZE - Use find_related_commits to match errors to recent code changes using semantic similarity
3. ACT - Create incidents and notify the team

RESPONSE STYLE:
- Be concise and action-oriented
- Use emojis for status: 🚨 for alerts, ✅ for success, 🔍 for investigating
- Always show error counts and confidence scores
- Recommend next steps

When you find a likely root cause commit, report:
- Commit ID and author
- What the commit changed
- Confidence score (from semantic similarity)
- Recommended action (revert, hotfix, etc.)
```

## Step 3: Enable Platform Tools

Check these boxes:
- ✅ `platform.core.search`
- ✅ `platform.core.execute_esql`
- ✅ `platform.core.generate_esql`
- ✅ `platform.core.get_index_mapping`
- ✅ `platform.core.list_indices`
- ✅ `platform.core.get_workflow_execution_status`

## Step 4: Create Custom Tools

### Tool 1: investigate_errors (ES|QL)

- **Tool ID**: `sre.investigate_errors`
- **Type**: ES|QL
- **Query**:
```sql
FROM application-logs
| WHERE level == "ERROR" AND timestamp > NOW() - 24 hours
| STATS error_count = COUNT(*) BY service, message
| SORT error_count DESC
| LIMIT 10
```

### Tool 2: find_related_commits (Index Search)

- **Tool ID**: `sre.find_related_commits`
- **Type**: Index Search
- **Index**: `github-commits`
- **Description**: Search for commits that might be related to an error using semantic similarity

### Tool 3: notify_slack (Workflow)

- **Tool ID**: `sre.notify_slack`
- **Type**: Workflow
- **Workflow**: `notify_slack_incident`

### Tool 4: create_revert_pr (Workflow)

- **Tool ID**: `sre.create_revert_pr`
- **Type**: Workflow
- **Workflow**: `create_github_revert_pr`

## Step 5: Test the Agent

Start a new chat and try:

```
Check service health and find any errors
```

Then:

```
Create a revert PR to fix the issue
```
