---
name: pricing-presentation-framework-baseline
description: >
  Pricing Presentation Framework — Baseline Run. Always-on pricing proposal
  generation for every deal entering Proposed stage, with outcome tracking,
  presentation scoring, and objection handling workflows running continuously.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "Pricing presented on >=80% of deals entering Proposed over 2 weeks with >=65% acceptance and average discount <=12%"
kpis: ["Pricing acceptance rate", "Average discount percentage", "Tier match rate", "Days to acceptance"]
slug: "pricing-presentation-framework"
install: "npx gtm-skills add sales/proposed/pricing-presentation-framework"
drills:
  - pricing-proposal-assembly
  - pricing-outcome-tracking
  - price-objection-response
  - threshold-engine
---

# Pricing Presentation Framework — Baseline Run

> **Stage:** Sales > Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Move from manual pricing proposal assembly (Smoke) to always-on instrumented pricing workflow. Every deal entering Proposed stage gets a generated pricing proposal within 24 hours. Every pricing conversation is tracked, scored, and analyzed. Objections are handled with data-backed response frameworks. Target: pricing presented on >=80% of qualifying deals over 2 weeks with >=65% acceptance rate and average discount <=12%.

## Leading Indicators

- Pricing proposal generated within 24 hours for >=80% of deals entering Proposed stage
- PostHog pricing event schema capturing all presentation lifecycle events
- Pricing presentation score (from `pricing-presentation-scoring`) averaging >=60/100
- Discount request rate declining week-over-week
- Tier match rate (prospect selects recommended tier) >=50%
- Average days from presentation to decision <=10

## Instructions

### 1. Set up pricing outcome tracking

Run the `pricing-outcome-tracking` drill to instrument the full pricing lifecycle:

1. Configure the PostHog event schema: `pricing_proposal_generated`, `pricing_presented`, `pricing_reaction_logged`, `pricing_discount_requested`, `pricing_discount_given`, `pricing_tier_selected`, `pricing_accepted`, `pricing_rejected`
2. Add Attio custom attributes to the Deal object: `pricing_proposal_status`, `pricing_tiers_presented`, `pricing_recommended_tier`, `pricing_tier_selected`, `pricing_discount_pct`, `pricing_reaction`, `pricing_days_to_acceptance`, `pricing_presentation_score`
3. Build the PostHog pricing funnel: `proposal_generated` -> `presented` -> `reaction_logged` -> `tier_selected` -> `accepted`
4. Create the bidirectional n8n sync (Attio <-> PostHog) for pricing events
5. Build the pricing performance dashboard with acceptance rate trends, discount analysis, tier distribution, and format comparison

This tracking runs continuously from this point forward.

### 2. Generate pricing proposals for all qualifying deals

Run the `pricing-proposal-assembly` drill for every deal that enters Proposed stage with qualifying pain data (`pain_count >= 2`, `pain_quantification_rate >= 0.5`). At Baseline, this is still agent-assisted — the agent generates the proposal, the seller reviews and presents.

For each deal:
1. Pull deal context and pain data from Attio
2. Validate pain-to-price ratio (flag deals below 3x for additional discovery)
3. Generate Good/Better/Best tier structure via `pricing-tier-generation`
4. Build proposal artifact (pricing comparison + value anchoring script)
5. Store in Attio and fire `pricing_proposal_generated` in PostHog
6. Notify the seller via Slack: "Pricing proposal ready for {company}. Recommended: {tier} at ${price}/year. ROI: {roi}%. Review and present: {link}"

Target: <=24 hours from deal entering Proposed to proposal generated.

### 3. Build the objection handling workflow

Run the `price-objection-response` drill for every pricing objection that arises:

1. When a prospect pushes back on price (detected from `pricing_reaction = pushback` or `pricing_discount_requested = true`), extract and classify the objection
2. Validate pain-to-price ratio — if <3x, recommend re-running discovery before responding to the price objection
3. Generate a tailored response using the highest-win-rate framework for this objection type
4. **Human action required:** Review the generated response and deliver it on the next call or via email
5. Log the outcome in Attio and PostHog: `price_objection_handled` with root cause, framework used, and resolution

Build a reference document in Attio capturing the most common objection types and their highest-performing responses. This becomes the pricing playbook.

### 4. Score every pricing presentation

After each pricing conversation, run `pricing-presentation-scoring` to evaluate seller effectiveness:

1. Score across 4 dimensions: value anchoring (25pts), tier presentation (25pts), discount discipline (25pts), close progression (25pts)
2. Tag the presentation pattern: `value_led_success`, `discount_leak`, `premature_price_reveal`, `strong_anchor_weak_close`, `objection_fumble`, or `textbook_execution`
3. Store the score and pattern in Attio on the deal record
4. Fire `pricing_presentation_scored` in PostHog

Use the scores to identify coaching opportunities. If a seller consistently scores low on value anchoring (presenting price before recapping value), address that specific behavior.

### 5. Monitor and evaluate over 2 weeks

Let the instrumented workflow run for 2 full weeks. Check the PostHog dashboard daily for:
- How many proposals were generated vs how many deals entered Proposed (coverage rate)
- Acceptance rate trend (target: >=65%)
- Average discount percentage (target: <=12%)
- Tier match rate (target: >=50%)
- Days to acceptance (target: <=10)

Run the `threshold-engine` drill at the end of 2 weeks:
- Coverage: pricing presented on >=80% of qualifying deals
- Acceptance: >=65% accepted or advancing
- Discount discipline: average discount <=12%

If PASS: document the pricing playbook (best presentation format, most effective value anchors, top objection responses) and proceed to Scalable.

If FAIL: diagnose using the pricing dashboard:
- Low coverage: proposal generation is bottlenecked. Check if deals lack pain data (fix discovery) or if agent latency is too high.
- Low acceptance: review presentation scores. If value anchoring scores are low, the problem is framing. If tier presentation scores are low, the tier structure needs adjustment.
- High discount: review objection handling. If sellers are discounting before using response frameworks, it's a discipline issue. If response frameworks aren't working, the value story is weak.

## Time Estimate

- 3 hours: setting up pricing-outcome-tracking (events, attributes, funnels, dashboard)
- 6 hours: generating and reviewing pricing proposals across all qualifying deals (ongoing over 2 weeks)
- 4 hours: handling objections and scoring presentations (ongoing over 2 weeks)
- 3 hours: threshold evaluation, playbook documentation, and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal records, pricing attributes, proposal storage, playbook | Standard stack (excluded from play budget) |
| PostHog | Pricing event tracking, funnels, dashboard | Standard stack (excluded from play budget) |
| n8n | Bidirectional sync between Attio and PostHog, Slack notifications | Standard stack (excluded from play budget) |
| Anthropic Claude API | Tier generation, presentation scoring, objection responses | ~$5-15/mo for 20-30 deals at Sonnet 4.6 rates ($3/$15 per M tokens) — [pricing](https://platform.claude.com/docs/en/about-claude/pricing) |

**Play-specific cost:** ~$5-15/month (Claude API for proposal generation and scoring)

## Drills Referenced

- `pricing-proposal-assembly` — generates Good/Better/Best proposals from deal pain data with value anchoring and discount guardrails
- `pricing-outcome-tracking` — instruments the full pricing lifecycle in PostHog and Attio with funnels and dashboards
- `price-objection-response` — diagnoses objection root cause, selects response framework, generates tailored response, and logs outcome
- `threshold-engine` — evaluates pass/fail against >=80% coverage / >=65% acceptance / <=12% discount targets
