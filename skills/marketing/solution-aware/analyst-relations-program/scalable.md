---
name: analyst-relations-program-scalable
description: >
  Analyst Relations Program — Scalable. Automate analyst monitoring, nurture cadences, and
  report tracking via n8n. Scale to 25+ analyst relationships, track analyst-influenced
  pipeline systematically, and hit 30+ influenced deals over 6 months.
stage: "Marketing > SolutionAware"
motion: "PREarnedMentions"
channels: "Other"
level: "Scalable"
time: "75 hours over 6 months"
outcome: ">=20 analyst interactions, >=5 report mentions or inclusions, and >=30 analyst-influenced deals over 6 months"
kpis: ["Analyst interactions/quarter", "Report mentions", "Analyst-influenced pipeline value", "Relationship score improvement", "Briefing-to-mention conversion rate", "Nurture email engagement rate"]
slug: "analyst-relations-program"
install: "npx gtm-skills add marketing/solution-aware/analyst-relations-program"
drills:
  - analyst-target-research
  - analyst-relationship-nurture
  - dashboard-builder
  - briefing-deck-preparation
---

# Analyst Relations Program — Scalable

> **Stage:** Marketing > SolutionAware | **Motion:** PartnershipsWarmIntros | **Channels:** Other

## Outcomes

Scale analyst relations from reactive briefing requests to a proactive, monitored program. Nurture cadences run automatically. Analyst publication monitoring detects when your category is being researched. Analyst-influenced pipeline is tracked systematically. The program expands to 25+ analysts across all four tiers.

**Pass threshold:** >=20 analyst interactions, >=5 report mentions or inclusions, and >=30 analyst-influenced deals over 6 months.

## Leading Indicators

- 25+ analysts tracked in Attio with regular engagement
- Quarterly nurture emails achieve >50% open rate and >10% reply rate
- At least 2 analysts proactively reach out to you (for briefings, data requests, or client referrals)
- Report inclusion pipeline has 3+ active opportunities at any time
- Analyst-influenced deals represent >10% of total pipeline value
- Relationship scores are improving: 10+ analysts at score >= 3

## Instructions

### 1. Scale the Analyst Portfolio

Run the `analyst-target-research` drill at Scalable volume (25+ analysts):

1. Expand to all four tiers comprehensively: every analyst who covers or could influence your category
2. Add G2 reviewers and Capterra category leaders as a fifth influencer category (peer review platforms that solution-aware buyers consult)
3. Run quarterly refresh cycles: re-score all analysts, add new ones, remove those who changed coverage areas
4. Use Clay automation for enrichment refreshes: detect job changes, coverage area shifts, new publications
5. Maintain the Attio list "Analyst Briefing Targets" with current scores and relationship statuses

### 2. Deploy Automated Nurture at Scale

Run the `analyst-relationship-nurture` drill with full automation:

1. **Quarterly update automation:** n8n workflow sends personalized updates to all "Briefed" analysts every quarter. Claude API generates each email referencing the analyst's specific coverage area and recent publications.
2. **Milestone notifications:** When a major event occurs (logged in PostHog), n8n auto-drafts notes for all relevant analysts and routes to Slack for approval.
3. **Content sharing pipeline:** When the company publishes substantive content (research reports, data analyses, product launches), n8n identifies which analysts cover that topic and queues personalized share emails.
4. **Re-briefing triggers:** When an analyst has not engaged in 2 quarters, auto-generate a re-briefing pitch with new data.
5. **Relationship health dashboard:** Attio list view showing: Healthy (engaged this quarter), Cooling (1-2 quarters silence), Cold (3+ quarters), Active (in conversation).

### 3. Deploy Analyst Monitoring

Run the `dashboard-builder` drill:

1. Build the PostHog analyst relations dashboard:
   - Briefing pipeline: requests sent, scheduled, completed, outcomes
   - Report tracking: publications where you are mentioned, pending inclusions
   - Pipeline influence: analyst-influenced deals by stage, total value
   - Relationship health: analysts by relationship score tier
