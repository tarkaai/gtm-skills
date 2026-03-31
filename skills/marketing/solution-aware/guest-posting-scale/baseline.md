---
name: guest-posting-scale-baseline
description: >
  Guest Posting at Scale — Baseline Run. Publish guest posts on relevant industry blogs to build backlinks and awareness, from manual pitching to automated outreach and AI-driven content placement optimization.
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
  - social-content-pipeline
  - blog-seo-pipeline
  - build-prospect-list
  - threshold-engine
---
# Guest Posting at Scale — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** PR & Earned Mentions | **Channels:** Content, Email

## Overview
Publish guest posts on relevant industry blogs to build backlinks and awareness, from manual pitching to automated outreach and AI-driven content placement optimization.

**Time commitment:** 25 hours over 6 weeks
**Pass threshold:** ≥6 published articles and ≥300 referral visits

---

## Budget

**Play-specific tools & costs**
- **Qwoted or HARO (journalist/podcast request monitoring):** Free–$50/mo

_Total play-specific: Free–$50/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **Attio** (CRM)
- **Ahrefs** (Analytics)
- **Anthropic** (AI/LLM)

---

## Instructions

1. Expand target list to 40-50 industry blogs and publications; categorize by tier (Tier 1: DA 50+, Tier 2: DA 30-50, Tier 3: DA 20-30).

2. Create 5-7 article templates that can be customized for different blogs: how-to guides, case studies, industry trends, tool comparisons.

3. Develop 10-15 pitch templates tailored to different blog types and topics; personalize each pitch with specific article references and value propositions.

4. Send 30-40 pitches over 4 weeks (8-10 per week); track in Attio or spreadsheet with follow-up reminders for non-responses after 1 week.

5. Set pass threshold: ≥8 pitches accepted and ≥6 articles published over 6 weeks, with combined referral traffic ≥300 visits.

6. For accepted pitches, write or use AI (Claude/GPT-4) to generate first drafts; edit thoroughly for quality and include 2-3 strategic backlinks.

7. Set up PostHog to track referral traffic by guest post source; measure conversion rate from guest post readers to signup or demo.

8. Use Ahrefs to monitor new backlinks from published guest posts; track impact on domain authority and organic search rankings.

9. After 6 weeks, calculate ROI: time invested vs. referral traffic, backlinks acquired, and conversions generated.

10. If you hit the threshold and ROI is positive, document your outreach templates, target blog list, and content templates and proceed to Scalable; if not, refine pitch quality or target higher-relevance blogs.

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

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/guest-posting-scale`_
