---
name: pain-discovery-framework-scalable
description: >
  Pain Discovery Framework — Scalable Automation. Uncover and quantify prospect pain points to build compelling business cases and justify budget allocation, from manual discovery note-taking to AI-driven pain intelligence that surfaces high-ROI opportunities and auto-generates business case content.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Scalable Automation"
time: "70 hours over 2 months"
outcome: ">=70% of prospects with quantified pains >=10x cost and >=30% faster deal velocity over 2 months"
kpis: ["Pain quantification rate", "Pain-to-price ratio", "AI extraction accuracy", "Business case conversion rate"]
slug: "pain-discovery-framework"
install: "npx gtm-skills add sales/connected/pain-discovery-framework"
---
# Pain Discovery Framework — Scalable Automation

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Overview
Uncover and quantify prospect pain points to build compelling business cases and justify budget allocation, from manual discovery note-taking to AI-driven pain intelligence that surfaces high-ROI opportunities and auto-generates business case content.

**Time commitment:** 70 hours over 2 months
**Pass threshold:** >=70% of prospects with quantified pains >=10x cost and >=30% faster deal velocity over 2 months

---

## Budget

**Play-specific tools & costs**
- **Apollo or Aircall (calling at volume):** ~$100–200/mo

_Total play-specific: ~$100–200/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Fireflies** (Sales Engagement)
- **OpenAI** (AI/LLM)

---

## Instructions

1. Scale pain discovery to 50+ prospects per quarter; integrate call recording tools (Fireflies, Gong) with Attio to auto-extract pain points from discovery call transcripts.

2. Build an n8n workflow that triggers after each discovery call: pull transcript from Fireflies, use AI to identify pain statements, extract quantifiable metrics, create pain summary in Attio, notify rep to validate.

3. Create industry-specific pain benchmarks: if you know SaaS companies typically spend 15% of revenue on customer support, use benchmarks to help prospects quantify pains they haven't measured.

4. Set up PostHog to track pain discovery effectiveness: measure pain points per call, quantification rate, and correlation between total pain value and close probability.

5. Build automated pain validation sequences in n8n: after extracting pains, send email with summary and ask prospect to confirm numbers; log validation status in Attio.

6. In Attio, create a pain intelligence dashboard showing distribution of pain types, average pain-to-price ratio, and which pains most strongly predict closed deals.

7. Develop AI-generated business cases: use Claude or GPT-4 to automatically generate business case documents based on quantified pains in Attio; reps review and send to prospects.

8. Implement pain prioritization: if prospects have 5+ pains, use AI to rank by impact, urgency, and alignment with your solution's strengths; focus on top 3 in proposals.

9. Each week, analyze which pain discovery questions yield highest quantification rates; update playbook with winning questions and retire low-signal questions.

10. After 2 months, if >=70% of prospects have quantified pains >=10x cost and pain-rich deals close >=30% faster, move to Durable; otherwise refine AI extraction or benchmarking.

---

## KPIs to track
- Pain quantification rate
- Pain-to-price ratio
- AI extraction accuracy
- Business case conversion rate

---

## Pass threshold
**>=70% of prospects with quantified pains >=10x cost and >=30% faster deal velocity over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/pain-discovery-framework`_
