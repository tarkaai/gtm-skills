---
name: podcast-sponsorships-b2b-baseline
description: >
  B2B Podcast Sponsorships — Baseline Run. Book 3-6 paid host-read sponsorships
  across multiple B2B podcasts over 6 weeks to validate repeatable lead generation
  and establish CPL benchmarks before scaling.
stage: "Marketing > Problem Aware"
motion: "LightweightPaid"
channels: "Paid, Content"
level: "Baseline Run"
time: "15 hours over 6 weeks"
outcome: "≥12 qualified leads and CPL within 2x of target across 3-6 podcast sponsorships in 6 weeks"
kpis: ["Total qualified leads", "Blended CPL", "CPC", "Click-to-lead conversion rate", "Promo code redemption rate"]
slug: "podcast-sponsorships-b2b"
install: "npx gtm-skills add marketing/problem-aware/podcast-sponsorships-b2b"
drills:
  - podcast-sponsor-research
  - podcast-sponsor-booking
  - posthog-gtm-events
  - threshold-engine
---

# B2B Podcast Sponsorships — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** LightweightPaid | **Channels:** Paid, Content

## Outcomes

3-6 paid host-read sponsorship placements booked across multiple B2B podcasts over 6 weeks. At least 12 qualified leads total with a blended CPL within 2x of your target, demonstrating that podcast sponsorships are a repeatable lead generation channel — not a one-off fluke from Smoke. You now have performance data across multiple shows, ad script angles, and audiences to inform scaling decisions.

## Leading Indicators

- 3+ podcast placements booked within the first 2 weeks (signal: pipeline velocity is sufficient)
- Each placement generates at least 10 clicks across all signals within 14 days (signal: consistent audience engagement)
- At least 2 different podcasts produce leads (signal: the channel works, not just one specific show)
- Blended CPL is declining week-over-week as you learn which shows and scripts convert (signal: the playbook is improving)
- Promo code redemptions appear across multiple placements (signal: the verbal CTA is driving purchase intent)

## Instructions

### 1. Expand the podcast research pipeline

Run the `podcast-sponsor-research` drill at full scope: search AdvertiseCast, Podcorn, Gumball, RedCircle, and direct outreach targets. Evaluate 25-30 candidate podcasts. Score and shortlist 10-15.

Use learnings from Smoke to refine selection criteria:
- If the Smoke podcast worked, find 5+ similar shows (same topic, similar audience size, comparable CPM)
- If the Smoke podcast failed, shift targeting: different audience segment, different podcast size tier, or different industry vertical
- Prioritize podcasts with weekly publishing cadence (faster testing velocity)

Push the shortlist to Attio with tier rankings. Plan to book Tier 1 podcasts first, Tier 2 after initial results confirm.

### 2. Configure end-to-end tracking pipeline

Run the `posthog-gtm-events` drill to set up standardized tracking across all podcast placements:

- Event: `podcast_sponsor_click` — fires on landing page load when `utm_medium` = `paid-podcast`
- Event: `podcast_sponsor_lead` — fires on CTA completion (signup, demo, form) with `podcast_name` property
- Event: `podcast_sponsor_promo_redeem` — fires on promo code redemption with `promo_code` property
- Dashboard: "Podcast Sponsorships — Baseline" with panels for click volume by podcast, lead funnel by podcast, and placement ROI table

Create unique UTM parameters, vanity URLs, and promo codes for each placement. Maintain a naming convention:
- UTM content: `{podcast_slug}-{YYYY-MM-DD}-v{variant}`
- Vanity URL: `yoursite.com/{podcast_slug}`
- Promo code: `{PODCASTNAME}` (all caps, no spaces)

### 3. Book 3-6 placements across different podcasts

Run the `podcast-sponsor-booking` drill for each placement, staggering bookings over 6 weeks:

- **Week 1-2**: Book 2 Tier 1 podcasts. Use the strongest ad script angle from Smoke.
- **Week 3-4**: Book 2 more podcasts (Tier 1 or Tier 2). Test a different ad script angle to compare.
- **Week 5-6**: Book 1-2 additional podcasts based on early results. Double down on the show type or script angle producing the best CPL.

