---
name: public-sharing-baseline
description: >
  Branded Public Sharing — Baseline Run. Roll out public sharing to 50% of users
  with always-on tracking, automated share prompts at moments of delight,
  and continuous funnel measurement.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product, Social"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=35% share publicly AND >=5% viewer-to-signup conversion"
kpis: ["Public share rate", "Share completion rate", "Share page views per share", "CTA click-through rate", "Viewer-to-signup conversion"]
slug: "public-sharing"
install: "npx gtm-skills add product/referrals/public-sharing"
drills:
  - referral-program
  - feature-announcement
  - activation-optimization
---

# Branded Public Sharing — Baseline Run

> **Stage:** Product > Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product, Social

## Outcomes

35% or more of users exposed to the feature share at least one piece of content publicly. 5% or more of share page viewers complete signup. The share funnel runs continuously with automated prompts, tracking, and attribution — no manual intervention required to maintain it.

## Leading Indicators

- Share prompt open rates above 15% (Intercom messages are reaching users at the right moment)
- Share completion rate above 70% (the share flow is frictionless)
- Average 5+ views per share page within 7 days (shared links get distributed)
- CTA click-through rate above 8% on share pages (the branded element is compelling)
- Signup form completion rate above 50% for share-referred visitors (the signup flow from share pages works)

## Instructions

### 1. Formalize the share incentive and tracking

Run the `referral-program` drill to build the tracking and incentive layer for public sharing:

**Incentive design:** Choose one model:
- **Creator reward:** Users who share publicly and drive signups earn product credits, extended storage, or premium features. Example: "Each signup from your shared page unlocks 1GB extra storage."
- **Two-sided reward:** Referrer gets a benefit, viewer gets a benefit for signing up. Example: "Share publicly — your viewers get a free Pro trial, you get a month of Pro for every 3 signups."
- **Recognition reward:** Top sharers get featured in a public gallery or leaderboard. No monetary cost, leverages status.

**Tracking chain:** Instrument the full attribution path:
1. `share_published` event carries `referrer_user_id`
2. Share page URL includes `ref={referrer_user_id}` parameter
3. Signup from share page captures `referrer_user_id` from the URL parameter
4. `share_signup_completed` event links the new user to the referrer
5. n8n webhook creates the Attio contact with `acquisition_source=public-share` and `referrer={referrer_user_id}`
6. When the referred user activates, fire `share_referral_activated` and trigger the referrer reward

### 2. Announce and prompt public sharing

Run the `feature-announcement` drill to deploy always-on share prompts:

**Announcement campaign (one-time):**
- Intercom in-app banner for all users in the 50% treatment group: "New: share your work publicly and earn [reward]"
- Loops email to the same cohort: subject "Your [content type] deserves an audience" with a direct link to the share flow

**Contextual prompts (always-on):**
Using Intercom in-app messages, trigger share prompts at moments of delight:
- After a user completes a significant piece of work (defined by your activation metric): "Nice work. Share it publicly?"
- After a user reaches a usage milestone (10th project, 50th edit, etc.): "You've hit [milestone]. Show the world what you've built."
- After a user receives positive feedback in the product (if applicable): "Others would love to see this. Share it publicly."

Set PostHog feature flags to gate the treatment group (50% of eligible users). The other 50% is the control group — they have the share feature available but receive no prompts.

### 3. Optimize the share-to-signup funnel

Run the `activation-optimization` drill to identify and fix the biggest drop-off in the share funnel:

1. Pull the PostHog funnel: `share_initiated` -> `share_published` -> `share_page_viewed` -> `share_cta_clicked` -> `share_signup_completed`
2. Identify the step with the largest drop-off percentage
3. For each possible bottleneck:
   - **Initiation to completion drop-off:** The share flow is too complex. Test: reduce form fields, pre-fill share title and description from content metadata, add a "one-click share" option that publishes with defaults.
   - **Published to viewed drop-off:** Users are not distributing their share links. Test: add social sharing buttons (LinkedIn, Twitter, email, copy-link) on the share confirmation page. Pre-populate share text with a hook.
   - **Viewed to CTA click drop-off:** The branded CTA is not compelling. Test: CTA copy variants ("Create yours free" vs "Try [Product]" vs "See how this was made"), CTA placement (sticky bottom bar vs inline after content vs floating badge), CTA design (button color, size, animation).
   - **CTA click to signup drop-off:** The signup page does not match expectations. Test: a dedicated signup page for share-referred visitors that references what they just saw ("You just viewed [content]. Create your own in 2 minutes.").
4. Implement the fix for the biggest bottleneck. Measure for 1 week. Move to the next bottleneck.

### 4. Run treatment vs. control comparison

After 2 weeks, compare the treatment group (share prompts enabled) vs. control group (no prompts):

- Treatment share rate vs. control share rate — measures the lift from prompts
- Treatment retention vs. control retention — ensures prompts do not annoy users into churning
- Share-acquired user activation rate — are viewers who sign up actually using the product?

Evaluate against threshold: >=35% share rate in the treatment group AND >=5% viewer-to-signup conversion across all share pages.

If PASS: Roll out prompts to 100% of users. Document the winning prompt timing, copy, and placement. Proceed to Scalable.

If FAIL: Identify whether the miss is on the share rate (not enough users sharing) or the conversion rate (viewers not signing up). Focus optimization on whichever is further from threshold. Re-run for another 2-week cycle.

## Time Estimate

- 3 hours: referral tracking chain setup and incentive implementation
- 3 hours: feature announcement campaign and contextual prompts
- 6 hours: funnel analysis and optimization (2 hours per bottleneck, 3 bottlenecks)
- 2 hours: treatment vs. control analysis
- 2 hours: documentation and Scalable preparation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Funnels, feature flags, A/B cohorts | Free tier: 1M events/mo — https://posthog.com/pricing |
| Intercom | In-app share prompts and announcements | Included in standard stack |
| Loops | Lifecycle email announcements | Included in standard stack |
| n8n | Signup routing and reward automation | Included in standard stack |
| Attio | Contact attribution tracking | Included in standard stack |

**Play-specific cost:** Free (all tools within standard stack or free tier)

## Drills Referenced

- `referral-program` — builds the share incentive structure, referral attribution chain, and reward fulfillment automation
- `feature-announcement` — deploys the one-time announcement campaign and always-on contextual share prompts via Intercom and Loops
- `activation-optimization` — identifies and fixes the largest drop-off point in the share-to-signup funnel
