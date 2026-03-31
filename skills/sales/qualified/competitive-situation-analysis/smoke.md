---
name: competitive-situation-analysis-smoke
description: >
  Competitive Situation Assessment — Smoke Test. Run structured competitive discovery on 10+
  qualification calls to identify which competitors prospects evaluate, map decision criteria,
  and validate that competitive intelligence can be systematically extracted from conversations.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "Competitive situation identified in ≥8 opportunities in 1 week with ≥60% having active competitor evaluation"
kpis: ["Competitive discovery completion rate", "Competitor identification rate", "Decision criteria clarity score", "Competitive intelligence extraction accuracy"]
slug: "competitive-situation-analysis"
install: "npx gtm-skills add sales/qualified/competitive-situation-analysis"
drills:
  - competitive-discovery-call
  - posthog-gtm-events
  - threshold-engine
---

# Competitive Situation Assessment — Smoke Test

> **Stage:** Sales → Qualified | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Competitive intelligence systematically extracted from at least 8 qualification calls in one week. For each call: competitors identified by name and type, evaluation stage mapped, decision criteria ranked, and status quo risk assessed. At least 60% of analyzed opportunities have an active competitor evaluation (not just status quo).

## Leading Indicators

- Fireflies transcripts available for all qualification calls (transcription pipeline working)
- Claude extraction producing valid structured JSON (extraction prompt working)
- Competitor names matching across multiple deals (real competitors, not noise)
- Decision criteria showing consistent themes (market is evaluable)
- Attio deal records updating with competitive fields (CRM pipeline working)

## Instructions

### 1. Configure competitive event tracking

Run the `posthog-gtm-events` drill to define competitive-specific events. Create these events in PostHog:

- `competitive_situation_extracted` — fired after each call analysis
- `competitor_named` — fired for each competitor identified, with `competitor_name`, `competitor_type`, `evaluation_stage`, and `prospect_sentiment` properties
- `status_quo_bias_detected` — fired when no competitors are found and prospect defaults to current solution
- `competitive_discovery_quality` — fired with `seller_score` (strong/adequate/weak) to track discovery skill

### 2. Run competitive discovery on 10+ qualification calls

For each qualification call with a Fireflies transcript, run the `competitive-discovery-call` drill manually:

1. Retrieve the transcript from Fireflies
2. Run `call-transcript-competitor-extraction` to extract: competitors evaluated, decision criteria, evaluation method, status quo analysis, and competitive risk level
3. Update the Attio deal record with competitive situation data
4. Create a structured competitive note on the deal
5. Fire the PostHog events

**Human action required:** During the actual qualification calls, ask these competitive discovery questions (the extraction fundamental evaluates whether you asked them):
- "What other solutions are you currently evaluating?"
- "How are you comparing alternatives — is there a formal process or informal?"
- "What's most important to you in selecting a solution?" (decision criteria)
- "How far along are you with [named competitor]?" (evaluation stage)
- "What do you wish [competitor/current solution] could do that it can't?" (gaps)

### 3. Analyze extraction results across all calls

After processing 10+ calls, query Attio for all deals with `competitive_situation_date` in the past week. Calculate:

- **Discovery completion rate:** Calls with competitive extraction / Total qualification calls
- **Competitor identification rate:** Calls with ≥1 named competitor / Calls analyzed
- **Decision criteria clarity:** Calls with ≥2 ranked criteria / Calls analyzed
- **Extraction accuracy:** Manually spot-check 3 extractions against raw transcripts — are competitor names correct? Are quotes actually in the transcript? Are evaluation stages plausible?

### 4. Map the competitive landscape

Aggregate competitor mentions across all analyzed calls:
- Which competitors appear most frequently?
- What competitor types dominate (direct, indirect, status quo, build in house)?
- Are there competitors appearing in 3+ deals already? (candidates for battlecard investment)
- What decision criteria recur across deals? (these become your positioning anchors)

Log this landscape summary as an Attio note on a "Competitive Intelligence" campaign record.

### 5. Evaluate against threshold

Run the `threshold-engine` drill to evaluate:
- **Primary threshold:** Competitive situation identified in ≥8 opportunities in 1 week
- **Secondary threshold:** ≥60% of analyzed opportunities have active competitor evaluation

If PASS: competitive discovery is producing signal. The extraction pipeline works, competitors are identifiable, and decision criteria are extractable. Proceed to Baseline.

If FAIL: diagnose the bottleneck:
- If < 10 calls available: volume problem. Need more qualification conversations.
- If extraction accuracy < 80%: prompt problem. Refine the `call-transcript-competitor-extraction` prompt.
- If < 60% have competitors: either prospects are status-quo-biased (adjust discovery questions to probe harder) or the market has low competitive density (which is actually positive intel).

## Time Estimate

- 1 hour: Configure PostHog events and verify Fireflies integration
- 2.5 hours: Run competitive discovery drill on 10+ calls (15 min per call)
- 1 hour: Analyze results, build competitive landscape map
- 0.5 hours: Threshold evaluation and decision

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Fireflies | Call transcription | Free (800 min/mo) or Pro $10/user/mo annual — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Anthropic Claude API | Competitive extraction from transcripts | ~$0.02-0.05 per call extraction — [anthropic.com/pricing](https://www.anthropic.com/pricing) |
| Attio | Deal records + competitive situation storage | Included in standard stack — [attio.com/pricing](https://attio.com/pricing) |
| PostHog | Event tracking | Free tier (1M events/mo) — [posthog.com/pricing](https://posthog.com/pricing) |

**Estimated play-specific cost:** Free (within free tiers) to ~$15/mo (Fireflies Pro + Claude API usage)

## Drills Referenced

- `competitive-discovery-call` — extracts competitive intelligence from each qualification call transcript and updates CRM
- `posthog-gtm-events` — sets up the event taxonomy for competitive tracking
- `threshold-engine` — evaluates results against pass/fail threshold
