---
name: github-sample-teaser-baseline
description: >
  GitHub Sample Teaser — Baseline Run. First always-on automation: daily traffic
  collection, structured promotion cadence, first release cycle, and persistent
  PostHog tracking to prove GitHub-sourced leads are repeatable over 2 weeks.
stage: "Marketing > Problem Aware"
motion: "Directories & Marketplaces"
channels: "Other"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: ">=50 stars or >=300 unique visitors and >=3 leads over 2 weeks"
kpis: ["Unique repo visitors", "Stars gained", "Clones", "README CTA click-through rate", "Leads attributed to GitHub"]
slug: "github-sample-teaser"
install: "npx gtm-skills add marketing/problem-aware/github-sample-teaser"
drills:
  - github-repo-promotion
  - posthog-gtm-events
---

# GitHub Sample Teaser — Baseline Run

> **Stage:** Marketing > Problem Aware | **Motion:** Directories & Marketplaces | **Channels:** Other

## Outcomes

Prove that GitHub-sourced traffic and leads are repeatable, not a one-time launch spike. A passing Baseline means the repo maintained steady traffic over 2 weeks (>=300 unique visitors or >=50 stars) and generated >=3 leads through the README CTA. Critically, the daily traffic collection automation is running -- you now have persistent GitHub metrics in PostHog beyond GitHub's 14-day retention window.

## Leading Indicators

- Daily n8n workflow successfully collecting GitHub traffic data to PostHog (zero missed days)
- Traffic does not drop >50% after the first launch week (confirms organic discovery, not just launch buzz)
- At least 1 new referral source appearing in top referrers (confirms cross-channel promotion is working)
- CTA click-through rate > 0.5% of unique visitors (confirms the README CTA converts at a sustainable rate)

## Instructions

### 1. Set up persistent traffic tracking

Run the `posthog-gtm-events` drill to establish the event taxonomy, then run the `github-repo-promotion` drill, Step 3 to build the daily n8n workflow:

The n8n workflow runs every 24 hours and:
1. Calls the GitHub Traffic API for views, clones, referrers, and star count
2. Sends each data point to PostHog as custom events:
   - `github_repo_views` with properties `{repo, count, uniques, date}`
   - `github_repo_clones` with properties `{repo, count, uniques, date}`
   - `github_repo_stars` with properties `{repo, total_stars, new_stars, date}`
   - `github_repo_referrer` with properties `{repo, referrer, count, uniques, date}`
3. Stores the raw JSON in Attio as a note on the campaign record

Also set up tracking on the landing page / product site:
- `github_readme_cta_clicked` (fires when someone arrives via UTM `utm_source=github`)
- `github_demo_booked` (fires when a GitHub-sourced visitor books a demo)
- `github_signup_completed` (fires when a GitHub-sourced visitor signs up)

### 2. Execute the launch promotion sequence

Run the `github-repo-promotion` drill, Steps 1-2:

**Day 1-2 launch blitz:**
- LinkedIn post: problem-first framing with repo link (UTM: `utm_source=linkedin`)
- Twitter/X post: hook + code screenshot + repo link (UTM: `utm_source=twitter`)
- 2-3 relevant subreddits (follow each subreddit's self-promotion rules)
- 1-2 relevant Discord/Slack developer communities
- Hacker News: `Show HN: <repo name> — <one-line description>`
- dev.to article: explain the problem, how the sample solves it, link to repo

**Day 2 email blast (if you have an existing list):**
- Send a one-time broadcast to relevant segments via Loops
- Subject: "We open-sourced [thing] -- here's the repo"
- Tag clicks with `source: github-sample-announcement`

### 3. Publish the first release

Run the `github-repo-promotion` drill, Step 4:
- Create a `v1.0.0` release within the first week
- Include CTA in release notes with UTM: `?utm_source=github&utm_medium=release&utm_campaign=<repo>-v1.0.0`
- Releases trigger notifications to all stargazers -- this is free re-engagement

### 4. Run the 2-week promotion cadence

After the initial launch:
- **End of week 1:** Check PostHog for top referral sources. Identify which channel drove the most clones (not just views -- clones indicate real evaluation). Post a follow-up in the top-performing channel.
- **End of week 2:** Post an update or tip on social media that demonstrates a specific use case of the sample. Link back to the repo.

### 5. Evaluate against threshold

After 2 weeks, query PostHog:
- Total unique visitors: target >=300 (sum daily `github_repo_views` uniques)
- Total stars: target >=50 (latest `github_repo_stars` total)
- Total leads: target >=3 (count of `github_readme_cta_clicked` leading to `github_signup_completed` or `github_demo_booked`)
- CTA click-through rate: total CTA clicks / total unique visitors

If PASS: proceed to Scalable. Document which promotion channels drove the most qualified traffic.
If FAIL with strong traffic but low leads: the CTA copy or placement is wrong -- A/B test CTA variants.
If FAIL with low traffic: the keyword targeting or promotion channels are wrong -- research new keywords, try different communities.

## Time Estimate

- 3 hours: n8n workflow setup + PostHog event configuration
- 4 hours: launch promotion sequence (writing posts, submitting to communities)
- 2 hours: first release preparation and publishing
- 2 hours: mid-point review + follow-up posts
- 1 hour: final threshold evaluation and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| GitHub | Repository hosting and traffic API | Free for public repos ([github.com/pricing](https://github.com/pricing)) |
| PostHog | Event tracking and traffic persistence | Free tier: 1M events/month ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Daily traffic collection automation | Free self-hosted; Cloud Starter: EUR24/month ([n8n.io/pricing](https://n8n.io/pricing)) |
| Loops | Email broadcast to existing list | Free tier: 1,000 contacts; Paid from $49/month ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated monthly cost at Baseline level: $0-24** (n8n cloud optional; all other tools within free tiers)

## Drills Referenced

- `github-repo-promotion` -- launch distribution, daily traffic collection, first release, ongoing cadence
- `posthog-gtm-events` -- standardized event taxonomy for GitHub traffic and conversion events
