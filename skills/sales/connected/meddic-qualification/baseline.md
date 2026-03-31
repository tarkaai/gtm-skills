---
name: meddic-qualification-baseline
description: >
  MEDDIC Qualification System — Baseline Run. Automate MEDDIC pre-scoring via Clay enrichment,
  run structured discovery calls on all new deals, and measure whether MEDDIC-qualified deals
  close faster and at higher rates than unqualified deals.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Baseline Run"
time: "22 hours over 2 weeks"
outcome: ">=60% of deals with >=80% MEDDIC completeness and >=20% faster deal velocity over 2 weeks"
kpis: ["MEDDIC completeness rate", "Deal velocity", "Close rate by MEDDIC score", "Element quality score"]
slug: "meddic-qualification"
install: "npx gtm-skills add sales/connected/meddic-qualification"
drills:
  - posthog-gtm-events
---

# MEDDIC Qualification System — Baseline Run

> **Stage:** Sales > Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Transition from manual MEDDIC scoring (Smoke) to automated pre-qualification. Every new deal gets auto-scored across all 6 MEDDIC elements via Clay enrichment before the first call. Discovery calls are MEDDIC-structured with auto-generated question guides. At least 60% of deals should reach 80%+ MEDDIC completeness, and MEDDIC-qualified deals should show 20%+ faster velocity (time from Connected to Proposal) compared to your pre-MEDDIC baseline.

## Leading Indicators

- Auto-scoring pipeline processing new deals within 5 minutes of CRM entry
- Discovery call prep briefs auto-generated for all deals scoring >= 50
- Post-call MEDDIC scores correlating with enrichment pre-scores (enrichment accuracy improving)
- At least 1 deal progressed to Champion Engaged or Economic Buyer Meeting stage within the first week
- Element completion rate above 50% across all 6 elements (no single element systematically missing)

## Instructions

### 1. Configure MEDDIC auto-scoring pipeline

Run the the play's scoring criteria drill. This creates an n8n workflow that:
1. Triggers on new deal creation in Attio
2. Pushes the lead to Clay for enrichment across all 6 MEDDIC elements
3. Clay enriches: org chart (Economic Buyer), tech stack and compliance (Decision Criteria), company size and procurement signals (Decision Process), job postings and competitor reviews (Identify Pain), LinkedIn engagement and content creation (Champion), revenue and growth data (Metrics)
4. Computes per-element scores and composite MEDDIC pre-score
5. Pushes scores back to Attio with element-level evidence
6. Routes: Qualified (70+) triggers Slack alert with booking link, Needs Work (40-69) gets prioritized, Disqualified (<40) goes to nurture

If the meddic scorecard setup workflow (see instructions below) was not already run at Smoke, run it first — the auto-scoring drill depends on the CRM fields being configured.

Estimated time: 4 hours setup.

### 2. Set up comprehensive event tracking

Run the `posthog-gtm-events` drill to configure tracking events specific to this play:
- `meddic_auto_score_completed` — every time a deal is auto-scored
- `meddic_discovery_call_completed` — every post-call MEDDIC extraction
- `meddic_element_completed` — individual element moves from Unknown to assessed
- `meddic_champion_identified` — champion status becomes Active Champion
- `meddic_economic_buyer_engaged` — economic buyer meeting completed
- `meddic_stage_changed` — deal moves between pipeline stages

Connect PostHog to Attio via webhook so all stage changes are tracked automatically.

Estimated time: 2 hours.

### 3. Run MEDDIC discovery calls on all new deals

For every deal that enters the pipeline during the 2-week run, run the the meddic discovery call workflow (see instructions below) drill:

1. Before each call, the agent pulls the deal's auto-scored MEDDIC profile and generates a targeted question guide focusing on the weakest elements
2. Fireflies records and transcribes the call
3. Post-call, `call-transcript-meddic-extraction` extracts structured MEDDIC scores from the transcript
4. The agent updates Attio with post-call scores, compares against pre-call enrichment scores, and logs the delta
5. Deal routes to the appropriate stage based on composite score

**Human action required:** The founder runs the discovery calls. The agent handles all prep, post-call processing, and CRM updates.

Target: Run MEDDIC discovery calls on 10-15 deals over the 2-week period. Each call should cover the weakest MEDDIC elements identified by auto-scoring.

Estimated time: 12 hours (prep + calls + follow-up across 10-15 deals).

### 4. Track enrichment accuracy

After each discovery call, compare the pre-call enrichment scores against the post-call scores extracted from the actual conversation. Track per-element:
- **Enrichment accuracy** = 1 - |pre_score - post_score| / 100
- If any element consistently has accuracy below 50%, the enrichment signals for that element need recalibration

Log accuracy data in PostHog to build a calibration dataset. Over time, this tells you which MEDDIC elements can be reliably pre-scored via enrichment and which require live conversation.

Estimated time: 1 hour analysis.

### 5. Evaluate against threshold

After 2 weeks, measure:
- **MEDDIC completeness rate:** What percentage of scored deals have >=80% completeness? Target: >=60%.
- **Deal velocity:** Compare average time from Connected to Proposal for MEDDIC-scored deals vs. your historical baseline. Target: >=20% faster.
- **Close rate by MEDDIC score:** Do deals with higher composite scores close at higher rates?
- **Element quality score:** For each of the 6 elements, what percentage of deals have that element scored above 50?

If PASS (>=60% completeness and >=20% velocity improvement), proceed to Scalable. If FAIL, diagnose:
- Low completeness? Check if auto-scoring is firing and if discovery calls are being run consistently.
- No velocity improvement? Check if MEDDIC insights are actually being used to prioritize next steps (not just scored and ignored).
- One element consistently weak? Adjust enrichment for that element or add more targeted discovery questions.

Estimated time: 3 hours analysis.

## Time Estimate

- Auto-scoring pipeline setup: 4 hours
- Event tracking setup: 2 hours
- Discovery calls (10-15 deals): 12 hours
- Enrichment accuracy analysis: 1 hour
- Threshold evaluation: 3 hours

**Total: ~22 hours over 2 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal records, MEDDIC attributes, pipeline | Standard stack (excluded) |
| PostHog | Event tracking, qualification funnel analytics | Standard stack (excluded) |
| n8n | Orchestration — auto-scoring workflow, webhooks | Standard stack (excluded) |
| Clay | Prospect enrichment across all 6 MEDDIC elements | Launch: $185/mo (2,500 credits). [clay.com/pricing](https://www.clay.com/pricing) |
| Fireflies.ai | Call transcription for MEDDIC extraction | Pro: $10/user/mo annual. [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Cal.com | Meeting scheduling | Standard stack (excluded) |
| Anthropic API | Claude for transcript MEDDIC extraction + call prep | ~$10-30/mo at this volume. [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Play-specific cost: ~$205-225/mo** (Clay Launch $185 + Fireflies Pro $10 + Anthropic API ~$10-30)

## Drills Referenced

- the play's scoring criteria — automated pre-qualification pipeline via Clay enrichment for all 6 MEDDIC elements
- the meddic discovery call workflow (see instructions below) — full discovery call lifecycle with element-targeted questions and transcript extraction
- the meddic scorecard setup workflow (see instructions below) — CRM infrastructure (run at Smoke, verify it is active)
- `posthog-gtm-events` — event tracking configuration for MEDDIC qualification milestones
