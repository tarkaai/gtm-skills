---
name: feature-gating-scalable
description: >
  Premium Feature Gating — Scalable Automation. Gate 5+ premium features with per-feature
  gate UX, per-segment trial experiences, systematic A/B testing of gate presentations,
  and automated upgrade pipeline across all gated features.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥20% overall trial-to-upgrade conversion sustained across 5+ gated features and 500+ gate-exposed users"
kpis: ["Overall trial-to-upgrade rate", "Per-feature conversion rate", "Gate-driven MRR", "Experiment win rate", "Gate fatigue rate"]
slug: "feature-gating"
install: "npx gtm-skills add product/upsell/feature-gating"
drills:
  - ab-test-orchestrator
  - upgrade-prompt
  - feature-adoption-monitor
---

# Premium Feature Gating — Scalable Automation

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

20% or more overall trial-to-upgrade conversion rate sustained across 5+ gated premium features with 500+ total gate-exposed users. Each gated feature has its own gate UX, value preview, and trial experience. The 10x multiplier comes from two dimensions: more features gated (each gate is an independent upgrade surface) and per-feature optimization (the best gate presentation varies by feature type and user segment).

## Leading Indicators

- New features gated without requiring custom development (the gate component is reusable)
- Per-feature conversion rates clustering above 15% (no single feature dragging the average)
- A/B test velocity: at least 2 experiments completed per month with documented outcomes
- Gate-driven MRR growing month over month (the pipeline is producing revenue)
- Gate fatigue rate below 15% across all features (users are not being overwhelmed by gates)
- Cross-feature trial stacking: users who trial multiple features convert at higher rates than single-feature trial users

## Instructions

### 1. Expand to 5+ gated features

Using the Baseline's gate infrastructure, select 4+ additional premium features to gate. Prioritize features that:

- Have high organic discovery rate (users encounter them during normal usage)
- Demonstrate clear value that can be previewed (output, visualization, or workflow result)
- Span different use cases so users on different workflows encounter different gates
- Do not overlap (a user should not hit 3 gates in the same session)

For each new gated feature, configure:

1. **Gate UX component** with feature-specific value preview:
   - **Data features** (reports, analytics, dashboards): Show a blurred or watermarked version of real output computed from the user's own data. "Here is what your [report] looks like on Pro."
   - **Workflow features** (automation, integrations, bulk actions): Show a before/after comparison. "Without [feature]: 12 manual steps. With [feature]: 1 click."
   - **Collaboration features** (permissions, team views, shared workspaces): Show a mock team view with the user's existing data. "Your team could see [this view] on the Pro plan."

2. **PostHog feature flag** gating the feature (reuse the flag infrastructure from Baseline)

3. **Trial configuration**: duration (7 or 14 days based on feature complexity), activation action (the first thing the user should do during the trial), and engagement threshold (how many uses indicates the trial is working)

4. **Nurture sequence in Loops**: per-feature trial emails using the 4-email template from Baseline, customized with feature-specific actions and value propositions

Deploy new gates one per week. Monitor each for 7 days before launching the next. If a feature's gate-to-trial rate is below 10% after 7 days, revise the value preview before continuing.

### 2. Run systematic experiments on gate presentations

Run the `ab-test-orchestrator` drill to test gate variations:

**Month 1 experiments:**

- **Value preview format**: Static screenshot vs. animated GIF vs. interactive demo for the highest-traffic gated feature. Hypothesis: interactive demos increase preview engagement by 20% because users experience the feature rather than just seeing it. Measure: `gate_preview_engaged` rate and `gate_trial_started` rate.

- **Trial duration**: 7-day trial vs. 14-day trial for a workflow-oriented feature. Hypothesis: 14-day trials increase trial-to-upgrade conversion by 10pp because complex features need more time to demonstrate value. Measure: `gate_upgrade_completed` rate and `gate_trial_feature_used` count.

**Month 2 experiments:**

- **Gate copy framing**: Loss-framed ("You are missing out on [benefit]") vs. gain-framed ("Unlock [benefit] with Pro") across all gated features. Hypothesis: Loss framing increases trial starts by 15% because it creates urgency. Measure: `gate_trial_started` rate.

- **Upgrade timing**: Upgrade prompt on day 3 of trial (after feature used 3+ times) vs. day 5 (closer to expiration). Hypothesis: Earlier prompts capture intent while engagement is highest. Measure: `gate_upgrade_completed` rate and `time_to_upgrade`.

For each experiment:
1. Form the hypothesis with expected impact
2. Calculate required sample size (minimum 200 per variant per gated feature)
3. Set up the PostHog feature flag split
4. Run for the calculated duration without checking results early
5. Evaluate: adopt the winner, document the learning

### 3. Segment the gate experience

Different user segments respond to different gate strategies. Using PostHog cohorts and the `upgrade-prompt` drill, configure segment-specific gate behaviors:

