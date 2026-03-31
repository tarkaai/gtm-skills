---
name: usage-limit-sales-upsell-scalable
description: >
  Usage-Based Upsell — Scalable Automation. Trigger upsell conversations when customers hit usage limits or demonstrate expansion readiness through product engagement, from manual usage monitoring to AI-driven upsell orchestration that identifies optimal upgrade moments and auto-generates expansion proposals.
stage: "Sales > Won"
motion: "Outbound Founder-Led"
channels: "Product, Email, Direct"
level: "Scalable Automation"
time: "70 hours over 2 months"
outcome: ">=35% upsell conversion for high-scoring accounts and expansion ARR >=15% of base ARR over 2 months"
kpis: ["Expansion conversion by score tier", "Expansion ARR growth", "Self-service vs assisted upsell mix", "Prompt engagement rate"]
slug: "usage-limit-sales-upsell"
install: "npx gtm-skills add sales/won/usage-limit-sales-upsell"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - posthog-gtm-events
---
# Usage-Based Upsell — Scalable Automation

> **Stage:** Sales → Won | **Motion:** Outbound Founder-Led | **Channels:** Product, Email, Direct

## Overview
Trigger upsell conversations when customers hit usage limits or demonstrate expansion readiness through product engagement, from manual usage monitoring to AI-driven upsell orchestration that identifies optimal upgrade moments and auto-generates expansion proposals.

**Time commitment:** 70 hours over 2 months
**Pass threshold:** >=35% upsell conversion for high-scoring accounts and expansion ARR >=15% of base ARR over 2 months

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing, scaled):** ~$100–200/mo
- **Clay (enrichment + AI personalization):** ~$150–400/mo
- **LinkedIn Sales Navigator (prospecting, optional):** ~$100/mo

_Total play-specific: ~$100–400/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **Attio** (CRM)
- **n8n** (Automation)
- **Instantly** (Email)

---

## Instructions

1. Scale to 200+ customers; build n8n workflows that trigger automatically when PostHog detects expansion signals: send usage alert email, create upsell task in Attio, notify account owner, schedule follow-up if no response.

2. Implement in-product upsell prompts using PostHog: when user hits usage threshold, show banner "You're at 90% of your seat limit—upgrade now to add more team members" with direct upgrade link.

3. Create expansion scoring in PostHog: combine usage level (40%), growth velocity (30%), feature adoption (20%), and engagement (10%) to generate expansion readiness score 0-100; target >=35% conversion for high-scoring accounts (>=70).

4. Set up PostHog to track expansion funnel: usage_threshold_hit → upsell_prompt_shown → upsell_engaged → upsell_closed; identify drop-off points and optimize.

5. Build automated expansion sequences in n8n: first touch (usage alert), second touch (ROI reminder: "You've saved $X—expand to save $Y more"), third touch (urgency: "You'll hit limit in 3 days"), fourth touch (personal call from CSM/AE).

6. Integrate usage data with Attio to auto-calculate expansion opportunity size: if customer is at 8/10 seats and adding 1 seat/month, project they'll need 15 seats in 6 months; present upgrade to 15-20 seat plan.

7. Create customer segmentation for expansion: Enterprise (high-touch, AE-led), Mid-market (CSM-led, assisted upsell), SMB (self-service, in-product prompts); route expansion opportunities accordingly.

8. Each week, analyze which expansion signals yield highest conversion rates and largest deal sizes; prioritize resources on high-ROI signals (e.g., if seat expansion converts 50% vs API limit 20%, focus on seat expansion).

9. Test expansion pricing strategies: volume discounts ("Upgrade to 50 seats and save 20%"), annual commitments ("Upgrade to annual and get 2 months free"), bundling ("Add X feature for only $Y/mo extra").

10. After 2 months, if expansion conversion >=35% for high-scoring accounts and expansion ARR >=15% of base ARR, move to Durable; otherwise refine scoring or prompt effectiveness.

---

## KPIs to track
- Expansion conversion by score tier
- Expansion ARR growth
- Self-service vs assisted upsell mix
- Prompt engagement rate

---

## Pass threshold
**>=35% upsell conversion for high-scoring accounts and expansion ARR >=15% of base ARR over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/won/usage-limit-sales-upsell`_
