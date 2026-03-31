---
name: retargeting-campaigns-multi-platform-scalable
description: >
  Multi-platform Retargeting — Scalable Automation. Automate creative rotation,
  audience refresh, budget reallocation, and cross-platform data sync via n8n.
  Scale spend 5-10x while maintaining or improving CPA through systematic A/B testing.
stage: "Marketing > Product Aware"
motion: "Lightweight Paid"
channels: "Paid"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: ">=2% blended CTR and >=70 conversions/month from $5,000-8,000/mo retargeting spend with automated creative rotation and budget reallocation"
kpis: ["Monthly conversions", "Blended CPA", "Creative win rate", "Audience refresh cadence", "Automation coverage ratio"]
slug: "retargeting-campaigns-multi-platform"
install: "npx gtm-skills add marketing/product-aware/retargeting-campaigns-multi-platform"
drills:
  - ab-test-orchestrator
  - tool-sync-workflow
---

# Multi-platform Retargeting — Scalable Automation

> **Stage:** Marketing → Product Aware | **Motion:** Lightweight Paid | **Channels:** Paid

## Outcomes

Scale retargeting spend 5-10x from Baseline while maintaining or improving CPA through automation. Target: >=70 conversions/month from $5,000-8,000/month spend across 2-3 platforms with >=2% blended CTR. At this level, creative rotation, audience refresh, budget reallocation, and cross-platform sync are handled by n8n workflows — not manual effort.

## Leading Indicators

- n8n creative rotation workflow fires on schedule and successfully pauses/launches ads (verify in workflow execution logs)
- New ad variants are launched every 2 weeks without manual intervention
- Cross-platform exclusion list sync runs daily without errors
- Budget reallocation triggers fire correctly when CPA thresholds are breached
- Monthly conversion volume increases 3x+ from Baseline without proportional CPA increase
- No creative runs longer than 4 weeks without replacement (fatigue prevention)
- Lead quality rate remains >= 50% (retargeting conversions that become qualified leads)

## Instructions

### 1. Automate creative production and rotation

Run the the paid social creative pipeline workflow (see instructions below) drill adapted for retargeting creative:

1. Build a creative production workflow in n8n:
   - Every 2 weeks, trigger a Claude API call via `hypothesis-generation` to generate 5 new retargeting ad variants per platform
   - Input to Claude: current top-performing ad copy, audience segment, product value propositions, and recent customer proof points
   - Claude outputs: 5 headline + body + CTA combinations, each with a different hook type (direct CTA, social proof, urgency, benefit, question)
   - Store generated variants in Attio as notes on the campaign record for human review

2. **Human action required:** Review AI-generated creative variants. Approve or edit before launch. Approve at least 3 per platform per 2-week cycle.

3. Build an n8n creative rotation workflow:
   - Daily check: for each active ad, query the platform API for CTR over the last 7 days
   - If CTR has dropped > 30% from the ad's first-week average, mark it as fatigued
   - If an ad has run > 28 days, mark it for replacement regardless of CTR
   - Pause fatigued/expired ads via the platform API
   - Activate the next approved variant from the queue
   - Log all rotation events to PostHog: `creative_rotated` with properties `{platform, old_creative_id, new_creative_id, reason, ctr_at_pause}`

### 2. Set up systematic A/B testing

Run the `ab-test-orchestrator` drill for retargeting experiments:

1. Define the testing roadmap (run 1 experiment per platform per month):

   **Month 1 experiments:**
   - Meta: Test high-intent (14-day) vs. expanded (30-day) audience window
   - LinkedIn: Test job-title targeting vs. company-list targeting for retargeting audiences

   **Month 2 experiments:**
   - Meta: Test static image vs. carousel ad format for retargeting
   - Google Display: Test responsive display ads vs. custom-sized banners

   **Month 3 experiments:**
   - Cross-platform: Test different landing pages per audience segment (high-intent gets demo page, medium-intent gets case study page)

2. For each experiment:
   - Create a PostHog feature flag to split traffic (for landing page tests) or use the platform's native A/B test (for creative tests)
   - Set minimum sample size: 200 conversions per variant (or 500 clicks if conversion volume is too low)
   - Run for minimum 14 days
   - Evaluate using `experiment-evaluation` fundamental: adopt winner if >= 95% statistical significance, extend if borderline, revert if loser

3. Build an n8n workflow that checks experiment status daily:
   - Query PostHog for variant performance
   - If sample size reached and one variant has >= 95% significance: send Slack alert recommending adoption
   - If experiment has run 28+ days without significance: send alert recommending it be stopped (variants are equivalent)

### 3. Build cross-platform data sync

Run the `tool-sync-workflow` drill for retargeting-specific integrations:

1. **Audience sync (daily via n8n):**
   - Export new customers and converters from Attio
   - Hash emails with SHA-256
   - Upload to exclusion audiences on Meta, LinkedIn, and Google via their APIs
   - Use the `cross-platform-retargeting-sync` fundamental for API calls
   - Log: `audience_sync_completed` event to PostHog with `{platform, records_added, audience_size}`

