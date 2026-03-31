---
name: onboarding-personalization
description: Route new users into persona-specific onboarding tours based on role, use case, and signup context to maximize activation
category: Product
tools:
  - Intercom
  - PostHog
  - n8n
fundamentals:
  - intercom-product-tours
  - intercom-user-properties
  - posthog-cohorts
  - posthog-feature-flags
  - posthog-custom-events
  - n8n-triggers
  - n8n-workflow-basics
---

# Onboarding Personalization

This drill routes new users into persona-specific onboarding tours based on their role, use case, company size, and signup context. Instead of one generic tour for all users, each persona gets a tour optimized for their fastest path to activation.

## Prerequisites

- Intercom installed with Product Tours enabled
- PostHog tracking user properties and events
- At least 2 distinct user personas identified (e.g., "admin vs end-user", "marketer vs developer", "solo vs team lead")
- A working generic onboarding tour (from the `onboarding-flow` drill) to use as the baseline

## Steps

### 1. Define persona segments

Using the `posthog-cohorts` fundamental, analyze your existing activated users. Group them by the properties available at signup or within the first session:

- **Role**: What is their job function? Collect via signup form or Intercom user properties.
- **Use case**: What are they trying to accomplish? Collect via a single-question in-app survey on first login.
- **Company size**: Solo user, small team (2-10), or larger organization (10+)?
- **Signup source**: Referral, organic search, paid ad, product hunt, etc.

Define 2-4 persona segments. More than 4 creates maintenance burden without proportional activation lift. Example segments for a project management tool:

- **Persona A — Solo creator**: Individual user, creative role, found via content
- **Persona B — Team lead**: Manager role, 3+ team invites expected, found via search
- **Persona C — Technical builder**: Developer role, API/integration interest, found via GitHub or docs

### 2. Map activation paths per persona

For each persona, identify the fastest path to their specific "aha moment." The activation metric may differ by persona:

- **Solo creator**: Creates first project and adds 3+ items (value = personal organization)
- **Team lead**: Creates project and invites 1+ teammates (value = team coordination)
- **Technical builder**: Connects an integration or makes first API call (value = automation)

Using `posthog-custom-events`, define persona-specific activation events:
- `activation_reached` with property `persona_type: "solo_creator"` (or "team_lead", "technical_builder")

### 3. Build persona-specific tours

Using the `intercom-product-tours` fundamental, create one tour per persona. Each tour is 3-5 steps and focuses only on reaching that persona's activation metric.

**Tour A — Solo Creator (3 steps):**
1. "Create your first project" — spotlight the New Project button, make step interactive
2. "Add your first items" — show how to add tasks/content, interactive step
3. "See your dashboard" — show the overview with their new content populated

**Tour B — Team Lead (4 steps):**
1. "Create a team project" — spotlight New Project with team template
2. "Invite your team" — spotlight the Invite button, interactive step
3. "Assign your first task" — show task assignment, interactive step
4. "Check team activity" — show the activity feed with team updates

**Tour C — Technical Builder (3 steps):**
1. "Connect your first integration" — spotlight the Integrations page
2. "See your data flow in" — show the data arriving from the integration
3. "Explore the API" — link to API docs with a pre-generated API key

### 4. Set up persona detection and routing

Using the `intercom-user-properties` fundamental, ensure the following properties are synced to Intercom at signup:
- `persona_type` (from signup survey or classification logic)
- `company_size`
- `signup_source`
- `role`

Using `posthog-feature-flags`, create a feature flag `onboarding-tour-persona` with variants matching your personas: `solo_creator`, `team_lead`, `technical_builder`. Set the flag to route users based on their `persona_type` property.

If persona detection is not available at signup (no survey), build a classification workflow using `n8n-triggers`: when `signup_completed` fires, the n8n workflow enriches the user (from signup data, email domain, referral source) and assigns a `persona_type` property to both PostHog and Intercom.

### 5. Configure tour triggers in Intercom

Set each tour to trigger only for its matching persona:
- Tour A: triggers when `persona_type = solo_creator` AND `onboarding_complete = false`
- Tour B: triggers when `persona_type = team_lead` AND `onboarding_complete = false`
- Tour C: triggers when `persona_type = technical_builder` AND `onboarding_complete = false`

Fallback: users without a detected persona get the generic tour from the `onboarding-flow` drill.

### 6. Instrument and measure per-persona performance

Using `posthog-custom-events`, track tour events with persona context:
- `tour_started` with `{persona_type, tour_variant}`
- `tour_step_completed` with `{persona_type, step_number, step_name}`
- `tour_completed` with `{persona_type, duration_seconds}`
- `tour_dismissed` with `{persona_type, step_number}`

Using `posthog-cohorts`, build per-persona activation funnels:
- `tour_started (persona=X)` → `tour_completed (persona=X)` → `activation_reached (persona=X)`

Compare activation rates across personas. If one persona activates at 60% and another at 30%, the 30% persona's tour needs iteration. The goal is to bring all personas within 10 percentage points of each other.

## Output

- 2-4 persona-specific product tours in Intercom
- Feature flag routing users to the correct tour
- Per-persona activation funnels in PostHog
- Baseline activation rates per persona for optimization
