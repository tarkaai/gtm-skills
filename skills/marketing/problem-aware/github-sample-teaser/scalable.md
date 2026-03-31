---
name: github-sample-teaser-scalable
description: >
  GitHub Sample Teaser — Scalable Automation. Automated issue triage, monthly
  release cadence, cross-channel amplification, and README A/B testing to reach
  10x Baseline traffic and leads without proportional manual effort.
stage: "Marketing > Problem Aware"
motion: "Directories & Marketplaces"
channels: "Other"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=150 stars or >=1,000 unique visitors and >=15 leads over 2 months"
kpis: ["Unique repo visitors", "Stars gained", "Clones", "README CTA click-through rate", "Leads attributed to GitHub", "Issue response time", "Release cadence"]
slug: "github-sample-teaser"
install: "npx gtm-skills add marketing/problem-aware/github-sample-teaser"
drills:
  - github-community-automation
  - ab-test-orchestrator
---

# GitHub Sample Teaser — Scalable Automation

> **Stage:** Marketing > Problem Aware | **Motion:** Directories & Marketplaces | **Channels:** Other

## Outcomes

Hit 10x Baseline traffic and leads without 10x manual effort. Automated workflows handle issue triage, release publishing, cross-channel amplification, and contributor engagement. The agent manages the repo's community presence while you focus on improving the sample code. A passing Scalable level means >=150 stars or >=1,000 unique visitors and >=15 leads over 2 months, with all automation running reliably.

## Leading Indicators

- Issue triage automation responds to new issues within 5 minutes (vs. hours/days manually)
- Monthly release cadence maintained automatically (no missed months)
- Cross-posting reaches 3+ channels per release without manual action
- README CTA click-through rate holds within 20% of Baseline level (confirms scaling does not dilute quality)
- At least 1 external contributor opens a PR (confirms the repo has community traction beyond stargazers)

## Instructions

### 1. Deploy issue triage and response automation

Run the `github-community-automation` drill, Step 1:

Build an n8n workflow triggered by GitHub webhook (`issues.opened`):
1. Receive the new issue payload (title, body, labels, author)
2. Classify the issue using Claude (via Anthropic API):
   - **Bug report:** Label `bug`, respond with a template requesting reproduction steps
   - **Feature request:** Label `enhancement`, acknowledge and link to the product roadmap
   - **Question / support:** Label `question`, answer using README/docs content, then include CTA: "For production use cases, check out [Product](https://yoursite.com/?utm_source=github&utm_medium=issue_response&utm_campaign=<repo>)"
   - **Spam / off-topic:** Label `invalid`, close with a polite note
3. Log the classification in PostHog: `github_issue_triaged` with properties `{repo, classification, response_time_seconds}`

**Human action required:** Review the AI-generated responses for the first 10 issues to calibrate quality. Adjust the classification prompt if the agent is miscategorizing.

### 2. Automate monthly release cadence

Run the `github-community-automation` drill, Step 2:

Build an n8n workflow on a monthly cron schedule (1st of each month, 10am):
1. Check if there are new commits since the last release
2. If yes: auto-generate release notes from merged PRs, increment patch version, publish the release with CTA in the body
3. If no: skip (do not publish empty releases)
4. Log in PostHog: `github_release_published` with `{repo, version, commit_count}`

### 3. Automate cross-channel amplification

Run the `github-community-automation` drill, Step 3:

Build an n8n workflow triggered by the release publish event:
1. Generate a social post using Claude: 2-3 sentences highlighting what is new and why it matters
2. Post to LinkedIn (via API or Buffer)
3. Post to Twitter/X (via API)
4. Post in relevant Discord/Slack communities (via webhook)
5. All links include UTM: `?utm_source=<platform>&utm_medium=social&utm_campaign=<repo>-<version>`

### 4. A/B test README elements

Run the `ab-test-orchestrator` drill:

Test one variable at a time, each test running for 2-4 weeks:
- **Test 1: CTA copy.** Variant A: current CTA. Variant B: different value proposition or urgency framing.
- **Test 2: CTA placement.** Variant A: CTA after "What It Does." Variant B: CTA after "Quick Start."
- **Test 3: Problem statement.** Variant A: current framing. Variant B: rewritten using different customer pain language.

Implementation: create branches with different README versions. Swap the default branch bi-weekly. Compare `github_readme_cta_clicked` rates in PostHog across periods.

**Guardrail:** If CTA click-through rate drops >30% during a test, revert immediately to the control README.

### 5. Expand the sample portfolio (optional multiplier)

If the first repo is working, create 1-2 additional sample repos targeting adjacent keywords. Each new repo follows the same `github-repo-setup` drill but targets a different ICP search query. This is the primary 10x lever: more repos = more keyword surface area = more organic discovery.

### 6. Evaluate against threshold

After 2 months, query PostHog:
- Total unique visitors across all repos: target >=1,000
- Total stars across all repos: target >=150
- Total leads: target >=15 (count of `github_signup_completed` or `github_demo_booked` with `utm_source=github`)
- All automation workflows running with <5% failure rate

If PASS: proceed to Durable. Document all workflows and their configurations.
If FAIL with strong traffic but low leads: CTA optimization needs more iterations -- continue A/B testing.
If FAIL with low traffic: the keyword space is too competitive or too niche -- research adjacent problem domains for new sample repos.

## Time Estimate

- 15 hours: n8n workflow development (issue triage, release automation, cross-posting)
- 10 hours: A/B test setup and README variant creation
- 10 hours: monitoring, reviewing AI-generated responses, calibrating prompts
- 15 hours: optional additional sample repos (if pursuing the portfolio strategy)
- 10 hours: threshold evaluation, documentation, Durable handoff

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| GitHub | Repository hosting and webhooks | Free for public repos ([github.com/pricing](https://github.com/pricing)) |
| PostHog | Event tracking, funnels, experiments | Free tier: 1M events/month ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Workflow automation (issue triage, releases, cross-posting) | Cloud Pro: EUR60/month for 10K executions ([n8n.io/pricing](https://n8n.io/pricing)) |
| Anthropic API | Claude for issue classification and social post generation | Haiku 4.5: $1/$5 per M tokens; ~$5-10/month at this volume ([claude.com/pricing](https://claude.com/pricing)) |
| Loops | Email list management (optional) | Free tier to $49/month ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated monthly cost at Scalable level: $65-120** (n8n Pro + Claude API usage)

## Drills Referenced

- `github-community-automation` -- automates issue triage, release cadence, cross-posting, contributor engagement
- `ab-test-orchestrator` -- designs and runs A/B tests on README CTA copy, placement, and framing
