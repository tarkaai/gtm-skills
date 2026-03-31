---
name: ai-user-segmentation-smoke
description: >
  AI Behavior Segmentation -- Smoke Test. Run the behavior clustering pipeline once
  on a sample of active users to validate that LLM-based segmentation produces distinct,
  interpretable behavioral clusters with measurable retention differences between segments.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=5 distinct behavioral segments identified with >=15pp retention spread between highest and lowest segment"
kpis: ["Segment count", "Segment stability", "Retention spread across segments", "Unclassified user rate"]
slug: "ai-user-segmentation"
install: "npx gtm-skills add product/retain/ai-user-segmentation"
drills:
  - behavior-segmentation-pipeline
  - threshold-engine
---
# AI Behavior Segmentation -- Smoke Test

> **Stage:** Product -> Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

Prove that LLM-based behavioral clustering produces distinct, meaningful user segments from your product's usage data. At this level, everything runs once by hand. You extract behavior vectors from PostHog, run them through Claude's clustering, and validate that the resulting segments have genuinely different retention rates. No automation, no personalization yet -- just proof that the signal exists.

**Pass threshold:** >=5 distinct behavioral segments AND >=15 percentage points retention spread between the highest-retaining and lowest-retaining segment.

## Leading Indicators

- Cluster discovery returns 4-8 segments (not 2-3 generic buckets or 10+ micro-segments)
- Each segment has a human-readable label that your team recognizes as a real user archetype
- Unclassified user rate is <15% (most users fit cleanly into a segment)
- Segment size distribution is balanced: no single segment contains >40% of users

## Instructions

### 1. Verify PostHog tracking coverage

Before running the pipeline, confirm you have sufficient behavioral data in PostHog. Query the last 30 days:

```sql
SELECT
  count(DISTINCT person_id) AS active_users,
  count(DISTINCT event) AS distinct_events,
  count() AS total_events
FROM events
WHERE timestamp > now() - interval 30 day
  AND event NOT IN ('$pageview', '$pageleave', '$autocapture')
```

You need at least 100 active users and 5+ distinct custom events to produce meaningful segments. If you have fewer, instrument more product features using the `posthog-gtm-events` drill before proceeding.

### 2. Extract behavior vectors manually

Run the `behavior-segmentation-pipeline` drill's step 1 (extract behavior vectors) manually. Execute the HogQL query against your PostHog project. Replace the placeholder feature event names (`feature_a_used`, etc.) with your actual tracked events. Export the results as JSON.

**Human action required:** Map your product's feature events to the vector schema. List your 5-10 core features by event name. Decide what counts as a "collaboration action" for your product. If your product has no collaboration features, set collaboration score to 0 for all users and note that this dimension will not contribute to clustering.

### 3. Run cluster discovery

Take a random sample of 100-200 users from the extracted vectors. Pass them to the `behavior-cluster-computation` fundamental's cluster discovery API call. Use the Anthropic API directly or via the Claude CLI.

Review the returned clusters. For each cluster, check:
- Does the label make intuitive sense? Would your team recognize this user type?
- Are the defining signals specific and behavioral (not just "high usage" vs "low usage")?
- Is the estimated percentage reasonable (no cluster at 60% or 1%)?

If the clusters are too generic (e.g., just "active" and "inactive"), add more behavior dimensions to the vectors: workflow sequences from step 3 of the pipeline drill, or time-of-day patterns.

### 4. Assign all active users to clusters

Run the `behavior-cluster-computation` fundamental's user assignment call. Process all active users in batches of 30. Record each user's cluster ID, label, and confidence.

Write the assignments to PostHog as person properties: `behavior_segment_id`, `behavior_segment_label`, `behavior_segment_confidence`. You can do this via the PostHog API or by firing `behavior_segment_assigned` events with `$set` person properties.

### 5. Measure retention by segment

Using PostHog, compute 14-day retention for each segment. Create a cohort for each segment (using the `behavior_segment_id` person property), then run a retention analysis:

For each segment cohort, query:
```sql
SELECT
  behavior_segment_label,
  count(DISTINCT person_id) AS segment_size,
  countIf(returned_within_14d = true) / count(DISTINCT person_id) AS retention_14d
FROM (
  SELECT
    e1.person_id,
    e1.properties.behavior_segment_label AS behavior_segment_label,
    EXISTS(
      SELECT 1 FROM events e2
      WHERE e2.person_id = e1.person_id
        AND e2.timestamp > e1.timestamp + interval 7 day
        AND e2.timestamp < e1.timestamp + interval 21 day
        AND e2.event NOT IN ('$pageview', '$pageleave', '$autocapture')
    ) AS returned_within_14d
  FROM events e1
  WHERE e1.event = 'behavior_segment_assigned'
    AND e1.timestamp > now() - interval 30 day
)
GROUP BY behavior_segment_label
```

Calculate the retention spread: highest segment retention minus lowest segment retention. This is the primary validation metric.

### 6. Evaluate against threshold

Run the `threshold-engine` drill to evaluate: did you identify >=5 distinct segments AND achieve >=15pp retention spread?

If PASS: The signal is real. Different behavior patterns predict different retention outcomes. Proceed to Baseline to automate the pipeline and start personalizing.

If FAIL -- fewer than 5 segments: Your product usage is too homogeneous, or the behavior vectors lack discriminating signals. Add more feature events, include workflow sequences, or segment by time-of-day patterns. Re-run discovery.

If FAIL -- retention spread <15pp: The segments are distinct in behavior but not in outcome. Try weighting the behavior vectors differently (e.g., emphasize collaboration and feature breadth over raw session count). Or the product experience is too uniform -- segments cannot differ in retention if every user gets the same experience.

## Time Estimate

- 1 hour: Verify PostHog tracking, map feature events to vector schema
- 1 hour: Extract behavior vectors and assemble JSON
- 1 hour: Run cluster discovery and review results
- 1 hour: Assign all users to clusters and write to PostHog
- 1 hour: Compute retention by segment and analyze spread
- 1 hour: Evaluate threshold, document findings, plan Baseline

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Behavior data extraction, retention analysis, cohorts | Free tier (1M events/mo) or existing plan -- [posthog.com/pricing](https://posthog.com/pricing) |
| Claude API (Anthropic) | Cluster discovery and user assignment | ~$0.15 total for this run (1 discovery + 4-7 assignment batches) -- [anthropic.com/pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |

**Estimated play-specific cost:** Free to ~$0.15 (Claude API for clustering)

## Drills Referenced

- `behavior-segmentation-pipeline` -- Extracts behavior vectors, runs LLM clustering, assigns users to segments
- `threshold-engine` -- Evaluates results against the pass threshold
