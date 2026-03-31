---
name: open-source-content-release-scalable
description: >
  Open Source Content Release — Scalable Automation. Automate issue triage, release publishing,
  cross-channel amplification, and community engagement. Expand to multiple OSS repos and run
  README A/B tests to find the 10x multiplier on stars and lead generation.
stage: "Marketing > Solution Aware"
motion: "Content"
channels: "Communities, Social, Content"
level: "Scalable Automation"
time: "40 hours over 3 months"
outcome: ">=1,000 total GitHub stars across all repos, >=50 qualified leads from OSS, and >=3% README CTA conversion rate over 6 months"
kpis: ["Total stars across repos", "Qualified leads from OSS", "README CTA conversion rate", "Issue response time (automated)", "Release cadence adherence"]
slug: "open-source-content-release"
install: "npx gtm-skills add marketing/solution-aware/open-source-content-release"
drills:
  - github-community-automation
  - ab-test-orchestrator
  - content-repurposing
---

# Open Source Content Release — Scalable Automation

> **Stage:** Marketing > Solution Aware | **Motion:** Content | **Channels:** Communities, Social, Content

## Outcomes

Issue triage, release publishing, and cross-channel amplification run autonomously via n8n workflows. The README CTA is continuously tested and optimized. A second (or third) OSS repo is launched using the validated playbook from Smoke and Baseline. The combined portfolio reaches >=1,000 total stars and >=50 qualified leads with >=3% README CTA conversion rate within 6 months.

## Leading Indicators

- Automated issue response time <10 minutes (triage classification + template response)
- Monthly releases publishing automatically with CTA and cross-channel posts
- A/B test on README CTA copy producing a statistically significant winner within 4 weeks
- Second repo reaching >=50 stars within 3 weeks of launch (proving the playbook repeats)
- Community posts (Reddit, HN, dev.to) about your OSS tools authored by people outside your team

## Instructions

### 1. Automate community engagement

Run the `github-community-automation` drill to build n8n workflows for:

- **Issue triage:** GitHub webhook triggers n8n on `issues.opened`. Claude classifies the issue (bug, feature request, question, spam) and responds with the appropriate template. Questions include a soft product CTA. All classifications logged to PostHog as `oss_issue_triaged`.
- **Release automation:** Monthly cron checks for new commits since the last release. If commits exist, auto-publishes a new semver release with generated notes and CTA in the release body. Cross-posts the release to LinkedIn, Twitter/X, and community channels.
- **Contributor engagement:** On `pull_request.opened` from first-time contributors, respond with a welcome message. On `pull_request.merged`, add contributor to README and send a thank-you via Loops.

After setup, verify each workflow fires correctly with a test issue, a manual release trigger, and a test PR.

### 2. Run README A/B tests

Run the `ab-test-orchestrator` drill to test README CTA variations:

**Test 1 (CTA copy):** Alternate between two CTA blocks in the README:
- Control: current CTA copy
- Variant: rewritten CTA emphasizing a specific outcome (e.g., "Automate this in production" vs. "Try the full platform free")

Implement by swapping the default branch between two branches with different READMEs on a bi-weekly rotation. Measure CTA click-through rate via PostHog UTM tracking. Run for 4 weeks (2 rotations per variant). Adopt the winner.

**Test 2 (README structure):** After Test 1, test section ordering:
- Control: current order (Problem > Quick Start > Features > CTA)
- Variant: move the CTA higher (Problem > Quick Start > CTA > Features)

Measure scroll depth and CTA clicks. Adopt the configuration that maximizes CTA conversion without reducing star rate.

### 3. Expand the OSS portfolio

Re-run the `oss-content-selection` drill (from Smoke level) to identify the next asset to release. Use the same playbook:
1. Select and extract the asset
2. Run `github-repo-setup` to publish
3. Run the Day 1-3 launch promotion from Smoke level
4. Immediately connect to the automated workflows from Step 1 (issue triage, release cadence, cross-posting)

Target: launch 1 additional repo every 6-8 weeks. Each repo targets a different keyword cluster to maximize search surface.

### 4. Amplify through content repurposing

Run the `content-repurposing` drill to turn the OSS release into multi-format content:

- Extract 3-5 key insights from the repo's documentation and turn each into a LinkedIn post
- Record a 60-90 second walkthrough video showing the Quick Start running
- Write a newsletter section highlighting one creative use case
- Create a Twitter/X thread walking through the architecture

Spread these across 3 weeks to extend the content lifecycle. Each piece links back to the repo with UTM parameters.

### 5. Build a community content flywheel

Using the `community-content-posting` drill patterns, post about your OSS tools in developer communities on a bi-weekly cadence:
- Answer questions on Stack Overflow, Reddit, and Discord that your tool solves -- link to the repo as the solution
- Write dev.to articles showing advanced use cases
- Respond to "what tool do you use for X?" threads with your OSS asset

Track which community channels produce the most repo traffic and leads. Focus effort on the top 3 channels.

### 6. Evaluate against threshold

After 6 months, measure against: >=1,000 total stars across all repos AND >=50 qualified leads AND >=3% README CTA conversion rate.

- **PASS:** Proceed to Durable. Document: top-performing repo, best promotion channels, winning CTA variant, pipeline contribution.
- **MARGINAL PASS:** Stay at Scalable for 2 more months. Focus on README optimization and community posting in highest-ROI channels.
- **FAIL:** Consolidate to the single highest-performing repo. Invest in improving that repo's quality and promotion before expanding.

## Time Estimate

- Community automation setup: 8 hours
- A/B test design and execution: 6 hours
- Second repo selection and launch: 12 hours
- Content repurposing: 6 hours
- Community content posting: 4 hours (ongoing, bi-weekly)
- Monitoring and threshold evaluation: 4 hours

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| GitHub | Host repos, webhooks, releases | Free for public repos |
| PostHog | Event tracking, A/B test measurement, funnels | Free up to 1M events/mo (https://posthog.com/pricing) |
| n8n | Issue triage, release automation, cross-posting | Free self-hosted or from EUR 20/mo cloud (https://n8n.io/pricing) |
| Anthropic | Claude API for issue classification and response | Pay-per-use, ~$3/1M input tokens (https://www.anthropic.com/pricing) |
| Attio | Lead tracking and campaign attribution | From $0/user/mo free tier (https://attio.com/pricing) |
| Loops | Contributor thank-you emails, release notifications | From $0/mo free tier (https://loops.so/pricing) |

**Play-specific cost:** ~$30-100/mo (n8n cloud + Anthropic API usage for issue triage)

_Your CRM, PostHog, and automation platform are not included -- standard stack paid once._

## Drills Referenced

- `github-community-automation` -- automate issue triage, release publishing, cross-posting, and contributor engagement
- `ab-test-orchestrator` -- design and run A/B tests on README CTA copy and structure
- `content-repurposing` -- transform OSS release into multi-format content across channels
