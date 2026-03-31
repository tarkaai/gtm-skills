---
name: bundle-deals-partnerships-smoke
description: >
  Bundle Deal Partnerships — Smoke Test. Structure and launch one co-branded
  product bundle with one complementary partner to validate that bundled pricing
  generates deals before investing in a multi-partner bundle program.
stage: "Marketing > Solution Aware"
motion: "Partnerships & Warm Intros"
channels: "Other"
level: "Smoke Test"
time: "8 hours over 2 weeks"
outcome: "≥1 live bundle with ≥3 bundle deals closed in 4 weeks"
kpis: ["Bundle page-to-deal conversion rate", "Bundle deal count", "Partner response rate"]
slug: "bundle-deals-partnerships"
install: "npx gtm-skills add marketing/solution-aware/bundle-deals-partnerships"
drills:
  - partner-prospect-research
  - threshold-engine
---

# Bundle Deal Partnerships — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Other

## Outcomes

One co-branded product bundle live with one complementary partner. A landing page shows the bundled offer with clear pricing (15-25% discount vs. buying separately), and both partners actively promote it to their audiences. At least 3 bundle deals close within 4 weeks of launch. This proves that customers in the shared ICP value the combined offer enough to purchase through a bundle rather than buying each product independently, and that the partner is motivated to promote it.

## Leading Indicators

- Partner responds to bundle pitch within 5 days (signal: bundling resonates as a growth lever for them)
- Partner agrees to a pricing structure without requiring >3 negotiation rounds (signal: the value split is fair)
- Bundle landing page receives >50 unique visitors in the first 2 weeks (signal: at least one partner is actively promoting)
- At least 1 visitor selects a tier above the lowest (signal: the pricing tiers are differentiated and the higher tiers have perceived value)
- First bundle deal closes within 14 days of page going live (signal: the offer converts, not just attracts)
- Neither partner's existing customer base complains about the bundle undercutting their standalone pricing (signal: the discount is positioned as additive value, not a price cut)

## Instructions

### 1. Identify and select one bundle partner

Run the `partner-prospect-research` drill with bundle-specific criteria. Instead of scoring on newsletter quality (as in list swaps), score on:

- **Product complementarity**: Does their product solve an adjacent problem for the same buyer? Example: if you sell data pipelines, partner with a BI tool, not another ETL product. The bundle must be "better together," not "either/or."
- **ICP overlap**: Do they sell to the same company size, industry, and buyer persona? The more overlap, the more natural the bundle feels to the customer.
- **Pricing compatibility**: Are their plans in a similar price range? A $29/mo product bundling with a $500/mo enterprise tool creates an awkward value imbalance.
- **Integration potential**: Do your products actually work together (or could they)? A bundle is more compelling when the products integrate, even if it is just "use both and get a discount."
- **Partnership willingness**: Have they done bundles, integrations, or co-marketing before? Check their website for existing partner pages, integration directories, or co-branded content.

Select the single best candidate. Prioritize partners where you have an existing relationship.

### 2. Structure the bundle deal

Run the the bundle deal structuring workflow (see instructions below) drill to:

- Research the partner's pricing and identify which plan combinations make sense
- Generate a 3-tier bundle pricing model (Starter, Growth, Scale) with 15-25% discount off combined list price
- Propose a revenue split (default: proportional to each product's list price)
- Build a co-branded landing page at `{your_domain}/bundles/{partner-slug}` with PostHog tracking
- Configure Attio to track bundle deals in a dedicated pipeline

**Human action required:** Present the bundle proposal to the partner. Walk them through the pricing, revenue split, and landing page mockup. Negotiate adjustments. Get written agreement on:
- Final pricing for each tier
- Revenue split percentage
- Which channels each partner will promote through
- Launch date
- Review date (4 weeks after launch)

### 3. Launch and promote the bundle

Once the partner approves:
- Publish the co-branded landing page
- Both partners share the bundle URL through their primary channels:
  - Email to existing customers and prospects who use only one of the two products
  - In-product notification or banner for existing users
  - Social media announcement
  - Sales team briefing: arm your reps with the bundle pitch for deals in progress
- Each partner uses their UTM-tagged URL so attribution is clean

**Human action required:** Coordinate launch timing with the partner. Both partners should begin promotion within the same week. Monitor the first 48 hours for any landing page issues, broken tracking, or customer confusion.

### 4. Monitor and assist deal closing

For 4 weeks after launch:
- Check PostHog daily for `bundle_page_viewed` and `bundle_deal_completed` events
- If visitors view the page but do not complete checkout, investigate: is the pricing unclear? Is the CTA too high-commitment? Is the checkout flow broken?
- If visitors select tiers but abandon, check if the checkout page loads correctly and if the payment flow works for both products
- Log every closed bundle deal in Attio with: partner name, tier selected, deal value, attribution source (your channel or partner's)

### 5. Evaluate against threshold

Run the `threshold-engine` drill 4 weeks after launch. Measure:

- Bundle deals closed (target: ≥3)
- Bundle page conversion rate (page views → completed deals)
- Traffic attribution (how much did each partner contribute?)
- Revenue generated and split accuracy

**Pass threshold: ≥1 live bundle AND ≥3 bundle deals closed in 4 weeks**

- **Pass**: Document which tier was most popular, which promotion channel drove the most traffic, and whether the partner was an active promoter. Note the conversion rate as the baseline for future bundles. Proceed to Baseline.
- **Marginal**: 1-2 deals closed, or good traffic but low conversion. Diagnose: Is the pricing too high? Is the landing page unclear? Is one partner not promoting? Adjust the weakest variable and extend the test by 2 weeks.
- **Fail**: 0 deals and <30 page views. The bundle concept may not resonate with this partner's audience, or the partner is not promoting. Try a different partner or a different bundle structure (e.g., free trial bundle instead of paid bundle).

## Time Estimate

- Partner research and selection: 2 hours
- Bundle pricing model generation and refinement: 1 hour
- Partner outreach and negotiation: 1 hour (human action)
- Landing page setup and tracking: 2 hours
- Launch coordination: 30 minutes
- Monitoring and evaluation (over 4 weeks): 1.5 hours

Total: ~8 hours of active work over 2 weeks setup + 4 weeks evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Partner research and enrichment | Launch: $185/mo ([clay.com/pricing](https://www.clay.com/pricing)) |
| Attio | Partner CRM and bundle deal tracking | Free for up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Bundle page tracking, funnel analytics | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Anthropic Claude | Bundle pricing model generation | Sonnet 4: $3/$15 per MTok; ~$0.10-0.50 per model ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| Webflow | Co-branded landing page | Starter: Free; Basic site: $18/mo ([webflow.com/pricing](https://webflow.com/pricing)) |
| Stripe | Bundle checkout (if self-serve) | 2.9% + $0.30 per transaction ([stripe.com/pricing](https://stripe.com/pricing)) |

**Estimated cost for this level: Free** (all tools within free tiers for a single bundle test)

## Drills Referenced

- `partner-prospect-research` — find and score complementary partners whose products and audiences overlap your ICP
- the bundle deal structuring workflow (see instructions below) — design pricing tiers, build the co-branded landing page, and configure deal tracking
- `threshold-engine` — evaluate bundle deals closed against the pass threshold
