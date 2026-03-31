---
name: upgrade-prompts-baseline
description: >
  In-App Upgrade CTAs — Baseline Run. Always-on upgrade prompts across 3 trigger
  types with automated email follow-up and CRM routing for high-value accounts.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥15% CTR across all triggers, ≥5% prompt-to-upgrade conversion rate"
kpis: ["Prompt CTR by trigger type", "Prompt-to-upgrade conversion rate", "Revenue attributed to prompts", "Email follow-up conversion rate"]
slug: "upgrade-prompts"
install: "npx gtm-skills add product/upsell/upgrade-prompts"
drills:
  - upgrade-prompt
  - posthog-gtm-events
  - lead-capture-surface-setup
---

# In-App Upgrade CTAs — Baseline Run

> **Stage:** Product → Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Three trigger types live and always-on: feature gate, limit proximity, and growth signals. Each trigger delivers a contextual in-app prompt plus an automated email follow-up for users who saw the prompt but did not click. High-value accounts route to sales via Attio expansion deals. Prompt-to-upgrade conversion rate ≥5% sustained over 2 weeks.

## Leading Indicators

- All 3 trigger types firing at expected volumes in PostHog (confirms trigger logic)
- Email follow-up sequences sending within 24-48 hours of prompt impression (confirms automation)
- At least 1 expansion deal created in Attio from high-value account routing (confirms CRM integration)
- Prompt dismissal rate below 70% (confirms prompts are not annoying users)

## Instructions

### 1. Expand to 3 trigger types

Run the full `upgrade-prompt` drill (all 6 steps). Build detection and prompts for:

- **Feature gate** (validated at Smoke): User attempts a premium-only feature. In-app modal with feature value prop and upgrade CTA.
- **Limit proximity**: User at 80%+ of a plan limit. In-app banner (not modal — less intrusive) showing current usage and upgrade benefit.
- **Growth signal**: User added 3+ team members in 30 days or usage volume doubled. In-app tooltip or banner highlighting team/volume features on the next plan.

Each trigger must fire the `upgrade_prompt_shown` event with `trigger_type` property so you can measure per-trigger performance.

### 2. Set up full event tracking

Run the `posthog-gtm-events` drill to instrument the complete upgrade prompt funnel:

| Event | When | Key Properties |
|-------|------|----------------|
| `upgrade_prompt_eligible` | User enters a trigger cohort | `trigger_type`, `plan_current`, `usage_pct` (for limits) |
| `upgrade_prompt_shown` | Prompt renders | `trigger_type`, `prompt_surface`, `prompt_variant` |
| `upgrade_prompt_clicked` | CTA clicked | `trigger_type`, `prompt_surface` |
| `upgrade_prompt_dismissed` | User closes/ignores prompt | `trigger_type`, `prompt_surface` |
| `upgrade_started` | User reaches checkout page | `trigger_type`, `plan_target` |
| `upgrade_completed` | Payment processed | `trigger_type`, `plan_target`, `revenue_delta_monthly` |

Build a PostHog funnel insight for each trigger type: eligible → shown → clicked → started → completed. Save as "Upgrade Prompts — [Trigger Type] Funnel."

### 3. Build email follow-up automation

Run the `upgrade-prompt` drill, Step 4. For users who saw a prompt but did not click within 24 hours, trigger a Loops transactional email:

- **Feature gate follow-up** (send 24h after): "Yesterday you tried [feature]. Here's how [feature] works on Pro, and what teams like yours use it for." Include a personalized usage stat and a direct upgrade link.
- **Limit proximity follow-up** (send 48h after): "You're using [X] of [Y] [resource]. Here's what happens when you hit the limit, and how Pro removes it." Include current usage numbers.
- **Growth signal follow-up** (send 48h after): "Your team grew to [N] members this month. Pro includes advanced permissions, team analytics, and priority support."

Each email links to the upgrade page with UTM parameters: `utm_source=loops&utm_medium=email&utm_campaign=upgrade_prompt_{trigger_type}`.

### 4. Route high-value accounts to sales

Run the `upgrade-prompt` drill, Step 5. Using n8n, build a workflow that:

1. Queries PostHog daily for accounts where `upgrade_prompt_shown` fired AND account has ≥10 seats OR ≥$X usage signals
2. Creates an expansion deal in Attio using the `lead-capture-surface-setup` drill's CRM routing pattern
3. Attaches the trigger data to the deal: which prompt they saw, their current usage, and the recommended target plan
4. Assigns to the account owner in Attio

**Human action required:** Define the revenue threshold for sales routing (e.g., accounts with estimated ACV > $5K/year). Sales team must acknowledge and follow up on routed deals within 48 hours.

### 5. Set frequency caps

Configure prompt suppression rules in Intercom or your messaging tool:

- Maximum 1 upgrade prompt per user per 7 days (across all trigger types)
- If a user dismisses 2 prompts in 14 days, suppress all prompts for 30 days
- If a user clicked but did not upgrade, do not show the same trigger prompt again for 14 days (the email follow-up handles re-engagement)

Track `upgrade_prompt_suppressed` events in PostHog with `reason` property.

### 6. Evaluate after 2 weeks

Run the `threshold-engine` drill. Query PostHog:

- Overall CTR: `upgrade_prompt_clicked / upgrade_prompt_shown` across all triggers
- Per-trigger CTR (identify which trigger converts best)
- Prompt-to-upgrade rate: `upgrade_completed / upgrade_prompt_shown`
- Email follow-up contribution: upgrades where the last touch before checkout was the email

**Pass:** CTR ≥ 15% across all triggers AND prompt-to-upgrade conversion ≥ 5%. Proceed to Scalable.
**Fail:** If CTR < 15%, diagnose by trigger type — one trigger may be dragging down the average. If conversion < 5% but CTR is high, the upgrade page or pricing is the bottleneck, not the prompt.

## Time Estimate

- 3 hours: Build and deploy prompts for 2 new trigger types (limit proximity + growth signal)
- 3 hours: Instrument all 6 PostHog events and build per-trigger funnels
- 4 hours: Build Loops email follow-up sequences (3 trigger-specific emails)
- 2 hours: Build n8n workflow for high-value account routing to Attio
- 1 hour: Configure frequency caps and suppression rules
- 3 hours: Monitor over 2 weeks and evaluate

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, cohorts | Free tier: 1M events/mo; paid ~$0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app prompt delivery | Essential $29/seat/mo; Advanced $85/seat/mo for outbound messaging add-on ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Triggered email follow-ups | Free under 1K contacts; paid from $49/mo with unlimited sends ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Automation for CRM routing | Self-hosted free; Cloud from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | CRM for expansion deal routing | Free tier available; paid from $29/seat/mo ([attio.com/pricing](https://attio.com/pricing)) |

## Drills Referenced

- `upgrade-prompt` — full trigger detection, prompt design, email follow-up, and sales routing workflow
- `posthog-gtm-events` — instruments the 6-event upgrade prompt funnel in PostHog
- `lead-capture-surface-setup` — CRM routing pattern used for high-value account deal creation
