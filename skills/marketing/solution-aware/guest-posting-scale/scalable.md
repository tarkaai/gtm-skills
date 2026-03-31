---
name: guest-posting-scale-scalable
description: >
  Guest Posting at Scale — Scalable Automation. Publish guest posts on relevant industry blogs to build backlinks and awareness, from manual pitching to automated outreach and AI-driven content placement optimization.
stage: "Marketing > Solution Aware"
motion: "PR & Earned Mentions"
channels: "Content, Email"
level: "Scalable Automation"
time: "55 hours over 2 months"
outcome: "≥20 published articles and ≥1,500 referral visits/month"
kpis: ["Pitch acceptance rate", "Articles published", "Referral traffic", "Backlinks acquired", "Conversion rate", "Cost per published article"]
slug: "guest-posting-scale"
install: "npx gtm-skills add marketing/solution-aware/guest-posting-scale"
drills:
  - social-content-pipeline
  - blog-seo-pipeline
  - build-prospect-list
  - cold-email-sequence
  - content-repurposing
  - posthog-gtm-events
---
# Guest Posting at Scale — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** PR & Earned Mentions | **Channels:** Content, Email

## Overview
Publish guest posts on relevant industry blogs to build backlinks and awareness, from manual pitching to automated outreach and AI-driven content placement optimization.

**Time commitment:** 55 hours over 2 months
**Pass threshold:** ≥20 published articles and ≥1,500 referral visits/month

---

## Budget

**Play-specific tools & costs**
- **Featured.com (expert quote placements):** ~$100/mo
- **Qwoted Pro:** ~$50/mo

_Total play-specific: ~$50–100/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **n8n** (Automation)
- **Attio** (CRM)
- **Ahrefs** (Analytics)
- **Anthropic** (AI/LLM)
- **Instantly** (Email)

---

## Instructions

1. Scale target list to 150-200 blogs; build n8n workflow to automate blog discovery via Ahrefs API (find blogs in your niche with DA 30+, accepting guest posts).

2. Create n8n outreach automation: fetch blog details, generate personalized pitches using AI (referencing recent articles), send via email, and track responses in Attio.

3. Send 100-120 pitches over 2 months (12-15 per week); n8n automatically follows up with non-responders after 7 days with a different angle.

4. Build AI content pipeline: for accepted pitches, n8n generates article drafts via Anthropic API based on approved outlines; human editor reviews and finalizes before submission.

5. Implement backlink strategy: for each article, identify 2-3 strategic internal pages to link to; track backlink acquisition in Ahrefs and referral traffic in PostHog.

6. Set guardrails: acceptance rate must stay ≥15%; if it drops below, pause outreach and refine pitch templates or target blog criteria.

7. Connect PostHog to n8n: when a guest post drives ≥100 referral visits, trigger workflow to repurpose the article into LinkedIn posts, Twitter threads, and email newsletter content.

8. Use PostHog to track conversion journeys from guest post referrals; identify which blog tiers and topics drive highest conversion rates.

9. After 2 months, evaluate: total articles published, backlinks acquired, referral traffic volume, and conversions; calculate cost per published article and cost per acquisition.

10. If metrics hold and ROI is positive, document the automated outreach and content pipeline and prepare for Durable agent-driven optimization; if metrics decline, reduce outreach volume or improve pitch quality.

---

## KPIs to track
- Pitch acceptance rate
- Articles published
- Referral traffic
- Backlinks acquired
- Conversion rate
- Cost per published article

---

## Pass threshold
**≥20 published articles and ≥1,500 referral visits/month**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/guest-posting-scale`_
