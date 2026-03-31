---
name: timing-qualification-smoke
description: >
  Timing Qualification Process — Smoke Test. Manually qualify 15-20 prospects on buying
  timeline through discovery calls. Validate that timing questions produce actionable
  categorization (Immediate/Near-term/Medium-term/Long-term) and that urgency predicts deal velocity.
  Agent preps questions and extracts signals from transcripts; founder executes calls.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Email, Direct"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=8 prospects timeline-qualified in 1 week with >=50% categorized as Immediate or Near-term"
kpis: ["Timeline identification rate", "Urgent opportunity percentage (Immediate + Near-term)", "Timeline confidence distribution", "Effective question hit rate"]
slug: "timing-qualification"
install: "npx gtm-skills add sales/qualified/timing-qualification"
drills:
  - icp-definition
  - build-prospect-list
  - timing-scorecard-setup
  - timing-discovery-call
  - threshold-engine
---

# Timing Qualification Process — Smoke Test

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Outcomes

Prove that structured timing questions produce meaningful signal about when prospects will buy. After qualifying 15-20 prospects, at least 8 should have a timeline category assigned with confidence >= 3. The categorization should differentiate deals that will move fast from those that will not — Immediate and Near-term prospects should represent at least 50% of qualified deals (indicating the ICP targets buyers with active urgency, not just general interest).

## Leading Indicators

- Discovery calls produce different timeline categories (not all clustering in one bucket)
- At least 2 distinct urgency drivers are identified across the batch (proving multiple timing triggers exist in your market)
- Timeline confidence scores vary (some 4-5, some 2-3) — this means the questions are probing deeply, not just getting surface answers
- Prospects categorized as Immediate are agreeing to next steps faster than Medium-term or Long-term prospects

## Instructions

### 1. Define your ICP and timing-specific criteria

Run the `icp-definition` drill to document your Ideal Customer Profile. Extend it with timing-specific criteria:

- **Urgency triggers in your market:** What events create buying urgency? Map at least 5: contract renewals, fiscal year end, leadership changes, funding rounds, regulatory deadlines, seasonal peaks, competitor moves, pain escalation.
- **Timeline indicators by ICP segment:** Which segments tend to buy fastest? B2B SaaS companies post-funding often have 30-90 day evaluation windows. Enterprise with procurement cycles are usually 3-6 months. Document these patterns.
- **Anti-urgency signals:** What tells you a prospect has no timeline? "Just exploring," "building a business case," "next fiscal year." Recognizing these saves time.

### 2. Set up timeline scoring in your CRM

Run the `timing-scorecard-setup` drill to create timeline custom fields on Attio Deals:
- Timeline category (Immediate/Near-term/Medium-term/Long-term)
- Target close date
- Urgency drivers (multi-select)
- Timeline confidence (1-5)
- Slippage risk (High/Medium/Low)
- Consequence of inaction (text)

This also configures pipeline routing rules so Immediate deals go to a fast-track lane.

### 3. Build a small prospect list

Run the `build-prospect-list` drill to source 15-20 contacts matching your ICP. Keep the list small — this is a smoke test. Source from Clay or Apollo, enrich with basic firmographics, and push to Attio. For each prospect, note any pre-call timing signals visible from public data (recent funding, job postings, contract renewal windows).

### 4. Run timing-focused discovery calls

**Human action required:** Book and conduct 10-15 discovery calls over the week. Use the `timing-discovery-call` drill for each call:

1. Before each call: the agent reviews pre-enrichment data and generates a customized timing question guide targeting the biggest unknowns
2. During the call: weave timing questions naturally into the conversation. Focus on the [MUST ASK] questions: "What's driving you to solve this now?", "When do you need this in place?", "What happens if you don't solve this by then?"
3. After each call: the agent retrieves the Fireflies transcript, runs `call-transcript-timing-extraction` to extract timeline signals, scores the deal, and updates Attio

The drill handles pre-call prep, post-call extraction, scoring, and CRM logging automatically. The only human step is conducting the actual call.

### 5. Score and evaluate

After completing your calls, review the timeline scores across all prospects. Run the `threshold-engine` drill to evaluate against the pass threshold: >=8 prospects timeline-qualified with >=50% categorized as Immediate or Near-term.

Analyze:
- **Timeline distribution:** What percentage fell into each category? If >70% are Long-term, your ICP may not be targeting active buyers.
- **Confidence calibration:** Did high-confidence predictions (4-5) come from prospects who stated explicit dates? Did low-confidence (1-2) come from vague answers?
- **Urgency driver frequency:** Which triggers appeared most often? This tells you what to look for in pre-enrichment at later levels.
- **Effective questions:** Which timing questions produced the most useful information? Document the top 3 for reuse.
- **Timeline vs. deal velocity:** Did Immediate prospects agree to next steps faster? If not, the categorization needs refinement.

If PASS, proceed to Baseline. If FAIL, diagnose: wrong ICP (no one has urgency), wrong questions (not probing deep enough), or wrong channels (not reaching decision-makers who control timing).

## Time Estimate

- ICP definition and timing criteria: 1 hour
- CRM scorecard setup: 30 minutes
- Prospect list build: 1 hour
- Discovery calls (10-15 at 20-30 min each): 3-4 hours
- Post-call scoring and analysis: 30 minutes

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM with timeline custom fields | Free (up to 3 users) — [attio.com/pricing](https://attio.com/pricing) |
| Fireflies | Call recording and transcription | Free (800 min/mo) or Pro $18/user/mo — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Cal.com | Discovery call scheduling | Free (1 user) — [cal.com/pricing](https://cal.com/pricing) |
| Clay | Prospect enrichment | Launch $185/mo — [clay.com/pricing](https://clay.com/pricing) |
| PostHog | Event tracking | Free (1M events/mo) — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API | Transcript timing extraction | ~$2-5 for smoke-test volume — [docs.anthropic.com/pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |

**Estimated play-specific cost:** $0-18/mo (Fireflies Pro optional; everything else fits free tiers at smoke-test volume)

## Drills Referenced

- `icp-definition` — define ICP and extend with timing-specific qualification criteria
- `build-prospect-list` — source and enrich 15-20 prospects from Clay/Apollo
- `timing-scorecard-setup` — create timeline scoring infrastructure in Attio
- `timing-discovery-call` — structured discovery call with transcript timing extraction
- `threshold-engine` — evaluate results against the pass threshold
