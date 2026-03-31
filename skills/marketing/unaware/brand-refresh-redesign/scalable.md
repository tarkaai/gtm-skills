---
name: brand-refresh-redesign-scalable
description: >
  Brand Refresh & Redesign — Scalable Automation. Extend the validated brand refresh
  across all website pages, automate continuous A/B testing of messaging variants,
  and build always-on conversion monitoring with n8n workflows.
stage: "Marketing > Unaware"
motion: "Lead Capture Surface"
channels: "Website, Content"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: ">=30% improvement in brand recognition and >=25% lift in conversion rates over 6 months"
kpis: ["Pages refreshed (count)", "Active A/B tests (count)", "Conversion rate by page", "Bounce rate trend", "Session duration trend", "Experiment velocity (tests/month)"]
slug: "brand-refresh-redesign"
install: "npx gtm-skills add marketing/unaware/brand-refresh-redesign"
drills:
  - ab-test-orchestrator
  - dashboard-builder
---

# Brand Refresh & Redesign — Scalable Automation

> **Stage:** Marketing > Unaware | **Motion:** Lead Capture Surface | **Channels:** Website, Content

## Outcomes

Extend the validated brand refresh from the Baseline high-traffic pages to every marketing page, landing page, and email touchpoint. Build an automated testing system that continuously runs A/B experiments on messaging, CTAs, page layout, and social proof. Deploy always-on conversion monitoring that detects regressions and opportunities across all pages. Target: >=30% improvement in brand recognition metrics and >=25% conversion rate lift across all pages over 6 months.

## Leading Indicators

- All marketing pages updated to new brand positioning (100% coverage)
- At least 2 active A/B experiments running at all times
- Conversion monitoring workflow running daily without manual intervention for 4+ weeks
- Bounce rate trending down across all refreshed pages vs. pre-refresh baseline
- Email sequences updated and click-through rates improving vs. pre-refresh baseline

## Instructions

### 1. Expand the brand refresh to all pages

Run the the brand refresh implementation workflow (see instructions below) drill for every remaining marketing page that was not updated in Baseline:

**Phase 1 (weeks 1-2) — High-traffic pages:**
- All feature/product pages
- All case study pages
- Documentation landing page
- Blog index page
- All active landing pages from paid campaigns

**Phase 2 (weeks 3-4) — Long-tail pages:**
- Individual blog posts (update headlines, CTAs, and author bios to match new brand voice)
- Partner/integration pages
- Legal pages (terms, privacy — update company description if applicable)
- 404 page (opportunity for brand personality)

**Phase 3 (weeks 5-6) — Non-website surfaces:**
- Email templates (Loops): welcome sequence, nurture sequence, re-engagement, transactional
- Social media bios and pinned posts
- Third-party listing pages (G2, Product Hunt, Capterra — update descriptions and screenshots)

For blog posts and CMS content, use the Webflow CMS API to batch-update headlines and CTAs programmatically rather than editing each page manually.

### 2. Build the systematic testing pipeline

Run the `ab-test-orchestrator` drill to automate continuous brand experiments:

**Test queue structure:**
Maintain a prioritized queue of experiments in Attio. Each experiment has:
- Variable: what's being tested (headline, CTA, social proof, page layout)
- Hypothesis: why this change should improve conversion
- Page(s): which pages are affected
- Success metric: which KPI determines the winner
- Duration: minimum test period (2 weeks or 1,000 visitors, whichever is longer)

**Automated test execution:**
Build an n8n workflow that:
1. Picks the top experiment from the queue
2. Creates a PostHog feature flag for the test (50/50 split)
3. Deploys the variant in Webflow (using `webflow-site-redesign` fundamental)
4. Monitors test progress daily
5. When statistical significance is reached: evaluates the result, implements the winner, archives the experiment, and picks the next test from the queue

