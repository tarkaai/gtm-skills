---
name: workflow-behavior-analysis
description: Analyze user behavior sequences to identify workflow inefficiencies, missed features, and optimization opportunities
category: Enablement
tools:
  - PostHog
  - Anthropic
fundamentals:
  - posthog-user-path-analysis
  - posthog-cohorts
  - posthog-custom-events
  - posthog-session-recording
  - ai-workflow-recommendation
---

# Workflow Behavior Analysis

This drill builds the data pipeline that powers proactive workflow optimization suggestions. It analyzes how users actually work in your product, compares their patterns to power users, identifies inefficiencies, and generates specific improvement recommendations using AI.

## Input

- PostHog tracking configured with custom events for all core product actions (not just pageviews)
- At least 30 days of event data with 50+ active users
- Power user cohort defined in PostHog (top 10% by usage volume or feature breadth)
- Anthropic API key for Claude

## Steps

### 1. Define the workflow event taxonomy

Before analyzing paths, ensure your product tracks the right events. Using `posthog-custom-events`, verify that these event categories are instrumented:

- **Workflow start/end events**: `workflow_started`, `workflow_completed` with properties `{workflow_type, duration_seconds}`
- **Feature usage events**: `feature_used` with property `{feature_name, context}`
- **Efficiency signals**: `keyboard_shortcut_used`, `template_applied`, `automation_triggered`
- **Friction signals**: `action_undone`, `error_encountered`, `same_action_repeated` (3+ times in 60 seconds)
- **Navigation events**: `search_used`, `menu_navigated`, `breadcrumb_clicked`

If any category is missing, instrument it before proceeding. Path analysis without complete event coverage produces blind spots.

### 2. Build the power user benchmark

Using `posthog-cohorts`, create or refine the Power Users cohort:

- Criteria: users active 20+ of the last 30 days AND used 5+ distinct features AND completed 10+ workflows
- Extract their aggregate behavior profile:
  - Most-used features (ranked by frequency)
  - Average workflow completion time by workflow type
  - Feature discovery breadth (how many features they use)
  - Shortcut and automation adoption rate

This benchmark is the target state. Every suggestion aims to move a user closer to this profile.

### 3. Run path analysis for each user segment

Using `posthog-user-path-analysis`, run the transition matrix query to map how users flow through your product. Break the analysis down by cohort:

- **New users** (signed up < 14 days ago): Are they finding the optimal path to first value?
- **Regular users** (active 30+ days, not power users): Where do their workflows diverge from power users?
- **Declining users** (usage dropped 30%+ in last 2 weeks): What changed in their behavior?

For each segment, identify:
- The 3 most common "detour" sequences (extra steps that power users skip)
- The 3 most-used features by power users that this segment ignores
- The average time penalty of inefficient paths vs. optimal paths

### 4. Detect repeated manual patterns

Query PostHog for users who repeat the same 3+ step sequence 5+ times per week. These are automation candidates — the user is doing something manually that could be streamlined.

```
Pattern detection query:
- Group events by person_id
- Identify subsequences of length 3-5 that appear 5+ times in a 7-day window
- Rank by frequency and number of affected users
```

Tag each detected pattern with: the sequence, frequency, affected user count, and estimated time spent on repetitions.

### 5. Generate AI-powered suggestions

For each user (or segment at Smoke/Baseline level), use `ai-workflow-recommendation` to generate 3 ranked suggestions. Feed in:

- The user's actual event sequence (last 50 actions)
- Their feature usage vs. power user benchmark
- Detected repeated patterns
- Time-on-task vs. power user benchmark
- Error/retry frequency

The AI generates specific, quantified suggestions: "Use the bulk edit feature instead of editing items one at a time. You edited 47 items individually last week — bulk edit would reduce this from ~25 minutes to ~3 minutes."

### 6. Validate suggestions against session recordings

Using `posthog-session-recording`, pull 5-10 recordings of users performing the workflows targeted by each suggestion. Verify:

- The inefficiency actually exists (not a data artifact)
- The suggested improvement is physically possible given the UI
- The user's workflow context makes the suggestion relevant (not suggesting a feature for a workflow they rarely do)

Discard suggestions that do not survive recording validation. Replace with the next-ranked suggestion from the AI.

## Output

- Power user benchmark profile (feature usage, workflow times, efficiency metrics)
- Per-segment path analysis with identified detours and feature gaps
- Repeated manual pattern catalog with automation candidates
- Validated suggestion queue: per-user or per-segment suggestions ready for delivery
- Session recording evidence for each suggestion category

## Triggers

Run the full analysis weekly at Baseline level. At Scalable and Durable levels, run incrementally: update the power user benchmark monthly, run per-user path analysis daily (batched overnight), and regenerate suggestions weekly.
