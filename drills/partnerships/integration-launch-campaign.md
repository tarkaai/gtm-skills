---
name: integration-launch-campaign
description: Execute a co-marketing launch campaign for a new product integration with a partner
category: Partnerships
tools:
  - Anthropic
  - Loops
  - PostHog
  - Attio
  - n8n
fundamentals:
  - partner-co-marketing-brief
  - loops-broadcasts
  - loops-audience
  - posthog-custom-events
  - posthog-funnels
  - attio-deals
  - attio-notes
  - n8n-workflow-basics
---

# Integration Launch Campaign

This drill executes the go-to-market launch for a completed product integration. It generates co-marketing assets, coordinates distribution across your audience and the partner's, tracks leads attributed to the integration, and measures launch performance.

## Input

- Completed and tested product integration with a partner
- Partner agreement on co-marketing scope (which assets, distribution channels, launch date)
- Your email list segmented by relevance (users who might benefit from this integration)
- Partner's commitment to distribute to their audience (email, blog, social, in-app)

## Steps

### 1. Generate co-marketing assets

Run the `partner-co-marketing-brief` fundamental with the integration context. This produces:

- Joint landing page copy (hero, benefits, setup steps, CTA)
- Co-marketing blog post (800 words, problem-solution-use cases format)
- Two email announcements (one for your audience, one for partner's audience)
- UTM tracking parameters for every asset and channel

**Human action required:** Review all generated copy with the partner. Agree on final versions. Implement the landing page on your website. Publish the blog post. The agent prepares the content; humans approve and ship it.

### 2. Configure tracking in PostHog

Use the `posthog-custom-events` fundamental to define integration launch events:

- `integration_landing_page_viewed`: User visits the integration landing page (fire on pageview with UTM filter)
- `integration_activated`: User enables or installs the integration in your product
- `integration_first_sync`: First data sync or action completed through the integration
- `integration_lead_captured`: A new lead arrives from the partner's distribution (identified by partner UTM source)

Use the `posthog-funnels` fundamental to build the integration launch funnel:
`integration_landing_page_viewed` -> `integration_activated` -> `integration_first_sync`

Filter by `utm_source` = partner slug to separate partner-sourced traffic from organic.

### 3. Send your audience announcement

Use the `loops-audience` fundamental to create a segment of users who would benefit from this integration. Criteria:
- Active users (logged in within last 30 days)
- Users in industries or roles where the partner product is commonly used
- Users who have not already activated this integration

Use the `loops-broadcasts` fundamental to send the announcement email to this segment. Include:
- Subject line and preview text from the co-marketing brief
- Email body with the integration value proposition
- CTA linking to the integration landing page with your UTM parameters
- Unsubscribe-safe (this is a product announcement, not a marketing blast)

### 4. Coordinate partner distribution

Provide the partner with their launch assets:
- Email copy (the "partner audience" version from the co-marketing brief)
- Blog post copy (for cross-posting on their blog)
- Social media copy (2-3 posts for LinkedIn/Twitter with partner UTM links)
- Landing page URL with partner UTM parameters

**Human action required:** Confirm the partner's distribution date and channels. Ensure UTM parameters are correctly applied to all partner links.

Track in Attio using the `attio-notes` fundamental: log the partner's planned distribution channels, dates, and estimated reach. Update as the partner confirms each distribution action.

### 5. Create the integration deal in Attio

Use the `attio-deals` fundamental to create a deal record for the integration partnership:

- Deal name: "Integration — {partner_name}"
- Pipeline: Partnerships
- Stage: Launched
- Fields: launch date, partner contact, co-marketing assets URLs, UTM tracking links
- Expected value: estimated pipeline from partner-sourced leads (based on partner audience size x estimated conversion)

### 6. Monitor launch performance

Build an n8n workflow using the `n8n-workflow-basics` fundamental that runs daily for the first 14 days post-launch:

1. Pull PostHog data: landing page views, integration activations, and leads by UTM source
2. Compare to pre-launch baseline (if this is an existing integration being re-launched) or to the play's threshold targets
3. Update the Attio deal record with cumulative metrics
4. If partner-sourced leads > 0 in the first 48 hours, send a Slack notification celebrating the early signal
5. If zero partner-sourced traffic after 72 hours, alert: partner distribution may not have happened — follow up

### 7. Post-launch retrospective

After 14 days, compile launch results:

- Total landing page views (by source: your email, partner email, blog, social, organic)
- Integration activations (total and by source)
- Leads captured from partner distribution
- Email performance (open rate, click rate for both your and partner's sends)
- Funnel conversion: views -> activations -> first sync

Log the retrospective as an Attio note on the deal. Flag whether the partnership met the lead target for this integration. If yes, mark for ongoing co-marketing. If no, diagnose: was it a distribution problem (partner didn't send) or a conversion problem (traffic came but didn't activate)?

## Output

- Complete set of co-marketing launch assets (landing page, blog, emails, social copy)
- PostHog tracking and funnel for the integration launch
- Email announcement sent to your relevant user segment
- Partner-ready distribution package with tracked URLs
- 14-day launch performance report
- Attio deal record with all launch metrics

## Triggers

Run this drill once per new integration launch. For major integrations, run a "re-launch" version quarterly with updated messaging and fresh audience segments.
