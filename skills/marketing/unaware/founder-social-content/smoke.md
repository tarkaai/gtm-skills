---
name: founder-social-content-smoke
description: >
  Founder Social & Content — Smoke Test. Publish a few posts per week with a clear CTA to see if founder-led content drives inbound leads or DMs before scaling.
stage: "Marketing > Unaware"
motion: "Founder Social Content"
channels: "Social"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: "≥ 3 leads or ≥ 2 meetings in 1 week"
kpis: ["Impressions", "Engagement rate", "Profile visits"]
slug: "founder-social-content"
install: "npx gtm-skills add marketing/unaware/founder-social-content"
drills:
  - social-content-pipeline
  - threshold-engine
---
# Founder Social & Content — Smoke Test

> **Stage:** Marketing → Unaware | **Motion:** Founder Social Content | **Channels:** Social

## Overview
Publish a few posts per week with a clear CTA to see if founder-led content drives inbound leads or DMs before scaling.

**Time commitment:** 3 hours over 1 week
**Pass threshold:** ≥ 3 leads or ≥ 2 meetings in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
_No specialized tools required at this level._

---

## Instructions

### 1. Optimize your LinkedIn profile
Use the `linkedin-organic-profile` fundamental to set up your profile as a GTM channel: value-prop headline, About section with clear positioning, Featured section with your best content and product link.

### 2. Plan your content
Run the `social-content-pipeline` drill to set up a content plan. For Smoke, plan 3 posts for the week:
- **Post 1:** Story post about a customer problem you solve (use `linkedin-organic-hooks` fundamental for the hook)
- **Post 2:** Framework or list post sharing your approach (use `linkedin-organic-formats` fundamental)
- **Post 3:** Contrarian opinion about your industry to drive comments

### 3. Write and publish
Use the `linkedin-organic-hooks` fundamental to write scroll-stopping hooks. Keep posts between 150-300 words. End each with a clear CTA: "DM me [keyword] if you want to learn more" or link to your booking page.

### 4. Engage actively
Use the `linkedin-organic-engagement` fundamental: spend 15 minutes before each post commenting on 5-10 posts from people in your ICP. Reply to every comment on your posts within 2 hours.

### 5. Track results
Log every lead (DM, comment expressing interest, profile visit that converts) in Attio using the `attio-contacts` fundamental. Tag source as "LinkedIn." Track impressions and engagement manually or via LinkedIn's native analytics.

### 6. Measure against threshold
Run the `threshold-engine` drill after 7 days:
- **Pass:** ≥ 3 leads or ≥ 2 meetings from social content
- **If pass:** Document which post types and hooks worked, proceed to Baseline
- **If fail:** Test different content angles, post times, or audience targeting

---

## KPIs to track
- Impressions
- Engagement rate
- Profile visits

---

## Pass threshold
**≥ 3 leads or ≥ 2 meetings in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/unaware/founder-social-content`_
