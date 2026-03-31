---
name: newsletter-sponsor-booking
description: Negotiate, book, and manage paid newsletter sponsorship placements with tracked creative
category: Paid
tools:
  - Attio
  - Anthropic
  - PostHog
fundamentals:
  - newsletter-rate-negotiation
  - newsletter-blurb-copywriting
  - newsletter-placement-tracking
  - attio-deals
  - attio-notes
  - posthog-custom-events
---

# Newsletter Sponsor Booking

This drill handles the end-to-end process of booking a paid newsletter sponsorship: negotiating the rate, writing the ad copy, setting up tracking, and confirming the placement. One run of this drill produces one confirmed, tracked newsletter placement.

## Input

- Newsletter selected from the shortlist (from `newsletter-sponsor-research` drill)
- Approved budget for this placement
- Landing page URL for the campaign
- CTA type (demo request, free trial, resource download)

## Steps

### 1. Negotiate the rate

Use the `newsletter-rate-negotiation` fundamental to contact the ad sales person and secure a placement. For a first-time booking:

- Request the media kit if not already obtained during research
- If the published rate is above your budget, negotiate using one of: test-placement discount, multi-issue package, or off-peak pricing
- Target effective CPM of $20-50 for niche B2B newsletters

Once terms are agreed, create a deal record in Attio using `attio-deals`:
- Deal name: "Newsletter Sponsor — {newsletter_name} — {date}"
- Amount: agreed price
- Stage: "Booked"
- Close date: the newsletter send date
- Custom fields: newsletter name, placement format, creative deadline, subscriber count, expected open rate

### 2. Set up placement tracking

Use the `newsletter-placement-tracking` fundamental to build the tracked URL:

```
{landing_page}?utm_source={newsletter_slug}&utm_medium=paid-newsletter&utm_campaign=newsletter-sponsorships&utm_content={newsletter_slug}-{date}-v1
```

Verify the URL loads correctly and PostHog captures the UTM parameters. Create the `newsletter_sponsor_click` and `newsletter_sponsor_lead` events in PostHog using `posthog-custom-events`.

### 3. Write the ad copy

Use the `newsletter-blurb-copywriting` fundamental to generate 3 blurb variants tailored to the newsletter's tone and audience:

- Variant A: Curiosity-driven (open loop that makes the reader click)
- Variant B: Data-driven (lead with a specific stat or insight)
- Variant C: Problem-driven (name a pain point the reader recognizes)

Each variant must:
- Match the newsletter's editorial voice
- Stay within the publisher's word count limits
- Contain exactly one CTA link (the tracked URL from step 2)
- Lead with the reader's problem, not your product name

Select the strongest variant. If this is a repeat placement with this newsletter, check past placement performance in Attio and lean toward the angle that produced the best CTR.

### 4. Submit creative to the publisher

Send the finalized blurb to the publisher by their creative deadline:

- Plain-text blurb (easy to paste into their email editor)
- Image/logo assets if the format supports it (provide 2x resolution PNG, max 600px wide)
- The tracked CTA link — ask them not to modify it
- A note: "Happy to adjust wording for tone. The link is the one thing that needs to stay as-is."

Log the creative submission in Attio using `attio-notes`: record the blurb text, variant used, and tracked URL.

### 5. Confirm placement on send day

On the scheduled send date:
- Confirm with the publisher that the newsletter was sent
- Request a screenshot or forward of the sent email for your records
- Monitor PostHog for incoming clicks from `utm_source` matching this newsletter
- Log the confirmation in Attio and update the deal stage to "Live"

### 6. Collect results after 7 days

Pull results from PostHog:
- Total clicks: `$pageview` events where `utm_content` = `{placement_id}`
- Total leads: `newsletter_sponsor_lead` events where `utm_source` = `{newsletter_slug}`
- CPC: `placement_cost / total_clicks`
- CPL: `placement_cost / total_leads`
- Click-to-lead conversion rate: `total_leads / total_clicks`

Update the Attio deal record with actual performance data using `attio-notes`. Update the deal stage to "Completed" with outcome: "Pass" or "Fail" based on whether CPC/CPL met targets.

## Output

- One confirmed, tracked newsletter sponsorship placement
- Creative submitted and verified
- PostHog tracking capturing clicks and leads with newsletter attribution
- Full cost and performance data logged in Attio
- Ready for `threshold-engine` evaluation

## Triggers

Run this drill for each newsletter placement. At Smoke: 1-2 placements. At Baseline: 4-6 placements over 4 weeks. At Scalable: 10-20 placements/month across multiple newsletters.
