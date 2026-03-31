---
name: invite-mechanism-smoke
description: >
  Team Invite System — Smoke Test. Build a single in-product invite surface, instrument
  the full invite funnel in PostHog, and validate that users will invite teammates when
  given a frictionless path. Run once with a small cohort to prove signal before automating.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: ">=30% of test cohort users open the invite form AND >=1 invite accepted within 7 days"
kpis: ["Invite form open rate", "Invites sent per user", "Acceptance rate", "Time to accept"]
slug: "invite-mechanism"
install: "npx gtm-skills add product/upsell/invite-mechanism"
drills:
  - invite-flow-setup
  - threshold-engine
---

# Team Invite System — Smoke Test

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

A working invite flow deployed at one high-intent product entry point (team settings or share button), with PostHog tracking every step from form open through invitee first action. At least 30% of users in a small test cohort (10-50 active users) open the invite form, and at least one invitation is accepted within 7 days. This proves that users will invite when given a clear path.

## Leading Indicators

- Users discover the invite surface without prompting (organic `invite_form_opened` events)
- Invitees click the accept link within 24 hours (fast cycle time = strong social pull)
- Invited users take a meaningful action within their first session (the acceptance flow works)
- Zero invite email bounces (deliverability is clean)

## Instructions

### 1. Build the invite flow

Run the `invite-flow-setup` drill to build the in-product invite mechanism. For Smoke, focus on ONE entry point only — pick the highest-intent location:

- **If your product has team settings:** Build the invite form there. Users who visit team settings are already thinking about collaboration.
- **If your product has a "Share" action:** Build an invite prompt that appears after a share action. Users sharing content are demonstrating collaborative intent.

Configure the invite form, invitation email via Loops, acceptance flow, and PostHog event tracking as specified in the drill. Wire the n8n workflow to route accepted invites to Attio.

**Human action required:** Review the invite email copy before sending. Ensure the accept link lands the invitee in the right context (shared resource or team workspace), not a generic dashboard. Test the full flow yourself — send an invite to a test email, accept it, and verify every PostHog event fires.

### 2. Deploy to a small test cohort

Enable the invite surface for 10-50 active users. Use PostHog feature flags to control the rollout. Choose users who:
- Have been active for at least 14 days (they know the product)
- Are on a plan with available seats (no seat-limit blocker)
- Have not previously invited anyone (measuring first-invite behavior)

Do not announce the feature. The Smoke test measures organic discovery and usage — if users need to be told to invite, the surface is not well-placed.

### 3. Observe for 7 days

Monitor the PostHog invite funnel daily. Track:
- How many users in the cohort opened the invite form (`invite_form_opened`)
- How many sent at least one invite (`invite_sent`)
- How many invites were accepted (`invite_accepted`)
- How quickly invitees accepted (time from `invite_sent` to `invite_accepted`)
- Whether accepted invitees took a first action (`invited_user_first_action`)

Note qualitative signals: Did anyone invite multiple people? Did anyone abandon the form? Did any invite emails bounce?

### 4. Evaluate against threshold

Run the `threshold-engine` drill to measure against the pass criteria:
- **>=30% invite form open rate** (users in cohort who opened the form / total cohort size)
- **>=1 invite accepted** (at least one invitation was accepted within the 7-day window)

If PASS: The invite surface is discoverable, and users will invite when given a clear path. Proceed to Baseline.
If FAIL on form open rate: The entry point is wrong or the surface is not visible enough. Move the invite surface to a higher-traffic location or add a subtle prompt.
If FAIL on acceptance: The invitation email is not compelling, the accept flow has too much friction, or the invitees are not the right audience. Review the email copy and the signup flow.

## Time Estimate

- 4 hours: Build invite flow (form, email template, acceptance flow, PostHog events, n8n wiring)
- 1 hour: Test end-to-end and fix issues
- 1 hour: Configure feature flag and deploy to test cohort
- 2 hours: Monitor over 7 days and evaluate results

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, feature flags | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app messages (optional at Smoke) | From $29/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Invitation emails, transactional sends | Free up to 1,000 contacts; transactional email free on all paid plans from $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Attio | CRM contact routing | Free up to 3 users ([attio.com](https://attio.com)) |
| n8n | Webhook workflows | Free self-hosted; cloud from $24/mo ([n8n.io/pricing](https://n8n.io/pricing/)) |

**Estimated play-specific cost at Smoke:** $0 (all tools within free tiers for a 10-50 user test)

## Drills Referenced

- `invite-flow-setup` — builds the complete in-product invite mechanism with form, email, acceptance flow, and tracking
- `threshold-engine` — evaluates invite funnel metrics against pass/fail thresholds
