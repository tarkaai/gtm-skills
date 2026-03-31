---
name: brand-refresh-redesign-baseline
description: >
  Brand Refresh & Redesign — Baseline Run. Implement the winning positioning
  concept across key website pages behind feature flags, A/B test against
  the current brand, and measure conversion impact over 8 weeks.
stage: "Marketing > Unaware"
motion: "Lead Capture Surface"
channels: "Website, Content"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: ">=20% improvement in homepage-to-conversion rate with new brand positioning vs. control over 8 weeks"
kpis: ["Homepage bounce rate (new vs. old)", "Homepage-to-pricing click rate", "Overall conversion rate (new vs. old)", "Avg session duration (new vs. old)", "Statistical significance reached (yes/no)"]
slug: "brand-refresh-redesign"
install: "npx gtm-skills add marketing/unaware/brand-refresh-redesign"
drills:
  - posthog-gtm-events
  - lead-capture-surface-setup
  - threshold-engine
---

# Brand Refresh & Redesign — Baseline Run

> **Stage:** Marketing > Unaware | **Motion:** Lead Capture Surface | **Channels:** Website, Content

## Outcomes

Take the winning positioning concept from the Smoke audit and implement it on the highest-traffic website pages. Deploy behind PostHog feature flags so 50% of visitors see the new brand and 50% see the old. Run for 8 weeks and measure whether the new positioning improves conversion. Pass threshold: >=20% improvement in homepage-to-conversion rate.

## Leading Indicators

- Feature flags deployed and both variants (old and new) receiving traffic within 48 hours
- New brand pages loading correctly with no broken links, forms, or CTAs (verify via automated checks)
- Bounce rate delta visible within 2 weeks (early signal of messaging resonance)
- At least 500 visitors per variant by week 2 (enough data for initial trend)
- Form submission rate trending up for the new variant by week 4

## Instructions

### 1. Snapshot pre-refresh baseline

Using `posthog-gtm-events`, record a baseline snapshot before any changes:
- Homepage bounce rate
- Homepage > pricing page click rate
- Pricing > signup conversion rate
- Overall visitor-to-lead conversion rate
- Average session duration
- Form submission rate across all lead capture surfaces

Store as a PostHog custom event `brand_refresh_baseline_snapshot` with all metrics as properties. Also log in Attio.

### 2. Set up lead capture surfaces

Run the `lead-capture-surface-setup` drill to ensure conversion infrastructure is ready:
- Primary form on homepage (newsletter, demo request, or free trial)
- Secondary forms on key landing pages
- All forms tracked in PostHog with `brand_refresh_form_submit` event
- Form submissions route to Attio via n8n webhook
- Ensure forms work identically on both old and new brand variants

### 3. Implement the brand refresh

Run the the brand refresh implementation workflow (see instructions below) drill with the winning positioning concept from Smoke:

**Pages to update (in priority order):**
1. **Homepage**: New H1, H2, primary CTA, social proof section
2. **Pricing page**: Updated feature descriptions using new messaging framework
3. **Top 3 landing pages**: Headline and CTA alignment with new positioning
4. **About page**: Mission/vision aligned with new positioning

**Deployment strategy:**
- All changes deployed behind PostHog feature flags: `brand-refresh-homepage`, `brand-refresh-pricing`, etc.
- 50/50 traffic split: half see original, half see new brand
- Feature flags are persistent (same visitor always sees the same variant across sessions)

The drill handles: Webflow page updates, feature flag configuration, conversion tracking, and email sequence updates.

**Human action required:** Review the new brand copy before enabling feature flags. Check that visual elements (images, colors, layout) still look correct with new headlines. Approve feature flag activation.

### 4. Monitor the A/B test

Track weekly using PostHog:

**Week 1-2**: Are both variants delivering? Check for implementation bugs. Verify event tracking works on both variants. Look at bounce rate — the fastest signal of brand resonance.

**Week 3-4**: Bounce rate and engagement trends. Is the new brand reducing bounce rate? Is session duration increasing? Are more visitors reaching the pricing page?

**Week 5-6**: Conversion data accumulating. Is the new brand driving more form submissions? What's the delta?

**Week 7-8**: Statistical significance check. Is there enough data to declare a winner?

### 5. Evaluate against threshold

Run the `threshold-engine` drill:
- **Homepage-to-conversion rate improvement >= 20%**: Compare the new variant's conversion rate against the old variant's rate.
- **Statistical significance**: p-value < 0.05 (PostHog experiments calculate this automatically).

Decision tree:
- **PASS (>=20% improvement, statistically significant)**: Roll out new brand to 100% of visitors. Proceed to Scalable for systematic multi-page optimization.
- **PARTIAL (5-19% improvement or not yet significant)**: Extend the test for 4 more weeks. If still not significant, the new brand is marginally better — consider implementing with continued monitoring.
- **FAIL (new brand performs worse)**: Revert to old brand. Return to Smoke to test a different positioning concept.

## Time Estimate

- 2 hours: Baseline snapshot and lead capture setup
- 6 hours: Brand refresh implementation (copy updates, feature flag deployment, email sequence updates)
- 2 hours: Implementation QA and launch verification
- 4 hours: Weekly monitoring (30 minutes/week for 8 weeks)
- 4 hours: Final evaluation, statistical analysis, and decision documentation

**Total: ~18 hours over 8 weeks (front-loaded: 10 hours in week 1, then monitoring)**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, A/B testing, web analytics | Free tier (1M events/mo) |
| Webflow | Website page updates | ~$15-40/mo |
| Tally | Lead capture forms (if not using Webflow forms) | Free tier |
| Loops | Email sequence updates | ~$30/mo Starter |
| n8n | Form submission routing to Attio | Free self-hosted or $20/mo cloud |

## Drills Referenced

- the brand refresh implementation workflow (see instructions below) — Executes all website copy and visual updates behind feature flags with A/B test configuration and conversion tracking
- `posthog-gtm-events` — Configures the baseline snapshot and all brand-refresh-specific tracking events
- `lead-capture-surface-setup` — Ensures all conversion forms are working, tracked, and routing leads to CRM
- `threshold-engine` — Evaluates the A/B test results against the >=20% conversion improvement threshold with statistical significance check
