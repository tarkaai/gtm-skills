---
name: partner-marketplace-listings-baseline
description: >
  Partner Marketplace Listings — Baseline Run. Optimize existing listings, build
  review velocity, configure full-funnel tracking, and run the channel always-on
  with automated review management and lead routing.
stage: "Marketing > SolutionAware"
motion: "DirectoriesMarketplaces"
channels: "Other"
level: "Baseline Run"
time: "20 hours setup + 2 hours/week ongoing"
outcome: ">=3 live marketplace listings, >=20 marketplace-sourced signups/month, and avg rating >=4.0 after 8 weeks"
kpis: ["Installs per marketplace per week", "Install-to-signup conversion rate", "Review count per marketplace", "Average rating per marketplace", "Marketplace-sourced MRR"]
slug: "partner-marketplace-listings"
install: "npx gtm-skills add marketing/solution-aware/partner-marketplace-listings"
drills:
  - posthog-gtm-events
  - partner-marketplace-review-generation
  - partner-marketplace-listing-setup
---

# Partner Marketplace Listings — Baseline Run

> **Stage:** Marketing > SolutionAware | **Motion:** DirectoriesMarketplaces | **Channels:** Other

## Outcomes

First always-on automation. The agent runs the review generation cadence continuously, tracks full-funnel conversion from marketplace view to paid customer, and maintains listing quality across 3+ marketplaces. The goal is to prove that partner marketplace listings are a sustainable, repeatable lead source -- not a one-time spike.

**Pass threshold:** >=3 live marketplace listings, >=20 marketplace-sourced signups/month, and avg rating >=4.0 after 8 weeks.

## Leading Indicators

- Full-funnel PostHog tracking live within the first week (marketplace visit -> signup -> activation -> paid)
- Review request cadence producing 2+ new reviews per marketplace per month
- All reviews responded to within 48 hours
- Listing descriptions updated with keywords from actual marketplace search data
- At least 2 of 3 marketplaces generating consistent weekly installs (not one-off spikes)

## Instructions

### 1. Configure full-funnel tracking

Run the `posthog-gtm-events` drill to instrument the complete marketplace-to-revenue funnel:

| Event | Trigger | Properties |
|-------|---------|-----------|
| `partner_marketplace_visit` | UTM-tagged site visit from a partner marketplace | `marketplace`, `listing_slug`, `utm_campaign`, `landing_page` |
| `partner_marketplace_signup` | Trial start or signup from marketplace-sourced session | `marketplace`, `listing_slug`, `signup_type` |
| `partner_marketplace_activation` | User connects the partner integration | `marketplace`, `listing_slug`, `integration_type`, `time_to_connect_hours` |
| `partner_marketplace_conversion` | Marketplace-sourced user converts to paid | `marketplace`, `listing_slug`, `plan`, `mrr` |

Create a PostHog funnel: `partner_marketplace_visit -> partner_marketplace_signup -> partner_marketplace_activation -> partner_marketplace_conversion`. Break down by `marketplace` property.

Set up a PostHog dashboard with:
- Weekly installs trend (stacked by marketplace)
- Weekly signups from marketplace sources
- Conversion rates at each funnel stage
- Current review count and rating per marketplace

### 2. Expand to 3+ marketplace listings

Run the `partner-marketplace-listing-setup` drill to add 1-2 more marketplace listings beyond the Smoke test listing(s). Apply lessons from the Smoke test:

- Which keywords drove the most impressions? Use them in the new listings.
- What listing format converted best? Mirror that structure.
- Which marketplace had the best install-to-signup ratio? Prioritize expanding to marketplaces with similar buyer intent characteristics.

### 3. Launch the review generation system

Run the `partner-marketplace-review-generation` drill to build a systematic review pipeline:

1. Build review candidate lists in Attio (customers using each specific integration, 30+ days tenure, no recent review ask)
2. Create the 2-touch review request email sequence in Loops
3. Set up the n8n workflow for weekly automated review candidate selection and enrollment
4. Configure daily review monitoring via the marketplace review APIs
5. Set up review response templates and Slack alerts for negative reviews

**Target:** 2-4 new reviews per marketplace per month. Respond to all reviews within 48 hours.

### 4. Optimize listing content based on data

After 4 weeks of Baseline tracking data:

1. Pull PostHog data: which marketplaces drive the most signups? Which have the highest conversion rate?
2. For underperforming listings, analyze: is the problem visibility (low views/installs) or conversion (installs happen but signups don't)?

**If visibility is low (few marketplace views):**
- Update the listing title with higher-volume keywords
- Add more tags/categories
- Update screenshots to show the highest-value integration workflow (the one that appears most in positive reviews and sales calls)
- Ensure the listing appears in the correct marketplace category

**If conversion is low (installs happen but users don't sign up):**
- Review the landing page: does it match what marketplace users expect?
- Simplify the signup/trial flow for marketplace-sourced users
- Add marketplace-specific social proof to the landing page ("Rated 4.8 on {Marketplace}")
- Check if the integration setup experience is smooth (high friction = abandonment)

Log every listing change in Attio with: date, what changed, hypothesis, expected impact.

### 5. Build marketplace-specific lead routing

Configure n8n to detect marketplace-sourced signups and route them appropriately:

1. When `partner_marketplace_signup` fires with `marketplace` property set:
2. Create/update the contact in Attio with `acquisition_source = "partner-marketplace"` and `acquisition_marketplace = "{marketplace}"`
3. Tag in Loops for marketplace-specific onboarding (e.g., "HubSpot integration setup guide" vs generic onboarding)
4. If the marketplace indicates enterprise intent (e.g., Salesforce AppExchange): alert sales for follow-up

### 6. Evaluate against threshold

After 8 weeks, measure:
- **>=3 live listings:** Count listings with "live" status in Attio
- **>=20 marketplace-sourced signups/month:** PostHog funnel data for the most recent 30 days
- **avg rating >=4.0:** Check rating on each marketplace

If PASS, proceed to Scalable. If FAIL, focus investment on the 1-2 marketplaces with the best conversion rate and improve listing quality + review volume before expanding further.

## Time Estimate

- 8 hours: Full-funnel PostHog tracking setup and dashboard creation
- 4 hours: New marketplace listing creation (1-2 additional marketplaces)
- 4 hours: Review generation system setup (Loops sequence, n8n workflow, monitoring)
- 2 hours: Lead routing configuration
- 2 hours: Initial listing optimization pass
- Ongoing: ~2 hours/week for review management, listing updates, and performance monitoring

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Full-funnel conversion tracking and dashboards | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | CRM for listing tracking and lead routing | Free for small teams; Plus $34/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Loops | Review request email sequences | Starter $49/mo for up to 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Automated review cadence and lead routing | Starter $24/mo self-hosted; Cloud from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Clay | Keyword research for listing optimization | Launch plan $185/mo ([clay.com/pricing](https://clay.com/pricing)) |
| Partner marketplaces | Listings on 3+ platforms | $0-19 (see Smoke level for per-marketplace costs) |

**Estimated monthly cost at this level:** ~$50-150/mo (Loops + n8n; Clay usage can be periodic; marketplace listings are free)

## Drills Referenced

- `posthog-gtm-events` -- instruments the full marketplace-to-revenue funnel in PostHog
- `partner-marketplace-review-generation` -- builds the systematic review request and response workflow
- `partner-marketplace-listing-setup` -- creates additional marketplace listings with optimized copy
