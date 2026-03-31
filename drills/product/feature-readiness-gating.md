---
name: feature-readiness-gating
description: Define readiness signals per feature tier and gate advanced features behind them using PostHog and Intercom
category: Product
tools:
  - PostHog
  - Intercom
  - n8n
fundamentals:
  - posthog-feature-flags
  - posthog-custom-events
  - posthog-cohorts
  - intercom-in-app-messages
  - intercom-product-tours
  - n8n-triggers
  - n8n-workflow-basics
---

# Feature Readiness Gating

This drill implements progressive feature disclosure: advanced features are hidden until users demonstrate readiness by completing prerequisite actions. Instead of showing everything at once (which overwhelms new users) or time-gating (which frustrates fast learners), features unlock based on behavior signals that indicate the user is ready to benefit from them.

## Input

- A complete list of your product's features, categorized into tiers (Core, Intermediate, Advanced, Power)
- PostHog tracking installed with user identification
- Intercom configured for in-app messaging and product tours
- n8n instance for automation workflows

## Steps

### 1. Map features to readiness tiers

Categorize every feature into four tiers based on complexity and prerequisite knowledge:

| Tier | Description | Unlock Condition | Example |
|------|-------------|-----------------|---------|
| Core | Essential actions every user needs immediately | Available on signup | Create a project, add a task |
| Intermediate | Features that build on Core mastery | Completed 3+ Core actions in 2+ sessions | Templates, bulk actions, basic integrations |
| Advanced | Features requiring product familiarity | Used 2+ Intermediate features, active 7+ days | Automation rules, custom fields, API access |
| Power | Expert features for sophisticated workflows | Used 1+ Advanced feature for 14+ days | Webhooks, custom scripts, admin controls |

For each feature, define exactly which prior actions constitute "readiness." Be specific: "Created 3 projects AND added tasks to each" not "used the product enough."

### 2. Define readiness signals as PostHog events

Using the `posthog-custom-events` fundamental, instrument every readiness-qualifying action:

```javascript
// Core completion signals
posthog.capture('core_action_completed', {
  action: 'project_created',
  tier: 'core',
  count: projectCount,
  session_number: sessionNumber
});

// Tier unlock events
posthog.capture('feature_tier_unlocked', {
  tier: 'intermediate',
  trigger_action: 'third_core_action_in_second_session',
  time_to_unlock_hours: hoursSinceSignup
});
```

Track these events for every qualifying action:
- `core_action_completed` with the specific action name and running count
- `intermediate_feature_first_used` when a user engages with an unlocked Intermediate feature
- `advanced_feature_first_used` when a user engages with an unlocked Advanced feature
- `feature_tier_unlocked` when a user transitions to a new tier

### 3. Build readiness cohorts in PostHog

Using the `posthog-cohorts` fundamental, create cohorts that represent each readiness state:

- **Core Only**: Signed up but has not met Intermediate unlock criteria
- **Intermediate Ready**: Met Intermediate criteria but not Advanced
- **Advanced Ready**: Met Advanced criteria but not Power
- **Power Ready**: Met all criteria, all features available
- **Stalled at Core**: Signed up 7+ days ago, still Core Only (intervention needed)
- **Fast Progressors**: Unlocked Intermediate within 48 hours of signup

These cohorts drive both the feature gating logic and the reveal messaging.

### 4. Implement feature gating with PostHog feature flags

Using the `posthog-feature-flags` fundamental, create a feature flag per gated feature tier:

```
POST /api/projects/<id>/feature_flags/
{
  "key": "tier-intermediate-features",
  "name": "Intermediate Feature Tier",
  "filters": {
    "groups": [{
      "properties": [{
        "key": "id",
        "value": <intermediate-ready-cohort-id>,
        "type": "cohort"
      }]
    }]
  },
  "active": true
}
```

Create flags: `tier-intermediate-features`, `tier-advanced-features`, `tier-power-features`. In your product code, check the flag before rendering each gated feature. When the flag is false, show a locked state with a hint about what the user needs to do to unlock it.

### 5. Build unlock reveal moments

Using the `intercom-in-app-messages` fundamental, create a celebration message for each tier unlock:

- **Intermediate unlock**: Banner message -- "You've mastered the basics. New tools are now available: [list 2-3 key Intermediate features]. Try [most impactful one] next."
- **Advanced unlock**: Modal with a short product tour invitation -- "You're ready for automation. Take a 60-second tour of what just unlocked."
- **Power unlock**: Subtle notification -- "All features are now available. You've earned full access."

Each message links directly to the newly unlocked feature, not to a generic dashboard. The reveal is the reward for demonstrating readiness.

### 6. Build the unlock automation workflow

Using `n8n-triggers` and `n8n-workflow-basics`, create an n8n workflow that:

1. Listens for PostHog webhook events (`core_action_completed`, `intermediate_feature_first_used`, etc.)
2. Evaluates the user's current readiness state against tier criteria
3. When a user qualifies for a new tier: updates their PostHog person properties (`feature_tier: "intermediate"`), which triggers the cohort-based feature flag to activate
4. Fires an Intercom event to trigger the unlock message
5. Logs the tier transition in your CRM

This workflow runs in real-time so users see features unlock immediately after qualifying, not on a delay.

### 7. Handle the locked state UX

For features the user has not unlocked yet, decide between two strategies:

- **Hidden**: Feature is completely invisible until unlocked. Simpler, but users do not know what they are working toward.
- **Teased**: Feature is visible but grayed out with a tooltip explaining the unlock condition. More motivating, but adds UI complexity.

Use the "Teased" approach for features one tier above the user's current level. Hide features two or more tiers above. This gives users a visible goal without overwhelming them with everything they cannot access yet.

For teased features, the tooltip should be specific: "Complete 2 more projects to unlock Templates" not "Upgrade to access this feature."

## Output

- Feature tier map: every feature assigned to Core, Intermediate, Advanced, or Power
- PostHog events tracking all readiness signals and tier transitions
- PostHog cohorts for each readiness state
- PostHog feature flags gating each tier
- Intercom unlock messages for each tier transition
- n8n workflow automating the readiness evaluation and unlock pipeline
- Locked-state UX for teased features

## Triggers

Run once during initial play setup. Re-run when adding new features to the product (assign them to a tier and gate them) or when adjusting readiness criteria based on data.
