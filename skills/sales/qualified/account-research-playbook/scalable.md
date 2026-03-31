---
name: account-research-playbook-scalable
description: >
  Account Research & Intelligence — Scalable Automation. Systematically research target accounts before outreach to personalize messaging and improve relevance, from manual LinkedIn research to AI-driven account intelligence that auto-generates comprehensive account profiles with buying signals and talk tracks.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Scalable Automation"
time: "70 hours over 2 months"
outcome: ">=80% research automation and >=35% reply rate maintained over 2 months"
kpis: ["Research automation rate", "Research accuracy", "Reply rate by research type", "Time savings"]
slug: "account-research-playbook"
install: "npx gtm-skills add sales/qualified/account-research-playbook"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - posthog-gtm-events
---
# Account Research & Intelligence — Scalable Automation

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Systematically research target accounts before outreach to personalize messaging and improve relevance, from manual LinkedIn research to AI-driven account intelligence that auto-generates comprehensive account profiles with buying signals and talk tracks.

**Time commitment:** 70 hours over 2 months
**Pass threshold:** >=80% research automation and >=35% reply rate maintained over 2 months

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
- **Attio** (CRM)
- **PostHog** (CDP)
- **n8n** (Automation)
- **Clay** (Enrichment)
- **OpenAI** (AI/LLM)
- **LinkedIn Sales Navigator** (Channel)

---

## Instructions

1. Scale account research to 200+ accounts per month; build n8n workflows that auto-research accounts when added to target list: pull data from Clay, scrape news from Google, analyze tech stack from BuiltWith, compile LinkedIn contacts, generate account brief, save to Attio.

2. Create AI-powered account research using OpenAI API: feed account name and industry to AI, generate comprehensive account brief including company overview, likely pain points, recent news, personalization hooks, and suggested talk tracks.

3. Set up PostHog to track research effectiveness: monitor reply rates, meeting conversion, and deal velocity by research depth; optimize for highest-ROI research activities (e.g., if tech stack research doesn't improve outcomes, deprioritize it).

4. Build account scoring based on research signals: assign points for positive signals (recent funding +15, hiring for relevant role +10, uses competitor +20, fast-growing +10); prioritize high-scoring accounts for outreach.

5. Implement trigger-based research alerts: when target accounts trigger key events (funding announcement, executive hire, product launch), n8n detects via news/LinkedIn monitoring, updates account brief in Attio, notifies SDR to reach out immediately.

6. Create persona-specific research templates: for CFO outreach, emphasize financial metrics and ROI; for CTO, emphasize tech stack and integrations; for VP Sales, emphasize sales efficiency and pipeline.

7. Build a research quality dashboard in PostHog showing research completion rate, average research time, signal coverage (% of accounts with each signal type), and correlation between research depth and outcomes.

8. Each week, analyze which research signals most strongly predict engagement and conversion; double down on high-signal research, reduce time on low-signal activities.

9. Test automated vs manual research: compare AI-generated briefs vs human-researched briefs on accuracy, usefulness, and outcome impact; optimize for best combination of speed and quality.

10. After 2 months, if automated research covers >=80% of accounts with >=90% accuracy and reply rates remain >=35%, move to Durable; otherwise refine AI prompts or data sources.

---

## KPIs to track
- Research automation rate
- Research accuracy
- Reply rate by research type
- Time savings

---

## Pass threshold
**>=80% research automation and >=35% reply rate maintained over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/account-research-playbook`_
