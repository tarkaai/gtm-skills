---
name: keyboard-shortcuts-promotion-baseline
description: >
  Power User Features — Baseline Run. Roll out shortcut hints to 50% of eligible users
  via feature flag, add command palette tour, instrument full adoption funnel, and run
  always-on monitoring to achieve >=30% shortcut trial rate with >=10pp lift in shortcut
  ratio vs control.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=30% shortcut trial rate AND >=10pp shortcut ratio lift vs control group"
kpis: ["Shortcut trial rate", "Shortcut ratio (treatment vs control)", "Hint-to-habitual conversion rate", "Time saved per user per week"]
slug: "keyboard-shortcuts-promotion"
install: "npx gtm-skills add product/retain/keyboard-shortcuts-promotion"
drills:
  - shortcut-discovery-promotion
  - shortcut-adoption-monitor
  - posthog-gtm-events
---

# Power User Features — Baseline Run

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Shortcut hints running always-on for 50% of eligible users. Treatment group achieves >=30% shortcut trial rate and >=10 percentage point higher shortcut ratio than the control group over 2 weeks. This proves the system works at medium scale with automated delivery.

## Leading Indicators

- Shortcut hint impressions scaling proportionally with treatment group size
- Hint-to-trial conversion rate holding at or above Smoke levels
- Users progressing from single-shortcut trial to multi-shortcut adoption
- Shortcut ratio trending upward week-over-week in treatment group
- No increase in churn or support tickets in treatment group vs control

## Instructions

### 1. Expand shortcut coverage to top 6-8 shortcuts

Run the full shortcut mapping from the `shortcut-discovery-promotion` drill. Expand beyond the Smoke test's 3 shortcuts to include 6-8 shortcuts covering the most frequent mouse actions. Add tracking events for each new shortcut.

Instrument all new shortcut events using the `posthog-gtm-events` drill. Verify each event fires correctly in PostHog before proceeding.

### 2. Build the command palette product tour

Run step 5 of the `shortcut-discovery-promotion` drill to create the Intercom product tour for command palette discovery. This 3-step interactive tour triggers once for users who have never opened the command palette and have been active for 5+ sessions.

**Human action required:** Review the tour flow in Intercom preview. Walk through it as a test user. Ensure the interactive step (pressing Cmd+K) registers correctly and advances the tour.

### 3. Set up the 50/50 feature flag experiment

Using PostHog feature flags, create a new flag `shortcut-hints-v2` that targets all eligible users (14+ days tenure, 3+ sessions/week, no prior shortcut usage). Set allocation to 50% treatment / 50% control. Ensure the flag is user-level sticky (same user always gets the same variant).

Define eligibility criteria in PostHog:
- Person property `days_since_signup` >= 14
- Event `$pageview` count >= 3 in last 7 days
- Person property `shortcut_ratio` is null or equals 0

### 4. Deploy always-on hint delivery

Run step 6 of the `shortcut-discovery-promotion` drill to build the progressive education pipeline in n8n. The daily workflow:

1. Queries PostHog for users in the treatment group
2. Assigns each user to a shortcut-readiness cohort (beginner, intermediate, power, dormant)
3. Updates Intercom user properties with their current cohort and next-best-shortcut
4. Intercom tooltips fire based on cohort assignment and frequency caps

This is the first always-on automation — it runs daily without human intervention.

### 5. Deploy the shortcut adoption monitor

Run the full `shortcut-adoption-monitor` drill to build:

- The adoption funnel (hint shown -> trial -> repeat -> habitual)
- Per-user shortcut ratio tracking as a PostHog person property
- Stalled-user detection running daily in n8n
- Automated interventions for each stall type (hint-ignored, one-and-done, regressing, plateaued)
- The 8-panel adoption dashboard
- Weekly adoption report posted to Slack

### 6. Monitor treatment vs control for 2 weeks

After 2 weeks of the experiment running, evaluate:

**Primary metric — shortcut trial rate in treatment group:**
```
trial_rate = count(distinct treatment users with >= 1 shortcut_hint_converted)
             / count(distinct treatment users with >= 1 shortcut_hint_shown)
```
Target: >= 30%

**Primary metric — shortcut ratio lift:**
```
lift = avg(shortcut_ratio for treatment users) - avg(shortcut_ratio for control users)
```
Target: >= 10 percentage points

**Secondary metrics:**
- Hint-to-habitual conversion (users who reach 10+ uses of any shortcut in 14 days): target >= 8%
- Average time saved per treatment user per week (from efficiency gain calculations)
- Treatment group retention rate vs control (must not be lower)
- Support ticket rate in treatment vs control (must not be higher)

### 7. Evaluate against threshold

**Pass threshold: >= 30% trial rate AND >= 10pp shortcut ratio lift vs control.**

If PASS: Roll out treatment to 100% of eligible users. Disable the control group. Document the winning shortcut set, hint timing, and cohort progression rates. Proceed to Scalable.

If FAIL on trial rate but PASS on ratio lift: The hints are not converting first tries, but the users who do try are sticking. Focus on improving hint copy, timing, or trigger conditions. Re-run for another 2 weeks.

If FAIL on ratio lift but PASS on trial rate: Users try shortcuts when prompted but revert to mouse. Focus on habit formation — the stalled-user interventions may need tuning, or the shortcuts themselves may not feel faster. Re-run.

If FAIL on both: Revisit the shortcut selection. The shortcuts being promoted may not be valuable enough. Test different shortcuts or a different delivery mechanism (email with video demo instead of in-app tooltips).

## Time Estimate

- 4 hours: expand shortcut map, instrument new events, build command palette tour
- 4 hours: configure feature flag experiment, deploy n8n progressive education pipeline
- 4 hours: deploy shortcut adoption monitor, build dashboard, configure stalled-user interventions
- 4 hours: 2-week monitoring, analysis, threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, feature flags, experiments, cohorts, dashboards | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Tooltips, product tours, in-app messages | Essential: $29/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Email sequences for hint-ignored users | Free: 1,000 contacts; Paid from $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Daily cohort evaluation, stalled-user detection, report generation | Self-hosted: free; Cloud from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |

**Estimated play-specific cost at this level:** $0-50/mo (Loops free tier likely sufficient; Intercom and PostHog within existing plans)

## Drills Referenced

- `shortcut-discovery-promotion` — expanded shortcut map, command palette tour, progressive education pipeline
- `shortcut-adoption-monitor` — adoption funnel, shortcut ratio tracking, stalled-user detection, dashboard, weekly report
- `posthog-gtm-events` — event instrumentation for all new shortcut tracking events
