---
name: github-sample-teaser-smoke
description: >
  GitHub Sample Teaser — Smoke Test. Publish a public repo with sample code,
  keyword-optimized README, and CTA to validate that developers in your ICP
  discover repos on GitHub and at least one converts to a lead.
stage: "Marketing > Problem Aware"
motion: "Directories & Marketplaces"
channels: "Other"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: ">=20 stars or >=100 unique visitors and >=1 lead in 1 week"
kpis: ["Unique repo visitors", "Stars", "Clones", "README CTA clicks", "Leads"]
slug: "github-sample-teaser"
install: "npx gtm-skills add marketing/problem-aware/github-sample-teaser"
drills:
  - github-repo-setup
  - threshold-engine
---

# GitHub Sample Teaser — Smoke Test

> **Stage:** Marketing > Problem Aware | **Motion:** Directories & Marketplaces | **Channels:** Other

## Outcomes

Prove that your ICP discovers open-source samples on GitHub and that a README CTA can convert a visitor into a lead. A passing Smoke Test means the repo attracted at least 20 stars or 100 unique visitors AND at least 1 person clicked through to your product signup or demo booking link. This confirms GitHub is a viable discovery channel before investing in automation.

## Leading Indicators

- Repo appears in GitHub search results for target keywords within 48 hours of publishing
- At least 10 unique visitors in the first 3 days (confirms search intent exists)
- At least 1 clone in the first 3 days (confirms developers evaluate the code, not just browse)
- At least 1 README CTA click within the first week (confirms the CTA placement and copy work)

## Instructions

### 1. Research the keyword landscape and pick the sample concept

Run the `github-repo-setup` drill, Step 1. Search GitHub for repos in your problem domain:

```bash
gh search repos "<your problem domain>" --limit 20 --json fullName,description,stargazersCount,repositoryTopics --sort stars
```

Identify:
- The 3-5 search terms your ICP uses when looking for solutions on GitHub
- Gaps in existing repos (common issues, missing features, outdated code)
- Naming patterns of top repos (these inform your repo name)

Pick a sample concept that solves a real, specific problem your ICP faces. The sample must be useful on its own -- not a demo of your product that only works with a paid account.

### 2. Create and publish the repository

Run the `github-repo-setup` drill, Steps 2-7:

1. Create a public repo with a keyword-rich name and description
2. Write a README following the exact structure: Title + Badges, Problem Statement, Quick Start, What It Does, CTA Block, Contributing, License
3. Add working sample code that runs from a fresh clone without errors
4. Set 8-12 topics based on your keyword research
5. Upload a social preview image (1280x640)
6. Set the homepage URL to your product site with UTM parameters

All CTA links must include UTM parameters: `?utm_source=github&utm_medium=readme&utm_campaign=<repo-slug>`

**Human action required:** Upload the social preview image via GitHub repo settings UI. Create the actual sample code (agent can scaffold the structure and README, but the code must solve a real problem your team understands).

### 3. Seed initial distribution

Share the repo in 2-3 places where your ICP already is:
- Post in 1 relevant subreddit (follow the subreddit rules on self-promotion)
- Share on your personal LinkedIn with a problem-first framing
- Post in 1 relevant Discord or Slack community

Do NOT run a full launch campaign at Smoke level. This is about organic discoverability, not manufactured traffic.

### 4. Monitor traffic daily

Check GitHub traffic via CLI each day for 7 days:

```bash
gh api repos/<org>/<repo>/traffic/views
gh api repos/<org>/<repo>/traffic/clones
gh api repos/<org>/<repo> --jq '.stargazers_count'
```

Also check your product analytics (PostHog) for visitors arriving via the UTM parameters on your README CTA links.

### 5. Evaluate against threshold

Run the `threshold-engine` drill after 1 week:
- Query GitHub API for total unique visitors (target: >=100) or star count (target: >=20)
- Query PostHog for `github_readme_cta_clicked` events (target: >=1 lead)
- If PASS: proceed to Baseline Run
- If FAIL with >50 visitors but 0 CTA clicks: the CTA copy or placement is wrong -- rewrite and reposition
- If FAIL with <30 visitors: keywords or repo name are not reaching your ICP -- research new keywords, rename the repo, update topics
- If FAIL with visitors but 0 stars: the sample code is not compelling enough -- improve the Quick Start or add more useful features

## Time Estimate

- 1.5 hours: keyword research + repo creation + README writing + topic optimization
- 1 hour: sample code scaffolding and testing
- 15 minutes: social preview creation + initial distribution posts
- 15 minutes: threshold evaluation after 1 week

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| GitHub | Repository hosting | Free for public repos ([github.com/pricing](https://github.com/pricing)) |
| PostHog | Track CTA click-throughs from README links | Free tier: 1M events/month ([posthog.com/pricing](https://posthog.com/pricing)) |
| Loops | Email capture if CTA points to a waitlist | Free tier: 1,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated monthly cost at Smoke level: $0** (all tools within free tiers)

## Drills Referenced

- `github-repo-setup` -- scaffolds the repo with README, topics, social preview, and analytics
- `threshold-engine` -- evaluates visitor count, star count, and lead count against pass threshold
