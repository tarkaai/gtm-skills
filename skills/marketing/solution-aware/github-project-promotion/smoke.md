---
name: github-project-promotion-smoke
description: >
  GitHub Project Promotion — Smoke Test. Set up one GitHub sample repo with
  optimized README, topics SEO, social preview, and launch promotion across
  developer channels to validate that GitHub presence generates stars and leads.
stage: "Marketing > SolutionAware"
motion: "DirectoriesMarketplaces"
channels: "Communities, Social"
level: "Smoke Test"
time: "8 hours over 2 weeks"
outcome: "≥50 GitHub stars and ≥3 inbound developer leads (demo bookings or signups via README CTA) in 3 weeks"
kpis: ["GitHub stars gained", "README CTA click-through rate", "Inbound leads from GitHub UTM", "Repo clone count"]
slug: "github-project-promotion"
install: "npx gtm-skills add marketing/solution-aware/github-project-promotion"
drills:
  - github-repo-setup
  - github-repo-promotion
---

# GitHub Project Promotion — Smoke Test

> **Stage:** Marketing → SolutionAware | **Motion:** DirectoriesMarketplaces | **Channels:** Communities, Social

## Outcomes

Prove that a well-optimized GitHub sample repo generates developer attention (stars, clones) and converts visitors into leads (demo bookings or signups via README CTA links). Pass threshold: ≥50 GitHub stars and ≥3 inbound developer leads within 3 weeks of launch.

## Leading Indicators

- Repository indexed by Google within 48 hours of creation (search `site:github.com/<org>/<repo>`)
- At least 10 stars within the first 72 hours of launch promotion
- README CTA receives ≥1 click within the first week (tracked via UTM parameters in PostHog)
- At least 1 community post (Reddit, HN, Discord) generates ≥5 upvotes or reactions
- Repo clones >20 in the first 2 weeks (indicates developers are actually trying the code)

## Instructions

### 1. Choose the sample project

Select one code sample, tool, or library that solves a specific problem your ICP faces. The sample must:
- Run without errors from a fresh `git clone` (test on a clean machine)
- Not require paid API keys or services to run the basic example
- Solve a pain point your ICP actively searches for on GitHub (validate by running `gh search repos "<problem keyword>" --limit 20 --json fullName,stargazersCount --sort stars`)
- Be small enough to understand in 15 minutes but useful enough to star

If you do not have a sample ready, build a minimal one: a CLI tool, a webhook handler, an API client, a framework integration, or a config generator targeting your ICP's stack.

### 2. Set up the repository

Run the `github-repo-setup` drill:

- Research competing repos in the space: `gh search repos "<problem domain>" --limit 20 --json fullName,description,stargazersCount,repositoryTopics --sort stars`
- Create the repo with a keyword-optimized name (e.g., `webhook-tester` not `cool-project-v2`)
- Write the README following the exact section order: Title + Badges, Problem Statement, Quick Start, What It Does, Architecture (optional), CTA Block, Contributing, License
- All CTA links must include UTM parameters: `?utm_source=github&utm_medium=readme&utm_campaign=<repo-slug>`
- Set 8-12 topics based on keyword research using `gh repo edit --add-topic`
- Set the homepage URL to your product site with UTM: `?utm_source=github&utm_medium=repo_homepage&utm_campaign=<repo>`
- Upload a 1280x640 social preview image

**Human action required:** Upload the social preview image via GitHub repo settings UI. Verify the Quick Start instructions run without errors on a clean machine.

### 3. Launch promotion

Run the `github-repo-promotion` drill:

- **Day 1 — Social:** Post on LinkedIn (problem-first framing, link to repo) and Twitter/X (hook + code screenshot + link). Use UTM: `?utm_source=<platform>&utm_medium=social&utm_campaign=<repo>-launch`
- **Day 1 — Communities:** Post in 2-3 relevant subreddits and Discord/Slack dev communities. Format: describe the problem, mention you open-sourced a solution, share the link. Follow each community's self-promotion rules.
- **Day 2 — Hacker News / dev.to:** Submit as `Show HN: <repo> — <one-line description>`. Publish a dev.to article explaining the problem and solution with repo link.
- **Day 3 — Email:** If you have an existing email list, send a one-time broadcast via Loops: "We open-sourced [thing] — here's the repo." Tag clicks with `source: github-sample-launch`.
- **Week 1 — First release:** Publish a `v1.0.0` release via `gh release create` with CTA in release notes. This notifies all stargazers.

### 4. Track results

Set up manual tracking (no always-on automation at Smoke level):

- Check GitHub traffic daily for the first week: `gh api repos/<org>/<repo>/traffic/views` and `gh api repos/<org>/<repo>/traffic/clones`
- Check star count: `gh api repos/<org>/<repo> --jq '.stargazers_count'`
- Check referral sources: `gh api repos/<org>/<repo>/traffic/popular/referrers`
- Check PostHog for events with `utm_source=github` to count CTA clicks, demo bookings, and signups
- Log all metrics in a spreadsheet or Attio note on the campaign record

### 5. Evaluate against threshold

After 3 weeks, measure:

- Total GitHub stars (target: ≥50)
- Inbound leads — demo bookings or signups where `utm_source=github` (target: ≥3)
- Top referral sources (which launch channel drove the most traffic)
- Clone count (signal of developer engagement depth)
- README CTA click-through rate (clicks / views from PostHog)

If PASS: proceed to Baseline. Document which launch channels drove the most stars and which drove the most leads — they may differ.
If FAIL: diagnose — are people finding the repo but not starring? (README quality issue.) Are people starring but not clicking the CTA? (CTA positioning or copy issue.) Is traffic low overall? (Promotion channels or keyword targeting issue.)

## Time Estimate

- 2 hours: sample project selection, keyword research, competitive repo analysis
- 3 hours: repo setup — README, topics, social preview, code polish, Quick Start testing
- 2 hours: launch promotion — writing social posts, community posts, HN submission, email broadcast
- 1 hour: daily traffic checks over 3 weeks, final evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| GitHub | Repository hosting and traffic analytics | Free for public repos — https://github.com/pricing |
| GitHub CLI (`gh`) | Repo creation, topic management, traffic API | Free — https://cli.github.com/ |
| PostHog | Track CTA clicks and signups via UTM | Free up to 1M events/mo — https://posthog.com/pricing |
| Anthropic (Claude) | README content generation, social post drafting | Pay-per-use ~$0.50-2 total — https://anthropic.com/pricing |
| Loops | Email broadcast to existing list (optional) | Free up to 1,000 contacts — https://loops.so/pricing |

**Smoke budget: Free** (all tools have free tiers that cover Smoke-level usage)

## Drills Referenced

- `github-repo-setup` — scaffold the public repo with keyword-optimized name, README with CTA, topics SEO, social preview, and analytics links
- `github-repo-promotion` — distribute the repo across developer channels (social, communities, HN, dev.to, email) with tracked UTM links
