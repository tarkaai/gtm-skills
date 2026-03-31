---
name: account-research-playbook-baseline
description: >
  Account Research & Intelligence — Baseline Run. Systematically research target accounts before outreach to personalize messaging and improve relevance, from manual LinkedIn research to AI-driven account intelligence that auto-generates comprehensive account profiles with buying signals and talk tracks.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "24 hours over 2 weeks"
outcome: ">=35% reply rate from researched outreach and >=2.5x faster progression to meetings over 2 weeks"
kpis: ["Reply rate by research depth", "Meeting rate (researched vs non-researched)", "Research time efficiency", "Signal-to-reply correlation"]
slug: "account-research-playbook"
install: "npx gtm-skills add sales/qualified/account-research-playbook"
drills:
  - icp-definition
  - build-prospect-list
  - cold-email-sequence
  - threshold-engine
---
# Account Research & Intelligence — Baseline Run

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Systematically research target accounts before outreach to personalize messaging and improve relevance, from manual LinkedIn research to AI-driven account intelligence that auto-generates comprehensive account profiles with buying signals and talk tracks.

**Time commitment:** 24 hours over 2 weeks
**Pass threshold:** >=35% reply rate from researched outreach and >=2.5x faster progression to meetings over 2 weeks

---

## Budget

**Play-specific tools & costs**
- **Instantly or Smartlead (email sequencing):** ~$40–100/mo
- **Clay or Apollo (list building + enrichment):** ~$50–150/mo

_Total play-specific: ~$40–150/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)
- **Clay** (Enrichment)
- **LinkedIn Sales Navigator** (Channel)

---

## Instructions

1. Expand account research to 30-50 accounts over 2 weeks; create a standardized research workflow: LinkedIn (company page, key contacts), Crunchbase (funding, investors), job postings (hiring signals), G2 reviews (competitor usage, pain points), news (Google News, company blog).

2. Integrate research tools: use LinkedIn Sales Nav for contact identification, BuiltWith or Wappalyzer for tech stack detection, Crunchbase for funding data; compile findings in Attio.

3. Set pass threshold: research 40+ accounts, achieve >=35% reply rate from researched outreach, and researched accounts progress to meetings >=2.5x faster than non-researched.

4. Develop research-to-messaging frameworks by signal type: Funding ("As you scale with new capital..."), Executive hire ("As [name] builds out [function]..."), Product launch ("Congrats on launching X—as you onboard customers..."), Competitor usage ("Noticed you're using [competitor]—customers switch to us for [differentiation]...").

5. Enrich accounts with Clay: pull firmographic data (revenue, employee count, location), technographic data (martech/sales stack), funding history, and recent news; auto-populate Attio fields.

6. Sync enriched account data from Attio to PostHog; create cohorts of accounts by research depth (no research, basic, deep) and measure engagement and conversion differences.

7. Train SDRs on account research: show examples of high-quality research, demonstrate how to find personalization hooks, role-play converting research into compelling outreach.

8. After each outreach attempt, log which research insights were used and whether prospect referenced them in reply; track which signals resonate most (funding, tech stack, job postings, news).

9. After 2 weeks, measure research ROI: time spent on research vs lift in reply rate, meeting rate, and pipeline value; if researched accounts generate >=3x ROI on time invested, research pays off.

10. If reply rate >=35% and researched accounts progress >=2.5x faster, move to Scalable; otherwise refine research workflow or improve research-to-messaging translation.

---

## KPIs to track
- Reply rate by research depth
- Meeting rate (researched vs non-researched)
- Research time efficiency
- Signal-to-reply correlation

---

## Pass threshold
**>=35% reply rate from researched outreach and >=2.5x faster progression to meetings over 2 weeks**

If you hit this threshold → move to the **Scalable Automation** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/account-research-playbook`_
