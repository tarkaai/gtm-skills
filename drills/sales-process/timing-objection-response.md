---
name: timing-objection-response
description: Classify a timing objection by root cause, determine if genuine or smokescreen, generate a strategy-matched response, and deliver it with appropriate follow-up assets
category: Competitive
tools:
  - Attio
  - Anthropic
  - PostHog
fundamentals:
  - call-transcript-timing-extraction
  - cost-of-delay-calculation
  - timing-response-generation
  - pain-quantification-prompt
  - attio-deals
  - attio-notes
  - posthog-custom-events
---

# Timing Objection Response

This drill handles a single timing objection end-to-end: classify the root cause, determine whether the objection is genuine or masking a deeper concern, generate a strategy-matched response, and log the outcome. It is the timing-objection analog of `price-objection-response`.

## Input

- A deal in Attio where the prospect has raised a timing objection ("not the right time", "maybe next quarter", "we're focused on other things")
- The objection text (from call transcript via `call-transcript-timing-extraction`, email, or manual CRM note)
- Deal context from Attio: pain data, timeline, stakeholders, competitor status

## Steps

### 1. Gather deal context from Attio

Query the deal record using `attio-deals` to pull:
- `deal_value`
- `total_quantified_pain` (from discovery)
- `pain_to_price_ratio`
- `timeline_category` (from `timing-scorecard-setup`)
- `urgency_drivers` (from previous timing qualification)
- `champion_name`, `champion_title`
- `economic_buyer_engaged` (boolean)
- `competitor_status`
- `stakeholder_count`

If `total_quantified_pain` is missing, flag the deal: "Pain not quantified. Run `pain-quantification-prompt` before responding to timing objection — cost-of-delay analysis requires dollar figures."

### 2. Classify the timing objection

Run `call-transcript-timing-extraction` with the objection text and deal context. Receive:
- Root cause (one of 9 categories)
- Real constraint vs smokescreen determination
- Confidence score
- Recommended response strategy
- Diagnostic questions
- Urgency levers
- Reengagement trigger and timeline

If `confidence < 5`: do NOT proceed to response generation. Instead, recommend the agent or seller ask the diagnostic questions on the next call to confirm the root cause. Log in Attio and exit.

### 3. Generate cost-of-delay analysis (if applicable)

If `root_cause` is `no_urgency`, `competing_priority`, or `budget_cycle`, run `cost-of-delay-calculation` with the deal's pain data and stated delay duration.

This produces:
- Monthly and cumulative cost-of-delay figures
- Champion-ready talking point
- Email version ready to send

If `root_cause` is a smokescreen type, skip cost-of-delay — the response strategy addresses the underlying concern instead.

### 4. Generate the response

Based on the `recommended_strategy`, generate the appropriate response:

**urgency_creation** (for `no_urgency`):
- Lead with cost-of-delay headline: "Every month of delay costs you approximately $X"
- Present 2-3 urgency levers specific to their situation
- Propose a concrete next step with a date

**cost_of_delay** (for `competing_priority`):
- Acknowledge the competing priority
- Present comparison: "The project you're prioritizing costs you $X/month in this area while you wait"
- Offer to run in parallel with minimal time investment

**bridging_solution** (for `risk_aversion`):
- Propose a phased approach: pilot program, limited rollout, or proof-of-concept
- Define clear success criteria for the bridge phase
- Set a decision date at the end of the bridge period

**phased_approach** (for `risk_aversion` or `budget_cycle`):
- Break the full implementation into phases
- Phase 1: solve the most painful problem with minimal scope
- Future phases: expand based on Phase 1 results

**deferred_start** (for `budget_cycle` or `genuine_constraint`):
- Lock current pricing with a signed agreement
- Set implementation start date aligned with their constraint
- Maintain engagement during the wait period

**executive_alignment** (for `smokescreen_authority`):
- Request a meeting with the decision maker
- Provide the champion with a one-page executive summary
- Frame the ask as helping the champion, not going around them

**reframe_to_pain** (for `smokescreen_budget`, `smokescreen_fit`, `competing_priority`):
- Redirect to their stated pain: "You mentioned {pain_quote}. Is that still happening?"
- Ask the diagnostic questions to surface the real blocker
- Do not accept "timing" at face value

**strategic_patience** (for `organizational_change`, `genuine_constraint`):
- Acknowledge the reality of their situation
- Set a specific reengagement date (not "let's circle back sometime")
- Provide value during the wait: relevant content, industry insights, introductions

### 5. Log the response in Attio and PostHog

Create an Attio note on the deal using `attio-notes`:
```json
{
  "title": "Timing Objection Response — {date}",
  "content": "Root cause: {root_cause}\nReal constraint: {is_real_constraint}\nStrategy: {recommended_strategy}\nResponse delivered: {response_summary}\nCost of delay: ${monthly_cost}/mo\nReengagement trigger: {trigger}\nNext step: {next_step}"
}
```

Update deal attributes:
- `timing_objection_root_cause`: the classified root cause
- `timing_objection_strategy`: the strategy used
- `timing_objection_date`: today
- `timing_objection_outcome`: initially `pending` (updated later when outcome is known)

Fire PostHog event using `posthog-custom-events`:
```json
{
  "event": "timing_objection_handled",
  "properties": {
    "deal_id": "...",
    "root_cause": "competing_priority",
    "is_real_constraint": false,
    "confidence": 7,
    "strategy_used": "cost_of_delay",
    "cost_of_delay_monthly": 15000,
    "cost_of_delay_presented": true,
    "diagnostic_questions_asked": true
  }
}
```

### 6. Deliver the response

**Human action required:** Review the generated response and cost-of-delay analysis. Adjust for your voice and relationship context. Deliver on the next call or via follow-up email.

After delivery, update `timing_objection_outcome` in Attio to one of:
- `timeline_accelerated` — prospect agreed to move forward sooner
- `bridging_accepted` — prospect accepted a pilot or phased approach
- `reengagement_scheduled` — concrete date set for future reengagement
- `partially_resolved` — progress made but no commitment yet
- `unresolved` — no change in timeline
- `deal_lost` — prospect disengaged entirely

## Output

- Classified timing objection with root cause and confidence
- Strategy-matched response ready for delivery
- Cost-of-delay analysis (when applicable)
- CRM notes and PostHog events logged
- Clear next step defined

## Triggers

Manual trigger: run when a timing objection is identified on a deal. At Scalable level, triggered automatically by `timing-detection-automation`.
