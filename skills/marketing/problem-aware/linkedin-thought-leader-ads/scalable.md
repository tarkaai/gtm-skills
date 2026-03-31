---
name: linkedin-thought-leader-ads-scalable
description: >
  Thought Leader Ads — Scalable. Automated content-to-ads pipeline across multiple thought leaders,
  AI-powered creative production, audience expansion with dynamic budget allocation, and integrated
  performance dashboards. Target 10x Baseline lead volume without proportional time investment.
stage: "Marketing > ProblemAware"
motion: "LightweightPaid"
channels: "Paid, Social"
level: "Scalable"
time: "60 hours over 3 months"
outcome: ">=250,000 impressions and >=70 qualified leads/month from $5,000-10,000/month budget, with cost per qualified lead below $120 and content pipeline producing 8+ promotable posts/month"
kpis: ["Monthly impressions", "Monthly qualified leads", "Cost per qualified lead", "Content velocity (promotable posts/month)", "Audience segment conversion rates", "Thought leader count", "Budget efficiency trend"]
slug: "linkedin-thought-leader-ads"
install: "npx gtm-skills add marketing/problem-aware/linkedin-thought-leader-ads"
drills:
  - budget-allocation
---

# Thought Leader Ads — Scalable

> **Stage:** Marketing > ProblemAware | **Motion:** LightweightPaid | **Channels:** Paid, Social

## Outcomes

Find the 10x multiplier. The content-to-ads pipeline is automated: the agent generates post drafts, the thought leaders review and publish, and n8n workflows automatically identify top performers and queue them for promotion. Multiple thought leaders (2-3) feed the program, expanding both content supply and audience resonance. Budget allocation across segments and thought leaders is data-driven and rebalanced weekly. The system produces 70+ qualified leads per month without proportional increase in human time.

**Pass threshold:** >=250,000 impressions and >=70 qualified leads/month from $5,000-10,000/month budget, with cost per qualified lead below $120, sustained for 3 months.

## Leading Indicators

- Content pipeline produces 8+ TLA-eligible posts per month across all thought leaders
- Automated organic-to-paid selection workflow runs weekly without manual intervention
- Creative rotation keeps average ad age below 3 weeks
- At least 2 thought leaders actively producing content
- Budget reallocation happens weekly based on segment performance data
- Cost per qualified lead is trending down (or stable) month over month
- Audience fatigue index stays below threshold (frequency < 5/week per segment)

## Instructions

### 1. Scale Content Production

Run the the tla content scaling workflow (see instructions below) drill:

1. **Build the content playbook** from Baseline data:
   - Analyze all promoted posts from Baseline: tag by hook type, pain point, format, and post length
   - Identify top 3 content templates by composite performance (engagement rate + CTR + conversion rate)
   - Document the winning patterns in a content playbook

2. **Deploy AI-assisted batch production:**
   - Generate 5-7 draft posts per thought leader per week using Claude and the `ai-content-ghostwriting` fundamental
   - Drafts follow the winning templates with ICP pain points rotated
   - Thought leader reviews and approves in 30 minutes/week
   - Schedule 3-4 posts/week via Taplio or Buffer

3. **Automate the organic-to-paid pipeline:**
   - Build the n8n workflow from the tla content scaling workflow (see instructions below) that runs every Monday:
     - Pulls last week's organic post performance via Taplio/Shield API
     - Scores each post against TLA selection criteria
     - Auto-recommends posts scoring above threshold for promotion
     - Sends Slack notification for human approval (or auto-promotes if confidence is high)
   - Build the fatigue monitor workflow that runs daily:
     - Checks per-ad engagement rate decline
     - Flags ads with 30%+ engagement drop for replacement
     - Alerts if any campaign has fewer than 4 active ads

4. **Expand to multiple thought leaders:**
   - Identify 1-2 additional thought leaders (head of product, lead engineer, customer success lead)
   - Grant TLA permissions for each
   - Create separate campaign groups per thought leader
   - Run the same batch production + selection pipeline for each

### 2. Expand and Optimize Audiences

Using `paid-social-audience-builder` (already deployed at Baseline) plus new segments:

1. **Create thought-leader-specific audiences:**
   - The CTO's posts may resonate with engineering leaders
   - The CEO's posts may resonate with executives and founders
   - Match thought leader to audience segment for higher relevance

2. **Add new audience types:**
   - LinkedIn Company List targeting: upload your target account list (from Attio) and target decision-makers at those companies
   - Lookalike audiences: if you have 300+ TLA-sourced leads in LinkedIn, create a matched audience and build a lookalike
   - Event-based retargeting: people who engaged with previous TLAs (liked, commented, clicked) but did not convert

3. **Implement audience rotation:**
   - Week 1-2: Core ICP + Retargeting
   - Week 3-4: Adjacent ICP + Lookalike
   - Week 5-6: ABM list + Event retargeting
   - Refresh and repeat. Track segment-level performance to inform next rotation.

