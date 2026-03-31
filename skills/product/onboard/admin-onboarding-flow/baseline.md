---
name: admin-onboarding-flow-baseline
description: >
  Admin vs User Onboarding — Baseline Run. First always-on automation of the dual onboarding
  paths. Intercom checklists, Loops email sequences, and n8n workflows run continuously.
  PostHog A/B test validates the role-split approach against a control group receiving the
  generic onboarding flow.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Baseline Run"
time: "18 hours setup + 2 weeks observation"
outcome: "≥70% admin setup completion AND ≥60% user activation AND ≥12 percentage point improvement over single-path control"
kpis: ["Admin setup completion rate", "User activation rate", "Team invite rate", "Time to workspace ready (median hours)", "Setup email click-through rate", "Checklist completion rate"]
slug: "admin-onboarding-flow"
install: "npx gtm-skills add product/onboard/admin-onboarding-flow"
drills:
  - posthog-gtm-events
  - onboarding-sequence-automation
  - activation-optimization
---

# Admin vs User Onboarding — Baseline Run

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Run the dual onboarding paths as always-on automation for 50% of new signups, with the remaining 50% on the existing generic onboarding flow as control. Prove that the role-split approach produces a statistically significant improvement in both admin setup completion and user activation. Pass threshold: ≥70% admin setup completion, ≥60% user activation, AND ≥12 percentage point improvement over the control group.

## Leading Indicators

- Admin median time-to-workspace-ready decreasing week over week
- Setup email sequence click-through rate ≥8% (indicating emails drive action)
- Checklist completion rate ≥55% (admins finishing all 6 steps)
- User first-session activation rate ≥30% (users reaching core action in session 1)
- Invited user acceptance rate ≥70% (team members accepting invites)
- Treatment group's combined admin+user activation rate exceeding control by ≥8pp within first week

## Instructions

### 1. Set up comprehensive event tracking

Run the `posthog-gtm-events` drill to establish a complete event taxonomy for both onboarding paths. Define these events:

**Admin path events:**
- `admin_onboarding_started` — admin enters the workspace setup flow
- `admin_checklist_step_completed` with properties: `step_name`, `step_number`, `time_since_signup_minutes`
- `admin_checklist_completed` — all 6 steps done
- `admin_stall_nudge_shown` with properties: `nudge_type`, `stall_step`, `hours_stalled`
- `admin_stall_nudge_clicked` — admin responded to a stall nudge
- `workspace_ready` — composite: billing + permissions + at least 1 integration
- `team_invite_sent` with properties: `invite_count`, `workspace_id`
- `team_invite_accepted` — an invited user joins

**User path events:**
- `user_onboarding_started` — user enters the getting-started flow
- `user_tour_started`, `user_tour_step_completed`, `user_tour_completed`
- `user_first_core_action` — user completes the key activation action
- `activation_reached` with properties: `role`, `time_since_signup_hours`, `activation_action`

**Cross-path events:**
- `onboarding_email_sent`, `onboarding_email_opened`, `onboarding_email_clicked` with `role` and `email_step` properties

Build PostHog funnels for each path and a combined funnel showing the full journey from signup → role classification → path completion → team expansion.

### 2. Wire always-on email automation

Run the `onboarding-sequence-automation` drill to connect PostHog events to Loops email sequences via n8n. Set up two separate automation pipelines:

**Admin pipeline:**
- PostHog `workspace_created` webhook → n8n → Loops creates contact with `user_role: admin` → starts admin email sequence
- PostHog `admin_checklist_step_completed` webhook → n8n → Loops updates contact properties → sequence skips completed-step emails
- PostHog `workspace_ready` webhook → n8n → Loops exits admin from setup sequence, enrolls in "admin ongoing" sequence

**User pipeline:**
- PostHog `team_invite_accepted` webhook → n8n → Loops creates contact with `user_role: user` → starts user email sequence
- PostHog `user_first_core_action` webhook → n8n → Loops updates contact → skips activation nudge emails
- PostHog `activation_reached` webhook → n8n → Loops exits user from onboarding, enrolls in engagement sequence

