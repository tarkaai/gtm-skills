---
name: onboarding-sequence-design
description: Map onboarding milestones, write behavioral email content, and define send timing for a signup-to-activation email sequence
category: Product
tools:
  - Loops
  - PostHog
fundamentals:
  - loops-sequences
  - loops-audience
  - posthog-custom-events
  - posthog-cohorts
---

# Onboarding Sequence Design

This drill produces a complete onboarding email sequence: the milestone map, the email content for each step, the behavioral triggers, and the timing logic. The output is a ready-to-implement sequence specification that the `onboarding-sequence-automation` drill wires into Loops and n8n.

## Prerequisites

- A clear definition of your product's "aha moment" (the first action that correlates with 30-day retention)
- PostHog data showing which early actions predict retention (or a strong hypothesis if you have no data yet)
- Loops account set up with sending domain verified

## Steps

### 1. Define the activation milestone

Using the `posthog-cohorts` fundamental, compare users who retained at day 30 vs users who churned. Identify the single action that best separates the two groups. This is your activation metric. Examples:

- Created their first [core object]
- Completed an end-to-end workflow
- Invited a teammate
- Connected an integration
- Reached a usage threshold (e.g., sent 10 messages)

If you lack data, pick the action that most directly delivers the product's core value promise. You will validate this in the Baseline level.

Document the activation metric as a PostHog event name using `posthog-custom-events`: e.g., `activation_reached` with properties `{activation_type: "first_project_created", days_since_signup: N}`.

### 2. Map the milestone ladder from signup to activation

Break the path from signup to activation into 3-5 intermediate milestones. Each milestone is a PostHog event. Example for a project management tool:

1. `signup_completed` — account created
2. `profile_completed` — name, avatar, company set
3. `first_project_created` — created their first project
4. `first_task_added` — added content to the project
5. `activation_reached` — invited a teammate or completed a workflow

Each milestone must be:
- Trackable as a distinct PostHog event
- Achievable in a single session (no multi-day milestones)
- On the critical path to activation (not a side quest)

### 3. Write the email sequence

Design 5-7 emails. Each email is triggered either by time (delay since signup) or behavior (milestone reached or NOT reached). Write the actual content — subject line, preview text, body, and CTA — not placeholders.

**Email 1 — Welcome (trigger: immediate on signup)**
- Subject: "[Product] — here's your quickstart"
- Purpose: Confirm signup, deliver one clear next step
- CTA: Link directly to the action for Milestone 2, not to the dashboard
- Tone: Warm, brief, no feature dump
- Skip condition: None (everyone gets this)

**Email 2 — Quickstart nudge (trigger: 24 hours after signup IF Milestone 2 not reached)**
- Subject: "Quick question — did you get stuck?"
- Purpose: Remove friction for users who signed up but did not take the first step
- CTA: Link to a 60-second setup guide or video
- Skip condition: Skip if user already completed Milestone 2

**Email 3 — Use case inspiration (trigger: 48 hours after signup OR immediately on Milestone 2 completion)**
- Subject: "How [similar company type] uses [Product] for [outcome]"
- Purpose: Show the user what's possible. Use a real customer example or a concrete use case walkthrough
- CTA: Link to start the workflow described in the use case
- Skip condition: Skip if user already reached activation

**Email 4 — Social proof (trigger: Day 5 if not activated)**
- Subject: "[X] teams activated this week — here's what they did first"
- Purpose: Create urgency and FOMO via social proof
- CTA: Link to the activation action
- Skip condition: Skip if user already reached activation

**Email 5 — Personal help offer (trigger: Day 7 if not activated)**
- Subject: "Can I help you get set up?"
- Purpose: Offer human assistance for stuck users. Send from a real person (founder or CSM), not from the product
- CTA: Calendar booking link (Cal.com) or reply-to
- Skip condition: Skip if user already reached activation

**Email 6 — Milestone celebration (trigger: immediately on activation)**
- Subject: "You did it — [specific achievement]"
- Purpose: Celebrate activation and suggest the next valuable action
- CTA: Link to the next feature that deepens engagement (e.g., invite teammates, set up integrations)
- Skip condition: None — send to all activated users

**Email 7 — Next steps (trigger: 2 days after activation)**
- Subject: "Now that you're set up, try [next feature]"
- Purpose: Bridge from onboarding to regular product usage
- CTA: Link to an advanced feature or integration
- Skip condition: None

### 4. Define the timing and branching logic

Document the full sequence as a decision tree:

```
signup_completed
  ├── Send Email 1 (immediate)
  ├── Wait 24h → check Milestone 2
  │   ├── NOT completed → Send Email 2
  │   └── Completed → skip Email 2
  ├── Wait 48h OR Milestone 2 completed → Send Email 3
  ├── Day 5, NOT activated → Send Email 4
  ├── Day 7, NOT activated → Send Email 5
  ├── activation_reached (any time) → Send Email 6, exit non-activated branch
  └── 2 days after activation → Send Email 7
```

Key rules:
- Never send more than 1 email per day
- Exit the "not activated" branch immediately when activation occurs
- Always send the celebration email regardless of where the user is in the time-based sequence

### 5. Set up the audience in Loops

Using the `loops-audience` fundamental:

1. Create contact properties: `signup_date`, `activation_date`, `milestone_2_completed`, `milestone_3_completed`, `plan_type`, `signup_source`
2. Create segments: "Not Activated" (signup_date exists, activation_date is null), "Activated" (activation_date exists), "Stuck at Milestone 2" (signup > 24h ago, milestone_2_completed is false)
3. Connect your app to sync these properties in real-time via the Loops API

### 6. Build the sequence in Loops

Using the `loops-sequences` fundamental:

1. Create a sequence triggered by the "Contact created" event
2. Add the 7 emails with the timing and branching logic from Step 4
3. Set exit conditions: activation_reached = true exits the "not activated" branch
4. Add conditional branches after each delay to check milestone status
5. Test the sequence by creating a test contact and walking through each branch

### 7. Document the sequence specification

Create a reference file listing: each email's trigger, subject, CTA URL, skip condition, and the PostHog events that feed into each decision point. This document is the input for the `onboarding-sequence-automation` drill.
