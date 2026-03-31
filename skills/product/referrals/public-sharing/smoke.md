---
name: public-sharing-smoke
description: >
  Branded Public Sharing — Smoke Test. Build a minimum viable public share page
  with branded CTA, instrument the share-to-signup funnel, and validate that
  users will share their work publicly and that viewers convert.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product, Social"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=25% of test users share publicly AND >=1 viewer signup"
kpis: ["Public share rate", "Share page views per share", "CTA click-through rate", "Viewer signup count"]
slug: "public-sharing"
install: "npx gtm-skills add product/referrals/public-sharing"
drills:
  - lead-capture-surface-setup
  - posthog-gtm-events
  - threshold-engine
---

# Branded Public Sharing — Smoke Test

> **Stage:** Product > Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product, Social

## Outcomes

At least 25% of a 10-20 user test group click "share publicly" and complete the share flow. At least 1 viewer who lands on a shared page clicks the branded CTA and signs up. This proves the mechanic works: users will share, viewers will see the brand, and some will convert.

## Leading Indicators

- Users find and click the "share publicly" button without prompting (share initiation events in PostHog)
- Share completion rate above 60% (users who start the share flow finish it)
- Share pages receive at least 3 views each within 7 days (shared links are actually being distributed)
- CTA impressions fire on share pages (the branded element renders correctly)

## Instructions

### 1. Instrument the share funnel

Run the `posthog-gtm-events` drill to define and implement these events:

| Event | Trigger | Properties |
|-------|---------|------------|
| `share_initiated` | User clicks "share publicly" button | `user_id`, `content_type`, `content_id` |
| `share_published` | Share page goes live (URL generated) | `user_id`, `content_type`, `share_url`, `share_id` |
| `share_page_viewed` | Viewer loads a shared page | `share_id`, `referrer`, `device_type`, `utm_source` |
| `share_cta_impression` | Branded CTA enters viewport on share page | `share_id`, `cta_variant` |
| `share_cta_clicked` | Viewer clicks the branded "Made with [Product]" CTA | `share_id`, `cta_variant` |
| `share_signup_completed` | Viewer completes signup from share page | `share_id`, `referrer_user_id`, `signup_method` |

Build a PostHog funnel: `share_initiated` -> `share_published` -> `share_page_viewed` -> `share_cta_clicked` -> `share_signup_completed`.

### 2. Build the branded share page

Run the `lead-capture-surface-setup` drill to build the public share page. The share page is the lead capture surface — it displays the user's content with a branded CTA that converts viewers to signups.

Configure the share page with:
- User's content rendered as the primary element (full-width, no login required to view)
- Branded header or footer: "[Product] — [tagline]" with a CTA button: "Create yours free" or "Try [Product] free"
- The CTA links to the signup page with UTM parameters: `?utm_source=public-share&utm_medium=product&utm_content={share_id}&ref={referrer_user_id}`
- Open Graph meta tags so the shared link previews well on social platforms (title = user's content title, image = content preview, description = "Made with [Product]")
- Mobile-responsive layout — most social traffic is mobile

**Human action required:** Review the share page design. Verify the branded CTA is visible without scrolling on mobile. Verify OG tags render correctly when the link is pasted into Slack, LinkedIn, and Twitter. Ship the share page to production behind a PostHog feature flag.

### 3. Enable the feature flag for test users

Using PostHog feature flags, enable public sharing for 10-20 active users. Select users who:
- Have been active for at least 14 days (established usage patterns)
- Have created content that is shareable (not empty or trivial)
- Represent different usage patterns (power users and moderate users)

Do not prompt users to share. Let them discover the feature organically for the first 3 days. On day 4, send a single Intercom in-app message: "New: share your [content type] publicly with a link." Track `share_prompt_shown` and `share_prompt_clicked` to measure whether the prompt drives sharing above organic discovery.

### 4. Evaluate against threshold

Run the `threshold-engine` drill after 7 days. Evaluate:

- **Primary threshold:** >=25% of test users published at least one public share
- **Secondary threshold:** >=1 viewer signed up via a share page CTA
- **Guardrail:** No user complaints about content being shared without consent (sharing must be opt-in only)

If PASS: Document which content types were shared most, which share pages got the most views, and where viewers came from (referrer data). Proceed to Baseline.

If FAIL: Diagnose using PostHog funnels. If share initiation is low, the button is not discoverable — test placement. If completion is low, the share flow is too complex — simplify. If views are low, users are not distributing links — test adding share-to-social buttons. If CTA clicks are low, the branded element is not compelling — test copy and placement.

## Time Estimate

- 1 hour: PostHog event instrumentation
- 2 hours: share page build + branded CTA setup
- 30 minutes: feature flag configuration and test user selection
- 30 minutes: Intercom prompt setup
- 1 hour: 7-day evaluation and analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, feature flags | Free tier: 1M events/mo — https://posthog.com/pricing |
| Intercom | In-app share prompt | Included in standard stack |
| n8n | Webhook for signup routing | Included in standard stack |

**Play-specific cost:** Free

## Drills Referenced

- `lead-capture-surface-setup` — builds the branded public share page as a lead capture surface with CTA tracking and signup routing
- `posthog-gtm-events` — defines and implements the share funnel event taxonomy in PostHog
- `threshold-engine` — evaluates share rate and conversion against pass/fail criteria after 7 days
