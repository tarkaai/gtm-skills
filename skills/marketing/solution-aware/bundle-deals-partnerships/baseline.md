---
name: bundle-deals-partnerships-baseline
description: >
  Bundle Deal Partnerships — Baseline Run. Scale to 3-5 active bundles with
  always-on tracking, automated partner attribution, and systematic deal
  management to prove the bundle channel sustains pipeline over 8 weeks.
stage: "Marketing > Solution Aware"
motion: "Partnerships & Warm Intros"
channels: "Other"
level: "Baseline Run"
time: "20 hours over 8 weeks"
outcome: "≥3 active bundles and ≥15 bundle deals closed in 8 weeks"
kpis: ["Bundle deals per partner", "Page-to-deal conversion rate", "Revenue per bundle", "Partner promotional effort"]
slug: "bundle-deals-partnerships"
install: "npx gtm-skills add marketing/solution-aware/bundle-deals-partnerships"
drills:
  - bundle-deal-structuring
  - posthog-gtm-events
  - warm-intro-request
---

# Bundle Deal Partnerships — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Other

## Outcomes

3-5 active product bundles live simultaneously, each with its own co-branded landing page, tracking, and deal pipeline. Always-on PostHog event tracking captures the full bundle funnel (page view → tier selection → checkout → deal completed) with per-partner attribution. At least 15 bundle deals close across all partners in 8 weeks, proving that the bundle channel generates sustained pipeline — not just a one-time spike from launch promotion.

## Leading Indicators

- 2nd and 3rd partners agree to bundle terms within 2 weeks of pitch (signal: your bundle template and pitch are replicable)
- Each new bundle landing page receives >30 unique visitors in its first week (signal: partners are promoting without heavy prodding)
- At least 2 of the 3+ bundles generate deals independently (signal: success is not dependent on a single partner)
- Repeat purchases or upgrades from bundle customers (signal: bundle customers are real, retaining users — not just discount seekers)
- Traffic from partner channels constitutes >30% of total bundle page views (signal: the partnership is bidirectional, not you doing all the promotion)
- Tier distribution across bundles shows purchases at multiple tiers (signal: the pricing model works at different price points)

## Instructions

### 1. Standardize the bundle event taxonomy

Run the `posthog-gtm-events` drill to establish a consistent event schema across all bundles:

