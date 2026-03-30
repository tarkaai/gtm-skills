---
name: guest-posting-scale-durable
description: >
  Guest Posting at Scale — Durable Intelligence. Publish guest posts on relevant industry blogs to build backlinks and awareness, from manual pitching to automated outreach and AI-driven content placement optimization.
stage: "Marketing > Solution Aware"
motion: "PR & Earned Mentions"
channels: "Content, Email"
level: "Durable Intelligence"
time: "90 hours over 6 months"
outcome: "Sustained or improving guest post acceptance rate and referral traffic over 6 months via continuous AI-driven outreach optimization and relationship management"
kpis: ["Pitch acceptance rate trend", "Articles published per month", "Referral traffic trend", "Backlink acquisition rate", "Conversion rate", "Blog relationship strength"]
slug: "guest-posting-scale"
install: "npx gtm-skills add marketing/solution-aware/guest-posting-scale"
---
# Guest Posting at Scale — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** PR & Earned Mentions | **Channels:** Content, Email

## Overview
Publish guest posts on relevant industry blogs to build backlinks and awareness, from manual pitching to automated outreach and AI-driven content placement optimization.

**Time commitment:** 90 hours over 6 months
**Pass threshold:** Sustained or improving guest post acceptance rate and referral traffic over 6 months via continuous AI-driven outreach optimization and relationship management

---

## Budget

**Play-specific tools & costs**
- **Featured.com + Qwoted:** ~$150/mo
- **PR Newswire (occasional press release distribution):** ~$300–1,000 per release

_Total play-specific: ~$150–1000/mo_

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **PostHog** (CDP)
- **n8n** (Automation)
- **Attio** (CRM)
- **Ahrefs** (Analytics)
- **Anthropic** (AI/LLM)
- **Instantly** (Email)

---

## Instructions

1. Deploy PostHog event streams that trigger n8n AI agents when: new high-DA blogs emerge in your niche, published guest posts gain traction, or backlink value changes.

2. Build n8n AI outreach strategist that analyzes pitch acceptance patterns: identifies which pitch angles, topics, and blog types yield highest acceptance rates; automatically refines pitch templates monthly.

3. Implement continuous pitch experimentation: AI agent tests different pitch structures, subject lines, and personalization approaches; promotes winning variants and retires low-performers.

4. Create automatic blog discovery and scoring: n8n monitors new blogs via Ahrefs API and RSS feeds; AI agent scores blogs by DA, audience overlap, and historical acceptance rates; automatically adds high-potential blogs to target list.

5. Build learning loop: PostHog tracks conversion journeys from each guest post; AI agent analyzes which blog tiers, topics, and backlink placements drive highest ROI; adjusts outreach prioritization accordingly.

6. Deploy AI content optimization agent: analyzes top-performing published articles by engagement and referral traffic; generates content briefs for future pitches based on winning patterns.

7. Implement relationship nurturing automation: for editors who accepted pitches, n8n schedules follow-up pitches quarterly; AI generates new pitch ideas based on blog's recent content themes.

8. Create competitor guest post monitoring: n8n tracks where competitors publish guest posts via Ahrefs backlink analysis; AI agent generates pitches for the same blogs with differentiated angles.

9. Set guardrails: if acceptance rate drops below 12% for 3+ weeks or referral traffic declines >20%, n8n alerts team and agent suggests strategy adjustments.

10. Establish monthly review cycle: analyze which outreach experiments succeeded, which blog relationships to deepen, which topics to prioritize; refine AI agent prompts and outreach strategy based on acceptance and conversion data.

---

## KPIs to track
- Pitch acceptance rate trend
- Articles published per month
- Referral traffic trend
- Backlink acquisition rate
- Conversion rate
- Blog relationship strength

---

## Pass threshold
**Sustained or improving guest post acceptance rate and referral traffic over 6 months via continuous AI-driven outreach optimization and relationship management**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/guest-posting-scale`_
