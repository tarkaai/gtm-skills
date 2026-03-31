---
name: paid-reddit-ads-scalable
description: >
  Paid Reddit Ads — Scalable Automation. Scale to $3,000-10,000/mo with automated creative testing,
  subreddit expansion, retargeting, and CRM sync for 10x lead volume.
stage: "Marketing > Problem Aware"
motion: "LightweightPaid"
channels: "Paid, Social"
level: "Scalable Automation"
time: "15 hours setup + 60 days runtime"
outcome: "≥ 30 leads or ≥ 16 meetings over 60 days at CPA ≤ $120"
kpis: ["Cost per acquisition", "Return on ad spend (ROAS)", "Lead-to-meeting conversion rate", "Subreddit-level CPA", "Creative win rate"]
slug: "paid-reddit-ads"
install: "npx gtm-skills add marketing/problem-aware/paid-reddit-ads"
drills:
  - ab-test-orchestrator
  - tool-sync-workflow
  - reddit-ads-subreddit-targeting
---

# Paid Reddit Ads — Scalable Automation

> **Stage:** Marketing -> Problem Aware | **Motion:** LightweightPaid | **Channels:** Paid, Social

## Outcomes

Scale Reddit Ads to 10x Baseline volume without proportional effort. A passing Scalable run demonstrates that automated creative testing, subreddit expansion, and CRM integration produce high-volume, high-quality leads at an efficient CPA. You need 30 leads or 16 meetings over 60 days at CPA at or below $120.

## Leading Indicators

- CPA remains within 120% of Baseline CPA during first 2 weeks of scale-up
- At least 2 new subreddit clusters producing leads by day 30
- Creative testing velocity: 3+ new ad variants tested per week via automation
- CRM sync: 100% of Reddit-sourced leads appear in Attio within 1 hour of conversion
- Retargeting pool reaches 1,000+ visitors by day 21

## Instructions

### 1. Automate creative testing

Run the `ab-test-orchestrator` drill to build a systematic creative testing pipeline for Reddit Ads:

Configure an n8n workflow that:
1. Generates new ad variant concepts using Claude (3 variants per week, referencing the `reddit-ads-creative` fundamental for Reddit-native tone rules)
2. Creates the ad variants in Reddit Ads via API
3. Monitors each variant for 500+ impressions
4. Pauses variants with CTR below 0.4%
5. After 1,000 impressions, identifies the winner and archives losers
6. Launches 3 replacement variants the following week

Target: 3-5 new variants per ad group per week. Over 60 days, test 30-60 creative variants total. The winning creative style should become clear by day 30.

**Human action required:** Review the first batch of AI-generated ad copy before enabling fully automated creative deployment.

### 2. Expand subreddit targeting

Re-run the `reddit-ads-subreddit-targeting` drill to find new subreddit clusters:

- Add a 3rd cluster (experimental, 20% budget) targeting adjacent communities
- Test keyword targeting on top of subreddit targeting in a new ad group (keywords matching your problem domain + subreddit intersection)
- Every 2 weeks, evaluate subreddit-level performance. Drop subreddits with CPA > 2x campaign average. Add new candidates from the targeting research.

Build an n8n workflow that pulls subreddit-level performance weekly and flags subreddits for rotation:
- Declining CTR over 3 weeks: flag for creative refresh
- CPA consistently above campaign average: flag for removal
- New high-scoring subreddit from research: flag for addition

### 3. Build tool sync workflows

Run the `tool-sync-workflow` drill to connect:

**Reddit Ads -> Attio (lead routing):**
- n8n workflow: Form submission webhook -> enrich lead via Clay -> create Attio contact with `source: reddit-ads`, `campaign: paid-reddit-ads`, `subreddit_cluster: {cluster}` -> create Attio deal if ICP match score > threshold
- Trigger: real-time on form submission

**Attio -> Reddit Ads (audience exclusion):**
- n8n workflow: Weekly cron -> export Attio contacts where `lifecycle_stage = customer` -> hash emails -> upload to Reddit Ads as custom audience exclusion list
- Prevents wasting ad spend on existing customers

