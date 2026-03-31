---
name: trial-intervention-orchestration
description: Route trial users to the right intervention channel and message based on their health score, trial day, and engagement signals
category: Conversion
tools:
  - n8n
  - PostHog
  - Intercom
  - Loops
  - Attio
  - Cal.com
fundamentals:
  - n8n-triggers
  - n8n-workflow-basics
  - n8n-crm-integration
  - posthog-cohorts
  - posthog-feature-flags
  - intercom-in-app-messages
  - loops-sequences
  - loops-transactional
  - attio-contacts
  - attio-notes
  - attio-deals
  - calcom-booking-links
---

# Trial Intervention Orchestration

This drill builds a routing engine that matches each trial user to the right intervention based on their health segment, trial day, engagement trajectory, and previous interventions. It prevents over-messaging, sequences interventions by urgency, and routes high-value trials to human sales when automation alone will not close the deal.

## Prerequisites

- `trial-activation-scoring` drill running (produces daily Hot/Warm/Cold segments)
- PostHog tracking trial events with milestone properties
- Intercom configured for in-app messaging
- Loops configured for triggered email sequences
- Attio tracking trial user records with `trial_health_score` and `trial_segment`
- Cal.com booking links for onboarding calls

## Steps

### 1. Define the intervention matrix

Build a routing table that maps trial state to intervention:

| Segment | Trial Day | Trajectory | Intervention | Channel | Priority |
|---------|-----------|------------|--------------|---------|----------|
| Hot | 1-7 | Rising | Milestone coaching — guide to next step | In-app (Intercom) | Low |
| Hot | 8-12 | Stable/Rising | Upgrade nudge — show value realized + upgrade CTA | In-app + Email | Medium |
| Hot | 12-14 | Any | Urgency prompt — trial expiring, one-click upgrade | In-app modal + Email | High |
| Warm | 1-3 | Flat | Quick-start help — link to fastest activation path | Email (Loops) | Medium |
| Warm | 4-7 | Flat/Falling | Use-case coaching — send role-specific guide | Email + In-app | Medium |
| Warm | 8-12 | Falling | Rescue call offer — Cal.com booking link from founder | Email (personal) | High |
| Warm | 12-14 | Any | Final nudge — "your data is ready, just upgrade" | Email + In-app | High |
| Cold | 1-3 | Absent | Re-engagement — "need help getting started?" | Email (Loops) | Low |
| Cold | 4-7 | Absent | Last chance re-engage — tutorial + Cal.com link | Email (personal) | Medium |
| Cold | 8+ | Absent | Let expire — do not spend resources | None | None |

### 2. Build the n8n routing workflow

Using `n8n-triggers` and `n8n-workflow-basics`, create the main orchestration workflow:

**Trigger:** Webhook from the daily scoring workflow (fires after `trial-activation-scoring` completes)

**For each trial user in the payload:**

1. Read current `trial_segment`, `trial_health_score`, `days_remaining`, and `intervention_history` from Attio
2. Calculate trajectory: compare today's score to 3-day average. Rising (>+5), Stable (within +/-5), Falling (>-5), Absent (no sessions in 3+ days)
3. Look up the intervention matrix row matching segment + trial day range + trajectory
4. Check intervention history: do NOT send the same intervention type within 48 hours. Do NOT send more than 1 email per day.
5. If an intervention is due, execute it via the appropriate channel

### 3. Wire the in-app intervention channel

Using `intercom-in-app-messages`, create targeted messages for each intervention type:

**Milestone coaching (Hot, Day 1-7):**
- Target: PostHog cohort `trial_segment = Hot AND days_since_trial_start <= 7`
- Message: "You've completed [N of M] setup steps. Next up: [next milestone]. Here's a 2-minute guide."
- Link: deep link to the action that completes the next milestone
- Dismiss tracking: track `coaching_message_dismissed` event

