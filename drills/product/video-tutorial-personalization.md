---
name: video-tutorial-personalization
description: Route users to persona-specific video tutorials based on behavior, role, and onboarding progress using PostHog cohorts and Intercom
category: Enablement
tools:
  - PostHog
  - Intercom
  - Loops
  - n8n
  - Loom
fundamentals:
  - posthog-cohorts
  - posthog-feature-flags
  - posthog-custom-events
  - intercom-in-app-messages
  - intercom-product-tours
  - loops-sequences
  - n8n-scheduling
  - n8n-workflow-basics
  - loom-workspace-management
---

# Video Tutorial Personalization

This drill builds a system that serves the right video tutorial to the right user at the right time. Instead of showing every user the same video library, it routes users to persona-specific tutorials based on their role, behavior, and onboarding progress.

## Input

- At least 15 published video tutorials across 3+ categories
- PostHog cohorts from the `video-tutorial-engagement-tracking` drill
- Persona definitions (from `icp-definition` or `onboarding-personalization`)
- Intercom configured for in-app messaging
- Loops configured for lifecycle emails
- n8n instance for orchestration

## Steps

### 1. Map tutorials to personas and onboarding stages

Create a tutorial routing matrix. For each persona, define which tutorials are relevant at each onboarding stage:

| Persona | Stage 1 (First Session) | Stage 2 (Setup Complete) | Stage 3 (First Value) | Stage 4 (Regular Use) |
|---------|------------------------|--------------------------|----------------------|----------------------|
| Admin | Account setup, Team invites | Permissions config, SSO setup | Custom workflows | Advanced reporting |
| End User | Quick start, Core workflow | Templates, Shortcuts | Collaboration features | Integrations |
| Data Analyst | Data import, Query basics | Custom fields, Filters | Dashboard creation | API access, Exports |

Each cell maps to 1-2 specific Loom video IDs. No user should see more than 2 video recommendations at a time.

### 2. Build persona detection via PostHog

Using `posthog-feature-flags`, create feature flags that segment users by persona:

```
Flag: tutorial-persona-admin
  Condition: user property "role" = "admin" OR user property "is_workspace_creator" = true

Flag: tutorial-persona-analyst
  Condition: user property "role" = "analyst" OR event "data_import_started" in last 7 days

Flag: tutorial-persona-end-user
  Condition: NOT (tutorial-persona-admin OR tutorial-persona-analyst)
```

Using `posthog-cohorts`, create stage detection cohorts:

- Stage 1: `signup_completed` AND NOT `setup_completed`
- Stage 2: `setup_completed` AND NOT `first_value_reached`
- Stage 3: `first_value_reached` AND `days_since_signup < 14`
- Stage 4: `first_value_reached` AND `days_since_signup >= 14`

### 3. Configure in-app video recommendations via Intercom

Using `intercom-in-app-messages`, create targeted messages for each persona-stage combination:

For each cell in the routing matrix:
1. Create an Intercom message with the video thumbnail (Loom GIF) and a 1-line description of what the user will learn
2. Set audience rules matching the persona flag AND stage cohort
3. Set display rules: show once per session, dismiss after click or explicit close
4. Link the CTA to the Loom video embed page or an in-app video player

Example message for Admin + Stage 1:
```
Title: "Set up your workspace in 2 minutes"
Body: [Loom GIF thumbnail]
CTA: "Watch tutorial" -> link to Loom video
Audience: tutorial-persona-admin AND stage-1 cohort
Frequency: Show once, do not re-show after dismissed
```

### 4. Build persona-specific email sequences via Loops

Using `loops-sequences`, create branched email sequences that include the right tutorials:

1. On signup, detect persona (from signup form role field or early behavior)
2. Branch the onboarding email sequence by persona
3. In each email, embed the Loom GIF thumbnail for the stage-appropriate tutorial
4. Link to the video with UTM parameters: `?utm_source=loops&utm_medium=email&utm_campaign=onboarding-{persona}`

Example for Admin persona:
- Email 1 (Day 0): Welcome + "Set up your workspace" tutorial video
- Email 2 (Day 1): "Invite your team" tutorial video (skip if team already invited)
- Email 3 (Day 3): "Configure permissions" tutorial video (skip if permissions set)

### 5. Build the recommendation engine in n8n

Using `n8n-scheduling`, create a daily workflow that identifies users who should see a new tutorial:

1. Query PostHog for users who completed a stage transition in the last 24 hours
2. For each user, look up their persona and new stage
3. Check which tutorials they have already watched (from person properties)
4. Select the next unwatched tutorial from the routing matrix
5. Trigger the appropriate Intercom message or Loops email

Using `n8n-workflow-basics`, add logic to:
- Never recommend a tutorial the user already completed
- Cap recommendations at 1 per day to avoid fatigue
- Escalate to human outreach if a user has been stuck at the same stage for 7+ days despite watching the relevant tutorials

### 6. Track personalization effectiveness

Using `posthog-custom-events`, add a `personalization_variant` property to all video events:

```javascript
posthog.capture('video_tutorial_impression', {
  // ... existing properties
  personalization_variant: 'persona-admin-stage-2',
  recommendation_source: 'intercom-in-app'  // or 'loops-email', 'n8n-recommendation'
});
```

Build a PostHog insight comparing:
- Personalized video recommendations vs. generic library browsing
- Activation rate by persona-stage combination
- Tutorial completion rate for recommended videos vs. self-discovered videos

## Output

- Tutorial routing matrix mapping personas to stage-appropriate videos
- PostHog feature flags for persona detection
- Intercom in-app messages for each persona-stage combination
- Loops email sequences branched by persona with embedded video tutorials
- n8n daily recommendation workflow
- Personalization effectiveness tracking in PostHog

## Triggers

The n8n recommendation engine runs daily. Intercom messages display in real-time based on audience rules. Loops emails trigger on signup and behavioral events. Review the routing matrix monthly and update when new tutorials are published or personas are refined.
