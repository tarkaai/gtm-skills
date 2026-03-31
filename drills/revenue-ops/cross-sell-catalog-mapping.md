---
name: cross-sell-catalog-mapping
description: Analyze product usage data to map cross-sell product catalog to behavioral triggers, qualifying which products to recommend to which user segments
category: Revenue Ops
tools:
  - PostHog
  - Attio
fundamentals:
  - posthog-cohorts
  - posthog-funnels
  - posthog-custom-events
  - attio-custom-attributes
---

# Cross-Sell Catalog Mapping

This drill builds the foundation for any in-product cross-sell play by mapping your product catalog to behavioral triggers. It answers: which products should be recommended to which users, and what behavior signals that a user is ready for a second product?

Without this mapping, cross-sell surfaces are generic ("Try our other product!") instead of contextual ("You just hit 50 exports — our Analytics module turns these into dashboards automatically").

## Input

- A catalog of products, modules, or add-ons available for cross-sell (names, descriptions, pricing, entry points)
- PostHog tracking installed with at least 30 days of user-level usage data
- Attio with account-level product ownership data
- A list of users who adopted a second product (even if small — 10+ is enough for initial patterns)

## Steps

### 1. Build the adopter vs. non-adopter comparison

For each cross-sell product in your catalog, use the `posthog-cohorts` fundamental to create two cohorts:

- **Multi-product adopters**: Users who are active on their primary product AND have adopted this cross-sell product
- **Single-product users**: Users who are active on their primary product but have NOT adopted this cross-sell product

If you have fewer than 10 multi-product adopters for a given product, deprioritize that product for now — there is not enough signal to build a reliable trigger.

### 2. Identify behavioral predictors

For each product with sufficient adopters, compare the two cohorts across these dimensions using `posthog-funnels` and `posthog-custom-events`:

**Usage velocity:**
- How many sessions per week did adopters have before they adopted the second product?
- What features did adopters use most frequently in the 30 days before adoption?
- Were there specific workflows that adopters completed that non-adopters did not?

**Friction signals:**
- Did adopters hit a feature limit or gate before adopting?
- Did adopters use workarounds (e.g., exporting data manually, using integrations to bridge gaps)?
- Did adopters visit help docs or support related to the cross-sell product's domain?

**Temporal patterns:**
- How many days after signing up did adopters typically add the second product?
- Was there a usage milestone (e.g., 100th record, 50th export) that preceded adoption?
- Did adoption cluster around specific events (quarterly reviews, team growth)?

Output a raw signal table per product:

| Signal | Adopter Rate | Non-Adopter Rate | Lift | Confidence |
|--------|-------------|-----------------|------|------------|
| Used export 10+ times in 30 days | 78% | 12% | 6.5x | High |
| Visited integrations page 3+ times | 65% | 8% | 8.1x | High |
| Added 3+ team members | 52% | 22% | 2.4x | Medium |
| Created custom report | 44% | 15% | 2.9x | Medium |

### 3. Define trigger thresholds

For each product, select the 1-2 signals with the highest lift AND sufficient volume. A trigger with 10x lift but only 5 users is not usable. Set the threshold at the point where adopter behavior clearly diverges from non-adopter behavior.

Output a trigger map:

| Cross-Sell Product | Primary Trigger | Threshold | Secondary Trigger | Threshold | Timing Window |
|-------------------|----------------|-----------|-------------------|-----------|---------------|
| Analytics Module | Export count | 10+ exports in 30 days | Custom view creation | 5+ views in 14 days | After day 21 |
| API Access | Manual data transfers | 15+ in 30 days | Integration page visits | 3+ in 7 days | After day 30 |
| Team Plan | Shared items | 5+ shares with external emails | Teammate invitations | 2+ invites in 14 days | After day 14 |

### 4. Validate triggers against historical data

Using `posthog-funnels`, backtest each trigger:

1. Take the last 90 days of user data
2. Identify all users who crossed the trigger threshold during that period
3. Of those, what percentage adopted the cross-sell product within 30 days?
4. What percentage adopted within 60 days?

A good trigger converts at 10%+ within 30 days of firing. If conversion is below 5%, the trigger is too broad — tighten the threshold or add a secondary qualifier.

### 5. Store the catalog mapping in Attio

Using `attio-custom-attributes`, store the mapping at the account level:

- `cross_sell_eligible_products`: List of products this account qualifies for based on current usage
- `cross_sell_trigger_fired_{product}`: Boolean + timestamp for each product trigger
- `cross_sell_surface_shown_{product}`: Boolean + timestamp for when the discovery surface was displayed
- `cross_sell_adopted_{product}`: Boolean + timestamp for adoption

This creates the CRM foundation for all downstream cross-sell drills — discovery surfaces read eligibility from Attio, and health monitors query adoption status.

### 6. Prioritize the catalog for deployment order

Rank cross-sell products by expected impact:

Score = (trigger conversion rate) x (product revenue) x (eligible user volume)

Deploy discovery surfaces in this order. Start with the single highest-scoring product at Smoke level. Add the next 2-3 at Baseline. Cover the full catalog at Scalable.

## Output

- Adopter vs. non-adopter behavioral comparison per cross-sell product
- Validated trigger map with thresholds and timing windows
- Backtested conversion rates for each trigger
- Attio custom attributes for cross-sell tracking
- Prioritized deployment order

## Triggers

Run once during play setup. Re-run quarterly or when adding new products to the cross-sell catalog. Re-run immediately if trigger conversion rates drop below 5% (signals a market or product change).
