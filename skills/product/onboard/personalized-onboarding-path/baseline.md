---
name: personalized-onboarding-path-baseline
description: >
  Adaptive Onboarding Paths — Baseline Run. Wire persona-based onboarding
  into always-on automation: behavioral email sequences per persona,
  automated tour triggers, and continuous funnel tracking. First always-on
  personalized onboarding system.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "20 hours over 2 weeks"
outcome: "Activation rate >= 60% for persona-routed users AND >= 12pp lift over generic control, sustained for 2 consecutive weeks"
kpis: ["Activation rate by persona", "Tour completion rate by persona", "Email sequence open rate by persona", "Email click-to-activation rate by persona", "Time to activation by persona"]
slug: "personalized-onboarding-path"
install: "npx gtm-skills add product/onboard/personalized-onboarding-path"
drills:
  - onboarding-sequence-automation
  - onboarding-flow
  - posthog-gtm-events
---

# Adaptive Onboarding Paths — Baseline Run

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Convert the manually-tested persona onboarding paths from Smoke into an always-on system. Every new signup is automatically classified, routed to a persona-specific product tour, enrolled in a persona-specific email sequence, and tracked through a per-persona activation funnel. The system runs continuously without manual intervention. Pass threshold: activation rate >= 60% for persona-routed users AND >= 12pp lift over generic control, sustained for 2 consecutive weeks.

## Leading Indicators

- Automated persona classification assigns a `persona_type` to >= 95% of new signups within 60 seconds of `signup_completed` event
- Email sequence enrollment fires within 5 minutes of signup for all classified users (check n8n execution logs)
- Per-persona email open rate >= 45% for Email 1 (welcome) — confirms persona-specific subject lines outperform generic
- Tour completion rate per persona holds at or above Smoke-level rates (no regression from automation)
- PostHog funnels show per-persona conversion data populating within 48 hours of launch

## Instructions

### 1. Set up comprehensive event tracking

Run the `posthog-gtm-events` drill to instrument the full onboarding journey. Configure these events with persona context:

| Event | Properties | Trigger |
|-------|-----------|---------|
| `personalized_onboarding_signup` | `persona_type`, `signup_source`, `plan_type` | User completes signup |
| `personalized_onboarding_classified` | `persona_type`, `confidence` (explicit/inferred) | Persona classification completes |
| `personalized_onboarding_tour_started` | `persona_type`, `tour_variant` | Product tour begins |
| `personalized_onboarding_tour_step` | `persona_type`, `step_number`, `step_name` | Each tour step completed |
| `personalized_onboarding_tour_completed` | `persona_type`, `duration_seconds` | Tour finished |
| `personalized_onboarding_tour_dismissed` | `persona_type`, `step_number` | User exits tour early |
| `personalized_onboarding_email_sent` | `persona_type`, `email_step`, `subject` | Email sent via Loops |
| `personalized_onboarding_email_opened` | `persona_type`, `email_step` | Email opened |
| `personalized_onboarding_email_clicked` | `persona_type`, `email_step`, `cta_url` | Email CTA clicked |
| `personalized_onboarding_activated` | `persona_type`, `activation_type`, `days_since_signup` | User reaches persona-specific activation |

Build a PostHog funnel: `signup → classified → tour_started → tour_completed → activated`. Add breakdown by `persona_type`. Save as "Personalized Onboarding Funnel".

Build a PostHog dashboard "Personalized Onboarding Baseline" with panels: activation rate trend by persona (line chart, 4-week window), tour completion rate by persona (bar chart, weekly), email engagement by persona (table: open rate, click rate per email step per persona), time-to-activation distribution by persona (histogram).

### 2. Wire the always-on onboarding flow

Run the `onboarding-flow` drill to build the multi-channel onboarding experience. For Baseline, extend the Smoke-level tours with parallel email sequences:

**In-app layer (Intercom):**
- The 2 persona-specific product tours from Smoke continue running, triggered automatically by `persona_type` + `onboarding_complete = false`
- Add contextual in-app messages for each persona's top stall point (identified from Smoke data):
  - If persona = A and `tour_step_2_completed = false` after 24 hours: show tooltip nudging toward that step
  - If persona = B and `tour_step_3_completed = false` after 48 hours: show tooltip with a direct shortcut

**Email layer (Loops):**
- Build a 5-email persona-specific sequence per persona using the email framework from the `onboarding-sequence-design` drill (referenced inside `onboarding-flow`). Each persona's sequence differs in:
  - Subject lines referencing the persona's use case
  - CTAs linking to the persona's activation action (not a generic dashboard)
  - Use case examples matching the persona's role
  - Skip logic: exit the non-activated branch when `activation_reached` fires for that persona

### 3. Wire automated event routing

Run the `onboarding-sequence-automation` drill to connect PostHog events to Loops sequences via n8n:

