---
name: podcast-sponsorships-b2b-scalable
description: >
  B2B Podcast Sponsorships — Scalable Automation. Scale to 8-15 monthly podcast
  sponsorships with automated booking pipelines, performance monitoring, and
  systematic ad script optimization to hit 40+ leads per quarter.
stage: "Marketing > Problem Aware"
motion: "LightweightPaid"
channels: "Paid, Content"
level: "Scalable Automation"
time: "60 hours over 3 months"
outcome: "≥40 qualified leads per quarter with CPL at or below Baseline benchmark across 8-15 monthly sponsorships"
kpis: ["Monthly placement volume", "Qualified leads per quarter", "Blended CPL", "CPL trend (improving/stable/declining)", "Ad script win rate"]
slug: "podcast-sponsorships-b2b"
install: "npx gtm-skills add marketing/problem-aware/podcast-sponsorships-b2b"
drills:
  - podcast-sponsor-research
  - podcast-sponsor-booking
  - dashboard-builder
  - ab-test-orchestrator
---

# B2B Podcast Sponsorships — Scalable Automation

> **Stage:** Marketing → Problem Aware | **Motion:** LightweightPaid | **Channels:** Paid, Content

## Outcomes

Scale from 3-6 placements at Baseline to 8-15 monthly sponsorship placements across a portfolio of validated B2B podcasts. Automated performance monitoring and systematic ad script testing produce at least 40 qualified leads per quarter with CPL at or below the Baseline benchmark. The agent manages the booking pipeline, attribution tracking, and performance reporting with minimal human intervention.

## Leading Indicators

- 8+ placements booked per month across Tier 1 and Tier 2 podcasts (signal: pipeline is sustaining volume)
- New podcast prospects added quarterly via automated research refreshes (signal: pipeline is not stagnating)
- Ad script A/B tests producing a clear winner within each 4-placement cycle (signal: systematic optimization is working)
- CPL trend is flat or declining month-over-month at increased volume (signal: quality is holding at scale)
- At least 3 Tier 1 podcasts have been rebooked with consistent results (signal: durable relationships, not one-off wins)

## Instructions

### 1. Build the podcast portfolio

Run the `podcast-sponsor-research` drill at scale: evaluate 50+ candidate podcasts. Build a tiered portfolio:

- **Tier 1 — Monthly rebooking (5-8 shows)**: Podcasts that delivered CPL at or below target during Baseline. Book these on a recurring monthly cadence. Negotiate multi-episode packages for 15-20% discounts.
- **Tier 2 — Quarterly rotation (5-10 shows)**: Podcasts with acceptable CPL. Rotate through these to maintain audience freshness and test new segments.
- **Tier 3 — Test pipeline (ongoing)**: New podcasts identified via quarterly research refreshes. Test each with a single placement before promoting to Tier 1 or 2.

Set up an Attio list for each tier. Use the `podcast-sponsor-research` drill quarterly to refresh Tier 3 and identify new sponsorship opportunities.

### 2. Automate the booking pipeline

Build an n8n workflow (via the `podcast-sponsor-booking` drill at scale) that systematizes the recurring booking process:

1. **Monthly trigger (1st of month)**: Pull the Tier 1 podcast list from Attio. For each podcast, check if the next episode's ad slot is available.
2. **Auto-generate booking requests**: Draft booking emails for each Tier 1 podcast using the Anthropic API. Include: preferred episode date, confirmed rate (from package agreement), and reference to the previous placement.
3. **Queue for human approval**: Present all booking requests in a batch for review.
4. **On approval**: Send booking confirmations. Create Attio deal records. Generate unique UTM, vanity URL, and promo code for each placement.
5. **Script deadline trigger**: 7 days before each placement's script deadline, auto-generate 3 ad script variants and queue for review.

**Human action required:** Approve monthly booking batch. Review ad scripts. Process payments for non-marketplace placements.

### 3. Systematize ad script optimization

Run the `ab-test-orchestrator` drill adapted for podcast ad scripts:

- Maintain a library of tested ad script templates in Attio, tagged by: angle (problem/story/data), CTA type (vanity URL / promo code / both), duration (30s / 60s / 90s)
- For every new placement, generate 3 variants from the current top-performing template + 1 experimental variant
- Track which template + variant wins across placements
- After every 4 placements, update the template library: promote winners, retire underperformers

