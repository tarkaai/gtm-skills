---
name: partner-marketplace-listings-smoke
description: >
  Partner Marketplace Listings — Smoke Test. Get listed on 1-2 partner ecosystem
  app marketplaces (Salesforce AppExchange, HubSpot, Shopify, Slack, Zapier) to
  test whether marketplace-sourced installs convert to leads.
stage: "Marketing > SolutionAware"
motion: "DirectoriesMarketplaces"
channels: "Other"
level: "Smoke Test"
time: "8 hours agent work + 2-6 weeks marketplace review"
outcome: ">=1 live marketplace listing and >=5 marketplace-sourced signups in 4 weeks post-approval"
kpis: ["Marketplace listing views", "Install count", "Marketplace-sourced signups", "Install-to-signup rate"]
slug: "partner-marketplace-listings"
install: "npx gtm-skills add marketing/solution-aware/partner-marketplace-listings"
drills:
  - icp-definition
  - threshold-engine
---

# Partner Marketplace Listings — Smoke Test

> **Stage:** Marketing > SolutionAware | **Motion:** DirectoriesMarketplaces | **Channels:** Other

## Outcomes

Run once, locally, with agent assistance. The goal is to prove that partner ecosystem marketplaces generate any signal at all -- installs of your integration and at least a handful of signups from marketplace-sourced users. No budget required. No always-on automation. Human submits listings; agent handles research, copy, and tracking setup.

**Pass threshold:** >=1 live marketplace listing and >=5 marketplace-sourced signups in 4 weeks post-approval.

## Leading Indicators

- Listing submitted to marketplace review within 48 hours of starting
- Marketplace review approved (timeline varies: 2-8 weeks depending on platform)
- UTM-tagged traffic from the marketplace appearing in PostHog within 3 days of going live
- At least 3 installs in the first week post-approval
- At least 1 signup from a marketplace-sourced session in the first 2 weeks

## Instructions

### 1. Identify target partner marketplaces

Run the `icp-definition` drill to determine which partner platforms your ICP already uses as core infrastructure. Specifically: which platforms do your closed-won customers integrate with? Which partner ecosystem shows up in your website referral traffic?

Select 1-2 marketplaces to start. Recommended priority order based on typical B2B SaaS ICP overlap:

| Marketplace | Best for | Review timeline |
|-------------|----------|----------------|
| HubSpot App Marketplace | SMB/mid-market B2B, marketing/sales tools | 2-4 weeks |
| Salesforce AppExchange | Enterprise B2B, CRM-adjacent tools | 4-8 weeks (security review required) |
| Shopify App Store | E-commerce, merchant tools | 2-6 weeks |
| Slack App Directory | Collaboration, notifications, workflow tools | 2-4 weeks |
| Zapier | Any product with an API; automation buyers | 1-3 weeks |

**Prerequisite:** You must have a working integration with the target platform before listing. If you do not yet have an integration, build the minimum viable integration first (API connection, OAuth flow, 1-2 core actions).

### 2. Create keyword-optimized listings

Run the the partner marketplace listing setup workflow (see instructions below) drill. For each target marketplace:

1. Research marketplace-specific search terms using Clay Claygent
2. Write keyword-optimized title, tagline, and description
3. Prepare 3+ screenshots showing the integration working inside the partner platform
4. Record or source a 60-120 second demo video of the integration workflow
5. Set UTM parameters on all outbound links: `?utm_source={marketplace}&utm_medium=partner-marketplace&utm_campaign=smoke`
6. Fill every metadata field the marketplace offers (categories, tags, supported editions, pricing)

**Human action required:** Submit the listing through the marketplace's developer/partner portal. The agent prepares all copy and assets; the human with developer portal access submits.

### 3. Seed initial reviews

**Human action required:** While waiting for marketplace review approval, identify 5-10 existing customers who already use the integration. Ask them personally (not via template) to leave a review once the listing goes live. Provide the direct review link. Prioritize customers who:
- Have been using the integration for 30+ days
- Match your ICP (their reviews resonate with marketplace browsers)
- Have expressed satisfaction in support interactions or NPS surveys

### 4. Set up basic attribution tracking

Configure PostHog to track marketplace-sourced traffic:
- Create a saved filter for sessions where `utm_source` matches your marketplace names
- Track: `partner_marketplace_visit`, `partner_marketplace_signup` events
- Check daily during the measurement period

### 5. Evaluate against threshold

Run the `threshold-engine` drill after 4 weeks of the listing being live:

- **PASS (>=5 signups from marketplace):** Marketplace presence generates pipeline-quality signal. Proceed to Baseline.
- **MARGINAL (installs >0 but <5 signups):** Integration is discoverable but not converting. Investigate: is the listing CTA clear? Does the landing page match marketplace user expectations? Optimize and re-measure for 2 more weeks.
- **FAIL (0 installs after 4 weeks live):** Listing may be in the wrong category, description is not keyword-optimized, or the marketplace does not have demand for your category. Revise listing or try a different marketplace.

## Time Estimate

- 3 hours: Marketplace research, keyword research, competitive analysis (agent)
- 3 hours: Listing copy, screenshot preparation, video sourcing (agent + human)
- 1 hour: PostHog tracking setup and CRM logging (agent)
- 1 hour: Review seeding outreach to existing customers (human)
- 2-8 weeks: Marketplace review period (waiting; no active work)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Salesforce AppExchange | Enterprise partner marketplace | Free listing; 15% revenue share on paid apps ([partners.salesforce.com](https://partners.salesforce.com)) |
| HubSpot App Marketplace | SMB/mid-market partner marketplace | Free listing; developer handles own billing ([developers.hubspot.com](https://developers.hubspot.com)) |
| Shopify App Store | E-commerce partner marketplace | $19 one-time registration; 0% rev share on first $1M, 15% after ([shopify.dev/docs/apps/launch/distribution/revenue-share](https://shopify.dev/docs/apps/launch/distribution/revenue-share)) |
| Slack App Directory | Collaboration partner marketplace | Free listing ([api.slack.com](https://api.slack.com)) |
| Zapier | Automation partner marketplace | Free listing for public integrations ([developer.zapier.com](https://developer.zapier.com)) |
| Clay | Keyword research and competitive analysis | Launch plan $185/mo ([clay.com/pricing](https://clay.com/pricing)) |
| PostHog | UTM traffic tracking | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | CRM for listing tracking | Free for small teams ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated monthly cost at this level:** $0-19 (free marketplace listings + existing stack tools). Clay usage can be done within a trial or existing plan.

## Drills Referenced

- `icp-definition` -- identifies which partner platforms your ICP uses as core infrastructure
- the partner marketplace listing setup workflow (see instructions below) -- creates keyword-optimized listings with UTM tracking and CRM logging
- `threshold-engine` -- evaluates pass/fail against the 5-signup threshold
