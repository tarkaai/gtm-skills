---
name: timing-objection-follow-up-sequence
description: Automated multi-touch follow-up sequence triggered after a timing objection, delivering urgency assets and cost-of-delay content timed to the objection root cause
category: Competitive
tools:
  - Attio
  - n8n
  - Instantly
  - Loops
  - PostHog
fundamentals:
  - attio-deals
  - attio-notes
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-scheduling
  - instantly-campaign
  - instantly-tracking
  - loops-sequences
  - posthog-custom-events
  - cost-of-delay-calculation
---

# Timing Objection Follow-Up Sequence

This drill builds and runs automated follow-up sequences that fire after a timing objection is logged on a deal. Each sequence delivers root-cause-specific content designed to either create legitimate urgency, maintain engagement until reengagement, or surface the real objection behind the timing smokescreen.

## Input

- Deal in Attio with `timing_objection_handled` event logged (from `timing-objection-response` drill)
- Timing objection root cause classification
- Strategy used in initial response
- Objection outcome: `partially_resolved`, `unresolved`, or `reengagement_scheduled` (do not send follow-ups for `timeline_accelerated` or `bridging_accepted`)

## Steps

### 1. Build the n8n trigger workflow

Create an n8n workflow triggered by an Attio webhook. The webhook fires when a deal's `timing_objection_outcome` field is set to `partially_resolved`, `unresolved`, or `reengagement_scheduled`.

Using `n8n-triggers`, configure:
```json
{
  "trigger": "attio_webhook",
  "event": "record.updated",
  "filter": {
    "object": "deals",
    "attribute": "timing_objection_outcome",
    "value_in": ["partially_resolved", "unresolved", "reengagement_scheduled"]
  }
}
```

### 2. Select the follow-up sequence by root cause

Route to a different sequence based on `timing_objection_root_cause`:

**competing_priority sequence (4 touches over 21 days):**
- Day 1: Cost-of-delay email — "While you focus on {competing_project}, here's what the delay costs: ${monthly_cost}/month in {pain_category}"
- Day 7: Case study showing a company in a similar situation that ran both projects in parallel with minimal overhead
- Day 14: Industry news or data point relevant to their pain — reinforce that the problem is growing
- Day 21: Direct check-in: "Has the priority picture shifted? Happy to discuss a phased approach that requires minimal bandwidth from your team."

**no_urgency sequence (5 touches over 30 days):**
- Day 1: Cost-of-delay analysis document (generated via `cost-of-delay-calculation`) with cumulative 6-month and 12-month costs
- Day 7: "Cost of doing nothing" case study — a company that waited and what happened
- Day 14: Share a relevant trigger event — regulatory change, competitor move, seasonal deadline that creates natural urgency
- Day 21: Offer a free assessment or audit that quantifies their pain more precisely — creates engagement without purchase commitment
- Day 30: Final check-in with an offer: "Lock current pricing now, start whenever you're ready"

**budget_cycle sequence (3 touches over period matching their budget cycle):**
- Immediately: Confirm the budget timeline and set a calendar reminder for 30 days before their budget window opens
- 60 days before budget opens: Send a pre-built business case document the champion can submit during budget planning
- 30 days before budget opens: Schedule a call to finalize scope and pricing so they can move quickly when budget is available

**organizational_change sequence (3 touches over 60 days):**
- Day 7: Send a brief value summary document — useful if the champion needs to brief a new stakeholder
- Day 30: Check-in: "How is the transition going? Happy to re-brief any new stakeholders."
- Day 60: Offer a fresh discovery call if the org structure has changed significantly

**risk_aversion sequence (4 touches over 14 days):**
- Day 1: Pilot proposal — detailed scope, timeline, and success criteria for a low-risk proof of concept
- Day 3: Reference customer who started with a similar pilot and expanded
- Day 7: Offer to connect them with a reference customer in the same industry
- Day 14: Direct ask: "What would you need to see to feel confident moving forward?"

**smokescreen sequences (for smokescreen_budget, smokescreen_authority, smokescreen_fit — 3 touches over 10 days):**
- Day 1: Acknowledge the timing concern, then ask a direct diagnostic question targeting the suspected real objection
- Day 5: Share content that addresses the real concern (pricing FAQ for budget, executive summary for authority, feature comparison for fit)
- Day 10: Direct: "I want to make sure timing is truly the blocker. Is there anything else holding this back?"

**genuine_constraint / reengagement_scheduled sequence (2-3 touches, timed to reengagement date):**
- Immediately: Confirm the reengagement date in writing, lock pricing if applicable
- Midpoint between now and reengagement date: Share relevant industry update or product improvement to maintain mindshare
- 7 days before reengagement date: Reach out to schedule the reengagement call

### 3. Create the sequences in Instantly or Loops

For deals where the prospect is not yet a customer, use Instantly via `instantly-campaign`:
- Create a campaign per root cause with the touch sequence above
- Set up tracking links on all assets using `instantly-tracking`
- Enable reply detection to pause the sequence if the prospect responds

For existing relationships or warmer contacts, use Loops via `loops-sequences`:
- Create a transactional sequence per root cause
- Personalize with deal-specific merge fields from Attio
- Track opens and link clicks

### 4. Attach urgency assets to each touch

For each email that references an asset:
- **Cost-of-delay analysis**: Generate using `cost-of-delay-calculation` with the prospect's pain data
- **Business case / budget justification**: Generate using their pain data and ROI model
- **Pilot proposal**: Template with prospect-specific scope and success criteria
- **Case study**: Match by industry, company size, and similar timing situation
- **Industry data/news**: Relevant recent developments that create urgency

### 5. Track engagement

Using `posthog-custom-events`, fire events for each touch:
```json
{
  "event": "timing_follow_up_sent",
  "properties": {
    "deal_id": "...",
    "root_cause": "no_urgency",
    "touch_number": 1,
    "asset_type": "cost_of_delay_analysis",
    "channel": "email"
  }
}
```

Track opens, clicks, and replies. If the prospect opens the cost-of-delay analysis or pilot proposal:
```json
{
  "event": "timing_asset_engaged",
  "properties": {
    "deal_id": "...",
    "asset_type": "cost_of_delay_analysis",
    "engagement_type": "opened"
  }
}
```

### 6. Handle responses and exits

Using `n8n-workflow-basics`, build response handling:
- **Prospect replies with timeline acceleration**: Pause the sequence. Update `timing_objection_outcome` to `timeline_accelerated` in Attio. Schedule next meeting.
- **Prospect accepts bridging solution**: Pause the sequence. Update to `bridging_accepted`. Begin pilot/phase 1 process.
- **Prospect reveals the real objection**: Pause the sequence. Re-classify and route to the appropriate objection handling play (e.g., price objection, fit objection).
- **Prospect confirms reengagement date**: Pause the sequence. Set Attio reminder for reengagement. Switch to the `reengagement_scheduled` sequence.
- **Prospect goes silent after full sequence**: Mark deal as stalled. Set a 60-day reengagement reminder in Attio.
- **Prospect replies "not interested"**: Pause the sequence. Update deal status to "Closed Lost" with reason "Timing". Log in PostHog.

## Output

- Root-cause-specific follow-up sequence running automatically after each unresolved timing objection
- Urgency assets (cost-of-delay, pilot proposals, case studies) delivered at optimal timing
- Engagement tracking on every touch and asset
- Automatic exit and routing based on prospect response
- Reengagement scheduling for genuine constraint deals

## Triggers

Triggered automatically by n8n webhook when a deal's `timing_objection_outcome` is set to `partially_resolved`, `unresolved`, or `reengagement_scheduled`. The sequence pauses on any reply.
