---
name: freemium-feature-upsell-baseline
description: >
  Freemium to Paid Conversion — Baseline Run. Always-on detection of free users hitting limits
  and encountering feature gates, automated upgrade prompts across multiple trigger types,
  full funnel tracking, and prompt performance monitoring.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Baseline Run"
time: "20 hours over 3 weeks"
outcome: "≥8% of prompted free users complete a paid upgrade within 14 days"
kpis: ["Free-to-paid conversion rate", "Prompt CTR by trigger type", "Revenue per conversion", "Days to convert", "Prompt fatigue rate"]
slug: "freemium-feature-upsell"
install: "npx gtm-skills add product/upsell/freemium-feature-upsell"
drills:
  - posthog-gtm-events
  - feature-adoption-monitor
  - upgrade-prompt-health-monitor
---

# Freemium to Paid Conversion — Baseline Run

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

8% or more of free users who receive an upgrade prompt (any trigger type) complete a paid upgrade within 14 days. This is the first always-on version: the system runs continuously, detecting limit proximity and feature gate encounters across all free users, delivering contextual prompts and follow-up emails without manual intervention, and tracking the full funnel from prompt to payment. The system must prove that conversion holds over time, not just in a one-week burst.

## Leading Indicators

- Daily prompt volume is stable or growing (the detection system is consistently finding upgrade-ready users)
- Prompt CTR by trigger type: limit_proximity should convert at 8-12%, feature_gate at 5-8%, time_based at 3-5%. If any trigger type is below its range, the messaging or timing is wrong.
- Email follow-up open rate >30% and click rate >5% (the Loops sequence is adding value beyond the in-app prompt)
- Prompt fatigue rate below 10% of active free users (the suppression system is working)
- Days from signup to conversion trending downward (the funnel is accelerating)

## Instructions

### 1. Expand event tracking to cover the full funnel

Run the `posthog-gtm-events` drill to instrument every touchpoint in the freemium conversion pipeline. Add these events beyond what Smoke configured:

| Event | When Fired | Properties |
|-------|-----------|-----------|
| `feature_gate_hit` | Free user encounters a gated premium feature | `feature_name`, `user_plan`, `page`, `gate_type` (lock/blur/disabled) |
| `feature_gate_preview_engaged` | User interacts with the gate preview | `feature_name`, `preview_type`, `engagement_seconds` |
| `upgrade_email_sent` | Follow-up email fires via Loops | `trigger_type`, `email_variant`, `days_since_prompt` |
| `upgrade_email_opened` | User opens the follow-up email | `trigger_type`, `email_variant` |
| `upgrade_email_clicked` | User clicks through from the email | `trigger_type`, `email_variant` |
| `pricing_page_viewed` | User lands on the pricing page | `referrer_source` (prompt/email/organic), `user_plan` |
| `checkout_started` | User enters the Stripe checkout flow | `target_plan`, `trigger_type` |
| `checkout_abandoned` | User leaves checkout without completing | `target_plan`, `step_abandoned`, `time_in_checkout_seconds` |

Build PostHog funnels:
- **Prompt-to-paid**: `upgrade_prompt_shown` -> `upgrade_prompt_clicked` -> `pricing_page_viewed` -> `checkout_started` -> `upgrade_completed`. Break down by `trigger_type`.
- **Gate-to-paid**: `feature_gate_hit` -> `feature_gate_preview_engaged` -> `upgrade_prompt_clicked` -> `upgrade_completed`. Break down by `feature_name`.
- **Email-to-paid**: `upgrade_email_sent` -> `upgrade_email_opened` -> `upgrade_email_clicked` -> `upgrade_completed`. Break down by `email_variant`.

### 2. Expand to multiple trigger types

The Smoke test validated one trigger (limit proximity). Now add all trigger types using the `upgrade-prompt` drill's full configuration:

- **Limit proximity** (proven in Smoke): Free user at 80%+ of a plan limit. In-app banner near the limited resource.
- **Feature gate**: Free user encounters a premium feature. Show a locked-state preview with "Upgrade to unlock" and "Start 7-day trial" CTAs. Implement using PostHog feature flags to control which features are gated.
- **Growth signal**: Free user added 3+ team members in a month, or usage volume doubled in 2 weeks. Show a team-focused upgrade message: "Your team is growing. Pro includes advanced permissions and team analytics."
- **Time-based**: Free user active for 30+ days with consistent usage (3+ sessions/week). Send a Loops email: "You have been using [product] for a month. Here is what Pro users accomplish that free users cannot."

Configure suppression rules across all triggers:
- Maximum 1 in-app prompt per 7-day period, regardless of trigger type
- If a user has dismissed 3+ prompts in 14 days, suppress all in-app prompts for that user for 14 days and switch to email-only
- Never show a prompt to a user who has an active trial
- Never show a limit proximity prompt to a user who just expanded their usage (give them 48 hours to naturally upgrade)

