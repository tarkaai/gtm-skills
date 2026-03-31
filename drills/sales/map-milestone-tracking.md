---
name: map-milestone-tracking
description: Monitor MAP milestone progress, detect delays, send automated updates to prospects, and escalate stalls
category: Sales
tools:
  - Attio
  - n8n
  - PostHog
  - Loops
fundamentals:
  - attio-deals
  - attio-custom-attributes
  - attio-notes
  - attio-reporting
  - n8n-workflow-basics
  - n8n-scheduling
  - n8n-crm-integration
  - n8n-email-integration
  - posthog-custom-events
---

# MAP Milestone Tracking

This drill creates the system that monitors Mutual Action Plan progress across all active deals, detects when milestones are delayed, sends automated progress updates to prospects, and escalates at-risk deals to the rep.

## Input

- Active MAPs stored in Attio (created by `map-auto-generation` or `map-template-creation`)
- n8n instance for scheduled workflows
- PostHog for event tracking

## Steps

### 1. Set up milestone tracking events in PostHog

Using `posthog-custom-events`, define MAP-specific events:

| Event | Properties | Fires When |
|-------|-----------|------------|
| `map_created` | deal_id, deal_type, milestone_count, expected_close | MAP is generated and activated |
| `map_milestone_completed` | deal_id, milestone_name, milestone_owner, days_early_late, completion_method | A milestone is marked done |
| `map_milestone_overdue` | deal_id, milestone_name, milestone_owner, days_overdue, escalation_level | Milestone passes its due date |
| `map_update_sent` | deal_id, update_type (weekly/milestone/escalation), recipient | Progress email sent to prospect |
| `map_stall_detected` | deal_id, stall_reason, consecutive_overdue_count | Multiple milestones delayed |
| `map_completed` | deal_id, total_days, on_time_pct, final_outcome (won/lost) | All milestones done or deal closed |

### 2. Build the daily milestone checker (n8n cron)

Using `n8n-scheduling`, create a workflow that runs daily at 9 AM:

**Step 1 — Query all active MAPs:**
Using `attio-deals`, query all deals where `map_status` = "Active". For each deal, read the MAP note to extract milestone data.

**Step 2 — Check each milestone against its due date:**
For each active MAP:
- Parse milestone dates from the Attio note
- Compare today's date against each upcoming milestone
- Classify:
  - **On track:** Next milestone due date is in the future, no overdue milestones
  - **At risk:** Next milestone due within 2 days and no completion signal
  - **Overdue:** A milestone's due date has passed without completion
  - **Stalled:** 2+ consecutive milestones are overdue

**Step 3 — Update Attio attributes:**
Using `attio-custom-attributes`, update deal records:
- `map_completion_pct` = (completed milestones / total milestones) x 100
- `map_at_risk` = true if any milestone overdue
- `map_stall_count` = number of overdue milestones

**Step 4 — Fire PostHog events:**
For each overdue milestone detected today, fire `map_milestone_overdue`. For each newly stalled deal, fire `map_stall_detected`.

### 3. Build the weekly prospect update workflow

Using `n8n-scheduling`, create a workflow that runs every Monday at 10 AM:

For each deal where `map_status` = "Active":

**Step 1 — Generate progress summary:**
Pull the MAP from Attio. Calculate:
- Milestones completed since last update
- Upcoming milestones for next 7 days
- Overall completion percentage
- Any overdue items

**Step 2 — Send progress email to prospect champion:**
Using `n8n-email-integration`, send a templated update:

```
Subject: {Company} Action Plan Update — Week of {date}

Hi {Champion},

Quick update on where we stand:

Completed this week:
{list of completed milestones with checkmarks}

Coming up next:
{list of upcoming milestones with dates and owners}

Overall progress: {completion_pct}% ({n} of {total} milestones complete)

{IF overdue milestones exist:}
Needs attention:
{overdue milestone} — was due {date}, owned by {owner}. Can you give me an update on timing?

{END IF}

Let me know if anything has changed on your end.

{Signature}
```

**Step 3 — Log the update:**
Fire `map_update_sent` in PostHog. Add a note to the Attio deal.

### 4. Build the escalation workflow

Using `n8n-triggers`, create escalation logic:

**Level 1 — Nudge (milestone 1-2 days overdue):**
Send a gentle reminder email to the milestone owner:
"Just checking in — {milestone} was due {date}. Are you on track, or should we adjust the timeline?"
Notify the rep via Slack.

**Level 2 — Escalation (milestone 5+ days overdue):**
Send a more direct email:
"We're {n} days past our target for {milestone}. I want to make sure we stay on track for {expected close date}. Can we schedule 15 minutes to discuss what's needed?"
Alert the rep with recommended actions.

**Level 3 — Stall intervention (2+ milestones overdue):**
Flag the deal as stalled in Attio (`map_status` = "Stalled"). Send the rep a stall diagnosis:
- Which milestones are blocked
- Who owns the blocked milestones
- Historical data: how often deals recover from this stall pattern
- Recommended intervention: champion re-engagement, executive-to-executive call, or timeline renegotiation

**Human action required:** Level 3 stalls require the rep to decide the intervention strategy. The agent provides the diagnosis and options but does not execute without approval.

### 5. Build milestone completion logging

Create an n8n workflow triggered when the rep marks a milestone as complete (via Attio update or Slack command):

- Update the MAP note in Attio with completion date
- Calculate `days_early_late` (positive = late, negative = early)
- Fire `map_milestone_completed` in PostHog
- Recalculate `map_completion_pct` and `map_expected_close`
- If all milestones complete, fire `map_completed` and update `map_status` to "Complete"

## Output

- Daily milestone health checks across all active MAPs
- Weekly prospect progress emails sent automatically
- 3-level escalation system for overdue milestones
- PostHog event stream for all MAP activity
- Attio deal attributes updated in real-time
- Stall detection with diagnosis and recommended interventions
