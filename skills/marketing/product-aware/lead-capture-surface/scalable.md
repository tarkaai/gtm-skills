---
name: lead-capture-surface-scalable
description: >
  Single CTA Lead Capture — Scalable Automation. Deploy lead capture surfaces across multiple
  high-intent pages, run systematic A/B tests on CTA copy, placement, and surface type, and
  build always-on conversion monitoring. Find the 10x by identifying which pages, surface types,
  and CTA variants convert best, then standardize the winners across all surfaces.
stage: "Marketing > ProductAware"
motion: "LeadCaptureSurface"
channels: "Direct"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥ 5% conversion rate sustained across ≥ 3 surfaces over 2 months with ≥ 30 leads/mo"
kpis: ["Overall conversion rate across all surfaces (target ≥ 5%)", "Number of active lead capture surfaces (target ≥ 3)", "Monthly lead volume (target ≥ 30)", "Best-performing surface conversion rate (target ≥ 8%)", "A/B test win rate (target ≥ 1 winning experiment per month)", "Mobile conversion rate (target ≥ 60% of desktop rate)"]
slug: "lead-capture-surface"
install: "npx gtm-skills add marketing/product-aware/lead-capture-surface"
drills:
  - ab-test-orchestrator
  - dashboard-builder
  - lead-capture-surface-setup
---

# Single CTA Lead Capture — Scalable Automation

> **Stage:** Marketing > ProductAware | **Motion:** LeadCaptureSurface | **Channels:** Direct

## Outcomes

Scale from one instrumented surface to multiple lead capture surfaces across your highest-traffic pages. Use systematic A/B testing to find the best CTA copy, placement, and surface type for each page. Build always-on conversion monitoring that alerts when any surface degrades. The 10x multiplier comes from deploying optimized surfaces wherever product-aware traffic lands, not just on one dedicated page.

Pass: ≥ 5% conversion rate sustained across ≥ 3 surfaces for 2 months, with ≥ 30 leads per month and at least 1 winning A/B experiment per month.
Fail: Conversion rate drops below 4% on the majority of surfaces, or lead volume does not scale with surface count.

## Leading Indicators

- Adding a second surface produces incremental leads (not just splitting the same traffic)
- At least 1 A/B test reaches statistical significance within the first month
- The best-performing surface exceeds 8% conversion rate (proving optimization headroom exists)
- Mobile conversion rate reaches ≥ 60% of desktop rate across all surfaces (mobile optimization is working)
- The `dashboard-builder` drill fires zero Critical alerts for 2+ consecutive weeks (all surfaces are healthy)
- Per-surface breakdown reveals which pages convert best, enabling prioritization

## Instructions

### 1. Deploy lead capture surfaces across multiple pages

Run the `lead-capture-surface-setup` drill for each new page. Identify 2-4 additional high-intent pages beyond the Baseline landing page:

- **Pricing page:** Visitors here are actively evaluating. Deploy an inline calendar or form below the pricing table. CTA: "Questions? Pick a time to talk" or "Start your trial."
- **Product/features page:** Visitors are learning what you do. Deploy a form or chat widget. CTA: "See it in action" or "Try it free."
- **Comparison pages** (if they exist): Visitors are deciding between you and alternatives. Deploy an inline calendar. CTA: "Let us show you the difference — 15 min."
- **Blog posts with high traffic:** Add a sticky CTA bar at the bottom or an inline form after the first section. CTA: contextual to the post topic.

For each surface:
- Configure the same PostHog events: `cta_impression`, `cta_clicked`, `lead_captured` with the `page` property set to that specific page
- Wire the n8n webhook to create Attio records with the source page attributed
- Enroll leads in the appropriate Loops sequence based on which page they converted on

### 2. Launch the always-on conversion monitor

Run the `dashboard-builder` drill to build the monitoring system across all surfaces. Configure:

- Daily funnel monitoring per surface (PostHog funnel broken down by `page`)
- Baseline conversion rates per surface (established after 2 weeks of data per surface)
- Anomaly detection thresholds: Warning at 15-30% below baseline for 3+ days, Critical at >30% below for 2+ days
- Weekly page performance ranking: top 3 and bottom 3 surfaces by conversion rate and lead volume
- Form abandonment analysis (for form surfaces): which field causes the most drop-off
- Device split monitoring: flag any surface where mobile conversion is < 50% of desktop

The monitor runs daily via n8n cron and sends alerts to Slack when any surface degrades.

### 3. Run systematic A/B tests

Run the `ab-test-orchestrator` drill to test one variable at a time across your surfaces. Prioritize tests by expected impact:

**Month 1 tests (highest impact):**

1. **CTA copy test:** On the highest-traffic surface, test 2 CTA headline variants. Example: "Book a demo" vs "See [product] in action — 15 min." Use PostHog feature flags to split traffic 50/50. Measure `lead_captured` rate per variant. Run for 7 days or until 200 impressions per variant.

