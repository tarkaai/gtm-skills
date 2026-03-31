---
name: discord-community-building-baseline
description: >
    Discord Community Management — Baseline Run. Build and nurture a Discord server to engage users,
  provide support, and generate product-aware leads through authentic community interaction.
stage: "Marketing > Product Aware"
motion: "Communities & Forums"
channels: "Communities, Product"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "≥200 members and ≥20 DAU with ≥10 qualified leads in 6 weeks"
kpis: ["Conversion rate", "Cost per result", "Response quality", "Cycle time"]
slug: "discord-community-building"
install: "npx gtm-skills add marketing/product-aware/discord-community-building"
drills:
  - posthog-gtm-events
  - content-repurposing
---
# Discord Community Management — Baseline Run

> **Stage:** Marketing → Product Aware | **Motion:** Communities & Forums | **Channels:** Communities, Product

## Overview
Discord Community Management — Baseline Run. Build and nurture a Discord server to engage users, provide support, and generate product-aware leads through authentic community interaction.

**Time commitment:** 18 hours over 2 weeks
**Pass threshold:** ≥200 members and ≥20 DAU with ≥10 qualified leads in 6 weeks

---

## Budget

**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Set up analytics
Run the `posthog-gtm-events` drill to track community-driven traffic and conversions: `discord-community-building_community_post`, `discord-community-building_referral_visit`, `discord-community-building_signup_from_community`. Use UTM parameters on all shared links to attribute traffic to specific communities.

### 2. Build a content repurposing system
Run the `content-repurposing` drill to adapt your best-performing community content across multiple communities and formats. One detailed answer can become a Reddit post, a Slack thread, a blog post, and a Twitter thread.

### 3. Execute a 2-week community engagement plan
Post 2-3 times per week across your top communities. Track everything in PostHog. Focus on communities that showed traction in Smoke.

### 4. Evaluate against threshold
Measure against: ≥200 members and ≥20 DAU with ≥10 qualified leads in 6 weeks. If PASS, proceed to Scalable. If FAIL, narrow focus to fewer communities or try different content types.

---

## KPIs to track
- Conversion rate
- Cost per result
- Response quality
- Cycle time

---

## Pass threshold
**≥200 members and ≥20 DAU with ≥10 qualified leads in 6 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/product-aware/discord-community-building`_
