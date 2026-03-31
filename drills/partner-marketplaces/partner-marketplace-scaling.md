---
name: partner-marketplace-scaling
description: Scale from 1-2 partner marketplace listings to 5+ with automated listing management, cross-marketplace optimization, and lead routing
category: Partner Marketplaces
tools:
  - Clay
  - n8n
  - PostHog
  - Attio
  - Loops
fundamentals:
  - partner-marketplace-listing-api
  - partner-marketplace-analytics-api
  - clay-claygent
  - clay-company-search
  - n8n-workflow-basics
  - n8n-scheduling
  - n8n-crm-integration
  - posthog-custom-events
  - posthog-funnels
  - posthog-cohorts
  - attio-contacts
  - attio-lists
  - attio-deals
  - loops-sequences
---

# Partner Marketplace Scaling

This drill scales your partner marketplace presence from 1-2 listings to 5+ marketplaces with automated listing management, cross-marketplace performance comparison, and marketplace-specific lead routing. The 10x multiplier: each new marketplace is a new discovery surface reaching buyers already using that ecosystem, and marketplace-specific landing pages convert 2-3x higher than generic pages.

## Input

- At least 1 partner marketplace listing with proven signal (Smoke passed: installs > 0, leads > 0)
- Performance data showing which marketplace(s) convert best
- Working integrations with additional partner platforms (or integrations in development)
- PostHog tracking configured for marketplace-sourced traffic

## Steps

### 1. Identify the next 3-5 partner marketplaces

Use Clay with `clay-claygent` and `clay-company-search` to systematically discover expansion opportunities:

**Claygent prompt:**
```
Given that our product {product_name} has a working integration with {current_platforms} and our {best_marketplace} listing generates {installs}/month:

1. Which partner platform ecosystems have the largest overlap with our ICP ({icp_description})?
2. For each platform, does it have a public app marketplace? What is the category structure?
3. How many competing apps exist in our category on each marketplace?
4. What is the estimated effort to build an integration? (API availability, SDK maturity, certification requirements)
5. Rank by: ICP overlap * marketplace traffic * (1 / competition density) * (1 / integration effort)

Return top 5 expansion targets with: platform name, marketplace URL, ICP overlap score, competition count, estimated integration effort (weeks), and composite priority score.
```

**Prioritize marketplaces where:**
- Your ICP is concentrated (validate against closed-won customer tech stacks in Attio)
- Competition is moderate (5-30 apps; too few means low demand, too many means hard to rank)
- You already have or can quickly build the integration
- The marketplace has a meaningful review/ranking system (organic discovery potential)

### 2. Build marketplace-specific landing pages

For each marketplace, create a dedicated landing page that speaks the language of that ecosystem's users:

**Page structure:**
1. Hero: "The {Category} Integration for {Platform Name}"
2. Integration demo: screenshots/video showing the product working inside that specific platform
3. Feature list: capabilities specific to that platform's integration
4. Social proof: reviews/testimonials from users of that specific platform
5. CTA: "Install from {Marketplace Name}" button linking to the marketplace listing
6. Secondary CTA: "Start Free Trial" for direct signups

**UTM structure for landing pages:**
- Marketplace -> Landing page: `?utm_source={marketplace}&utm_medium=partner-marketplace&utm_campaign=listing`
- Landing page -> Signup: pass through `utm_source` to track full funnel

### 3. Configure per-marketplace lead routing

Using `n8n-workflow-basics` and `n8n-crm-integration`, build a lead routing workflow:

**Trigger:** New signup or trial start where `utm_source` matches a partner marketplace

**Steps:**
1. Create or update the contact in Attio using `attio-contacts`
2. Set field `acquisition_source = "partner-marketplace"` and `acquisition_marketplace = "{marketplace_name}"`
3. Create a deal in Attio using `attio-deals` in the appropriate pipeline
4. Tag the contact in Loops for marketplace-specific onboarding sequence
5. If the marketplace is high-value (e.g., Salesforce = enterprise): alert sales in Slack for immediate follow-up

### 4. Build marketplace-specific onboarding sequences

Using `loops-sequences`, create onboarding emails per marketplace that reference the specific integration:

**Sequence per marketplace:**
1. Day 0: "Welcome! Here's how to connect {Product} with {Platform}" -- link to integration setup guide
2. Day 2: "3 workflows {Platform} users love with {Product}" -- use cases specific to that ecosystem
3. Day 5: "See what {Customer X} achieved with {Product} + {Platform}" -- case study from a user of that platform
4. Day 10: "Unlock advanced {Platform} features" -- upsell to paid plan with platform-specific value props

### 5. Configure cross-marketplace conversion funnels

Using `posthog-funnels` and `posthog-cohorts`:

**Funnel per marketplace:**
```
partner_marketplace_visit (utm_source = {marketplace}) ->
  marketplace_landing_page_view ->
    signup_started ->
      integration_connected ->
        activation_milestone_reached
```

**Cohorts per marketplace:**
- "{Marketplace} Signups" -- all users acquired from that marketplace
- Compare cohorts: which marketplace produces users with the highest activation rate? Highest retention at day 30?

### 6. Automate listing health monitoring

Using `n8n-scheduling` and `partner-marketplace-analytics-api`, create a weekly monitoring workflow:

**n8n workflow (Monday 8am):**
1. Pull analytics from all marketplace listings
2. Compare week-over-week: installs, views, rating, rank
3. Flag anomalies: >20% decline in any metric
4. Update Attio campaign records with latest metrics
5. Post summary to Slack:
```
Partner Marketplace Weekly:
- Total installs across all marketplaces: {X} ({change}% WoW)
- Best performing: {marketplace} ({installs} installs)
- Needs attention: {marketplace} ({reason})
- Review requests pending: {count}
```

### 7. Build Zap/scenario templates (for Zapier/Make)

If listed on Zapier or Make, create 10+ pre-built automation templates:

Use `clay-claygent` to research popular Zap/scenario patterns:
```
Prompt: "For the {category} category on Zapier, what are the 10 most-used Zap templates involving CRM/sales/marketing tools? For each, what trigger and action pattern do they use? Which ones could our product replace or improve?"
```

Create templates covering: the top 5 trigger/action combinations your integration supports. Zapier and Make rank integrations partly by available template count.

## Output

- 5+ partner marketplace listings live and tracking
- Marketplace-specific landing pages and onboarding sequences
- Automated lead routing by acquisition marketplace
- Cross-marketplace conversion funnels in PostHog
- Weekly automated performance monitoring
- 10+ Zap/scenario templates (if on Zapier/Make)

## Triggers

- Run at Scalable level to expand from 1-2 to 5+ marketplace listings
- Weekly monitoring runs continuously once set up
- Re-evaluate marketplace portfolio quarterly based on performance data
