---
name: sample-data-templates-scalable
description: >
  Sample Data Acceleration — Scalable Automation. Expand to persona-segmented sample data,
  systematically A/B test sample content and template variants, and build automated
  template health scoring that retires underperformers and promotes winners.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "50 hours over 2 months"
outcome: "≥80% interaction rate at 500+ users AND ≥15pp activation lift across all personas"
kpis: ["Per-persona interaction rate", "Template install-to-edit rate", "Activation lift by persona", "Time to graduation (sample → real data)"]
slug: "sample-data-templates"
install: "npx gtm-skills add product/onboard/sample-data-templates"
drills:
  - ab-test-orchestrator
  - activation-optimization
  - upgrade-prompt
---

# Sample Data Acceleration — Scalable Automation

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Success at Scalable means: the sample data system runs at full scale (500+ new users/month) with persona-segmented content, systematic experimentation improves activation lift beyond Baseline, and automated template health scoring keeps the gallery fresh without manual curation.

## Leading Indicators

- Per-persona interaction rates are within 10% of each other (no persona left behind)
- A/B tests on sample data variants produce measurable winners within 2-week cycles
- Template gallery grows from 8-12 to 20+ templates via automated contribution pipeline
- "Graduation rate" (sample data cleared → real data created within 7 days) exceeds 50%
- New user activation rate sustains ≥25pp above the pre-sample-data baseline

## Instructions

### 1. Expand to persona-segmented sample data

The Smoke/Baseline levels used a single sample data package. At Scalable, create differentiated experiences:

1. Define 3-5 user personas based on your ICP segmentation (from PostHog cohort data and Attio deal analysis). Examples: "Solo founder," "Marketing team lead," "Engineering manager," "Agency operator."
2. For each persona, generate a dedicated seed file with domain-appropriate sample data: different project types, industry-specific terminology, workflow patterns matching that persona's use case.
3. Add a persona detection step to the signup flow. Options:
   - **Explicit**: Ask during onboarding: "What best describes your role?" Map answers to personas.
   - **Implicit**: Use enrichment data (company size, industry from Clearbit/Clay) to auto-classify.
   - **Hybrid**: Auto-classify with enrichment, confirm with an onboarding question.
4. Wire PostHog feature flags to serve the correct seed file based on detected persona. Track `persona_detected` and `persona_sample_data_injected` events.

### 2. Launch systematic experimentation on sample data

Run the `ab-test-orchestrator` drill to test sample data variants. Experiment targets:

**Experiment 1 — Content density:**
- Variant A: 3 sample objects (minimal, fast to scan)
- Variant B: 8 sample objects (comprehensive, shows more features)
- Metric: interaction rate and activation rate
- Hypothesis: "Fewer sample objects with higher quality will produce higher activation because users are less overwhelmed."

**Experiment 2 — Hero record prominence:**
- Variant A: Hero record appears first in the list with a "Start here" badge
- Variant B: Hero record is mixed into the list with no special treatment
- Metric: time to first meaningful interaction
- Hypothesis: "Directing attention to the hero record reduces time-to-first-action by 30%."

**Experiment 3 — Template suggestion timing:**
- Variant A: Template gallery shown during onboarding (before seeing sample data)
- Variant B: Template gallery shown after 2 days (once user has explored sample data)
- Metric: template install rate and template-to-activation rate
- Hypothesis: "Showing templates after users explore sample data produces higher install-to-edit rates because users understand what they are choosing."

**Experiment 4 — Graduation prompt:**
- Variant A: Passive "Clear sample data" button in settings
- Variant B: Active prompt after user's 3rd session: "Ready to start with your own data? We can keep your sample data or clear it."
- Metric: graduation rate (cleared + created real data)
- Hypothesis: "Active graduation prompts increase real-data creation by 20pp."

Run each experiment for 2 weeks or until statistical significance. Log results in PostHog and Attio.

### 3. Optimize the activation funnel around sample data

