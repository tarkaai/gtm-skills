---
name: executive-demo-scalable
description: >
  Executive-Focused Demo — Scalable Automation. Deliver condensed, business-focused demos for C-level stakeholders emphasizing strategic value and ROI rather than feature details, from manual executive demo prep to AI-driven dynamic executive presentations that auto-adapt based on stakeholder priorities and company context.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Scalable Automation"
time: "70 hours over 2 months"
outcome: ">=75% exec demo conversion and >=35% faster close time for exec-engaged deals over 2 months"
kpis: ["Exec demo conversion rate", "Exec engagement score", "Deal velocity by exec engagement", "Demo quality score"]
slug: "executive-demo"
install: "npx gtm-skills add sales/aligned/executive-demo"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - posthog-gtm-events
---
# Executive-Focused Demo — Scalable Automation

> **Stage:** Sales → Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Overview
Deliver condensed, business-focused demos for C-level stakeholders emphasizing strategic value and ROI rather than feature details, from manual executive demo prep to AI-driven dynamic executive presentations that auto-adapt based on stakeholder priorities and company context.

**Time commitment:** 70 hours over 2 months
**Pass threshold:** >=75% exec demo conversion and >=35% faster close time for exec-engaged deals over 2 months

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
- **Clay** (Enrichment)
- **Loom** (Video)
- **Fireflies** (Sales Engagement)

---

## Instructions

1. Scale to 50+ exec demos per quarter; build n8n workflows that trigger when exec stakeholder is added to deal: pull exec research (LinkedIn, company news, tech stack) from Clay, generate custom demo agenda, send to rep with talking points.

2. Create dynamic exec demo decks that auto-populate with prospect-specific data: company name, industry, relevant case studies, tailored ROI projections; use n8n + Clay + OpenAI to generate custom slides.

3. Set up PostHog to track exec demo engagement: which slides generate questions, where execs lean in (detected via call recording sentiment analysis), which ROI metrics resonate most by persona.

4. Implement exec demo training program: record best exec demos, create playbook with winning narratives by persona, conduct role-play sessions; ensure all AEs can deliver executive-level conversations.

5. Build a library of executive proof points: peer case studies, industry benchmarks, analyst quotes, customer testimonials from recognizable brands; auto-recommend relevant proof for each exec based on industry and role.

6. Integrate call recording tools with Attio to analyze exec demo performance: use AI to score demos on time discipline, strategic framing, ROI clarity, and objection handling; provide coaching based on scores.

7. Create exec engagement scoring: track how many execs engaged per deal, seniority of execs, quality of engagement (questions, enthusiasm, next steps); high exec engagement = high close probability.

8. Each week, analyze which exec personas convert best and which are hardest to engage; refine messaging and proof points for challenging personas (e.g., if CTOs are skeptical, add more technical validation).

9. Test different exec demo formats: live interactive demo vs pre-recorded walkthrough vs exec briefing document; measure which yields highest next-step rates by persona and company size.

10. After 2 months, if >=75% exec demo conversion and exec-engaged deals close >=35% faster, move to Durable; otherwise refine exec messaging or demo structure.

---

## KPIs to track
- Exec demo conversion rate
- Exec engagement score
- Deal velocity by exec engagement
- Demo quality score

---

## Pass threshold
**>=75% exec demo conversion and >=35% faster close time for exec-engaged deals over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/aligned/executive-demo`_
