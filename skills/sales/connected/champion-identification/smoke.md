---
name: champion-identification-smoke
description: >
  Champion Identification & Development — Smoke Test. Find and nurture internal champions who advocate for your solution inside prospect organizations, from manual champion vetting to AI-driven champion development programs that increase win rates by ensuring strong internal advocates in every deal.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=3 deals with active champions and >=30% faster progression in 1 week"
kpis: ["Champions per deal", "Deal velocity (champion vs non-champion)", "Champion engagement score"]
slug: "champion-identification"
install: "npx gtm-skills add sales/connected/champion-identification"
drills:
  - icp-definition
  - threshold-engine
---
# Champion Identification & Development — Smoke Test

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Find and nurture internal champions who advocate for your solution inside prospect organizations, from manual champion vetting to AI-driven champion development programs that increase win rates by ensuring strong internal advocates in every deal.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** >=3 deals with active champions and >=30% faster progression in 1 week

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

1. Define champion criteria in a spreadsheet: has pain, sees value, willing to advocate internally, has credibility, accessible to you; score each active contact on these 5 traits (1-5).

2. Review 5-10 active deals; identify 1-2 potential champions per deal based on engagement (attends calls, asks questions, shares internal context, introduces other stakeholders).

3. Set pass threshold: identify >=1 champion in >=3 deals within 1 week, and deals with champions progress >=30% faster than deals without champions.

4. During discovery calls, ask champion-identifying questions: "How does this problem affect your day-to-day?" "Would you be willing to help us understand your org's priorities?" "Can you connect us with [specific stakeholder]?"

5. After each call, score contacts on champion traits; contacts scoring >=20/25 are champion candidates.

6. For champion candidates, send personalized enablement materials: one-pager explaining value, ROI calculator, case study from similar company; gauge their willingness to use materials internally.

7. Log champion status in Attio with custom field (No Champion, Potential Champion, Active Champion); track champion progression in PostHog as champion_identified events.

8. Test champion impact: compare deal velocity and progression for deals with Active Champions vs deals without; champions should accelerate deals by >=30%.

9. If >=3 deals have Active Champions and those deals progress >=30% faster, champions are a high-leverage sales asset.

10. Document champion identification questions and enablement materials, then proceed to Baseline; if champions don't accelerate deals, refine champion selection criteria.

---

## KPIs to track
- Champions per deal
- Deal velocity (champion vs non-champion)
- Champion engagement score

---

## Pass threshold
**>=3 deals with active champions and >=30% faster progression in 1 week**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/champion-identification`_