Test both pipelines end-to-end with test accounts before enabling for real users.

### 3. Optimize the activation bottleneck

Run the `activation-optimization` drill to find and fix the biggest drop-off point in each path. Analyze the PostHog funnels from the Smoke test data plus the first week of Baseline data:

**For admins:** Identify which checklist step has the highest abandonment rate. Common bottlenecks:
- Billing step: reduce friction by offering "skip for now, start free trial" option
- Permissions step: simplify to 2-3 preset templates instead of custom configuration
- Integration step: pre-detect installed tools and auto-suggest the most relevant integration

**For users:** Identify where users drop off in the product tour or before their first core action. Common bottlenecks:
- Tour too long: reduce to 3 steps max
- First action unclear: add a "quick win" action that delivers value in under 60 seconds
- Workspace empty: ensure admins have set up enough context that invited users see a populated workspace

Implement one fix per path per week. Measure impact via PostHog funnels before and after.

### 4. Launch the A/B test

Configure PostHog to split new signups 50/50:
- **Treatment (50%)**: dual onboarding paths (admin setup checklist + user getting-started tour)
- **Control (50%)**: existing generic onboarding flow (same for all users regardless of role)

Use PostHog feature flags to control which experience each user sees. Ensure the randomization is user-level and sticky (same user always sees the same variant across sessions).

**Human action required:** Verify the control group experience is stable and unchanged. Document exactly what the control group sees so you can accurately attribute differences. Review the first 10 signups in each group to confirm correct assignment.

### 5. Monitor weekly and analyze at 2 weeks

Build a PostHog dashboard comparing treatment vs control:
- Admin setup completion rate (treatment admins vs control admins)
- User activation rate (treatment users vs control users)
- Combined activation rate (all treatment users vs all control users)
- Time to workspace ready (treatment admins only — no equivalent in control)
- Team invite rate (both groups)
- Email engagement by path and step

At the end of week 2, analyze:
- Is the difference statistically significant? (Use PostHog experiment analysis or manual chi-squared test. Need 95% confidence.)
- What is the absolute improvement in each metric?
- Are there any negative effects? (e.g., higher support tickets, more confusion)

### 6. Evaluate against threshold

Measure against pass criteria:
- **Admin setup completion** (treatment group): ≥70%
- **User activation** (treatment group): ≥60%
- **Improvement over control**: ≥12 percentage points on the combined activation metric

If PASS: roll out the dual path to 100% of signups. Document the winning configuration. Proceed to Scalable.

If FAIL: diagnose which metric is short. If admin completion is low, simplify the setup flow further. If user activation is low, improve the user onboarding path. If improvement over control is insufficient, investigate whether the generic flow is actually better for certain user segments.

## Time Estimate

- 4 hours: comprehensive event tracking setup
- 6 hours: always-on email automation wiring (admin + user pipelines)
- 4 hours: activation bottleneck analysis and fixes
- 2 hours: A/B test configuration and launch
- 2 hours: dashboard setup and monitoring configuration
- 2 weeks observation (~30 min/day reviewing dashboards)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Analytics, feature flags, experiments, funnels | Free tier: 1M events/mo (https://posthog.com/pricing) |
| Intercom | Checklists, product tours, in-app messages | Essential: $29/seat/mo billed annually (https://www.intercom.com/pricing) |
| Loops | Lifecycle email sequences (admin + user paths) | Paid: from $49/mo (https://loops.so/pricing) |
| n8n | Automation (PostHog→Loops webhooks, routing) | Free self-hosted; Cloud Starter: $20/mo (https://n8n.io/pricing) |

**Estimated monthly cost at Baseline:** ~$50-100/mo (Intercom $29 + Loops $0-49 + n8n $0-20)

## Drills Referenced

- `posthog-gtm-events` — establishes the full event taxonomy for admin and user onboarding tracking
- `onboarding-sequence-automation` — wires PostHog events to Loops email sequences via n8n for always-on delivery
- `activation-optimization` — identifies and fixes the biggest activation bottleneck in each onboarding path
