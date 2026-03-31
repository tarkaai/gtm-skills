---
name: stack-overflow-presence-baseline
description: >
  Stack Overflow Presence — Baseline Run. First always-on automation for Stack Overflow answering.
  Automated question monitoring surfaces high-opportunity questions daily. Agent drafts answers,
  tracks performance, and measures sustained lead generation over 6 weeks.
stage: "Marketing > SolutionAware"
motion: "CommunitiesForums"
channels: "Communities"
level: "Baseline Run"
time: "18 hours over 6 weeks"
outcome: "≥30 answers, ≥1,000 cumulative answer views, and ≥5 qualified leads in 6 weeks"
kpis: ["Answer volume", "Cumulative answer views", "Average upvote score", "Acceptance rate", "Referral sessions from SO", "Qualified leads attributed"]
slug: "stack-overflow-presence"
install: "npx gtm-skills add CommunitiesForums/Marketing/SolutionAware/stack-overflow-presence"
drills:
  - posthog-gtm-events
---
# Stack Overflow Presence — Baseline Run

> **Stage:** Marketing → SolutionAware | **Motion:** CommunitiesForums | **Channels:** Communities

## Overview
Stack Overflow Presence — Baseline Run. First always-on automation for Stack Overflow answering. Automated question monitoring surfaces high-opportunity questions daily. Agent drafts answers, tracks performance, and measures sustained lead generation over 6 weeks.

**Time commitment:** 18 hours over 6 weeks
**Pass threshold:** ≥30 answers, ≥1,000 cumulative answer views, and ≥5 qualified leads in 6 weeks

---

## Budget

**Play-specific cost:** Free

Stack Exchange API is free. n8n self-hosted is free. Syften monitoring is optional ($20-100/mo) for faster question detection.

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Set up automated question monitoring

Run the the so question monitoring automation workflow (see instructions below) drill to build the n8n pipeline that:
- Polls Stack Exchange API every 30 minutes for new questions in your primary tags
- Scores each question by opportunity (unanswered, high views, community-validated)
- Routes high-priority questions to Slack for immediate action
- Produces a daily digest of engagement metrics

Configure the pipeline with your primary tags (from Smoke Test results) and tune filters over the first week.

### 2. Configure referral tracking

Run the `posthog-gtm-events` drill to set up tracking for:
- `stack-overflow-presence_referral_visit`: fires when a visitor arrives with `utm_source=stackoverflow`
- `stack-overflow-presence_signup`: fires when an SO-referred visitor creates an account
- `stack-overflow-presence_qualified_lead`: fires when an SO-referred signup meets qualification criteria

Add UTM parameters to any links included in SO answers:
```
https://yoursite.com/docs/PAGE?utm_source=stackoverflow&utm_medium=community&utm_campaign=stack-overflow-presence&utm_content=q_{QUESTION_ID}
```

### 3. Execute a 6-week answering cadence

Using the the so answer crafting workflow (see instructions below) drill, answer 5+ questions per week:

**Week 1-2:** Focus exclusively on primary tags. Answer the highest-opportunity questions surfaced by the monitoring pipeline. Establish quality patterns.

**Week 3-4:** Expand to secondary tags when primary tag volume is low. Start including links to your technical documentation in 1 of every 10 answers (where genuinely the best resource).

**Week 5-6:** Optimize based on data. Double down on tags where your answers earn the most upvotes. Respond to comments and edit older answers that are gaining views.

Log every answer in the activity log. Record: question ID, tags, answer type, time spent, link included (y/n).

### 4. Track reputation and authority growth

Monitor weekly using the Stack Exchange API:
```bash
GET /users/{USER_ID}?site=stackoverflow&key=YOUR_API_KEY
GET /users/{USER_ID}/top-tags?site=stackoverflow&key=YOUR_API_KEY
```

Track:
- Total reputation and weekly growth
- Per-tag answer count and score
- Badge progress (bronze badges in target tags are early authority signals)

### 5. Evaluate against threshold

Measure against: ≥30 answers, ≥1,000 cumulative answer views, and ≥5 qualified leads in 6 weeks.

Check cumulative answer views:
```bash
GET /users/{USER_ID}/answers?order=desc&sort=creation&fromdate={6_WEEKS_AGO}&site=stackoverflow&key=YOUR_API_KEY&filter=withbody
```
Sum the `view_count` of the parent questions for all your answers.

Check qualified leads in PostHog and Attio: filter contacts where `lead_source_detail` contains 'stackoverflow'.

If PASS: proceed to Scalable. The cadence and monitoring pipeline produce consistent results.
If FAIL: analyze which tags and answer types generated the most views and leads. Reallocate effort toward high-performing segments.

---

## KPIs to track
- Answer volume
- Cumulative answer views
- Average upvote score
- Acceptance rate
- Referral sessions from SO
- Qualified leads attributed

---

## Pass threshold
**≥30 answers, ≥1,000 cumulative answer views, and ≥5 qualified leads in 6 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your tag targeting and answer quality, then re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add CommunitiesForums/Marketing/SolutionAware/stack-overflow-presence`_
