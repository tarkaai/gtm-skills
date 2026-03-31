---
name: pr-earned-baseline
description: >
    PR & Earned Placements — Baseline Run. Pitch micro newsletters or podcasts for one placement to
  test if earned coverage drives clicks and inbound interest.
stage: "Marketing > Unaware"
motion: "PR & Earned Mentions"
channels: "Email, Content"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 2 placements and ≥ 80 referral clicks over 2 weeks"
kpis: ["Placement rate", "Referral clicks"]
slug: "pr-earned"
install: "npx gtm-skills add marketing/unaware/pr-earned"
drills:
  - case-study-creation
  - newsletter-pipeline
  - posthog-gtm-events
---
# PR & Earned Placements — Baseline Run

> **Stage:** Marketing → Unaware | **Motion:** PR & Earned Mentions | **Channels:** Email, Content

## Overview
PR & Earned Placements — Baseline Run. Pitch micro newsletters or podcasts for one placement to test if earned coverage drives clicks and inbound interest.

**Time commitment:** 12 hours over 2 weeks
**Pass threshold:** ≥ 2 placements and ≥ 80 referral clicks over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Build a PR content machine
Run the `case-study-creation` drill to create 2-3 customer case studies that serve as PR assets. Run the `newsletter-pipeline` drill to start your own newsletter that establishes thought leadership and gives journalists a reason to follow you.

### 2. Configure PR tracking
Run the `posthog-gtm-events` drill to track: `pr-earned_mention_published`, `pr-earned_backlink_acquired`, `pr-earned_referral_traffic`, `pr-earned_lead_from_pr`. Set up Google Alerts or a media monitoring tool for brand mentions.

### 3. Execute a 4-week PR push
Pitch 10-20 publications. Submit 2-3 guest articles. Publish your case studies and promote them. Track all coverage and resulting traffic in PostHog.

### 4. Evaluate against threshold
Measure against: ≥ 2 placements and ≥ 80 referral clicks over 2 weeks. If PASS, proceed to Scalable. If FAIL, test different story angles or target tier-2 publications first to build credibility.

---

## KPIs to track
- Placement rate
- Referral clicks

---

## Pass threshold
**≥ 2 placements and ≥ 80 referral clicks over 2 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/unaware/pr-earned`_
