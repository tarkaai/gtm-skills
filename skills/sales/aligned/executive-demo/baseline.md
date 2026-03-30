---
name: executive-demo-baseline
description: >
  Executive-Focused Demo — Baseline Run. Deliver condensed, business-focused demos for C-level stakeholders emphasizing strategic value and ROI rather than feature details, from manual executive demo prep to AI-driven dynamic executive presentations that auto-adapt based on stakeholder priorities and company context.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Baseline Run"
time: "20 hours over 2 weeks"
outcome: ">=75% exec demo-to-nextstep conversion and >=30% faster close time for exec-engaged deals over 2 weeks"
kpis: ["Exec demo conversion", "Deal velocity (exec vs non-exec)", "Close rate (exec vs non-exec)", "Exec satisfaction score"]
slug: "executive-demo"
install: "npx gtm-skills add sales/aligned/executive-demo"
---
# Executive-Focused Demo — Baseline Run

> **Stage:** Sales → Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Overview
Deliver condensed, business-focused demos for C-level stakeholders emphasizing strategic value and ROI rather than feature details, from manual executive demo prep to AI-driven dynamic executive presentations that auto-adapt based on stakeholder priorities and company context.

**Time commitment:** 20 hours over 2 weeks
**Pass threshold:** >=75% exec demo-to-nextstep conversion and >=30% faster close time for exec-engaged deals over 2 weeks

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

1. Expand to 10-15 executive demos over 2 weeks; build persona-specific exec demo decks: CEO (growth, competitive advantage), CFO (ROI, risk), CTO (architecture, security), COO (efficiency, scale).

2. Create pre-demo research process: 15 minutes of research per exec (LinkedIn, recent company news, earnings highlights, competitive positioning) to identify top 3 priorities; tailor demo opening to those priorities.

3. Set pass threshold: >=75% of exec demos yield next-step commitment, and exec-influenced deals close >=30% faster than deals without exec engagement.

4. Structure exec demos with tight time discipline: 2 min context (their business), 3 min problem (quantified pain), 5 min solution (strategic approach), 3 min outcomes (ROI and proof), 2 min next steps; leave 5+ min for Q&A.

5. Develop executive-specific ROI narratives: CFO gets payback period and NPV, CEO gets market share and competitive positioning, CTO gets technical debt reduction and risk mitigation.

6. Sync exec engagement data from Attio to PostHog; create a funnel showing exec_demo_delivered → exec_endorsement → proposal_approved → deal_accelerated; measure exec impact on deal velocity.

7. After each exec demo, send follow-up email within 2 hours with exec summary (1-pager), ROI calculator, case study, and next-step proposal; track email engagement in PostHog.

8. For deals with multiple execs, orchestrate exec alignment: identify which exec cares about what (CFO = cost, CTO = security, CEO = strategy) and address each in tailored conversations.

9. After 2 weeks, compare deals with exec engagement vs deals without: measure close rate, deal velocity, and average deal size; if exec-engaged deals perform >=30% better, exec demos are high-leverage.

10. If >=75% exec demo next-step rate and exec-engaged deals close faster, move to Scalable; otherwise refine exec messaging or improve demo-to-decision process.

---

## KPIs to track
- Exec demo conversion
- Deal velocity (exec vs non-exec)
- Close rate (exec vs non-exec)
- Exec satisfaction score

---

## Pass threshold
**>=75% exec demo-to-nextstep conversion and >=30% faster close time for exec-engaged deals over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/aligned/executive-demo`_
