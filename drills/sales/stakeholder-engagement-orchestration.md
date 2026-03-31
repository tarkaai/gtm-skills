---
name: stakeholder-engagement-orchestration
description: Automate scheduling, outreach sequencing, and coverage tracking across all stakeholders in a deal
category: Sales
tools:
  - n8n
  - Attio
  - Instantly
  - Cal.com
  - Anthropic
fundamentals:
  - n8n-workflow-basics
  - n8n-scheduling
  - n8n-crm-integration
  - n8n-triggers
  - attio-contacts
  - attio-deals
  - attio-custom-attributes
  - attio-lists
  - instantly-campaign
  - calcom-booking-links
  - calcom-event-types
  - ai-content-ghostwriting
  - posthog-custom-events
---

# Stakeholder Engagement Orchestration

This drill automates the coordination of outreach across all stakeholders in a deal. It ensures every mapped stakeholder gets contacted with role-appropriate messaging at the right time, prevents outreach collisions, tracks engagement coverage, and alerts when key stakeholders are going dark.

## Input

- Completed stakeholder map in Attio (from `stakeholder-map-assembly` drill)
- Discovery question sets per stakeholder (from `discovery-question-bank` drill)
- n8n instance for workflow automation
- Instantly for email sequencing (or Smartlead as alternative)
- Cal.com for meeting booking

## Steps

### 1. Create Engagement Priority Queue

Build an n8n workflow that queries Attio for all stakeholders with `engagement_status = Unengaged` or `discovery_status = Not Started`, sorted by influence score descending:

```
n8n HTTP node → Attio API:
GET /v2/objects/people/records/query
filter: { linked_deal_id: "{deal_id}", engagement_status: "Unengaged" }
sort: { influence_score: "desc" }
```

Group stakeholders by role for sequenced engagement:
1. **First wave**: Champion and Economic Buyer (if accessible). Start here because they unlock access to others.
2. **Second wave**: Influencers and Technical Evaluators. Engage once you understand top-level priorities.
3. **Third wave**: End Users and Gatekeepers. Engage last with specific questions informed by prior discovery.

### 2. Generate Role-Specific Outreach Messages

For each stakeholder in the queue, use `ai-content-ghostwriting` to generate a personalized meeting request:

```
Prompt context:
- Stakeholder: {name}, {title}, {role}
- Their likely priorities (from role classification)
- What you already know from other stakeholders (if any)
- The specific discovery questions you need answered

Output: 3-5 sentence email requesting a 20-minute discovery conversation. Reference something specific to their role. Do NOT pitch the product. Frame as "understanding their perspective before recommending anything."
```

### 3. Build Outreach Sequences in Instantly

For each engagement wave, create an Instantly campaign using `instantly-campaign`:
- **Sequence**: 3 touches over 10 days (initial request → follow-up with added context → final attempt with calendar link)
- **Personalization**: Each touch uses the generated role-specific message
- **Calendar link**: Include a Cal.com booking link (via `calcom-booking-links`) specific to this deal's discovery meetings
- **Labels**: Tag each campaign with deal_id, stakeholder_role, and wave_number for tracking

### 4. Build Engagement Tracking Workflow

Create an n8n workflow triggered by Instantly reply webhooks and Cal.com booking webhooks:

**On email reply:**
1. Parse reply sentiment (positive/negative/question)
2. Update Attio: set `engagement_status = Engaged`, log the reply
3. Fire PostHog event: `stakeholder_outreach_replied`
4. If positive: trigger calendar link follow-up
5. If negative: flag for human review with context

**On meeting booked:**
1. Update Attio: set `discovery_status = Scheduled`, log meeting date
2. Fire PostHog event: `stakeholder_discovery_scheduled`
3. Trigger `discovery-question-bank` drill to refresh questions with latest intelligence

**On no response after sequence completes:**
1. Update Attio: set `engagement_status = Unresponsive`
2. Fire PostHog event: `stakeholder_outreach_failed`
3. Check if another stakeholder at the account can introduce them (ask the Champion)

### 5. Build Coverage Dashboard

Create an Attio saved view "Stakeholder Coverage by Deal" showing:
- Each active deal with columns: total stakeholders, engaged count, discovery complete count, consensus score
- Color-code: green (>75% coverage), yellow (50-75%), red (<50%)
- Filter: deals at Connected stage or later

### 6. Build Gap Alert Workflow

Create an n8n workflow on a daily cron schedule:
1. For each deal at Connected+ stage, check stakeholder engagement coverage
2. If a deal has been at Connected for >14 days AND the Economic Buyer is still Unengaged: high-priority alert
3. If a deal has <3 engaged stakeholders AND is advancing toward Proposed: risk alert
4. If any stakeholder has been Unresponsive for >21 days: suggest alternative approach (LinkedIn, champion introduction, different angle)

Route alerts to Slack or email with the specific deal, stakeholder, and recommended action.

## Output

- Automated outreach sequences for all unmapped stakeholders, personalized by role
- Engagement tracking with real-time status updates in Attio
- Coverage dashboard showing multi-threading progress per deal
- Gap alerts when key stakeholders are missing or unresponsive
- PostHog events for every outreach attempt, reply, booking, and failure

## Triggers

Run this drill:
- After `stakeholder-map-assembly` identifies new unengaged stakeholders
- When a deal advances to a new stage (re-check coverage)
- Daily via n8n cron for gap alerting
