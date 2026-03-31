---
name: bant-qualification-baseline
description: >
  BANT Qualification Framework — Baseline Run. First always-on BANT qualification with automated
  outreach feeding discovery calls, structured scoring after every call, and continuous pipeline
  tracking. Proves BANT qualification works repeatably over 2 weeks.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: ">=40% qualification rate (composite >=70) from 30+ scored prospects over 2 weeks"
kpis: ["Qualification rate", "Time to qualify", "Disqualification reason breakdown", "Call-to-qualified conversion rate", "BANT dimension accuracy (pre-score vs post-call)"]
slug: "bant-qualification"
install: "npx gtm-skills add sales/qualified/bant-qualification"
drills:
  - cold-email-sequence
  - linkedin-outreach
  - bant-discovery-call
  - posthog-gtm-events
  - enrich-and-score
---

# BANT Qualification Framework — Baseline Run

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Prove that BANT qualification works repeatably with automated outreach feeding the top of the funnel. Over 2 weeks, score 30+ prospects through discovery calls and achieve a >=40% qualification rate. The BANT scoring model should produce consistent, actionable results — qualified deals should be progressing through your pipeline while disqualified ones are correctly filtered out.

## Leading Indicators

- Reply rate on cold outreach is >=5% (enough to fill the discovery call pipeline)
- Discovery calls are being scheduled at a rate of 3+ per week
- BANT scores from discovery calls are distributed across the spectrum (not all clustering)
- Pre-enrichment scores are directionally correlated with post-call scores (enrichment model is learning)
- Disqualified prospects have clear, documented reasons (not vague "not a fit")

## Instructions

### 1. Scale the prospect list and enrich for BANT signals

Run the `enrich-and-score` drill to build a list of 100-150 prospects. Use Clay's enrichment waterfall to populate BANT-relevant signals for each prospect:

- **Budget signals:** Funding round, estimated revenue, tech spend indicators, headcount growth
- **Authority signals:** Title seniority, department match, org chart position
- **Need signals:** Job postings for relevant roles, tech stack gaps, competitor usage
- **Timeline signals:** Recent funding, leadership changes, fiscal year timing

Score each prospect in Clay using the BANT formula from Smoke. Push scored prospects to Attio with their per-dimension scores. Prioritize outreach to prospects scoring 50+ (Warm and Hot tiers).

### 2. Launch cold email sequences

Run the `cold-email-sequence` drill to set up a 4-step email sequence in Instantly targeting your scored prospect list. Personalize the first line using BANT-relevant signals from Clay:

- For prospects with strong Need signals: lead with their specific pain point
- For prospects with strong Timeline signals: reference the triggering event (funding, hiring, etc.)
- For prospects with strong Authority signals: reference a peer who solved a similar problem

Set up A/B testing on subject lines (2 variants minimum). Configure Instantly to detect positive replies and route them to Attio as hot leads.

### 3. Launch LinkedIn outreach in parallel

Run the `linkedin-outreach` drill to set up connection requests + follow-up messages targeting the same list. Coordinate with email timing — do not email and LinkedIn-message the same person on the same day. Focus LinkedIn messages on Need and Authority (these dimensions benefit most from conversational context).

### 4. Configure qualification tracking

Run the `posthog-gtm-events` drill to set up event tracking for the BANT qualification funnel:

- `bant_outreach_sent` — cold email or LinkedIn message sent
- `bant_reply_received` — positive reply detected
- `bant_discovery_scheduled` — call booked via Cal.com
- `bant_discovery_completed` — call held and scored
- `bant_qualified` — composite score >=70
- `bant_needs_work` — composite score 40-69
- `bant_disqualified` — composite score <40

Connect PostHog to Attio via n8n webhook so deal stage changes fire the corresponding events.

### 5. Run discovery calls and score

**Human action required:** Conduct discovery calls as they get booked from outreach replies.

For each call, run the `bant-discovery-call` drill:
1. Pre-call: review enrichment data, identify weakest BANT dimensions, generate tailored questions
2. Post-call: extract BANT signals from Fireflies transcript using LLM analysis
3. Update CRM: log structured BANT scores, call notes, and next steps in Attio
4. Route: move deal to the correct pipeline stage based on composite score

Track the delta between pre-enrichment scores and post-call scores for each prospect. This calibrates your enrichment model — if pre-scores consistently overestimate Authority, adjust the enrichment formula.

### 6. Evaluate against threshold

After 2 weeks, review all scored prospects:

- Total prospects scored: target 30+
- Qualification rate: target >=40% (composite >=70)
- Disqualification reasons: which BANT dimensions are causing the most disqualifications?
- Pre-score accuracy: how closely do enrichment-based pre-scores predict post-call scores?

If PASS (>=40% qualification rate at 30+ prospects), proceed to Scalable. If FAIL, diagnose:
- Low reply rate (<3%): messaging or targeting problem — revisit ICP and email copy
- Low call-to-qualified rate: your pipeline has prospects who look good on paper but fail on the phone — tighten enrichment scoring thresholds
- One dimension consistently failing: address that specific gap (e.g., always failing on Budget = wrong company size/stage)

## Time Estimate

- Prospect enrichment and list building: 3 hours
- Cold email sequence setup: 2 hours
- LinkedIn outreach setup: 1 hour
- PostHog event tracking: 1 hour
- Discovery calls (12-15 calls at 25 min each): 5-6 hours
- Post-call scoring and CRM logging: 3 hours
- Analysis and calibration: 2 hours

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM with BANT pipeline | Free tier or Plus $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Instantly | Cold email sequences | Growth $47/mo — [instantly.ai/pricing](https://instantly.ai/pricing) |
| Clay | Prospect enrichment with BANT signals | Launch $185/mo — [clay.com/pricing](https://clay.com/pricing) |
| Fireflies | Call transcription for BANT extraction | Pro $18/user/mo — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| PostHog | Qualification funnel tracking | Free (1M events/mo) — [posthog.com/pricing](https://posthog.com/pricing) |
| Cal.com | Discovery call booking | Free — [cal.com/pricing](https://cal.com/pricing) |
| Anthropic API | LLM BANT extraction from transcripts | ~$3/MTok input (Sonnet) — [docs.anthropic.com/pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |

**Estimated play-specific cost:** ~$250-350/mo (Instantly $47 + Clay $185 + Fireflies $18 + Anthropic ~$5-10 for transcript analysis)

## Drills Referenced

- `cold-email-sequence` — 4-step cold email sequence in Instantly with BANT-personalized copy
- `linkedin-outreach` — parallel LinkedIn connection + message sequence
- `bant-discovery-call` — structured discovery call lifecycle with LLM-based BANT extraction
- `posthog-gtm-events` — event tracking for the full BANT qualification funnel
- `enrich-and-score` — Clay enrichment with BANT-specific signal scoring