For each placement:
- Negotiate rate (target effective CPM $20-50 for niche B2B)
- Write host-read ad script tailored to each podcast's audience and tone
- Configure unique tracking (UTM + vanity URL + promo code)
- Submit creative by the host's deadline
- Verify placement on air date

**Human action required:** Approve each placement cost. Process payments. Review ad scripts before submission.

### 4. Run ad script A/B testing across placements

Systematically test ad script angles across your placements:

- **Test variable 1**: Script angle. Run problem-led on 2 podcasts and story-led on 2 podcasts. Compare click-to-lead conversion rate.
- **Test variable 2**: CTA type. Run vanity-URL-only CTA on half the placements and vanity-URL-plus-promo-code on the other half. Compare total attributed leads.
- **Test variable 3**: Landing page. If you have 4+ placements, split half to a demo-request page and half to a free-trial page. Compare conversion rate.

Log every variant in Attio on the deal record so you can compare performance by variable.

### 5. Monitor and adjust biweekly

Every 2 weeks, review all placement results to date:

- Which podcasts generated the most leads relative to cost?
- Which ad script angle (problem vs. story vs. data) had the highest conversion rate?
- Which attribution signal (UTM, vanity URL, promo code) accounts for the most leads?
- Is there a pattern in podcast size, topic, or audience that predicts success?

Adjust the remaining bookings based on these learnings. Cancel or defer Tier 2 podcasts if Tier 1 is producing strong results and you want to double down.

### 6. Evaluate against threshold

Run the `threshold-engine` drill after 6 weeks (or when all placements have completed their 14-day measurement windows). Measure:

- **Total qualified leads across all placements**: UTM leads + promo code redemptions
- **Blended CPL**: total spend / total leads
- **Per-podcast CPL**: identify the best and worst performers
- **Click-to-lead conversion rate**: total leads / total clicks

**Pass threshold: >= 12 qualified leads AND blended CPL within 2x of target**

- **Pass**: Document the top-performing podcasts, script angles, and CTA formats. Proceed to Scalable.
- **Marginal**: 6-11 leads or CPL between 2-3x target. Continue testing for 4 more weeks with refined targeting.
- **Fail**: <6 leads or CPL above 3x target. Diagnose: wrong podcast audience, weak ad scripts, or landing page conversion problem? Consider pivoting to newsletter sponsorships or a different LightweightPaid play.

## Time Estimate

- Expanded podcast research: 3 hours
- Tracking pipeline setup: 1.5 hours
- Booking 3-6 placements (negotiation, scripts, tracking per placement): 7 hours (1-1.5 hours each)
- Biweekly monitoring and analysis: 2 hours (1 hour x 2 reviews)
- Final evaluation: 1.5 hours

Total: ~15 hours of active work over 6 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| AdvertiseCast / Podcorn / Gumball | Marketplace booking | Free for advertisers |
| ListenNotes | Directory search | $9/mo for 300 req/day ([listennotes.com/pricing](https://www.listennotes.com/api/pricing/)) |
| Clay | Publisher enrichment | Launch: $185/mo ([clay.com/pricing](https://www.clay.com/pricing)) |
| Attio | CRM deal tracking | Free up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Multi-signal attribution | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Dub.co | Vanity URLs | Free: 1,000 links/mo ([dub.co/pricing](https://dub.co/pricing)) |
| Anthropic Claude | Ad script generation | ~$0.10-0.50 per script ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| Podcast placements (3-6x) | Paid sponsorships | $300-2,400 total ($100-400 per placement) |

**Estimated cost for this level: $500-2,500/mo** (primarily the sponsorship placements; tools at free/entry tiers)

## Drills Referenced

- `podcast-sponsor-research` — expanded search across 25+ candidates, shortlist 10-15
- `podcast-sponsor-booking` — end-to-end booking for each placement with multi-signal tracking
- `posthog-gtm-events` — standardized event tracking across all placements
- `threshold-engine` — evaluate total leads and blended CPL against the pass threshold
