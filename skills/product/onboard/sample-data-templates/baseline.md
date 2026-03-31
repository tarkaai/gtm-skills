---
name: sample-data-templates-baseline
description: >
  Sample Data Acceleration — Baseline Run. Deploy sample data and a template gallery to all new
  signups via feature flag. Run always-on A/B test measuring seeded vs. empty accounts on
  activation rate. Add template gallery as a second value-discovery surface.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "20 hours over 2 weeks"
outcome: "≥80% interaction rate AND ≥10pp activation lift vs. control"
kpis: ["Sample data interaction rate", "Template install rate", "Activation rate lift", "Time to first real object"]
slug: "sample-data-templates"
install: "npx gtm-skills add product/onboard/sample-data-templates"
drills:
  - posthog-gtm-events
  - template-gallery-setup
---

# Sample Data Acceleration — Baseline Run

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Success at Baseline means: sample data and templates produce a statistically significant activation lift when deployed to all new signups. The system runs always-on with automated tracking, and the template gallery gives users a second path to value beyond sample data.

## Leading Indicators

- Template gallery page views exceed 30% of new signups within first week
- Template install-to-edit rate exceeds 40%
- Users who interact with sample data AND install a template activate at 2x the rate of control users
- Sample data clearance followed by real data creation (the "graduated" signal) increases week over week
- Time-to-first-real-object for seeded users is <50% of control users

## Instructions

### 1. Instrument comprehensive event tracking

Run the `posthog-gtm-events` drill to set up the full event taxonomy for this play. Beyond the Smoke-level events, add:

- `sample_data_record_cloned` — user duplicates a sample record as a starting point for their own
- `sample_data_graduated` — user cleared sample data AND created their first real object within 7 days
- `template_gallery_viewed`, `template_previewed`, `template_installed`, `template_object_edited`
- `onboarding_path_chosen` — which path the user took: explored sample data, installed a template, started from scratch, or some combination

Build PostHog funnels:
1. **Sample data funnel**: `sample_data_injected` → `sample_data_record_viewed` → `sample_data_record_edited` → `real_object_created` → `activation_reached`
2. **Template funnel**: `template_gallery_viewed` → `template_previewed` → `template_installed` → `template_object_edited` → `activation_reached`
3. **Combined onboarding funnel**: `signup_completed` → `onboarding_path_chosen` → `first_meaningful_action` → `activation_reached`

### 2. Build the template gallery

Run the `template-gallery-setup` drill. For Baseline, build:

- **8-12 templates** across 3 categories matching your top ICP segments
- **Three surfaces**: dedicated gallery page, empty-state template suggestions, and a template selection step in the onboarding flow
- **Install tracking**: every template install creates a PostHog event with template ID, surface source, and user cohort

Populate the gallery with templates designed from the patterns observed in Smoke: what configurations do activated users most commonly create? Turn those into one-click templates.

**Human action required:** Review template content and previews before launch. Verify each template installs correctly and creates the expected objects. Test the install flow end-to-end.

### 3. Deploy to all signups with A/B test

Expand from the Smoke test group to 100% of new signups, split:
- **Treatment A (50%)**: Sample data injected at signup + template gallery available
- **Control (50%)**: No sample data, no template gallery (current empty-state experience)

Use PostHog feature flags for the split. Run for 2 weeks or until each group reaches 200+ users, whichever is longer.

### 4. Launch engagement monitoring

Run the `sample-data-engagement-monitor` drill to deploy:

- The PostHog dashboard with volume, engagement quality, activation impact, and lifecycle signal panels
- Comparison cohorts: seeded vs. control, template adopters vs. non-adopters
- Daily automated checks via n8n: interaction rate drop alerts, template health flags
- Weekly summary report posted to Slack with activation lift and top/bottom templates

### 5. Evaluate against threshold

At the end of 2 weeks, compute:

- **Sample data interaction rate**: Target ≥80% (up from Smoke's 70%)
- **Activation rate lift**: Compute the percentage point difference in activation rate between treatment and control. Target ≥10pp lift.
- **Template install rate**: % of treatment users who installed at least 1 template. Benchmark: ≥20%.
- **Statistical significance**: Activation lift must reach 95% confidence.

**Pass threshold: ≥80% interaction rate AND ≥10pp activation rate lift vs. control at 95% confidence.**

If PASS: Disable the control group (give everyone sample data + templates). Document the winning configuration. Proceed to Scalable.
If FAIL: Diagnose by cohort. If interaction rate is high but activation lift is low, the sample data is entertaining but not driving real product usage — redesign the graduation path (sample → real data). If interaction rate is low, the discoverability or relevance of sample data needs work.

## Time Estimate

- 4 hours: Set up comprehensive PostHog event taxonomy and funnels
- 8 hours: Build template gallery with 8-12 templates across 3 surfaces
- 3 hours: Configure engagement monitoring dashboard and n8n alerts
- 2 hours: Feature flag configuration and A/B test setup
- 3 hours: Monitor over 2 weeks, weekly analysis, final evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, funnels, cohorts, dashboards | Free tier: 1M events/mo; paid: usage-based from $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app messages for template suggestions and orientation | Essential: $29/seat/mo; Advanced: $85/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Lifecycle emails for template discovery and sample data graduation | Free: 1K contacts / 4K sends; Paid from $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Automated monitoring workflows and alert routing | Self-hosted: Free; Cloud from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |

**Estimated monthly cost: ~$50-130/mo** (Loops paid tier + n8n cloud if not self-hosting)

## Drills Referenced

- `posthog-gtm-events` — comprehensive event taxonomy for sample data and template interactions
- `template-gallery-setup` — build the browseable template catalog across 3 product surfaces
