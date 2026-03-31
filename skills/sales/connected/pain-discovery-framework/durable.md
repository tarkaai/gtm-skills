---
name: pain-discovery-framework-durable
description: >
  Pain Discovery Framework — Durable Intelligence. Uncover and quantify prospect pain points to build compelling business cases and justify budget allocation, from manual discovery note-taking to AI-driven pain intelligence that surfaces high-ROI opportunities and auto-generates business case content.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Durable Intelligence"
time: "130 hours over 6 months"
outcome: "Sustained or improving pain discovery effectiveness (>=70% quantification, >=10x cost) over 6 months via continuous agent-driven question optimization, benchmark refinement, and market adaptation"
kpis: ["Pain quantification rate", "Pain-to-price ratio trend", "Agent experiment win rate", "Business case win rate"]
slug: "pain-discovery-framework"
install: "npx gtm-skills add sales/connected/pain-discovery-framework"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - multi-channel-cadence
  - dashboard-builder
  - ab-test-orchestrator
---
# Pain Discovery Framework — Durable Intelligence

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Overview
Uncover and quantify prospect pain points to build compelling business cases and justify budget allocation, from manual discovery note-taking to AI-driven pain intelligence that surfaces high-ROI opportunities and auto-generates business case content.

**Time commitment:** 130 hours over 6 months
**Pass threshold:** Sustained or improving pain discovery effectiveness (>=70% quantification, >=10x cost) over 6 months via continuous agent-driven question optimization, benchmark refinement, and market adaptation

---

## Budget

**Play-specific tools & costs**
- **Apollo or Aircall (AI-assisted calling):** ~$100–300/mo

_Total play-specific: ~$100–300/mo_

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

1. Deploy an AI agent in n8n that continuously analyzes which pain types and severities best predict closed-won deals; auto-prioritizes pain discovery based on revenue correlation.

2. Set up the agent to run experiments on pain quantification techniques: test different questioning approaches, benchmark sources, and validation methods; promote techniques with highest accuracy.

3. Build a feedback loop where every closed-won deal triggers the agent to analyze pain discovery quality; identify which pains were most influential in close decision and emphasize those in future discoveries.

4. Deploy real-time pain intelligence: agent listens to discovery calls and suggests follow-up questions mid-call to dig deeper into high-value pain areas (e.g., prospect mentions compliance—agent suggests asking about penalty costs).

5. Implement market adaptation: if certain pain types become less relevant (e.g., remote work pains decrease as offices reopen), agent adjusts discovery priorities and updates playbooks.

6. Build AI-driven business case personalization: agent analyzes prospect's industry, role, and quantified pains to generate custom business cases emphasizing most relevant ROI dimensions (CFO gets payback period, CTO gets risk reduction).

7. Create automatic pain validation sequences: agent monitors prospect engagement with pain summaries and business cases; if low engagement, suggests alternative pain framing or additional discovery.

8. Agent continuously refines pain benchmarks: learns from each new data point to improve industry/role-specific pain estimates; increases accuracy of pain quantification for prospects without measured data.

9. Implement predictive pain scoring: agent predicts which prospects will yield high quantifiable pain based on early signals (company size, industry, tech stack); prioritizes those prospects for discovery.

10. Establish monthly review cycles: agent generates pain intelligence reports showing pain type trends, quantification accuracy, ROI impact, and recommended discovery updates; team reviews and approves question library changes or rolls back underperforming experiments.

---

## KPIs to track
- Pain quantification rate
- Pain-to-price ratio trend
- Agent experiment win rate
- Business case win rate

---

## Pass threshold
**Sustained or improving pain discovery effectiveness (>=70% quantification, >=10x cost) over 6 months via continuous agent-driven question optimization, benchmark refinement, and market adaptation**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/pain-discovery-framework`_
