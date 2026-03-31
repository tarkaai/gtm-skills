---
name: guest-posting-scale-baseline
description: >
    Guest Posting at Scale — Baseline Run. Publish guest posts on relevant industry blogs to build
  backlinks and awareness, from manual pitching to automated outreach and AI-driven content
  placement optimization.
stage: "Marketing > Solution Aware"
motion: "PR & Earned Mentions"
channels: "Content, Email"
level: "Baseline Run"
time: "25 hours over 6 weeks"
outcome: "≥6 published articles and ≥300 referral visits"
kpis: ["Pitch acceptance rate", "Articles published", "Referral traffic", "Backlinks acquired", "Conversion rate from referrals"]
slug: "guest-posting-scale"
install: "npx gtm-skills add marketing/solution-aware/guest-posting-scale"
drills:
  - case-study-creation
  - newsletter-pipeline
  - posthog-gtm-events
---
# Guest Posting at Scale — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** PR & Earned Mentions | **Channels:** Content, Email

## Overview
Guest Posting at Scale — Baseline Run. Publish guest posts on relevant industry blogs to build backlinks and awareness, from manual pitching to automated outreach and AI-driven content placement optimization.

**Time commitment:** 25 hours over 6 weeks
**Pass threshold:** ≥6 published articles and ≥300 referral visits

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
Run the `posthog-gtm-events` drill to track: `guest-posting-scale_mention_published`, `guest-posting-scale_backlink_acquired`, `guest-posting-scale_referral_traffic`, `guest-posting-scale_lead_from_pr`. Set up Google Alerts or a media monitoring tool for brand mentions.

### 3. Execute a 4-week PR push
Pitch 10-20 publications. Submit 2-3 guest articles. Publish your case studies and promote them. Track all coverage and resulting traffic in PostHog.

### 4. Evaluate against threshold
Measure against: ≥6 published articles and ≥300 referral visits. If PASS, proceed to Scalable. If FAIL, test different story angles or target tier-2 publications first to build credibility.

---

## KPIs to track
- Pitch acceptance rate
- Articles published
- Referral traffic
- Backlinks acquired
- Conversion rate from referrals

---

## Pass threshold
**≥6 published articles and ≥300 referral visits**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/guest-posting-scale`_
