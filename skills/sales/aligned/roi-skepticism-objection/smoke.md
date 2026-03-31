---
name: roi-skepticism-objection-smoke
description: >
  ROI Skepticism Handling — Smoke Test. For 5 deals where the prospect questions
  ROI or value claims, manually build a prospect-specific ROI calculator using
  their own pain data, present it collaboratively, and track whether it resolves
  the skepticism and advances the deal.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "ROI skepticism resolved on >=3 of 5 opportunities, measured by deal advancing to next stage within 7 days of ROI presentation"
kpis: ["ROI objection resolution rate", "Collaborative model acceptance rate", "Deal progression rate post-ROI presentation", "Prospect-initiated follow-up rate"]
slug: "roi-skepticism-objection"
install: "npx gtm-skills add sales/aligned/roi-skepticism-objection"
drills:
  - roi-calculator-build
  - threshold-engine
---

# ROI Skepticism Handling — Smoke Test

> **Stage:** Sales > Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

ROI skepticism resolved on 3 or more of 5 opportunities. Resolution means the prospect accepts the ROI model (with or without adjustments), references it in subsequent conversations, or advances the deal to the next stage within 7 days of presentation. The collaborative model approach (prospect adjusts their own inputs) outperforms static ROI claims.

## Leading Indicators

- Prospect adjusts inputs in the ROI calculator rather than dismissing it (engagement signal)
- Prospect asks "What assumptions are behind X?" rather than "I don't believe your numbers" (curiosity vs rejection)
- Prospect forwards the ROI calculator to a colleague or decision maker
- Prospect references ROI numbers from the calculator in a follow-up email or call
- Meeting runs past scheduled time because prospect wants to explore scenarios

## Instructions

### 1. Identify 5 deals with ROI skepticism

Query Attio for deals currently in Proposed or Negotiation stage where the prospect has expressed doubt about value or ROI. Signals to look for:

- Call transcript containing phrases like "I'm not sure the ROI is there," "we need to see more proof," "how do you quantify that," "those numbers seem high"
- Email replies questioning pricing relative to value
- Deal stalled after pricing was shared with no objection explicitly stated (implicit ROI skepticism)
- Champion flagging that the economic buyer needs "more justification"

Select 5 deals with the strongest pain data (at least 2 quantified pains from discovery). These need enough raw material to build a credible ROI model.

### 2. Build prospect-specific ROI calculators

For each of the 5 deals, run the `roi-calculator-build` drill. This drill:

1. Validates readiness: checks that the deal has >= 2 quantified pains, >= 50% pain quantification rate, and >= 3x pain-to-price ratio
2. Re-quantifies weak pains using the `pain-quantification-prompt` fundamental with any new context
3. Generates a structured ROI model via `roi-model-generation` with conservative estimates, cited sources, and sensitivity analysis (conservative/moderate/optimistic scenarios)
4. Builds a shareable artifact — use Google Sheets format so the prospect can adjust inputs

Critical: every number in the calculator must trace back to something the prospect said or to a cited industry benchmark. No invented savings. Conservative by default.

If any deal fails the readiness check (pain-to-price ratio < 3), note it and either run additional discovery or replace it with another deal.

### 3. Present the ROI collaboratively

**Human action required:** Present the ROI calculator to each prospect. The key differentiator at this play is the collaborative approach — the prospect builds conviction by adjusting their own numbers, not by reading your claims.

Recommended framing for each presentation:

1. **Anchor to their words (1 min):** "You told me [exact pain quote]. Based on your numbers, that costs you approximately $X per year."
2. **Show the model structure (3 min):** Walk through the inputs, assumptions, and calculation logic. Point out every input they can change. "This assumes 12 reps at $80K average cost — adjust that to match your actual numbers."
3. **Let them drive (5-10 min):** Hand over the calculator. Let the prospect adjust inputs. Track what they change and what they accept. If they adjust a number down, ask why — this reveals hidden context. If they adjust up, that is a strong buying signal.
4. **Reveal scenarios (2 min):** Show conservative vs moderate vs optimistic. Anchor the conversation on conservative: "Even in the worst case, you're looking at Xx return."
5. **Ask for validation (1 min):** "Does this model capture your situation accurately? What am I missing?" Their answer tells you where conviction gaps remain.

### 4. Log results in Attio

After each ROI presentation, update the deal record in Attio:

```json
{
  "roi_presented": true,
  "roi_presented_date": "2026-03-30",
  "roi_prospect_validated": true,
  "roi_prospect_adjustments": "Reduced headcount from 12 to 10, increased hourly rate to $90",
  "roi_final_value": 1420,
  "roi_final_payback_months": 2,
  "roi_presentation_format": "collaborative_spreadsheet",
  "roi_skepticism_resolved": true,
  "roi_resolution_method": "collaborative_model",
  "deal_advanced_within_7_days": true
}
```

Create an Attio note summarizing: what the prospect was skeptical about, what changed their mind (or did not), what adjustments they made, and what the next step is.

### 5. Track events in PostHog

Fire PostHog events for each presentation:

- `roi_calculator_presented` with properties: `deal_id`, `format` ("spreadsheet"), `roi_percentage`, `payback_months`, `pain_to_price_ratio`, `pain_count`
- `roi_calculator_validated` (if prospect engaged with the model) with properties: `deal_id`, `prospect_adjusted` (boolean), `adjustment_direction` ("up", "down", "unchanged"), `original_roi`, `adjusted_roi`
- `roi_skepticism_resolved` or `roi_skepticism_unresolved` with properties: `deal_id`, `resolution_method`, `days_to_resolution`

### 6. Evaluate against threshold

Run the `threshold-engine` drill after all 5 presentations. The threshold engine checks:

- Primary: >= 3 of 5 deals advanced to the next stage within 7 days of ROI presentation
- Secondary: Collaborative model acceptance rate (prospect engaged with inputs) >= 60%
- Secondary: At least 1 deal where the prospect referenced the ROI model in a subsequent communication

If PASS, document which resolution methods worked (collaborative model, case study reference, scenario analysis) and proceed to Baseline. If FAIL, diagnose: was the problem model quality (prospects rejected the math), proof quality (no credible references), or presentation approach (prospect never engaged with the calculator).

## Time Estimate

- 30 min per deal for ROI calculator build (agent-assisted): 2.5 hours
- 30 min per presentation (human-led): 2.5 hours
- 15 min per deal for logging and tracking: 1.25 hours
- 30 min for threshold evaluation: 0.5 hours
- **Total: ~7 hours over 1 week** (rounded to ~6 hours in metadata accounting for parallel work)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal records, pain data, ROI tracking | Free tier for up to 3 users; Plus $29/user/mo |
| PostHog | Analytics — ROI presentation events and funnel tracking | Free tier includes 1M events/mo |
| Fireflies | Transcription — call recordings for pain extraction | Free tier 800 min/mo; Pro $10/user/mo |
| Google Sheets | ROI calculator artifact — shareable, editable by prospect | Free |
| Anthropic API | AI — ROI model generation and pain quantification | ~$0.10-0.30 per model (~$1.50 total for 5 deals) |

**Estimated play-specific cost at Smoke:** $0-2 (Anthropic API only; all other tools have free tiers)

## Drills Referenced

- `roi-calculator-build` — validates pain data readiness, generates a prospect-specific ROI model with conservative estimates and sensitivity analysis, builds a shareable calculator artifact
- `threshold-engine` — evaluates the 5 presentations against pass/fail criteria and diagnoses failure patterns
