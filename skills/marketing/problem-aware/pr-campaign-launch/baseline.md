---
name: pr-campaign-launch-baseline
description: >
    PR Campaign Launch — Baseline Run. Coordinated press outreach for product launches or milestones
  to generate media coverage and awareness with problem-aware audiences.
stage: "Marketing > Problem Aware"
motion: "PR & Earned Mentions"
channels: "Other, Social"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥10 press mentions and ≥20 qualified leads from coordinated launch campaign"
kpis: ["Conversion rate", "Cost per result", "Response quality", "Cycle time"]
slug: "pr-campaign-launch"
install: "npx gtm-skills add marketing/problem-aware/pr-campaign-launch"
drills:
  - case-study-creation
  - newsletter-pipeline
  - posthog-gtm-events
---
# PR Campaign Launch — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** PR & Earned Mentions | **Channels:** Other, Social

## Overview
PR Campaign Launch — Baseline Run. Coordinated press outreach for product launches or milestones to generate media coverage and awareness with problem-aware audiences.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** ≥10 press mentions and ≥20 qualified leads from coordinated launch campaign

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
Run the `posthog-gtm-events` drill to track: `pr-campaign-launch_mention_published`, `pr-campaign-launch_backlink_acquired`, `pr-campaign-launch_referral_traffic`, `pr-campaign-launch_lead_from_pr`. Set up Google Alerts or a media monitoring tool for brand mentions.

### 3. Execute a 4-week PR push
Pitch 10-20 publications. Submit 2-3 guest articles. Publish your case studies and promote them. Track all coverage and resulting traffic in PostHog.

### 4. Evaluate against threshold
Measure against: ≥10 press mentions and ≥20 qualified leads from coordinated launch campaign. If PASS, proceed to Scalable. If FAIL, test different story angles or target tier-2 publications first to build credibility.

---

## KPIs to track
- Conversion rate
- Cost per result
- Response quality
- Cycle time

---

## Pass threshold
**≥10 press mentions and ≥20 qualified leads from coordinated launch campaign**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/problem-aware/pr-campaign-launch`_
