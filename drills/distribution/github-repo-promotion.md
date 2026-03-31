---
name: github-repo-promotion
description: Distribute a GitHub sample repo across developer channels to build initial traction and sustained traffic
category: GitHub
tools:
  - GitHub CLI
  - PostHog
  - Loops
  - n8n
fundamentals:
  - github-traffic-api
  - github-release-publish
  - posthog-custom-events
  - n8n-workflow-basics
  - n8n-triggers
  - linkedin-organic-posting
  - loops-sequences
---

# GitHub Repo Promotion

Systematic distribution workflow to drive traffic and stars to a GitHub sample repo. This drill covers initial launch promotion and ongoing distribution cadence.

## Input

- **Live GitHub repo URL:** The repo created by the `github-repo-setup` drill
- **Author's social accounts:** LinkedIn, Twitter/X, dev.to, Hacker News username
- **Email list (optional):** Existing subscribers who might care about this sample
- **Target communities:** Subreddits, Discord servers, Slack groups where the ICP hangs out

## Steps

### 1. Launch announcement sequence

Execute these within the first 48 hours of publishing the repo:

**Day 1 — Social posts:**
- LinkedIn post: problem-first framing, mention you open-sourced a solution, link to repo with UTM `?utm_source=linkedin&utm_medium=social&utm_campaign=<repo>-launch`
- Twitter/X post: short hook + code screenshot + repo link with UTM `?utm_source=twitter&utm_medium=social&utm_campaign=<repo>-launch`
- Use `linkedin-organic-posting` fundamental for the LinkedIn post

**Day 1 — Community posts:**
- Post in 2-3 relevant subreddits (follow each subreddit's rules on self-promotion)
- Post in relevant Discord/Slack dev communities
- Format: describe the problem first, then mention you built an open-source solution, share the link
- UTM: `?utm_source=<platform>&utm_medium=community&utm_campaign=<repo>-launch`

**Day 2 — Hacker News / dev.to:**
- Submit to Hacker News as `Show HN: <repo name> — <one-line description>` with the GitHub URL
- Publish a dev.to article explaining the problem and how the sample solves it, with repo link
- UTM: `?utm_source=hackernews&utm_medium=community&utm_campaign=<repo>-launch` (note: HN strips UTMs on the submission URL, but your README CTA links retain them)

### 2. Email notification to existing list

Using `loops-sequences` fundamental:
- Send a one-time broadcast to relevant segments of your email list
- Subject: "We open-sourced [thing] — here's the repo"
- Body: problem statement, what the sample does, direct link to repo, ask for a star if they find it useful
- Tag clicks with `source: github-sample-announcement`

### 3. Set up traffic tracking automation

Using `n8n-workflow-basics` and `n8n-triggers`:

Build an n8n workflow that runs daily:
1. Call `github-traffic-api` fundamental to fetch views, clones, referrers, and star count
2. Send each data point to PostHog as custom events:
   - `github_repo_views` with properties: `{repo, count, uniques, date}`
   - `github_repo_clones` with properties: `{repo, count, uniques, date}`
   - `github_repo_stars` with properties: `{repo, total_stars, date}`
   - `github_repo_referrer` with properties: `{repo, referrer, count, uniques, date}`
3. Store the raw JSON in Attio as a note on the campaign record (backup)

This solves GitHub's 14-day traffic retention limit by persisting data in PostHog.

### 4. Publish the first release

Using `github-release-publish` fundamental:
- Create a `v1.0.0` release within the first week
- Include a CTA in the release notes with UTM: `?utm_source=github&utm_medium=release&utm_campaign=<repo>-v1.0.0`
- Attach any relevant binary assets

Releases trigger notifications to all stargazers — this is free re-engagement.

### 5. Set up ongoing promotion cadence

After the initial launch:
- **Weekly:** Check GitHub traffic via the n8n workflow. Identify top referral sources. Double down on the channel driving the most clones.
- **Bi-weekly:** Post an update, tip, or use case on social media that links back to the repo
- **Monthly:** Publish a new release (even if minor). Each release re-engages stargazers.

## Output

- Launch announcement posted across 4+ channels
- n8n workflow persisting daily GitHub traffic data to PostHog
- First release published with CTA
- Ongoing promotion cadence documented

## Triggers

Run once for launch, then follow the ongoing cadence. Re-run the launch sequence if you make a major update to the sample.
