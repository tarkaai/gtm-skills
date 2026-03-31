---
name: open-source-content-release-baseline
description: >
  Open Source Content Release — Baseline Run. Instrument always-on tracking, publish companion
  content, establish a release cadence, and build automated lead capture from the open-source repo
  to validate sustained inbound generation over 8 weeks.
stage: "Marketing > Solution Aware"
motion: "Content"
channels: "Communities, Social, Content"
level: "Baseline Run"
time: "20 hours over 8 weeks"
outcome: ">=200 total GitHub stars, >=15 qualified leads attributed to OSS, and a repeatable monthly release cadence in 8 weeks"
kpis: ["Total GitHub stars", "Qualified leads from OSS", "README CTA conversion rate", "Monthly release cadence"]
slug: "open-source-content-release"
install: "npx gtm-skills add marketing/solution-aware/open-source-content-release"
drills:
  - posthog-gtm-events
  - github-repo-promotion
  - blog-seo-pipeline
---

# Open Source Content Release — Baseline Run

> **Stage:** Marketing > Solution Aware | **Motion:** Content | **Channels:** Communities, Social, Content

## Outcomes

The repo has always-on event tracking, a companion blog post driving organic traffic, an automated daily traffic persistence workflow, and a monthly release cadence that re-engages stargazers. The repo reaches >=200 total stars with >=15 qualified leads attributed to OSS channels (GitHub referral, UTM-tagged traffic) in 8 weeks.

## Leading Indicators

- Daily GitHub traffic data flowing into PostHog without gaps
- Companion blog post ranking for target keyword within 4 weeks
- Each monthly release generating a measurable star bump (>=10 new stars within 48 hours of release)
- README CTA conversion rate (clicks / unique views) >=2%
- Leads with `first_touch_channel = github` appearing in Attio

## Instructions

### 1. Instrument event tracking

Run the `posthog-gtm-events` drill to establish the event taxonomy for this play. Define and implement these events:

- `oss_repo_viewed` -- daily aggregate from GitHub Traffic API (views count + uniques)
- `oss_repo_cloned` -- daily aggregate from GitHub Traffic API (clones count + uniques)
- `oss_repo_starred` -- daily delta in star count
- `oss_readme_cta_clicked` -- fired when a visitor arrives at your site via a README UTM link
- `oss_demo_booked` -- fired when a GitHub-sourced visitor books a demo
- `oss_signup_completed` -- fired when a GitHub-sourced visitor signs up
- `oss_issue_opened` -- count of new issues by external users
- `oss_referrer_traffic` -- daily referrer breakdown from GitHub Traffic API

All events should carry properties: `repo`, `date`, `source` (github/linkedin/hackernews/etc).

### 2. Build the traffic persistence workflow

GitHub's Traffic API only retains 14 days of data. Build an n8n workflow (per the `github-repo-promotion` drill, Step 3) that runs daily at 6am:

1. Query GitHub Traffic API for views, clones, referrers, and star count
2. Send each data point to PostHog as the custom events defined in Step 1
3. Store raw JSON as an Attio note on the campaign record (backup)

This workflow runs indefinitely from this point forward. Verify it produces data for 3 consecutive days before moving to the next step.

### 3. Publish companion blog content

Run the `blog-seo-pipeline` drill to write and publish a blog post that targets the same keyword space as the repo. The post should:

- Explain the problem the OSS asset solves (use the same framing as the README)
- Show 2-3 use cases with code examples pulled from the repo
- Link to the repo with UTM: `?utm_source=blog&utm_medium=content&utm_campaign=<repo>-companion`
- Include a CTA for your paid product positioned as the next step after the OSS tool

The blog post serves as a second discovery surface -- developers who find the post via Google search are directed to the repo, and vice versa.

### 4. Establish release cadence

Using the `github-repo-promotion` drill (Steps 4-5), establish a monthly release cadence:

- **Week 4:** Publish v1.1.0 with at least one improvement (bug fix, new example, documentation update, or minor feature). Include a CTA in the release notes with UTM parameters.
- **Week 8:** Publish v1.2.0 with accumulated improvements.

Each release triggers notifications to all stargazers. After each release:
- Post a brief update on LinkedIn and Twitter mentioning the release
- Reply to any open issues that the release addresses
- Send a one-time email to relevant Loops segments announcing the update

### 5. Set up lead attribution

Configure Attio to tag leads by source. When a new contact arrives via a GitHub UTM link:

1. Set `first_touch_channel = github` and `first_touch_campaign = <repo-slug>` on the contact
2. Add the contact to an "OSS Leads" list in Attio
3. If the contact books a demo, tag the deal with `source = oss-content-release`

This attribution chain lets you measure real pipeline contribution from the OSS play.

### 6. Evaluate against threshold

After 8 weeks, measure against: >=200 total GitHub stars AND >=15 qualified leads AND at least 2 releases published.

- **PASS:** Proceed to Scalable. Document: top referral sources, CTA conversion rate, lead quality scores.
- **MARGINAL PASS (150-199 stars or 10-14 leads):** Stay at Baseline for 4 more weeks. Improve the blog post, optimize README CTA copy, and promote the next release more aggressively.
- **FAIL:** Review whether the asset matches ICP demand. Consider running the oss content selection workflow (see instructions below) again or pivoting promotion channels.

## Time Estimate

- Event tracking setup: 3 hours
- Traffic persistence workflow: 2 hours
- Blog post research and writing: 6 hours
- Two monthly releases: 4 hours (2 hours each)
- Lead attribution setup: 2 hours
- Monitoring and threshold evaluation: 3 hours

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| GitHub | Host repo, releases, traffic API | Free for public repos |
| PostHog | Event tracking, funnels, attribution | Free up to 1M events/mo (https://posthog.com/pricing) |
| n8n | Daily traffic persistence workflow | Free self-hosted or from EUR 20/mo cloud (https://n8n.io/pricing) |
| Ghost | Companion blog post | From $0 self-hosted or $9/mo (https://ghost.org/pricing/) |
| Attio | Lead attribution and campaign tracking | From $0/user/mo free tier (https://attio.com/pricing) |
| Loops | Email notification on releases | From $0/mo free tier (https://loops.so/pricing) |

**Play-specific cost:** ~$0-30/mo (if using free tiers of all tools)

_Your CRM, PostHog, and automation platform are not included -- standard stack paid once._

## Drills Referenced

- `posthog-gtm-events` -- define and implement the event taxonomy for OSS tracking
- `github-repo-promotion` -- distribute the repo, build the traffic persistence workflow, establish release cadence
- `blog-seo-pipeline` -- research, write, and publish a companion blog post targeting the same keyword space
