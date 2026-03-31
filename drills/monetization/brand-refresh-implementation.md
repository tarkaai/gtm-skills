---
name: brand-refresh-implementation
description: Execute brand refresh changes across website pages, update messaging, and deploy new positioning with conversion tracking
category: Conversion
tools:
  - Webflow
  - PostHog
  - Loops
  - n8n
fundamentals:
  - webflow-site-redesign
  - webflow-landing-pages
  - posthog-custom-events
  - posthog-feature-flags
  - posthog-funnels
  - loops-audience
  - n8n-workflow-basics
---

# Brand Refresh Implementation

Execute the brand refresh changes identified in the `brand-audit-analysis` drill. Updates website copy, visual elements, and conversion paths. Deploys changes behind feature flags for A/B testing before full rollout.

## Input

- Completed brand audit report with prioritized action list
- New brand positioning: updated value proposition, tagline, messaging hierarchy
- Updated visual assets (if applicable): colors, typography, imagery style
- Current website analytics baseline from PostHog

## Steps

### 1. Snapshot current performance baseline

Before making any changes, lock in baseline metrics using `posthog-custom-events`:

```
Event: brand_refresh_baseline_snapshot
Properties:
  - homepage_bounce_rate: {current %}
  - homepage_to_pricing_rate: {current %}
  - pricing_to_signup_rate: {current %}
  - overall_conversion_rate: {current %}
  - avg_session_duration: {current seconds}
  - snapshot_date: {today}
```

Store this in Attio as a timestamped note. Every future measurement compares against this baseline.

### 2. Update website copy

Using `webflow-site-redesign`, update pages in priority order (highest traffic and conversion impact first):

**Homepage:**
- H1: New value proposition headline (from audit recommendations)
- H2: Supporting statement that explains how you deliver the value
- CTAs: Updated to match new messaging hierarchy
- Social proof: Refresh customer logos, testimonials, or metrics

**Pricing page:**
- Updated feature descriptions to use new terminology
- CTA copy aligned with new positioning

**Features/Product pages:**
- Headlines rewritten to lead with outcomes, not features
- Each section tied to a specific ICP pain point

**About page:**
- Mission/vision updated to reflect new positioning

For each page, deploy changes behind a PostHog feature flag using `posthog-feature-flags`:
```
Feature flag: brand-refresh-{page-slug}
Rollout: 50% of visitors see new version, 50% see original
```

### 3. Update conversion paths

Using `posthog-funnels`, verify the conversion funnel still works after copy changes:
- Homepage > Features/Pricing > Signup
- Check that no forms, buttons, or links were broken during the update

Using `webflow-landing-pages`, rebuild or update key landing pages:
- Match new brand voice and visual style
- Update form copy and CTA buttons
- Maintain all UTM parameter tracking

### 4. Update email sequences

Using `loops-audience`, update lifecycle email templates to match new brand voice:
- Welcome sequence copy
- Nurture sequence messaging
- Re-engagement emails
- Ensure email templates use new brand colors and logo

### 5. Deploy measurement

Using `posthog-custom-events`, add brand-refresh-specific events:
- `brand_refresh_variant_shown` — which version (old vs. new) was displayed
- `brand_refresh_cta_clicked` — clicks on refreshed CTAs
- `brand_refresh_form_submitted` — conversions from refreshed pages

Using `posthog-funnels`, create comparison funnels:
- Old brand funnel: visitors who saw original pages
- New brand funnel: visitors who saw refreshed pages

### 6. Evaluate and roll out

After 2 weeks (or 1,000 visitors per variant, whichever is first):
1. Compare conversion rates between old and new versions
2. If new version wins by >10% with statistical significance: roll out to 100%
3. If new version is within 10%: extend test for 2 more weeks
4. If new version loses: revert to old version, diagnose what went wrong, iterate on the copy

Build an n8n workflow using `n8n-workflow-basics` to automatically check experiment results daily and send a Slack alert when statistical significance is reached.

## Output

- Updated website with new brand positioning (behind feature flags)
- A/B test running on each updated page
- Before/after metrics comparison
- Updated email sequences matching new brand voice
- Decision report: which pages to roll out, which to iterate

## Triggers

- Run once after brand audit is complete
- Re-run for each batch of page updates (prioritize high-traffic pages first)
