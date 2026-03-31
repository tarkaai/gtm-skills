---
name: demo-follow-up-automation
description: Build n8n workflows that auto-trigger personalized demo follow-up sequences based on CRM events and prospect behavior
category: Demos
tools:
  - n8n
  - Attio
  - Fireflies
  - Anthropic
  - Instantly
  - Loops
  - PostHog
  - Loom
  - Cal.com
fundamentals:
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-scheduling
  - n8n-crm-integration
  - attio-deals
  - attio-notes
  - attio-automation
  - fireflies-transcription
  - call-transcript-pain-extraction
  - instantly-campaign
  - instantly-reply-detection
  - instantly-tracking
  - loops-sequences
  - loom-analytics
  - posthog-custom-events
  - posthog-funnels
  - calcom-booking-links
  - calcom-crm-sync
---

# Demo Follow-Up Automation

This drill builds the n8n workflow layer that makes demo follow-ups happen automatically. Instead of the founder manually running `demo-recap-assembly` and `demo-follow-up-cadence` for every demo, these workflows detect demo completion, generate the recap, schedule the cadence, and adapt based on prospect behavior — all without manual intervention.

## Input

- Fireflies integration configured to transcribe demo calls
- Attio deal pipeline with deals at "Connected" stage
- n8n instance with credentials for: Attio, Fireflies, Anthropic, Instantly/Loops, PostHog, Loom, Cal.com
- `demo-recap-assembly` and `demo-follow-up-cadence` drills understood and validated at Baseline level

## Steps

### 1. Build the demo completion trigger workflow

Using `n8n-triggers`, create a workflow that fires when a demo ends:

**Trigger option A — Fireflies webhook:**
Fireflies sends a webhook when a transcript is ready. Configure n8n to receive this webhook and filter for meetings tagged "demo" or containing "demo" in the title.

**Trigger option B — Attio webhook:**
When a deal's `last_meeting_type` field is updated to "demo" (set by Cal.com integration or manually), trigger the workflow.

**Trigger option C — Cal.com webhook:**
When a Cal.com event of type "Product Demo" ends (event.completed webhook), trigger the workflow with the attendee email and deal context.

Use `n8n-workflow-basics` to build the trigger handler:
```json
{
  "trigger": "webhook",
  "source": "fireflies|attio|calcom",
  "filter": "meeting_type == demo AND transcript_available == true",
  "action": "start_recap_generation"
}
```

### 2. Build the automated recap generation workflow

Chain these steps in n8n after the trigger fires:

1. **Fetch transcript:** Use `fireflies-transcription` to pull the full transcript. If not yet available (Fireflies can take 10-30 minutes), set a retry with exponential backoff: 10 min, 20 min, 40 min.

2. **Extract demo signals:** Send the transcript to Claude using `call-transcript-pain-extraction` enhanced with demo-specific extraction (features shown, questions asked, concerns, interest signals, stakeholders, next step suggestion).

3. **Fetch deal context:** Using `n8n-crm-integration` and `attio-deals`, pull the deal record to enrich the recap with: deal value, stage history, previous touchpoints, and any existing notes.

4. **Generate recap email:** Send extracted signals + deal context to Claude to produce the personalized recap email, subject line, and internal notes.

5. **Store in Attio:** Using `attio-notes`, save the recap as a deal note tagged `demo-recap-auto`. Update the deal record with extracted signals using `attio-deals`.

6. **Queue for human review:** Send a notification (Slack or email) to the founder with the recap email preview and a one-click "Approve & Send" or "Edit" action. Include a 2-hour timer — if no response, send a reminder.

7. **On approval:** Send the email via Loops using `loops-sequences` (transactional email for warm contacts). Update Attio: `demo_recap_sent: true`. Fire PostHog event.

8. **Start the cadence:** Trigger the follow-up cadence workflow (Step 3 below) with the deal context and recap data.

### 3. Build the automated cadence execution workflow

