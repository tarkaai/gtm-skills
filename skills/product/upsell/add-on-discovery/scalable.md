---
name: add-on-discovery-scalable
description: >
  Module Cross-Sell — Scalable Automation. Expand discovery surfaces to your full add-on
  catalog, run systematic A/B tests on surface type/copy/timing, and build segment-specific
  cross-sell paths that scale to 500+ users without proportional effort.
stage: "Product > Upsell"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥8% activation rate sustained across 3+ add-ons at 500+ triggered users/month"
kpis: ["Add-on activation rate by module", "Cross-sell revenue", "ARPU lift", "Surface conversion by type", "Catalog penetration"]
slug: "add-on-discovery"
install: "npx gtm-skills add product/upsell/add-on-discovery"
drills:
  - addon-discovery-surface-build
  - ab-test-orchestrator
  - addon-cross-sell-health-monitor
  - upgrade-prompt
---

# Module Cross-Sell — Scalable Automation

> **Stage:** Product → Upsell | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

Discovery surfaces are live for 3+ add-ons, each with validated triggers. A/B testing has identified the best-performing surface type, copy, and timing for each add-on. The system handles 500+ triggered users per month without manual intervention. Cross-sell revenue is a predictable, growing line item.

## Leading Indicators

- 3+ add-ons have active discovery surfaces with triggers validated against PostHog data
- A/B tests running continuously (one test per add-on at a time)
- Weekly cross-sell brief shows improving or stable activation rates
- No add-on has a dismissal rate above 50%
- Cross-sell revenue increases month over month

## Instructions

### 1. Expand the add-on catalog

Run the `addon-discovery-surface-build` drill for each additional add-on you want to cross-sell. For each new add-on:

- Analyze PostHog data to identify the trigger behavior (Step 1 of the drill)
- Instrument the PostHog events using the same event schema but with the new `addon_slug` value
- Build both tooltip and banner surfaces with add-on-specific copy
- Add the add-on to the existing n8n daily trigger detection workflow (extend, do not duplicate the workflow)
- Implement fatigue controls per the drill's Step 6 — critical at scale because users may now qualify for multiple add-on surfaces

Prioritize add-ons by: (1) revenue potential, (2) clarity of trigger signal, (3) activation flow quality. Do not launch more than 2 new add-ons per month — each needs a 2-week validation window.

### 2. Run systematic A/B tests

Run the `ab-test-orchestrator` drill to test variations for each add-on's discovery surface. Test one variable at a time per add-on:

**Round 1 — Surface type**: Tooltip vs. banner vs. modal for the same trigger. Measure: impression-to-click rate. Minimum 200 impressions per variant. Typical test duration: 2-3 weeks.

**Round 2 — Copy**: Test 2-3 copy variants for the winning surface type. Variant A: benefit-focused ("Save 4 hours/week with automated reports"). Variant B: social proof ("Teams like yours use Reporting to track 3x more metrics"). Variant C: urgency ("You've built 7 manual views — automate them"). Measure: impression-to-click rate and click-to-activation rate.

**Round 3 — Timing**: Test when the surface appears relative to the trigger. Variant A: immediately after the trigger behavior. Variant B: next session after the trigger. Variant C: 48 hours after the trigger. Measure: click-to-activation rate (not just CTR — later timing may get fewer clicks but higher quality).

Use PostHog feature flags to split traffic. Run each test to statistical significance (95% confidence, 80% power). Document every test result in Attio.

### 3. Build segment-specific cross-sell paths

Not every user should see the same surface for the same add-on. Using the data from A/B tests and the `upgrade-prompt` drill, create segment-specific paths:

- **Power users** (high feature usage, long tenure): Show advanced add-ons with technical messaging. Surface type: tooltips at point-of-use. Example: "You're running 15 automations manually — the API module lets you trigger them programmatically."
- **Growing teams** (recently added seats, increasing collaboration): Show team-oriented add-ons. Surface type: banner on team settings page. Example: "Your team grew to 8 members — Advanced Permissions lets you control who sees what."
- **Limit-approaching users** (approaching plan caps): Combine add-on discovery with upgrade prompts. Surface type: contextual warning + add-on suggestion. Example: "You've used 90% of your storage. The Storage Add-on gives you 10x capacity."

Use PostHog cohorts to define each segment. Assign each segment its best-performing surface variant from A/B test results.

### 4. Scale the monitoring layer

Extend the `addon-cross-sell-health-monitor` drill to cover the full catalog:

- Expand the PostHog dashboard to show per-add-on funnel metrics
- Enable weekly and monthly alert checks (these were skipped at Baseline)
- Add A/B test tracking to the weekly brief: which tests are running, which concluded, what was learned
- Track catalog penetration: what percentage of eligible users have been shown at least one add-on surface, and what percentage have activated at least one add-on

### 5. Evaluate against threshold

After 2 months, measure: ≥8% activation rate sustained across 3+ add-ons with 500+ triggered users per month. Also measure:

- **Catalog penetration**: percentage of active users who have activated at least one add-on
- **Cross-sell revenue**: total monthly MRR attributable to add-on activations
- **ARPU lift**: delta between cross-sold and non-cross-sold users
- **Test velocity**: how many A/B tests completed per month

If PASS, proceed to Durable. If FAIL:
- Activation rate below 8% on all add-ons: the discovery surfaces are getting clicks but the activation flows are failing. Audit each add-on's activation UX.
- Activation rate above 8% on 1-2 add-ons but not the rest: focus on the winners. Retire or redesign the underperformers. You may have add-ons that users do not want — that is a product signal, not a discovery problem.
- Volume below 500 triggered users/month: triggers are too restrictive. Lower thresholds or add additional trigger behaviors. Check if the user base is large enough for this play at scale.

## Time Estimate

- 15 hours: Expand discovery surfaces to 3+ add-ons (5h per add-on setup)
- 15 hours: Run 3 rounds of A/B tests across add-ons (5h per round)
- 10 hours: Build segment-specific cross-sell paths
- 10 hours: Scale monitoring, dashboards, and alerts
- 10 hours: Weekly monitoring, test evaluation, and optimization over 2 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Funnels, cohorts, feature flags, experiments, dashboards | Free up to 1M events/mo; $0.00031/event after — https://posthog.com/pricing |
| Intercom | In-app tooltips, banners, product tours per add-on | Included in existing plan — https://www.intercom.com/pricing |
| Loops | Segment-specific email nudges | Free up to 1,000 contacts; $49/mo for 5,000 — https://loops.so/pricing |
| n8n | Trigger detection, test routing, alerts, weekly briefs | Free self-hosted; Cloud from $24/mo — https://n8n.io/pricing |
| Attio | Expansion deals, test result logging, campaign tracking | Included in existing plan — https://attio.com/pricing |

## Drills Referenced

- `addon-discovery-surface-build` — repeated for each new add-on in the catalog
- `ab-test-orchestrator` — systematic testing of surface type, copy, and timing
- `addon-cross-sell-health-monitor` — full monitoring with per-add-on breakdowns and weekly briefs
- `upgrade-prompt` — integrates limit-approaching triggers with add-on discovery for compound upsell surfaces
