---
name: upgrade-prompts-scalable
description: >
  In-App Upgrade CTAs — Scalable Automation. Multi-segment prompt personalization
  with A/B testing across prompt copy, placement, and timing to find the 10x multiplier.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "40 hours over 6 weeks"
outcome: "≥12% CTR at 500+ monthly impressions, ≥8% prompt-to-upgrade conversion"
kpis: ["Prompt CTR by segment", "Prompt-to-upgrade conversion rate", "Monthly revenue attributed to prompts", "A/B test velocity", "Prompt fatigue rate"]
slug: "upgrade-prompts"
install: "npx gtm-skills add product/upsell/upgrade-prompts"
drills:
  - ab-test-orchestrator
  - upgrade-prompt-health-monitor
---

# In-App Upgrade CTAs — Scalable Automation

> **Stage:** Product → Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Upgrade prompts run across all trigger types and multiple user segments with no manual intervention. Systematic A/B testing finds the best prompt copy, placement, and timing per segment. A health monitor detects degradation and prompt fatigue automatically. Monthly prompt-attributed revenue is tracked and growing. The system handles 500+ monthly prompt impressions while maintaining ≥12% CTR and ≥8% conversion.

## Leading Indicators

- A/B tests reaching statistical significance within planned timelines (confirms sufficient volume)
- Winning variants producing ≥15% lift over control (confirms optimization is finding real improvements)
- Prompt fatigue cohort staying below 10% of active free/lower-plan users (confirms suppression rules work)
- Revenue attribution increasing month-over-month (confirms upgrades, not just clicks)

## Instructions

### 1. Segment the prompt audience

Using PostHog cohorts, create segments that get different prompt experiences:

| Segment | Definition | Prompt Strategy |
|---------|-----------|-----------------|
| Power free users | Free plan, 20+ core actions/week, 30+ days active | Emphasize advanced features and team capabilities |
| Limit-approaching | Any plan, 70-90% of any limit | Show specific usage numbers and what upgrading unlocks |
| Feature explorers | Attempted 3+ gated features in 14 days | Bundle the features they tried into the upgrade pitch |
| Growing teams | Added 2+ members in 30 days on a plan with seat limits | Lead with team management, permissions, and collaboration features |
| Trial expiring | Trial ending in 3 days or less | Urgency-based: "Your trial ends in [N] days. Keep access to [features they used most]" |

Each segment gets tailored prompt copy and, potentially, a different prompt surface (modal vs banner vs tooltip). The `upgrade-prompt` drill's trigger detection (already running from Baseline) feeds users into these segments via PostHog cohorts.

### 2. Launch systematic A/B testing

Run the `ab-test-orchestrator` drill. Test one variable at a time across these dimensions:

**Round 1 — Prompt copy (weeks 1-2):**
- Control: Current prompt copy from Baseline
- Variant A: Social proof — "Teams like yours upgraded and saw [specific outcome]"
- Variant B: Loss aversion — "You'll lose access to [feature] when you hit the limit"

Use PostHog feature flags to split traffic 33/33/33. Primary metric: `upgrade_prompt_clicked` / `upgrade_prompt_shown`. Minimum 200 impressions per variant before evaluating.

**Round 2 — Prompt timing (weeks 3-4):**
- Control: Prompt appears immediately on trigger
- Variant: Prompt appears on next session after trigger (delayed trigger)

Test whether immediate context or a "cool off" period converts better. Some triggers (feature gate) likely work best immediately; others (growth signal) may work better with a delay.

**Round 3 — Prompt surface (weeks 5-6):**
- Control: In-app modal (current)
- Variant A: Inline banner within the feature area
- Variant B: Tooltip anchored to the gated/limited element

Test per segment — power users may prefer subtle tooltips while new users respond to modals.

After each round, implement the winner permanently and move to the next variable. Log all test results in Attio as notes on the upgrade-prompts campaign record.

### 3. Deploy the health monitor

Run the `upgrade-prompt-health-monitor` drill (all 6 steps). This creates:

- Per-trigger-type funnel dashboards in PostHog
- Daily degradation detection via n8n that alerts when any trigger's CTR drops 20%+ from its 4-week average
- Prompt fatigue cohort that auto-suppresses users who dismissed 3+ prompts in 14 days
- Revenue attribution tracking: `upgrade_completed.revenue_delta_monthly` tagged by trigger type and prompt variant

Review the health dashboard weekly. The degradation alerts run daily and require no manual checking.

### 4. Scale to additional surfaces

Extend prompts beyond in-app messages to capture users who are not in the product when the trigger fires:

- **Email** (already running from Baseline): Continue the Loops follow-up sequences. A/B test email subject lines and send timing using the `ab-test-orchestrator` drill.
- **In-app checkout shortcut**: For limit-proximity triggers, add a one-click upgrade button directly in the usage indicator (e.g., next to "45/50 projects used" show an "Upgrade" link). This removes the friction of a modal.
- **Intercom Product Tour**: For feature-gate triggers, build a 2-step Intercom Product Tour: step 1 shows what the feature does with a screenshot/GIF, step 2 shows the price and a CTA. This educates before asking for the upgrade.

Each new surface gets its own `prompt_surface` property value in PostHog events so the health monitor tracks them separately.

### 5. Evaluate at 6 weeks

Query the `upgrade-prompt-health-monitor` dashboard:

- Overall CTR across all triggers and segments (target ≥12%)
- Prompt-to-upgrade conversion rate (target ≥8%)
- Monthly prompt-attributed revenue (should be a meaningful and growing number)
- A/B test results: how many tests run, what was the cumulative lift from winning variants
- Fatigue rate: what percentage of eligible users are in the prompt-fatigued cohort

**Pass:** CTR ≥ 12% at 500+ monthly impressions AND conversion ≥ 8%. Proceed to Durable.
**Fail:** If CTR is high but conversion is low, the bottleneck is the upgrade page or pricing — not the prompts. If CTR is low, the best A/B test result tells you the ceiling — if even the best variant is below 12%, reconsider trigger quality and audience segmentation.

## Time Estimate

- 6 hours: Build 5 audience segments in PostHog cohorts and configure segment-specific prompt copy
- 12 hours: Run 3 rounds of A/B tests (4 hours per round: setup, monitoring, evaluation)
- 8 hours: Deploy upgrade-prompt-health-monitor drill (dashboard, cohorts, degradation detection, revenue attribution)
- 6 hours: Build additional prompt surfaces (checkout shortcut, Intercom Product Tour)
- 4 hours: Weekly reviews (30 min/week for 6 weeks) and Attio logging
- 4 hours: Final evaluation and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, funnels, cohorts, dashboards | Free tier: 1M events/mo + 1M feature flag requests/mo; paid ~$0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app messages, Product Tours, chat | Advanced $85/seat/mo; Proactive Support add-on $99/mo for 500 outbound messages ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Email follow-up sequences | From $49/mo with unlimited sends ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Automation for health monitor and degradation detection | Self-hosted free; Cloud from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Campaign record, test result logging | From $29/seat/mo ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated play-specific monthly cost at Scalable:** $150-350/mo (Intercom Advanced + outbound add-on is the main cost driver; PostHog and Loops likely stay in free tier at this volume).

## Drills Referenced

- `ab-test-orchestrator` — designs, runs, and evaluates A/B tests on prompt copy, timing, and surface
- `upgrade-prompt-health-monitor` — per-trigger funnel dashboards, degradation alerts, fatigue cohorts, and revenue attribution
