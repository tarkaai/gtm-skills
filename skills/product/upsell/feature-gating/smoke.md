---
name: feature-gating-smoke
description: >
  Premium Feature Gating — Smoke Test. Gate one premium feature behind a locked state with
  a value preview, offer a time-limited trial, and measure whether gate encounters drive
  upgrade intent.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥15% of gate-exposed users start a trial or click upgrade within 7 days"
kpis: ["Gate impression rate", "Preview engagement rate", "Trial start rate", "Upgrade click rate"]
slug: "feature-gating"
install: "npx gtm-skills add product/upsell/feature-gating"
drills:
  - feature-readiness-gating
  - upgrade-prompt
  - threshold-engine
---

# Premium Feature Gating — Smoke Test

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

15% or more of users who encounter a premium feature gate either start a trial of the gated feature or click the upgrade CTA within 7 days. This proves that the gate presentation communicates enough value to create upgrade intent, not just awareness. "Gate-exposed users" means users who triggered a `gate_impression` event by encountering the locked feature state.

## Leading Indicators

- Gate impressions per day (users are discovering the gated feature organically through normal product usage)
- Preview engagement rate: percentage of gate-exposed users who interact with the value preview (watch the demo, expand the feature description, or hover for more than 3 seconds)
- Time from gate impression to trial start (shorter means the value proposition is compelling)
- Trial engagement: users who start a trial and use the premium feature within 24 hours

## Instructions

### 1. Select and configure the gated feature

Run the `feature-readiness-gating` drill to identify which premium feature to gate. Pick one feature that:

- Exists on a paid tier that free or lower-tier users do not have access to
- Is encountered organically during normal product usage (users do not need to go looking for it)
- Has clear, demonstrable value that can be previewed without full access
- Already has PostHog events tracking its usage, or instrument them now

Define the gate interaction events in PostHog:

| Event | When Fired | Properties |
|-------|-----------|-----------|
| `gate_impression` | User encounters the locked feature state | `feature`, `user_plan`, `page` |
| `gate_preview_engaged` | User interacts with the value preview | `feature`, `preview_type` (demo/screenshot/description), `engagement_seconds` |
| `gate_trial_started` | User clicks "Start free trial" on the gate | `feature`, `trial_duration_days` |
| `gate_upgrade_clicked` | User clicks "Upgrade" on the gate | `feature`, `user_plan`, `target_plan` |
| `gate_dismissed` | User closes or navigates away from the gate | `feature`, `time_on_gate_seconds` |

### 2. Design the gate UX

The gate replaces the gated feature's normal UI with a locked state. The locked state must communicate three things:

1. **What the feature does** — a 1-sentence description of the capability and its benefit
2. **What it looks like in action** — a static screenshot, short GIF, or blurred preview of real data showing the feature working. If the product generates output (reports, charts, recommendations), show a sample output with a "Powered by Pro" watermark.
3. **How to get access** — two CTAs: "Start 7-day free trial" (primary) and "See pricing" (secondary)

The gate must feel helpful, not punishing. Frame it as "here is what you are missing" not "you cannot do this." Show the locked feature in the same location where it would normally appear so the user understands the context.

**Human action required:** Design and implement the gate UI component. Deploy it to the selected feature. Verify it renders correctly for users on the free/lower plan and does not appear for users who already have the premium tier.

### 3. Configure the trial mechanism

Using the `feature-readiness-gating` drill's feature flag infrastructure, set up a trial flow:

- When a user clicks "Start free trial," update their PostHog person property: `trial_feature: "{feature-name}"`, `trial_start: "{ISO timestamp}"`, `trial_end: "{ISO timestamp + 7 days}"`
- Enable the PostHog feature flag for this user so the premium feature becomes accessible
- Fire `gate_trial_started` event
- Show an in-app confirmation: "Your 7-day trial of [feature] is active. Try [specific high-value action] first."

At trial expiration (checked via n8n daily cron or application middleware):
- Disable the feature flag for the user
- Show a re-gate with a modified message: "Your trial of [feature] has ended. You [accomplished X] during your trial. Upgrade to keep access."
- Fire `gate_trial_expired` event with properties: `feature_used_count` (how many times they used it during trial), `last_feature_use` (timestamp)

### 4. Set up upgrade prompt for high-engagement trial users

Run the `upgrade-prompt` drill configured for one trigger: trial users who used the premium feature 3+ times during their trial. For these users, on day 5 of the trial (before expiration), show an in-app message:

"You have used [feature] [N] times this week. Your trial ends in 2 days. Upgrade to Pro to keep [specific outcome they achieved]."

Include a one-click upgrade link that preserves context (the user stays on the page they were on, the upgrade modal opens inline).

### 5. Evaluate against threshold

Run the `threshold-engine` drill to measure at the end of 7 days:

- **Primary metric:** Percentage of gate-exposed users who started a trial or clicked upgrade. Target: >=15%.
- **Secondary metric:** Of trial starters, how many used the premium feature at least once. Target: >=60% (validates that the trial is not just curiosity clicks).

**Pass (>=15% and >=60% trial engagement):** The gate creates real upgrade intent. Proceed to Baseline to prove it converts to actual upgrades with always-on automation.

**Fail:** Diagnose the funnel:
- Low gate impressions: Users are not discovering the gated feature. Move the feature to a more visible location or add a "Preview [feature]" entry point.
- Low preview engagement: The value preview is not compelling. Improve the screenshot/demo or rewrite the benefit copy.
- Low trial starts: Users see the value but the trial barrier is too high. Test removing the trial requirement and going straight to an upgrade CTA, or make the trial one-click with no form.
- Low trial engagement: Users start trials but do not use the feature. The feature's first-run experience has friction. Simplify it or add a guided first action.

## Time Estimate

- 1 hour: Feature selection, gate event definition, PostHog instrumentation
- 2 hours: Gate UX design and implementation (human), trial mechanism setup
- 1 hour: Upgrade prompt configuration, n8n trial expiration workflow
- 1 hour: 7-day monitoring, threshold evaluation, and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, event tracking, funnel analysis | Free up to 1M events/mo — https://posthog.com/pricing |
| Intercom | In-app messages for trial confirmation and upgrade prompts | Included in existing plan — https://www.intercom.com/pricing |

**Play-specific cost:** Free (uses existing stack)

## Drills Referenced

- `feature-readiness-gating` — define which feature to gate, design the gate tiers, and implement PostHog feature flags
- `upgrade-prompt` — configure contextual upgrade prompts for high-engagement trial users
- `threshold-engine` — evaluate 7-day gate-to-intent conversion against the 15% threshold
