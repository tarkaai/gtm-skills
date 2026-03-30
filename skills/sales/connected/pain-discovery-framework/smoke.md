---
name: pain-discovery-framework-smoke
description: >
  Pain Discovery Framework — Smoke Test. Uncover and quantify prospect pain points to build compelling business cases and justify budget allocation, from manual discovery note-taking to AI-driven pain intelligence that surfaces high-ROI opportunities and auto-generates business case content.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Smoke Test"
time: "7 hours over 1 week"
outcome: ">=3 quantified pain points per prospect for >=3 prospects with total pain >=5x product cost in 1 week"
kpis: ["Pain points per prospect", "Quantification rate", "Pain-to-price ratio", "Discovery call quality"]
slug: "pain-discovery-framework"
install: "npx gtm-skills add sales/connected/pain-discovery-framework"
---
# Pain Discovery Framework — Smoke Test

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Overview
Uncover and quantify prospect pain points to build compelling business cases and justify budget allocation, from manual discovery note-taking to AI-driven pain intelligence that surfaces high-ROI opportunities and auto-generates business case content.

**Time commitment:** 7 hours over 1 week
**Pass threshold:** >=3 quantified pain points per prospect for >=3 prospects with total pain >=5x product cost in 1 week

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)

---

## Instructions

1. Create a pain discovery template in a spreadsheet with columns: Pain Type (inefficiency, revenue loss, compliance risk, manual work), Description, Quantified Impact ($/time), Frequency, Owner, Urgency (1-5).

2. Select 5 active discovery calls; prepare 5-7 pain discovery questions: "What's your biggest challenge with [process]?" "How much time does your team spend on [task]?" "What does [problem] cost you per month?" "What happens if you don't solve this?"

3. Set pass threshold: uncover >=3 quantified pain points per prospect for >=3 prospects within 1 week, and quantified pain >=5x your product's cost.

4. During calls, ask open-ended pain questions, then drill into impact: "You said 10 hours/week—at $100/hour, that's $4K/month. Is that accurate?" Validate and document numbers.

5. After each call, fill out pain template; categorize each pain point and calculate annual cost impact; share summary with prospect for validation.

6. Log pain points in Attio with custom fields for pain_type, quantified_impact, and urgency_score; track total pain value per opportunity.

7. In PostHog, create events for pain_discovered and pain_quantified with properties for pain type, value, and discovery stage.

8. Test whether prospects with >=3 quantified pains progress faster to proposal stage than prospects with vague or unquantified pains.

9. After 1 week, analyze: did you uncover >=3 quantified pains for >=3 prospects? Is total pain >=5x your pricing? If yes, pain discovery is working.

10. If threshold met, document pain questions and quantification method, then proceed to Baseline; otherwise refine questions to surface quantifiable impact.

---

## KPIs to track
- Pain points per prospect
- Quantification rate
- Pain-to-price ratio
- Discovery call quality

---

## Pass threshold
**>=3 quantified pain points per prospect for >=3 prospects with total pain >=5x product cost in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/pain-discovery-framework`_
