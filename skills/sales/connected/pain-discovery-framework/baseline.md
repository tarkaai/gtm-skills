---
name: pain-discovery-framework-baseline
description: >
  Pain Discovery Framework — Baseline Run. Uncover and quantify prospect pain points to build compelling business cases and justify budget allocation, from manual discovery note-taking to AI-driven pain intelligence that surfaces high-ROI opportunities and auto-generates business case content.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Baseline Run"
time: "20 hours over 2 weeks"
outcome: ">=70% of prospects with >=4 quantified pains totaling >=10x product cost over 2 weeks"
kpis: ["Quantified pain per prospect", "Pain-to-price ratio", "Pain validation rate", "Business case conversion rate"]
slug: "pain-discovery-framework"
install: "npx gtm-skills add sales/connected/pain-discovery-framework"
---
# Pain Discovery Framework — Baseline Run

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Overview
Uncover and quantify prospect pain points to build compelling business cases and justify budget allocation, from manual discovery note-taking to AI-driven pain intelligence that surfaces high-ROI opportunities and auto-generates business case content.

**Time commitment:** 20 hours over 2 weeks
**Pass threshold:** >=70% of prospects with >=4 quantified pains totaling >=10x product cost over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Apollo (includes dialer) or Aircall:** ~$50–100/mo

_Total play-specific: ~$50–100/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **Loom** (Video)

---

## Instructions

1. Expand pain discovery to 10-15 prospects over 2 weeks; build a pain discovery playbook in Attio with question frameworks for each pain category (cost, time, risk, opportunity cost).

2. Develop a pain quantification calculator: if prospect says "10 hours/week on manual reports," calculate: 10 hrs × 52 weeks × $80/hr = $41,600/year; show ROI if you save 80% = $33,280 saved.

3. Set pass threshold: uncover >=4 quantified pain points per prospect for >=70% of prospects, and total pain value >=10x your product cost over 2 weeks.

4. After each discovery call, send pain summary email: "Based on our conversation, you're spending $40K/year on [pain 1] and losing $25K in [pain 2]—total $65K. Does that align with your experience?"

5. Use validated pain to build a mini business case: "You're losing $65K/year on these issues. Our solution costs $10K/year and addresses 80% of this pain—net ROI of $42K annually."

6. Sync pain data from Attio to PostHog; create a funnel showing pain_discovered → pain_quantified → pain_validated → business_case_presented → opportunity_advanced.

7. Track which pain types most strongly correlate with deal progression: if compliance risk pains accelerate deals faster than efficiency pains, prioritize uncovering compliance issues.

8. For prospects with low quantified pain (<5x product cost), either find additional pains or consider disqualifying (weak business case = low close probability).

9. After 2 weeks, analyze: did >=70% of prospects yield >=4 quantified pains? Did prospects with strong pain quantification progress faster or close at higher rates?

10. If pain discovery yields strong quantification (>=10x product cost) and accelerates deal progression, move to Scalable; otherwise refine quantification techniques or questioning approach.

---

## KPIs to track
- Quantified pain per prospect
- Pain-to-price ratio
- Pain validation rate
- Business case conversion rate

---

## Pass threshold
**>=70% of prospects with >=4 quantified pains totaling >=10x product cost over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/pain-discovery-framework`_
