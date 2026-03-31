---
name: directories-marketplaces-smoke
description: >
  Directory & Marketplace Listings — Smoke Test. Claim and optimize listings on 3-5 top directories,
  seed initial reviews, and measure whether directory presence generates any views or inquiries.
stage: "Marketing > SolutionAware"
motion: "DirectoriesMarketplaces"
channels: "Other"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: ">= 50 listing views and >= 1 inquiry in 1 week"
kpis: ["Listing views", "Inquiry count", "Review count"]
slug: "directories-marketplaces"
install: "npx gtm-skills add marketing/solution-aware/directories-marketplaces"
drills:
  - icp-definition
  - directory-listing-setup
  - threshold-engine
---

# Directory & Marketplace Listings — Smoke Test

> **Stage:** Marketing > SolutionAware | **Motion:** DirectoriesMarketplaces | **Channels:** Other

## Outcomes

Run once, locally, with agent assistance. The goal is to prove that directory presence generates any signal at all -- views on your listings and at least one inbound inquiry from a directory-sourced visitor. No budget required. No always-on automation.

**Pass threshold:** >= 50 listing views and >= 1 inquiry in 1 week.

## Leading Indicators

- Listings approved and live on 3-5 directories within 48 hours of submission
- UTM-tagged traffic appearing in PostHog within 3 days
- At least 2 reviews posted within the first week
- Profile appearing in directory search results for your primary category keyword

## Instructions

### 1. Identify target directories

Run the `icp-definition` drill to understand where your ICP evaluates and compares tools. Specifically: which directories do your closed-won customers mention during sales calls? Which comparison sites show up in your website referral traffic?

Focus on 3-5 directories. Recommended starting set:
- **G2** -- largest B2B software review site, strong SEO, high buyer intent
- **Capterra** -- high traffic for SMB buyers, strong PPC option (skip PPC at Smoke)
- **Product Hunt** -- strong for dev tools and early-stage products, one-time launch event

Add 1-2 niche directories specific to your category (e.g., StackShare for dev tools, AlternativeTo for consumer-adjacent products).

### 2. Create optimized listings

Run the `directory-listing-setup` drill. For each directory:

1. Claim or create your profile via the vendor portal
2. Write keyword-optimized descriptions (use the keyword research step from the drill)
3. Upload 3+ screenshots with captions
4. Add a 60-90 second demo video
5. Fill out every comparison/feature field the directory offers
6. Set UTM parameters on all outbound links: `?utm_source={directory}&utm_medium=directory&utm_campaign=smoke`
7. Be transparent about pricing

Log each listing in Attio with: directory name, URL, date created, status.

### 3. Seed initial reviews

**Human action required:** Ask 5-10 existing customers to leave reviews. Prioritize:
- Customers who have expressed satisfaction in support tickets or NPS surveys
- Customers who have been active for 30+ days
- Customers whose profiles match your ICP (their reviews will resonate with other buyers)

Send a personal email (not a template) from the founder or their primary contact. Include the direct review link for the specific directory. Ask for an honest review, not a favorable one.

### 4. Monitor and measure

Check directory dashboards daily for the 1-week measurement period:
- Log views and clicks from each directory's vendor analytics
- Check PostHog for `utm_source` traffic matching your directory names
- Track any form submissions, demo requests, or signups from directory-sourced sessions

### 5. Evaluate against threshold

Run the `threshold-engine` drill to assess results after 1 week:

- **PASS (>= 50 views, >= 1 inquiry):** Directory presence generates signal. Proceed to Baseline.
- **MARGINAL (>= 50 views, 0 inquiries):** Views prove discoverability. Optimize listing CTA and landing page, then re-run.
- **FAIL (< 50 views):** Listings may be in wrong categories or descriptions are not keyword-optimized. Revise and re-submit.

## Time Estimate

- 1 hour: Directory research and selection
- 1.5 hours: Listing creation and optimization (agent-assisted copy, human submits)
- 0.5 hours: Review asks and monitoring setup

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| G2 | Software review directory | Free listing; sponsored starts ~$1,000+/quarter ([g2.com/pricing](https://sell.g2.com/plans)) |
| Capterra | Software review directory | Free listing; PPC min $500/mo at $2+/click ([capterra.com/vendors](https://www.capterra.com/vendors/)) |
| Product Hunt | Product launch directory | Free listing; Pro $100/mo ([producthunt.com](https://www.producthunt.com/)) |
| PostHog | UTM traffic tracking | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | CRM for listing tracking | Free for small teams ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated monthly cost at this level:** $0 (free listings only)

## Drills Referenced

- `icp-definition` -- identifies which directories your ICP uses to evaluate tools
- `directory-listing-setup` -- creates and optimizes listings with keyword-targeted copy and UTM tracking
- `threshold-engine` -- evaluates pass/fail against the 50-view, 1-inquiry threshold
