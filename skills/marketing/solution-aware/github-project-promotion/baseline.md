---
name: github-project-promotion-baseline
description: >
  GitHub Project Promotion — Baseline Run. First always-on automation: daily
  GitHub traffic collection persisted to PostHog, ongoing promotion cadence,
  and CRM-routed lead capture from README CTAs.
stage: "Marketing > SolutionAware"
motion: "DirectoriesMarketplaces"
channels: "Communities, Social"
level: "Baseline Run"
time: "20 hours over 8 weeks"
outcome: "≥300 GitHub stars and ≥10 qualified developer leads (CRM-tracked) over 8 weeks"
kpis: ["GitHub stars gained per week", "README CTA click-through rate", "Qualified leads from GitHub UTM", "Clone-to-lead conversion rate", "Top referral source traffic"]
slug: "github-project-promotion"
install: "npx gtm-skills add marketing/solution-aware/github-project-promotion"
drills:
  - posthog-gtm-events
  - github-repo-promotion
---

# GitHub Project Promotion — Baseline Run

> **Stage:** Marketing → SolutionAware | **Motion:** DirectoriesMarketplaces | **Channels:** Communities, Social

## Outcomes

Convert the Smoke test's manual tracking into an always-on system: daily GitHub traffic data persisted to PostHog (solving GitHub's 14-day retention limit), CRM-routed lead capture from README CTAs, and a repeatable bi-weekly promotion cadence. Pass threshold: ≥300 GitHub stars and ≥10 qualified developer leads tracked in Attio over 8 weeks.

## Leading Indicators

- n8n workflow collecting daily GitHub traffic data without failures for 2+ consecutive weeks
- Star growth rate ≥15 stars/week sustained over 4+ weeks
- At least 2 different referral sources each contributing ≥10% of total traffic (not over-reliant on one channel)
- Leads from GitHub flowing into Attio with correct source attribution within 24 hours of conversion
- Bi-weekly social posts consistently generating ≥5 engagements (likes, comments, reposts)

## Instructions

### 1. Configure always-on tracking

Run the `posthog-gtm-events` drill to instrument the following events:

- `github_repo_views` — daily views (total + unique) per repo, collected via n8n cron calling `gh api repos/<org>/<repo>/traffic/views`
- `github_repo_clones` — daily clones (total + unique), collected via `gh api repos/<org>/<repo>/traffic/clones`
- `github_repo_stars` — current star count snapshot, collected via `gh api repos/<org>/<repo> --jq '.stargazers_count'`
- `github_repo_referrer` — top referral sources, collected via `gh api repos/<org>/<repo>/traffic/popular/referrers`
- `github_readme_cta_clicked` — fired on your landing page when a visitor arrives with `utm_source=github`
- `github_demo_booked` — fired when a GitHub-sourced visitor books a demo via Cal.com
- `github_signup_completed` — fired when a GitHub-sourced visitor completes signup

Build the n8n workflow: daily cron trigger at 06:00 UTC → call all 4 GitHub traffic API endpoints → send each data point to PostHog as a custom event with properties `{repo, count, uniques, date}` → store raw JSON as a note in Attio on the campaign record.

This solves GitHub's 14-day traffic data retention by persisting all data in PostHog.

### 2. Wire CRM lead capture

Configure the lead capture pipeline for GitHub-sourced visitors:

- On your landing page (where README CTA links point), detect `utm_source=github` and `utm_campaign=<repo>` from URL parameters
- When a visitor with GitHub UTM parameters books a demo or signs up, fire a PostHog event and trigger an n8n webhook
- n8n workflow: create a contact in Attio with `first_touch_channel: github`, `first_touch_campaign: <repo>`, and `first_touch_date: <timestamp>`
- Create a deal at the "Lead Captured" stage in Attio with the repo name as context
- Enroll the lead in a Loops nurture sequence tailored to developers: technical content, code examples, integration guides — not generic marketing

