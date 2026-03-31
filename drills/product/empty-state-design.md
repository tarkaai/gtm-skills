---
name: empty-state-design
description: Audit product empty states, design contextual CTAs with sample data and templates, and implement tracking for each empty state surface
category: Product
tools:
  - PostHog
  - Intercom
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-funnels
  - posthog-session-recording
  - intercom-in-app-messages
  - intercom-product-tours
  - n8n-workflow-basics
---

# Empty State Design

This drill audits every empty state surface in a product, designs contextual CTAs that guide users to their first action, and instruments tracking on each surface. An empty state is any screen, panel, list, dashboard, or widget that displays no data because the user has not yet created or imported content. Empty states are high-leverage onboarding surfaces because they appear at the exact moment a user needs guidance.

## Input

- Access to the product codebase or staging environment
- PostHog installed with user identification
- A list of core features or objects in the product (projects, documents, contacts, workflows, etc.)
- The product's activation metric (the action that predicts retention)

## Steps

### 1. Audit all empty states

Systematically enumerate every screen where a user can encounter an empty state. For each feature or object type in the product, identify the list/dashboard/detail view that shows "no data" when the user has not created anything yet.

Categorize each empty state by priority:

| Priority | Criteria | Example |
|----------|----------|---------|
| P0 — Critical path | On the direct path to activation. User MUST pass through this empty state to reach the aha moment. | Dashboard with no projects, inbox with no messages |
| P1 — Common path | Most users encounter this within their first 3 sessions, but it is not strictly required for activation. | Settings page with no integrations, team page with no members |
| P2 — Discovery path | Users find this later as they explore. Not critical for initial activation. | Advanced analytics with no data, templates library when user has no custom templates |

Document each empty state: screen name, URL path or route, current behavior (blank page, generic message, or nothing), and priority level.

Use `posthog-session-recording` to watch 10-20 new user sessions. Note which empty states users encounter first, where they hesitate, and where they abandon. This reveals the real user flow versus the assumed flow.

### 2. Design the empty state experience for each P0 surface

For each P0 empty state, design an experience with these elements:

**Contextual headline:** Tell the user what this screen will contain once they take action. Not "No items yet" but "Your projects will appear here once you create one."

**Visual illustration or sample data:** Show what the screen will look like with real content. Options:
- **Sample data:** Pre-populate the screen with 2-3 example items the user can interact with (view, edit, delete). Mark them clearly as examples. Sample data lets users explore the product without committing to creating their own content first.
- **Screenshot or illustration:** Show a populated version of the screen as a static image. Lower engineering effort but less interactive.
- **Template gallery:** Offer 3-5 pre-built templates the user can start from. "Start from scratch" should also be an option but not the default.

**Single CTA button:** One clear action that creates the user's first real item. The button text should be specific: "Create your first project" not "Get started." The CTA must link directly to the creation flow, not to documentation.

**Supporting link:** A secondary link to a help article, video, or tutorial for users who want more context before acting. Keep this visually secondary to the CTA.

### 3. Implement tracking for each empty state surface

Using `posthog-custom-events`, fire the following events on each empty state:

| Event | Trigger | Properties |
|-------|---------|-----------|
| `empty_state_viewed` | Empty state screen loads for a user with zero items | `surface` (screen name), `priority` (P0/P1/P2), `user_signup_age_hours`, `variant` |
| `empty_state_cta_clicked` | User clicks the primary CTA | `surface`, `cta_text`, `variant` |
| `empty_state_template_selected` | User selects a template from the template gallery | `surface`, `template_name`, `variant` |
| `empty_state_sample_explored` | User interacts with sample data (clicks, expands, edits) | `surface`, `sample_item`, `action_type` |
| `empty_state_help_clicked` | User clicks the secondary help link | `surface`, `help_type` (article/video/tutorial) |
| `empty_state_dismissed` | User navigates away without taking any action | `surface`, `time_on_surface_seconds`, `variant` |
| `first_item_created` | User creates their first real item from the empty state flow | `surface`, `creation_method` (from_scratch/from_template/from_sample), `time_since_empty_state_view_seconds` |

### 4. Build the empty state funnel in PostHog

Using `posthog-funnels`, create a funnel per P0 surface:

`empty_state_viewed` -> `empty_state_cta_clicked` -> `first_item_created`

This gives you the core conversion metric: what percentage of users who see an empty state take the intended action. Break down by:
- `user_signup_age_hours` (do users who see it immediately convert better than those who find it later?)
- `variant` (for A/B testing different empty state designs)
- Device type (mobile vs desktop)

### 5. Build P1 empty states

Repeat the design process for P1 surfaces, but with lower investment. P1 empty states can use simpler treatments:
- Contextual headline + CTA button (no sample data or templates)
- Link to relevant help article
- A short sentence explaining why this feature matters

P2 surfaces get minimal treatment: a contextual headline and a CTA. No sample data, no templates.

### 6. Set up in-app guidance for stuck users

Using `intercom-in-app-messages`, create a targeted message that fires when a user has viewed a P0 empty state 2+ times without clicking the CTA. The message should:
- Acknowledge they have visited this area before
- Offer a quick-start option (template or guided walkthrough)
- Include a link to book a setup call if the product requires complex configuration

Using `intercom-product-tours`, create a 2-3 step micro-tour that activates from the empty state CTA for first-time users. The tour guides them through creating their first item step by step.

## Output

- Audit document listing all empty states with priority classification
- Designed empty state experiences for all P0 and P1 surfaces
- PostHog event tracking on every empty state surface
- Per-surface conversion funnels in PostHog
- Intercom messages for stuck users
- Baseline CTR data per surface after 1 week of observation

## Triggers

Run once during initial play setup. Re-run when new features ship that introduce new empty states, or when a P0 surface's CTR drops below threshold.
