---
name: list-swaps-adjacent-startups-baseline
description: >
  List Swap With Partner — Baseline Run. Run list swaps with 3-5 partners over
  2 weeks with proper event tracking and per-partner attribution to validate
  repeatability across different audiences before automating.
stage: "Marketing > Solution Aware"
motion: "Partnerships & Warm Intros"
channels: "Email"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 80 clicks and ≥ 2 meetings over 2 weeks"
kpis: ["Click-through rate", "Email open rate", "Click-to-meeting rate", "Reciprocity ratio"]
slug: "list-swaps-adjacent-startups"
install: "npx gtm-skills add marketing/solution-aware/list-swaps-adjacent-startups"
drills:
  - posthog-gtm-events
  - list-swap-email-copy
  - warm-intro-request
---

# List Swap With Partner — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Email

## Outcomes

List swaps completed with 3-5 different adjacent startup partners over 2 weeks. At least 80 total clicks and 2 meetings across all swaps. This level proves the channel is repeatable across multiple partners with different audiences, not a one-off win from a single lucky pairing. It also establishes per-partner performance baselines and identifies which partner types and email variants drive the most meetings.

## Leading Indicators

- 3+ partners agree to swap within the first week (signal: the pitch template works across different companies)
- Per-partner click volume is consistent (within ±40%) across partners of similar list size (signal: results are not partner-dependent flukes)
- At least 2 different email variants produce clicks above the median (signal: the channel works beyond one lucky angle)
- Click-to-meeting conversion rate holds above 3% across partners (signal: traffic quality is real)
- Unsubscribe rate on inbound swaps stays below 0.3% across all partners (signal: your list tolerates swap content at this frequency)
- At least 1 partner proactively proposes a second swap (signal: the exchange felt valuable to them)

## Instructions

### 1. Set up event tracking

Run the `posthog-gtm-events` drill to configure a standardized event taxonomy for this play. Create these PostHog events:

- `list_swap_partner_contacted` — fired when outreach is sent to a partner
- `list_swap_agreed` — fired when a partner agrees to a swap
- `list_swap_email_sent` — fired when the partner sends your email to their list
- `list_swap_reciprocal_sent` — fired when you send the partner's email to your list
- `list_swap_click` — fired when a swap-sourced visitor takes the landing page CTA
- `list_swap_meeting_booked` — fired when a swap-sourced click converts to a meeting

Set standard properties on each event: `partner_slug`, `email_variant`, `swap_date`, `partner_list_size_estimate`.

### 2. Expand partner outreach

Using the partner list from Smoke (or run `partner-prospect-research` again with a larger scope of 15-20 candidates), reach out to 8-10 partners. For partners where you lack a direct relationship, run the `warm-intro-request` drill to map mutual connections and request introductions.

For each partner outreach:
- Personalize the pitch based on their specific audience and product
- Reference the Smoke test results: "We ran a test swap with [similar partner type] and saw [X clicks, Y meetings]"
- Propose a specific swap date within the next 2 weeks
- Share your email draft upfront to lower the commitment barrier
- Log every outreach attempt in Attio with the `list_swap_partner_contacted` event

**Human action required:** Send the outreach messages. Swap pitches work better coming from a founder or head of marketing, not a cold automation.

### 3. Write and deliver swap emails for each confirmed partner

For each partner that confirms, run the `list-swap-email-copy` drill:

- Tailor each swap email to the specific partner's audience persona and tone
- Use different email variants across partners to test which angles perform best
- Tag each email with a unique `utm_content` parameter (e.g., `curiosity-v1`, `data-v2`, `story-v1`)
- Track which variant goes to which partner and their list size estimate
- Review each partner's reciprocal email before scheduling it to your list

### 4. Stagger swap execution

Do not run all 3-5 swaps in the same week. Stagger them across 2 weeks:
- Week 1: 2 swaps (Tuesday and Thursday)
- Week 2: 1-3 swaps (staggered across the week)

This prevents your own list from receiving too many inbound swap emails in a short period (which would spike unsubscribes) and gives you time to learn from early swaps before executing later ones.

### 5. Monitor per-partner performance

After each swap, track in PostHog:
- Clicks per partner (`utm_source` breakdown where `utm_medium=list-swap`)
- Meetings per partner
- Click velocity (how fast clicks arrive after the partner sends)
- Email variant performance (`utm_content` breakdown)
- Reciprocal performance (how your list responded to each partner's email: opens, clicks, unsubscribes)

Build a PostHog insight: bar chart of clicks grouped by `utm_source`, filtered to `utm_campaign=list-swaps-adjacent-startups`.

### 6. Identify top-performing patterns

After all swaps have run (7+ days after the last swap), analyze:

- **Per-partner efficiency**: Which partners drove the most clicks per estimated list subscriber? This is your partner-level efficiency metric.
- **Email variant winners**: Which variants (curiosity, data, story) drove the highest CTR and click-to-meeting rate?
- **Audience fit patterns**: Do partners in certain verticals or company stages convert better?
- **Reciprocity balance**: For each partner, calculate net swap value (clicks you received minus clicks they received from your list). Flag any imbalanced swaps for renegotiation.
- **Zero-performers**: Did any swaps generate <5 clicks? Diagnose: wrong audience, bad email, disengaged list, or wrong send time?

### 7. Evaluate against threshold

Measure aggregate results across all swaps:

**Pass threshold: >= 80 clicks AND >= 2 meetings over 2 weeks**

- **Pass**: Document per-partner performance, top email variants, click-to-meeting rates, and reciprocity balances. Rank partners by efficiency. Identify the 2-3 partner archetypes that work best. Proceed to Scalable.
- **Marginal**: 50-79 clicks or 1 meeting. Investigate which partners underperformed and whether better email copy, different landing pages, or a different partner profile would close the gap. Run one more week with 2 additional partners.
- **Fail**: <50 clicks across all swaps. Diagnose: Are your partners' audiences truly solution-aware? Are the swap emails too generic? Is the landing page converting? Consider: the list swap model may not fit your category if partner audiences consistently do not respond.

## Time Estimate

- Event tracking setup: 1 hour
- Partner outreach (8-10 partners): 3 hours
- Swap email writing (3-5 variants): 3 hours
- Partner communication, approval, and reciprocal review: 2 hours
- Swap execution and send coordination: 1 hour
- Monitoring and analysis: 1.5 hours
- Final evaluation: 0.5 hours

Total: ~12 hours of active work over 2 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking and per-partner analytics | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | Partner CRM and swap tracking | Free for up to 3 users; Plus: $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Anthropic Claude | Swap email copywriting (3-5 variants) | Sonnet 4.6: ~$0.50-2.00 total ([platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing)) |
| Clay | Partner enrichment (if re-running research) | Launch: $185/mo ([clay.com/pricing](https://www.clay.com/pricing)) |
| Loops | Send partner swap emails to your list | Free up to 1K contacts; paid from $49/mo ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated cost for this level: Free** (all within free tiers for 3-5 swaps; Clay only needed if re-running partner research)

## Drills Referenced

- `posthog-gtm-events` — set up event tracking for list swap attribution
- `list-swap-email-copy` — write and deliver tracked swap emails per partner
- `warm-intro-request` — get introductions to partners you lack a direct relationship with