### 3. Set up email follow-up sequences

Configure Loops transactional emails as a secondary channel for users who do not convert from the in-app prompt:

- **Limit proximity follow-up**: 24 hours after the prompt, if the user did not click: "You are at [X]% of your [resource] limit. Here is what happens when you hit it, and how Pro removes the constraint." Include a personalized usage summary.
- **Feature gate follow-up**: 48 hours after the gate encounter: "You discovered [feature name] yesterday. Here is how [similar company or persona] uses it to [specific outcome]." Include a deep link to start a trial of that specific feature.
- **Growth signal follow-up**: 3 days after detecting the growth signal: "Your team grew to [N] people this month. Here is what teams your size typically need from Pro." Include a comparison table: what they have now vs. what Pro adds.

### 4. Build the performance monitoring layer

Run the `feature-adoption-monitor` drill to track how free users discover and engage with premium features. This creates visibility into the top of the freemium funnel: which premium features are free users encountering, which ones create the most upgrade intent, and where users stall.

Run the `upgrade-prompt-health-monitor` drill to build the measurement and alerting layer:
- Prompt-to-upgrade funnels per trigger type
- Health dashboard with 7 panels and weekly delivery
- Dynamic cohorts: prompt-converted, prompt-fatigued, prompt-high-intent, prompt-never-shown
- Daily degradation detection with Slack and Attio alerting
- Revenue attribution per trigger type

### 5. Launch as always-on with feature flag control

Deploy the full system behind PostHog feature flags:
- `freemium-upsell-limit-prompt`: controls limit proximity prompts (flag from Smoke, now expanded to all free users)
- `freemium-upsell-gate-prompt`: controls feature gate prompts
- `freemium-upsell-growth-prompt`: controls growth signal prompts
- `freemium-upsell-time-prompt`: controls time-based email nudges

Roll out each trigger type sequentially with 24 hours between launches. Monitor the upgrade-prompt-health-monitor dashboard after each rollout. If any trigger type causes a spike in the prompt-fatigued cohort, pause that trigger and adjust frequency or targeting before re-enabling.

### 6. Evaluate against threshold

Measure at the end of 3 weeks (allowing time for the 14-day conversion window to close for all cohorts):

- **Primary metric**: Overall free-to-paid conversion rate for prompted users. Target: >=8%.
- **By trigger**: Limit proximity >=10%, feature gate >=6%, growth signal >=5%, time-based >=3%.
- **Revenue metric**: Average revenue per conversion >= your product's standard paid plan price (validates users are not just converting to the cheapest plan).
- **Health metric**: Prompt fatigue rate <10% of active free users.

**Pass (>=8% overall, fatigue <10%):** The always-on system converts at a sustainable rate. Proceed to Scalable to find the 10x multiplier.

**Fail:** Diagnose by trigger type:
- If limit proximity dropped from Smoke levels: suppression rules may be too aggressive, or the always-on cadence feels different from the one-time Smoke prompt. Check session recordings.
- If feature gates underperform: the locked-state preview is not compelling enough, or the gated features are not ones free users organically encounter. Move gates to higher-traffic features.
- If email follow-ups have low open rates: subject lines are generic. Test including the specific resource or feature name in the subject.
- If checkout abandonment is high: the pricing page has too many options or the checkout has too many steps. Consider a simplified one-click upgrade path from the prompt.

## Time Estimate

- 4 hours: Expand event tracking, build PostHog funnels across all trigger types
- 5 hours: Configure 4 trigger types with prompt copy, suppression rules, and feature flags
- 3 hours: Set up Loops email follow-up sequences for each trigger type
- 4 hours: Deploy feature-adoption-monitor and upgrade-prompt-health-monitor drills
- 4 hours: Sequential rollout, 3-week monitoring, threshold evaluation, documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, cohorts, feature flags, dashboards | Free up to 1M events/mo — https://posthog.com/pricing |
| Intercom | In-app upgrade prompts, feature gate previews | Included in existing plan — https://www.intercom.com/pricing |
| Loops | Email follow-up sequences for each trigger type | Starter $49/mo — https://loops.so/pricing |
| n8n | Usage detection workflows, degradation monitoring | Free self-hosted; Cloud from $24/mo — https://n8n.io/pricing |
| Attio | Deal creation, revenue attribution, alerting | Free tier — https://attio.com/pricing |

**Play-specific cost:** ~$50-75/mo (Loops Starter for email sequences)

## Drills Referenced

- `posthog-gtm-events` — instrument the full conversion funnel: gate events, email events, checkout events, and build PostHog funnels per trigger type
- `feature-adoption-monitor` — track how free users discover and engage with premium features, detect stalled users, and trigger nudges
- `upgrade-prompt-health-monitor` — build the measurement dashboard, degradation detection, prompt fatigue tracking, and revenue attribution per trigger type