**PostHog -> Reddit Ads (conversion optimization):**
- Ensure CAPI events include all available user match data (hashed email, click ID, IP) so Reddit's algorithm can optimize toward your best-converting audiences

### 4. Scale budget with guardrails

Increase budget to $3,000-10,000/mo. Apply the 70/20/10 framework from the `budget-allocation` drill:

- 70% to proven subreddit clusters (CPA below target)
- 20% to optimization experiments (new targeting, creative angles)
- 10% to new subreddit exploration

Set automated budget guardrails in n8n:
- If daily CPA exceeds 200% of target: auto-reduce daily budget by 30% and alert team
- If daily CPA is below 80% of target: auto-increase daily budget by 20% (up to monthly cap)
- Weekly budget rebalancing across ad groups based on CPA performance

**Human action required:** Approve monthly budget increase. Set the maximum monthly cap.

### 5. Add retargeting layer

Build a Reddit retargeting campaign targeting:
- Landing page visitors who did not convert (from Reddit Pixel data)
- Website visitors who viewed pricing or product pages (cross-channel retargeting)

Retargeting creative should be more direct than prospecting creative:
- Reference their previous visit: "Still researching [problem domain]?"
- Offer a lower-commitment CTA: free tool, case study, or 5-minute demo video
- Allocate 10-15% of total budget to retargeting

### 6. Run for 60 days with continuous optimization

**Weeks 1-2:** Launch scaled campaign. Verify all automations working. Establish new baseline metrics.
**Weeks 3-4:** First creative rotation cycle. First subreddit performance review. Adjust budget allocation.
**Weeks 5-6:** Second rotation cycle. Add keyword targeting experiments. Launch retargeting campaign.
**Weeks 7-8:** Third rotation cycle. Major budget rebalancing based on 6 weeks of data. Final push.

### 7. Evaluate against threshold

Measure against: >= 30 leads or >= 16 meetings over 60 days at CPA <= $120.

Document the Scalable report:

- Total spend, CPA, ROAS
- Volume: leads and meetings by month, week, subreddit cluster
- Creative testing: total variants tested, win rate by hook type, best-performing copy patterns
- Subreddit performance: ranked list of all subreddits tested with CPA and volume
- Automation health: sync latency, error rates, alert frequency
- Full-funnel attribution: ad click -> lead -> qualified -> meeting -> deal (if available)

**PASS:** Reddit Ads are a scalable lead channel. Move to Durable.
**FAIL:** If CPA is too high at scale, Reddit may have a volume ceiling for your audience. Consider capping Reddit budget and diversifying to other channels.

## Time Estimate

- Creative testing automation setup: 4 hours
- Subreddit targeting expansion: 2 hours
- Tool sync workflows (CRM, exclusion, CAPI): 4 hours
- Budget scaling and guardrails: 2 hours
- Retargeting setup: 1 hour
- Weekly optimization (8 sessions at 15 min): 2 hours

**Total active time: ~15 hours. Calendar time: 60 days.**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Reddit Ads | Ad platform | $3,000-10,000/mo ad spend. https://ads.reddit.com |
| PostHog | Analytics, experiments, dashboards | Free up to 1M events, then $0.00031/event. https://posthog.com/pricing |
| n8n | Automation (creative rotation, syncs, monitoring) | Free self-hosted or $20/mo cloud. https://n8n.io/pricing |
| Attio | CRM for lead routing and deal tracking | Free up to 3 users, $29/user/mo Pro. https://attio.com/pricing |
| Clay | Lead enrichment for ICP scoring | From $149/mo. https://clay.com/pricing |
| Anthropic API | AI creative generation | ~$15/mo at this volume. https://www.anthropic.com/pricing |
| Webflow | Landing page hosting | $14-39/mo. https://webflow.com/pricing |

**Estimated monthly cost: $3,200-10,250 (primarily ad spend).**

## Drills Referenced

- `ab-test-orchestrator` — automated creative testing pipeline with statistical rigor
- `tool-sync-workflow` — CRM sync, audience exclusions, and CAPI optimization
- `reddit-ads-subreddit-targeting` — ongoing subreddit research and rotation