2. **Conversion sync (real-time via n8n webhook):**
   - When PostHog fires a `retargeting_conversion` event, trigger an n8n workflow
   - Push the conversion back to the originating platform via its conversion API (Meta CAPI, LinkedIn Conversions API, Google offline conversions)
   - This feeds the platform's optimization algorithm with accurate conversion data

3. **CRM enrichment (real-time via n8n webhook):**
   - When a retargeting conversion occurs, create or update the contact in Attio
   - Set properties: `source: retargeting`, `platform: {platform}`, `audience_segment: {segment}`, `ad_variant: {creative_id}`
   - This enables lead quality analysis by retargeting source

4. **Budget reallocation (weekly via n8n):**
   - Every Monday, query PostHog for per-platform CPA over the last 7 days
   - Compare to 4-week rolling average
   - If a platform's CPA improved > 15%: increase its daily budget by 10%
   - If a platform's CPA worsened > 25%: decrease its daily budget by 15% and redistribute to the best performer
   - Apply the change via platform APIs (adjust campaign daily budget)
   - Log: `budget_reallocation` event to PostHog with `{platform, old_budget, new_budget, reason}`
   - Guardrail: total daily spend across all platforms must not exceed 110% of the approved monthly budget / 30

### 4. Scale spend methodically

Increase total retargeting budget from Baseline levels ($1,500/2-weeks) to $5,000-8,000/month:

1. **Month 1**: Increase to $3,000/mo. Focus on the best-performing platform from Baseline. Add the second platform at 30% of budget. If CPA stays within 120% of Baseline CPA by week 2, proceed.

2. **Month 2**: Increase to $5,000/mo. Activate the third platform at 15% of budget. Begin audience expansion: broaden from high-intent only to include medium-intent segments. If CPA stays within 130% of Baseline CPA, proceed.

3. **Month 3**: Increase to $6,000-8,000/mo. Let the automated budget reallocation workflow manage platform splits based on CPA data. Introduce low-intent audiences on the cheapest platform (typically Google Display at $0.66-1.23 CPC).

At each stage, the n8n budget guardrail workflow must confirm CPA is within target before the agent increases spend.

### 5. Evaluate against threshold

After 3 months, measure:

- **Pass**: >=70 conversions/month AND blended CPA within 130% of Baseline CPA AND at least 2 platforms contributing conversions AND automation handling >=80% of routine tasks (creative rotation, audience sync, budget reallocation)
- **Marginal pass**: 50-69 conversions/month — continue for 1 more month, optimize creative and audience targeting
- **Fail — automation gap**: Conversions meet target but require manual intervention > 5 hours/week — fix the automation workflows before proceeding to Durable
- **Fail — CPA drift**: CPA has increased > 50% from Baseline despite scaling — audience exhaustion likely. Reduce spend, refresh all audiences, and rebuild from the retargeting-setup drill with new segments

## Time Estimate

- Creative pipeline setup and n8n automation: 15 hours
- A/B test design and PostHog experiment setup: 10 hours
- Cross-platform sync workflows (n8n): 15 hours
- Monthly monitoring, optimization, and experiment evaluation (3 months): 25 hours
- Budget scaling and reallocation over 3 months: 5 hours
- Final evaluation and documentation: 5 hours
- **Total: 75 hours over 3 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Meta Ads | Retargeting on Facebook/Instagram | Ad spend: $2,000-4,000/mo (largest share of budget). https://www.facebook.com/business/ads/pricing |
| LinkedIn Ads | Retargeting on LinkedIn | Ad spend: $1,000-2,500/mo. CPC $4.50-12. https://business.linkedin.com/advertise/ads/pricing |
| Google Ads | Retargeting on Display Network | Ad spend: $500-1,500/mo. CPC $0.66-1.23 for remarketing. https://ads.google.com/intl/en/home/pricing/ |
| Webflow | Landing page hosting and A/B variants | $14-29/mo. https://webflow.com/pricing |
| PostHog | Tracking, funnels, experiments, feature flags | Free up to 1M events/mo, then $0.00045/event. https://posthog.com/pricing |
| Anthropic API | AI-generated creative variants | ~$15-30/mo for creative generation volume. https://www.anthropic.com/pricing |

**Estimated total cost: $5,000-8,000/mo ad spend + $30-75/mo tools = $5,030-8,075/month**

## Drills Referenced

- the paid social creative pipeline workflow (see instructions below) — produce, test, and rotate retargeting ad creative across platforms on a 2-week cycle
- `ab-test-orchestrator` — design and run systematic A/B tests on audiences, creative formats, and landing pages with statistical rigor
- `tool-sync-workflow` — build n8n workflows that sync audiences, conversions, and budget allocations across platforms and CRM
