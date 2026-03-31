---
name: co-marketing-shoutouts-smoke
description: >
    Partner Newsletter Shoutout — Smoke Test. Run a short co-marketing blurb in a partner newsletter
  to test awareness and lead flow before committing to bigger formats like LinkedIn Live.
stage: "Marketing > Problem Aware"
motion: "Partnerships & Warm Intros"
channels: "Email"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: "≥ 20 clicks and ≥ 1 lead in 1 week"
kpis: ["Impressions", "Click-through rate"]
slug: "co-marketing-shoutouts"
install: "npx gtm-skills add marketing/problem-aware/co-marketing-shoutouts"
drills:
  - icp-definition
  - build-prospect-list
  - threshold-engine
---
# Partner Newsletter Shoutout — Smoke Test

> **Stage:** Marketing → Problem Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Email

## Overview
Partner Newsletter Shoutout — Smoke Test. Run a short co-marketing blurb in a partner newsletter to test awareness and lead flow before committing to bigger formats like LinkedIn Live.

**Time commitment:** 3 hours over 1 week
**Pass threshold:** ≥ 20 clicks and ≥ 1 lead in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Define partner ICP
Run the `icp-definition` drill to define your ideal partner profile: complementary products, overlapping audiences, similar company stage, and shared values. Identify 10-20 potential partners.

### 2. Build a partner prospect list
Run the `build-prospect-list` drill to research and enrich partner contacts: find the right person at each company (partnerships lead, founder, head of BD), get their email and LinkedIn, and add them to an Attio list.

**Human action required:** Reach out to 10 partners personally. Use warm intros where possible. Propose a specific, low-commitment collaboration (content swap, co-promotion, intro exchange). Log all outreach in Attio.

### 3. Track partner conversations
Log every partner interaction in Attio: outreach sent, response received, meeting booked, collaboration agreed, results generated.

### 4. Evaluate against threshold
Run the `threshold-engine` drill to measure against: ≥ 20 clicks and ≥ 1 lead in 1 week. If PASS, proceed to Baseline. If FAIL, adjust your partner ICP or value proposition.

---

## KPIs to track
- Impressions
- Click-through rate

---

## Pass threshold
**≥ 20 clicks and ≥ 1 lead in 1 week**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/co-marketing-shoutouts`_