2. Implement the analyst event taxonomy in PostHog:
   - `analyst_briefing_requested`, `analyst_briefing_completed`
   - `analyst_mention_detected`, `analyst_report_published`
   - `analyst_referral_received`, `deal_analyst_influenced`
   - `analyst_update_sent`, `analyst_update_opened`
3. Configure anomaly detection:
   - Briefing acceptance rate drops >30% -> trigger investigation
   - Zero report mentions in 3 months -> trigger review
   - Analyst-influenced deals drop >50% -> trigger sales process audit
4. Weekly automated reports via n8n

### 4. Track Report Cycles Proactively

Build a report calendar in Attio:

1. For each major analyst firm, track their publication cycles: when Magic Quadrants, Waves, MarketScapes refresh
2. Set reminders 6 months before expected refresh dates: initiate re-briefing with updated data
3. For each active report inclusion opportunity, maintain a checklist: submission package sent, customer references provided, follow-up calls scheduled
4. When a report publishes: log the result (included/not included, positioning, rating), share internally, amplify on social media, update your website

### 5. Systematize Sales Integration

Ensure analyst influence is captured in every deal:

1. Add "Analyst Research Consulted" as a required field in Attio deal records
2. In the sales process: discovery call template includes the question "What research or reports have you reviewed while evaluating solutions like ours?"
3. Build an n8n workflow: when a deal with the "Analyst Influenced" tag closes, attribute it to the specific analyst and report
4. Quarterly report to leadership: analyst-influenced pipeline value, influenced win rate vs non-influenced, ROI of analyst program

### 6. Monthly Optimization

Monthly review cycle:

1. Pull weekly reports from the `dashboard-builder` drill
2. Analyze:
   - Which analyst tiers produce the most pipeline influence?
   - Which nurture tactics generate the most engagement (quarterly updates, content shares, milestone notes)?
   - Which report types (Magic Quadrant, Wave, market guide, blog mention) produce the most prospect awareness?
3. Adjust:
   - Increase effort on high-influence analyst tiers
   - Refresh briefing materials with new customer data and metrics
   - Target upcoming report cycles with proactive outreach
   - Add new analysts identified from prospect feedback (who else are buyers consulting?)

## Time Estimate

- 4 hours: Quarterly analyst list expansion and refresh (x2 = 8 hours)
- 3 hours/quarter: Briefing outreach and preparation (x2 = 6 hours)
- 10 hours: Conducting briefings over 6 months (20+ interactions at ~30 min each)
- 6 hours: Analyst nurture automation setup and maintenance
- 6 hours: Analyst monitoring setup (dashboard, events, anomaly detection)
- 12 hours: Report inclusion tracking and submission preparation
- 12 hours: Sales integration, pipeline tracking, and reporting
- 15 hours: Monthly optimization reviews (2.5 hours/month x 6 months)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — analyst contacts, relationship tracking, pipeline attribution | $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — analyst research, quarterly refreshes | $149/mo (Starter) — [clay.com/pricing](https://www.clay.com/pricing) |
| Loops | Email — quarterly nurture sequences | $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| Cal.com | Scheduling — briefing booking | Free plan — [cal.com/pricing](https://cal.com/pricing) |
| n8n | Automation — nurture cadences, monitoring, reporting | $60/mo (Pro) — [n8n.io/pricing](https://n8n.io/pricing) |
| PostHog | Analytics — analyst dashboards, pipeline attribution | Free up to 1M events — [posthog.com/pricing](https://posthog.com/pricing) |
| Claude API | Briefing docs, nurture emails, report analysis | ~$30-50/mo — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** Loops ~$49/mo for analyst nurture. Other tools are standard stack.

## Drills Referenced

- `analyst-target-research` — quarterly analyst list refresh with 25+ analysts, Clay enrichment, and scoring
- `analyst-relationship-nurture` — automated quarterly updates, milestone notifications, content sharing, and re-briefing triggers
- `dashboard-builder` — continuous monitoring of briefing pipeline, report mentions, pipeline influence, and relationship health
- `briefing-deck-preparation` — tailored briefing materials for each analyst, updated with latest metrics
