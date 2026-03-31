---
name: stack-overflow-presence-scalable
description: >
  Stack Overflow Presence — Scalable Automation. AI-assisted answer generation pipeline scales
  volume 5-10x while maintaining quality. Batch processing, quality gates, and performance
  dashboards enable 10-25 answers/day across all target tags.
stage: "Marketing > SolutionAware"
motion: "CommunitiesForums"
channels: "Communities"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: "≥100 answers, ≥10,000 cumulative views, and ≥20 qualified leads over 4 months"
kpis: ["Weekly answer volume", "Average upvote score", "Acceptance rate", "Referral sessions/week", "Qualified leads/month", "AI quality gate pass rate", "Cost per qualified lead"]
slug: "stack-overflow-presence"
install: "npx gtm-skills add CommunitiesForums/Marketing/SolutionAware/stack-overflow-presence"
drills:
  - community-health-scoring
---
# Stack Overflow Presence — Scalable Automation

> **Stage:** Marketing → SolutionAware | **Motion:** CommunitiesForums | **Channels:** Communities

## Overview
Stack Overflow Presence — Scalable Automation. AI-assisted answer generation pipeline scales volume 5-10x while maintaining quality. Batch processing, quality gates, and performance dashboards enable 10-25 answers/day across all target tags.

**Time commitment:** 75 hours over 3 months
**Pass threshold:** ≥100 answers, ≥10,000 cumulative views, and ≥20 qualified leads over 4 months

---

## Budget

**Play-specific tools & costs**
- **Anthropic API (Claude):** ~$20-50/mo for answer drafting (est. 500 answers/mo at ~$0.05/answer)
- **Syften (optional):** $20-100/mo for real-time question detection

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Deploy the AI answer generation pipeline

Run the the so answer scaling workflow (see instructions below) drill to build the n8n pipeline that:
- Receives high-opportunity questions from the monitoring pipeline
- Uses Claude to draft technically accurate answers following SO formatting rules
- Applies quality gates: code validation, length check, self-promotion filter, uniqueness check
- Queues passing answers for human review (initially) or auto-posting (once trust is established)
- Rate-limits posting to comply with Stack Overflow's write API limits (max 40/day, 1 per 3 minutes)

Configure tag-specific prompts based on Baseline data: which answer formats, lengths, and styles earned the most upvotes per tag.

### 2. Establish quality guardrails

Set hard stops in the pipeline:
- **Downvote rate threshold**: If >10% of answers posted in a week receive downvotes, pause auto-posting and switch to full human review
- **Deletion threshold**: If any answer is deleted by SO moderators, pause and investigate
- **Reputation velocity check**: If weekly reputation growth turns negative, pause all posting
- **Daily budget**: Start at 10 answers/day. Increase by 5/day each week if quality metrics hold. Cap at 25/day.

### 3. Scale across all tag groups

Expand from primary tags to full tag coverage:
- Add secondary tags to the monitoring pipeline
- Create tag-group-specific system prompts (e.g., Python answers need different code style than JavaScript)
- Track per-tag ROI: (upvotes + acceptances + referral sessions) / answers posted
- Reallocate answer budget weekly toward highest-ROI tags

### 4. Build tag-level health scoring

Run the `community-health-scoring` drill adapted for SO tags instead of communities:
- Score each tag weekly: answer volume, upvote rate, acceptance rate, referral traffic, pipeline attribution
- Classify tags: thriving (increase effort), healthy (maintain), watch (investigate), declining (reduce), dormant (pause)
- Generate weekly tag health report in Slack
- Use the scores to auto-adjust the monitoring pipeline's tag priorities

### 5. Optimize referral capture

Refine the link strategy for answers that include documentation references:
- A/B test link placement: in-line vs. end of answer
- Track which documentation pages generate the most signups (via PostHog UTM analysis)
- Create dedicated landing pages for high-traffic SO topics with content tailored to the SO question context
- Ensure links add genuine value — SO moderators remove answers that are link-only

### 6. Evaluate against threshold

Measure against: ≥100 answers, ≥10,000 cumulative views, and ≥20 qualified leads over 4 months.

Track in PostHog:
- Total answers posted (from activity log)
- Cumulative answer views (sum parent question `view_count` via Stack Exchange API)
- Qualified leads (PostHog events + Attio deal attribution)

If PASS: proceed to Durable. The pipeline produces consistent volume and quality at scale.
If FAIL: analyze per-tag performance. Focus on the tags with highest lead conversion rates and cut underperforming tags.

---

## KPIs to track
- Weekly answer volume
- Average upvote score
- Acceptance rate
- Referral sessions/week
- Qualified leads/month
- AI quality gate pass rate
- Cost per qualified lead

---

## Pass threshold
**≥100 answers, ≥10,000 cumulative views, and ≥20 qualified leads over 4 months**

If you hit this threshold, move to the **Durable Intelligence** level.
If not, iterate on your AI prompts and tag targeting, then re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add CommunitiesForums/Marketing/SolutionAware/stack-overflow-presence`_
