---
name: founder-guest-podcasts-baseline
description: >
    Founder Guest Podcast — Baseline Run. Pitch a handful of micro podcasts for one guest spot to
  test whether podcast exposure drives at least one inbound lead.
stage: "Marketing > Unaware"
motion: "PR & Earned Mentions"
channels: "Content"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 3 inbound leads over 2 weeks"
kpis: ["Podcast listens", "Referral traffic"]
slug: "founder-guest-podcasts"
install: "npx gtm-skills add marketing/unaware/founder-guest-podcasts"
drills:
  - case-study-creation
  - newsletter-pipeline
  - posthog-gtm-events
---
# Founder Guest Podcast — Baseline Run

> **Stage:** Marketing → Unaware | **Motion:** PR & Earned Mentions | **Channels:** Content

## Overview
Founder Guest Podcast — Baseline Run. Pitch a handful of micro podcasts for one guest spot to test whether podcast exposure drives at least one inbound lead.

**Time commitment:** 12 hours over 2 weeks
**Pass threshold:** ≥ 3 inbound leads over 2 weeks

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
Run the `posthog-gtm-events` drill to track: `founder-guest-podcasts_mention_published`, `founder-guest-podcasts_backlink_acquired`, `founder-guest-podcasts_referral_traffic`, `founder-guest-podcasts_lead_from_pr`. Set up Google Alerts or a media monitoring tool for brand mentions.

### 3. Execute a 4-week PR push
Pitch 10-20 publications. Submit 2-3 guest articles. Publish your case studies and promote them. Track all coverage and resulting traffic in PostHog.

### 4. Evaluate against threshold
Measure against: ≥ 3 inbound leads over 2 weeks. If PASS, proceed to Scalable. If FAIL, test different story angles or target tier-2 publications first to build credibility.

---

## KPIs to track
- Podcast listens
- Referral traffic

---

## Pass threshold
**≥ 3 inbound leads over 2 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/unaware/founder-guest-podcasts`_
