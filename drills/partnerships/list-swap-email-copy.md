---
name: list-swap-email-copy
description: Write, personalize, and deliver a standalone swap email for a partner to send to their list
category: Partnerships
tools:
  - Anthropic
  - PostHog
  - Attio
fundamentals:
  - list-swap-email-authoring
  - posthog-custom-events
  - attio-contacts
---

# List Swap Email Copy

This drill produces a ready-to-send standalone email that a partner sends to their subscriber list on your behalf. Unlike a newsletter blurb (embedded inside the partner's email), a swap email is a dedicated message — the entire email is about your product/offer. In exchange, you send a similar email to your list on the partner's behalf.

## Input

- Partner company record from Attio (from `partner-prospect-research` drill)
- Partner newsletter audit data (tone, format, audience, subscriber count)
- Your landing page URL for this campaign
- Agreement from partner on swap terms (date, format, constraints)
- Partner's swap email to you (so you can send it to your list in return)

## Steps

### 1. Prepare tracking infrastructure

Before writing the email, set up measurement:

- Build the UTM-tagged landing page URL:
  `{base_url}?utm_source={partner_slug}&utm_medium=list-swap&utm_campaign=list-swaps-adjacent-startups&utm_content={variant_id}`

- Use the `posthog-custom-events` fundamental to verify PostHog captures:
  - `pageview` events with UTM parameters from the swap URL
  - `list_swap_click` event — fires when a visitor from this UTM source takes the primary CTA (signup, demo request, meeting booking)
  - `list_swap_meeting_booked` event — fires when a swap-sourced lead books a meeting

- Set PostHog person properties on swap-sourced visitors: `first_touch_source = list-swap`, `partner_source = {partner_slug}`

### 2. Write the swap email

Run the `list-swap-email-authoring` fundamental. Generate 3 email variants (curiosity, data-driven, story-driven). Each variant includes: subject line, preview text, HTML body, and plain-text body.

Key differences from a blurb:
- This is a full email (200-400 words), not a 60-100 word blurb
- It needs a subject line and preview text (the partner sends it, not embeds it)
- It should feel like a personal recommendation from the partner to their audience
- One CTA only — every link in the email points to the same tracked URL

### 3. Select the best variant

Review all 3 variants against the partner's newsletter style and audience. Choose the variant that:
- Reads most naturally as if the partner wrote it
- Leads with a pain point the audience immediately recognizes
- Has the clearest, most specific CTA (not "learn more" — instead "see the 2-minute walkthrough")

If this is a repeat swap with the same partner, check past swap performance in PostHog. Use the highest-performing angle as the starting template.

### 4. Prepare the reciprocal email

In a list swap, you must also send the partner's email to YOUR list. Coordinate:
- Receive the partner's swap email copy and CTA link
- Review it for quality (reject if it's irrelevant to your audience — protect your list)
- Schedule it in your email tool (Loops broadcast or Instantly one-off)
- Use your own UTM tags to track how your audience responds to the partner's content

### 5. Deliver the email to the partner

Send your approved swap email to the partner contact. Include:
- Subject line and preview text
- Plain-text version
- HTML version (if requested)
- The UTM-tracked CTA link — non-negotiable, must not be modified
- Any image/logo assets (2x resolution PNG)
- Preferred send date and time (Tuesday-Thursday, 9-11am in their audience timezone)
- Note: "Feel free to adjust wording for your voice. The CTA link must stay exactly as-is."

### 6. Coordinate simultaneous send

Both emails should send within the same week (ideally same day) so neither partner feels they gave more than they got. Agree on:
- Exact send date and time for both emails
- Confirmation protocol: both partners confirm "sent" after their email goes out
- Log both send timestamps in Attio

### 7. Monitor results

On send day and for 7 days after:
- Watch PostHog for `pageview` events with `utm_medium=list-swap` and `utm_source={partner_slug}`
- Track click velocity: burst arrival (engaged list) vs. trickle (low engagement)
- Monitor `list_swap_click` events for landing page conversions
- Monitor `list_swap_meeting_booked` events for meetings generated
- Also track how the partner's email to YOUR list performed (for reciprocity scoring)

### 8. Log results in CRM

After 7 days, pull from PostHog and record in Attio on the partner record:
- Outbound swap: clicks received, leads generated, meetings booked, click-to-meeting rate
- Inbound swap: how your list responded to the partner's email (opens, clicks, unsubscribes)
- Net swap value: did you give more value or receive more?
- Swap quality score: partner responsiveness, email quality, audience fit

This data feeds the `threshold-engine` drill for pass/fail evaluation.

## Output

- One approved, tracked swap email delivered to the partner for sending
- One reciprocal email from the partner scheduled to your list
- PostHog tracking capturing clicks, leads, and meetings with partner attribution
- Bidirectional performance data logged in Attio

## Triggers

Run this drill for each swap. At Smoke level, run once with one partner. At Baseline, run 3-5 times across partners. At Scalable, templatize and run 10+ per month with automated scheduling.