### 3. Deploy Data-Driven Budget Allocation

Run the `budget-allocation` drill adapted for TLAs:

1. **Weekly budget rebalancing:**
   Build an n8n workflow that runs every Monday:
   - Pull per-segment and per-thought-leader CPA from LinkedIn Marketing API + PostHog
   - Apply the 70/20/10 framework: 70% to proven segments, 20% to optimization experiments, 10% to new audience tests
   - Generate a budget reallocation recommendation
   - Send to Slack for approval

2. **Set automated rebalancing triggers:**
   - If a segment's CPA exceeds 150% of target for 7 days: reduce budget 30%
   - If a segment's CPA is below 75% of target for 7 days: increase budget 20%
   - If a new thought leader's campaign hits target CPA within 14 days: increase from test budget to standard allocation

3. **Cross-thought-leader budget optimization:**
   - Compare CPA across thought leaders
   - Allocate more budget to the thought leader with the best CPA
   - Minimum budget per thought leader: enough for 1,000 impressions/day (maintain learning)

### 4. Build Scalable Tracking Infrastructure

Extend the Baseline tracking to support scale:

1. **PostHog dashboards** (8 panels from Baseline, plus):
   - Per-thought-leader comparison dashboard
   - Content template performance (which templates produce the best TLAs?)
   - Audience saturation tracker (frequency trends by segment)
   - Month-over-month trend lines for all core KPIs

2. **Attio pipeline integration:**
   - Every TLA-sourced lead has full attribution: thought_leader, post_id, audience_segment, content_template
   - Closed-loop reporting: track TLA-sourced deals through to close
   - Monthly ROAS calculation: TLA spend vs pipeline + revenue generated

3. **Automated weekly report:**
   - n8n workflow generates a comprehensive weekly brief covering:
     - Spend, reach, and CPC by thought leader and segment
     - Content velocity: posts published, eligible, promoted, retired
     - Lead volume and quality by segment
     - Budget allocation changes and their impact
   - Post to Slack, store in Attio

### 5. Implement Quality Guardrails

At 10x volume, quality can slip. Set guardrails:

- **Content quality:** If engagement rate for a thought leader drops below 1% for 2 consecutive weeks, pause their content production and diagnose (voice drift, wrong pain points, audience fatigue)
- **Lead quality:** If the percentage of leads scoring 70+ drops below 40%, tighten audience targeting before increasing spend
- **Brand safety:** All posts are reviewed by the thought leader before publishing. The agent generates drafts but never publishes without human approval
- **Frequency cap:** If any audience segment exceeds frequency 5/week, pause that segment's campaigns for 1 week and refresh creative
- **Budget cap:** Total monthly spend never exceeds the approved budget by more than 10%

### 6. Monthly Strategic Review

At the end of each month:

1. Compare actual vs target on all KPIs
2. Identify the single biggest lever for next month (usually: audience expansion, content refresh, or budget shift)
3. Calculate blended CPA across all thought leaders and segments
4. Compare TLA channel performance to other paid channels (Google, Meta, newsletters)
5. Decide: if metrics are stable and repeatable at volume for 3 consecutive months, proceed to Durable

## Time Estimate

- 15 hours: Content scaling setup (playbook, AI production pipeline, multi-thought-leader onboarding)
- 10 hours: Audience expansion and budget allocation automation
- 5 hours: Tracking infrastructure and dashboard builds
- 20 hours: Ongoing management over 3 months (~1.5 hours/week)
- 5 hours: Monthly strategic reviews (3 reviews)
- 5 hours: Guardrail configuration and quality monitoring

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn Ads | TLA campaign management | Ad spend ($5,000-10,000/mo) |
| PostHog | Analytics — dashboards, funnels, attribution | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM — lead and deal management, reporting | $29/user/mo (Plus) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — lead scoring for all TLA leads | $349/mo (Explorer, 100K actions) — [clay.com/pricing](https://www.clay.com/pricing) |
| Loops | Email — nurture sequences at scale | $99/mo (Growth) — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Automation — content pipeline, budget allocation, reporting | $60/mo (Pro, 10K executions) — [n8n.io/pricing](https://n8n.io/pricing) |
| Taplio | LinkedIn analytics and scheduling | $49/mo (Standard) — [taplio.com/pricing](https://taplio.com/pricing) |
| Anthropic API | AI — content generation and scoring | Usage-based, ~$30-60/mo — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** $5,000-10,000/mo ad spend + ~$650-900/mo tools. Total: $5,650-10,900/mo.

## Drills Referenced

- the tla content scaling workflow (see instructions below) — automated content-to-ads pipeline with AI-assisted batch production, multi-thought-leader support, creative rotation, and fatigue detection
- `budget-allocation` — data-driven weekly budget rebalancing across audience segments and thought leaders using the 70/20/10 framework
