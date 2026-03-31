---
name: integration-setup-assistant-baseline
description: >
  Integration Setup Assistant -- Baseline Run. Deploy the integration wizard to all
  new users with always-on automation. Behavioral email sequences and continuous
  failure recovery run without manual intervention. First always-on level.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=65% integration completion rate, >=15pp lift over unguided control group"
kpis: ["Integration setup completion rate", "Integration success rate per integration", "Time to first integration (median)", "Post-integration 7-day retention", "Rescue recovery rate"]
slug: "integration-setup-assistant"
install: "npx gtm-skills add product/onboard/integration-setup-assistant"
drills:
  - onboarding-sequence-automation
  - activation-optimization
  - threshold-engine
---

# Integration Setup Assistant -- Baseline Run

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

>=65% integration completion rate among all new users, with >=15 percentage point lift over the unguided control group. The wizard, email sequences, and failure recovery all run continuously without manual intervention.

## Leading Indicators

- Wizard checklist completion rate stable or improving week over week
- Per-integration success rates all above 50%
- Rescue workflow recovering >25% of stalled users
- Email sequence open rates >35%, click rates >8%
- Time to first integration decreasing week over week (median <10 minutes)

## Instructions

### 1. Wire behavioral email sequences to integration events

Run the `onboarding-sequence-automation` drill to connect PostHog integration events to Loops email sequences via n8n. Build these automated email flows:

**Integration nudge sequence (for users who have NOT started the wizard after 24 hours):**
- Email 1 (24h after signup, if `integration_wizard_started` is false): Subject: "Connect [Top Integration] in 2 minutes". Body: explains what the integration does, deep-links to the setup page. CTA: "Start connecting".
- Email 2 (48h after signup, if still no integration): Subject: "Here's how [similar company] uses [Product] with [Integration]". Body: use case walkthrough. CTA: deep-link to integration setup.
- Email 3 (72h after signup, if still no integration): Subject: "Need help connecting?". Body: offer to help, link to help article and Cal.com booking link for setup call.
- Exit condition: user fires `integration_setup_succeeded` for any integration.

**Integration failure recovery sequence (triggered by `integration_setup_failed`):**
- Email 1 (immediate, via Loops transactional): Subject: "Your [Integration] setup hit a snag -- here's the fix". Body: specific troubleshooting steps based on `error_type` property. CTA: deep-link to retry.
- Email 2 (24h after failure, if not resolved): Subject: "Still having trouble with [Integration]?". Body: alternative setup method or offer human help.
- Exit condition: user fires `integration_setup_succeeded` for that integration.

**Post-connection activation sequence (triggered by `integration_wizard_completed`):**
- Email 1 (immediate): Subject: "Your integrations are live -- here's what to do next". Body: guide to the first high-value action enabled by the connected integration.
- Email 2 (48h after completion): Subject: "Have you tried [feature enabled by integration]?". Body: feature walkthrough with specific steps.

Configure n8n to sync all email events (sent, opened, clicked) back to PostHog as `onboarding_email_sent`, `onboarding_email_opened`, `onboarding_email_clicked` events with properties `{sequence: "integration_nudge|failure_recovery|post_connection", email_step: N}`.

### 2. Optimize the biggest activation bottleneck

Run the `activation-optimization` drill focused specifically on the integration setup funnel:

1. Pull the PostHog funnel from Smoke: `integration_wizard_started` -> `integration_step_started` -> `integration_setup_attempted` -> `integration_setup_succeeded` -> `integration_wizard_completed`
2. Identify the step with the largest drop-off
3. For that step, diagnose the root cause:
   - **Drop-off at wizard_started -> step_started:** Users see the checklist but do not click. Fix: improve checklist step descriptions, add urgency ("Connect now to start seeing value"), or move the checklist higher in the UI
   - **Drop-off at step_started -> setup_attempted:** Users visit the integration page but do not try to connect. Fix: simplify the setup UI, add the Intercom product tour to guide them through the connect flow
   - **Drop-off at setup_attempted -> setup_succeeded:** Users try but fail. Fix: improve error messages, add the contextual bot for this integration, pre-fill configuration where possible
   - **Drop-off at setup_succeeded -> wizard_completed:** Users connect one integration but stop. Fix: improve the checklist's next-step guidance, highlight the value of additional integrations
4. Implement one fix for the biggest drop-off point

**Human action required:** Review the proposed fix before deploying. If the fix involves UI changes, approve the mockup. If the fix involves copy changes, review the new copy.

### 3. Roll out to 50% of new users with a control group

Configure a PostHog feature flag `integration-wizard-baseline` to roll out to 50% of new signups. The other 50% get the existing unguided experience as a control group. Run for 2 weeks.

Track both groups in PostHog using the feature flag as a breakdown dimension on all integration events. Compare:
- Integration completion rate (wizard group vs control)
- Time to first integration
- 7-day retention rate
- Support ticket volume related to integrations

### 4. Monitor weekly and iterate

At the end of week 1:
- Pull the PostHog funnel for both groups
- Compare integration completion rates
- Check email sequence performance: open rates, click rates, and whether email-prompted users complete setup
- Check rescue workflow stats: how many users stalled, how many recovered
- If the wizard group is underperforming, diagnose and fix before week 2

At the end of week 2:
- Run final comparison

### 5. Evaluate against threshold

Run the `threshold-engine` drill:

- **Primary metric:** Integration completion rate for the wizard group
- **Pass threshold:** >=65% AND >=15pp lift over control
- **Secondary metrics:** per-integration success rates, rescue recovery rate, email sequence engagement, 7-day retention

If PASS: Roll out the wizard to 100% of new users. Document the final funnel metrics and per-integration breakdown. Proceed to Scalable.

If FAIL: If completion rate is <65% but lift is clear, extend the test for another week. If lift is <15pp, the wizard is not adding enough value -- investigate whether the integrations chosen are wrong, the guidance is insufficient, or the rescue workflow is not reaching users.

## Time Estimate

- 4 hours: Email sequence build and n8n automation (Step 1)
- 3 hours: Activation bottleneck diagnosis and fix (Step 2)
- 1 hour: Feature flag setup and rollout (Step 3)
- 4 hours: Weekly monitoring and iteration (Step 4, 2 hours per week)
- 4 hours: Final analysis and threshold evaluation (Step 5)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Funnels, cohorts, feature flags, experiments | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Checklists, bots, in-app messages | Essential: $29/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| n8n | Email automation, rescue workflows, event sync | Free self-hosted; Cloud Starter: $24/mo ([n8n.io/pricing](https://n8n.io/pricing/)) |
| Loops | Onboarding and recovery email sequences | Starter: $49/mo for unlimited emails ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated play-specific cost at Baseline:** ~$50-100/mo (Loops Starter + additional Intercom bot conversations if beyond free tier)

## Drills Referenced

- `onboarding-sequence-automation` -- wires behavioral email sequences to PostHog integration events via n8n and Loops
- `activation-optimization` -- identifies and fixes the biggest drop-off point in the integration setup funnel
- `threshold-engine` -- evaluates pass/fail against the 65% completion and 15pp lift thresholds