**Test categories to cycle through:**
- **Headlines**: Test benefit-driven vs. outcome-driven vs. question-based H1s
- **CTAs**: Test copy ("Get Started Free" vs. "See How It Works" vs. "Book a Demo"), color, placement
- **Social proof**: Test customer logos vs. testimonial quotes vs. specific metrics ("Used by 500+ teams")
- **Page structure**: Test hero section layouts, feature section order, FAQ placement
- **Lead capture**: Test form fields (fewer vs. more), form placement (inline vs. popup), incentives (free trial vs. content download)

**Velocity target**: 2-3 experiments per month. Each experiment runs for 2-4 weeks depending on traffic volume.

### 3. Deploy always-on conversion monitoring

Run the `dashboard-builder` drill to set up:

**Daily monitoring:**
- n8n workflow checks all page-level metrics against post-refresh baseline
- Detects: bounce rate regressions, conversion rate drops, session duration decreases
- Classifies severity: improving, stable, degrading
- Routes alerts to Slack for degrading metrics

**Weekly brand health report:**
- Overall conversion rate trend (pre-refresh vs. current)
- Page-level performance table (each page's before/after metrics)
- Experiment results from the testing pipeline
- Recommended next experiments based on underperforming pages

**Regression handling:**
If any page's conversion rate drops below pre-refresh baseline for 5+ consecutive days:
1. Alert fires immediately
2. Agent pulls session recordings from that page
3. Agent generates diagnostic hypothesis
4. Agent recommends revert or fix

### 4. Measure cumulative brand impact

Track the overall brand refresh impact over 6 months:

**Quantitative metrics:**
- Overall site conversion rate: compare 30-day rolling average to pre-refresh baseline
- Bounce rate by entry point: track improvement per page
- Brand-related search volume: monitor brand name searches in Google Search Console
- Direct traffic growth: measure visitors arriving via direct URL (brand awareness proxy)

**Qualitative metrics:**
- Session recording analysis: monthly review of 20 recordings to assess user behavior changes
- Support ticket language: are users using terminology from the new positioning?

### 5. Evaluate against threshold

After 6 months:
- **Conversion rate lift >= 25%**: Compare current 30-day conversion rate against pre-refresh baseline.
- **Brand recognition improvement >= 30%**: Measured by direct traffic growth, brand search volume increase, or survey data if available.

Decision tree:
- **PASS**: Brand refresh is working at scale. Proceed to Durable for autonomous optimization.
- **PARTIAL**: Some pages improved significantly but others lag. Focus remaining experiments on underperforming pages. Extend Scalable for 3 more months.
- **FAIL**: Conversion improvement is below 10% after 6 months. The positioning concept may not resonate. Return to Smoke to test a fundamentally different concept.

## Time Estimate

- 20 hours: Full-site brand refresh implementation (all pages, emails, listings)
- 10 hours: Testing pipeline setup (n8n workflows, experiment queue, automation)
- 5 hours: Conversion monitoring setup (dashboard, alerts, reporting)
- 10 hours/month: Experiment production (create variants, review results, implement winners)
- 5 hours/month: Monitoring review, strategy adjustments

**Total: ~75 hours over 6 months (35 setup + ~7/month ongoing)**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, A/B testing, web analytics, session recordings | Free tier or ~$50/mo at scale |
| Webflow | Website pages and CMS content updates | ~$15-40/mo |
| n8n | Test pipeline automation, conversion monitoring, reporting | Free self-hosted or $20/mo cloud |
| Anthropic API | Variant generation, diagnostic analysis | ~$15-30/mo |
| Loops | Email template updates | ~$30/mo |
| Hotjar (optional) | Heatmaps and session recordings (supplement PostHog) | ~$30/mo |

## Drills Referenced

- `ab-test-orchestrator` — Automates the continuous testing pipeline: experiment queue management, feature flag deployment, winner detection, and variant implementation
- `dashboard-builder` — Always-on daily monitoring of page-level conversion metrics with regression detection, weekly health reports, and diagnostic analysis
- the brand refresh implementation workflow (see instructions below) — Executes page updates across remaining marketing pages, CMS content, and email templates
