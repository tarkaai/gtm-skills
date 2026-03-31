---
name: deal-term-ab-testing
description: A/B test multi-year deal structures — discount levels, term lengths, incentive packages, and presentation formats to find the highest-TCV combination
category: Deal Management
tools:
  - PostHog
  - n8n
  - Attio
  - Anthropic
fundamentals:
  - posthog-experiments
  - posthog-feature-flags
  - posthog-custom-events
  - n8n-workflow-basics
  - attio-deals
  - attio-custom-attributes
  - experiment-evaluation
---

# Deal Term A/B Testing

This drill runs controlled experiments on multi-year deal variables to find the optimal combination of discount level, term length, incentive structure, and presentation format. Each experiment tests ONE variable at a time, uses PostHog feature flags to randomly assign deals to variants, and evaluates results after reaching statistical significance.

## Input

- PostHog with deal negotiation events flowing (from `deal-negotiation-tracking`)
- At least 20 multi-year proposals sent (need sufficient volume for A/B testing)
- n8n instance managing proposal automation
- Attio CRM with deal-level negotiation data

## Steps

### 1. Identify testable variables

Map every variable in the multi-year deal process that affects close rate or TCV:

| Variable | Control | Variant Ideas | Primary Metric |
|----------|---------|--------------|----------------|
| Discount level | 15% annual, 20% 2-year | 10%/15%, 20%/25%, tiered by ACV | Close rate, TCV |
| Term options | 2 and 3-year | 2-year only, 3-year only, 1+2+3 year | Average term length |
| Number of options shown | 3 options | 2 options, 4 options | Decision speed, close rate |
| Presentation order | High-to-low anchor | Low-to-high, middle-first | Final TCV selected |
| Payment terms | Annual upfront | Quarterly, monthly+commitment | Close rate, cash flow |
| Incentives | Rate lock only | Rate lock + support upgrade, rate lock + onboarding | Close rate, perceived value |
| Delivery format | Email comparison table | PDF proposal, interactive pricing page, live walkthrough | Close rate, engagement |
| Timing | Propose at deal stage change | Propose 2 weeks before fiscal year end | Close rate |

Prioritize by expected impact and ease of implementation. Start with discount level and number of options — these have the largest effect on TCV.

### 2. Set up the experiment framework

Using `posthog-feature-flags`, create a feature flag for each experiment:

```
Flag name: multiyear_experiment_{variable}_{date}
Rollout: 50/50 split
Targeting: All deals entering Proposed stage with multiyear_readiness_score >= 50
```

Using `n8n-workflow-basics`, modify the proposal automation workflow to check the feature flag before generating proposals. The flag determines which variant of the variable to apply.

### 3. Run the first experiment

Example: Testing discount level.

**Control:** Standard pricing (15% annual discount, 20% 2-year discount)
**Variant:** Reduced pricing (10% annual discount, 15% 2-year discount)

Hypothesis: Reducing discount by 5 percentage points will decrease close rate by <5% but increase average TCV by >8% (because the deals that still close are at higher prices).

Setup:
1. Create PostHog feature flag `multiyear_experiment_discount_level_2026Q1`
2. In the proposal automation n8n workflow, check the flag for each deal
3. Control deals get standard discount parameters passed to `deal-term-modeling`
4. Variant deals get reduced discount parameters
5. Both groups fire `multiyear_proposal_sent` with an `experiment_variant` property

Duration: Run until 30+ proposals sent per variant, minimum 4 weeks.

### 4. Evaluate results

Using `experiment-evaluation`, analyze:

**Primary metric:** TCV per proposal sent (combines close rate and deal size)
**Secondary metrics:**
- Close rate (did the variant scare away too many buyers?)
- Average negotiation rounds (did tighter discounts increase back-and-forth?)
- Time to close (did it slow down decisions?)
- Revert-to-annual rate (did more buyers bail to annual?)

Decision framework:
- **Adopt:** Variant TCV-per-proposal > Control by >= 10% with statistical significance (p < 0.05)
- **Iterate:** Variant shows directionally positive results but not significant — extend the test or try a middle ground
- **Revert:** Variant TCV-per-proposal is worse or close rate dropped > 20%

### 5. Implement winners and start next experiment

For adopted variants:
1. Update the default parameters in the proposal automation workflow
2. Log the change in Attio: "Experiment {name} adopted. Changed {variable} from {old} to {new}. Expected impact: {X}% TCV improvement."
3. Fire `multiyear_experiment_adopted` PostHog event

Start the next experiment on a different variable. Never run 2 experiments on overlapping variables simultaneously.

### 6. Build the experiment history

Using `posthog-custom-events`, track every experiment:
```json
{
  "event": "multiyear_experiment_completed",
  "properties": {
    "experiment_name": "discount_level_2026Q1",
    "variable_tested": "discount_level",
    "control_description": "15%/20%",
    "variant_description": "10%/15%",
    "control_tcv_per_proposal": 35000,
    "variant_tcv_per_proposal": 38500,
    "improvement_pct": 10,
    "decision": "adopted",
    "proposals_per_variant": 35,
    "duration_days": 28
  }
}
```

Over time, this builds a dataset of what works and what doesn't for your specific market, enabling the `autonomous-optimization` drill to make better hypotheses at the Durable level.

## Output

- Experiment framework with feature flag integration
- First experiment running on the highest-impact variable
- Evaluation protocol with clear adopt/iterate/revert criteria
- Winner implementation workflow
- Experiment history tracking for long-term optimization

## Triggers

Experiments run continuously. Each experiment runs for 4+ weeks or until statistical significance. Maximum 1 active experiment at a time. After an experiment concludes, start the next within 1 week.
