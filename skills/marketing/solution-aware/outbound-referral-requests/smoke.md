---
name: outbound-referral-requests-smoke
description: >
    Outbound Referral Requests — Smoke Test. Ask existing customers and contacts for warm
  introductions to specific target accounts to generate high-quality solution-aware leads through
  trusted networks.
stage: "Marketing > Solution Aware"
motion: "Partnerships & Warm Intros"
channels: "Email, Direct"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥3 warm intros from 15 referral requests in 2 weeks"
kpis: ["Response rate", "Engagement quality", "Time to response"]
slug: "outbound-referral-requests"
install: "npx gtm-skills add marketing/solution-aware/outbound-referral-requests"
drills:
  - icp-definition
  - build-prospect-list
  - threshold-engine
---
# Outbound Referral Requests — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Email, Direct

## Overview
Outbound Referral Requests — Smoke Test. Ask existing customers and contacts for warm introductions to specific target accounts to generate high-quality solution-aware leads through trusted networks.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** ≥3 warm intros from 15 referral requests in 2 weeks

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
Run the `threshold-engine` drill to measure against: ≥3 warm intros from 15 referral requests in 2 weeks. If PASS, proceed to Baseline. If FAIL, adjust your partner ICP or value proposition.

---

## KPIs to track
- Response rate
- Engagement quality
- Time to response

---

## Pass threshold
**≥3 warm intros from 15 referral requests in 2 weeks**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/outbound-referral-requests`_
