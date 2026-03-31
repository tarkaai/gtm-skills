---
name: twitter-x-ads-scalable
description: >
  Twitter/X Ads — Scalable Automation. Automate X Ads management with always-on
  creative rotation, automated budget rebalancing, and full-funnel attribution
  syncing ad data to PostHog and CRM. Target 10x volume with stable CPL.
stage: "Marketing > Solution Aware"
motion: "Lightweight Paid"
channels: "Paid, Social"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: ">=750,000 impressions and >=65 qualified leads from $8,000/month over 4 months"
kpis: ["Monthly impressions", "Monthly qualified leads", "CPL trend", "Creative refresh rate", "Automation coverage %", "Lead-to-opportunity rate"]
slug: "twitter-x-ads"
install: "npx gtm-skills add marketing/solution-aware/twitter-x-ads"
drills:
  - ab-test-orchestrator
  - tool-sync-workflow
  - twitter-x-ads-performance-monitor
---

# Twitter/X Ads — Scalable Automation

> **Stage:** Marketing > Solution Aware | **Motion:** Lightweight Paid | **Channels:** Paid, Social

## Outcomes

Automate the X Ads campaign to run at 10x Baseline volume without proportional manual effort. Build n8n workflows that handle creative rotation, budget rebalancing, and performance monitoring. Sync all ad data to PostHog and Attio for full-funnel attribution. Target: >=750,000 impressions and >=65 qualified leads per month at $8,000/month ad spend.

## Leading Indicators

- Automation workflows running without manual intervention for 2+ consecutive weeks
- Creative refresh cycle executing on schedule (new variants every 2 weeks)
- CPL staying within 20% of Baseline benchmark as budget scales
- Full-funnel data flowing: X Ads stats visible in PostHog dashboards and leads attributed in Attio
- At least 5 active creative variants at all times (no single ad running more than 4 weeks)

## Instructions

### 1. Build systematic creative testing

Run the `ab-test-orchestrator` drill to automate creative testing on X:
- **Test structure**: Always run 5-8 promoted tweet variants per ad group
- **Decision rules**: After 500 impressions, pause variants with CTR below 0.3%. After 2,000 impressions, declare winner and create 3 new variants inspired by the winning hook.
- **Creative pipeline**: Produce a batch of 10-15 new variants every 2 weeks. Use Claude to generate variants based on winning patterns: "The top-performing ad used a [data hook] about [topic] with [CTA]. Generate 10 new variants that use the same hook type but different data points and angles."
- **Format testing**: Systematically test text-only vs. Website Cards vs. Video Cards across all ad groups. Track format performance as a dimension in PostHog.
- **Fatigue prevention**: No single promoted tweet runs more than 4 weeks. The n8n workflow automatically pauses any variant older than 28 days.

### 2. Connect full-funnel data sync

Run the `tool-sync-workflow` drill to build bidirectional data pipelines:

**X Ads -> PostHog** (daily):
- Pull campaign, ad group, and promoted tweet stats via X Ads API
- Send as PostHog custom events with full attribution (campaign_id, ad_group_id, variant_id)
- Enables PostHog dashboards that show ad spend alongside on-site conversion data

**PostHog -> X Ads** (weekly):
- Export converter profiles from PostHog (users who submitted forms)
- Upload to X as a custom audience for exclusion (don't re-target converters)
- Build lookalike audiences from converters for prospecting

**X Ads -> Attio** (real-time via n8n):
- When a new lead submits the landing page form, n8n creates the Attio contact with source attribution: `utm_source=twitter`, `utm_medium=paid`, `campaign_id`, `variant_id`
- As leads progress through the pipeline, Attio deal data feeds back into ROAS calculations

### 3. Deploy always-on performance monitoring

Run the `twitter-x-ads-performance-monitor` drill to set up:
- **Daily monitoring**: n8n workflow checks all KPIs against thresholds
- **Creative fatigue detection**: Flags variants with declining CTR
- **Audience exhaustion detection**: Flags ad groups with rising frequency or declining impressions
- **Budget guardrails**: Auto-pauses campaigns if daily spend exceeds 120% of target
- **Automated alerts**: Slack notifications for any metric deviating >30% from 14-day average

### 4. Scale budget with automated rebalancing

Build an n8n workflow that runs weekly:
1. Pull CPL and conversion data per ad group
2. Calculate budget efficiency: which ad groups deliver the lowest CPL?
3. Shift 10-20% of budget from highest-CPL to lowest-CPL ad groups
4. If overall CPL is below target: increase total daily budget by 10%
5. If overall CPL is above target: decrease budget by 10% and investigate
6. Log all budget changes in Attio with reasoning

**Guardrail**: Monthly spend never exceeds $8,000 without human approval. If the automation recommends exceeding this, it requests approval via Slack instead of auto-executing.

### 5. Evaluate against threshold

After 4 months of continuous operation, measure:
- **Monthly impressions >= 750,000**: Is the campaign delivering at scale?
- **Monthly qualified leads >= 65**: Is CPL stable as volume increased?
- **Automation coverage**: What % of campaign management is automated vs. manual?

Decision tree:
- **PASS**: X Ads are running autonomously with stable metrics. Proceed to Durable for self-optimization.
- **PARTIAL**: Volume met but CPL is trending up. Investigate: is it audience exhaustion, creative fatigue, or competitive pressure? Fix before proceeding.
- **FAIL**: Automation is breaking or CPL is unsustainable. Simplify the automation, reduce budget, and stabilize before re-attempting scale.

## Time Estimate

- 15 hours: Initial automation build (creative pipeline, data sync, monitoring)
- 5 hours/month: Creative production (10-15 variants every 2 weeks)
- 3 hours/month: Performance review and strategy adjustments
- 2 hours/month: Automation maintenance and debugging

**Total: ~75 hours over 4 months (15 setup + 15/month ongoing)**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| X Ads | Promoted tweets at scale | $8,000/mo ad spend |
| PostHog | Full-funnel dashboards and attribution | Free tier or $0.00045/event |
| n8n | Automation workflows (creative rotation, budget rebalancing, monitoring) | Free self-hosted or $20/mo cloud |
| Anthropic API | Creative variant generation | ~$10-20/mo at this volume |
| Webflow | Landing page hosting | ~$15-40/mo |

## Drills Referenced

- `ab-test-orchestrator` — Automates creative testing: variant production, performance-based pausing, winner detection, and refresh cycles
- `tool-sync-workflow` — Builds bidirectional data pipelines between X Ads, PostHog, and Attio for full-funnel attribution
- `twitter-x-ads-performance-monitor` — Always-on daily monitoring with fatigue detection, exhaustion alerts, budget guardrails, and optimization recommendations
