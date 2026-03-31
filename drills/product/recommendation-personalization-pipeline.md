---
name: recommendation-personalization-pipeline
description: Scale AI recommendations with behavioral clustering, segment-specific models, and automated delivery across the full user base
category: Product
tools:
  - PostHog
  - Anthropic
  - Intercom
  - Loops
  - n8n
fundamentals:
  - posthog-cohorts
  - posthog-custom-events
  - posthog-feature-flags
  - posthog-user-path-analysis
  - behavior-cluster-computation
  - ai-workflow-recommendation
  - intercom-in-app-messages
  - loops-transactional
  - n8n-workflow-basics
  - n8n-scheduling
---

# Recommendation Personalization Pipeline

This drill transforms the Baseline recommendation engine from a one-model-fits-all system into a segment-aware pipeline. It uses behavioral clustering to group users into archetypes, generates segment-specific recommendation strategies, and delivers personalized suggestions at scale through automated n8n workflows.

## Input

- Recommendation engine running at Baseline level with 4+ weeks of performance data
- PostHog with 200+ active users and comprehensive event tracking
- Behavioral data: feature usage, session patterns, workflow sequences per user
- Anthropic API key for Claude
- n8n instance for automated orchestration
- Intercom and Loops configured for multi-channel delivery

## Steps

### 1. Compute behavioral clusters

Using the `behavior-cluster-computation` fundamental, analyze your user base to identify natural behavioral segments. Feed in:

- Feature usage vectors (per user, last 30 days)
- Session frequency and depth
- Primary workflow patterns
- Account age and collaboration score

Expect 4-8 clusters. Typical archetypes for a SaaS product:
- **Power Users**: high feature breadth, high session frequency, already using advanced features
- **Single-Feature Users**: deep usage of 1-2 features, ignoring the rest
- **Explorers**: broad but shallow usage, trying many features without depth
- **Declining Users**: previously active, usage trending down over 2+ weeks
- **New Arrivals**: account age < 14 days, behavior pattern still forming

Store cluster assignments as PostHog person properties (`behavior_segment_id`, `behavior_segment_label`).

### 2. Build segment-specific recommendation strategies

For each cluster, define a recommendation strategy:

- **Power Users**: Suggest advanced integrations, automation workflows, or keyboard shortcuts they have not discovered. Frame as "pro tips" not "you should try this."
- **Single-Feature Users**: Recommend the 1 feature most complementary to their primary feature. Frame as "people who use [X] also get value from [Y]."
- **Explorers**: Recommend going deeper on the feature they used most last week. Frame as "here's a faster way to [specific task]."
- **Declining Users**: Recommend the feature most correlated with retention. Frame as "you might have missed [feature] — it helps with [their primary use case]."
- **New Arrivals**: Skip AI recommendations entirely — use the onboarding flow instead.

Using `ai-workflow-recommendation`, customize the prompt context per segment so Claude generates suggestions aligned with each strategy.

### 3. Build the automated recommendation pipeline

Using `n8n-workflow-basics` and `n8n-scheduling`, create a weekly pipeline:

1. **Pull user data**: Query PostHog for all active users with their behavior vectors and cluster assignments
2. **Filter eligible users**: Exclude users who received a recommendation in the last 7 days, dismissed 3+ consecutive recommendations, are in onboarding, or have churn risk score > 70
3. **Batch by segment**: Group users by cluster ID
4. **Generate recommendations**: For each batch, call `ai-workflow-recommendation` with the segment-specific prompt and strategy
5. **Quality filter**: Reject suggestions with confidence < 0.6 or that recommend a feature the user's plan does not include
6. **Route delivery**: Active users (session in last 48h) get Intercom in-app messages; inactive users (no session in 3+ days) get Loops email
7. **Log everything**: Record `recommendation_generated`, `recommendation_delivered` events in PostHog with segment, channel, and suggestion metadata

### 4. Configure segment-specific delivery

Using `intercom-in-app-messages`, create message variants per segment:

- **Power Users**: Subtle tooltip triggered when they perform a related action. Minimal, expert tone.
- **Single-Feature Users**: Banner on dashboard with a visual showing the complementary feature. Friendly, benefit-led.
- **Explorers**: In-app post on next login with a "Quick win" framing. Specific, quantified.
- **Declining Users**: Intercom Custom Bot that opens with "We built something that helps with [their use case]." Conversational.

Using `loops-transactional`, create email variants for each segment with matching tone and framing.

### 5. Run segment-level A/B tests

Using `posthog-feature-flags`, test recommendation strategies per segment:

- Test different recommendation strategies within the same segment (e.g., for Single-Feature Users: "complementary feature" vs "efficiency tip for their primary feature")
- Test delivery timing: immediately after a session vs. next session start vs. 24h delayed email
- Test framing: quantified benefit vs. social proof vs. "new feature" framing

Run each test for 2+ weeks or until 100+ users per variant per segment.

### 6. Measure personalization lift

Using `posthog-custom-events`, compare performance metrics between the personalized pipeline and the old uniform approach:

- Adoption rate by segment (target: 15%+ improvement over non-personalized baseline)
- Dismissal rate by segment (target: 20%+ reduction)
- Feature discovery breadth per user over 30 days
- Time to first use of recommended feature

Build a PostHog dashboard showing per-segment performance: CTR, adoption rate, dismissal rate, and which recommendation categories perform best per segment.

## Output

- Behavioral cluster definitions and per-user assignments
- Segment-specific recommendation strategies
- Automated weekly pipeline in n8n
- Segment-specific Intercom message templates (4 variants)
- Segment-specific Loops email templates (4 variants)
- Per-segment A/B test configurations
- Personalization lift dashboard in PostHog

## Triggers

The pipeline runs weekly via n8n cron. Cluster re-computation runs monthly. Review segment performance and adjust strategies bi-weekly. If a segment consistently underperforms (<5% adoption rate for 4 consecutive weeks), revise the recommendation strategy for that segment.
