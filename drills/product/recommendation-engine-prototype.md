---
name: recommendation-engine-prototype
description: Build a minimal AI recommendation engine that analyzes user behavior and surfaces contextual feature suggestions
category: Product
tools:
  - PostHog
  - Anthropic
  - Intercom
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - posthog-user-path-analysis
  - ai-workflow-recommendation
  - intercom-in-app-messages
---

# Recommendation Engine Prototype

This drill builds the first version of an AI-powered recommendation engine. It connects PostHog behavior data to the Claude API to generate personalized feature-discovery suggestions, then surfaces them via Intercom in-app messages. The goal is proving that AI-generated recommendations produce measurable engagement — not building a production system.

## Input

- PostHog tracking installed with at least 14 days of event data
- At least 20 active users with meaningful usage history
- Anthropic API key for Claude
- Intercom configured for in-app messaging
- A list of product features with descriptions and which events indicate usage

## Steps

### 1. Define the feature catalog

Create a JSON document listing every product feature an AI recommendation could surface:

```json
{
  "features": [
    {
      "name": "Bulk Edit",
      "description": "Edit multiple items at once instead of one-by-one",
      "trigger_event": "bulk_edit_started",
      "prerequisite": "Has created 5+ items",
      "benefit": "Saves ~20 minutes per batch vs individual edits",
      "plan_required": "free"
    }
  ]
}
```

Include 10-20 features. For each, define: what it does, the PostHog event that proves someone used it, what prerequisite behavior the user should have before this recommendation makes sense, the quantified benefit, and the minimum plan required.

### 2. Build the behavior snapshot query

Using `posthog-custom-events`, pull the data the AI needs per user:

- Last 50 events (action sequence)
- Feature usage counts over the last 30 days
- Features from the catalog the user has NOT used
- Average session duration and frequency
- Any repeated action sequences (same 3-step pattern 3+ times)

Run this as a PostHog HogQL query or via the PostHog API. At Smoke level, do this manually for 10-20 users.

### 3. Generate recommendations via Claude

For each user, call the `ai-workflow-recommendation` fundamental. Pass:

- The feature catalog (as undiscovered features)
- The user's behavior snapshot
- A power-user benchmark (aggregate the top 20% of users by feature breadth)

Claude returns 3 ranked suggestions with specific actions, quantified benefits, and step-by-step instructions.

### 4. Review and filter suggestions

Before delivering any recommendation, manually review the first batch:

- Does the suggestion match the user's actual workflow?
- Is the suggested feature available on the user's plan?
- Is the benefit claim reasonable?
- Would this feel helpful or intrusive?

Discard suggestions that fail any check. At Smoke level, expect to discard 20-30% of AI output.

**Human action required:** Review the first 20 generated suggestions and approve or reject each one. This calibrates quality expectations before any automation.

### 5. Deliver recommendations via Intercom

Using `intercom-in-app-messages`, create a recommendation message template:

- Format: non-blocking banner or tooltip, NOT a modal
- Content: "[Feature name]: [one-sentence benefit]. [Quantified impact based on their usage]."
- CTA: "Try it now" deep-linking to the feature
- Dismissal: one-click dismiss, never show the same recommendation twice

Deliver the top-ranked approved suggestion to each user in the test group.

### 6. Track recommendation performance

Using `posthog-custom-events`, instrument:

```
recommendation_shown     -> {user_id, recommendation_id, feature_name, source: "ai"}
recommendation_clicked   -> {user_id, recommendation_id, feature_name}
recommendation_adopted   -> {user_id, recommendation_id, feature_name, days_to_adopt}
recommendation_dismissed -> {user_id, recommendation_id, feature_name}
```

Define "adopted" as: the user performed the recommended feature's trigger event within 7 days of seeing the recommendation.

Calculate: show rate, click-through rate, adoption rate, and dismissal rate.

## Output

- Feature catalog JSON (10-20 features with metadata)
- Per-user behavior snapshot queries
- AI-generated recommendation set for test group
- Intercom recommendation message template
- PostHog event tracking for the full recommendation lifecycle
- Performance data: CTR, adoption rate, dismissal rate

## Triggers

At Smoke level, this is a one-time manual run. Generate recommendations once, deliver once, measure once. If adoption rate exceeds the play's pass threshold, proceed to Baseline where the pipeline becomes automated.