Optimization variables to test systematically:
- **Script angle**: problem-led vs. story-led vs. data-led
- **CTA format**: vanity URL only vs. promo code only vs. both
- **Read length**: 30s pre-roll vs. 60s mid-roll vs. 90s extended read
- **Offer type**: discount vs. extended trial vs. exclusive content
- **Show notes copy**: short (1 sentence) vs. detailed (3 sentences + bullet points)

### 4. Deploy automated performance monitoring

Run the `dashboard-builder` drill to set up always-on monitoring:

- PostHog dashboard: all placements, all signals, updated in real-time
- Automated 14-day post-placement performance collection via n8n
- Biweekly performance report with per-podcast CPL, script variant analysis, and rebooking recommendations
- Podcast scoring model updated with actual performance data
- Anomaly alerts: dead placements, exceptional performers, portfolio CPL drift

Use the performance data to continuously rebalance the portfolio: promote strong podcasts to Tier 1, demote underperformers to Tier 3, drop consistently poor performers entirely.

### 5. Scale budget with guardrails

Increase total monthly sponsorship spend by 20-30% per month as long as blended CPL stays within target:

- **Budget guardrail**: If blended CPL exceeds Baseline benchmark by 30% for 2 consecutive biweekly reports, pause new Tier 2/3 bookings and consolidate to Tier 1 only.
- **Volume guardrail**: Maximum 15 placements per month. Beyond this, individual attention per placement drops and quality suffers.
- **Diversity guardrail**: No single podcast should account for more than 25% of total monthly spend. Maintain portfolio diversification.
- **Freshness guardrail**: At least 2 new podcasts tested per month (from Tier 3 pipeline) to prevent portfolio stagnation.

### 6. Evaluate against threshold

Measure quarterly:

**Pass threshold: >= 40 qualified leads per quarter AND CPL at or below Baseline benchmark**

- **Pass**: CPL is stable or declining at 3x+ the Baseline volume. The podcast sponsorship channel is scalable. Proceed to Durable.
- **Marginal**: 25-39 leads or CPL 1-1.5x above Baseline. Continue optimizing for one more quarter before advancing.
- **Fail**: <25 leads or CPL above 1.5x Baseline at scale. The channel may have a natural ceiling. Consolidate to Tier 1 podcasts only and cap the budget.

## Time Estimate

- Quarterly podcast research refresh: 4 hours/quarter
- Monthly booking pipeline management: 6 hours/month (2 hours pipeline, 2 hours scripts, 2 hours monitoring)
- Ad script optimization analysis: 2 hours/month
- Biweekly performance review: 2 hours/month
- Portfolio rebalancing: 1 hour/month

Total: ~60 hours over 3 months (20 hours/month)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| AdvertiseCast / Podcorn / Gumball | Marketplace booking | Free for advertisers |
| ListenNotes | Directory search | $24/mo for 10,000 req/day ([listennotes.com/pricing](https://www.listennotes.com/api/pricing/)) |
| Clay | Publisher enrichment | Explorer: $385/mo ([clay.com/pricing](https://www.clay.com/pricing)) |
| Attio | CRM portfolio management | Plus: $34/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Multi-signal attribution | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Booking pipeline automation | Starter: $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Dub.co | Vanity URL management | Pro: $24/mo ([dub.co/pricing](https://dub.co/pricing)) |
| Anthropic Claude | Script generation + analysis | ~$5-20/mo at this volume ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| Podcast placements (8-15/mo) | Paid sponsorships | $1,500-6,000/mo ($200-400 per placement at volume rates) |

**Estimated cost for this level: $2,000-7,000/mo** (primarily sponsorship placements; tools ~$200-500/mo)

## Drills Referenced

- `podcast-sponsor-research` — quarterly pipeline refresh, 50+ candidates evaluated
- `podcast-sponsor-booking` — systematized booking at 8-15 placements/month
- `dashboard-builder` — always-on monitoring, biweekly reports, podcast scoring model
- `ab-test-orchestrator` — systematic ad script optimization across placements
