---
name: referral-pipeline-automation
description: n8n workflows that automate the referral request lifecycle — from ask scheduling through intro tracking to meeting attribution
category: Partnerships
tools:
  - n8n
  - Attio
  - PostHog
  - Loops
fundamentals:
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-scheduling
  - n8n-crm-integration
  - n8n-email-integration
  - attio-automation
  - attio-contacts
  - attio-deals
  - posthog-custom-events
  - loops-sequences
---

# Referral Pipeline Automation

This drill builds n8n workflows that manage the full referral request lifecycle at scale. Without this automation, tracking 50+ active referral requests across different connectors, targets, and follow-up stages becomes unmanageable.

## Input

- Referral map in Attio with scored connector-target pairs (from `referral-network-mapping`)
- Ask messages generated and stored in Attio (from `referral-ask-copywriting`)
- n8n instance with Attio, PostHog, and Loops integrations configured
- PostHog tracking for referral events already configured

## Steps

### 1. Build the ask scheduling workflow

Using the `n8n-scheduling` and `n8n-crm-integration` fundamentals, create an n8n workflow:

- **Trigger**: Daily cron (9am local time, Tuesday through Thursday — highest response days)
- **Action 1**: Query Attio for referral pairs with status "Ask Ready" and no ask sent yet
- **Action 2**: Rate-limit: select a maximum of 3 asks per day. Prioritize by composite score descending. Sending too many asks at once depletes your social capital.
- **Action 3**: For each selected pair, pull the ask message from the connector's Attio notes
- **Action 4**: If the connector prefers email, queue the message via Loops using the `loops-sequences` fundamental (single send, not a drip). If the connector prefers LinkedIn DM, create a task in Attio for the founder to send manually.
- **Action 5**: Update the pair status in Attio: "Ask Sent" with timestamp
- **Action 6**: Fire a PostHog event: `referral_ask_sent` with properties: connector_name, target_company, composite_score, channel (email/linkedin), ask_variant (A/B)

### 2. Build the follow-up workflow

Using the `n8n-triggers` fundamental, create a time-delayed follow-up workflow:

- **Trigger**: 7 days after `referral_ask_sent` event, if no `referral_intro_received` event exists for the same connector-target pair
- **Action 1**: Check Attio for the pair's current status. If still "Ask Sent" (no response), proceed.
- **Action 2**: Send a single gentle follow-up. Template:

```
{Connector first name},

Just floating this back up — totally understand if the timing is not right. Let me know either way and I will stop bugging you.

{Your name}
```

- **Action 3**: Update status to "Follow-up Sent" with timestamp
- **Action 4**: Fire PostHog event: `referral_followup_sent`
- **Action 5**: If no response after 14 more days (21 days total from original ask), update status to "No Response" and do NOT send additional follow-ups. Mark the connector's willingness score down by 1 for future asks.

### 3. Build the intro received workflow

Using the `n8n-triggers` fundamental, create a webhook-triggered workflow:

- **Trigger**: Manual trigger (founder marks "Intro Received" in Attio) OR email parsing detects an introduction email
- **Action 1**: Update pair status to "Intro Received" with timestamp
- **Action 2**: Calculate intro response time (days between ask sent and intro received)
- **Action 3**: Fire PostHog event: `referral_intro_received` with properties: connector_name, target_company, response_time_days
- **Action 4**: Create a new deal in Attio pipeline: stage "Intro Made", source "Warm Intro — {connector name}", linked to the target company and contact
- **Action 5**: Send a thank-you message to the connector (via the same channel they received the ask). Template:

```
{Connector first name},

Thank you — this means a lot. I will keep you posted on how it goes.

{Your name}
```

- **Action 6**: Increment the connector's "Total Intros Made" field in Attio

### 4. Build the meeting attribution workflow

Using the `n8n-triggers` and `posthog-custom-events` fundamentals:

- **Trigger**: A `meeting_booked` event fires in PostHog where the deal source contains "Warm Intro"
- **Action 1**: Look up the deal in Attio to find the originating connector
- **Action 2**: Fire PostHog event: `referral_meeting_booked` with properties: connector_name, target_company, days_from_intro_to_meeting
- **Action 3**: Update the Attio deal stage to "Meeting Booked"
- **Action 4**: Increment the connector's "Total Meetings from Intros" field in Attio

### 5. Build the connector health dashboard fields

Using the `attio-automation` fundamental, maintain these computed fields on each connector record (updated weekly by n8n):

- `total_asks_sent`: Count of referral asks sent to this connector
- `total_intros_made`: Count of intros this connector actually made
- `total_meetings_from_intros`: Meetings resulting from this connector's intros
- `ask_to_intro_rate`: intros / asks (percentage)
- `intro_to_meeting_rate`: meetings / intros (percentage)
- `avg_response_time_days`: Average days from ask to intro
- `last_ask_date`: When the most recent ask was sent
- `last_intro_date`: When the most recent intro was made
- `connector_status`: Active / Cooling Off / Dormant / Exhausted

### 6. Build the weekly referral pipeline summary

Using `n8n-scheduling`, create a weekly workflow (Friday 4pm):

1. Count: asks sent this week, intros received, meetings booked, deals created
2. Calculate: request-to-intro rate, intro-to-meeting rate
3. List: top 3 connectors by activity this week
4. List: overdue follow-ups (asks sent >7 days ago with no response and no follow-up sent)
5. Post summary to Slack

## Output

- Automated ask scheduling with daily rate-limiting (max 3/day)
- Time-delayed follow-up workflow (7 days, single follow-up, then stop)
- Intro tracking with automatic deal creation and connector attribution
- Meeting attribution back to originating connector
- Per-connector performance fields updated weekly
- Weekly pipeline summary

## Triggers

Build these workflows once at the start of Scalable level. They run continuously. The ask scheduling workflow requires connector-target pairs to be in "Ask Ready" status (populated by the `referral-ask-copywriting` drill).
