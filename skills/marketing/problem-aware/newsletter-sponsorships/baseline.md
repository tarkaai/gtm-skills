---
name: newsletter-sponsorships-baseline
description: >
  Newsletter Sponsorship — Baseline Run. Run 4-6 paid newsletter placements across
  3+ newsletters over 4 weeks to validate repeatable lead generation and establish
  baseline CPC and CPL benchmarks.
stage: "Marketing > Problem Aware"
motion: "LightweightPaid"
channels: "Email"
level: "Baseline Run"
time: "10 hours over 4 weeks"
outcome: "≥ 80 clicks and ≥ 5 leads from 4-6 paid newsletter placements over 4 weeks, with CPL below $200"
kpis: ["Total clicks", "Total leads", "Blended CPC", "Blended CPL", "Click-to-lead conversion rate"]
slug: "newsletter-sponsorships"
install: "npx gtm-skills add marketing/problem-aware/newsletter-sponsorships"
drills:
  - newsletter-sponsor-booking
  - posthog-gtm-events
  - threshold-engine
---

# Newsletter Sponsorship — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** LightweightPaid | **Channels:** Email

## Outcomes

4-6 paid newsletter placements executed across at least 3 different newsletters over 4 weeks. At least 80 total clicks and 5 leads with a blended CPL below $200. This proves that newsletter sponsorships are a repeatable lead generation channel, not a one-off fluke, and establishes CPC/CPL benchmarks for scaling.

## Leading Indicators

- At least 3 newsletters booked within the first week (signal: publisher pipeline is healthy)
- Each placement generates clicks within 24 hours of send (signal: consistent audience engagement across newsletters)
- CPC stays below $5 across placements (signal: the channel is cost-competitive with other paid channels)
- At least 2 different newsletters produce leads (signal: the channel works beyond a single newsletter, reducing concentration risk)

## Instructions

### 1. Expand the newsletter shortlist

Using the research from your Smoke test as a starting point, run the `newsletter-sponsor-research` drill again with broader scope. You now know what a good newsletter looks like for your ICP. Expand to 15-20 candidates and shortlist the top 8-10 based on ICP density and cost-efficiency.

Include a mix of:
- The newsletter that passed your Smoke test (rebook it)
- 2-3 newsletters from Paved with similar audience profiles
- 1-2 newsletters found through direct outreach (often cheaper than marketplace newsletters)
- 1 newsletter in an adjacent category (test whether a broader audience still converts)

### 2. Set up standardized tracking

Run the `posthog-gtm-events` drill to establish a complete event taxonomy for newsletter sponsorships:
- `newsletter_sponsor_click`: fires on pageview where `utm_medium` = `paid-newsletter`
- `newsletter_sponsor_lead`: fires when a newsletter-sourced visitor completes the CTA
- `newsletter_sponsor_qualified`: fires when the lead is confirmed as ICP-matching in Attio

Use consistent UTM structure across all placements:
```
utm_source={newsletter_slug}&utm_medium=paid-newsletter&utm_campaign=newsletter-sponsorships&utm_content={newsletter_slug}-{date}-{variant}
```

### 3. Book 4-6 placements over 4 weeks

Run the `newsletter-sponsor-booking` drill for each placement. Stagger bookings across the 4-week period — ideally 1-2 placements per week. This gives you:
- Time to analyze early results and adjust copy for later placements
- Data on whether placement day-of-week affects performance
- Comparison data across multiple newsletters

For each placement:
- Negotiate the rate (leverage multi-booking intent: "We plan to test 5-6 newsletters this month")
- Write blurb copy tailored to each newsletter's tone (do not reuse identical copy across newsletters)
- Submit creative by each publisher's deadline
- Use a fresh `utm_content` tag per placement for granular tracking

**Human action required:** Approve the total budget allocation for 4-6 placements ($500-2,000 total). Process payments as invoiced.

### 4. Build the performance monitoring system

Run the `newsletter-sponsor-performance-monitor` drill to set up:
- A PostHog dashboard tracking clicks and leads per newsletter
- Automated 7-day post-placement performance collection via n8n
- Newsletter tier assignments based on actual CPL data
- A weekly performance report aggregating all placements

### 5. Optimize blurb copy based on early data

After the first 2 placements produce results:
- Compare click-through rates across blurb angles (curiosity vs. data vs. problem-driven)
- Identify which CTA framing produces the best click-to-lead conversion
- Apply the winning angle to subsequent placements
- For newsletters you are rebooking, iterate on the blurb rather than reusing the same copy

### 6. Evaluate against threshold

Run the `threshold-engine` drill after 4 weeks. Measure:
- Total clicks across all placements
- Total leads across all placements
- Blended CPC: total spend / total clicks
- Blended CPL: total spend / total leads
- Click-to-lead conversion rate: total leads / total clicks
- Newsletter concentration: are leads coming from multiple newsletters or just one?

**Pass threshold: >= 80 clicks AND >= 5 leads AND CPL below $200**

- **Pass**: You have a repeatable channel. Document the best-performing newsletters, blurb angles, and CPL benchmarks. Proceed to Scalable.
- **Marginal**: 50-79 clicks or 3-4 leads. Extend the test for 2 more weeks with 2-3 additional placements. Iterate on blurb copy and newsletter selection.
- **Fail**: <50 clicks or CPL above $300 after 4-6 placements. The newsletter sponsorship channel may not work for your ICP at current pricing. Consider: are you targeting the right newsletters? Is your landing page converting? Is your value proposition clear to this audience?

## Time Estimate

- Newsletter research expansion: 2 hours
- Tracking setup: 1 hour
- Booking 4-6 placements (negotiation, copy, submission): 4 hours (split across 4 weeks)
- Performance monitoring setup: 1.5 hours
- Analysis and optimization: 1.5 hours

Total: ~10 hours of active work over 4 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Paved | Newsletter marketplace | Free for advertisers ([paved.com](https://www.paved.com)) |
| Clay | Publisher research | Launch: $185/mo ([clay.com/pricing](https://www.clay.com/pricing)) |
| Attio | Placement and lead CRM tracking | Free up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Analytics and funnel tracking | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Automated performance collection | Free self-hosted; Cloud from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Anthropic Claude | Blurb copywriting | Pay-per-use, ~$0.50-2.00 total ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| Newsletter placements | 4-6 paid sponsorships | $500-2,000 total for 4-6 niche placements |

**Estimated cost for this level: $600-2,200/mo** (dominated by placement spend)

## Drills Referenced

- `newsletter-sponsor-booking` — book, write, track, and collect results for each placement
- `posthog-gtm-events` — set up standardized event taxonomy for newsletter sponsorship tracking
- `threshold-engine` — evaluate aggregate performance against pass thresholds
