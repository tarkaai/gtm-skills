---
name: segment-personalization-routing
description: Route personalized in-app experiences, emails, and feature flags to users based on their behavioral segment assignment
category: Product
tools:
  - PostHog
  - Intercom
  - Loops
  - n8n
fundamentals:
  - posthog-feature-flags
  - posthog-cohorts
  - posthog-custom-events
  - intercom-in-app-messages
  - intercom-product-tours
  - loops-sequences
  - n8n-workflow-basics
  - n8n-triggers
---

# Segment Personalization Routing

This drill takes the behavioral segment assignments from `behavior-segmentation-pipeline` and routes each segment to a tailored product experience. It configures PostHog feature flags per segment, sets up Intercom in-app messages and product tours per archetype, and triggers Loops email sequences tuned to each segment's usage patterns. The result is that two users with different behavior patterns see different onboarding tips, feature prompts, and re-engagement emails.

## Input

- Behavioral segment assignments stored as PostHog person properties (`behavior_segment_id`, `behavior_segment_label`)
- Dynamic PostHog cohorts per segment (from `behavior-segmentation-pipeline`)
- Cluster definitions with `personalization_strategy` per segment
- Intercom workspace with access to in-app messages and product tours
- Loops account with transactional and sequence email access
- n8n instance for orchestrating the routing logic

## Steps

### 1. Define the personalization matrix

For each behavioral segment, define what changes in the product experience. Start with 3 personalization surfaces:

| Surface | What changes per segment | Tool |
|---------|------------------------|------|
| In-app messaging | Message copy, timing, and CTA | Intercom |
| Feature discovery | Which features to highlight, tour content | Intercom product tours |
| Email sequences | Email cadence, content focus, and CTAs | Loops |

Example matrix for a typical 5-segment model:

| Segment | In-app message | Feature highlight | Email focus |
|---------|---------------|-------------------|-------------|
| Power Collaborator | "Invite more teammates" | Advanced sharing, permissions | Team expansion tips |
| Focused Specialist | "Discover related features" | Adjacent features to their primary | Depth-building tutorials |
| Casual Browser | "Get started with [core feature]" | Core value feature | Activation nudges |
| Team Driver | "See your team's activity" | Analytics dashboard, reports | Team productivity digest |
| New Explorer | "Complete your setup" | Onboarding checklist | Getting-started series |

**Human action required:** Review and customize this matrix for your product. The behavioral segments and their personalization strategies come from the cluster definitions. Translate each strategy into specific messages, features, and email content.

### 2. Configure PostHog feature flags per segment

Using the `posthog-feature-flags` fundamental, create feature flags that gate personalized experiences:

For each segment, create a flag:
- Flag key: `segment-experience-{segment_id}` (e.g., `segment-experience-power-collaborator`)
- Match condition: person property `behavior_segment_id` equals `{segment_id}`
- Payload: JSON with the personalization config for that segment

```json
{
  "in_app_message_id": "msg_team_invite_prompt",
  "feature_highlight": "advanced_sharing",
  "email_sequence_id": "seq_team_expansion",
  "cta_text": "Invite your team",
  "cta_link": "/settings/team"
}
```

The product code reads this flag payload to render the right experience. If no flag matches (unclassified users), fall back to a generic default experience.

### 3. Build Intercom in-app messages per segment

Using the `intercom-in-app-messages` fundamental, create targeted messages for each segment. Each message targets the corresponding PostHog cohort (synced to Intercom via user properties or n8n integration).

**Message design rules for agents:**
- Subject line: 8 words or fewer. Reference the user's actual behavior pattern.
- Body: 2 sentences maximum. One value statement, one CTA.
- CTA: Single button. Deep link to the relevant product area.
- Display rule: Show once per user. Re-show only if segment assignment changes.
- Timing: Display 10 seconds after page load (not immediately -- avoid interrupting the user's task).

For "Focused Specialist" segment example:
- Subject: "You use {primary_feature} a lot"
- Body: "Users like you also get value from {adjacent_feature}. It works great alongside {primary_feature}."
- CTA: "Try {adjacent_feature}" -> deep link to that feature

### 4. Build Intercom product tours per segment

Using the `intercom-product-tours` fundamental, create segment-specific tours that highlight the features most relevant to each archetype:

- **Power Collaborator:** Tour of advanced team features (permissions, shared views, activity feed)
- **Focused Specialist:** Tour of power-user features adjacent to their primary workflow
- **Casual Browser:** Tour of the core value proposition (the one feature that drives retention)
- **Team Driver:** Tour of team analytics and management features
- **New Explorer:** Full onboarding tour with checklist

Trigger each tour based on the PostHog cohort membership. Set each tour to display once.

### 5. Configure Loops email sequences per segment

Using the `loops-sequences` fundamental, create a segment-specific email sequence for each cluster. Each sequence runs for 14 days after segment assignment (or re-assignment).

**Sequence structure (per segment, 4 emails over 14 days):**

- **Day 0:** Welcome to segment. "Based on how you use {product}, here's what we recommend next." Include the single highest-impact action for their segment.
- **Day 3:** Feature deep-dive. Tutorial or guide for the feature most relevant to their behavior pattern.
- **Day 7:** Social proof. "Other {segment_label} users achieved {outcome} by doing {action}." Include a specific metric or case study.
- **Day 14:** Progress check. "Here's what you've accomplished this month" with a usage summary and next step.

**Personalization tokens:** Use Loops contact properties synced from PostHog: `behavior_segment_label`, `primary_feature`, `engagement_score`, `days_since_signup`.

### 6. Build the routing orchestration in n8n

Using `n8n-workflow-basics` and `n8n-triggers`, create a workflow that fires when a user's segment assignment changes:

1. **Trigger:** Webhook from the `behavior-segmentation-pipeline` when `behavior_segment_changed` event fires
2. **Fetch context:** Pull the user's new segment, previous segment, and cluster personalization config
3. **Update Intercom:** Set user properties in Intercom to trigger the correct in-app messages and tours
4. **Enroll in Loops sequence:** Add the user to the new segment's email sequence. Remove from previous segment's sequence if applicable.
5. **Log:** Fire `personalization_routed` event in PostHog with: `user_id`, `new_segment`, `previous_segment`, `surfaces_updated` (array of what changed)

### 7. Track personalization effectiveness

Using `posthog-custom-events`, instrument every personalized touchpoint:

- `segment_message_shown`: when an in-app message renders for a segmented user
- `segment_message_clicked`: when user clicks the CTA
- `segment_tour_started`: when a segment-specific tour begins
- `segment_tour_completed`: when user finishes the tour
- `segment_email_opened`: when a segment-specific email is opened
- `segment_email_clicked`: when user clicks through from a segment email

For each event, include properties: `segment_id`, `segment_label`, `surface` (in_app | tour | email), `content_id`.

Measure per segment:
- **Engagement rate:** % of users who interacted with at least one personalized touchpoint
- **Conversion rate:** % of users who completed the recommended action (the CTA target)
- **Retention lift:** Compare 30-day retention of segmented users vs. a control cohort receiving generic experiences

## Output

- PostHog feature flags routing segment-specific experiences
- Intercom in-app messages and product tours per segment
- Loops email sequences per segment
- n8n orchestration workflow for segment change routing
- Effectiveness tracking events in PostHog

## Triggers

- **On segment assignment/change:** n8n webhook processes immediately
- **Message/tour refresh:** Monthly review of personalization content performance. Retire low-performing messages, test new variants.
