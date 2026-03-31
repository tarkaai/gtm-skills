---
name: social-share-surface-build
description: Design and deploy in-product share buttons, shareable URLs, OG preview cards, and share tracking for viral growth
category: Product
tools:
  - PostHog
  - Intercom
  - n8n
  - Attio
fundamentals:
  - share-widget-embed
  - share-link-generation
  - og-meta-generation
  - posthog-custom-events
  - intercom-in-app-messages
---

# Social Share Surface Build

This drill builds the complete in-product sharing infrastructure: the share button component, the share link generation system, the OG preview card generator, and the event tracking layer. The output is a working share surface attached to one shareable resource type that users can use to share product content to social channels.

## Prerequisites

- Product with at least one shareable resource type (dashboards, reports, achievements, projects, results)
- PostHog installed in the product
- A deployment pipeline for the OG image endpoint

## Steps

### 1. Identify shareable resource types

Audit your product for content users would want to share. Rank by shareability:

| Resource Type | Share Motivation | Viral Potential |
|---------------|-----------------|-----------------|
| Achievements/milestones | Pride, social proof | High — triggers curiosity ("how did they do that?") |
| Results/outputs | Demonstrate value | High — shows the product working |
| Dashboards/reports | Professional sharing | Medium — useful to peers in same role |
| Projects/workspaces | Collaboration invite | Medium — invites new users directly |
| Templates/configurations | Helpfulness | Medium — provides immediate value to recipient |

Pick the highest-ranked resource type for the initial build. Do not build share surfaces for more than one resource type at Smoke level.

### 2. Build the share link system

Use `share-link-generation` to deploy the share URL infrastructure:

1. Create the `share_links` and `share_clicks` database tables
2. Deploy the `POST /api/share` endpoint that generates tracked short URLs
3. Deploy the `GET /s/{code}` redirect handler with click tracking and attribution cookies
4. Wire signup attribution: when a new user signs up with a `ref` cookie, credit the sharer

Test the full chain: generate a link, click it, verify the click is recorded, sign up via the link, verify the conversion is attributed.

### 3. Build the OG preview card generator

Use `og-meta-generation` to deploy dynamic social preview cards:

1. Deploy the `GET /api/og` endpoint with a branded template
2. Include dynamic data: resource title, key metric (if applicable), sharer name
3. Set meta tags on the shared resource page: `og:title`, `og:description`, `og:image`, `twitter:card`
4. Test with LinkedIn Post Inspector and Twitter Card Validator to confirm rich previews render

### 4. Build the share widget

Use `share-widget-embed` to build the in-product share UI:

1. Create the share button component and place it on the chosen resource type
2. Build the share popover with channel options: Copy Link, Twitter/X, LinkedIn, Email
3. Wire each channel action to the correct share URL format
4. Implement the native Web Share API fallback for mobile users

### 5. Instrument share tracking

Use `posthog-custom-events` to track the complete share funnel:

- `share_widget_opened` — user clicked the share button
- `share_channel_selected` — user chose a channel
- `share_action_completed` — share was executed (link copied, tweet window opened)
- `share_link_clicked` — someone clicked a shared link (fired by redirect handler)
- `share_referral_signup` — a clicked share link led to a signup
- `share_referral_activated` — a referred signup completed activation

Build a PostHog funnel: widget opened -> channel selected -> action completed -> link clicked -> signup -> activated.

### 6. Add contextual share prompts

Use `intercom-in-app-messages` to prompt sharing at high-intent moments:

- After a user completes a milestone (first project, 100th action, etc.): "You just hit [milestone]. Share your achievement?"
- After a user views their results/dashboard: "These results look great. Share them with your team?"
- After a positive interaction (NPS 9-10, support resolution): "Glad we could help. Know someone who'd benefit from [Product]?"

Each prompt includes a one-click share button that opens the share widget pre-configured for that resource.

## Output

- Share button component deployed on one resource type
- Share link generation system with attribution tracking
- Dynamic OG preview cards rendering on social platforms
- PostHog funnel tracking the complete share journey
- Contextual share prompts at 2-3 high-intent moments

## Triggers

Run once during initial setup. Re-run for each additional resource type added to the share system (Scalable level).
