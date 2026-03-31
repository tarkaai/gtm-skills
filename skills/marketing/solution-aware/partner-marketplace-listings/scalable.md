---
name: partner-marketplace-listings-scalable
description: >
  Partner Marketplace Listings — Scalable Automation. Expand to 5+ partner marketplaces
  with automated listing management, cross-marketplace performance comparison,
  marketplace-specific landing pages, and Zap/scenario template creation.
stage: "Marketing > SolutionAware"
motion: "DirectoriesMarketplaces"
channels: "Other"
level: "Scalable Automation"
time: "40 hours setup + 3 hours/week ongoing over 3 months"
outcome: ">=5 live marketplace listings, >=50 marketplace-sourced signups/month, and marketplace channel contributes >=5% of new MRR after 12 weeks"
kpis: ["Total installs across all marketplaces per week", "Marketplace-sourced signups per month", "Install-to-paid conversion rate per marketplace", "Marketplace-attributed MRR", "Review velocity (new reviews/month)", "Average rating across portfolio"]
slug: "partner-marketplace-listings"
install: "npx gtm-skills add marketing/solution-aware/partner-marketplace-listings"
drills:
  - partner-marketplace-scaling
  - partner-marketplace-review-generation
---

# Partner Marketplace Listings — Scalable Automation

> **Stage:** Marketing > SolutionAware | **Motion:** DirectoriesMarketplaces | **Channels:** Other

## Outcomes

Find the 10x multiplier. Each new partner marketplace listing is a new discovery surface reaching buyers already embedded in that ecosystem. The compounding effect: marketplace-specific landing pages convert 2-3x higher than generic pages, cross-marketplace review velocity improves ranking on every platform, and Zap/scenario templates on Zapier/Make create additional organic discovery channels. The agent manages the full portfolio and optimizes each listing independently.

**Pass threshold:** >=5 live marketplace listings, >=50 marketplace-sourced signups/month, and marketplace channel contributes >=5% of new MRR after 12 weeks.

## Leading Indicators

- 2+ new marketplace listings submitted per month during the expansion phase
- Marketplace-specific landing pages live for each listing within 1 week of approval
- Cross-marketplace conversion funnel data showing per-marketplace ROI within 4 weeks
- 10+ Zap/scenario templates published (if on Zapier/Make) within 6 weeks
- Review velocity maintaining 2-4 new reviews per marketplace per month
- At least 3 of 5+ marketplaces generating consistent weekly signups

## Instructions

### 1. Scale to 5+ partner marketplaces

Run the `partner-marketplace-scaling` drill to identify and execute the expansion plan:

1. Use Clay to research which partner ecosystems have the highest ICP overlap
2. Prioritize by: ICP concentration x marketplace traffic x inverse competition density x integration effort
3. Build or complete integrations for the next 3+ platforms
4. Submit listings using the optimized listing copy process established at Baseline
5. Target: submit 2 new listings per month until 5+ are live

**Marketplace expansion targets by typical B2B SaaS category:**

| Tier | Marketplaces | Why |
|------|-------------|-----|
| Tier 1 (high traffic, high intent) | Salesforce AppExchange, HubSpot App Marketplace, Shopify App Store | Large buyer bases actively searching for solutions |
| Tier 2 (automation ecosystems) | Zapier, Make (Integromat), Slack App Directory | Automation-minded users; Zap templates create passive discovery |
| Tier 3 (niche/vertical) | Microsoft AppSource, Atlassian Marketplace, Intercom App Store, Pipedrive Marketplace | Smaller but highly targeted audiences |

### 2. Build marketplace-specific landing pages

For each marketplace listing, create a dedicated landing page (from the `partner-marketplace-scaling` drill):

**Page template:**
1. Hero: "The Best {Category} Integration for {Platform Name}" -- mirror the search terms users typed on the marketplace
2. Integration-specific demo: screenshots and/or video showing the product working inside that specific partner platform
3. Feature list: capabilities unique to that platform's integration, not generic product features
4. Social proof: pull reviews and ratings from that specific marketplace listing
5. Primary CTA: "Start Free Trial" with hidden `utm_source={marketplace}` pass-through
6. Secondary CTA: "See on {Marketplace}" linking back to the listing (builds listing view count)

Track per-page conversion rate in PostHog. Compare: do marketplace-specific pages outperform the generic product page for marketplace-sourced traffic?

### 3. Create Zap and scenario templates

If listed on Zapier and/or Make, create 10+ pre-built automation templates:

