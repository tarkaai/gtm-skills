---
name: open-source-content-release-smoke
description: >
  Open Source Content Release — Smoke Test. Select one internal asset (library, tool, dataset, or
  template), extract and publish it as an open-source GitHub repo, and promote it across developer
  channels to validate whether OSS content generates inbound interest from solution-aware technical
  audiences.
stage: "Marketing > Solution Aware"
motion: "Content"
channels: "Communities, Social, Content"
level: "Smoke Test"
time: "12 hours over 2 weeks"
outcome: ">=50 GitHub stars and >=3 inbound inquiries (issues, DMs, or demo requests) within 3 weeks of launch"
kpis: ["GitHub stars", "README CTA click-through rate", "Inbound inquiries from OSS"]
slug: "open-source-content-release"
install: "npx gtm-skills add marketing/solution-aware/open-source-content-release"
drills:
  - github-repo-setup
  - threshold-engine
---

# Open Source Content Release — Smoke Test

> **Stage:** Marketing > Solution Aware | **Motion:** Content | **Channels:** Communities, Social, Content

## Outcomes

The agent selects one internal asset to open-source, publishes it as a fully optimized GitHub repo, and manually promotes it across 3-5 developer channels. Success means the repo accumulates >=50 stars and generates >=3 inbound inquiries (GitHub issues asking about your product, DMs from developers, or demo bookings via the README CTA) within 3 weeks.

## Leading Indicators

- Stars accumulating in the first 72 hours after launch (>=15 in first 3 days signals traction)
- README CTA clicks tracked via UTM parameters in PostHog
- GitHub Traffic API showing referral traffic from at least 2 distinct sources
- Issues or discussions opened by external users (not your team)
- Forks by users outside your org

## Instructions

### 1. Select the asset to open-source

Run the the oss content selection workflow (see instructions below) drill to identify and score candidate internal assets. The drill produces a ranked list -- take the top-scoring candidate that passes legal/IP review.

Key criteria: the asset must deliver standalone value without requiring your paid product, it must be extractable in under 40 hours of work, and it must connect to a pain point your ICP actively searches for.

**Human action required:** Confirm legal clearance for open-source release under MIT license. Verify no customer data, API keys, or proprietary algorithms are included.

### 2. Build and publish the repository

Run the `github-repo-setup` drill to create the public repo. This drill handles:
- Keyword research for repo naming and topics
- Creating the repo with optimized name, description, and 8-12 topics
- Writing the README with problem statement, Quick Start, CTA block with UTM parameters
- Adding the sample code with proper structure (src/, examples/, CONTRIBUTING.md)
- Setting the social preview image
- Instrumenting PostHog analytics on the linked landing page

Verify the Quick Start works from a fresh clone on a clean machine. If it fails, fix before promoting.

### 3. Promote the launch manually

Execute a one-time launch push across developer channels within 48 hours of publishing:

**Day 1 posts (social):**
- LinkedIn post: lead with the problem the asset solves, mention you open-sourced a solution, link to repo with `?utm_source=linkedin&utm_medium=social&utm_campaign=<repo>-launch`
- Twitter/X post: short hook + code screenshot or terminal output + repo link with UTM
- Post in 2-3 relevant subreddits (follow each subreddit's self-promotion rules). Frame as: "I built [tool] to solve [problem] and open-sourced it"

**Day 2 posts (developer platforms):**
- Submit to Hacker News as `Show HN: <repo name> -- <one-line description>`
- Publish a dev.to article explaining the problem, what the tool does, and how to use it
- Post in relevant Discord/Slack developer communities

**Day 3-5:**
- Reply to every GitHub issue, comment, and star notification
- Engage with comments on social posts and community threads
- DM anyone who asks interesting questions -- offer to help and mention your product only if directly relevant

**Human action required:** Post content manually on each platform. Engage with comments personally for the first week.

### 4. Track initial performance

Monitor these metrics daily for 3 weeks:
- Star count (via `gh api repos/<org>/<repo>` -- check `stargazers_count`)
- Traffic views and clones (via GitHub Traffic API -- note 14-day retention limit)
- README CTA clicks (via PostHog UTM tracking)
- Referral sources (via GitHub Traffic API referrers endpoint)
- Issues, discussions, and forks (via GitHub API)
- Inbound inquiries: any DM, email, or demo booking that mentions the OSS repo

Log all metrics in Attio on the campaign record.

### 5. Evaluate against threshold

Run the `threshold-engine` drill to measure results against: >=50 GitHub stars AND >=3 inbound inquiries within 3 weeks.

- **PASS:** Proceed to Baseline. Document which channels drove the most stars and inquiries.
- **MARGINAL PASS (30-49 stars or 1-2 inquiries):** Stay at Smoke. Improve README CTA copy, re-promote on channels that showed promise, and re-evaluate in 2 more weeks.
- **FAIL (<30 stars and 0 inquiries):** Re-run the oss content selection workflow (see instructions below) -- the asset may not match ICP demand. Try the second-ranked candidate.

## Time Estimate

- Asset selection and legal review: 3 hours
- Repo setup and code extraction: 5 hours
- Launch promotion and engagement: 3 hours
- Tracking and threshold evaluation: 1 hour

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| GitHub | Host the open-source repo | Free for public repos |
| PostHog | Track README CTA clicks and landing page conversions | Free up to 1M events/mo (https://posthog.com/pricing) |
| Attio | Log campaign metrics and inbound inquiries | From $0/user/mo free tier (https://attio.com/pricing) |

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included -- standard stack paid once._

## Drills Referenced

- the oss content selection workflow (see instructions below) -- research, score, and select the internal asset to open-source
- `github-repo-setup` -- scaffold the public repo with README CTA, analytics, topics SEO, and social preview
- `threshold-engine` -- evaluate pass/fail and decide whether to advance to Baseline
