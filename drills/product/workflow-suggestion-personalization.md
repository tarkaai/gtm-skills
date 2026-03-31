---
name: workflow-suggestion-personalization
description: Segment users by behavior profile and tailor workflow suggestions to role, usage maturity, and workflow patterns
category: Product
tools:
  - PostHog
  - Anthropic
  - Intercom
  - n8n
fundamentals:
  - posthog-cohorts
  - posthog-feature-flags
  - posthog-custom-events
  - ai-workflow-recommendation
  - intercom-user-properties
  - n8n-workflow-basics
  - n8n-scheduling
---

# Workflow Suggestion Personalization

This drill adds segment-level personalization to workflow optimization suggestions. Instead of one-size-fits-all recommendations, each user receives suggestions matched to their role, usage maturity, workflow patterns, and learning style. This is the multiplier that takes suggestion acceptance from 20% to 40%+.

## Input

- `workflow-behavior-analysis` drill running with per-user path data
- `workflow-suggestion-delivery` drill operational with tracking
- PostHog with 8+ weeks of suggestion delivery and acceptance data
- At least 500 active users (volume needed for meaningful segments)

## Steps

### 1. Define behavior-based user segments

Using `posthog-cohorts`, create segments that predict suggestion receptivity. Do not use static demographics — use actual behavior:

**By usage maturity:**
- **Beginners** (< 30 days, < 50% feature discovery): Need discovery suggestions. Suggest foundational features they have not found yet.
- **Intermediates** (30-90 days, 50-80% feature discovery): Need efficiency suggestions. They know the features but use them suboptimally.
- **Advanced** (90+ days, 80%+ feature discovery): Need automation suggestions. They have mastered the basics and benefit from workflow automation.

**By workflow pattern:**
- **Sequential workers**: Complete tasks in long, linear sequences. Suggest parallel processing and batch operations.
- **Explorers**: Jump between features frequently. Suggest favorites, dashboards, and quick-access patterns.
- **Specialists**: Use 2-3 features deeply, ignore the rest. Suggest complementary features that enhance their core workflow.

**By suggestion response history:**
- **Adopters**: Accepted 2+ past suggestions. Ready for more complex recommendations.
- **Browsers**: View suggestions but rarely adopt. Need lower-friction suggestions with clearer benefits.
- **Dismissers**: Consistently dismiss. Reduce suggestion frequency to 1/month, make them high-confidence only.

### 2. Build the segmentation pipeline

Using `n8n-scheduling`, create a weekly workflow that:

1. Queries PostHog for each user's feature usage breadth, account age, workflow patterns, and suggestion history
2. Classifies each user into maturity + pattern + response segments
3. Writes the segment assignments to PostHog person properties: `workflow_maturity`, `workflow_pattern`, `suggestion_responsiveness`
4. Syncs segment properties to Intercom using `intercom-user-properties` for in-app targeting

### 3. Create segment-specific suggestion templates

For each maturity x pattern combination, configure the AI suggestion prompt differently using `ai-workflow-recommendation`:

**Beginners + Sequential**: Focus on "did you know [feature] exists?" suggestions for features that are adjacent to their current workflow. Keep steps under 3. Use screenshot references.

**Intermediates + Specialists**: Focus on "combine [feature A] with [feature B]" suggestions that expand their capability without abandoning their core pattern. Quantify the efficiency gain.

**Advanced + Explorers**: Focus on "automate [repeated pattern]" and "create a custom shortcut for [frequent action]" suggestions. These users can handle complexity.

### 4. Configure segment-based delivery rules

Using `posthog-feature-flags`, create feature flags that control suggestion frequency and channel per segment:

- **Adopters**: Up to 2 suggestions per week, in-app preferred
- **Browsers**: 1 suggestion per week, use Intercom Custom Bot (interactive > passive)
- **Dismissers**: 1 suggestion per month, email only (less intrusive), highest confidence suggestions only

Using `n8n-workflow-basics`, update the delivery pipeline to read segment properties and apply the correct frequency cap, channel, and suggestion template.

### 5. Run per-segment A/B tests

For each segment, test variations of the suggestion format using PostHog experiments:

- **Copy style**: Quantified benefit ("saves 5 min/day") vs. social proof ("used by 80% of power users") vs. curiosity ("most people miss this feature")
- **Timing**: Immediately when the inefficiency occurs vs. at session start vs. at session end
- **Depth**: One-line tooltip vs. 3-step walkthrough vs. video gif

Run each test for 2 weeks minimum. Use the segment-specific acceptance rate as the primary metric.

### 6. Track per-segment performance

Using `posthog-custom-events`, add segment properties to all suggestion events:

```
suggestion_delivered → {suggestion_id, category, channel, workflow_maturity, workflow_pattern, suggestion_responsiveness}
suggestion_adopted   → {same properties + adopted_within_days}
```

Build a PostHog dashboard with:
- Suggestion acceptance rate by maturity segment (line chart, weekly)
- Suggestion acceptance rate by pattern segment (line chart, weekly)
- Best-performing suggestion category per segment (table, monthly)
- Channel effectiveness per segment (bar chart, monthly)

Target: every segment achieves 15%+ overall adoption rate. If a segment is below 15%, investigate whether the suggestions are relevant, the format is wrong, or the timing is off.

## Output

- 3 maturity segments, 3 pattern segments, 3 response segments in PostHog
- Weekly segmentation pipeline in n8n
- Segment-specific AI prompt configurations
- Segment-based delivery rules via feature flags
- Per-segment performance dashboard in PostHog

## Triggers

Segmentation pipeline runs weekly via n8n. Segment definitions reviewed monthly. A/B tests run continuously, cycling through format variations per segment.
