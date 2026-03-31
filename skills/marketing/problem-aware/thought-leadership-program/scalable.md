---
name: thought-leadership-program-scalable
description: >
    Thought Leadership Program — Scalable Automation. Systematic approach to building founder or
  executive as recognized thought leader to attract inbound interest from problem-aware and
  solution-aware audiences.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Social, Content, Events"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: "≥50 thought pieces, ≥8 speaking slots, and ≥60 qualified leads over 6 months"
kpis: ["Weekly volume", "Conversion rate", "Cost per result", "Automation efficiency", "Quality score"]
slug: "thought-leadership-program"
install: "npx gtm-skills add marketing/problem-aware/thought-leadership-program"
drills:
  - follow-up-automation
  - ab-test-orchestrator
---
# Thought Leadership Program — Scalable Automation

> **Stage:** Marketing → Problem Aware | **Motion:** Founder Social Content | **Channels:** Social, Content, Events

## Overview
Thought Leadership Program — Scalable Automation. Systematic approach to building founder or executive as recognized thought leader to attract inbound interest from problem-aware and solution-aware audiences.

**Time commitment:** 75 hours over 3 months
**Pass threshold:** ≥50 thought pieces, ≥8 speaking slots, and ≥60 qualified leads over 6 months

---

## Budget

**Play-specific tools & costs**
- **Tool and automation costs:** ~$100-500/mo at scale

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Automate content distribution
Run the `follow-up-automation` drill to build n8n workflows that: schedule posts across platforms, auto-DM new followers who match ICP criteria, and notify you when high-engagement posts deserve a follow-up or repurpose.

### 2. Launch content A/B testing
Run the `ab-test-orchestrator` drill to systematically test: hook styles (question vs statistic vs story), content length (short vs long-form), posting times, CTAs (comment vs DM vs link). Run each test over 10+ posts before declaring winners.

### 3. Scale to daily publishing
Increase to daily posting with automated scheduling. Use the repurposing pipeline to generate 5+ pieces from each original piece of content. Monitor engagement rates to ensure quality doesn't drop with volume.

### 4. Evaluate against threshold
Measure against: ≥50 thought pieces, ≥8 speaking slots, and ≥60 qualified leads over 6 months. If PASS, proceed to Durable. If FAIL, focus on the content pillars and formats that showed the best results and cut the rest.

---

## KPIs to track
- Weekly volume
- Conversion rate
- Cost per result
- Automation efficiency
- Quality score

---

## Pass threshold
**≥50 thought pieces, ≥8 speaking slots, and ≥60 qualified leads over 6 months**

If you hit this threshold, move to the **Durable Intelligence** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/thought-leadership-program`_