**Upgrade nudge (Hot, Day 8-12):**
- Target: `trial_segment = Hot AND days_since_trial_start BETWEEN 8 AND 12`
- Message: "You've [usage summary]. Teams like yours get [specific benefit] on [Plan]. Upgrade now."
- CTA: one-click upgrade link
- Track: `upgrade_nudge_shown`, `upgrade_nudge_clicked`

**Urgency prompt (Hot, Day 12-14):**
- Target: `trial_segment = Hot AND days_remaining <= 2`
- Message type: modal (higher visibility than banner)
- Message: "Your trial ends in [N] days. You've built [specific work] — upgrade to keep it all."
- CTA: primary = "Upgrade now", secondary = "Extend trial"
- Track: `urgency_prompt_shown`, `urgency_prompt_upgraded`, `urgency_prompt_extended`

**Use-case coaching (Warm, Day 4-7):**
- Target: `trial_segment = Warm AND days_since_trial_start BETWEEN 4 AND 7`
- Message: "Teams in [industry/role] get the most value by [specific workflow]. Try it now."
- Link: deep link to the relevant feature
- Track: `coaching_message_clicked`

### 4. Wire the email intervention channel

Using `loops-sequences` and `loops-transactional`:

**Quick-start help (Warm, Day 1-3):**
- From: product@company.com
- Subject: "[Product] — get set up in 5 minutes"
- Content: the 3 fastest steps to activation. Screenshot or GIF of each step.
- CTA: deep link to step 1

**Rescue call offer (Warm, Day 8-12, Falling):**
- From: founder's personal email
- Subject: "Quick question about your trial"
- Content: "I noticed you signed up [N] days ago. I'd love to help you get value from [Product]. Here's my calendar for a 15-minute call: [Cal.com link]"
- Use `calcom-booking-links` to generate a personalized booking URL with pre-filled context

**Re-engagement (Cold, Day 1-3):**
- From: product@company.com
- Subject: "Need help getting started?"
- Content: "We noticed you haven't logged in since signing up. Here's the #1 thing to try first: [link]"
- If no response after 48h, suppress further emails to this user

**Final nudge (any segment, Day 12-14):**
- From: founder's personal email
- Subject: "Your trial ends [tomorrow/in 2 days]"
- Content: "You've [usage summary if any, or 'started exploring']. Upgrade now to keep your [specific data/work]. If budget is the blocker, reply and let's talk."

### 5. Wire the human escalation channel

For high-value trial users that automation cannot close:

Using `attio-deals` and `attio-contacts`:
- If a Hot user reaches Day 12 without upgrading AND their company has >50 employees (from enrichment), create an expansion deal in Attio
- Assign to the account owner with context: trial health score, milestones completed, usage summary, days remaining
- Add an Attio note with recommended talking points using `attio-notes`
- The human outreach should happen within 24 hours of deal creation

### 6. Track intervention effectiveness

Using `posthog-cohorts`, create cohorts for each intervention type and measure:

- **Reach:** what percentage of eligible users received the intervention
- **Engagement:** what percentage clicked/responded within 24 hours
- **Outcome:** what percentage converted to paid within 7 days of the intervention
- **Control:** what percentage of users in the same segment who did NOT receive the intervention converted (natural conversion rate)

Calculate lift per intervention: (intervention conversion rate - natural conversion rate) / natural conversion rate. Interventions with < 0% lift should be disabled and reworked.

### 7. Log all interventions

Using `attio-notes`, log every intervention on the trial user's Attio record:
- Timestamp
- Intervention type
- Channel (in-app, email, human)
- Content summary
- User response (clicked, dismissed, no action, replied, booked call, upgraded)

This log feeds the `autonomous-optimization` drill at Durable level with the data needed to generate hypotheses about intervention effectiveness.

## Output

- Automated routing of trial users to the right intervention at the right time
- Multi-channel delivery (in-app, email, human) based on segment and urgency
- Intervention effectiveness tracking with lift measurement
- Full audit trail of every intervention per user in Attio

## Triggers

Fires daily after `trial-activation-scoring` completes. In-app messages are always-on via Intercom targeting rules. Emails trigger via n8n-to-Loops webhook. Human escalation creates Attio deals on demand.
