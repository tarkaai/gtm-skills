---
name: social-sharing-features-baseline
description: >
  Built-In Social Sharing — Baseline Run. Run share features always-on for all
  users, deploy auto-generated share content, instrument the full viral funnel,
  and measure the baseline K-factor over 4 weeks.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Social"
level: "Baseline Run"
time: "20 hours over 4 weeks"
outcome: ">=10% share initiation rate across all users AND K-factor >=0.05 (measurable viral loop) over 4 weeks"
kpis: ["Share initiation rate (all users)", "Share completion rate", "Share link CTR by channel", "Viral signup rate", "K-factor (4-week rolling)", "Sharer repeat rate (shared 2+ times in 30 days)"]
slug: "social-sharing-features"
install: "npx gtm-skills add product/referrals/social-sharing-features"
drills:
  - posthog-gtm-events
  - feature-announcement
---

# Built-In Social Sharing — Baseline Run

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Social

## Outcomes

The share features run always-on for all users. Auto-generated share content (channel-specific text and dynamic OG images) makes sharing frictionless. The full viral funnel — share initiated, share completed, link clicked, signup, activation — is instrumented and measured. After 4 weeks, the share initiation rate across all active users is at least 10%, and the K-factor (shares per user * conversion per share) is at least 0.05, proving a measurable viral loop exists.

## Leading Indicators

- Feature announcement reaches >80% of active users (Intercom delivery + Loops open rates)
- Share button impression rate is >60% of DAU (the button is visible to most users)
- Auto-generated share content has higher CTR than static templates (content generator adds value)
- At least 3 social channels show organic clicks (the share mechanism works across platforms)
- Repeat sharers emerge: >10% of first-time sharers share again within 2 weeks
- At least 5 viral signups occur in the first 4 weeks (the loop closes)

## Instructions

### 1. Instrument the full viral funnel

Run the `posthog-gtm-events` drill to set up comprehensive tracking for the sharing viral loop:

Implement these events:

| Event | Trigger | Key Properties |
|-------|---------|---------------|
| `share_surface_impression` | Share button enters user viewport | `resource_type`, `surface_location`, `user_tenure_days` |
| `share_widget_opened` | User clicks share button | `resource_type`, `resource_id`, `surface_location` |
| `share_channel_selected` | User selects a share channel | `channel`, `resource_type` |
| `share_action_completed` | Share executed (link copied, tweet opened, etc.) | `channel`, `resource_type`, `content_variant`, `share_text_length` |
| `share_link_clicked` | External visitor clicks a shared link | `sharer_user_id`, `resource_type`, `channel`, `referrer_domain` |
| `share_referral_signup` | Visitor from a share link creates an account | `sharer_user_id`, `channel`, `resource_type`, `time_to_signup_hours` |
| `share_referral_activated` | Referred user completes activation milestone | `sharer_user_id`, `channel`, `days_to_activation` |

Build these PostHog funnels:
- **Share funnel**: impression -> widget opened -> channel selected -> action completed
- **Viral funnel**: action completed -> link clicked -> signup -> activated
- **End-to-end**: impression -> share completed -> link clicked -> signup -> activated

Build a PostHog dashboard: "Social Sharing — Baseline" with panels for share volume by day, funnel conversion rates, channel distribution, K-factor trend, and top shared resources.

### 2. Launch the share feature to all users

Run the `feature-announcement` drill to announce built-in sharing to the full user base:

**Tier 1 announcement (this is a major feature):**

- In-app message (Intercom): targeted to all active users. Banner at the top of the resource page: "New: Share your [resource type] with your network. Click the share button to get started." Include a 3-second GIF showing the share flow. Dismiss after 7 days.
- Email (Loops broadcast): to all active users. Subject: "Share your work — new share features in [Product]". Show the OG preview card as an example of what their shared content will look like. Direct CTA: "Open [Product] and try sharing."
- Changelog entry: "Built-in social sharing: share dashboards, results, and achievements directly to Twitter, LinkedIn, email, and more."

Deploy the share button to ALL users (remove the test-group restriction from Smoke). Ensure the contextual share prompts are active for all users at the 2-3 high-intent moments identified in Smoke.

### 3. Deploy auto-generated share content

Run the the share content generator workflow (see instructions below) drill to improve share quality:

- Configure the content generation pipeline: when a user opens the share widget, auto-generate channel-specific share text based on their resource data
- Deploy dynamic OG images for every shareable resource (not just the single type from Smoke — extend to all resource types that have share buttons)
- Set up the Anthropic API integration for complex share text (LinkedIn posts that sound natural, not templated)
- Implement content variant tracking: tag each share with the content variant used, track CTR per variant

Monitor content generation latency: the share popover must load in <2 seconds. If content generation is slow, pre-generate content when the user views the resource (before they click share).

### 4. Monitor for 4 weeks without intervention

Let the sharing system run for 4 full weeks. Monitor the PostHog dashboard daily:

- Is share volume trending up, flat, or declining week over week?
- Which channels produce the highest CTR? (This informs Scalable-level channel optimization)
- Which resource types are shared most often?
- Are shared links converting to signups? At what rate?
- Is the K-factor stable or fluctuating?
- Are repeat sharers emerging?

Do not adjust the share prompts, content templates, or UI during the 4-week baseline period. Collect clean data.

### 5. Evaluate against threshold

After 4 weeks, compute:

- **Share initiation rate**: share_widget_opened / unique active users who saw a share button over 4 weeks. Target: >=10%.
- **K-factor**: (average shares per active user per month) * (signups per share). Target: >=0.05.

If PASS: the viral loop exists and is measurable. The share features add net-new user acquisition. Proceed to Scalable.
If FAIL on initiation rate (K-factor not measurable): users are not sharing. Diagnose: is the share button visible (check impression rate)? Is the prompt timing wrong? Is the content not share-worthy? Test 2-3 changes to the prompt or button placement. Re-run for 2 more weeks.
If FAIL on K-factor only (people share but nobody clicks/signs up): the share content quality or OG preview cards need work. Or the shared resource landing page is not converting visitors. Diagnose the viral funnel and fix the biggest drop-off. Re-run.

## Time Estimate

- 4 hours: PostHog event instrumentation, funnels, and dashboard
- 3 hours: feature announcement (Intercom message, Loops email, changelog)
- 5 hours: share content generator setup and testing
- 4 hours: extend share surfaces to additional resource types
- 4 hours: 4-week monitoring and evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Full funnel tracking, funnels, dashboards, cohorts | Usage-based: ~$0.00005/event beyond 1M free/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Feature announcement in-app messages, share prompts | Essential: $29/seat/mo ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Feature announcement email, sharer notification emails | Starter: $49/mo up to 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| Anthropic API | Share text generation for LinkedIn and complex channels | Claude API: ~$15/MTok input, ~$75/MTok output; estimated $10-30/mo for share text generation ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| Vercel | OG image generation at scale | Pro: $20/mo for higher Edge Function limits ([vercel.com/pricing](https://vercel.com/pricing)) |
| Attio | Sharer tracking, share link performance records | Free tier: 3 seats ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated play-specific cost at this level:** $80-150/mo (Intercom + Loops + Anthropic API for share content)

## Drills Referenced

- `posthog-gtm-events` — instruments the complete viral funnel from share impression through referred-user activation
- `feature-announcement` — coordinates the multi-channel launch of sharing features to all users
- the share content generator workflow (see instructions below) — auto-generates channel-specific share text and dynamic OG images
