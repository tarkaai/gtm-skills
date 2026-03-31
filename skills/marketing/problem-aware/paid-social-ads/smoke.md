---
name: paid-social-ads-smoke
description: >
  Paid Social Ads — Smoke Test. Run targeted LinkedIn and/or Meta ads to problem-aware
  prospects with a $300-1,000 test budget. Validate that your ICP responds to paid social
  by getting at least 2 leads or 1 meeting in 1 week.
stage: "Marketing > Problem Aware"
motion: "Lightweight Paid"
channels: "Paid"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: "≥ 2 leads or ≥ 1 meeting in 1 week"
kpis: ["Cost per lead (CPL)", "Click-through rate (CTR)", "Landing page conversion rate", "Lead-to-ICP match rate"]
slug: "paid-social-ads"
install: "npx gtm-skills add marketing/problem-aware/paid-social-ads"
drills:
  - paid-social-audience-builder
  - paid-social-creative-pipeline
  - ad-campaign-setup
  - landing-page-pipeline
  - threshold-engine
---

# Paid Social Ads — Smoke Test

> **Stage:** Marketing → Problem Aware | **Motion:** Lightweight Paid | **Channels:** Paid

## Outcomes

Get at least 2 leads or 1 meeting from a small paid social test ($300-1,000 budget) in 1 week. This proves that your ICP pays attention on LinkedIn or Meta and responds to problem-aware messaging. You are NOT trying to optimize CPA or prove ROI yet — you are testing whether paid social is a viable channel for reaching problem-aware prospects at all.

## Leading Indicators

- Ad impressions served to the target audience (confirms targeting is working)
- CTR above 0.4% on LinkedIn or 0.8% on Meta (confirms creative resonates)
- Landing page visits from ad clicks (confirms ad-to-page handoff works)
- Form submissions or lead gen form completions (confirms offer is compelling enough)

## Instructions

### 1. Choose one platform to start

Pick LinkedIn OR Meta based on your ICP:
- **Choose LinkedIn if** your ICP is defined by job title, seniority, company size, or industry. LinkedIn's firmographic targeting is unmatched for B2B. Expect CPC of $4-12.
- **Choose Meta if** you have existing website traffic (for retargeting) or a customer email list (for lookalikes). Meta is cheaper (CPC $0.50-3.00) but less precise for B2B.

Do not split a smoke test budget across two platforms. Pick one.

### 2. Build your audience

Run the `paid-social-audience-builder` drill. For the smoke test, build only ONE audience segment:
- On LinkedIn: Core ICP segment (job function + seniority + industry + company size). Target audience size 20,000-80,000.
- On Meta: 1% lookalike from your best customers, or retargeting audience of website visitors from the last 30 days.

Set up exclusions: current customers, your own employees, competitors.

### 3. Create 3 ad variants

Run the `paid-social-creative-pipeline` drill. For the smoke test, create 3 variants using one pain point from your ICP:
- Variant A: Statistic hook (lead with a surprising data point about the problem)
- Variant B: Question hook (ask a question they will answer "yes" to)
- Variant C: Social proof hook (lead with a customer result)

Each ad should offer something educational: a guide, checklist, calculator, or case study. Do NOT pitch your product. Problem-aware prospects are not ready for that.

### 4. Set up the campaign

Run the `ad-campaign-setup` drill with these smoke-test-specific settings:
- **Objective**: Lead Generation (use LinkedIn Lead Gen Forms or Meta Instant Forms for lowest friction) OR Traffic (to a landing page, if you want to test the full funnel)
- **Budget**: $300-1,000 total for the week. Set as a lifetime budget so the platform paces delivery.
- **Bidding**: Use automated bidding (Maximum Delivery on LinkedIn, Lowest Cost on Meta). Do not try to optimize bids on a smoke test.

If using a landing page instead of lead gen forms, run the `landing-page-pipeline` drill to build a single page with: problem-focused headline, offer description, short form (name + email + company), and PostHog tracking.

### 5. Launch and do NOT touch it for 5 days

**Human action required:** Activate the campaign in the ad platform. Set a calendar reminder for 5 days later.

Do NOT optimize mid-flight. The smoke test needs unbiased data. Resist the urge to pause underperforming ads before they have 500+ impressions each.

### 6. Collect and log results

After 5-7 days, pull results from the ad platform:
- Total impressions, clicks, CTR per variant
- Total leads (form submissions or lead gen form completions)
- Cost per lead
- For each lead: name, company, title (check against ICP criteria)

Log in PostHog using `posthog-custom-events`: `paid_social_smoke_impression`, `paid_social_smoke_click`, `paid_social_smoke_lead`.

### 7. Evaluate against threshold

Run the `threshold-engine` drill. Compare results to: **≥ 2 leads or ≥ 1 meeting in 1 week**.

Also check lead quality: of the leads received, how many match your ICP? If you got 5 leads but 0 match your ICP, that is a targeting failure, not a success.

- **PASS (2+ leads, ≥50% ICP match):** Proceed to Baseline. Document which variant performed best and which audience segment.
- **MARGINAL (1 lead, or 2+ leads but <50% ICP match):** Iterate targeting or creative. Try a different pain point or audience segment. Re-run smoke.
- **FAIL (0 leads):** Check CTR first. If CTR < 0.2% (LinkedIn) or < 0.5% (Meta), the creative is not working — test new messaging. If CTR is fine but no conversions, the offer or landing page is the problem. If the platform struggled to spend your budget, the audience is too narrow.

## Time Estimate

- 1 hour: Audience setup + ad creative writing
- 30 minutes: Campaign setup and launch
- 5-7 days: Campaign runs (no active time)
- 1 hour: Results analysis and threshold evaluation
- 30 minutes: Documentation and decision

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn Ads | Ad platform for B2B targeting | $10/day minimum. Expect $4-12 CPC. Budget: $300-1,000 for smoke test. [Pricing](https://business.linkedin.com/marketing-solutions/ads/pricing) |
| Meta Ads | Ad platform for retargeting/lookalikes | $1/day minimum. Expect $0.50-3.00 CPC. Budget: $300-1,000 for smoke test. [Pricing](https://www.facebook.com/business/ads/pricing) |
| Webflow | Landing page (if not using lead gen forms) | $14/mo Basic plan. [Pricing](https://webflow.com/pricing) |
| PostHog | Conversion tracking and analytics | Free up to 1M events/mo. [Pricing](https://posthog.com/pricing) |

**Estimated smoke test cost:** $300-1,000 ad spend + $0-14 tooling = $300-1,014 total

## Drills Referenced

- `paid-social-audience-builder` — build one targeted audience segment on LinkedIn or Meta
- `paid-social-creative-pipeline` — create 3 problem-aware ad variants for the smoke test
- `ad-campaign-setup` — configure the campaign structure, budget, and tracking
- `landing-page-pipeline` — build a dedicated landing page (if not using lead gen forms)
- `threshold-engine` — evaluate smoke test results against the pass threshold
