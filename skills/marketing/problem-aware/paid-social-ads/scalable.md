---
name: paid-social-ads-scalable
description: >
  Paid Social Ads — Scalable Automation. Scale to $3,000-10,000/mo with automated creative
  testing, cross-platform audience sync, and n8n-driven campaign management. Hit ≥ 30 leads
  or ≥ 16 meetings over 2 months without proportional increase in manual effort.
stage: "Marketing > Problem Aware"
motion: "Lightweight Paid"
channels: "Paid"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥ 30 leads or ≥ 16 meetings over 2 months"
kpis: ["Cost per lead (CPL)", "Cost per meeting", "Lead-to-meeting conversion rate", "Blended ROAS across platforms", "Creative refresh rate (new variants per 2-week cycle)", "Audience saturation rate"]
slug: "paid-social-ads"
install: "npx gtm-skills add marketing/problem-aware/paid-social-ads"
drills:
  - ab-test-orchestrator
  - paid-social-audience-builder
  - tool-sync-workflow
  - budget-allocation
  - threshold-engine
---

# Paid Social Ads — Scalable Automation

> **Stage:** Marketing → Problem Aware | **Motion:** Lightweight Paid | **Channels:** Paid

## Outcomes

Generate at least 30 leads or 16 meetings over 2 months with $3,000-10,000/mo spend. The 10x multiplier at this level comes from three things: (1) systematic creative testing that finds winners faster, (2) cross-platform audience sync that feeds conversion data back into targeting, and (3) automated campaign management that adjusts budgets and pauses underperformers without human intervention.

At Scalable, the agent manages campaigns weekly. A human approves major changes (new audiences, budget increases above 30%) but does not need to log into ad platforms daily.

## Leading Indicators

- New creative variants launched every 2 weeks (pipeline is not stalling)
- Winner variant CTR is at least 1.5x the average (testing is finding real winners, not noise)
- CPL stays within 20% of Baseline CPL despite higher spend (scale is not degrading quality)
- Retargeting conversion rate stays 2x+ higher than cold traffic (retargeting pool is healthy)
- CRM pipeline from paid social grows month-over-month (leads are converting downstream)
- Audience overlap between segments stays below 30% (you are reaching new people, not the same ones)

## Instructions

### 1. Run on both LinkedIn and Meta simultaneously

If you only ran one platform in Baseline, add the second now. The goal is to reach your ICP through both channels:
- LinkedIn: primary for cold targeting (firmographic precision)
- Meta: primary for retargeting and lookalikes (lower CPM, broader reach)

Run the `paid-social-audience-builder` drill to build all 6 audience types: 3 LinkedIn segments (Core ICP, Adjacent ICP, Title-based) and 3 Meta audiences (Custom/retargeting, 1% Lookalike, Interest-based).

### 2. Set up systematic A/B testing

Run the `ab-test-orchestrator` drill configured for paid social:

**What to test (in priority order):**
1. Pain points: Which of your 3 ICP pain points generates the lowest CPL?
2. Hook types: Do stat hooks, question hooks, or proof hooks perform better?
3. Offer formats: Does a guide, checklist, calculator, case study, or webinar registration convert better?
4. Ad formats: Lead gen forms vs. landing page — which produces higher quality leads?
5. Creative formats: Single image vs. carousel vs. video (Meta only)

**Testing framework:**
- Run each test for 7 days minimum or until each variant has 500+ impressions
- Primary metric: Cost per lead (CPL)
- Secondary metric: Lead-to-meeting conversion rate (check 14 days after lead capture)
- Use PostHog experiments to track which variant each lead came from and measure downstream conversion

**Automation:**
Build an n8n workflow that runs daily:
1. Pull campaign performance from LinkedIn Marketing API and Meta Insights API
2. For each active variant, check: impressions >= 500 AND CTR < 0.3% (LinkedIn) or < 0.8% (Meta)
3. If both conditions are true, pause the variant via the platform API
4. Send a summary to Slack: "Paused variant X (CTR 0.15% after 847 impressions). Top performer is variant Y (CTR 0.62%, CPL $43)."

### 3. Build cross-platform audience sync

Run the `tool-sync-workflow` drill to connect your platforms:

**CRM-to-ad-platform sync (weekly via n8n):**
- Export closed-won customers from Attio -> upload as exclusion audience to LinkedIn and Meta (never target existing customers)
- Export churned customers from Attio -> create a "winback" audience on Meta for separate campaigns (optional)
- Export qualified leads from Attio -> create a LinkedIn Matched Audience for lookalike targeting

**Ad-platform-to-CRM sync (real-time via n8n):**
- When a lead converts from a specific campaign, tag the Attio contact with `campaign_id`, `platform`, `variant_id`
- When a deal closes, attribute revenue back to the ad campaign by looking up the contact's first paid_social event in PostHog

**PostHog-to-ad-platform sync (weekly via n8n):**
- Export PostHog cohort "website visitors who viewed 3+ pages" -> upload as retargeting audience to Meta
- Export PostHog cohort "trial users who activated" -> upload as source for lookalike on Meta

