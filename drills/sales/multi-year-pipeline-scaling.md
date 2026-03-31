---
name: multi-year-pipeline-scaling
description: Scale multi-year deal pipeline with intent signals, commitment-readiness scoring, automated routing, and segment-specific deal structures
category: Sales
tools:
  - Clay
  - Attio
  - n8n
  - PostHog
  - Anthropic
fundamentals:
  - clay-intent-signals
  - clay-scoring
  - attio-deals
  - attio-custom-attributes
  - attio-automation
  - n8n-workflow-basics
  - n8n-scheduling
  - posthog-cohorts
  - posthog-custom-events
  - deal-term-modeling
---

# Multi-Year Pipeline Scaling

This drill expands multi-year deal volume by proactively identifying accounts that should receive multi-year proposals, scoring them for commitment readiness, routing them to the right deal structure, and running segment-specific campaigns. Instead of waiting for deals to reach Proposed stage, this drill finds opportunities upstream.

## Input

- Clay table with account enrichment data
- Attio CRM with historical deal data (at least 10 multi-year wins for pattern matching)
- PostHog with deal negotiation events from `deal-negotiation-tracking` drill
- n8n instance for orchestration
- At least 2 months of multi-year deal data (from Baseline level)

## Steps

### 1. Build the multi-year ICP from historical wins

Using `posthog-cohorts` and `attio-deals`, analyze closed-won multi-year deals to find patterns:

Query Attio for all deals where `multi_year_status` = "closed_won". Extract:
- Company size range (headcount, revenue)
- Industry vertical
- ACV range
- Pain-to-price ratio at time of proposal
- Negotiation rounds (fewer = stronger fit)
- Champion title/seniority
- Time from first contact to multi-year close

Build a "multi-year ICP" profile: the account characteristics that predict multi-year deal success. Store this as a Clay scoring formula.

### 2. Score the existing pipeline for multi-year readiness

Using `clay-scoring`, create a scoring model in Clay that evaluates every account in the pipeline:

| Signal | Weight | Source |
|--------|--------|--------|
| Matches multi-year ICP profile | +30 | Clay enrichment |
| ACV >= $15,000 | +20 | Attio deal value |
| Pain-to-price ratio >= 8x | +15 | Attio pain data |
| Currently in Proposed or Connected stage | +10 | Attio deal stage |
| Fiscal year end within 90 days | +15 | Clay enrichment |
| Has identified champion and economic buyer | +10 | Attio contacts |
| No active competitive evaluation | +10 | Attio competitive intel |
| Previous vendor commitment history (long-term contracts) | +10 | Clay enrichment via LinkedIn/news |

Score range: 0-120. Classify:
- **High readiness (80+):** Auto-trigger multi-year proposal
- **Medium readiness (50-79):** Queue for next proposal cycle
- **Low readiness (<50):** Not a multi-year candidate now

Using `attio-custom-attributes`, store `multiyear_readiness_score` and `multiyear_readiness_tier` on each deal.

### 3. Build segment-specific deal structures

Using `deal-term-modeling`, pre-generate deal structures for each segment:

**High-ACV segment ($50K+ ACV):**
- 3-year terms with rate lock
- Dedicated CSM session included
- Custom SLA provisions
- Payment: annual upfront or quarterly

**Mid-ACV segment ($15K-50K ACV):**
- 2-year terms with rate lock
- Priority support upgrade
- Payment: annual upfront preferred, quarterly available

**Growth segment ($10K-15K ACV):**
- 2-year terms
- Savings-focused positioning (show 3-year total cost)
- Payment: flexible (annual, quarterly, or monthly with commitment)

Store these templates as n8n environment variables so the proposal automation can apply the right structure per segment.

### 4. Build the proactive campaign workflow

Using `n8n-scheduling`, create a weekly workflow:

1. Run the readiness scoring model against all active deals
2. For new High-readiness accounts (not yet proposed): trigger `multi-year-proposal-automation` drill
3. For Medium-readiness accounts approaching fiscal year end (within 60 days): move them to High and trigger proposal
4. For accounts that previously declined multi-year but whose readiness score has increased by 20+ points: flag for re-engagement

Using `clay-intent-signals`, monitor for external triggers:
- Prospect company raises funding (signals growth commitment)
- Prospect company has layoffs (signals cost optimization need — position multi-year as savings)
- Procurement team LinkedIn activity (signals budget cycle)
- Competitor contract renewal mentions (signals switching window)

When an intent signal fires for an account with readiness score >= 50, boost their score by 20 and re-evaluate.

### 5. Track scaling metrics

Using `posthog-custom-events`, fire:
- `multiyear_readiness_scored` — per account, weekly
- `multiyear_proactive_trigger` — when scoring triggers a proposal
- `multiyear_intent_signal_matched` — when an external signal boosts readiness

Build a PostHog dashboard:
- Multi-year pipeline coverage: accounts scored / total active deals
- Proactive vs reactive proposals (triggered by scoring vs manual)
- Conversion rate by readiness tier
- Revenue impact: TCV from proactively identified deals vs organic

## Output

- Multi-year ICP profile derived from historical wins
- Readiness scoring model running weekly on all active deals
- Segment-specific deal structure templates
- Proactive campaign workflow that identifies and triggers proposals
- Intent signal monitoring for external triggers
- Scaling metrics dashboard

## Triggers

Readiness scoring runs weekly via n8n cron. Intent signal monitoring runs continuously via Clay webhooks. Proposal triggers fire in real-time when scoring thresholds are met.