2. **Surface type test:** On a page where you have enough traffic, test form vs calendar (or form vs chat). Deploy both variants using PostHog feature flags. One variant shows the form, the other shows the inline calendar. Measure which surface type produces a higher conversion rate on that specific page.

**Month 2 tests (refinement):**

3. **Form length test** (if using forms): Test the current form against a shorter version (remove one field). Measure conversion rate and lead quality (do shorter-form leads still convert to meetings?).

4. **Placement test:** On a page with high traffic but below-average conversion, test current placement vs a higher position (above the fold). Use PostHog feature flags to show different page layouts.

5. **Mobile-specific test:** If mobile conversion is significantly lower than desktop, test a mobile-optimized surface: simplified form, larger touch targets, or a "call us" CTA instead of a form.

For each test:
- Form a hypothesis with predicted outcome and reasoning (per `ab-test-orchestrator`)
- Calculate required sample size before launching
- Do not peek at results before the planned end date
- Document: hypothesis, variants, sample size, result, confidence level, and decision
- Implement winners permanently across all relevant surfaces

### 4. Standardize winning variants

After each successful A/B test, roll out the winning variant to all applicable surfaces:

- If a CTA copy variant wins on the pricing page, test it on other pages too (the same copy may not work everywhere, but it is worth testing)
- If a surface type wins (e.g., calendar beats form on high-intent pages), deploy that surface type on all similar pages
- If a form length wins, standardize across all form surfaces
- Update the `cta_variant` PostHog property so historical data distinguishes old vs new variants

### 5. Evaluate after 2 months

Review the `dashboard-builder` weekly reports and PostHog funnels for the full 2-month period:

- Overall conversion rate across all surfaces (weighted by traffic volume)
- Per-surface conversion rates: which pages perform best and worst?
- Monthly lead volume: did adding surfaces increase total leads proportionally?
- A/B test results: how many tests ran, how many produced significant winners, cumulative improvement?
- Mobile vs desktop: has the gap narrowed?

- **PASS (≥ 5% overall conversion rate, ≥ 30 leads/mo, ≥ 3 active surfaces):** Lead capture is a scalable, multi-surface system. Document: the winning surface types per page category, the winning CTA variants, and the per-surface conversion rates. Proceed to Durable.
- **MARGINAL (4-5% overall, or 20-30 leads/mo):** Check: Are you testing enough variants? Is traffic sufficient for statistical significance? Are there high-traffic pages without surfaces that should have them? Add surfaces or increase test velocity. Stay at Scalable.
- **FAIL (< 4% overall, or < 20 leads/mo):** The multi-surface approach is not scaling. Check: Are the new pages actually receiving product-aware traffic? Are the surfaces appropriate for each page's intent level? Consider consolidating to fewer, higher-performing surfaces rather than spreading thin.

## Time Estimate

- Deploy 2-4 additional surfaces: 8 hours (2 hours each)
- Conversion monitor setup: 4 hours
- A/B test setup and management (4-5 tests over 2 months): 16 hours
- Weekly monitoring and reporting review: 2 hours/week x 8 weeks = 16 hours
- Winner rollout and standardization: 8 hours
- Evaluation and documentation: 4 hours
- Buffer for troubleshooting: 4 hours
- Total: ~60 hours over 2 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Funnel analytics, A/B experiments, feature flags | Free tier: 1M events/mo; paid ~$0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Webflow | Landing pages and form surfaces | CMS plan $23/mo ([webflow.com/pricing](https://webflow.com/pricing)) |
| Cal.com | Inline scheduling embeds (calendar surfaces) | Free plan ([cal.com/pricing](https://cal.com/pricing)) |
| Tally | Form builder (form surfaces) | Free plan ([tally.so/pricing](https://tally.so/pricing)) |
| Intercom | Chat widget (chat surfaces) | Essential $29/seat/mo annual ([intercom.com/pricing](https://intercom.com/pricing)) |
| Attio | CRM — lead pipeline and attribution | Plus $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| n8n | All automation: webhooks, monitoring, alerts | Pro €60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Loops | Nurture sequences per surface | Starter $49/mo ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated monthly cost for Scalable:** $100-200/mo (Webflow + n8n Pro + Loops; PostHog and Attio may stay on free tiers depending on volume)

## Drills Referenced

- `ab-test-orchestrator` — design, run, and analyze A/B tests on CTA copy, surface type, placement, and form length using PostHog feature flags and experiments
- `dashboard-builder` — always-on monitoring for all lead capture surface funnels with per-page breakdown, anomaly alerts, form abandonment analysis, and device split tracking
- `lead-capture-surface-setup` — deploy additional surfaces on new pages with full tracking, CRM routing, and nurture enrollment
