---
name: role-based-onboarding-scalable
description: >
  Persona-Based Onboarding — Scalable Automation. Expand to 5+ personas with automated
  classification, multi-channel delivery (tours + emails + in-app messages), per-persona A/B
  testing, and systematic activation optimization across 500+ new users per month.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Scalable Automation"
time: "50 hours over 2 months"
outcome: "≥50% activation rate sustained across 500+ new users/month with 5+ active persona paths"
kpis: ["Overall activation rate", "Activation rate per persona", "Persona classification accuracy", "Tour completion rate", "Email CTR per persona", "Time to activation"]
slug: "role-based-onboarding"
install: "npx gtm-skills add product/onboard/role-based-onboarding"
drills:
  - onboarding-persona-scaling
  - ab-test-orchestrator
  - activation-optimization
---

# Persona-Based Onboarding — Scalable Automation

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Activation rate holds ≥50% across 500+ new users per month with 5+ active persona paths. Persona classification is fully automated (≥95% of signups classified without manual tagging). Each persona's onboarding spans tours, emails, and in-app messages. At least one completed A/B test per persona has improved the weakest paths.

## Leading Indicators

- Automated persona classification assigns ≥95% of new signups without manual intervention
- All persona activation rates are within 15 percentage points of each other (no one persona dragging down the average)
- Per-persona A/B tests produce statistically significant results within 3-week windows (sufficient traffic per persona)
- Email sequence fatigue metrics (declining open rates over time) remain stable or improving
- New persona paths achieve ≥40% activation within their first 4 weeks of operation

## Instructions

### 1. Expand persona coverage

Run the `onboarding-persona-scaling` drill, Steps 1-2. Analyze PostHog data to discover 2-3 additional persona segments beyond the 2-3 proven at Baseline. Focus on users who currently fall into the "default/general" classification bucket — these are users getting the generic experience despite having distinct needs.

Build the automated persona classification workflow in n8n. On every `signup_completed` event, the workflow:
1. Collects all available signals: role field, email domain, company size, signup source UTM, referral path
2. Applies classification rules to assign `persona_type`
3. Writes `persona_type` and `persona_confidence` to both PostHog and Intercom
4. Falls back to "general" only when no signals are available

Target: ≤5% of signups classified as "general" (down from whatever the current fallback rate is).

### 2. Build multi-channel onboarding per persona

Run the `onboarding-persona-scaling` drill, Steps 3-5. For each persona (including new ones), build three coordinated channels:

**In-app product tours** (Intercom): The 3-5 step tour from Baseline, refined based on completion data. Each new persona gets its own tour focused on its specific activation action.

**Email sequences** (Loops): Persona-specific 5-7 email sequences with behavioral triggers (designed at Baseline, now expanded to new personas). Each email references the persona's role and use case in subject line and body.

**Contextual in-app messages** (Intercom): Nudge messages for each persona's known stall points. These fire when a user has not reached the expected milestone within the expected time window. Each message fires once and does not overlap with active tour steps.

Wire all three channels together: if the user activates via any channel, exit the non-activated branch in all channels. PostHog feature flags control which tour, which sequence, and which nudges each persona sees.

### 3. Run per-persona A/B tests

Run the `ab-test-orchestrator` drill. For each persona (starting with the worst-performing), design and run one A/B test:

Identify the biggest drop-off point in that persona's activation funnel. Form a hypothesis about why users drop off there and what change would fix it. Common test variables:

- Tour structure: fewer steps vs more steps
- Tour content: interactive steps vs informational steps
- Email timing: faster cadence (24h) vs standard cadence (48h)
- Email tone: educational vs motivational
- First action: simpler initial milestone vs the current one
- Channel priority: tour-first vs email-first (which drives activation better for this persona?)

Use PostHog experiments with 50/50 split. Require 100+ users per variant before evaluating. Run one test per persona at a time.

### 4. Optimize the weakest personas

Run the `activation-optimization` drill. For any persona with activation rate below 40%:

1. Build a detailed drop-off analysis in PostHog: which step in the activation funnel loses the most users?
2. Check tour dismissal: if users dismiss the tour early, the first steps are not compelling enough
3. Check email engagement: if email open rates are below 25% for a persona, the subject lines are not relevant to that role
4. Check classification accuracy: manually review 20 users classified as this persona — are they actually this persona? Misclassification causes poor activation
5. Implement fixes targeting the single biggest drop-off point
6. Measure improvement over 2 weeks before moving to the next problem

### 5. Build comparative dashboards

Create a PostHog dashboard "Onboarding Scalable Performance" with:

- **Activation rate by persona (weekly trend)**: Line chart, one line per persona, 8-week window
- **Persona classification distribution**: Pie chart showing % of signups per persona. Watch for unexpected shifts.
- **Per-persona funnel**: Side-by-side funnel comparison: `enrolled → tour_completed → email_clicked → activated`
- **A/B test results tracker**: Table of active and completed experiments per persona with current results
- **Email engagement by persona**: Open rate and CTR per persona, weekly trend

### 6. Evaluate against threshold

After 2 months, measure:

- Overall activation rate across all personas: must be ≥50%
- Total users onboarded: must be ≥500/month (proving scale, not just a small cohort)
- Number of active persona paths: must be ≥5
- Automated classification rate: ≥95% of signups classified without manual tagging

If PASS: Document the full persona matrix (personas, classification rules, tours, sequences, nudges) and proceed to Durable.

If FAIL on activation rate: Focus on the persona dragging the average down. Run `activation-optimization` on that persona specifically.

If FAIL on scale: Not enough signups to sustain 5+ personas. Consolidate to 3-4 personas and merge the smallest segments into the nearest neighbor.

## Time Estimate

- 8 hours: Persona discovery, classification workflow build, and testing
- 12 hours: Building tours, email sequences, and in-app messages for 2-3 new personas
- 10 hours: Per-persona A/B test design, implementation, and evaluation
- 8 hours: Activation optimization for underperforming personas
- 6 hours: Dashboard creation, monitoring, and threshold evaluation
- 6 hours: Iteration cycles (fixing issues found during monitoring)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, funnels, cohorts | Free tier: 1M events/mo; paid ~$0.00005/event beyond ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Product tours + in-app messages per persona | Essential: $29/seat/mo; Proactive Support Plus: $99/mo for messages ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Persona-specific email sequences at scale | $49/mo for up to 5,000 contacts; scales with contact count ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Persona classification + event routing workflows | Standard stack |

**Estimated play-specific cost at this level:** $49-148/mo (Loops $49/mo for 5K contacts + Intercom Proactive Support Plus $99/mo if using in-app messages beyond basic plan)

## Drills Referenced

- `onboarding-persona-scaling` — expand to 5+ personas with automated classification, multi-channel delivery, and per-segment email sequences
- `ab-test-orchestrator` — design, run, and evaluate per-persona A/B tests with statistical rigor
- `activation-optimization` — systematically identify and fix the biggest drop-off points per persona
