---
name: template-tool-marketplaces-baseline
description: >
  Template or Tool Marketplace — Baseline Run. Optimize template listings with keyword research,
  conversion funnel tracking, and a landing page tuned for marketplace-sourced traffic. First
  always-on tracking. Prove repeatable download-to-lead conversion.
stage: "Marketing > SolutionAware"
motion: "DirectoriesMarketplaces"
channels: "Other"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: ">= 150 downloads and >= 3 leads over 2 weeks"
kpis: ["Total downloads (all templates, all marketplaces)", "Download-to-site-visit rate", "Site-visit-to-lead conversion rate", "Leads captured"]
slug: "template-tool-marketplaces"
install: "npx gtm-skills add marketing/solution-aware/template-tool-marketplaces"
drills:
  - posthog-gtm-events
  - lead-capture-surface-setup
---

# Template or Tool Marketplace — Baseline Run

> **Stage:** Marketing > SolutionAware | **Motion:** DirectoriesMarketplaces | **Channels:** Other

## Outcomes

First always-on automation for the template marketplace channel. The agent configures persistent tracking, optimizes listing metadata for search visibility, and builds a conversion-optimized landing page for marketplace-sourced traffic. The goal is to prove that template distribution reliably and repeatedly converts downloads into leads.

**Pass threshold:** >= 150 downloads and >= 3 leads over 2 weeks.

## Leading Indicators

- PostHog events flowing for all marketplace-sourced traffic within 24 hours of setup
- Listing titles and descriptions updated with high-volume keywords
- Marketplace-specific landing page live with a single clear CTA
- Download-to-site-visit rate exceeds 5% (1 in 20 downloaders clicks the CTA)
- Site-visit-to-lead conversion rate exceeds 10% (1 in 10 CTA clickers converts)
- Downloads trending up week-over-week (listing optimization taking effect)

## Instructions

### 1. Configure full-funnel tracking

Run the `posthog-gtm-events` drill to set up persistent tracking for the marketplace-to-lead funnel:

**Events to configure:**

| Event | Trigger | Properties |
|-------|---------|-----------|
| `marketplace_visit` | Page load where `utm_source` matches a known marketplace AND `utm_medium` = "marketplace" | `marketplace`, `template_slug`, `utm_campaign` |
| `marketplace_cta_click` | Click on any product CTA during a marketplace-sourced session | `marketplace`, `template_slug`, `cta_location` |
| `marketplace_lead_captured` | Form submit, trial start, or demo booking from a marketplace-sourced session | `marketplace`, `template_slug`, `lead_type`, `email` |

**UTM parsing logic:** Match `utm_source` against: "notion", "gumroad", "figma", "airtable", "canva", "producthunt". Match `utm_medium` against: "marketplace", "cross-promo".

**Saved funnel in PostHog:**
```
marketplace_visit -> marketplace_cta_click -> marketplace_lead_captured
```
Break down by `marketplace` and `template_slug`.

### 2. Optimize template listings

Run the the marketplace listing optimization workflow (see instructions below) drill. This covers:

1. Researching marketplace-specific keywords using Clay Claygent
2. Rewriting listing titles to include the highest-volume keyword
3. Restructuring descriptions: outcome-first opening, what's included, who it's for, how to start, CTA
4. Filling all available tag slots with keyword variants
5. Updating cover images to be more visually distinctive than competitors
6. Setting up bi-weekly performance tracking in n8n

Focus optimization effort on the marketplace(s) that showed the most signal at Smoke level. If Notion drove 80% of downloads, optimize Notion first.

### 3. Build a marketplace-specific landing page

Run the `lead-capture-surface-setup` drill to create a dedicated landing page for marketplace-sourced traffic.

**Why a dedicated page:** Template users arrive with different expectations than organic search or ad traffic. They just used your template and want to know: "What does the full product do that the template doesn't?" A generic homepage does not answer this question.

**Landing page structure:**
1. **Headline:** "You just tried {Template Name}. Here's what happens when you stop doing it manually." (Reference the specific template they came from)
2. **Pain bridge:** "The template works for {use case}. But as your team grows, you need {automation/collaboration/analytics} that a template can't provide."
3. **Product demo:** 60-second video or interactive preview showing how the product automates what the template does manually
4. **Social proof:** "{X} teams upgraded from our templates to the full platform"
5. **CTA:** Single clear action -- start a free trial, book a demo, or sign up

**Personalization by UTM:** If `utm_campaign` includes the template slug, dynamically display the relevant template name in the headline and pain bridge. This requires PostHog feature flags or simple URL parameter parsing in your frontend.

### 4. Evaluate against threshold

After 2 weeks, measure against: >= 150 downloads and >= 3 leads.

Review the full funnel data:
- **Downloads per marketplace:** Which marketplace drives volume?
- **Download-to-visit rate per marketplace:** Where are CTAs most effective?
- **Visit-to-lead rate:** Is the landing page converting?

**PASS:** Proceed to Scalable. Document which marketplace and template topic performed best.
**MARGINAL:** Downloads are there but leads are low. Focus on: (a) improving in-template CTA placement and copy, (b) optimizing the landing page, (c) testing different CTA offers (free trial vs. demo vs. resource download). Re-run for 2 more weeks.
**FAIL:** Downloads below threshold. Revisit template topic selection and marketplace choice. Consider creating a new template targeting a higher-demand topic.

## Time Estimate

- 3 hours: PostHog event tracking setup and funnel configuration
- 4 hours: Listing keyword research and optimization across marketplaces
- 3 hours: Landing page creation and deployment
- 2 hours: Monitoring, analysis, and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Funnel tracking, conversion analytics | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Bi-weekly performance reporting automation | Cloud Pro EUR 60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Clay | Keyword and competitive research | Explorer $149/mo ([clay.com/pricing](https://clay.com/pricing)) |
| Attio | CRM for lead and listing tracking | Plus $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Loops | Nurture sequence for template leads | Starter $49/mo ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated monthly cost at this level:** $150-300 (n8n + Clay if using paid tiers; PostHog and marketplace listings remain free)

## Drills Referenced

- `posthog-gtm-events` -- configures the marketplace-to-lead tracking events and funnel
- the marketplace listing optimization workflow (see instructions below) -- keyword research, listing A/B testing, and bi-weekly optimization cycles
- `lead-capture-surface-setup` -- builds the marketplace-specific landing page with conversion tracking and CRM routing
