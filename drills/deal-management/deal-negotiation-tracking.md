---
name: deal-negotiation-tracking
description: Instrument multi-year deal negotiation events in PostHog and Attio — track proposals sent, concessions made, terms accepted/rejected, and close outcomes
category: Deal Management
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-funnels
  - attio-deals
  - attio-custom-attributes
  - n8n-workflow-basics
  - n8n-triggers
---

# Deal Negotiation Tracking

This drill instruments the full multi-year deal negotiation lifecycle so every proposal, counter-offer, concession, and outcome is tracked. The data feeds the threshold engine at Smoke/Baseline and the autonomous optimization loop at Durable.

## Input

- PostHog project with API access
- Attio CRM with deals pipeline
- n8n instance for webhook-based event capture
- At least 1 deal in active multi-year negotiation

## Steps

### 1. Define the negotiation event schema

Using `posthog-custom-events`, create the following events:

| Event | When to Fire | Key Properties |
|-------|-------------|----------------|
| `multiyear_proposal_generated` | Agent generates deal term options | `deal_id`, `options_count`, `target_tcv`, `max_discount_pct`, `term_years_target` |
| `multiyear_proposal_sent` | Comparison doc or proposal delivered to prospect | `deal_id`, `delivery_channel` (email/call/in_person), `options_presented`, `anchor_option_tcv` |
| `multiyear_counter_received` | Prospect responds with counter-terms | `deal_id`, `requested_discount_pct`, `requested_term_years`, `requested_payment_schedule`, `counter_type` (discount/term/payment/scope) |
| `multiyear_concession_made` | Seller adjusts terms in response to counter | `deal_id`, `concession_type`, `concession_value`, `concession_number` (1st, 2nd, 3rd), `remaining_to_floor` |
| `multiyear_deal_closed_won` | Multi-year deal signed | `deal_id`, `final_term_years`, `final_annual_price`, `final_tcv`, `final_discount_pct`, `payment_schedule`, `incentives_included`, `negotiation_rounds`, `days_to_close` |
| `multiyear_deal_closed_lost` | Multi-year negotiation fails | `deal_id`, `lost_reason` (reverted_to_annual/competitor/no_decision/budget/timing), `best_offer_tcv`, `negotiation_rounds` |
| `multiyear_deal_reverted_annual` | Prospect chose annual instead of multi-year | `deal_id`, `annual_acv`, `foregone_tcv`, `revert_reason` |

### 2. Set up Attio custom attributes

Using `attio-custom-attributes`, add these fields to the Deal object:

- `multi_year_status`: Enum (not_proposed, proposed, negotiating, closed_won, closed_lost, reverted_annual)
- `proposed_term_years`: Number
- `proposed_discount_pct`: Number
- `final_term_years`: Number
- `final_discount_pct`: Number
- `final_tcv`: Currency
- `negotiation_rounds`: Number
- `concessions_made`: Number
- `days_in_negotiation`: Number
- `anchor_to_close_ratio`: Number (final TCV / initial anchor TCV — measures how much you gave away)

### 3. Build the negotiation funnel in PostHog

Using `posthog-funnels`, create a saved funnel:

`multiyear_proposal_generated` -> `multiyear_proposal_sent` -> `multiyear_counter_received` -> `multiyear_deal_closed_won`

With breakdown by:
- `term_years_target` (do 2-year or 3-year proposals win more?)
- `delivery_channel` (does presenting in-person close better than email?)
- `concession_number` (how many rounds of negotiation is typical?)

Create a second funnel for loss analysis:
`multiyear_proposal_sent` -> `multiyear_deal_closed_lost`
Breakdown by `lost_reason` to identify the most common failure modes.

### 4. Build the n8n sync workflow

Using `n8n-workflow-basics` and `n8n-triggers`, create a bidirectional sync:

**Attio -> PostHog:** When a deal's `multi_year_status` changes in Attio, fire the corresponding PostHog event with all deal properties. This handles cases where deal updates happen manually in the CRM.

**PostHog -> Attio:** When negotiation events fire in PostHog (e.g., from an agent workflow), update the deal record in Attio. Keep both systems in sync.

**Computed metrics:** After each `multiyear_deal_closed_won` event, compute and store:
- `anchor_to_close_ratio` = `final_tcv / anchor_option_tcv`
- `days_in_negotiation` = days between `proposal_sent` and `deal_closed`
- `discount_efficiency` = `final_discount_pct / negotiation_rounds` (discount given per round — lower is better)

### 5. Create the negotiation summary view

Using `posthog-funnels`, create a dashboard insight showing:
- Multi-year proposal rate (proposals generated / total deals at Proposed stage)
- Multi-year close rate (closed won / proposals sent)
- Average TCV for multi-year deals
- Average discount given
- Average negotiation duration (days)
- Anchor-to-close ratio distribution
- Win rate by term length (2-year vs 3-year)

## Output

- Full event schema for multi-year negotiation lifecycle
- Attio custom attributes for deal-level negotiation tracking
- PostHog funnels for win/loss analysis
- Bidirectional n8n sync between Attio and PostHog
- Dashboard insights for negotiation performance

## Triggers

Event schema is set up once. Events fire in real-time as negotiation progresses. Dashboard updates continuously. Run the setup steps before the first multi-year proposal is sent.