### 4. Scale budget with automated guardrails

Run the `budget-allocation` drill with scalable-specific rules:

**Budget scaling protocol:**
- If blended CPL is below target for 2 consecutive weeks, increase total budget by 20%
- If blended CPL exceeds target by 20% for 1 week, freeze budget and diagnose
- If any single campaign's CPL exceeds 2x target for 5 days, reduce that campaign's budget by 30%
- Maximum single budget increase: 30% per month

**Automate via n8n:**
Build a workflow that runs every Monday:
1. Pull last 7 days of spend and lead data from both platforms
2. Calculate blended CPL and per-campaign CPL
3. Compare against target CPL
4. If scaling conditions are met, adjust daily budgets via the LinkedIn and Meta APIs
5. Log the adjustment in PostHog: `paid_social_budget_adjusted`, with properties `direction` (up/down), `amount`, `reason`

**Human action required:** Set a maximum monthly budget cap that the automation cannot exceed. Review and approve any budget increase above $5,000/mo.

### 5. Produce creative at scale

Run the the paid social creative pipeline workflow (see instructions below) drill on a 2-week cadence:
- Every 2 weeks: generate 5-8 new variants using Claude/Anthropic API
- Use winning patterns from A/B tests: if stat hooks outperform question hooks, create more stat hooks but with new data points
- Test at least one entirely new angle each cycle (different pain point, different persona, different offer format) to prevent creative tunnel vision
- Archive every variant's performance data: variant_id, pain_point, hook_type, impressions, CTR, CPL, lead_quality_score

Over 2 months, you should produce and test 20-30 unique ad variants. Your top 3-5 performers will drive the majority of leads.

### 6. Evaluate against threshold

Run the `threshold-engine` drill at months 1 and 2.

**Month 1 checkpoint:** ≥ 12 leads or ≥ 6 meetings. If behind pace, diagnose and adjust before month 2.

**Month 2 final:** ≥ 30 leads or ≥ 16 meetings over the full 2-month period.

Also evaluate operational metrics:
- Is creative production keeping pace? (new variants every 2 weeks)
- Is lead routing still working? (check for failures in n8n workflows)
- Is audience fatigue setting in? (check frequency metrics — if average frequency > 4, audiences need refresh)
- Are leads converting downstream? (check meeting rate and pipeline value)

Decision:
- **PASS:** 30+ leads or 16+ meetings, CPL within target, automation running smoothly. Proceed to Durable.
- **MARGINAL:** 20-29 leads or 10-15 meetings. Extend Scalable by 1 month. Focus on the weakest area (creative, audience, or budget).
- **FAIL:** <20 leads or <10 meetings despite $3,000+/mo spend. Re-evaluate whether paid social is the right motion for your ICP. Consider pivoting to a different play (organic content, cold outreach, community).

## Time Estimate

- 8 hours: Cross-platform setup and audience sync (one-time)
- 6 hours: A/B test framework and n8n automation for campaign management (one-time)
- 4 hours: Initial creative batch production (5-8 variants per platform)
- 4 hours bi-weekly: Creative refresh (produce + launch new variants)
- 2 hours weekly: Performance review and budget adjustments
- 4 hours: Month 1 checkpoint analysis
- 4 hours: Month 2 final evaluation and documentation

Total: ~60 hours over 2 months (front-loaded in first 2 weeks, then ~5 hrs/week ongoing)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn Ads | B2B targeting and lead gen | $3,000-10,000/mo ad spend. [Pricing](https://business.linkedin.com/marketing-solutions/ads/pricing) |
| Meta Ads | Retargeting, lookalikes, broad reach | Included in above budget. [Pricing](https://www.facebook.com/business/ads/pricing) |
| Clay | Lead enrichment and ICP scoring | $185/mo Launch or $495/mo Growth (for CRM sync). [Pricing](https://clay.com/pricing) |
| Loops | Nurture sequences | Free up to 1,000 contacts, then $49/mo. [Pricing](https://loops.so/pricing) |
| PostHog | Experiments, funnels, event tracking | Free up to 1M events/mo. [Pricing](https://posthog.com/pricing) |
| n8n | Campaign automation, lead routing, budget management | Free self-hosted or $20/mo cloud. [Pricing](https://n8n.io/pricing) |
| Webflow | Landing pages | $14-23/mo (CMS plan if testing multiple pages). [Pricing](https://webflow.com/pricing) |

**Estimated scalable monthly cost:** $3,000-10,000 ad spend + ~$450-750 tooling = $3,450-10,750/mo

## Drills Referenced

- `ab-test-orchestrator` — systematic creative and audience testing with statistical rigor
- the paid social creative pipeline workflow (see instructions below) — bi-weekly creative production at scale (20-30 variants over 2 months)
- `paid-social-audience-builder` — build all 6 audience segments across LinkedIn and Meta
- `tool-sync-workflow` — sync CRM, PostHog, and ad platforms bidirectionally via n8n
- `budget-allocation` — automated budget scaling with guardrails and per-campaign CPL triggers
- `threshold-engine` — evaluate at month 1 checkpoint and month 2 final
