---
name: self-serve-signup-optimization-scalable
description: >
  Signup Funnel Optimization — Scalable Automation. Personalize signup flows by segment, run
  systematic A/B tests on copy and layout, and recover abandoned signups across all channels.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Website, Product"
level: "Scalable Automation"
time: "40 hours over 2 months"
outcome: "≥50% signup CVR across 500+ monthly signups with per-segment personalization live"
kpis: ["Overall signup CVR", "Per-segment CVR", "Experiment win rate", "Abandoned signup recovery rate"]
slug: "self-serve-signup-optimization"
install: "npx gtm-skills add product/onboard/self-serve-signup-optimization"
drills:
  - ab-test-orchestrator
---

# Signup Funnel Optimization — Scalable Automation

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Website, Product

## Outcomes

Signup flow automatically adapts to the visitor: mobile users see a mobile-optimized flow, paid traffic visitors see copy matched to the ad, content readers see a softer entry point. A/B testing runs continuously on form copy, layout, and CTA placement. Abandoned signups are recovered via segment-specific nurture. Overall signup CVR reaches 50%+ across 500+ monthly signups.

## Leading Indicators

- Per-segment CVR converging upward as personalized variants win
- At least 2 A/B tests completed per month with clear winners or learnings
- Abandoned signup recovery emails generating measurable re-entries
- No segment converting at less than 50% of the overall average
- Experiment documentation accumulating a knowledge base of what works

## Instructions

### 1. Launch systematic A/B testing

Run the `ab-test-orchestrator` drill to set up a continuous testing program for the signup flow. Test these elements in priority order:

1. **Headline copy**: Test 3 variants of the signup page headline (benefit-focused, social-proof-focused, action-focused). Use PostHog experiments with the `signup_completed` event as the primary metric.
2. **Form layout**: Test reduced-field form (email only) vs standard form (email + name + company). Measure both signup CVR and downstream activation rate to catch quality trade-offs.
3. **CTA button copy**: Test action-specific CTAs ("Start building free" vs "Create account" vs "Get started in 60 seconds").
4. **Social proof placement**: Test customer logos above vs below the form, or a real-time counter ("X teams signed up this week").

Rules from `ab-test-orchestrator`: run one test at a time, require 200+ samples per variant, do not peek at results early, and document every test outcome regardless of whether it won.

### 2. Personalize by segment

Run the the signup flow personalization workflow (see instructions below) drill. Analyze PostHog cohorts to find segments where conversion diverges significantly from the mean:

- **Mobile visitors**: if mobile CVR < 60% of desktop, deploy the mobile-optimized variant (single-column, OAuth-first, minimal fields)
- **Paid traffic**: if paid CVR < organic CVR, deploy message-matched landing pages with simplified forms
- **Blog/content readers**: if content CVR < direct CVR, deploy a softer entry (free tool or template before full signup)
- **Referral visitors**: deploy pre-filled referral badges and incentive offers

Each personalized variant runs as a PostHog experiment. After 14+ days with 200+ conversions per variant, promote winners and retire losers.

### 3. Build abandoned signup recovery

Using the partial-signup nurture from the signup flow personalization workflow (see instructions below):

- Configure n8n to detect users who focused the signup form but did not complete within 24 hours
- If the user entered an email (captured via partial form data or PostHog person properties), enroll them in a segment-specific Loops recovery sequence:
  - Mobile abandoned: email with deep link to mobile-optimized page
  - Paid abandoned: email with simplified value prop matching original ad
  - Generic abandoned: email with social proof and direct signup link
- Track recovery rate: what percentage of abandoned signups return and complete

### 4. Evaluate against threshold

Measure against the pass criteria:

- Overall signup CVR >= 50% (calculated as signup_completed / signup_page_viewed across all segments)
- Monthly signup volume >= 500
- Per-segment personalization deployed for at least 2 underperforming segments
- At least 4 A/B tests completed with documented outcomes

If CVR is below 50% at 500+ volume, focus testing on the segment with the lowest absolute conversion contribution (largest segment x lowest CVR = biggest opportunity).

## Time Estimate

- 8 hours: Set up A/B testing infrastructure and first 2 experiments
- 12 hours: Build and deploy 2-4 personalized signup variants
- 6 hours: Configure abandoned signup recovery workflows
- 8 weeks: Run experiments and personalization variants (mostly passive)
- 4 hours: Analyze segment results, promote winners
- 2 hours: Final threshold evaluation and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, cohorts, funnels | Free tier: 1M events + 1M flag requests/mo. Paid: usage-based. [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | Segment-specific help bots on signup pages | Essential: $29/seat/mo. Advanced: $85/seat/mo. [intercom.com/pricing](https://www.intercom.com/pricing) |
| n8n | A/B test routing, recovery workflows, monitoring | Community (self-hosted): Free. Cloud Pro: ~$60/mo for 10K executions. [n8n.io/pricing](https://n8n.io/pricing/) |
| Loops | Abandoned signup recovery email sequences | Free tier: 1,000 contacts. Growth: from $49/mo. [loops.so/pricing](https://loops.so/pricing) |

## Drills Referenced

- `ab-test-orchestrator` — designs, runs, and analyzes A/B tests with statistical rigor on signup flow elements
- the signup flow personalization workflow (see instructions below) — builds segment-specific signup variants, deploys via feature flags, and recovers abandoned signups
