---
name: github-community-automation
description: Automate GitHub issue responses, release cadence, cross-posting, and contributor engagement at scale
category: GitHub
tools:
  - GitHub CLI
  - n8n
  - PostHog
  - Anthropic
fundamentals:
  - github-release-publish
  - github-traffic-api
  - n8n-workflow-basics
  - n8n-scheduling
  - n8n-triggers
  - posthog-custom-events
  - hypothesis-generation
---

# GitHub Community Automation

Scale a GitHub sample repo's engagement without proportional manual effort. This drill automates the repetitive tasks that keep a repo active and discoverable: issue triage, release publishing, cross-channel amplification, and contributor engagement.

## Input

- **Live GitHub repo** with at least 50 stars and established traffic patterns (from Baseline)
- **n8n instance** with GitHub webhook connected
- **PostHog** receiving daily traffic data (from `github-repo-promotion` drill)
- **Anthropic API key** for AI-powered issue responses

## Steps

### 1. Automate issue triage and response

Build an n8n workflow triggered by GitHub webhook (`issues.opened` event):

1. Receive the new issue payload (title, body, labels, author)
2. Use Claude (via Anthropic API) to classify the issue:
   - **Bug report:** Label `bug`, respond with template asking for reproduction steps
   - **Feature request:** Label `enhancement`, respond acknowledging the request and linking to the roadmap
   - **Question / support:** Label `question`, respond with an answer pulled from README or docs. Include the product CTA: "For production use cases, check out [Product](https://yoursite.com/?utm_source=github&utm_medium=issue_response&utm_campaign=<repo>)"
   - **Spam / off-topic:** Label `invalid`, close with a polite note
3. Log the issue classification and response in PostHog: `github_issue_triaged` with properties `{repo, classification, response_time_seconds}`

```yaml
# n8n webhook trigger configuration
trigger: GitHub Webhook
event: issues.opened
```

### 2. Automate release cadence

Build an n8n workflow on a monthly cron schedule:

1. Check if there are new commits since the last release:
   ```bash
   gh api repos/<org>/<repo>/compare/$(gh release view --repo <org>/<repo> --json tagName -q '.tagName')...main --jq '.total_commits'
   ```
2. If commits > 0, run `github-release-publish` fundamental:
   - Auto-generate release notes from merged PRs
   - Increment patch version
   - Include CTA in release body
3. After publishing, trigger the cross-posting workflow (Step 3)
4. Log in PostHog: `github_release_published` with properties `{repo, version, commit_count}`

### 3. Cross-post releases to social channels

Build an n8n workflow triggered by the release workflow (or by GitHub webhook `release.published`):

1. Generate a short social post using Claude:
   - Input: release notes + repo description
   - Output: 2-3 sentence post highlighting what's new and why it matters
2. Post to LinkedIn (via LinkedIn API or Buffer API)
3. Post to Twitter/X (via Twitter API)
4. Post in relevant Discord/Slack communities (via webhook)
5. All links include UTM: `?utm_source=<platform>&utm_medium=social&utm_campaign=<repo>-<version>`
6. Log: `github_release_cross_posted` with properties `{repo, version, platforms}`

### 4. Contributor engagement automation

Build an n8n workflow triggered by GitHub webhook (`pull_request.opened`, `pull_request.merged`):

**On PR opened:**
- If first-time contributor: respond with a welcoming message and link to CONTRIBUTING.md
- If returning contributor: respond with thanks and faster review commitment

**On PR merged:**
- Add contributor to a "Contributors" section in README (or use the all-contributors bot)
- Send a thank-you DM or email via Loops (if contributor email is available from GitHub profile)
- Log: `github_contributor_engaged` with properties `{repo, contributor, type: first-time|returning}`

### 5. Scale traffic through README A/B testing

Using `hypothesis-generation` fundamental:

1. Formulate hypotheses about README changes that could improve conversion:
   - Different CTA copy
   - Different problem statement framing
   - Reordering sections
2. Implement by creating branches with different README versions
3. Use GitHub's default branch feature to test (swap default branch bi-weekly)
4. Compare traffic and CTA click-through rates across periods in PostHog
5. Adopt the winner

## Output

- n8n workflows handling: issue triage, monthly releases, cross-posting, contributor engagement
- All GitHub activity events flowing to PostHog
- README optimization running continuously
- Repo stays active and responsive without manual daily effort

## Triggers

Set up once after reaching Scalable level. Workflows run continuously via cron and webhooks.
