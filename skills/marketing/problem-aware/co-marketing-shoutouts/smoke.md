---
name: co-marketing-shoutouts-smoke
description: >
  Partner Newsletter Shoutout — Smoke Test. Place one co-marketing blurb in one
  partner's newsletter to validate that partner audiences generate clicks and leads
  before investing in a multi-partner program.
stage: "Marketing > Problem Aware"
motion: "Partnerships & Warm Intros"
channels: "Email"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: "≥ 20 clicks and ≥ 1 lead in 1 week"
kpis: ["Impressions", "Click-through rate"]
slug: "co-marketing-shoutouts"
install: "npx gtm-skills add marketing/problem-aware/co-marketing-shoutouts"
drills:
  - partner-prospect-research
  - newsletter-shoutout-copy
  - threshold-engine
---

# Partner Newsletter Shoutout — Smoke Test

> **Stage:** Marketing → Problem Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Email

## Outcomes

One co-marketing blurb placed in one partner newsletter. At least 20 clicks to your landing page and at least 1 lead (signup, demo request, or form submission) within 7 days of the newsletter send. This proves that partner newsletter audiences respond to your value proposition before you invest in scaling the channel.

## Leading Indicators

- Partner responds to outreach within 3 days (signal: the partnership pitch resonates)
- Partner agrees to a placement without requiring payment (signal: mutual value is clear)
- Blurb CTR exceeds 1% of estimated newsletter audience (signal: copy and audience are aligned)
- Clicks arrive within 24 hours of newsletter send (signal: audience is engaged and active)

## Instructions

### 1. Research and select one partner

Run the `partner-prospect-research` drill with a reduced scope: identify 5-10 candidate companies with newsletters whose audiences overlap your ICP. Score each newsletter on audience overlap, size, engagement quality, and co-marketing friendliness.

Select the single highest-scoring partner for this smoke test. Prioritize partners where you have an existing relationship (founder knows someone there, shared investor, met at an event) because cold partner outreach adds latency to a smoke test.

### 2. Pitch the partnership

**Human action required:** Reach out to your selected partner. Send a short email or LinkedIn DM to the newsletter owner or partnerships lead:

- Explain what you are proposing: a one-time, free blurb in their next newsletter issue
- Explain the mutual value: you get exposure to their audience, they get useful content for their readers
- Offer to reciprocate: feature them in your newsletter, social channels, or provide something of value in return
- Propose a specific date for the placement (their next newsletter send)

Log the outreach in Attio. Update the partner status from "Prospect" to "In Conversation."

### 3. Prepare your landing page

Ensure you have a landing page ready to receive traffic from the newsletter. The page must:
- Have one clear CTA (demo request, free trial signup, resource download)
- Load in under 3 seconds
- Work on mobile (most newsletter readers open on phones)
- Have PostHog tracking installed to capture `pageview` and `co_marketing_click` events

Build the UTM-tagged URL: `{your_landing_page}?utm_source={partner_slug}&utm_medium=newsletter&utm_campaign=co-marketing-shoutouts&utm_content=smoke-v1`

### 4. Write and deliver the blurb

Run the `newsletter-shoutout-copy` drill. Generate 3 blurb variants, select the best fit for the partner's newsletter tone, and send it to your partner contact for approval. Include:
- Plain-text blurb (60-100 words)
- Logo/image if the format supports it
- The UTM-tracked CTA link
- A note giving them permission to adjust wording for tone

### 5. Monitor results in real-time

On the day the newsletter sends:
- Watch PostHog for incoming `pageview` events with `utm_source` matching the partner
- Note the click velocity: are clicks arriving in a burst (engaged audience) or a trickle?
- Monitor `co_marketing_click` events for lead conversions

### 6. Evaluate against threshold

Run the `threshold-engine` drill 7 days after the newsletter send. Measure:
- Total clicks (pageviews from this UTM source)
- Total leads (co_marketing_click events)

**Pass threshold: ≥ 20 clicks AND ≥ 1 lead**

- **Pass**: Document what worked (partner, blurb angle, landing page). Proceed to Baseline.
- **Marginal**: 10-19 clicks or 0 leads but high engagement signals. Try one more partner before deciding.
- **Fail**: <10 clicks. Diagnose: Was the audience wrong? Was the blurb off-target? Was the newsletter too small? Iterate and re-test with a different partner.

## Time Estimate

- Partner research and selection: 1 hour
- Partner outreach and negotiation: 30 minutes (human action)
- Landing page prep and tracking setup: 30 minutes
- Blurb writing and partner approval: 30 minutes
- Monitoring and evaluation: 30 minutes

Total: ~3 hours of active work over 1 week (waiting for partner response and newsletter send date)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Partner research and enrichment | Launch: $185/mo; legacy Starter from $149/mo ([clay.com](https://www.clay.com)) |
| Attio | Partner CRM tracking | Free for up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Click and lead tracking | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Anthropic Claude | Blurb copywriting | Pay-per-use, ~$0.10-0.50 per blurb ([anthropic.com/pricing](https://anthropic.com/pricing)) |

**Estimated cost for this level: Free** (all tools within free tiers for a single placement)

## Drills Referenced

- `partner-prospect-research` — find and score newsletter partners matching your ICP
- `newsletter-shoutout-copy` — write, track, and deliver the co-marketing blurb
- `threshold-engine` — evaluate clicks and leads against the pass threshold
