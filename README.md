# Elastic SRE Agent

**AI-powered incident response that detects outages, finds root causes, and creates fixes automatically.**

[![Built with Elastic Agent Builder](https://img.shields.io/badge/Built%20with-Elastic%20Agent%20Builder-005571?style=for-the-badge&logo=elasticsearch)](https://www.elastic.co/docs/explore-analyze/ai-features/elastic-agent-builder)
[![No Code](https://img.shields.io/badge/No%20Code-100%25-green?style=for-the-badge)](/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue?style=for-the-badge)](LICENSE)

> Built for the [Elasticsearch Agent Builder Hackathon](https://elasticsearch.devpost.com/)

---

## 🎬 Demo

[Watch the 3-minute demo video](https://vimeo.com/1165186173?share=copy&fl=sv&fe=ci)

---

## 💡 The Problem

When production crashes at 3 AM, engineers spend **3-4 hours** doing this manually:

```
📋 Scroll logs → 🔍 Search git → 🧠 Correlate → 📝 Create PR → 📢 Notify team
```

## ✨ The Solution

**One prompt. Three minutes. Problem solved.**

```
User: "Check service health and fix any issues"

Agent: 🔍 Found 100 errors in checkout-service
       🧠 Root cause: Commit f9ed964 by devdave "Removed null safety checks"
       🔧 Created revert PR #42
       📢 Notified #sre-alerts on Slack
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     ELASTIC SRE AGENT                           │
│                                                                 │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐          │
│   │   DETECT    │──▶│   ANALYZE   │──▶│     ACT     │          │
│   │   ES|QL     │   │  Semantic   │   │  Workflows  │          │
│   │             │   │   Search    │   │             │          │
│   └─────────────┘   └─────────────┘   └─────────────┘          │
│                                              │                  │
└──────────────────────────────────────────────┼──────────────────┘
                                               │
                    ┌──────────────────────────┼──────────────────┐
                    │                          ▼                  │
                    │    ┌─────────┐    ┌─────────┐    ┌───────┐ │
                    │    │ GitHub  │    │  Slack  │    │ More  │ │
                    │    │   PR    │    │  Alert  │    │  ...  │ │
                    │    └─────────┘    └─────────┘    └───────┘ │
                    │              EXTERNAL SYSTEMS               │
                    └─────────────────────────────────────────────┘
```

---

## 🔧 Components Built

### 1. Elasticsearch Indices

| Index | Purpose | Key Field |
|-------|---------|-----------|
| `application-logs` | Store service errors | `semantic_text` for message |
| `github-commits` | Store commit history | `semantic_text` for message |

### 2. Agent Tools

| Tool | Type | Purpose |
|------|------|---------|
| `investigate_errors` | ES\|QL | Find error spikes by service |
| `find_related_commits` | Index Search | Semantic match errors → commits |
| `create_revert_pr` | Workflow | Trigger GitHub Action |
| `create_github_issue` | Workflow | Create incident tracking issue |
| `notify_slack` | Workflow | Send Slack alert |

### 3. Elastic Workflows

| Workflow | Action |
|----------|--------|
| `notify_slack_incident` | POST to Slack webhook |
| `create_github_revert_pr` | Trigger GitHub Action via API |
| `create_github_issue` | Create GitHub issue for tracking |

### 4. GitHub Action

| Action | Purpose |
|--------|---------|
| `auto_revert.yml` | Run `git revert` and create PR |

---

## 🪄 The Magic: Semantic Search

The agent matched these with **94% confidence**:

| Error Message | Commit Message |
|--------------|----------------|
| `NullPointerException in PaymentProcessor` | `Removed null safety checks` |

**Zero keywords in common.** That's the power of `semantic_text`!

---

## 📊 Impact

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Time to Resolution | 3-4 hours | <3 min | **98% faster** |
| Manual Steps | 15+ | 1 | **Fully automated** |
| Systems Connected | Siloed | 3 | **End-to-end** |

---

## 🚀 Setup Guide

### Prerequisites
- Elastic Cloud account ([free trial](https://cloud.elastic.co/registration))
- GitHub account
- Slack workspace (optional)

### Step 1: Create Indices

In Kibana → Dev Tools, run:

```json
PUT application-logs
{
  "mappings": {
    "properties": {
      "timestamp": { "type": "date" },
      "level": { "type": "keyword" },
      "service": { "type": "keyword" },
      "message": { "type": "text", "copy_to": "semantic_field" },
      "semantic_field": { "type": "semantic_text" }
    }
  }
}

PUT github-commits
{
  "mappings": {
    "properties": {
      "commit_id": { "type": "keyword" },
      "author": { "type": "keyword" },
      "message": { "type": "text", "copy_to": "semantic_field" },
      "semantic_field": { "type": "semantic_text" },
      "timestamp": { "type": "date" }
    }
  }
}
```

### Step 2: Load Sample Data

Use the data generator in `/sample-data` or upload via Kibana.

### Step 3: Create Agent

1. Go to **AI Agent** in Kibana
2. Create new agent "SRE Agent"
3. Add tools (see `/docs/agent-setup.md`)

### Step 4: Create Workflows

Import workflows from `/workflows` directory.

### Step 5: Set Up GitHub Action

Copy `.github/workflows/auto_revert.yml` to your target repository.

---

## 📁 Repository Structure

```
elastic-sre-agent/
├── README.md
├── LICENSE
├── indices/
│   ├── application-logs.json
│   └── github-commits.json
├── workflows/
│   ├── notify_slack_incident.yml
│   └── create_github_revert_pr.yml
├── sample-data/
│   └── generate_data.py
├── .github/
│   └── workflows/
│       └── auto_revert.yml
└── docs/
    ├── agent-setup.md
    ├── architecture.md
    └── screenshots/
```

---

## 🔌 Production Integration

This demo uses sample data. For production:

- **Logs**: Use Elastic Agent to collect from your servers
- **Commits**: Set up GitHub webhook → Elasticsearch
- **See**: [`docs/production-setup.md`](docs/production-setup.md)

---

## 🏆 Hackathon Tracks

- ✅ Automate messy internal work (incident response)
- ✅ Build tool-driven agents (ES|QL + Search + Workflows)
- ✅ Narrow agents for one domain (SRE/DevOps)
- ✅ Show measurable impact (98% faster)
- ✅ Connect disconnected systems (Elastic + GitHub + Slack)
- ✅ Time-series aware (error spike detection)
- ✅ Let agents take reliable action (auto-creates PRs)

---

## 📄 License

Apache 2.0 - See [LICENSE](LICENSE)

---

**Built with ❤️ for the [Elasticsearch Agent Builder Hackathon](https://elasticsearch.devpost.com/)**
