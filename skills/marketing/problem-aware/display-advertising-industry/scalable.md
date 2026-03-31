---
name: display-advertising-industry-scalable
description: >
  Display Advertising — Scalable. Automated creative production pipeline, systematic A/B testing,
  cross-platform budget optimization, expanded placement coverage, and integrated performance
  dashboards. Target 5-10x Baseline lead volume without proportional time investment.
stage: "Marketing > ProblemAware"
motion: "LightweightPaid"
channels: "Paid"
level: "Scalable"
time: "75 hours over 3 months"
outcome: ">=1,000,000 impressions and >=60 qualified leads/month from $5,000-10,000/month budget, with cost per qualified lead below $120 and creative pipeline producing 10+ new variants per month"
kpis: ["Monthly impressions", "Monthly qualified leads", "Cost per qualified lead", "Creative pipeline velocity", "Placement quality distribution", "Cross-platform CPA comparison", "Automation efficiency"]
slug: "display-advertising-industry"
install: "npx gtm-skills add Marketing/ProblemAware/display-advertising-industry"
drills:
  - display-creative-scaling
  - budget-allocation
---

# Display Advertising — Scalable

> **Stage:** Marketing > ProblemAware | **Motion:** LightweightPaid | **Channels:** Paid

## Outcomes

Find the 10x multiplier. The creative-to-ads pipeline is automated: the agent generates display ad variants using AI, systematically tests them, detects fatigue, and rotates creatives without manual intervention. Placement coverage expands from 20-25 sites to 50+ via topic targeting and custom intent audiences working alongside managed placements. Budget allocation across platforms, campaigns, and audience segments is data-driven and rebalanced weekly. The system produces 60+ qualified leads per month without proportional increase in human time.

**Pass threshold:** >=1,000,000 impressions and >=60 qualified leads/month from $5,000-10,000/month budget, with cost per qualified lead below $120, sustained for 3 months.

## Leading Indicators

- Creative pipeline produces 10+ new display ad variants per month via AI generation
- Automated fatigue detection catches declining creatives within 48 hours
- No creative runs more than 4 weeks without refresh
- Placement portfolio expands beyond managed placements into validated custom intent and topic audiences
- Budget reallocation happens weekly based on CPA data across segments
- Cost per qualified lead is trending down or stable month over month
- Cross-platform reporting shows clear ROI by campaign type, placement, and audience
- At least 3 audience types (managed placements, custom intent, retargeting, lookalike) produce qualified leads

## Instructions

### 1. Scale Creative Production

Run the `display-creative-scaling` drill:

1. **Analyze winning patterns from Baseline:**
   - Query PostHog for per-creative performance: CTR, conversion rate, CPA
   - Segment by: hook type (stat/question/proof), pain point, image style (text overlay/product screenshot/illustration), CTA type
   - Document the top 3 performing combinations as the creative playbook

2. **Deploy AI-assisted batch creative production:**
   - Build an n8n workflow using the Anthropic API that generates 10+ display ad variants bi-weekly
   - Each batch covers multiple pain points and hook types based on the creative playbook
   - Agent generates: headlines, descriptions, long headlines, image concepts
   - Human reviews and approves copy (15 min per batch)
   - Images produced from approved concepts using brand templates in Canva/Figma

3. **Expand pain point coverage from 3 to 5-7:**
   - Mine GDN search query reports and placement reports for new pain-point language
   - Analyze PostHog scroll depth data on landing pages to identify which sections resonate most
   - For each new pain point: generate 5 creative variants, create a new ad group, allocate 10% of budget as a test

4. **Automate creative fatigue detection:**
   - Build a daily n8n workflow that checks CTR decay per creative_id
   - Flag creatives where CTR declined 30%+ from first-week baseline
   - Auto-pause fatigued creatives and replace with the next variant from the staging queue
   - Alert if creative pipeline drops below 5 ready-to-deploy variants

5. **Cross-platform creative sync:**
   - When a creative wins on GDN, adapt and deploy on Meta Audience Network within 48 hours
   - Track a `creative_concept_id` across platforms so you can compare the same message on different networks
   - GDN format: responsive display ad (multiple headlines/descriptions, Google mixes and matches)
   - Meta format: single image with bold text overlay (more visual, shorter copy)

### 2. Expand Placement and Audience Strategy

Using validated Baseline data, expand reach:

1. **Graduate from managed placements to managed + automated:**
   - Keep the top 20 managed placements from Baseline (proven performers)
   - Add topic targeting campaigns for the top 3 content categories where managed placements performed well
   - Add affinity audience campaigns targeting users interested in your problem space
   - Monitor placement reports weekly; promote high-quality auto-discovered sites to the managed placement list

2. **Build new audience segments:**
   - **Custom intent (expanded):** Add keyword themes from Baseline search query data and landing page engagement data
   - **In-market audiences:** Target Google's in-market segments for relevant B2B categories
   - **Similar audiences:** Build similar audiences from your conversion pixel data
   - **Cross-platform retargeting:** Retarget GDN clickers on Meta and vice versa using `cross-platform-retargeting-sync`

3. **Implement audience rotation:**
   - Week 1-2: Managed placements + GDN retargeting + Meta retargeting
   - Week 3-4: Custom intent + Meta lookalike
   - Week 5-6: Topic targeting + in-market + Meta interest
   - After 6 weeks: retire exhausted audiences, build new ones from conversion data

### 3. Deploy Data-Driven Budget Allocation

Run the `budget-allocation` drill adapted for display:

