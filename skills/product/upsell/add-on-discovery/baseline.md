---
name: add-on-discovery-baseline
description: >
  Module Cross-Sell — Baseline Run. Deploy always-on add-on discovery for your top add-on
  with full funnel tracking, automated trigger detection, and email fallback. Validate that
  cross-sell conversion sustains over 2 weeks.
stage: "Product > Upsell"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥10% of triggered users activate the add-on within 14 days of first impression"
kpis: ["Add-on activation rate", "Cross-sell revenue", "ARPU lift", "Discovery-to-activation time"]
slug: "add-on-discovery"
install: "npx gtm-skills add product/upsell/add-on-discovery"
drills:
  - addon-discovery-surface-build
  - posthog-gtm-events
  - addon-cross-sell-health-monitor
---

# Module Cross-Sell — Baseline Run

> **Stage:** Product → Upsell | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

The add-on discovery system runs continuously without manual intervention. Trigger detection fires daily via n8n. Users who match the trigger see in-app surfaces; those who do not engage in-app receive an email nudge 48 hours later. At least 10% of triggered users activate the add-on within 14 days. Cross-sell revenue from this add-on is measurable and attributable.

## Leading Indicators

- n8n trigger detection workflow runs daily without errors
- In-app surfaces are shown to 100% of eligible triggered users within 24 hours
- Email nudges fire for users who did not engage in-app
- Dismissal rate remains below 50%
- At least 3 add-on activations in the first week

## Instructions

### 1. Instrument full-funnel tracking

Run the `posthog-gtm-events` drill to ensure complete event coverage for the cross-sell funnel. You need every event from the `addon-discovery-surface-build` drill flowing reliably: `addon_discovery_impression`, `addon_discovery_clicked`, `addon_activation_started`, `addon_activated`, `addon_discovery_dismissed`. Build a PostHog funnel insight showing the full conversion path. Verify events are flowing by checking PostHog Live Events.

### 2. Deploy always-on discovery

Run the full `addon-discovery-surface-build` drill for your proven add-on (the one that passed Smoke). This time, complete all 6 steps:

- Step 1: Refine the trigger map using Smoke data — adjust the threshold if the trigger fired too early or too late
- Step 2: Confirm all PostHog events are instrumented (done in step 1 above)
- Step 3: Deploy both tooltip AND banner surfaces. Show the tooltip at the specific UI interaction point; show the banner on the related settings/features page
- Step 4: Build the n8n daily trigger detection workflow. This is the transition from manual to always-on — the workflow queries PostHog daily, identifies newly triggered users, activates their feature flag for the in-app surface, and enqueues email nudges for non-engagers after 48 hours
- Step 5: Route high-value accounts to Attio expansion deals if the account's potential add-on revenue exceeds $200/mo
- Step 6: Implement all fatigue controls (1 surface per session, 2 add-ons per week max, suppress after 2 dismissals for 30 days)

### 3. Set up monitoring

Run the `addon-cross-sell-health-monitor` drill to build the monitoring layer. Specifically:
- Build the cross-sell funnel in PostHog (Step 1)
- Build the cross-sell dashboard (Step 2)
- Set up the daily alert workflow (Step 3, daily check only — skip weekly and monthly for now)

Review the dashboard daily during the 2-week baseline window.

### 4. Evaluate against threshold

After 14 days, measure: of all users who received at least one add-on discovery impression, what percentage activated the add-on? Target: ≥10%. Also measure:

- **Cross-sell revenue**: total new MRR from add-on activations during the window
- **ARPU lift**: compare ARPU of cross-sold users vs. non-cross-sold users
- **Time to activation**: median days between first impression and activation

If PASS (≥10% activation rate), proceed to Scalable. If FAIL:
- Activation rate 5-9%: the funnel is working but leaky. Use PostHog session recordings to find where users drop off between click and activation. Fix the activation flow.
- Activation rate 1-4%: users are clicking but not converting. The add-on's value proposition or pricing may not match the trigger. Test different copy or offer a trial.
- Activation rate <1%: the trigger is wrong or the add-on does not solve the user's problem at this point. Revisit the trigger map.

## Time Estimate

- 3 hours: Refine trigger map and update cohort criteria from Smoke data
- 4 hours: Build n8n daily trigger detection workflow and email nudge automation
- 3 hours: Deploy tooltip + banner surfaces with fatigue controls
- 2 hours: Set up PostHog cross-sell funnel, dashboard, and daily alerts
- 2 hours: Configure Attio deal routing for high-value accounts
- 2 hours: Daily monitoring and 14-day evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Funnel tracking, cohorts, feature flags, dashboards | Free up to 1M events/mo — https://posthog.com/pricing |
| Intercom | In-app tooltips, banners, product tours | Included in existing plan — https://www.intercom.com/pricing |
| Loops | Email nudges for non-engagers | Free up to 1,000 contacts — https://loops.so/pricing |
| n8n | Daily trigger detection, email enqueue, alerting | Free self-hosted — https://n8n.io/pricing |
| Attio | Expansion deal tracking, custom attributes | Included in existing plan — https://attio.com/pricing |

## Drills Referenced

- `addon-discovery-surface-build` — full build of trigger detection, in-app surfaces, email nudges, and fatigue controls
- `posthog-gtm-events` — ensures all cross-sell funnel events are instrumented and flowing
- `addon-cross-sell-health-monitor` — dashboard, funnel, and daily alerts for the cross-sell pipeline
