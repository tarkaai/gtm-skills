---
name: github-project-promotion-scalable
description: >
  GitHub Project Promotion — Scalable Automation. Scale from 1 repo to a portfolio
  of 3-5 sample repos, automate issue triage and release cadence, cross-post
  releases to social channels, and run README A/B tests to find the 10x multiplier.
stage: "Marketing > SolutionAware"
motion: "DirectoriesMarketplaces"
channels: "Communities, Social"
level: "Scalable Automation"
time: "50 hours over 3 months"
outcome: "≥2,000 total stars across repo portfolio and ≥30 qualified leads/quarter from GitHub presence"
kpis: ["Total stars across portfolio", "Qualified leads per quarter from GitHub", "Issue response time (automated)", "Release cadence (releases per month)", "Cross-post engagement rate"]
slug: "github-project-promotion"
install: "npx gtm-skills add marketing/solution-aware/github-project-promotion"
drills:
  - github-community-automation
  - github-repo-promotion
---

# GitHub Project Promotion — Scalable Automation

> **Stage:** Marketing → SolutionAware | **Motion:** DirectoriesMarketplaces | **Channels:** Communities, Social

## Outcomes

Scale from a single repo to a portfolio of 3-5 sample repos covering different ICP segments and keywords. Automate the manual work that made Baseline run: issue triage, release publishing, cross-channel amplification, and contributor engagement. Run README A/B tests to optimize conversion. Pass threshold: ≥2,000 total stars across the repo portfolio and ≥30 qualified leads/quarter from GitHub presence.

## Leading Indicators

- 3-5 repos live with optimized READMEs and active traffic collection
- Automated issue triage responding to new issues within 5 minutes (24/7)
- Monthly automated releases publishing without manual intervention
- Cross-post workflow reaching 3+ channels per release within 1 hour
- README A/B test producing a statistically significant winner within 4 weeks
- Portfolio-wide star growth rate ≥50 stars/week across all repos

## Instructions

### 1. Expand the repo portfolio

Create 2-4 additional sample repos targeting different keywords and ICP segments. For each new repo, run the `github-repo-setup` drill (from Smoke) and the `github-repo-promotion` drill (launch sequence):

- Map your ICP's top 5 pain points. Each repo should address a distinct pain point.
- Research keyword gaps: `gh search repos "<pain point keyword>" --limit 10 --json fullName,stargazersCount --sort stars` — look for problems with high search volume but few quality repos (<500 stars on the top result).
- Create each repo with a keyword-optimized name, full README with CTA, topics SEO, and social preview.
- Run the launch sequence for each new repo: social posts, community posts, HN/dev.to, email broadcast.
- Configure the n8n daily traffic collection workflow (from Baseline) to cover all repos in the portfolio.

Portfolio strategy:
- **1 flagship repo** (your best sample from Smoke/Baseline) — gets the most promotion effort
- **2-3 niche repos** targeting long-tail keywords with less competition
- **1 integration repo** (optional) showing how your product integrates with a popular framework or tool

### 2. Automate community management

Run the `github-community-automation` drill to set up n8n workflows for all repos in the portfolio:

**Issue triage (triggered by GitHub webhook `issues.opened`):**
1. Receive the new issue payload
2. Classify using Claude via Anthropic API: bug report, feature request, question/support, or spam
3. Auto-label and auto-respond:
   - Bug: label `bug`, respond requesting reproduction steps
   - Feature request: label `enhancement`, acknowledge and link to roadmap
   - Question: label `question`, answer from README/docs, include product CTA with UTM: `?utm_source=github&utm_medium=issue_response&utm_campaign=<repo>`
   - Spam: label `invalid`, close with polite note
4. Log in PostHog: `github_issue_triaged` with `{repo, classification, response_time_seconds}`

**Automated release cadence (monthly cron):**
1. Check for new commits since last release: `gh api repos/<org>/<repo>/compare/<last-tag>...main --jq '.total_commits'`
2. If commits > 0: auto-generate release notes from merged PRs, increment patch version, publish via `gh release create --generate-notes`
3. Include CTA in release body with UTM parameters
4. Log in PostHog: `github_release_published` with `{repo, version, commit_count}`

