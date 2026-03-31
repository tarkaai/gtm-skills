---
name: pricing-presentation-framework-scalable
description: >
  Pricing Presentation Framework — Scalable Automation. Fully automated
  pricing proposal generation triggered by deal stage changes, A/B testing
  of tier structures and presentation formats, and intelligent discount
  guidance across all deals at volume.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Scalable Automation"
time: "50 hours over 2 months"
outcome: "Automated pricing proposals for 100% of qualifying deals with acceptance rate >=60% of Baseline and average discount <=12% at 3x+ deal volume"
kpis: ["Pricing acceptance rate at scale", "Discount optimization", "Tier mix revenue impact", "Proposal generation latency"]
slug: "pricing-presentation-framework"
install: "npx gtm-skills add sales/proposed/pricing-presentation-framework"
drills:
  - roi-auto-generation
  - dashboard-builder
  - threshold-engine
---

# Pricing Presentation Framework — Scalable Automation

> **Stage:** Sales > Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Remove the human bottleneck from pricing proposal generation. Every deal entering Proposed stage with qualifying pain data gets an auto-generated pricing proposal within 1 hour — no agent intervention needed. A/B test tier structures, presentation formats, and value anchoring approaches to find the highest-acceptance, lowest-discount combination. Target: automated proposals for 100% of qualifying deals, acceptance rate >=60% of Baseline level, average discount <=12%, at 3x or more deal volume.

## Leading Indicators

- n8n pricing automation workflow running with zero manual triggers for >=90% of proposals
- Proposal generation latency <=1 hour from deal stage change
- At least 2 A/B experiments completed with statistically significant results
- Tier recommendation accuracy improving (tier match rate trending up)
- Discount intelligence reducing unnecessary concessions (zero-discount acceptance rate increasing)
- Average deal size stable or increasing despite higher volume

## Instructions

### 1. Build automated pricing proposal generation

Create an n8n workflow triggered by Attio deal stage changes:

**Trigger:** Attio webhook fires when a deal enters Proposed stage
**Filter conditions:**
- `pain_count >= 2`
- `pain_quantification_rate >= 0.5`
- `pricing_proposal_status` != "generated" (prevent duplicates)

**Workflow steps:**
1. Pull full deal record from Attio (pains, ROI model, champion, company data, competitive context)
2. Check if ROI model exists. If not, run the `roi-auto-generation` drill inline to generate ROI from pain data automatically — this is the key difference from Baseline where ROI was pre-built
3. Validate pain-to-price ratio. If <3x, skip auto-generation and alert seller: "Deal {name} has weak ROI ({ratio}x). Complete additional discovery before pricing."
4. Run `pricing-tier-generation` to produce Good/Better/Best structure
5. Build proposal artifact (formatted pricing comparison document)
6. Store in Attio, fire `pricing_proposal_generated` in PostHog
7. Notify seller via Slack with review link and recommended presentation talking points
8. Schedule a follow-up check: if `pricing_proposal_status` is still "generated" (not "presented") after 48 hours, send a reminder

**Rate limit:** Maximum 15 auto-generated proposals per day (controls API costs at ~$1-2/proposal).

**Error handling:** If `pricing-tier-generation` fails (API error, invalid output), retry once. On second failure, alert seller and log the error. Do not block the deal.

### 2. Launch pricing A/B experiments

Run the the deal term ab testing workflow (see instructions below) drill to systematically test pricing variables. Unlike the generic deal-term drill, configure experiments specifically for pricing presentation:

**Experiment 1: Presentation format**
- Control: email proposal with pricing PDF attachment
- Variant: interactive pricing page (Qwilr or equivalent) with adjustable tier comparison
- Primary metric: acceptance rate
- Secondary metric: days to decision, discount request rate

**Experiment 2: Number of tiers**
- Control: 3 tiers (Good/Better/Best)
- Variant: 2 tiers (Standard/Premium, removing the cheapest option)
- Primary metric: average deal size (does removing Good tier push prospects to Better?)
- Secondary metric: acceptance rate (does fewer options reduce decision paralysis or increase rejection?)

**Experiment 3: Value anchoring depth**
- Control: brief value recap (1-2 sentences summarizing total ROI)
- Variant: detailed value recap (specific pain quotes, line-item savings, payback period)
- Primary metric: acceptance rate
- Secondary metric: discount request rate