1. Research the top trigger/action patterns in your category using Clay Claygent
2. Build templates covering the 5 most common automation workflows your integration supports
3. Create templates pairing your product with the 5 most popular complementary apps (e.g., "New {YourProduct} lead -> Create HubSpot contact -> Send Slack notification")
4. Write template titles using the format `{Primary Keyword} + {Platform Pair}` (e.g., "Sync CRM Contacts to Email: HubSpot + Loops")
5. Submit templates for Zapier/Make review

Zapier and Make rank integrations partly by available template count and template usage. Templates are a passive discovery channel that compounds over time.

### 4. Automate cross-marketplace listing management

Extend the n8n workflows from Baseline to manage the full portfolio:

**Weekly portfolio management workflow (n8n, Monday 8am):**
1. Pull analytics from all marketplace listings (views, installs, rating, rank)
2. Pull PostHog data for all marketplace-sourced signups and conversions
3. Calculate per-marketplace ROI: (marketplace-attributed MRR) / (time invested in that marketplace)
4. Compare all marketplaces: rank by install-to-paid conversion rate
5. Flag: marketplaces where rating dropped below 4.0, where installs declined >20% WoW, or where a new competitor entered the top 5
6. Update Attio records
7. Generate Slack summary

**Monthly listing refresh workflow (n8n, 1st of month):**
1. For each marketplace, check if listing copy is older than 90 days
2. If so, re-run keyword research and generate updated listing copy
3. Update screenshots if the product UI has changed
4. Queue updates for human submission

### 5. Scale the review generation system

Continue running the `partner-marketplace-review-generation` drill across all marketplaces:

- Rotate review requests across marketplaces (different marketplace each week)
- Increase candidate pool as customer base grows
- Track review conversion rate per marketplace -- some marketplaces have much higher review completion rates than others; allocate more requests to high-completion platforms
- Target: maintain 4.0+ average rating on every marketplace; generate 2-4 reviews per marketplace per month

### 6. Build the cross-marketplace attribution model

In PostHog, create a comprehensive attribution view:

**Cohort comparison:**
Create cohorts for each marketplace source. Compare at 30, 60, and 90 days:
- Activation rate (connected integration)
- Retention rate (still active)
- Paid conversion rate
- Average MRR per user
- LTV projection

This data determines where to invest more (high-LTV marketplaces) and where to reduce effort (low-LTV marketplaces).

### 7. Evaluate against threshold

After 12 weeks, measure:
- **>=5 live listings:** Count listings with "live" status in Attio
- **>=50 marketplace-sourced signups/month:** PostHog funnel data for the most recent 30 days
- **>=5% of new MRR from marketplace channel:** Compare marketplace-attributed MRR to total new MRR

If PASS, proceed to Durable. If FAIL, consolidate to the 3 highest-ROI marketplaces and double down on listing quality, review volume, and conversion optimization before expanding further.

## Time Estimate

- 15 hours: New marketplace listing creation and integration work (3+ new marketplaces)
- 8 hours: Marketplace-specific landing page creation
- 6 hours: Zap/scenario template creation (if on Zapier/Make)
- 5 hours: Cross-marketplace automation setup (n8n portfolio management)
- 3 hours: Attribution model and cohort analysis setup
- 3 hours: Review system expansion
- Ongoing: ~3 hours/week for portfolio monitoring, review management, and optimization

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Full-funnel tracking, cohorts, dashboards | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | CRM for portfolio tracking and lead routing | Plus $34/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Loops | Review request and onboarding sequences | Growth $99/mo for up to 20,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Portfolio management automation | Pro $50/mo for higher execution limits ([n8n.io/pricing](https://n8n.io/pricing)) |
| Clay | Marketplace research and competitive intel | Launch $185/mo or Growth $495/mo ([clay.com/pricing](https://clay.com/pricing)) |
| Zapier | Zap template creation (developer platform) | Free for public integration developers ([developer.zapier.com](https://developer.zapier.com)) |
| Make | Scenario template creation (partner platform) | Free for technology partners ([make.com/en/partners](https://www.make.com/en/partners)) |
| Partner marketplaces | 5+ platform listings | $0-19 total (most are free; Shopify is $19 one-time) |

**Estimated monthly cost at this level:** ~$200-400/mo (Loops Growth + n8n Pro + periodic Clay usage)

## Drills Referenced

- `partner-marketplace-scaling` -- expands from 1-2 to 5+ marketplaces with automated management, landing pages, and Zap templates
- `partner-marketplace-review-generation` -- continues the review generation cadence across the expanded marketplace portfolio
