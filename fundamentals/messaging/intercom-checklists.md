---
name: intercom-checklists
description: Create and manage Intercom Checklists for guided in-app setup flows with auto-completion tracking
tool: Intercom
difficulty: Config
---

# Create Checklists in Intercom

## Prerequisites
- Intercom account with Messenger configured (Essential plan or higher)
- User properties and events flowing into Intercom (see `intercom-user-properties`)
- Product Tours add-on if linking checklist steps to tours

## Steps

1. **Understand checklist mechanics.** Intercom Checklists are persistent in-app task lists that appear inside the Messenger widget. Each checklist has 3-15 steps. Steps can auto-complete based on user data events, or require manual user clicks. Checklists persist across sessions and show progress (e.g., "3 of 6 complete"). They are ideal for multi-step setup wizards where users may complete steps across multiple sessions.

2. **Create a checklist via the Intercom API.** Use the Intercom REST API to create a new checklist programmatically. Intercom does not expose a public REST endpoint for checklist CRUD -- use the Intercom dashboard to create the checklist, then trigger it programmatically via the JavaScript API:
   ```javascript
   // Trigger a specific checklist by ID
   Intercom('startChecklist', CHECKLIST_ID);
   ```
   Alternatively, set audience rules in the Intercom dashboard to auto-show the checklist to users matching a segment (e.g., `signed_up_at` within last 7 days AND `setup_completed` is false).

3. **Define checklist steps.** Each step needs:
   - **Title**: Short action label (e.g., "Connect your data source")
   - **Description**: 1-2 sentences explaining what to do and why
   - **Action type**: One of:
     - **Link**: Opens a URL (use deep links into your app, e.g., `/settings/integrations`)
     - **Open article**: Opens an Intercom Help Center article
     - **Start tour**: Launches a Product Tour (see `intercom-product-tours`)
     - **No action**: Informational step, auto-completes on event
   - **Auto-completion rule**: Tie to a user event or data attribute. Example: step "Connect your data source" auto-completes when the Intercom user attribute `integration_connected` becomes `true`. Set this in the checklist step configuration under "Mark as complete when."

4. **Configure auto-completion via user data.** For each step that should auto-complete, ensure your app sends the corresponding event or updates the user attribute in Intercom. Use the Intercom JavaScript SDK:
   ```javascript
   // Update user attribute when they complete an action
   Intercom('update', {
     integration_connected: true,
     setup_step_3_completed_at: new Date().toISOString()
   });
   ```
   Or use the Intercom REST API from your backend:
   ```
   POST https://api.intercom.io/contacts/{id}
   Authorization: Bearer {token}
   Content-Type: application/json

   {
     "custom_attributes": {
       "integration_connected": true
     }
   }
   ```
   When the attribute matches the auto-completion rule, Intercom checks off that step in the user's checklist.

5. **Segment checklists by persona.** Create multiple checklists for different user types. Use Intercom's audience rules to show the right checklist based on user properties:
   - Rule: `persona_type` equals `technical_builder` -> show "Developer Setup" checklist
   - Rule: `persona_type` equals `team_lead` -> show "Team Setup" checklist
   - Rule: `persona_type` equals `solo_creator` -> show "Quick Start" checklist
   Each persona gets only the steps relevant to their setup path.

6. **Track checklist engagement.** Intercom fires events when users interact with checklists. Forward these to PostHog for funnel analysis:
   ```javascript
   // Listen for checklist events and forward to PostHog
   // Intercom does not expose granular checklist JS callbacks directly.
   // Instead, track step completions via the same user attribute updates
   // you use for auto-completion:
   posthog.capture('wizard_step_completed', {
     step_name: 'connect_data_source',
     step_number: 3,
     checklist_id: CHECKLIST_ID,
     persona_type: userPersona
   });
   ```

7. **Handle checklist completion.** When all steps are complete, trigger a celebration moment and next action:
   ```javascript
   // Check if all setup steps complete
   Intercom('update', {
     setup_wizard_completed: true,
     setup_wizard_completed_at: new Date().toISOString()
   });

   // Show a congratulations in-app message (configure in Intercom)
   // Trigger: setup_wizard_completed = true AND setup_wizard_celebrated != true
   ```
   Use `intercom-in-app-messages` to show a completion banner that suggests the next high-value action.

8. **Shareable checklist links.** Generate a shareable checklist link from the Intercom dashboard for use in onboarding emails. Include the link in Loops email sequences so users can access their checklist from email:
   ```
   https://app.intercom.com/checklist/{checklist_link_id}
   ```
   This opens the checklist in the Messenger widget on your site.

## Error Handling

- **Checklist not showing**: Verify the user matches the audience rules. Check that Intercom Messenger is loaded on the page. Confirm the user's `signed_up_at` and other filter attributes are set correctly.
- **Steps not auto-completing**: Verify the user attribute is updating in Intercom. Check the auto-completion rule matches the exact attribute name and expected value. Use Intercom's "Test as user" feature to debug.
- **Multiple checklists conflicting**: Intercom shows one checklist at a time. If a user matches multiple checklist audiences, Intercom shows the most recently created one. Use mutually exclusive audience rules to prevent overlap.

## Tool Alternatives

- **Appcues** (appcues.com): Checklist and onboarding flow builder with no-code editor. API for programmatic control. Starts at $249/mo.
- **UserGuiding** (userguiding.com): In-app checklists with auto-completion. Starts at $69/mo.
- **Userpilot** (userpilot.com): Checklist widget with analytics. Starts at $249/mo.
- **Chameleon** (chameleon.io): Launchers (checklist-like widgets) with deep targeting. Starts at $279/mo.
- **CommandBar** (commandbar.com): AI-powered checklists and nudges. Usage-based pricing.
