---
name: testimonial-collection-scalable
description: >
  Systematic Testimonial Collection — Scalable Automation. A/B test collection
  methods, segment by ICP and use case, scale to ≥50 testimonials per 2 months
  with targeted inventory coverage across verticals and personas.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥50 testimonials in 2 months with coverage across ≥3 verticals and ≥2 personas"
kpis: ["Collection rate", "Quality score", "Submission rate", "Inventory coverage", "Segment metrics"]
slug: "testimonial-collection"
install: "npx gtm-skills add product/referrals/testimonial-collection"
drills:
  - ab-test-orchestrator
  - power-user-scoring
  - dashboard-builder
---
# Systematic Testimonial Collection — Scalable Automation

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes
Scale testimonial collection to 50+ per 2-month period without proportional manual effort. Build a testimonial inventory with deliberate coverage across at least 3 industry verticals and 2 buyer personas. Optimize every stage of the collection funnel through systematic A/B testing.

## Leading Indicators
- Request-to-submission conversion rate ≥30% (up from Baseline's 25%+ target)
- Average quality score ≥4.0 (up from Baseline's 3.5)
- At least 10 testimonials with video willingness
- Inventory gap score decreasing week over week (fewer uncovered segments)

## Instructions

### 1. A/B test every funnel stage
Run the `ab-test-orchestrator` drill to systematically optimize the testimonial collection pipeline. Test one variable at a time with PostHog feature flags:

**Request copy tests:**
- Test direct ask ("Share your experience in 3 minutes") vs social proof ask ("Join 50+ customers who shared their story")
- Test trigger-specific vs generic messages: does referencing the exact trigger event ("You just hit 100 projects") outperform a general ask?
- Test in-app message format: Intercom post vs tooltip vs chat message

**Form optimization tests:**
- Test long form (8 questions) vs short form (3 questions: role, outcome, quote permission)
- Test with vs without example text in form fields
- Test with vs without a progress bar
- Test incentivized ("Get a $25 gift card") vs unincentivized submission

**Timing tests:**
- Test immediate (within 1 hour of trigger) vs delayed (24 hours after trigger) vs next-day (next morning)
- Test weekday vs weekend requests

Run each test for statistical significance (minimum 100 per variant or 2 weeks, whichever is longer). Document every result in Attio.

### 2. Build segmented collection targeting
Run the `power-user-scoring` drill to enrich your testimonial candidate pool with scored data. Then build segmented targeting:

1. Map your current testimonial inventory by: industry vertical, company size, buyer persona (role), use case, and plan tier
2. Identify coverage gaps: which segments have fewer than 3 testimonials?
3. Create PostHog cohorts for each underrepresented segment
4. Prioritize requests to users in gap segments by weighting their candidate score higher in the n8n routing logic
5. For critical gaps (e.g., zero enterprise testimonials), create a dedicated outreach track: personalized email from the founder or CS lead, offering a video call instead of a form

This converts testimonial collection from "whoever responds" to "strategically filling inventory gaps for sales enablement."

### 3. Build the testimonial operations dashboard
Run the `dashboard-builder` drill to create a PostHog dashboard with:

- **Collection funnel**: requests → opens → submissions → published (with conversion rates at each step)
- **Volume trend**: testimonials collected per week, trailing 8 weeks
- **Quality distribution**: histogram of quality scores, with 3.5 threshold line
- **Inventory heatmap**: grid of verticals x personas, color-coded by coverage (red = 0-1, yellow = 2-3, green = 4+)
- **A/B test tracker**: active experiments, sample sizes, preliminary results
- **Top testimonials**: highest quality score submissions this month with pull quotes

Set alerts:
- Weekly collection rate drops below 5 per week for 2 consecutive weeks
- Any segment drops to 0 fresh testimonials (published in last 90 days)
- Form submission rate drops below 25%

### 4. Evaluate against threshold
Measure against: ≥50 testimonials in 2 months with coverage across ≥3 verticals and ≥2 personas. If PASS, proceed to Durable. If FAIL, focus on the highest-leverage experiment result and double down on the winning variant.

## Time Estimate
- 15 hours: design and launch A/B tests across request copy, form, and timing
- 15 hours: build segmented targeting with inventory gap analysis
- 10 hours: build the operations dashboard with alerts
- 20 hours: monitor tests, analyze results, implement winners, iterate

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| Typeform | Testimonial forms (multiple variants for A/B tests) | $25/mo Basic or $50/mo Plus (unlimited responses) |
| PostHog | Feature flags, experiments, funnels, dashboards | Free tier or $0.00045/event beyond 1M |
| n8n | Automation: segmented routing, test allocation, processing | Self-hosted free or $20/mo cloud |
| Attio | Testimonial inventory tracking, segment metadata | Included in standard stack |
| Intercom | In-app message variants for A/B tests | Included in standard stack |
| Loops | Email variants for A/B tests | Included in standard stack |

**Play-specific cost:** ~$45-70/mo (Typeform Plus + n8n cloud)

## Drills Referenced
- `ab-test-orchestrator` — systematic testing of request copy, form design, timing, and incentives
- `power-user-scoring` — enrich candidate pool with scored data for segmented targeting
- `dashboard-builder` — testimonial operations dashboard with funnel, inventory, and experiment tracking

---

## Pass threshold
**≥50 testimonials in 2 months with coverage across ≥3 verticals and ≥2 personas**

If you hit this threshold, move to the **Durable Intelligence** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/referrals/testimonial-collection`_