**Cross-post releases (triggered by `release.published` webhook):**
1. Generate a social post using Claude: 2-3 sentences highlighting what is new and why it matters
2. Post to LinkedIn, Twitter/X, and relevant Discord/Slack communities
3. All links include UTM: `?utm_source=<platform>&utm_medium=social&utm_campaign=<repo>-<version>`
4. Log in PostHog: `github_release_cross_posted` with `{repo, version, platforms}`

**Contributor engagement (triggered by PR webhooks):**
1. First-time contributor: welcome message + link to CONTRIBUTING.md
2. PR merged: thank-you message + add to contributors list
3. If contributor email is available: enroll in Loops sequence for developer advocates

### 3. Run README A/B tests

Use the `github-community-automation` drill's README testing workflow:

1. Formulate 2-3 hypotheses about README changes that could improve CTA click-through rate. Examples:
   - Move the CTA block higher (after Quick Start instead of after Architecture)
   - Change the CTA copy from "Try it free" to "See how [Product] automates this"
   - Add a GIF showing the tool in action before the CTA
2. Create branches with different README versions
3. Swap the default branch bi-weekly to test each variant
4. Compare CTA click-through rates across 2-week periods in PostHog
5. Adopt the winner. Document the lift for the next optimization cycle.

Run 2-3 README A/B tests during the 3-month Scalable period.

### 4. Consolidate the portfolio dashboard

Expand the Baseline PostHog dashboard to cover the full portfolio:

- Summary panel: total stars, total views, total leads across all repos
- Per-repo breakdown: stars, views, clones, CTA clicks, leads for each repo
- Automation health: issue response time, releases published this month, cross-posts completed
- README A/B test results: variant performance comparison

### 5. Evaluate against threshold

After 3 months, measure:

- Total stars across all repos in the portfolio (target: ≥2,000)
- Qualified leads per quarter from GitHub presence (target: ≥30)
- Issue response time (automated — should be <5 minutes)
- Release cadence (should be ≥1 release/repo/month)
- Cross-post engagement: average likes/comments per release post
- README A/B test results: cumulative CTA click-through rate improvement

If PASS: proceed to Durable. Document which repos drive the most leads (not just stars), which promotion channels have the highest ROI, and the current CTA click-through rate benchmark.
If FAIL: diagnose per-repo performance. Are some repos getting stars but no leads? (CTA needs work — run more A/B tests.) Is the portfolio too broad? (Consolidate to the 2 highest-performing repos and invest deeper.) Is automation failing silently? (Check n8n workflow execution logs for errors.)

## Time Estimate

- 12 hours: create and launch 2-4 additional repos (3-4 hours each including code, README, launch)
- 10 hours: set up n8n automation workflows (issue triage, release cadence, cross-posting, contributor engagement)
- 8 hours: README A/B testing (hypothesis generation, branch creation, analysis) across 2-3 tests
- 10 hours: ongoing promotion cadence across portfolio (bi-weekly posts, community engagement)
- 5 hours: dashboard expansion, weekly monitoring, evaluation
- 5 hours: debugging automation, tuning Claude classification prompts, workflow maintenance

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| GitHub | Repository hosting, webhooks, traffic APIs | Free for public repos — https://github.com/pricing |
| PostHog | Portfolio-wide tracking, dashboards, A/B test analysis | Free up to 1M events/mo — https://posthog.com/pricing |
| n8n | Issue triage, release automation, cross-posting workflows | Cloud from $24/mo or free self-hosted — https://n8n.io/pricing |
| Anthropic (Claude) | Issue classification, release post generation, README drafting | ~$10-20/mo at portfolio scale — https://anthropic.com/pricing |
| Attio | CRM for lead tracking across repo portfolio | Free up to 3 users — https://attio.com/pricing |
| Loops | Developer nurture sequences for GitHub-sourced leads | Free up to 1,000 contacts — https://loops.so/pricing |

**Scalable budget: n8n ~$24/mo + Claude API ~$10-20/mo = ~$35-45/mo** (other tools covered by free tiers or standard stack)

## Drills Referenced

- `github-community-automation` — n8n workflows for automated issue triage, monthly releases, cross-channel release amplification, contributor engagement, and README A/B testing
- `github-repo-promotion` — launch sequence for each new repo in the portfolio plus ongoing bi-weekly promotion cadence
