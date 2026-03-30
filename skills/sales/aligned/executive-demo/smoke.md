---
name: executive-demo-smoke
description: >
  Executive-Focused Demo — Smoke Test. Deliver condensed, business-focused demos for C-level stakeholders emphasizing strategic value and ROI rather than feature details, from manual executive demo prep to AI-driven dynamic executive presentations that auto-adapt based on stakeholder priorities and company context.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Smoke Test"
time: "7 hours over 1 week"
outcome: ">=3 exec demos with >=70% next-step commitment within 1 week"
kpis: ["Exec demo-to-nextstep conversion", "Demo duration (target 15-20 min)", "Questions asked per demo", "Sentiment score"]
slug: "executive-demo"
install: "npx gtm-skills add sales/aligned/executive-demo"
---
# Executive-Focused Demo — Smoke Test

> **Stage:** Sales → Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Overview
Deliver condensed, business-focused demos for C-level stakeholders emphasizing strategic value and ROI rather than feature details, from manual executive demo prep to AI-driven dynamic executive presentations that auto-adapt based on stakeholder priorities and company context.

**Time commitment:** 7 hours over 1 week
**Pass threshold:** >=3 exec demos with >=70% next-step commitment within 1 week

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

1. Create an executive demo template (15-20 minutes max) with structure: Business context (their pain), Strategic solution (your approach), Key outcomes (quantified value), Proof (case study), Next steps (decision process); avoid feature details.

2. Identify 3 upcoming executive stakeholder calls (CEO, CFO, CTO, VP+); for each, research executive's priorities via LinkedIn, company news, earnings calls, and discovery notes.

3. Set pass threshold: deliver >=3 executive demos with >=70% achieving next-step commitment (follow-up with decision, proposal request, or trial approval) within 1 week.

4. Before each exec demo, customize opening: "[Exec name], based on your [priority from research], here's how we help companies like yours [achieve outcome]" — establish relevance in first 30 seconds.

5. Lead with business outcomes, not features: "We help companies reduce customer acquisition cost by 35%" not "We have a multi-channel attribution dashboard"; tie every point back to exec's priorities (revenue, cost, risk, competitive advantage).

6. Use executive-friendly visuals: simple charts showing ROI, before/after comparisons, customer testimonials from peer companies; avoid technical screenshots or feature lists.

7. Include peer proof points: "Companies like [similar company in their industry] saw [quantified result] in [timeframe]" — executives trust peer experiences.

8. Reserve 5-10 minutes for Q&A; expect strategic questions ("How does this integrate with our roadmap?" "What's the implementation timeline?" "What resources do we need?").

9. Log exec demo outcomes in Attio with fields for exec_title, demo_duration, questions_asked, next_step_committed, and sentiment_score; track which approaches resonate.

10. If >=3 exec demos yield >=70% next-step commitment, executive demo format is working; document template and proceed to Baseline; otherwise refine value messaging or demo structure.

---

## KPIs to track
- Exec demo-to-nextstep conversion
- Demo duration (target 15-20 min)
- Questions asked per demo
- Sentiment score

---

## Pass threshold
**>=3 exec demos with >=70% next-step commitment within 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/aligned/executive-demo`_