Using `n8n-scheduling`, create a workflow that executes the follow-up cadence from `demo-follow-up-cadence`:

1. **Day 1 check-in:** Schedule an n8n delay node for 24 hours after recap sent. When it fires:
   - Check Attio for replies since recap (using `attio-deals` — if `last_reply_date` is after `demo_recap_sent_at`, skip this touch)
   - If no reply: generate check-in email via Claude with the unanswered questions context
   - Send via Loops or Instantly. Log in Attio and PostHog.

2. **Day 3 value asset:** Schedule 48 hours after check-in. When it fires:
   - Check for replies (skip if responded)
   - Select the resource based on deal context (use the mapping table from `demo-follow-up-cadence`)
   - Generate the value asset email
   - Send and track using `instantly-tracking`

3. **Day 5-7 engagement-based touch:** Schedule 2-4 days after value asset. When it fires:
   - Pull engagement data: `loom-analytics` for video views, `instantly-tracking` for link clicks, PostHog for website visits
   - Branch on engagement level (high/low as defined in `demo-follow-up-cadence`)
   - Generate the appropriate email variant
   - Send with `calcom-booking-links` included

4. **Day 10 momentum check:** Schedule 3-5 days after engagement touch. When it fires:
   - Check for any response or booking across all channels
   - If still no engagement: send the momentum check email
   - If sequence completes with no response: update Attio, set 30-day re-engagement reminder

### 4. Build the reply detection and exit workflow

Using `n8n-triggers`, create a webhook listener for reply events from Instantly and Loops:

1. **Reply detected:** Immediately pause all scheduled follow-up nodes for this deal.
2. **Classify reply sentiment:** Send reply text to Claude: "Classify this reply as: positive (wants next step), neutral (acknowledged, no commitment), negative (not interested), question (has a question), or out_of_office. Return JSON."
3. **Route by classification:**
   - Positive: Update Attio deal stage, cancel remaining sequence, notify founder
   - Neutral: Extend the cadence timing (+2 days per remaining touch)
   - Negative: Cancel sequence, update Attio deal status, log reason
   - Question: Forward to founder for manual response, pause sequence
   - OOO: Pause sequence, re-schedule from the return date

### 5. Build the behavioral signal workflow

Using `n8n-triggers` and PostHog webhooks, react to prospect behavior:

- **Website visit after follow-up:** If PostHog detects the prospect visiting product pages (pricing, docs, integrations) within 24 hours of a follow-up touch, fast-track the next touch and include content related to the pages visited.
- **Loom recap view:** When `loom-analytics` shows the prospect watched >75% of the recap video, promote the deal to "high engagement" and move up the next-step proposal.
- **Calendar booking:** When `calcom-crm-sync` detects a booking from this prospect, cancel all remaining follow-up touches and update Attio.
- **Stakeholder forward signal:** If a new person from the same company views the recap video or visits the website, flag in Attio as multi-thread opportunity.

### 6. Monitor workflow health

Using `n8n-scheduling`, create a daily monitoring workflow:

1. Count active follow-up sequences (deals with `follow_up_sequence_status: active`)
2. Check for stuck sequences (next touch overdue by >24 hours — indicates n8n failure)
3. Check for sequences without any PostHog events in >3 days (tracking may be broken)
4. Calculate: sequences started today, completed today, average touches to conversion
5. Send a daily digest to the founder: "Today: {N} new demos recapped, {N} sequences active, {N} next steps booked"

## Output

- Fully automated demo-to-follow-up pipeline: demo ends, recap generates, cadence executes
- Behavior-reactive follow-up timing and content selection
- Reply classification and automatic sequence exit routing
- Daily workflow health monitoring
- All touchpoints logged in Attio and PostHog

## Triggers

The main trigger fires automatically when a demo transcript becomes available. The cadence workflows run on n8n delay/schedule nodes. Reply and behavior workflows run on webhooks. Health monitoring runs daily at 9 AM.