1. **Weekly budget rebalancing:**
   Build an n8n workflow that runs every Monday:
   - Pull per-campaign, per-audience, per-platform CPA from PostHog
   - Apply the 70/20/10 framework: 70% to proven campaigns, 20% to optimization experiments, 10% to new audience tests
   - Generate a budget reallocation recommendation
   - Send to Slack for approval

2. **Set automated rebalancing triggers:**
   - If a campaign's CPA exceeds 150% of target for 7 days: reduce budget 30%
   - If a campaign's CPA is below 75% of target for 7 days: increase budget 20%
   - If a new audience test hits target CPA within 14 days: promote to optimization bucket
   - If GDN CPA is 30%+ lower than Meta for comparable audiences: shift allocation toward GDN

3. **Cross-platform budget optimization:**
   - Compare CPA by platform monthly
   - Allocate more budget to the platform with the best quality-adjusted CPA (not just cheapest clicks -- quality matters)
   - Minimum allocation per platform: enough to maintain learning (at least $500/mo per platform)

### 4. Build Scalable Tracking Infrastructure

Extend Baseline tracking to support 10x volume:

1. **PostHog dashboards (expand from Baseline):**
   - Placement quality matrix: per-domain CPA and lead quality
   - Creative performance heatmap: which combinations of hook type x pain point x image style work best
   - Audience segment comparison: CPA and lead quality by audience type across platforms
   - Month-over-month trend lines for all core KPIs
   - Creative pipeline health: variants in queue, average creative age, fatigue rate

2. **Attio pipeline integration:**
   - Every display lead has full attribution: platform, campaign_type, placement_domain, pain_point, creative_concept, audience_segment
   - Closed-loop reporting: track display-sourced deals through to close
   - Monthly ROAS calculation: display spend vs. pipeline + revenue generated

3. **Automated weekly report:**
   Build an n8n workflow that generates a comprehensive weekly brief:
   - Spend, reach, and CPA by platform, campaign type, and audience
   - Creative velocity: variants generated, deployed, paused, in queue
   - Placement health: new sites discovered, sites excluded, top performers
   - Lead volume and quality by segment
   - Budget allocation changes and their impact
   - Post to Slack, store in Attio

### 5. Implement Quality Guardrails

At 10x volume, quality risks increase:

- **Placement quality:** Review the GDN placement report weekly. Exclude any domain that produces 500+ impressions with zero conversions or CTR below 0.03%. Build a blocklist of low-quality sites.
- **Lead quality:** If the percentage of leads scoring 70+ drops below 40%, tighten audience targeting before increasing spend. Investigate which campaign types produce the lowest quality leads.
- **Creative quality:** All AI-generated copy is reviewed before deployment. The agent generates, the human approves.
- **Frequency cap enforcement:** If any audience segment exceeds frequency 5/week on GDN or 3/week on Meta, pause that segment and refresh creative.
- **Budget cap:** Total monthly spend never exceeds the approved budget by more than 10%. n8n workflow checks daily spend and pauses campaigns if budget pacing exceeds 110%.
- **Brand safety:** Maintain and update the placement exclusion list. Block entire categories (gambling, adult content, controversial news).

### 6. Monthly Strategic Review

At the end of each month:

1. Compare actual vs. target on all KPIs
2. Identify the single biggest lever for next month: placement expansion, creative refresh, audience testing, or budget shift
3. Calculate blended CPA across all platforms and campaign types
4. Compare display channel performance to other paid channels (search, social, newsletter sponsorships)
5. Review the creative playbook: update winning patterns based on the latest month's data
6. Decide: if metrics are stable and repeatable at volume for 3 consecutive months, proceed to Durable

## Time Estimate

- 15 hours: Creative scaling setup (AI pipeline, fatigue detection, cross-platform sync)
- 10 hours: Audience expansion and budget allocation automation
- 10 hours: Tracking infrastructure, dashboards, and reporting workflows
- 30 hours: Ongoing management over 3 months (~2.5 hours/week)
- 5 hours: Monthly strategic reviews (3 reviews)
- 5 hours: Guardrail configuration and quality monitoring

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Google Ads (GDN) | Display campaigns — managed placements, custom intent, topic targeting | Ad spend ($3,000-6,000/mo) |
| Meta Ads (Audience Network) | Display campaigns — retargeting, lookalike, interest | Ad spend ($2,000-4,000/mo) |
| PostHog | Analytics — dashboards, funnels, experiments, attribution | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM — lead and deal management, reporting | $29/user/mo (Plus) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — lead scoring for all display leads | $349/mo (Explorer) — [clay.com/pricing](https://www.clay.com/pricing) |
| Loops | Email — nurture sequences at scale | $99/mo (Growth) — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Automation — creative pipeline, budget allocation, reporting | $60/mo (Pro, 10K executions) — [n8n.io/pricing](https://n8n.io/pricing) |
| Anthropic API | AI — creative generation and scoring | Usage-based, ~$30-60/mo — [anthropic.com/pricing](https://www.anthropic.com/pricing) |
| Webflow | Landing pages | $29/mo (CMS) — [webflow.com/pricing](https://webflow.com/pricing) |

**Estimated play-specific cost this level:** $5,000-10,000/mo ad spend + ~$600-900/mo tools. Total: $5,600-10,900/mo.

## Drills Referenced

- `display-creative-scaling` — automated creative production pipeline with AI generation, systematic A/B testing, fatigue detection, pain point expansion, and cross-platform creative sync
- `budget-allocation` — data-driven weekly budget rebalancing across platforms, campaigns, and audience segments using the 70/20/10 framework