| Segment | Gate Strategy | Rationale |
|---------|--------------|-----------|
| Free users, active 30+ days | Aggressive: show gate + trial offer on first encounter | They know the product, the gate introduces premium value |
| Free users, active <7 days | Gentle: show "teased" gate (feature visible but grayed out, no trial offer yet) | Too early for upgrade pressure, build awareness first |
| Trial expired, did not upgrade | Re-engagement: show gate with "Pick up where you left off" + usage summary from previous trial | They already experienced value, remind them |
| Downgraded users | Winback: show gate with personalized loss message: "You used to have [feature] — you [accomplished X] with it" | Emotional connection to past usage |
| Power users on lower tier | Usage-triggered: show gate only when they hit a plan limit or try an action that requires the premium feature | The gate appears at the moment of highest intent |

Configure n8n to evaluate segment membership on each `gate_impression` event and route to the appropriate gate variant.

### 4. Build cross-feature upgrade intelligence

Track users across multiple gated features to identify upgrade patterns:

- **Multi-gate exposure:** Users who encounter 3+ different feature gates convert at what rate vs. users who encounter only 1?
- **Gate sequence:** Is there an optimal order of feature gate encounters? (e.g., users who see the analytics gate first and the automation gate second convert better than the reverse)
- **Trial stacking:** Users who trial multiple features — does the second trial convert at a higher rate than the first?

Using PostHog funnels, build a cross-feature journey: first `gate_impression` (any feature) -> second `gate_impression` (different feature) -> `gate_trial_started` (any feature) -> `gate_upgrade_completed`. Identify the feature combination that produces the highest upgrade rate.

If cross-feature exposure correlates with higher conversion, configure n8n to strategically expose users to a second gated feature 3-5 days after their first gate encounter — not pushy, but discoverable (e.g., a subtle in-app message: "While you are here, Pro also includes [second feature] — preview it").

### 5. Monitor and optimize per-feature performance

Run the `feature-adoption-monitor` drill expanded to cover all gated features:

| Metric | Action Threshold |
|--------|-----------------|
| Per-feature trial-to-upgrade <10% for 2 weeks | Pause the gate, test a different value preview or trial experience |
| Gate fatigue rate >20% for any feature | Suppress the gate for fatigued users, switch to email-based trial offer |
| Gate dismissal rate >50% on first impression | The gate UX is perceived as a nuisance — reduce prominence or improve the value preview |
| Cross-feature gate encounters >3 per session | Too many gates in one session — implement a session-level gate cap of 2 |
| Overall MRR from gates declining | Check if the user pool is being exhausted — add new gated features or refresh value previews |

### 6. Evaluate against threshold

At the end of 2 months:

- **Overall trial-to-upgrade rate** across all gated features (target: >=20%)
- **Total gate-exposed users** (target: 500+)
- **Number of gated features with >=15% conversion** (target: 5+)
- **Gate-driven MRR** growing month over month

**Pass:** The gating system scales across features without proportional effort. Each new gate deploys via the established component and workflow. Proceed to Durable for autonomous optimization.

**Fail:** Identify which features underperform. If most gates work but 1-2 fail, retire those and replace with better-suited features. If most gates fail, the product's free tier may be too generous (users do not feel the need to upgrade) or the pricing gap is too large (the upgrade feels disproportionate to the gated value).

## Time Estimate

- 15 hours: Gate UX implementation for 4+ additional features, per-feature trial configuration, Loops sequences
- 15 hours: A/B test design, execution, and analysis (4 experiments over 2 months)
- 10 hours: Segment-specific gate strategy configuration, n8n routing workflows
- 10 hours: Cross-feature upgrade intelligence, funnel analysis
- 10 hours: Weekly performance reviews, optimization, documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Cohorts, feature flags, experiments, funnels, dashboards | Free up to 1M events/mo; Growth from $0.00045/event — https://posthog.com/pricing |
| Intercom | Per-segment in-app gate variants and upgrade prompts | ~$75-300/mo depending on MAU — https://www.intercom.com/pricing |
| Loops | Per-feature trial nurture sequences | Starter $49/mo for 5,000 contacts — https://loops.so/pricing |
| n8n | Gate routing, trial provisioning, segment evaluation, monitoring | Free self-hosted; Cloud from $24/mo — https://n8n.io/pricing |
| Attio | Trial records, upgrade deals, revenue attribution | Free tier — https://attio.com/pricing |

**Play-specific cost:** ~$100-400/mo (Intercom and Loops scale with user volume)

## Drills Referenced

- `ab-test-orchestrator` — run systematic experiments on gate UX, trial duration, copy framing, and upgrade timing
- `upgrade-prompt` — configure per-segment upgrade prompts with context-aware triggers
- `feature-adoption-monitor` — monitor per-feature gate performance, detect fatigue, and alert on conversion drops