Run one experiment at a time. Each experiment needs at least 30 proposals per variant (minimum 4 weeks at typical deal flow). Use PostHog feature flags to randomly assign deals to control or variant.

For each experiment, use `posthog-experiments` to set up the feature flag, and modify the n8n proposal automation to check the flag and generate the appropriate variant.

### 3. Build intelligent discount guidance

Create an n8n workflow that fires when `pricing_discount_requested = true` on any deal:

1. Pull the deal context: tier presented, prospect reaction, competitive situation, pain-to-price ratio
2. Query PostHog for historical discount patterns: what discount levels have led to closes vs losses for similar deals (same tier, similar company size, similar competitive situation)?
3. Generate a discount recommendation:
   - "Hold firm" if historical data shows discounting does not improve close rate for this deal profile
   - "Offer [X]% maximum" if the data shows a sweet spot where minimal discount closes the deal
   - "Restructure" if the data suggests payment terms or tier adjustment works better than price cuts
4. Send the recommendation to the seller via Slack before they respond to the prospect
5. Log the recommendation and actual outcome for future model improvement

### 4. Deploy the pricing intelligence monitor

Run the `dashboard-builder` drill to generate weekly reports:

1. Aggregate all pricing metrics from the past 7 days (volume, acceptance, discount, tier mix, latency)
2. Detect trends: compare against 4-week rolling average
3. Generate recommendations: what to test next, what to adjust, what's working
4. Distribute via Slack and archive in Attio

Use the weekly report to identify when experiments should be started, stopped, or extended.

### 5. Set guardrails and evaluate

**Guardrails (automated via n8n):**
- Acceptance rate must stay >=60% of Baseline level. If it drops below for 2 consecutive weeks, pause experiments and diagnose.
- Average discount must not exceed 12%. If it does, tighten discount guidance and review objection handling workflows.
- Proposal generation errors must stay below 5%. If error rate exceeds this, check API reliability and input data quality.

Run the `threshold-engine` drill monthly. After 2 months, evaluate:
- Are automated proposals performing at or above Baseline acceptance rates?
- Have A/B experiments identified at least 1 winning variant that measurably improved a pricing metric?
- Is deal volume handling >=3x Baseline with no degradation?

If PASS: document all winning experiment variants, update the default pricing configuration, and proceed to Durable.

If FAIL: identify the bottleneck:
- Automated proposals underperforming manual: the generation quality may be too generic. Add more deal-specific context to the prompts.
- Experiments inconclusive: not enough deal volume for statistical significance. Extend test periods or test bolder variants.
- Discount creep: sellers overriding discount guidance. This is a process/training issue, not a tooling issue.

## Time Estimate

- 12 hours: building and testing the automated proposal generation n8n workflow
- 10 hours: setting up A/B experiments with PostHog feature flags
- 8 hours: building intelligent discount guidance workflow
- 8 hours: configuring pricing intelligence monitor for weekly reports
- 12 hours: monitoring, analyzing experiments, and iterating over 2 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal records, pricing data, automated triggers | Standard stack (excluded from play budget) |
| PostHog | Pricing events, funnels, experiments, feature flags, dashboards | Standard stack (excluded from play budget) |
| n8n | Automated proposal generation, discount guidance, weekly reports | Standard stack (excluded from play budget) |
| Anthropic Claude API | Tier generation, ROI modeling, discount analysis at scale | ~$30-80/mo for 50-100 proposals at Sonnet 4.6 rates ($3/$15 per M tokens) — [pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Qwilr (optional) | Interactive pricing pages for format A/B test | $35/user/mo billed annually — [pricing](https://qwilr.com/pricing/) |
| PandaDoc (optional) | Formatted proposal documents with e-sign | $49/user/mo Business plan billed annually — [pricing](https://www.pandadoc.com/pricing/) |

**Play-specific cost:** ~$30-80/month (Claude API at scale) + optional $35-49/month (proposal tool for format experiments)

## Drills Referenced

- `roi-auto-generation` — auto-generates ROI calculators and business cases when deals enter Proposed stage with qualifying pain data
- the deal term ab testing workflow (see instructions below) — runs controlled experiments on pricing variables (format, tier count, value anchoring depth) using PostHog feature flags
- `dashboard-builder` — weekly report on pricing effectiveness with trends, anomalies, and experiment recommendations
- `threshold-engine` — monthly evaluation against acceptance rate, discount, and volume targets