- `bundle_page_viewed` — properties: `partner_slug`, `bundle_id`, `utm_source`, `utm_medium`, `utm_campaign`
- `bundle_tier_selected` — properties: `partner_slug`, `bundle_id`, `tier_name`, `tier_price`
- `bundle_cta_clicked` — properties: `partner_slug`, `bundle_id`, `tier_name`
- `bundle_checkout_started` — properties: `partner_slug`, `bundle_id`, `tier_name`, `deal_value`
- `bundle_deal_completed` — properties: `partner_slug`, `bundle_id`, `tier_name`, `deal_value`, `attribution_source` (your channel vs. partner's channel)
- `bundle_deal_churned` — properties: `partner_slug`, `bundle_id`, `tier_name`, `months_active`, `churn_reason`

This taxonomy must be identical across all bundle landing pages so aggregate reporting works.

### 2. Launch 2-4 additional bundles

Using the validated process from Smoke, run the `bundle-deal-structuring` drill for each new partner. Improvements over Smoke:

- **Templatize the landing page**: Clone the Smoke-level landing page and swap partner branding, pricing, and copy. Each new page should take <2 hours to build, not 4+.
- **Templatize the pricing model**: Start from the Smoke-level pricing structure and adjust per partner. Keep the same tier names (Starter, Growth, Scale) across bundles for consistency.
- **Templatize the pitch**: Create a standard bundle proposal deck or one-pager that you customize per partner. Include Smoke-level results as proof ("Our first bundle generated X deals in 4 weeks").

Prioritize partners from different segments so you test bundle appeal across your ICP. If Smoke succeeded with a dev tools partner, try a marketing tools partner or a data platform partner.

### 3. Build warm intro paths for high-value bundle prospects

Run the `warm-intro-request` drill to source introductions to partnership leads at target companies. For bundle deals, the best intro path is often:

- A shared customer who uses both products and can vouch for the combined value
- A shared investor or advisor who knows both founding teams
- A conference connection where you met the partner's BD or marketing lead

Warm intros accelerate the pitch-to-agreement cycle. Cold outreach to partnership teams at larger companies typically takes 4-8 weeks; warm intros can cut this to 1-2 weeks.

### 4. Manage the bundle portfolio in Attio

Maintain the Bundles pipeline in Attio with all active bundles tracked:

- Each bundle has a deal record with: partner name, launch date, tier structure, revenue split, current status, total deals closed, total revenue, and next review date
- Weekly update: pull PostHog data for each bundle and update the deal record with latest metrics
- Flag bundles with zero deals in 2+ weeks as "At Risk" — investigate whether the partner stopped promoting or the landing page has issues
- Flag bundles with strong performance (>5 deals in a week) as "Expand" candidates — explore deeper integration, joint webinars, or exclusive bundle tiers

### 5. Coordinate ongoing promotion with partners

For each active bundle, maintain a promotion cadence:

- **Week 1 (launch)**: Both partners announce via email, social, and in-product messaging
- **Week 2-3**: Both partners include the bundle in their regular email newsletter or blog
- **Week 4**: Share early results with the partner ("We've generated X deals together — here's what's working")
- **Monthly**: Each partner re-promotes the bundle at least once per month. If a partner stops promoting, the bundle will decay — proactively share performance data to keep them motivated

**Human action required:** Monthly check-in call or async update with each partner to review metrics, share what is working, and plan next month's promotion.

### 6. Evaluate against threshold

Run the `threshold-engine` drill at week 8. Measure across all active bundles:

- Total bundle deals closed (target: ≥15)
- Number of active bundles generating deals (target: ≥3)
- Per-partner conversion rate (page views → deals)
- Revenue attribution: how much came from your promotion vs. partner promotion
- Bundle customer retention: are bundle customers staying beyond month 1?

**Pass threshold: ≥3 active bundles AND ≥15 bundle deals closed in 8 weeks**

- **Pass**: Document per-partner performance, identify the highest-converting bundle structures and promotion channels. Calculate the blended cost per bundle deal. Proceed to Scalable.
- **Marginal**: 2 active bundles or 10-14 deals. Investigate the underperforming bundles: pricing mismatch, partner not promoting, landing page conversion issues. Fix and extend by 4 weeks.
- **Fail**: <10 deals across all bundles. Diagnose: Is the discount compelling enough? Are partners actually promoting? Is the checkout flow creating friction? Are bundle customers the same people who would have bought standalone? If the channel is fundamentally weak for your ICP, consider pivoting to a different partnership format (integration partnerships, referral programs, co-webinars).

## Time Estimate

- Event taxonomy setup: 2 hours
- New bundle structuring (3-4 partners, ~3 hours each): 9-12 hours
- Warm intro sourcing for partner leads: 2 hours
- Portfolio management and partner coordination: 4 hours (spread over 8 weeks)
- Evaluation: 1 hour

Total: ~20 hours of active work over 8 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Partner research and enrichment for new bundles | Launch: $185/mo ([clay.com/pricing](https://www.clay.com/pricing)) |
| Attio | Bundle deal pipeline, partner CRM | Plus: $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Bundle funnel tracking, attribution | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Anthropic Claude | Pricing model generation for each new bundle | Sonnet 4: ~$0.10-0.50 per model ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| Webflow | Co-branded landing pages (3-5 pages) | Basic site: $18/mo ([webflow.com/pricing](https://webflow.com/pricing)) |
| Stripe | Bundle checkout | 2.9% + $0.30 per transaction ([stripe.com/pricing](https://stripe.com/pricing)) |

**Estimated cost for this level: ~$50-250/mo** (Attio Plus + Webflow required; other tools within free tiers at this volume)

## Drills Referenced

- `bundle-deal-structuring` — design pricing, build landing pages, and configure deal tracking for each new bundle partner
- `posthog-gtm-events` — establish the standard bundle event taxonomy across all landing pages
- `warm-intro-request` — source introductions to partnership leads at target companies to accelerate pitch-to-agreement