### 3. Execute ongoing promotion cadence

Continue running the `github-repo-promotion` drill on a repeating schedule:

- **Bi-weekly:** Post a tip, use case, or code snippet on LinkedIn and Twitter/X that links back to the repo. Vary the angle each time: "How to use [repo] for [use case]", "TIL you can [trick] with [repo]", "[Repo] now supports [feature]"
- **Monthly:** Publish a new release via `gh release create`. Even minor updates (README improvements, new examples, dependency bumps) justify a release. Each release notifies all stargazers.
- **Monthly:** Write and publish a dev.to or blog post about a specific use case solved by the sample. Link to the repo with UTM parameters.
- **Weekly:** Check top referral sources in PostHog. If a new referral source appears (someone linked to your repo), amplify it — thank them publicly, repost their content, engage with their community.

### 4. Build the PostHog dashboard

Create a PostHog dashboard named "GitHub Project Promotion — Baseline" with:

- Line chart: daily views (total + unique) over last 60 days
- Line chart: stars gained per week over last 60 days
- Counter: current total star count
- Funnel: `github_repo_views` → `github_readme_cta_clicked` → `github_signup_completed` (or `github_demo_booked`)
- Table: top referral sources by unique visitors (last 30 days)
- Counter: total leads from GitHub (contacts with `first_touch_channel = github` in Attio)

### 5. Evaluate against threshold

After 8 weeks, measure:

- Total GitHub stars (target: ≥300)
- Qualified developer leads in Attio with `first_touch_channel: github` (target: ≥10)
- Star growth trend: is it accelerating, stable, or decelerating?
- README CTA click-through rate: clicks / views
- Clone-to-lead conversion: leads / clones
- Which referral sources drive the most qualified leads (not just traffic)

If PASS: proceed to Scalable. Document the promotion cadence that worked, which referral sources convert best, and the CTA click-through rate as the benchmark to beat.
If FAIL: diagnose — is star growth stalling? (Promotion cadence not reaching new audiences — try new communities or content angles.) Are stars growing but leads are not? (CTA is not compelling or is poorly positioned — A/B test CTA copy and placement.) Are clones high but signups low? (The sample works but the product pitch does not land — revise the CTA value proposition.)

## Time Estimate

- 4 hours: n8n workflow setup (daily traffic collection + CRM lead capture pipeline)
- 3 hours: PostHog event configuration and dashboard creation
- 2 hours: Loops nurture sequence for GitHub-sourced developer leads
- 8 hours: bi-weekly social posts, monthly releases, monthly blog posts over 8 weeks (~1 hour/week)
- 3 hours: weekly referral monitoring, evaluation, and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| GitHub | Repository hosting and traffic APIs | Free for public repos — https://github.com/pricing |
| PostHog | Event tracking, dashboards, funnel analysis | Free up to 1M events/mo — https://posthog.com/pricing |
| n8n | Daily cron workflows for traffic collection and lead routing | Free self-hosted or Cloud from $24/mo — https://n8n.io/pricing |
| Attio | CRM for lead tracking with source attribution | Free up to 3 users — https://attio.com/pricing |
| Loops | Developer-focused nurture email sequences | Free up to 1,000 contacts — https://loops.so/pricing |
| Cal.com | Demo booking links in README CTAs | Free for individuals — https://cal.com/pricing |
| Anthropic (Claude) | Social post and blog content generation | ~$2-5/mo at this cadence — https://anthropic.com/pricing |

**Baseline budget: n8n ~$24/mo** (if using cloud; free if self-hosted). All other tools covered by free tiers or standard stack.

## Drills Referenced

- `posthog-gtm-events` — configure daily GitHub traffic collection via n8n, CRM lead capture webhooks, and PostHog event instrumentation for the full GitHub → CTA → signup funnel
- `github-repo-promotion` — execute the ongoing bi-weekly social posts, monthly releases, monthly blog posts, and referral source amplification cadence
