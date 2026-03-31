---
name: objection-follow-up-sequence
description: Automated multi-touch follow-up sequence triggered after a price objection, delivering value assets timed to objection root cause
category: Sales
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
---

# Objection Follow-Up Sequence

This drill builds and runs an automated follow-up sequence that fires after a price objection is logged on a deal. Instead of generic follow-ups, each touch delivers a specific value asset matched to the objection's root cause, timed to maintain momentum without overwhelming the prospect.

## Input

- Deal in Attio with `price_objection_handled` event logged (from `price-objection-response` drill)
- Objection root cause classification
- Response framework used in initial response
- Objection outcome: `partially_resolved` or `unresolved` (do not send follow-ups for `resolved` objections)

## Steps

### 1. Build the n8n trigger workflow

Create an n8n workflow triggered by an Attio webhook. The webhook fires when a deal's `objection_outcome` field is set to `partially_resolved` or `unresolved`.

Using `n8n-triggers`, configure:
```json
{
  "trigger": "attio_webhook",
  "event": "record.updated",
  "filter": {
    "object": "deals",
    "attribute": "objection_outcome",
    "value_in": ["partially_resolved", "unresolved"]
  }
}
```

### 2. Select the follow-up sequence by root cause

Route to a different sequence based on `primary_objection_root_cause`:

**no_budget sequence (5 touches over 14 days):**
- Day 1: Follow-up email with payment flexibility options (quarterly, monthly, deferred start)
- Day 3: Case study showing similar company that started with a smaller scope and expanded
- Day 7: ROI calculator pre-filled with their pain data showing payback period
- Day 10: Champion enablement email with budget justification template
- Day 14: Direct ask: "Is budget the blocker or is there something else?"

**value_gap sequence (4 touches over 10 days):**
- Day 1: Business case document generated from their pain data (trigger `pain-based-business-case` drill)
- Day 3: Case study from same industry showing quantified ROI
- Day 7: "Cost of doing nothing" analysis using their own pain numbers
- Day 10: Offer a live ROI walkthrough meeting

**competitor_comparison sequence (4 touches over 10 days):**
- Day 1: TCO comparison showing total cost of ownership including implementation, training, ongoing maintenance
- Day 3: Feature comparison focused on capabilities the competitor lacks that map to their stated pains
- Day 7: Customer story of a company that switched from the competitor
- Day 10: Offer a technical deep-dive to address any feature concerns

**sticker_shock sequence (3 touches over 7 days):**
- Day 1: Re-anchor email: "Here's what {strongest_pain} is costing you today: ${annual_cost}. Our solution costs ${deal_value}. That's ${ratio}x return."
- Day 3: Breakdown of pricing by feature/module — show where the value concentrates
- Day 7: Offer a scoped pilot at reduced price to prove value before full commitment

**authority_gap sequence (4 touches over 10 days):**
- Day 1: Send champion a one-page executive summary they can forward to the decision maker
- Day 3: Offer to join a call with the decision maker to address budget concerns directly
- Day 7: Send the champion a budget justification email template pre-filled with their data
- Day 10: If no progress, request a direct introduction to the economic buyer

**timing sequence (3 touches over 14 days):**
- Day 1: Acknowledge timing concern. Share what a deferred start looks like (lock pricing now, begin implementation in Q+1).
- Day 7: Share a "cost of delay" analysis: each month of delay costs ${monthly_pain} in continued pain.
- Day 14: Gentle check-in on whether timing has shifted.

### 3. Create the sequences in Instantly or Loops

For cold/warm prospects (not yet customers), use Instantly via `instantly-campaign`:
- Create a campaign per root cause with the touch sequence above
- Set up tracking links on all assets using `instantly-tracking`
- Enable reply detection to pause the sequence if the prospect responds

For existing relationships or warmer contacts, use Loops via `loops-sequences`:
- Create a transactional sequence per root cause
- Personalize with deal-specific merge fields from Attio
- Track opens and link clicks

### 4. Attach value assets to each touch

For each email in the sequence that references an asset (ROI calculator, case study, TCO comparison):
- Pull the asset from your content library or generate it:
  - ROI calculator: pre-fill with the prospect's pain data from Attio
  - Business case: trigger `pain-based-business-case` drill
  - Case study: match by industry + company size from your case study library
  - TCO comparison: build from competitive intelligence data
- Attach or link the asset in the email

### 5. Track engagement

Using `posthog-custom-events`, fire events for each touch in the sequence:
```json
{
  "event": "objection_follow_up_sent",
  "properties": {
    "deal_id": "...",
    "root_cause": "value_gap",
    "touch_number": 1,
    "asset_type": "business_case",
    "channel": "email"
  }
}
```

Track opens, clicks, and replies. If the prospect opens the ROI calculator or business case, fire:
```json
{
  "event": "objection_asset_engaged",
  "properties": {
    "deal_id": "...",
    "asset_type": "roi_calculator",
    "engagement_type": "opened"
  }
}
```

### 6. Handle responses and exits

Using `n8n-workflow-basics`, build response handling:
- **Prospect replies positively:** Pause the sequence. Update `objection_outcome` to `resolved` in Attio. Route to next deal stage.
- **Prospect replies with a new objection:** Pause the sequence. Re-classify the objection and re-enter the `price-objection-response` drill.
- **Prospect goes silent after full sequence:** Mark deal as stalled. Set a 30-day re-engagement reminder in Attio.
- **Prospect replies "not interested":** Pause the sequence. Update deal status to "Closed Lost" with reason "Price". Log in PostHog.

## Output

- Root-cause-specific follow-up sequence running automatically after each unresolved price objection
- Value assets delivered at optimal timing
- Engagement tracking on every touch and asset
- Automatic exit and routing based on prospect response

## Triggers

Triggered automatically by n8n webhook when a deal's `objection_outcome` is set to `partially_resolved` or `unresolved`. The sequence pauses on any reply.
