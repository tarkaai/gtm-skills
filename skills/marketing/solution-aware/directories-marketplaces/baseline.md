---
name: directories-marketplaces-baseline
description: >
  Directory & Marketplace Listings — Baseline Run. Set up always-on tracking, automated review
  collection, and directory-specific landing pages to sustain and grow directory-sourced pipeline.
stage: "Marketing > SolutionAware"
motion: "DirectoriesMarketplaces"
channels: "Other"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: ">= 150 views and >= 3 inquiries over 2 weeks"
kpis: ["Listing views", "Inquiry count", "Review count", "Review velocity (reviews/week)"]
slug: "directories-marketplaces"
install: "npx gtm-skills add marketing/solution-aware/directories-marketplaces"
drills:
  - posthog-gtm-events
  - directory-review-generation
  - landing-page-pipeline
---

# Directory & Marketplace Listings — Baseline Run

> **Stage:** Marketing > SolutionAware | **Motion:** DirectoriesMarketplaces | **Channels:** Other

## Outcomes

First always-on automation. The agent sets up continuous tracking, automated review collection, and directory-specific landing pages. The question this level answers: does directory presence reliably produce inquiries over time, not just in a one-week burst?

**Pass threshold:** >= 150 views and >= 3 inquiries over 2 weeks.

## Leading Indicators

- PostHog events firing correctly for all directory-sourced traffic within 2 days of setup
- Automated review ask sequence live and sending within 3 days
- At least 1 new review per week from the automated sequence
- Directory-specific landing pages converting at >= 3% click-to-inquiry rate

## Instructions

### 1. Configure full-funnel tracking

Run the `posthog-gtm-events` drill to establish the directory event taxonomy in PostHog:

- `directory_listing_view`: visitor arrives from a directory (UTM match). Properties: `directory_name`, `listing_type` (organic/ppc).
- `directory_listing_click`: visitor clicks a CTA on the landing page. Properties: `directory_name`, `cta_type` (signup/demo/pricing).
- `directory_inquiry_submitted`: visitor completes a form, books a demo, or starts a trial. Properties: `directory_name`, `inquiry_type`, `form_id`.

Build a PostHog funnel: `directory_listing_view` -> `directory_listing_click` -> `directory_inquiry_submitted`. Break down by `directory_name` to see which directories convert best.

### 2. Launch automated review collection

Run the `directory-review-generation` drill to build and activate the review pipeline:

1. Build the review candidate list from Attio (active 30+ days, positive sentiment, have not reviewed)
2. Create the 3-email review ask sequence in Loops
3. Set up automated triggers: post-milestone, post-positive-support, post-upgrade
4. Configure review monitoring webhooks to track new reviews and update Attio

Target: 2-3 new reviews per week across all directories.

### 3. Build directory-specific landing pages

Run the `landing-page-pipeline` drill to create dedicated landing pages for directory traffic. Why: visitors from G2 or Capterra are comparing tools. A generic homepage does not address their evaluation mindset.

For each Tier 1 directory, create a page at `/from/{directory-name}` with:

- **Headline** that acknowledges their research: "Comparing {category} tools? Here's why teams choose {product}."
- **Social proof from that directory**: "Rated 4.7/5 on G2 with 50+ reviews"
- **Comparison points**: address the top 3 things buyers compare in your category
- **Direct CTA**: demo booking or free trial start
- **UTM-aware personalization**: if `utm_source=g2`, show G2 badge. If `utm_source=capterra`, show Capterra badge.

Update your directory listings to point to these landing pages instead of your homepage.

### 4. Set up weekly monitoring

Run the the directory performance monitor workflow (see instructions below) drill to configure:

1. Weekly n8n workflow that pulls analytics from each directory API
2. PostHog dashboard with views, clicks, inquiries, and review trends by directory
3. Alerts for traffic drops (>30% week-over-week) or negative reviews (1-2 stars)
4. Weekly Slack report summarizing directory performance

### 5. Evaluate against threshold

After 2 weeks, measure:

- **PASS (>= 150 views, >= 3 inquiries):** Directory channel is producing repeatable results. Proceed to Scalable.
- **MARGINAL (>= 150 views, 1-2 inquiries):** Traffic is there but conversion is low. Optimize landing pages and review the quality of directory-sourced traffic. Re-run for another 2 weeks.
- **FAIL (< 150 views or 0 inquiries):** Revisit directory selection. Double down on the directories that showed signal at Smoke. Consider whether your category has enough directory search volume.

## Time Estimate

- 3 hours: PostHog event taxonomy and funnel setup
- 3 hours: Review generation sequence build and trigger configuration
- 4 hours: Landing page creation (1-2 pages)
- 2 hours: Monitoring dashboard and alert setup

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| G2 | Review directory | Free listing ([sell.g2.com/plans](https://sell.g2.com/plans)) |
| Capterra | Review directory | Free listing; PPC min $500/mo ([capterra.com/vendors](https://www.capterra.com/vendors/)) |
| PostHog | Event tracking and dashboards | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Loops | Automated review ask emails | Starter $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Workflow automation | Community (self-hosted) free; Cloud from EUR 24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | CRM tracking | Free for small teams ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated monthly cost at this level:** $0-50 (free listings + Loops starter if not already on stack)

## Drills Referenced

- `posthog-gtm-events` -- establishes the directory event taxonomy for tracking views, clicks, and inquiries
- `directory-review-generation` -- automated review collection via Loops sequences and CRM-triggered asks
- `landing-page-pipeline` -- builds directory-specific landing pages that convert comparison shoppers
- the directory performance monitor workflow (see instructions below) -- weekly analytics collection, dashboard, and alerts
