---
name: budget-follow-up-sequence
description: Automated multi-touch follow-up sequence triggered after a budget objection, delivering budget navigation assets timed to root cause and budget cycle
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

# Budget Follow-Up Sequence

This drill builds and runs automated follow-up sequences that fire after a budget objection is logged on a deal. Each sequence is matched to the budget objection's root cause and timed to the prospect's budget cycle. Unlike price objection follow-ups (which deliver value proof), budget follow-ups deliver actionable materials that help the prospect navigate internal procurement.

## Input

- Deal in Attio with `budget_objection_handled` event logged (from `budget-objection-response` drill)
- Budget objection root cause classification
- Budget navigation framework used in initial response
- Objection outcome: `partially_resolved` or `unresolved` (do not send follow-ups for `resolved` objections)

## Steps

### 1. Build the n8n trigger workflow

Create an n8n workflow triggered by an Attio webhook. The webhook fires when a deal's `budget_objection_outcome` field is set to `partially_resolved` or `unresolved`.

Using `n8n-triggers`, configure:
```json
{
  "trigger": "attio_webhook",
  "event": "record.updated",
  "filter": {
    "object": "deals",
    "attribute": "budget_objection_outcome",
    "value_in": ["partially_resolved", "unresolved"]
  }
}
```

### 2. Select the follow-up sequence by root cause

Route to a different sequence based on `budget_objection_root_cause`:

**no_allocated_budget sequence (5 touches over 21 days):**
- Day 1: Email with 2-3 creative payment structures (phased rollout, pilot-to-full, ramp pricing). Subject: "A few ways to make this work within your current budget."
- Day 5: Budget justification memo — a one-page document written from the champion's perspective that they can forward to the budget holder. Includes pain quantification, ROI, and proposed payment structure.
- Day 10: "Cost of inaction" analysis using the prospect's own pain data. Show what each month of delay costs.
- Day 15: Case study of a similar company that found budget through cost center reallocation or tool consolidation.
- Day 21: Direct ask: "Has anything changed on the budget front? Happy to explore any creative structure that works for your team."

**budget_exhausted sequence (4 touches over 30 days, timed to budget cycle):**
- Day 1: Confirm the deferred start option with pricing lock. Subject: "Locking in your rate for {next_fiscal_start}."
- Day 14: Budget planning primer — when budget planning starts, what the champion should include in their request, and how to position the ask.
- Day 21: Offer to draft the budget request: "I can prepare a one-page budget justification you can drop into your planning process. Would that be helpful?"
- Day 30 (or 30 days before next fiscal year, whichever is sooner): Check-in on budget status. Offer to join a call with the budget holder.

**wrong_budget_owner sequence (3 touches over 10 days):**
- Day 1: Send the champion a pre-written email they can forward to the actual budget owner, introducing the project and requesting a 15-minute call.
- Day 4: One-page executive briefing customized for the budget owner's role. Focus on their priorities (cost savings, efficiency, competitive advantage) — not the champion's priorities.
- Day 10: If no progress, propose a three-way meeting: champion + budget owner + seller. Frame it as "a quick alignment call to answer any questions."

**competing_priorities sequence (5 touches over 14 days):**
- Day 1: Comparative business case showing this initiative's ROI vs the competing priority. If the competing priority's ROI is unknown, show this initiative's ROI in absolute terms.
- Day 3: Case study of a company that ran both initiatives in parallel (or replaced the competing initiative with your solution).
- Day 7: Phased rollout proposal showing how to start small without impacting the competing priority's budget.
- Day 10: "What if we could run alongside {competing_initiative}?" — propose a minimal pilot that doesn't cannibalize the other project's budget.
- Day 14: Direct ask: "Is the priority decision still open, or has {competing_initiative} been locked in?"

**procurement_friction sequence (4 touches over 14 days):**
- Day 1: Ask: "What does your procurement process require? I'll get everything ready so we don't slow things down." Offer to complete security questionnaires, vendor qualification forms, and compliance documentation proactively.
- Day 3: Send all requested procurement materials (or a standard package if the prospect hasn't responded: SOC 2, security policy, DPA, vendor information sheet).
- Day 7: Status check: "Has our vendor qualification been submitted? Is there anything else the procurement team needs from us?"
- Day 14: If still blocked, propose a structure that bypasses procurement: monthly billing under approval thresholds, or a free pilot that doesn't require procurement.

### 3. Create the sequences in Instantly or Loops

For cold/warm prospects (not yet customers), use Instantly via `instantly-campaign`:
- Create a campaign per root cause with the touch sequence above
- Set up tracking links on all assets using `instantly-tracking`
- Enable reply detection to pause the sequence on any response

For existing relationships or warmer contacts, use Loops via `loops-sequences`:
- Create a transactional sequence per root cause
- Personalize with deal-specific merge fields from Attio
- Track opens and link clicks

### 4. Attach budget navigation assets to each touch

For each email that references an asset:
- Budget justification memo: generate from the deal's pain data using `budget-navigation-response` output
- Payment structure options: pull from `payment-structure-generation` output
- Cost-of-inaction analysis: calculate from quantified pains (annual pain cost * months of delay / 12)
- Comparative business case: build from ROI data and competitive intelligence
- Case study: match by industry + company size + budget objection type

### 5. Track engagement

Using `posthog-custom-events`, fire events for each touch:
```json
{
  "event": "budget_follow_up_sent",
  "properties": {
    "deal_id": "...",
    "root_cause": "no_allocated_budget",
    "touch_number": 1,
    "asset_type": "payment_structures",
    "channel": "email"
  }
}
```

Track asset engagement:
```json
{
  "event": "budget_asset_engaged",
  "properties": {
    "deal_id": "...",
    "asset_type": "budget_justification_memo",
    "engagement_type": "opened|forwarded|downloaded"
  }
}
```

### 6. Handle responses and exits

Using `n8n-workflow-basics`, build response handling:
- **Prospect replies positively (budget found/approved):** Pause the sequence. Update `budget_objection_outcome` to `resolved`. Route to next deal stage.
- **Prospect replies with new information (different budget owner, different timeline):** Pause. Re-classify the budget objection with the new info. Re-enter the `budget-objection-response` drill.
- **Prospect forwards the justification memo (detected via Attio activity):** Fire `budget_asset_forwarded` event. This is a strong signal — the champion is working internally.
- **Prospect goes silent after full sequence:** Mark deal as `budget_stalled`. Set a reminder for 2 weeks before the next budget cycle.
- **Prospect replies "not happening":** Pause. Update deal status. Set a nurture for next budget cycle — do NOT close-lost immediately for genuine budget constraints.

## Output

- Root-cause-specific follow-up sequence running automatically after each unresolved budget objection
- Budget navigation assets delivered at optimal timing relative to budget cycles
- Engagement tracking on every touch and asset
- Automatic exit and routing based on prospect response
- Budget cycle-aware timing for nurture sequences

## Triggers

Triggered automatically by n8n webhook when a deal's `budget_objection_outcome` is set to `partially_resolved` or `unresolved`. The sequence pauses on any reply.
