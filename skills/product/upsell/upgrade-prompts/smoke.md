---
name: upgrade-prompts-smoke
description: >
  In-App Upgrade CTAs — Smoke Test. Deploy one contextual upgrade prompt on the
  highest-converting trigger and measure whether users click.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥20% CTR on upgrade prompt from ≥30 impressions"
kpis: ["Prompt CTR", "Prompt-to-upgrade-start rate", "Impressions count"]
slug: "upgrade-prompts"
install: "npx gtm-skills add product/upsell/upgrade-prompts"
drills:
  - upgrade-prompt
  - threshold-engine
---

# In-App Upgrade CTAs — Smoke Test

> **Stage:** Product → Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

One upgrade prompt live on the single highest-intent trigger (feature gate or limit proximity). At least 30 users see the prompt. At least 20% click through to the upgrade page. This proves that contextual prompts tied to real usage moments generate upgrade intent.

## Leading Indicators

- Users encountering the trigger condition at the expected rate (confirms the trigger fires)
- Prompt renders without errors in PostHog live events (confirms instrumentation)
- At least 5 clicks within the first 48 hours (early signal before full measurement window)

## Instructions

### 1. Identify the highest-intent upgrade trigger

Run the `upgrade-prompt` drill, Step 1 only. Pick ONE trigger to test — the one most likely to generate clicks:

- **Feature gate** (recommended first choice): User attempts a premium-only feature. The prompt appears immediately in context. This trigger has the highest intent because the user just tried to do the thing.
- **Limit proximity** (second choice): User is at 80%+ of a plan limit. The prompt appears contextually when they view usage or try to create another item.

Do NOT test growth signals or time-based triggers at Smoke. Those require larger samples and longer measurement windows.

### 2. Deploy the prompt

Run the `upgrade-prompt` drill, Steps 2-3 for your chosen trigger. Deploy a single in-app prompt using Intercom in-app messages (or your messaging tool). The prompt must:

- Appear in context (at the moment of the trigger, not on next login)
- State what the user gets: "Upgrade to Pro for unlimited [resource]" or "This feature is available on Pro — here's what you'll unlock"
- Include the price difference and a single CTA button linking to the upgrade/checkout page
- Track `upgrade_prompt_shown` and `upgrade_prompt_clicked` events in PostHog with properties: `trigger_type`, `prompt_surface`, `plan_current`, `user_id`

**Human action required:** Review the prompt copy before deploying. Verify the upgrade checkout page exists and works. Deploy the prompt to all users who hit the trigger (no sampling at Smoke).

### 3. Instrument the funnel

Using PostHog, verify these events fire correctly:

| Event | When | Properties |
|-------|------|------------|
| `upgrade_prompt_shown` | Prompt renders in the UI | `trigger_type`, `plan_current` |
| `upgrade_prompt_clicked` | User clicks the CTA | `trigger_type`, `plan_current` |
| `upgrade_started` | User lands on the upgrade/checkout page | `trigger_type`, `plan_current` |

Open PostHog Live Events. Trigger the condition yourself (e.g., attempt the gated feature on a free account). Confirm all 3 events appear with correct properties. If any event is missing, fix the instrumentation before proceeding.

### 4. Run for 1 week and evaluate

Let the prompt run for 7 days. Do not change the copy or targeting mid-run.

Run the `threshold-engine` drill to evaluate: query PostHog for `upgrade_prompt_shown` count and `upgrade_prompt_clicked` count. Calculate CTR = clicked / shown.

**Pass:** CTR ≥ 20% from ≥ 30 impressions. Proceed to Baseline.
**Fail:** CTR < 20%. Diagnose: Was the trigger firing at the right moment? Was the copy specific to the user's action? Was the CTA button visible? Revise and re-run.

## Time Estimate

- 1 hour: Identify trigger and review plan limits/feature gates
- 1.5 hours: Build and deploy the in-app prompt with Intercom
- 1 hour: Instrument PostHog events and verify in Live Events
- 0.5 hours: Review after 48 hours for early signal
- 1 hour: Final evaluation after 7 days

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnel measurement | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app message delivery | Essential $29/seat/mo; in-app messaging included ([intercom.com/pricing](https://www.intercom.com/pricing)) |

## Drills Referenced

- `upgrade-prompt` — defines the trigger taxonomy and builds the contextual prompt with tracking
- `threshold-engine` — evaluates CTR against the 20% pass threshold and recommends next action
