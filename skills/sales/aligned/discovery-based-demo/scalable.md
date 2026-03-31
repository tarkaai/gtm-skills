---
name: discovery-based-demo-scalable
description: >
  Discovery-Based Demo — Scalable Automation. Tailor product demos to pain points uncovered in discovery to maximize relevance and engagement, from manual demo customization to AI-driven dynamic demos that auto-adapt based on prospect signals and deliver personalized value narratives.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Product"
level: "Scalable Automation"
time: "75 hours over 2 months"
outcome: ">=70% demo-to-nextstep and >=45% demo-to-proposal conversion over 2 months"
kpis: ["Demo-to-nextstep conversion", "Demo-to-proposal conversion", "Demo personalization score", "Engagement analytics"]
slug: "discovery-based-demo"
install: "npx gtm-skills add sales/aligned/discovery-based-demo"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - posthog-gtm-events
---
# Discovery-Based Demo — Scalable Automation

> **Stage:** Sales → Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product

## Overview
Tailor product demos to pain points uncovered in discovery to maximize relevance and engagement, from manual demo customization to AI-driven dynamic demos that auto-adapt based on prospect signals and deliver personalized value narratives.

**Time commitment:** 75 hours over 2 months
**Pass threshold:** >=70% demo-to-nextstep and >=45% demo-to-proposal conversion over 2 months

---

## Budget

**Play-specific tools & costs**
- **Apollo or Aircall (calling at volume):** ~$100–200/mo
- **Intercom or Loops (automated sequences):** ~$100–300/mo

_Total play-specific: ~$100–300/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Loom** (Video)
- **Fireflies** (Sales Engagement)

---

## Instructions

1. Scale to 50+ demos per quarter; integrate Attio with demo automation tools to auto-populate demo environments with prospect-specific data (company name, use case examples).

2. Build an n8n workflow that triggers before scheduled demos: pull discovery notes from Attio, identify top pains, generate custom demo agenda, send pre-demo email with agenda to prospect and rep.

3. Create personalized demo environments using tools like Walnut or Navattic: pre-configure product with prospect's branding, sample data relevant to their use case, and workflows that match their processes.

4. Set up PostHog to track in-demo engagement: which features shown, time spent on each section, questions asked (via call recording analysis), drop-off points.

5. In Attio, create demo scoring: rate each demo on preparation quality (1-5), pain coverage (1-5), engagement (1-5), and outcome (1-5); identify patterns in high-scoring demos.

6. Build automated demo follow-up sequences in n8n: send recap video + ROI summary within 2 hours, send case study relevant to top pain in 2 days, send competitive comparison in 4 days if no response.

7. Integrate call recording tools with PostHog to analyze demo sentiment: use AI to detect prospect engagement cues ("That's interesting!", "Can you show that again?") and flag high-engagement demos for fast follow-up.

8. Create a demo performance dashboard in PostHog showing demo-to-nextstep rate, average engagement score, most-shown features, and correlation between pain coverage and outcomes.

9. Each week, identify low-performing demos (no next step, low engagement); review recordings to understand why customization failed and update demo playbook.

10. After 2 months, if >=70% of demos yield next steps and demo-to-proposal conversion >=45%, move to Durable; otherwise refine personalization or follow-up sequences.

---

## KPIs to track
- Demo-to-nextstep conversion
- Demo-to-proposal conversion
- Demo personalization score
- Engagement analytics

---

## Pass threshold
**>=70% demo-to-nextstep and >=45% demo-to-proposal conversion over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/aligned/discovery-based-demo`_
