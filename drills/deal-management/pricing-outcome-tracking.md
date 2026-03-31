---
name: pricing-outcome-tracking
description: Instrument pricing presentation events in PostHog and Attio — track tier presented, prospect reaction, discount requests, acceptance, and deal progression
category: Deal Management
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-funnels
  - posthog-dashboards
  - attio-deals
  - attio-custom-attributes
  - n8n-workflow-basics
  - n8n-triggers
---

# Pricing Outcome Tracking

This drill instruments the full pricing presentation lifecycle so every proposal, reaction, objection, discount request, and outcome is tracked. The data feeds the threshold engine at Smoke/Baseline and the autonomous optimization loop at Durable.

## Input

- PostHog project with API access
- Attio CRM with deals pipeline including Proposed stage
- n8n instance for webhook-based event capture
- At least 1 deal with a pricing proposal generated

## Steps

### 1. Define the pricing event schema

Using `posthog-custom-events`, create the following events:

| Event | When to Fire | Key Properties |
|-------|-------------|----------------|
| `pricing_proposal_generated` | Agent generates tier structure | `deal_id`, `tiers_count`, `recommended_tier`, `recommended_annual_price`, `pain_to_price_ratio`, `roi_year_1`, `discount_applied_pct` |
| `pricing_presented` | Seller presents pricing to prospect | `deal_id`, `presentation_format` (live_call/email/video/in_person), `tiers_shown`, `value_recap_given` (bool), `pains_referenced_count` |
| `pricing_reaction_logged` | Seller logs prospect's initial reaction | `deal_id`, `reaction` (positive/neutral/pushback/silence/asked_for_discount), `tier_discussed`, `questions_asked` |
| `pricing_discount_requested` | Prospect asks for a discount | `deal_id`, `requested_discount_pct`, `discount_reason` (budget/competitor/sticker_shock/negotiation_tactic), `tier_targeted` |
| `pricing_discount_given` | Seller grants a discount | `deal_id`, `original_price`, `discounted_price`, `discount_pct`, `approval_required` (bool), `concession_type` (price_cut/extended_term/bundle_adjustment/payment_flexibility) |
| `pricing_tier_selected` | Prospect selects a tier | `deal_id`, `tier_selected` (Good/Better/Best), `annual_price`, `term_years`, `payment_schedule` |
| `pricing_accepted` | Prospect accepts proposal and moves to close | `deal_id`, `final_annual_price`, `final_tier`, `final_discount_pct`, `days_to_acceptance`, `negotiation_rounds` |
| `pricing_rejected` | Prospect declines or stalls past threshold | `deal_id`, `rejection_reason` (too_expensive/wrong_tier/competitor_chosen/no_decision/timing), `best_offer_price`, `days_since_presentation` |

### 2. Set up Attio custom attributes

Using `attio-custom-attributes`, add these fields to the Deal object:

- `pricing_proposal_status`: Enum (not_generated, generated, presented, accepted, rejected)
- `pricing_tiers_presented`: Number (how many tiers shown)
- `pricing_recommended_tier`: Text (Good/Better/Best)
- `pricing_recommended_annual`: Currency
- `pricing_tier_selected`: Text (Good/Better/Best)
- `pricing_final_annual`: Currency
- `pricing_discount_pct`: Number
- `pricing_discount_requested`: Boolean
- `pricing_presentation_format`: Enum (live_call, email, video, in_person)
- `pricing_reaction`: Enum (positive, neutral, pushback, silence, asked_for_discount)
- `pricing_days_to_acceptance`: Number
- `pricing_negotiation_rounds`: Number
- `pricing_presentation_score`: Number (0-100, from scoring fundamental)

### 3. Build the pricing funnel in PostHog

Using `posthog-funnels`, create a saved funnel:

`pricing_proposal_generated` -> `pricing_presented` -> `pricing_reaction_logged` -> `pricing_tier_selected` -> `pricing_accepted`

With breakdown by:
- `recommended_tier` (does Better/Best/Good recommendation affect acceptance?)
- `presentation_format` (do live calls close better than email proposals?)
- `value_recap_given` (does leading with value before price improve acceptance?)
- `discount_requested` (do discount requests correlate with eventual acceptance or rejection?)

Create a second funnel for loss analysis:
`pricing_presented` -> `pricing_rejected`
Breakdown by `rejection_reason` to identify the most common failure modes.

### 4. Build the n8n sync workflow

Using `n8n-workflow-basics` and `n8n-triggers`, create a bidirectional sync:

**Attio -> PostHog:** When a deal's `pricing_proposal_status` changes in Attio, fire the corresponding PostHog event with all deal properties. This handles cases where deal updates happen manually in the CRM.

**PostHog -> Attio:** When pricing events fire in PostHog (from agent workflows), update the deal record in Attio. Keep both systems in sync.

**Computed metrics:** After each `pricing_accepted` event, compute and store:
- `days_to_acceptance` = days between `pricing_presented` and `pricing_accepted`
- `discount_efficiency` = `pricing_discount_pct / pricing_negotiation_rounds` (discount per round -- lower is better)
- `tier_match_rate` = did the prospect select the recommended tier? (boolean)
- `value_anchor_effectiveness` = acceptance rate when `value_recap_given = true` vs false

### 5. Create the pricing performance dashboard

Using `posthog-dashboards`, create a dashboard with:
- Pricing acceptance rate (accepted / presented) -- weekly trend
- Average discount percentage -- weekly trend
- Tier distribution (Good/Better/Best selected) -- pie chart
- Tier match rate (recommended vs selected) -- percentage
- Average days to acceptance -- weekly trend
- Discount request rate -- weekly trend
- Acceptance rate by presentation format -- bar chart
- Acceptance rate with vs without value recap -- comparison
- Top rejection reasons -- ranked bar chart

## Output

- Full event schema for pricing presentation lifecycle
- Attio custom attributes for deal-level pricing tracking
- PostHog funnels for pricing win/loss analysis
- Bidirectional n8n sync between Attio and PostHog
- Dashboard insights for pricing presentation performance

## Triggers

Event schema is set up once. Events fire in real-time as pricing conversations progress. Dashboard updates continuously. Run the setup steps before the first pricing proposal is generated.
