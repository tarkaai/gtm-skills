---
name: freemium-feature-upsell-smoke
description: >
  Freemium to Paid Conversion — Smoke Test. Identify free users approaching plan limits or
  repeatedly hitting feature gates, show one contextual upgrade prompt, and measure whether
  it generates upgrade intent within 7 days.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥5% of prompted free users click upgrade or start a trial within 7 days"
kpis: ["Prompt impression rate", "Prompt CTR", "Trial start rate", "Upgrade click rate"]
slug: "freemium-feature-upsell"
install: "npx gtm-skills add product/upsell/freemium-feature-upsell"
drills:
  - usage-threshold-detection
  - upgrade-prompt
  - threshold-engine
---

# Freemium to Paid Conversion — Smoke Test

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

5% or more of free users who see an upgrade prompt either click the upgrade CTA or start a trial within 7 days. This proves that the prompt is positioned at a moment of real need (the user is hitting a limit or encountering a gate), the value proposition is clear enough to create intent, and the upgrade path has low enough friction to act on. "Prompted free users" means users who fired an `upgrade_prompt_shown` event.

## Leading Indicators

- Free users entering the `usage-imminent` or `usage-critical` cohorts per day (the limit detection system is finding real candidates)
- Prompt impressions per day: are free users organically encountering the upgrade surface through normal product usage
- Time from prompt shown to upgrade click: shorter means the value proposition is compelling at the moment of need
- Prompt dismiss rate: if above 80%, the prompt is showing at the wrong time or the copy is wrong

## Instructions

### 1. Detect free users approaching plan limits

Run the `usage-threshold-detection` drill to build the system that identifies free users approaching their plan caps. Configure it for your freemium model:

- Enumerate every resource that differs between free and paid tiers: seats, projects, storage, API calls, or whatever your product meters
- Define the plan caps per tier in a JSON config accessible to the n8n detection workflow
- Instrument PostHog events: for each metered resource, emit `resource_consumed` events with `account_id`, `resource_type`, `current_count`, `plan_limit`, `plan_tier`, `pct_used`
- Build the daily detection query: find all free accounts at 70%+ of any limit
- Classify urgency: approaching (70-84%), imminent (85-94%), critical (95-100%)
- Create PostHog cohorts for each urgency tier

For the Smoke test, focus on ONE resource that has the clearest limit differential between free and paid. Pick the resource where free users most commonly hit the cap.

### 2. Configure one contextual upgrade prompt

Run the `upgrade-prompt` drill to set up a single upgrade prompt for the highest-urgency trigger. Configure it for `usage-imminent` and `usage-critical` free users:

- **Trigger**: User in the `usage-imminent` or `usage-critical` cohort logs in and navigates to a page related to the metered resource
- **Message**: Tied to the specific limit. Example: "You have used 47 of 50 projects. Upgrade to Pro for unlimited projects — your existing work stays exactly as-is."
- **Surface**: Intercom in-app message. Show as a banner, not a blocking modal. Position it contextually near the resource the user is running out of.
- **CTAs**: Primary: "See Pro plan" (links to pricing page with the user's current usage stats pre-populated). Secondary: "Start 7-day trial" (if your product supports per-feature trials).
- **Suppression**: Do not show the prompt more than once per 7-day period. If the user dismisses it, do not re-show for 14 days.

Define PostHog events:

| Event | When Fired | Properties |
|-------|-----------|-----------|
| `upgrade_prompt_shown` | Prompt renders in viewport | `trigger_type`, `resource_type`, `pct_used`, `user_plan`, `prompt_surface` |
| `upgrade_prompt_clicked` | User clicks either CTA | `trigger_type`, `cta_type` (see_plan / start_trial), `resource_type` |
| `upgrade_prompt_dismissed` | User closes the prompt | `trigger_type`, `time_on_prompt_seconds` |
| `upgrade_started` | User reaches the checkout or trial activation flow | `trigger_type`, `target_plan` |
| `upgrade_completed` | User completes payment or trial activation | `trigger_type`, `target_plan`, `revenue_delta` |

**Human action required:** Implement the upgrade prompt UI component. Deploy it behind a PostHog feature flag so you can control rollout. Verify it renders correctly for free users and does not appear for paid users. Launch to a small group (10-50 active free users) first. Observe prompt impressions in PostHog Live Events for the first 24 hours.

### 3. Route high-value accounts

For free accounts with enterprise signals (large team, heavy API usage, company domain matching a target list), do not show a self-serve prompt. Instead, use the `upgrade-prompt` drill's sales routing step: create an expansion deal in Attio with the usage data and trigger reason attached, and assign it to the account owner for a personal conversation.

### 4. Evaluate against threshold

Run the `threshold-engine` drill to measure at the end of 7 days:

- **Primary metric**: Percentage of free users who saw the prompt and clicked upgrade or started a trial. Target: >=5%.
- **Secondary metric**: Of those who clicked, how many reached the checkout or trial activation flow. Target: >=40% (validates the click is not just curiosity).

**Pass (>=5% prompt-to-intent and >=40% click-to-action):** The prompt generates real upgrade intent at a moment of need. Proceed to Baseline to prove it converts to actual paid upgrades with always-on automation.

**Fail:** Diagnose the funnel:
- Low prompt impressions: The limit detection is not finding candidates. Verify the threshold percentages are realistic (maybe your free tier is too generous and users rarely approach limits). Try lowering the threshold from 70% to 50%.
- Low CTR: Users see the prompt but do not engage. The message is wrong. Test: make the copy more specific to what the user will lose (not gain) when they hit the limit. Or the prompt is showing at the wrong moment — test showing it when the user actually tries to use the limited resource, not on login.
- High dismiss rate with fast dismiss time (<2 seconds): Users are treating it as noise. Reduce prompt frequency, make it smaller, or move it inline with the resource UI instead of a banner.
- Good CTR but low follow-through: The pricing page or trial activation has friction. Check if users are dropping off at the pricing page (too many options), the checkout (too many steps), or the trial activation (too much commitment).

## Time Estimate

- 1.5 hours: Usage threshold detection setup — instrument PostHog events, define plan caps, build the detection query, create urgency cohorts
- 2 hours: Upgrade prompt design and implementation (human), PostHog event instrumentation, Intercom message configuration
- 1 hour: Sales routing for enterprise signals, feature flag setup, small group rollout
- 1.5 hours: 7-day monitoring, threshold evaluation, funnel diagnosis, documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, cohorts, feature flags, funnel analysis | Free up to 1M events/mo — https://posthog.com/pricing |
| Intercom | In-app upgrade prompts | Included in existing plan — https://www.intercom.com/pricing |
| n8n | Daily usage threshold detection workflow | Free self-hosted; Cloud from $24/mo — https://n8n.io/pricing |
| Attio | Enterprise lead routing, deal creation | Free tier — https://attio.com/pricing |

**Play-specific cost:** Free (uses existing stack)

## Drills Referenced

- `usage-threshold-detection` — detect free accounts approaching plan limits, classify urgency tiers, create PostHog cohorts
- `upgrade-prompt` — configure the contextual in-app upgrade message tied to the limit trigger, including suppression rules and sales routing
- `threshold-engine` — evaluate the 7-day prompt-to-intent conversion against the 5% threshold
