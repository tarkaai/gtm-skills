---
name: alumni-campus-pro-orgs-smoke
description: >
    Alumni & Campus Outreach — Smoke Test. Post or email in alumni, campus, or professional org
  groups to reach warm communities and test whether 1–2 meetings come from low-friction
  participation.
stage: "Marketing > Unaware"
motion: "Communities & Forums"
channels: "Communities, Other"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: "≥ 1 meeting in 1 week"
kpis: ["Post engagement", "Inbound inquiries"]
slug: "alumni-campus-pro-orgs"
install: "npx gtm-skills add marketing/unaware/alumni-campus-pro-orgs"
drills:
  - icp-definition
  - social-content-pipeline
  - threshold-engine
---
# Alumni & Campus Outreach — Smoke Test

> **Stage:** Marketing → Unaware | **Motion:** Communities & Forums | **Channels:** Communities, Other

## Overview
Alumni & Campus Outreach — Smoke Test. Post or email in alumni, campus, or professional org groups to reach warm communities and test whether 1–2 meetings come from low-friction participation.

**Time commitment:** 3 hours over 1 week
**Pass threshold:** ≥ 1 meeting in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Identify target communities
Run the `icp-definition` drill to map where your ICP spends time: Slack communities, Discord servers, Reddit subreddits, forums, Facebook groups. List 5-10 communities ranked by relevance and activity level.

### 2. Create valuable content for communities
Run the `social-content-pipeline` drill to create 5-10 pieces of community-appropriate content: helpful answers, resource shares, discussion starters, case studies. Avoid promotional content -- focus on being genuinely useful.

**Human action required:** Join the communities and post content manually. Engage authentically in discussions. Build reputation before mentioning your product. Log all activity in Attio.

### 3. Track community engagement
Log each interaction: post/comment, community name, engagement received, DMs or follows generated, any leads captured. Note which communities and content types generate the most interest.

### 4. Evaluate against threshold
Run the `threshold-engine` drill to measure against: ≥ 1 meeting in 1 week. If PASS, proceed to Baseline. If FAIL, try different communities or adjust your content approach.

---

## KPIs to track
- Post engagement
- Inbound inquiries

---

## Pass threshold
**≥ 1 meeting in 1 week**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/unaware/alumni-campus-pro-orgs`_
