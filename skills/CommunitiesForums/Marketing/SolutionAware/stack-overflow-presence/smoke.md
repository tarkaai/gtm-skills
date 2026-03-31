---
name: stack-overflow-presence-smoke
description: >
  Stack Overflow Presence — Smoke Test. Answer questions on Stack Overflow to build authority,
  drive organic traffic, and generate awareness with solution-aware developers searching for
  solutions. Manually identify target tags, answer 10 questions, and measure signal.
stage: "Marketing > SolutionAware"
motion: "CommunitiesForums"
channels: "Communities"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥10 high-quality answers posted and ≥100 profile views in 2 weeks"
kpis: ["Answers posted", "Average upvote score per answer", "Profile views", "Acceptance rate"]
slug: "stack-overflow-presence"
install: "npx gtm-skills add CommunitiesForums/Marketing/SolutionAware/stack-overflow-presence"
drills:
  - so-tag-reconnaissance
  - threshold-engine
---
# Stack Overflow Presence — Smoke Test

> **Stage:** Marketing → SolutionAware | **Motion:** CommunitiesForums | **Channels:** Communities

## Overview
Stack Overflow Presence — Smoke Test. Answer questions on Stack Overflow to build authority, drive organic traffic, and generate awareness with solution-aware developers searching for solutions. Manually identify target tags, answer 10 questions, and measure signal.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** ≥10 high-quality answers posted and ≥100 profile views in 2 weeks

---

## Budget

**Play-specific cost:** Free

Stack Exchange API key is free (10,000 requests/day). No paid tools required.

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Identify target tags

Run the `so-tag-reconnaissance` drill to discover and rank Stack Overflow tags where your expertise is relevant. Produce a ranked list of 10-15 target tags with engagement profiles. Focus on tags where:
- Unanswered question ratio is above 30%
- Average views on unanswered questions exceed 100
- Your team has genuine deep expertise

Select 3-5 primary tags to focus on for this smoke test.

### 2. Find high-opportunity questions

Manually search your primary tags using the Stack Exchange API:

```bash
GET /search/advanced?tagged={PRIMARY_TAG}&accepted=false&answers=0&sort=creation&order=desc&site=stackoverflow&key=YOUR_API_KEY&pagesize=50
```

Identify 15-20 candidate questions that meet all of these criteria:
- Posted within the last 7 days
- 0-1 existing answers
- Question score >= 0 (not downvoted)
- You can provide a complete, technically correct answer

### 3. Answer 10 questions

Run the the so answer crafting workflow (see instructions below) drill for each question. Target 2 answers per day over 5 days. For each answer:
- Follow the answer crafting rules precisely (working code, explanations, no self-promotion)
- Log the interaction: question ID, tags, answer type, word count, time spent
- Track the answer URL for follow-up monitoring

**Human action required:** If your Stack Overflow account is new (under 50 reputation), post answers manually. The agent drafts each answer; you review and post. Once reputation passes 50, API posting is available.

### 4. Monitor and follow up

Check each answer at 24h and 48h after posting:
- Record upvote score and acceptance status
- Respond to any comments or follow-up questions on your answers
- Edit answers if comments reveal gaps or errors

### 5. Evaluate against threshold

Run the `threshold-engine` drill to measure against: ≥10 high-quality answers posted and ≥100 profile views in 2 weeks. Check your SO profile page for view count (`GET /users/{USER_ID}?site=stackoverflow`).

If PASS: proceed to Baseline. The signal confirms your expertise maps to real SO demand.
If FAIL: analyze which tags and answer types performed best. Adjust your tag selection and try again with a narrower focus.

---

## KPIs to track
- Answers posted
- Average upvote score per answer
- Profile views
- Acceptance rate

---

## Pass threshold
**≥10 high-quality answers posted and ≥100 profile views in 2 weeks**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your tag selection and answer approach, then re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add CommunitiesForums/Marketing/SolutionAware/stack-overflow-presence`_
