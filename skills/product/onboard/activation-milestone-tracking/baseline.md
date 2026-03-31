---
name: activation-milestone-tracking-baseline
description: >
  Activation Milestone Tracking — Baseline Run. Deploy always-on milestone
  monitoring with automated nudges for stalled users, driving activation rate
  to ≥50% across all new signups over 2 weeks.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥50% activation rate across all signups over a rolling 2-week window"
kpis: ["Activation rate", "Per-milestone completion rate", "Time-to-activation (median)", "Stalled user count"]
slug: "activation-milestone-tracking"
install: "npx gtm-skills add product/onboard/activation-milestone-tracking"
drills:
  - onboarding-flow
  - feature-adoption-monitor
  - threshold-engine
---

# Activation Milestone Tracking — Baseline Run

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Activation rate reaches ≥50% across all new signups measured over a rolling 2-week window. Always-on funnel monitoring detects stalled users automatically. Automated nudge sequences re-engage stalled users at each milestone. Per-milestone conversion data is available in a PostHog dashboard for ongoing analysis.

## Leading Indicators

- Onboarding flow emails and in-app messages are deployed and triggering correctly
- Stalled-user detection workflow fires daily and identifies users correctly
- Nudge messages produce measurable re-engagement (at least 10% of nudged users proceed to the next milestone within 48 hours)
- Per-milestone completion rates trend upward week-over-week
- Time-to-activation median decreases or stabilizes

## Instructions

### 1. Build the onboarding flow around milestones

Run the `onboarding-flow` drill to create a multi-channel onboarding experience keyed to your activation milestones (defined in Smoke level). For each milestone transition:

**In-app guidance (Intercom):**
- After Milestone 1 (account created): Show a product tour pointing to the setup step required for Milestone 2. Keep it to 3 steps max. Trigger: user has completed signup but not started configuration within 1 hour.
- After Milestone 2 (workspace configured): Show a contextual tooltip encouraging the first core action. Trigger: user has configured workspace but not performed core action within 24 hours.
- After Milestone 3 (first core action): Show a congratulations banner with a direct link to the next action that produces the value moment. Trigger: immediately after core action completes.

**Lifecycle emails (Loops):**
- Email 1 (immediate after signup): Welcome email with one clear next step — a deep link directly to the configuration page, not the dashboard.
- Email 2 (24 hours if Milestone 2 not reached): "Quick setup guide" showing the fastest path to configuration. Skip if already completed.
- Email 3 (48 hours if Milestone 3 not reached): Tutorial email showing how to perform the first core action. Include a screenshot or GIF. Skip if already completed.
- Email 4 (72 hours if Milestone 4 not reached): Social proof email showing how a similar user got value. Include a direct link to the value-producing action. Skip if already completed.
- Email 5 (7 days if not activated): Personal check-in email from a founder or CS lead. Include a calendar booking link for a 15-minute help call. Skip if already activated.

Each email must check the user's current milestone state before sending. Never send a nudge for a milestone the user has already passed.

### 2. Deploy stalled-user detection and automated intervention

Run the `feature-adoption-monitor` drill to build daily monitoring for users stalled at each milestone. Configure the stalled-user detection workflow in n8n:

**Stall definitions:**
- **Stalled at Milestone 1:** Signed up 48+ hours ago, has not completed account setup. Intervention: Intercom in-app message offering guided setup.
- **Stalled at Milestone 2:** Completed setup 48+ hours ago, has not performed first core action. Intervention: Loops email with step-by-step tutorial.
- **Stalled at Milestone 3:** Performed core action 72+ hours ago, has not reached value moment. Intervention: Intercom tooltip pointing to the specific next step.
- **Stalled at Milestone 4:** Reached value moment but no return session within 5 days. Intervention: Loops email highlighting what they accomplished and suggesting next steps.

**The n8n workflow runs daily:**
1. Query PostHog for users matching each stall definition
2. Check Attio to confirm the user has not already received this specific nudge
3. Trigger the appropriate intervention via Intercom API or Loops API
4. Log the nudge in Attio as a note on the contact record (nudge_type, milestone, timestamp)

### 3. Build the milestone monitoring dashboard

Using the `feature-adoption-monitor` drill's dashboard setup, create a PostHog dashboard titled "Activation Milestone Health" with these panels:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Milestone funnel | Funnel chart | Step-by-step conversion from signup through activation |
| Per-milestone completion rates (weekly) | Line chart | One line per milestone, 8-week trend |
| Time-to-milestone distribution | Histogram | Minutes from signup to each milestone |
| Stalled user count by milestone | Bar chart | How many users are stalled at each step |
| Nudge effectiveness | Table | Nudges sent vs. milestone completed within 48 hours |
| Activation rate trend | Line chart | Overall activation rate with threshold line |

### 4. Evaluate against threshold

Run the `threshold-engine` drill to measure results after the 2-week evaluation window. Pass criteria:

- **≥50% activation rate:** At least 50% of new signups reach the `activation_reached` event within 14 days, measured across the full 2-week window.

If PASS: Always-on monitoring and nudges are working. Proceed to Scalable.

If FAIL: Identify the milestone with the highest drop-off from the funnel dashboard. Focus all iteration on that single step:
- If drop-off is at Milestone 2 (configuration): Simplify the setup flow, add pre-filled defaults, or offer a setup wizard.
- If drop-off is at Milestone 3 (first core action): Improve product tour clarity, add sample data, or reduce steps to first action.
- If drop-off is at Milestone 4 (value moment): The product may need to deliver value faster — shorten the feedback loop.
- If drop-off is at return session: Nudge timing or content may be wrong — test different email triggers.

Re-run for another 2-week window after changes.

## Time Estimate

- 4 hours: Build onboarding flow (in-app tours + email sequence)
- 4 hours: Configure stalled-user detection and automated nudges in n8n
- 3 hours: Build PostHog monitoring dashboard
- 2 hours: Monitor and iterate on nudge effectiveness
- 3 hours: Threshold evaluation and iteration

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnel analysis, cohorts, dashboards | Free up to 1M events/month; paid ~$0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app product tours and contextual messages | Essential $29/seat/mo; Advanced $85/seat/mo; Early-stage program up to 90% off year 1 ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Lifecycle email sequences with milestone-based triggers | Free up to 1,000 contacts; paid from $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Daily stalled-user detection workflow | Community Edition free (self-hosted); Cloud from €24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |

## Drills Referenced

- `onboarding-flow` — builds the multi-channel onboarding experience (Intercom tours + Loops emails) keyed to activation milestones
- `feature-adoption-monitor` — deploys stalled-user detection, automated nudges, and the milestone monitoring dashboard
- `threshold-engine` — evaluates pass/fail against the 50% activation threshold
