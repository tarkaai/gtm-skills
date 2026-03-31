---
name: wizard-step-builder
description: Build a multi-step setup wizard with validation, conditional branching, and progress persistence using Intercom Checklists and PostHog tracking
category: Onboarding
tools:
  - Intercom
  - PostHog
  - n8n
fundamentals:
  - intercom-checklists
  - intercom-product-tours
  - intercom-in-app-messages
  - posthog-custom-events
  - posthog-feature-flags
  - n8n-triggers
  - n8n-workflow-basics
---

# Wizard Step Builder

This drill builds an interactive setup wizard that guides users through initial product configuration. The wizard uses Intercom Checklists as the persistent progress tracker, Intercom Product Tours for step-level guidance, and PostHog for granular event tracking. The wizard validates each step before allowing progression and supports conditional branching based on user type.

## Input

- A list of 4-8 configuration steps required for your product's initial setup (e.g., connect data source, invite team, configure workspace, set preferences)
- Persona definitions from the `icp-definition` drill (which users need which steps)
- PostHog tracking installed with user identification
- Intercom Messenger installed in your app

## Steps

### 1. Define the wizard step map

Map every configuration action a new user must complete, ordered by dependency and value:

| Step | Action | Validation | Why It Matters |
|------|--------|------------|----------------|
| 1 | Complete profile (name, role, company) | All fields non-empty | Enables persona classification |
| 2 | Choose use case / goal | Selection made | Routes to the right wizard variant |
| 3 | Connect primary data source | API connection verified | Unlocks core product value |
| 4 | Configure workspace settings | Settings saved | Personalizes the experience |
| 5 | Create first core object | Object exists in database | First value moment |
| 6 | Invite team member (if applicable) | Invite sent OR skipped | Drives collaboration and stickiness |

Rules for step design:
- Each step must be completable in under 3 minutes
- Each step must have a binary validation (done or not done)
- Steps with dependencies must enforce ordering (cannot do step 3 before step 2)
- Optional steps must be explicitly skippable (not silently ignored)

### 2. Build persona-specific wizard variants

Not every user needs every step. Using the `posthog-feature-flags` fundamental, create a multi-variant feature flag `setup-wizard-variant` that controls which steps appear:

- `technical_builder`: Steps 1, 3 (API setup), 5 (code-first object creation) -- skip step 6 initially
- `team_lead`: Steps 1, 2, 4 (permissions, roles), 6 (invite team) -- step 3 delegated to technical team member
- `solo_creator`: Steps 1, 2, 5 (template-based creation) -- skip steps 3, 4, 6

Assign the flag based on `persona_type` property set during signup classification (see `onboarding-persona-scaling` drill for classification logic).

### 3. Build the Intercom Checklist

Using the `intercom-checklists` fundamental, create one checklist per persona variant:

For each step in the variant:
- **Title**: Action verb + object (e.g., "Connect your data source")
- **Description**: One sentence explaining the benefit, not the mechanics (e.g., "Your data powers everything -- connect it now to see real results in minutes")
- **Action**: Deep link into the app's setup page for that step (e.g., `/setup/integrations`)
- **Auto-completion**: Tied to the Intercom user attribute that the app sets when the step is done

Set the audience rule: show checklist when `signup_completed` is true AND `setup_wizard_completed` is false AND `persona_type` matches the variant.

### 4. Build step-level Product Tours

Using the `intercom-product-tours` fundamental, create a short tour (2-4 stops) for each wizard step that involves complex UI interaction:

- **Step 3 (Connect data source)**: Tour highlights the integration settings page, the "Add connection" button, and the API key field. Final stop shows the success state.
- **Step 5 (Create first object)**: Tour highlights the "New" button, walks through the creation form, and celebrates the result.

Trigger each tour from the checklist step's action (the "Start tour" action type in Intercom Checklists). Tours only fire once per user per step -- if the user dismisses the tour, the step remains on the checklist but the tour does not replay.

### 5. Implement validation and progress tracking

For each wizard step, instrument your app to:

1. **Track the attempt**: Fire a PostHog event when the user starts the step:
   ```javascript
   posthog.capture('wizard_step_started', {
     step_name: 'connect_data_source',
     step_number: 3,
     persona_type: user.persona_type,
     wizard_variant: user.wizard_variant
   });
   ```

2. **Validate completion**: After the user takes the action, verify it succeeded (API connection returns 200, object exists in DB, etc.)

3. **Track completion**: Fire PostHog event and update Intercom:
   ```javascript
   posthog.capture('wizard_step_completed', {
     step_name: 'connect_data_source',
     step_number: 3,
     time_on_step_seconds: elapsed,
     persona_type: user.persona_type,
     wizard_variant: user.wizard_variant
   });

   Intercom('update', {
     setup_step_3_completed: true,
     setup_step_3_completed_at: new Date().toISOString()
   });
   ```

4. **Handle failure**: If validation fails (bad API key, missing field), show an inline error and fire:
   ```javascript
   posthog.capture('wizard_step_failed', {
     step_name: 'connect_data_source',
     step_number: 3,
     error_type: 'invalid_api_key',
     persona_type: user.persona_type
   });
   ```

### 6. Build stall detection and nudges

Using `n8n-triggers` and `n8n-workflow-basics`, create a workflow that runs every 6 hours:

1. Query PostHog for users who started a wizard step more than 4 hours ago but have not completed it
2. For each stalled user, determine the stall step and persona
3. Trigger a contextual Intercom in-app message (using `intercom-in-app-messages`):
   - If stalled at data connection: "Need help connecting? Here's a 60-second guide" with link to help article
   - If stalled at team invite: "You can skip this for now and invite teammates later" with skip action
   - If stalled at first object: "Try one of our templates to get started in seconds" with link to template picker
4. If stalled for 24+ hours, trigger a Loops email with a setup guide and calendar booking link for help

### 7. Handle wizard completion

When the user completes all steps in their variant:

1. Fire the completion event:
   ```javascript
   posthog.capture('wizard_completed', {
     persona_type: user.persona_type,
     wizard_variant: user.wizard_variant,
     total_time_minutes: totalMinutes,
     steps_completed: completedCount,
     steps_skipped: skippedCount
   });

   Intercom('update', {
     setup_wizard_completed: true,
     setup_wizard_completed_at: new Date().toISOString(),
     setup_wizard_time_minutes: totalMinutes
   });
   ```

2. Show a celebration in-app message (via `intercom-in-app-messages`) that congratulates the user and suggests their first high-value action based on their persona
3. Remove the checklist from the Messenger widget (auto-hides when all steps complete)
4. Transition the user to the standard product experience

## Output

- One setup wizard per persona variant, delivered via Intercom Checklists
- Step-level Product Tours for complex configuration steps
- Full PostHog event tracking: `wizard_step_started`, `wizard_step_completed`, `wizard_step_failed`, `wizard_completed`
- Stall detection with automated nudges via n8n
- Validation at each step ensuring configuration success

## Triggers

Run once during initial play setup. Re-run when adding new personas, adding new setup steps, or redesigning the wizard flow.
