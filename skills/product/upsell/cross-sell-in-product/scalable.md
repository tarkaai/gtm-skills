---
name: cross-sell-in-product-scalable
description: >
  Related Product Cross-Sell — Scalable Automation. Expand cross-sell surfaces to the
  full product catalog with segment-specific messaging, A/B testing across surface types,
  and multi-product coordination that prevents fatigue at scale.
stage: "Product > Upsell"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Scalable Automation"
time: "50 hours over 2 months"
outcome: ">=10% cross-sell activation rate sustained across 4+ products with 500+ triggered users/month"
kpis: ["Cross-sell activation rate by product", "ARPU lift (cross-sell adopters vs. single-product)", "Cross-sell revenue as % of total expansion revenue", "Fatigue score trend", "Surface variant win rate"]
slug: "cross-sell-in-product"
install: "npx gtm-skills add product/upsell/cross-sell-in-product"
drills:
  - ab-test-orchestrator
---

# Related Product Cross-Sell — Scalable Automation

> **Stage:** Product → Upsell | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

Cross-sell surfaces deployed for 4+ products across the full catalog. Segment-specific messaging delivers the right product to the right user with the right message. Multi-product coordination prevents fatigue. Cross-sell activation rate sustained at >=10% with 500+ triggered users per month. A/B testing systematically improves conversion at every funnel stage.

## Leading Indicators

- Monthly triggered user volume reaches 500+ across all products
- No single product's dismissal rate exceeds 40% for more than 7 consecutive days
- A/B tests produce at least 1 statistically significant winner per month
- Email channel drives >=20% of total cross-sell activations (proving multi-channel value)
- Sales-assisted expansion deals from cross-sell signals close at >=30% rate
- ARPU for multi-product users is >=40% higher than single-product users

## Instructions

### 1. Scale across the product catalog

Run the the cross sell segment scaling workflow (see instructions below) drill. This is the core work of the Scalable level. Specifically:

- Complete Step 1: Expand discovery surfaces to the next 3-5 products from the prioritized catalog. For each product, build 2 surface variants (contextual tooltip + page banner) with PostHog feature flags for A/B testing.
- Complete Step 2: Build segment-specific messaging. Write different copy for each combination of plan tier (free/paid/enterprise), usage maturity (new/power), and role (admin/individual). Target via PostHog cohorts.
- Complete Step 3: Deploy the email fallback channel. Build the 2-email cross-sell sequence in Loops for users who see but do not engage with in-app surfaces. Wire the suppression logic in n8n.
- Complete Step 4: Build the multi-product coordination layer. When a user qualifies for multiple products, the n8n priority workflow ranks by (trigger strength x product revenue x recency) and shows only the top product per session.
- Complete Step 5: Deploy the fatigue management system. Track per-user and per-product fatigue scores. Auto-suppress surfaces when fatigue thresholds are crossed.
- Complete Step 6: Scale the sales handoff. Auto-create Attio expansion deals for high-value opportunities with full context.

### 2. Run systematic A/B tests

Run the `ab-test-orchestrator` drill on each major lever:

**Test 1 — Surface type:** Tooltip vs. banner vs. inline card for the same product. Measure impression-to-click conversion. Run for 2 weeks or until 200+ impressions per variant.

**Test 2 — Messaging angle:** Benefit-led ("Save 5 hours/week with Analytics") vs. behavior-led ("You exported 47 reports — Analytics turns these into dashboards") vs. social-proof ("Teams like yours use Analytics to..."). Measure click-to-activation conversion.

**Test 3 — Timing:** Show at trigger moment vs. 24 hours after trigger vs. next session after trigger. Measure activation rate (not just CTR — timing affects quality of engagement).

**Test 4 — Email sequence:** 1-email vs. 2-email cross-sell sequence. Measure incremental activations from email channel.

Run one test at a time per product. Implement winners before starting the next test. Document every result in Attio.

### 3. Monitor and maintain

Build a weekly review cadence (no new drill needed — use the PostHog dashboard from Baseline):

- Check each product's cross-sell funnel conversion: impression -> click -> activation start -> activated
- Identify products where conversion is declining (trigger may need recalibration)
- Check fatigue metrics: are dismissal rates trending up for any product?
- Review sales handoff results: are expansion deals closing?
- Calculate total monthly cross-sell revenue and ARPU lift

### 4. Evaluate against threshold

Measure after 2 months: >=10% cross-sell activation rate sustained across 4+ products with 500+ triggered users per month. If PASS, proceed to Durable. If FAIL, diagnose:

- Activation rate below 10% on 1-2 products: Those products may have weaker product-market fit for cross-sell. Consider tightening triggers or improving those products' first-use experience.
- Volume below 500 triggered users: Trigger thresholds are too tight. Lower the thresholds for the highest-converting products (if historical data supports it) or expand the user base.
- Activation rate declining over the 2 months: Fatigue management may be insufficient. Increase suppression durations or reduce surface frequency.

## Time Estimate

- 16 hours: Build discovery surfaces for 3-5 additional products with segment messaging
- 8 hours: Build multi-product coordination and fatigue management in n8n
- 12 hours: Run 4 A/B tests (3 hours each: setup, monitor, analyze, implement)
- 8 hours: Build email fallback sequences and suppression logic
- 6 hours: Weekly monitoring and optimization over 2 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, feature flags, experiments, cohorts | Free up to 1M events/mo; paid from $0.00031/event — https://posthog.com/pricing |
| Intercom | In-app messages, product tours, tooltips | From $39/seat/mo — https://www.intercom.com/pricing |
| Loops | Cross-sell email sequences with suppression | Free up to 1,000 contacts; from $49/mo — https://loops.so/pricing |
| n8n | Trigger detection, multi-product coordination, fatigue management | Free self-hosted / from $20/mo cloud — https://n8n.io/pricing |
| Attio | Cross-sell tracking, expansion deals, result logging | From $29/seat/mo — https://attio.com/pricing |

## Drills Referenced

- the cross sell segment scaling workflow (see instructions below) — expands cross-sell across the full product catalog with segment messaging, multi-product coordination, and fatigue management
- `ab-test-orchestrator` — designs, runs, and analyzes A/B tests on surface type, messaging, timing, and email sequences
