---
name: social-sharing-features-smoke
description: >
  Built-In Social Sharing — Smoke Test. Build a share button on one shareable
  resource type, deploy tracked share links with OG preview cards, and validate
  that at least 20% of prompted users initiate a share action and at least one
  shared link generates a click-through.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Social"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: ">=20% share initiation rate among prompted users AND >=1 share link click-through from external traffic"
kpis: ["Share initiation rate (share_widget_opened / prompted users)", "Share completion rate (share_action_completed / share_widget_opened)", "Share link CTR (share_link_clicked / share_action_completed)", "Channels used distribution"]
slug: "social-sharing-features"
install: "npx gtm-skills add product/referrals/social-sharing-features"
drills:
  - threshold-engine
---

# Built-In Social Sharing — Smoke Test

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Social

## Outcomes

Deploy a working share button on one shareable resource type (achievements, dashboards, or results), generate tracked share links with branded OG preview cards, and validate that users actually share. At least 20% of users who are prompted to share open the share widget, and at least one shared link generates a click from an external visitor. This proves that your product has content worth sharing and that users will share it when given a frictionless mechanism.

## Leading Indicators

- Share button renders correctly on the target resource type (visual check on 3 browsers)
- OG preview cards display correctly on LinkedIn Post Inspector and Twitter Card Validator
- At least 50% of test users see the share button (impression tracking confirms visibility)
- At least 3 different channels are used (copy link, Twitter, LinkedIn, email — signals the widget works across channels)
- At least one shared link receives a click within 48 hours of sharing

## Instructions

### 1. Build the share surface on one resource type

Run the the social share surface build workflow (see instructions below) drill to deploy the complete sharing infrastructure:

**Step 1 — Choose the shareable resource type:**
Audit your product for the resource most likely to be shared. Rank candidates by share motivation:
- Achievements/milestones (pride, social proof) — highest
- Results/outputs (demonstrate product value) — high
- Dashboards/reports (professional sharing) — medium
- Templates/configurations (helpfulness) — medium

Pick ONE. At Smoke level, do not build share surfaces for multiple resource types.

**Step 2 — Deploy the share link system:**
Create the `share_links` and `share_clicks` database tables. Deploy the `POST /api/share` endpoint (generates tracked short URLs with attribution). Deploy the `GET /s/{code}` redirect handler (records clicks, sets attribution cookies). Test end-to-end: generate a link, click it in an incognito browser, verify the click is recorded.

**Step 3 — Deploy OG preview cards:**
Deploy the `/api/og` endpoint using @vercel/og or equivalent. Configure the template to show: resource title, key metric (if applicable), sharer name, product branding. Set the `og:image` meta tag on the shared resource page. Validate with LinkedIn Post Inspector and Twitter Card Validator.

**Step 4 — Build the share widget:**
Create the share button component and attach it to the chosen resource type. Build the share popover with channel options: Copy Link, Twitter/X, LinkedIn, Email. On mobile, use the native Web Share API. Each channel action calls the share link generation endpoint and opens the appropriate share flow.

**Step 5 — Instrument tracking:**
Configure PostHog events: `share_widget_opened`, `share_channel_selected`, `share_action_completed`, `share_link_clicked`. Build a PostHog funnel: widget opened -> channel selected -> action completed -> link clicked.

### 2. Deploy share prompts to a test group

Using the contextual share prompts from the social share surface build workflow (see instructions below):

- Identify 20-50 active users who have recently interacted with the target resource type
- Deploy an Intercom in-app message to this cohort: "You created [resource] — share it with your network?"
- The message includes a one-click button that opens the share widget pre-configured for their resource
- Time the prompt to appear immediately after the user views or completes the resource

**Human action required:** Review the test group selection. Ensure the 20-50 users are genuinely active and have a shareable resource. Approve the prompt copy before deploying.

### 3. Track results over 7 days

Monitor PostHog daily:
- How many users saw the share prompt? (Intercom delivery rate)
- How many opened the share widget? (share_widget_opened count)
- How many completed a share action? (share_action_completed count)
- Which channels did they use? (channel distribution)
- Did any shared links get clicked? (share_link_clicked count)
- Did any clicks lead to a signup? (share_referral_signup — bonus at Smoke level)

### 4. Evaluate against threshold

Run the `threshold-engine` drill to measure against pass criteria:

- **Share initiation rate**: share_widget_opened / users who saw the prompt >= 20%
- **External click-through**: at least 1 share_link_clicked event from a user who is not the sharer

If PASS: the share mechanism works and users will share when prompted. Proceed to Baseline.
If FAIL on initiation rate but some shares happened: the prompt timing or copy needs work. Test a different prompt moment (after a milestone vs. after viewing a report). Re-run for 1 more week.
If HARD FAIL (no shares at all): the chosen resource type may not be shareable. Try a different resource type. Or the share button placement is not visible — check impression tracking.

## Time Estimate

- 3 hours: share link system, OG cards, and share widget deployment
- 2 hours: PostHog event instrumentation and funnel setup
- 1 hour: test group identification and Intercom prompt configuration
- 2 hours: 7-day monitoring and evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Share event tracking, funnel analysis, user cohorts | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Share prompt in-app messages | Essential: $29/seat/mo ([intercom.com/pricing](https://intercom.com/pricing)) |
| Vercel | OG image generation endpoint hosting | Free tier: 100K Edge Function invocations/mo ([vercel.com/pricing](https://vercel.com/pricing)) |
| Attio | Track sharers and share link performance | Free tier: 3 seats ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated play-specific cost at this level:** Free (all within free tiers for a 20-50 user test)

## Drills Referenced

- the social share surface build workflow (see instructions below) — deploys the share button, share links, OG cards, and tracking layer
- `threshold-engine` — evaluates pass/fail and recommends next action
