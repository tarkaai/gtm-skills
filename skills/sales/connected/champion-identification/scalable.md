---
name: champion-identification-scalable
description: >
  Champion Identification & Development — Scalable Automation. Find and nurture internal champions who advocate for your solution inside prospect organizations, from manual champion vetting to AI-driven champion development programs that increase win rates by ensuring strong internal advocates in every deal.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Scalable Automation"
time: "65 hours over 2 months"
outcome: ">=60% of deals with active champions and >=40% higher win rate over 2 months"
kpis: ["Champion rate", "Champion engagement score", "Win rate lift", "Champion health score"]
slug: "champion-identification"
install: "npx gtm-skills add sales/connected/champion-identification"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - posthog-gtm-events
---
# Champion Identification & Development — Scalable Automation

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Find and nurture internal champions who advocate for your solution inside prospect organizations, from manual champion vetting to AI-driven champion development programs that increase win rates by ensuring strong internal advocates in every deal.

**Time commitment:** 65 hours over 2 months
**Pass threshold:** >=60% of deals with active champions and >=40% higher win rate over 2 months

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
- **Loom** (Video)

---

## Instructions

1. Scale champion development to 50+ deals per quarter; integrate PostHog with Attio to auto-score champion candidates based on engagement behaviors (call attendance, email clicks, material shares).

2. Build an n8n workflow that triggers when a contact hits high engagement thresholds: send automated champion recruitment email with enablement kit, log as champion_candidate in Attio, notify rep.

3. Create tiered champion enablement kits by deal size: SMB kit (one-pager, case study), Mid-market (ROI calculator, implementation plan), Enterprise (executive briefing, CFO business case, security docs).

4. Set up PostHog to track champion engagement across multiple dimensions: material downloads, internal forwards (tracked via unique links), stakeholder introductions, meeting attendance.

5. In Attio, create automated champion nurture sequences: drip educational content, share customer success stories, provide competitive intelligence, offer to join champion-only events or workshops.

6. Build a champion health score in n8n: combine engagement data from PostHog, Attio activity, and meeting attendance; champions dropping below threshold get proactive outreach.

7. Launch a champion advocacy program: invite high-engagement champions to exclusive dinners, early product access, or advisory board; deepen their investment in your success.

8. Track champion impact in PostHog: create cohorts for champion deals vs non-champion deals; measure win rate, deal size, and velocity differences; target >=40% lift in win rate.

9. Each week, identify deals without champions (high risk); assign reps to specifically recruit champions in those deals or consider disqualifying if no champion emerges.

10. After 2 months, if >=60% of deals have Active Champions and champion deals win >=40% more often, move to Durable; otherwise refine recruitment tactics or enablement content.

---

## KPIs to track
- Champion rate
- Champion engagement score
- Win rate lift
- Champion health score

---

## Pass threshold
**>=60% of deals with active champions and >=40% higher win rate over 2 months**

If you hit this threshold → move to the **Durable Intelligence** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/champion-identification`_