Build 3 n8n workflows:

**Workflow 1 — Enrollment:**
```
PostHog webhook (signup_completed)
  → Extract: email, name, persona_type, signup_source, plan_type
  → POST to Loops /api/v1/contacts/create with persona properties
  → Loops auto-starts the persona-matched onboarding sequence
  → Log: personalized_onboarding_email_enrolled to PostHog
```

**Workflow 2 — Milestone sync:**
```
PostHog webhook (tour_completed OR milestone_N_completed)
  → Extract: email, persona_type, milestone details
  → PUT to Loops /api/v1/contacts/update with {milestone_completed: true}
  → POST to Loops /api/v1/events/send (triggers sequence branching/skipping)
```

**Workflow 3 — Activation exit:**
```
PostHog webhook (personalized_onboarding_activated)
  → Extract: email, persona_type, activation_type
  → PUT to Loops /api/v1/contacts/update with {activated: true, activation_date: timestamp}
  → POST to Loops /api/v1/events/send with {eventName: "activation_reached"}
  → Loops exits user from non-activated email branch, sends celebration email
```

Add error handling to all workflows: retry on 5xx, alert on 4xx, queue on timeout.

### 4. Launch with feature flag control

Use the PostHog feature flag from Smoke. Set it to route 50% of new signups to persona-specific paths (treatment) and 50% to the existing generic tour (control). This A/B split continues generating lift data at Baseline scale.

**Human action required:** Before enabling the flag at 50%, verify the full automation pipeline end-to-end:
1. Create a test user, confirm `signup_completed` fires in PostHog
2. Confirm n8n Workflow 1 creates the Loops contact and enrolls in the correct persona sequence
3. Confirm the Intercom product tour triggers for the test user's persona
4. Simulate milestone completion and confirm n8n Workflow 2 updates Loops and skips the nudge email
5. Simulate activation and confirm n8n Workflow 3 exits the sequence and sends the celebration email
6. Check that all PostHog events appear in the Personalized Onboarding Funnel
If any step fails, fix before enabling the flag for real users.

### 5. Monitor for 2 weeks

Check the PostHog dashboard daily for the first 3 days (catch automation failures early), then every 2-3 days:
- Confirm persona classification is assigning types (check for a growing "unclassified" bucket)
- Compare activation rate: personalized vs generic cohort
- Check per-persona email engagement: if one persona's open rate is below 30%, the subject lines need rewriting
- Check n8n execution logs for errors or timeouts

### 6. Evaluate against threshold

After 2 full weeks of automated operation:

- **Activation rate >= 60%** for the persona-routed treatment group (combined across personas)
- **Lift >= 12pp** above the generic-tour control group
- **Sustained:** Both weeks individually meet the activation threshold (not just the 2-week average — this catches a strong week 1 masking a declining week 2)
- **Per-persona check:** No persona below 45% activation. If one persona is dragging, iterate on that persona's tour and email sequence specifically.

Decision tree:
- **Pass:** Proceed to Scalable. Roll out personalized onboarding to 100% of signups. Begin planning persona expansion.
- **Marginal pass (one week passes, one doesn't):** Run for 1 more week. If the third week passes, proceed.
- **Fail:** Diagnose using PostHog session recordings for the persona-routed group. Identify where users drop off. Fix the biggest drop-off point and re-run for 2 weeks.

## Time Estimate

- 4 hours: PostHog event instrumentation and funnel/dashboard setup
- 6 hours: Building persona-specific email sequences in Loops (2 personas x 5 emails)
- 4 hours: n8n workflow creation (3 workflows + error handling + testing)
- 2 hours: Intercom contextual messages for stall points
- 2 hours: End-to-end pipeline testing
- 2 hours: Monitoring and analysis over 2 weeks (15 min/day)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, dashboards, feature flags, session recordings | Free tier: 1M events/mo, 5K recordings — [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | Persona-specific product tours + contextual stall-point messages | Essential: $29/seat/mo + Proactive Support Plus: $99/mo (500 messages) — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Persona-specific onboarding email sequences | Free up to 1K contacts; paid from $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| n8n | 3 automation workflows (enrollment, milestone sync, activation exit) | Starter: €24/mo (2,500 executions); self-hosted: free — [n8n.io/pricing](https://n8n.io/pricing/) |

**Estimated monthly cost at this level:** $100-275/mo (PostHog likely still free tier; Intercom $128; Loops $0-49; n8n $0-24)

## Drills Referenced

- `onboarding-sequence-automation` — wires PostHog onboarding events to Loops email sequences via n8n webhooks for always-on behavioral email delivery
- `onboarding-flow` — builds the multi-channel onboarding experience combining Intercom product tours, in-app messages, and Loops lifecycle emails
- `posthog-gtm-events` — instruments all onboarding events with persona context for funnel tracking and dashboarding
