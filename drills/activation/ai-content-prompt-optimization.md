---
name: ai-content-prompt-optimization
description: Systematically improve AI content generation quality by analyzing rejection patterns, tuning system prompts, and running prompt A/B tests
category: Enablement
tools:
  - PostHog
  - n8n
  - Anthropic
fundamentals:
  - posthog-experiments
  - posthog-feature-flags
  - posthog-custom-events
  - n8n-workflow-basics
  - hypothesis-generation
  - experiment-evaluation
---

# AI Content Prompt Optimization

This drill systematically improves the quality of AI-generated content by analyzing why users reject or heavily edit output, tuning system prompts based on observed patterns, and running controlled experiments to validate improvements. It is the play-specific optimization layer that feeds into the broader `autonomous-optimization` loop at Durable level.

## Input

- AI content feature with PostHog event tracking (see `ai-content-usage-health-monitor` drill for event taxonomy)
- At least 30 days of generation data with acceptance/rejection/edit signals
- Access to modify system prompts or model configuration for the AI content feature
- PostHog experiments enabled for feature flag-based A/B testing

## Steps

### 1. Analyze rejection and edit patterns

Query PostHog for the last 30 days of AI content interactions. For each content type, compute:

- **Acceptance rate**: `ai_content_accepted / ai_content_generated`
- **Clean acceptance rate**: `(ai_content_accepted AND NOT ai_content_edited) / ai_content_generated` -- content good enough to use without changes
- **Heavy edit rate**: accepted content where edit distance is >50% of original generation
- **Regeneration rate**: `ai_content_regenerated / ai_content_generated`
- **Rejection reasons**: if you capture feedback text on rejection, cluster it into categories (too long, off-topic, wrong tone, factual errors, formatting issues)

Rank content types by quality gap: the difference between generation volume (demand) and clean acceptance rate (satisfaction). The content type with the highest volume and lowest clean acceptance rate is priority 1 for optimization.

### 2. Generate improvement hypotheses

Run `hypothesis-generation` with the rejection pattern data:

Input context: content type, current system prompt, sample rejected outputs, rejection reason clusters, current acceptance rate, target acceptance rate.

The agent produces 3 ranked hypotheses, e.g.:
- "Blog post generations are too formal because the system prompt specifies 'professional tone' -- switching to 'conversational, expert tone' will increase acceptance by 10pp"
- "Social post generations are too long because the system prompt has no length constraint -- adding 'under 280 characters' will reduce regeneration rate by 20%"
- "Email subject lines are generic because the system prompt does not include company context -- injecting the user's product description will increase clean acceptance by 15pp"

### 3. Design the prompt experiment

Using `posthog-feature-flags`, create a feature flag that routes users between:
- **Control**: Current system prompt
- **Variant**: Modified system prompt based on the top hypothesis

Using `posthog-experiments`, configure the experiment:
- Primary metric: clean acceptance rate for the target content type
- Secondary metrics: regeneration rate, edit rate, generation time
- Minimum sample: 100 generations per variant (not users -- generations, since one user may generate multiple times)
- Duration: minimum 7 days or until sample size is reached

### 4. Implement the prompt variant

In your AI content feature's backend, check the PostHog feature flag before selecting the system prompt. Route control users to the current prompt and variant users to the modified prompt. Log the variant assignment as a PostHog event property on every `ai_content_generated` event:

```json
{
  "event": "ai_content_generated",
  "properties": {
    "prompt_experiment": "blog-tone-v2",
    "prompt_variant": "conversational",
    "content_type": "blog_post"
  }
}
```

### 5. Evaluate and implement

When the experiment reaches its planned sample size:

1. Pull experiment results from PostHog
2. Run `experiment-evaluation` with control vs variant metrics
3. Decision matrix:
   - **Clean acceptance rate improved 5%+ with no regression on other metrics**: Adopt. Update the production system prompt.
   - **Metrics improved <5%**: Not significant. Log the result. Move to the next hypothesis.
   - **Regression on secondary metrics**: Revert. Investigate what the prompt change broke.
4. Document: hypothesis, variant prompt text, sample size, result, decision, reasoning

### 6. Build the prompt version registry

Maintain a log (in Attio or a version-controlled file) tracking every system prompt version:

```
| Version | Content Type | Change Description | Acceptance Rate (before) | Acceptance Rate (after) | Status |
|---------|-------------|-------------------|-------------------------|------------------------|--------|
| v1.0    | blog_post   | Baseline prompt    | 42%                     | --                     | Retired |
| v1.1    | blog_post   | Conversational tone | 42%                     | 55%                    | Active |
| v2.0    | social_post | Added length constraint | 38%                | 51%                    | Active |
```

This registry prevents repeating failed experiments and shows the cumulative improvement from optimization.

## Output

- Rejection pattern analysis by content type
- Ranked improvement hypotheses
- Feature flag-based prompt A/B test
- Evaluated results with adopt/revert decision
- Prompt version registry tracking cumulative improvement

## Triggers

Run this drill monthly, or immediately when the `ai-content-usage-health-monitor` detects a critical decline in acceptance rate or satisfaction score. At Durable level, the `autonomous-optimization` drill triggers this drill automatically when it detects content quality anomalies.
