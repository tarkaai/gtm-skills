---
name: newsletter-shoutout-copy
description: Write, personalize, and deliver a co-marketing blurb for placement in a partner's newsletter
category: Partnerships
tools:
  - Anthropic
  - PostHog
fundamentals:
  - newsletter-blurb-copywriting
  - posthog-custom-events
---

# Newsletter Shoutout Copy

This drill produces a ready-to-publish co-marketing blurb tailored to a specific partner's newsletter, with tracking in place to measure clicks and leads.

## Input

- Partner company record from Attio (from `partner-prospect-research` drill)
- Partner newsletter audit data (tone, format, audience, constraints)
- Your landing page URL for this campaign
- Agreement from the partner on placement date and format

## Steps

### 1. Prepare the landing page and tracking

Before writing the blurb, ensure your landing page is ready:
- Confirm the landing page loads and converts (has a clear CTA: signup, demo request, or download)
- Build the UTM-tagged URL using this format:
  `{base_url}?utm_source={partner_slug}&utm_medium=newsletter&utm_campaign=co-marketing-shoutouts&utm_content={variant_id}`
- Use the `posthog-custom-events` fundamental to verify PostHog captures `pageview` events with UTM parameters from this URL
- Create a PostHog event `co_marketing_click` that fires when a visitor from this UTM source takes the primary CTA action (signup, demo request, etc.)

### 2. Write the blurb

Use the `newsletter-blurb-copywriting` fundamental to generate 3 blurb variants:
- Variant A: Curiosity-driven (open loop that makes the reader want to click)
- Variant B: Data-driven (lead with a specific stat or insight relevant to the audience)
- Variant C: Story-driven (short anecdote or scenario the reader relates to)

Each variant must:
- Match the partner newsletter's tone and voice
- Be under 100 words (unless partner specifies otherwise)
- Contain exactly one CTA link with UTM tracking
- Lead with the reader's problem, not your product

### 3. Select and refine the best variant

Review all 3 variants against the partner's newsletter style. Pick the one that reads most native. Tighten the copy: remove any word that doesn't earn its place. Verify the CTA link is correct and clickable.

If this is a repeat placement with the same partner, check past blurb performance in PostHog. Use the highest-performing angle as the starting template and iterate from there.

### 4. Send to partner for approval

Email the selected blurb to the partner contact. Include:
- Plain-text blurb (easy to copy-paste into their email editor)
- Image/logo if their format supports it (provide in 2x resolution, PNG format)
- The tracked CTA link (ask them not to modify it)
- Suggested placement in the newsletter (after their main content performs best)
- A note: "Feel free to adjust the wording to match your voice — the link is the one thing that needs to stay as-is."

### 5. Confirm placement and track

On the scheduled send date:
- Confirm with the partner that the newsletter was sent
- Monitor PostHog in real-time for `pageview` events with the UTM source matching this partner
- Log the placement in Attio on the partner record: date, newsletter issue, blurb variant used

### 6. Log results

After 7 days, pull results from PostHog:
- Total clicks (pageviews from this UTM source)
- Leads generated (co_marketing_click events)
- Click-to-lead conversion rate

Log these metrics in Attio on the partner record. This data feeds the `threshold-engine` drill for pass/fail evaluation and the `partner-performance-reporting` drill for ongoing optimization.

## Output

- One approved, tracked co-marketing blurb placed in a partner newsletter
- PostHog tracking capturing clicks and leads with partner attribution
- Performance data logged in Attio for future optimization

## Triggers

Run this drill for each newsletter placement. At Smoke level, run once. At Baseline, run 5-10 times across multiple partners. At Scalable, templatize and run 20+ times/month.
