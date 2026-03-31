---
name: experiment-learnings-database
description: Build and maintain a cumulative knowledge base of experiment outcomes, patterns, and transferable insights
category: Experimentation
tools:
  - Attio
  - Anthropic
  - PostHog
fundamentals:
  - attio-notes
  - attio-custom-attributes
  - hypothesis-generation
  - posthog-custom-events
---

# Experiment Learnings Database

This drill maintains a structured knowledge base of every experiment ever run: what was tested, what happened, and what it means. The database prevents repeating failed experiments, surfaces transferable insights across product areas, and improves hypothesis quality over time by grounding new hypotheses in historical evidence. At Durable level, the autonomous optimization agent queries this database before generating new hypotheses.

## Prerequisites

- Attio configured with experiment tracking records
- At least 10 completed experiments (minimum viable knowledge base)
- Anthropic API key for pattern extraction

## Input

- Completed experiment record from Attio: hypothesis, variants, results, decision, product area
- PostHog experiment data: full metric breakdown for control and variant

## Steps

### 1. Structure the experiment record

For each completed experiment, create a standardized record in Attio using `attio-custom-attributes`:

```json
{
  "experiment_id": "exp-2024-042",
  "hypothesis": "Adding social proof badges to the pricing page will increase checkout starts by 3pp",
  "product_area": "pricing",
  "metric_tested": "pricing_page_to_checkout_conversion",
  "baseline_value": "38.2%",
  "variant_value": "39.1%",
  "absolute_lift": "+0.9pp",
  "relative_lift": "+2.4%",
  "confidence": "78%",
  "decision": "not_significant",
  "sample_size": 2840,
  "duration_days": 14,
  "date_completed": "2024-11-15",
  "tags": ["social-proof", "pricing-page", "conversion", "not-significant"],
  "key_learning": "Social proof had no measurable impact on checkout starts. Users who reached the pricing page were already past the trust threshold — social proof addresses a problem they do not have at this stage.",
  "transferable_insight": "Social proof interventions should target earlier funnel stages (landing page, signup) where trust is still being established, not downstream decision points.",
  "related_experiments": ["exp-2024-031", "exp-2024-019"]
}
```

### 2. Extract patterns across experiments

After every 5 new experiment completions, run a pattern extraction using the `hypothesis-generation` fundamental. Pass the last 20 experiment records and ask Claude to identify:

**What works in this product:**
- Which types of changes consistently produce lift? (e.g., reducing friction > adding features > changing copy)
- Which product areas have the highest experiment win rates?
- What effect sizes are typical for this product? (calibrates future hypotheses)

**What does not work:**
- Which types of changes consistently fail? (e.g., "adding more information to decision points has failed 4 out of 5 times")
- Are there product areas where experimentation yields nothing? (may indicate the area is already optimized or the wrong metrics are being measured)

**Cross-area insights:**
- Do learnings from one area predict outcomes in another? (e.g., "reducing choices from 4 to 2 improved conversion in pricing AND onboarding — choice reduction may be a universal lever for this product")

Store the pattern analysis in Attio as a "Learning Pattern" record, tagged with the relevant product areas and experiment types.

### 3. Build the pre-hypothesis check

Before any new hypothesis is generated (in the `experiment-hypothesis-design` drill), query the learnings database:

1. Search Attio for experiments in the same product area
2. Search for experiments testing similar change types (using tags)
3. Check if the proposed hypothesis contradicts a known pattern
4. Check if the proposed hypothesis duplicates a previous experiment

Output a pre-check report:
```
Hypothesis: "Simplify the onboarding wizard from 5 steps to 3"
Related experiments found: 3
- exp-2024-027: Reduced pricing options from 4 to 2 → +4.1pp conversion (adopted)
- exp-2024-033: Reduced onboarding fields from 8 to 4 → +2.8pp completion (adopted)
- exp-2024-038: Removed optional onboarding steps → -1.2pp activation (reverted, users skipped important setup)

Pattern match: "Choice/step reduction generally works for this product (+3.4pp average lift across 2 wins). However, removing steps that contain important setup actions backfired."

Recommendation: Proceed, but ensure the 3 remaining steps cover all critical setup actions. Do not simply remove steps — consolidate them.
```

### 4. Maintain the database

**Monthly cleanup:** Remove experiments older than 18 months that have been superseded by more recent tests in the same area. Archive them but exclude from active pattern analysis (the product has likely changed enough to make old results unreliable).

**Quarterly pattern refresh:** Re-run the full pattern extraction across all active experiments. Update the "What works / What doesn't" summaries. Share with the team as a quarterly experimentation retrospective.

**Tag hygiene:** Ensure consistent tagging. Merge duplicate tags (e.g., "social-proof" and "social_proof"). Add missing tags to older experiments when new tag categories emerge.

### 5. Feed the autonomous optimization loop

At Durable level, the `autonomous-optimization` drill's Phase 2 (Diagnose) queries this database before generating hypotheses. The integration:

1. When an anomaly is detected and hypothesis generation begins, the agent first queries the learnings database for the relevant product area
2. The pattern analysis and related experiment history are included in the hypothesis generation prompt
3. This prevents the agent from re-testing failed hypotheses and biases it toward change types with historical evidence of working in this product

Log each query and its influence on hypothesis selection as an `experiment_knowledge_query` event in PostHog using `posthog-custom-events`.

## Output

- Structured experiment records for every completed test
- Pattern analysis updated every 5 experiments
- Pre-hypothesis check that grounds new ideas in historical evidence
- Quarterly experimentation retrospective
- Knowledge feed for the autonomous optimization loop

## Triggers

- After every experiment completion (to log the record)
- Before every hypothesis generation (to run the pre-check)
- Monthly (database cleanup)
- Quarterly (full pattern refresh)