Run the `activation-optimization` drill with a focus on the sample-data-specific funnel:

1. Pull the `sample_data_injected → activation_reached` funnel from PostHog, broken down by persona
2. Identify the biggest per-persona drop-off point
3. For each persona's worst step, design a targeted intervention:
   - If users view sample data but do not edit: add an in-app nudge ("Try editing this — change the [field] to see what happens")
   - If users edit sample data but do not create real objects: add a "Create your own based on this" button on each sample record
   - If users install templates but do not customize: add a guided customization wizard that walks through 3-5 key fields
4. Deploy interventions behind PostHog feature flags and measure impact

### 4. Build automated template health scoring

Create an n8n workflow that runs weekly and scores every template:

```
Template Health Score = (install_rate × 0.3) + (install_to_edit_rate × 0.4) + (edit_to_activation_rate × 0.3)
```

Actions by score:
- **Score ≥ 0.7**: Promote (feature in "Popular" section, recommend in onboarding)
- **Score 0.4-0.7**: Monitor (keep live, review monthly)
- **Score < 0.4**: Retire or redesign (archive from gallery, investigate why it underperforms)

The workflow should:
1. Query PostHog for template metrics over the last 30 days
2. Calculate health scores
3. Auto-promote templates scoring ≥0.7 (update `featured: true` flag)
4. Auto-archive templates scoring <0.4 for 2 consecutive months
5. Post a weekly template health report to Slack

### 5. Set up expansion prompts for engaged users

Run the `upgrade-prompt` drill to identify users who are extracting high value from sample data and templates but are on the free plan:

- Users who installed 3+ templates → prompt: "You're using [Product] like a pro. Unlock [premium feature] to take it further."
- Users who created 5+ real objects after graduating from sample data → prompt: "Your team is growing. Invite teammates and unlock collaboration features."
- Users who completed sample data orientation AND activated within 48 hours → flag as "power onboarders" in Attio for the sales team

### 6. Evaluate against threshold

After 2 months (or 500+ users through the system):

- **Per-persona interaction rate**: Each persona should hit ≥80%. If any persona falls below 70%, that persona's sample data needs redesign.
- **Activation lift**: ≥15pp across all personas combined (up from Baseline's 10pp). Break down by persona — no persona should show <8pp lift.
- **Template install-to-edit rate**: ≥40% (proves templates are relevant, not just installed and forgotten).
- **Graduation rate**: ≥40% of seeded users clear sample data and create real data within 14 days.

**Pass threshold: ≥80% interaction rate at 500+ users AND ≥15pp activation lift across all personas.**

If PASS: Document all experiment results, per-persona configurations, and template health scores. Proceed to Durable.
If FAIL: Focus on the worst-performing persona. If one persona drags down the average, redesign that persona's sample data rather than changing the overall strategy.

## Time Estimate

- 12 hours: Build 3-5 persona-specific seed files and implement persona detection
- 15 hours: Design and run 4 A/B experiments (setup + monitoring + analysis)
- 8 hours: Build activation funnel optimizations per persona
- 8 hours: Build automated template health scoring workflow
- 4 hours: Set up upgrade prompts and expansion triggers
- 3 hours: Final evaluation and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, funnels, cohorts, dashboards | Usage-based from $0.00005/event; experiments included ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app nudges, graduation prompts, upgrade messages | Essential: $29/seat/mo; Proactive Support add-on: $349/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Persona-specific onboarding emails, template discovery emails | From $49/mo based on contacts ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Template health scoring automation, weekly reports | Self-hosted: Free; Cloud from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |

**Estimated monthly cost: ~$100-450/mo** (Intercom Proactive Support is the largest cost if using in-app prompts at scale)

## Drills Referenced

- `ab-test-orchestrator` — design, run, and evaluate A/B tests on sample data variants and template surfaces
- `activation-optimization` — identify and fix per-persona drop-off points in the sample data funnel
- `upgrade-prompt` — contextual expansion prompts for users extracting high value from sample data
