---
name: deprecation-segment-routing
description: Dynamically route deprecation-affected users into personalized migration paths based on their usage patterns, dependency tier, and migration velocity
category: Product
tools:
  - PostHog
  - n8n
  - Intercom
  - Loops
  - Attio
fundamentals:
  - posthog-cohorts
  - posthog-feature-flags
  - posthog-custom-events
  - n8n-triggers
  - n8n-workflow-basics
  - n8n-scheduling
  - intercom-in-app-messages
  - intercom-checklists
  - loops-sequences
  - loops-transactional
  - attio-contacts
  - attio-custom-attributes
---

# Deprecation Segment Routing

This drill scales the deprecation migration process by building dynamic routing logic that matches each user to the right migration path based on their actual behavior. At Smoke/Baseline, every user gets roughly the same experience. At Scalable, the system needs to handle hundreds of users across different dependency levels, usage patterns, and migration velocities — each needing a different approach.

## Input

- Deprecation migration tracker running with per-user scores
- At least 50 users in the migration pipeline
- Multiple migration paths available (self-serve wizard, guided tour, video walkthrough, 1:1 session)
- PostHog cohorts and Attio records populated from the migration tracker

## Steps

### 1. Define migration path archetypes

Based on observed migration patterns, create routing rules:

| User Pattern | Identified By | Routed To |
|-------------|---------------|-----------|
| Self-starter | Clicked CTA, used replacement within 48h | Self-serve: Intercom checklist only |
| Needs guidance | Clicked CTA, did NOT use replacement within 7 days | Guided: Intercom product tour + 2-email Loops sequence |
| Workflow-dependent | Critical tier + uses deprecated feature in 3+ distinct workflows | High-touch: Personal migration plan + Cal.com session + Loops sequence with workflow-specific guides |
| Resistant | Regressed after trying replacement OR dismissed all notices | Rescue: Direct Attio task for account owner + personalized Loops email addressing specific objections |
| Passive | Low tier + has not engaged with any deprecation notice | Light touch: Single Loops reminder email 14 days before sunset |

### 2. Build the routing workflow

Using `n8n-workflow-basics`, create a workflow triggered daily that evaluates each user in the deprecation cohort:

1. Pull the user's migration score, tier, stall status, and engagement history from Attio (via `attio-contacts`)
2. Apply the routing rules from Step 1
3. Check if the user is already in an active migration path (avoid duplicate routing)
4. If the user's pattern changed (e.g., was a self-starter but has stalled), re-route to the next appropriate path
5. Fire the appropriate action for each route

### 3. Implement self-serve path

Using `intercom-checklists`, create a migration checklist that appears in the product for self-starter users:

- [ ] Open the replacement feature
- [ ] Import your data from [old feature]
- [ ] Set up your first workflow in the replacement
- [ ] Verify your workflows are working
- [ ] Confirm migration complete

Using `posthog-feature-flags`, show the checklist only to users routed to the self-serve path.

### 4. Implement guided path

For users who need guidance, trigger a multi-step journey:

1. `intercom-in-app-messages`: Show an in-app message with a video walkthrough of the migration process
2. `loops-sequences`: Enroll in a 2-email sequence:
   - Email 1 (immediate): "Here's your migration guide" with step-by-step instructions and screenshots
   - Email 2 (Day 3): "Need help? Here are the top 3 questions we're hearing" with FAQ and support link
3. If still stalled after the sequence, escalate to high-touch path

### 5. Implement high-touch path

For workflow-dependent users:

1. Using `attio-contacts`, create a task for the account owner with the user's workflow map (from deprecation impact assessment)
2. Using `loops-transactional`, send a personalized email: "We know you use [deprecated feature] in {N} workflows. We've prepared a migration plan specific to your setup."
3. Include a Cal.com booking link for a 1:1 migration session
4. Track whether they book and attend the session via PostHog events

### 6. Implement rescue path

For resistant users:

1. Using `attio-contacts`, create a high-priority task for the account owner
2. The task includes: which deprecation notices the user dismissed, whether they tried the replacement and when they reverted, their MRR, and their feature usage patterns
3. Using `loops-transactional`, send a message from the product team (not marketing): "We noticed you tried [replacement] and went back to [old feature]. We want to understand what didn't work."
4. Include a Typeform survey link (3 questions max) to capture their objection

### 7. Track routing effectiveness

Using `posthog-custom-events`, log every routing decision and its outcome:

```javascript
posthog.capture('deprecation_route_assigned', {
  feature_slug: '{feature_slug}',
  route: 'guided',
  tier: 'high',
  migration_score_at_routing: 10
});

posthog.capture('deprecation_route_completed', {
  feature_slug: '{feature_slug}',
  route: 'guided',
  tier: 'high',
  migration_score_at_completion: 100,
  days_to_complete: 12
});
```

Calculate per-route: completion rate, median days to complete, and cost per migration (staff time for high-touch/rescue). This data feeds back into the routing rules — if guided users complete at the same rate as high-touch users, stop over-investing in 1:1 sessions.

### 8. Scale with PostHog feature flags

Using `posthog-feature-flags`, create flags that control which migration experience each user sees:

- `deprecation-{slug}-self-serve`: Self-serve checklist visible
- `deprecation-{slug}-guided`: Guided tour + email sequence active
- `deprecation-{slug}-high-touch`: Personal migration plan active
- `deprecation-{slug}-rescue`: Rescue flow active

The n8n routing workflow sets these flags automatically. No manual intervention needed to route users.

## Output

- Dynamic routing workflow in n8n that evaluates and routes users daily
- Four distinct migration paths (self-serve, guided, high-touch, rescue) with appropriate tooling
- PostHog feature flags controlling which experience each user sees
- Routing effectiveness tracking with per-route metrics
- Automatic re-routing when user behavior changes

## Triggers

Runs daily via the n8n routing workflow. Re-routing evaluations happen automatically when migration scores change. Review routing rule effectiveness weekly and adjust thresholds based on completion data.
