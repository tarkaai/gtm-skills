---
name: co-marketing-shoutouts-baseline
description: >
  Partner Newsletter Shoutout — Baseline Run. Run co-marketing blurbs across
  5-10 partner newsletters with proper tracking and attribution to validate
  repeatability before automating.
stage: "Marketing > Problem Aware"
motion: "Partnerships & Warm Intros"
channels: "Email"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 50 clicks and ≥ 3 leads over 2 weeks"
kpis: ["Impressions", "Click-through rate"]
slug: "co-marketing-shoutouts"
install: "npx gtm-skills add marketing/problem-aware/co-marketing-shoutouts"
drills:
  - posthog-gtm-events
  - newsletter-shoutout-copy
  - warm-intro-request
---

# Partner Newsletter Shoutout — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Email

## Outcomes

Co-marketing blurbs placed in 5-10 different partner newsletters over 2 weeks. At least 50 total clicks and 3 leads across all placements. This level proves the channel is repeatable across multiple partners, not just a one-off win, and establishes per-partner performance baselines that inform which partnerships to scale.

## Leading Indicators

- 3+ partners agree to placements within the first week (signal: the pitch template works)
- Per-partner click volume is consistent (±30%) across newsletters of similar size (signal: results are not partner-dependent flukes)
- At least 2 different blurb variants produce clicks (signal: the channel works beyond one lucky angle)
- Click-to-lead conversion rate holds above 2% across partners (signal: traffic quality is real)
- Partners proactively offer repeat placements (signal: the partnership is genuinely mutual)

## Instructions

### 1. Set up event tracking

Run the `posthog-gtm-events` drill to configure a standardized event taxonomy for this play. Create these PostHog events:

- `co_marketing_partner_contacted` — fired when outreach is sent to a partner
- `co_marketing_placement_confirmed` — fired when a partner agrees to a placement
- `co_marketing_blurb_sent` — fired when the blurb is delivered to the partner
- `co_marketing_click` — fired when a visitor from a co-marketing UTM source takes the landing page CTA
- `co_marketing_lead_created` — fired when a co-marketing click converts to a CRM lead

Set standard properties on each event: `partner_slug`, `blurb_variant`, `placement_date`, `newsletter_name`.

### 2. Expand partner outreach

Using the partner list from Smoke (or run `partner-prospect-research` again with a larger scope of 20 candidates), reach out to 10-15 partners. For partners where you lack a direct relationship, run the `warm-intro-request` drill to map mutual connections and request introductions.

For each partner outreach:
- Personalize the pitch based on their specific newsletter and audience
- Reference the Smoke test results if the same partner type: "We ran a test with [similar partner] and saw [X clicks, Y leads]"
- Propose a specific placement date
- Log every outreach attempt in Attio with the `co_marketing_partner_contacted` event

**Human action required:** Send the outreach messages. Warm intros and partnership pitches work better coming from a founder or senior team member, not a cold automation.

### 3. Write and deliver blurbs for each confirmed partner

For each partner that confirms, run the `newsletter-shoutout-copy` drill:
- Tailor the blurb to each partner's specific newsletter tone and audience
- Use different blurb variants across partners to test which angles perform best
- Tag each blurb with a unique `utm_content` parameter (e.g., `curiosity-v1`, `data-v2`, `story-v1`)
- Track which variant goes to which partner

### 4. Monitor per-partner performance

After each newsletter sends, track in PostHog:
- Clicks per partner (utm_source breakdown)
- Leads per partner
- Click velocity (how fast clicks arrive after send)
- Blurb variant performance (utm_content breakdown)

Build a simple PostHog insight: bar chart of clicks grouped by `utm_source`, filtered to `utm_campaign = co-marketing-shoutouts`.

### 5. Identify top-performing patterns

After all placements have run (7+ days after the last send), analyze:
- Which partners drove the most clicks per estimated newsletter subscriber? (This is your partner-level efficiency metric)
- Which blurb variants drove the highest CTR? (This is your copy optimization lever)
- Which landing page CTA drove the highest click-to-lead conversion? (This is your conversion optimization lever)
- Did any partners generate zero clicks? (Diagnose: wrong audience, bad placement position, or newsletter engagement issues)

### 6. Evaluate against threshold

Measure aggregate results across all placements:

**Pass threshold: ≥ 50 clicks AND ≥ 3 leads over 2 weeks**

- **Pass**: Document per-partner performance, top blurb variants, and conversion rates. Rank partners by efficiency. Proceed to Scalable.
- **Marginal**: 30-49 clicks or 1-2 leads. Investigate which partners underperformed and whether better copy or landing pages would close the gap. Run one more week.
- **Fail**: <30 clicks across all partners. The channel may not fit your ICP. Before pivoting, test: different partner types, different blurb angles, or a different landing page offer.

## Time Estimate

- Event tracking setup: 1 hour
- Partner outreach (10-15 partners): 3 hours
- Blurb writing (5-10 variants): 3 hours
- Partner communication and approval: 2 hours
- Monitoring and analysis: 2 hours
- Final evaluation: 1 hour

Total: ~12 hours of active work over 2 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking and analytics | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | Partner CRM and lead tracking | Free for up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| Anthropic Claude | Blurb copywriting (5-10 variants) | ~$0.50-2.00 total ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| Clay | Partner enrichment (if re-running research) | Launch: $185/mo ([clay.com](https://www.clay.com)) |

**Estimated cost for this level: Free** (all within free tiers; Clay only needed if re-running partner research)

## Drills Referenced

- `posthog-gtm-events` — set up event tracking for co-marketing attribution
- `newsletter-shoutout-copy` — write and deliver tracked blurbs per partner
- `warm-intro-request` — get introductions to partners you lack a direct relationship with
