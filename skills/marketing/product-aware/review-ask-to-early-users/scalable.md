---
name: review-ask-to-early-users-scalable
description: >
  Review Ask to Early Users — Scalable. Expand review collection across 5+ directories with
  multi-trigger automation, A/B tested ask copy, and incentive programs to hit 20+ reviews.
stage: "Marketing > Product Aware"
motion: "Directories & Marketplaces"
channels: "Other"
level: "Scalable"
time: "60 hours over 2 months"
outcome: "≥ 20 new reviews across 5+ directories and ≥ 15 inbound leads from directories over 2 months"
kpis: ["Total reviews across all directories", "Inbound leads from directories", "Ask-to-review conversion rate", "Average rating across directories", "Cost per review"]
slug: "review-ask-to-early-users"
install: "npx gtm-skills add marketing/product-aware/review-ask-to-early-users"
drills:
  - directory-review-generation
  - directory-performance-monitor
  - ab-test-orchestrator
---

# Review Ask to Early Users — Scalable

> **Stage:** Marketing -> Product Aware | **Motion:** Directories & Marketplaces | **Channels:** Other

## Outcomes

Find the 10x multiplier for review generation. Expand from 2-3 directories to 5+ directories, add trigger-based review asks for every major customer lifecycle event, A/B test ask copy and timing to maximize conversion, and optionally introduce incentive programs. Success = 20+ reviews across 5+ directories and 15+ directory-attributed inbound leads over 2 months, with conversion rates holding within 20% of Baseline.

## Leading Indicators

- Review ask volume: total asks sent per week across all triggers (target: 20-50/week)
- Ask-to-review conversion holding at 15%+ despite higher volume
- Directory coverage: reviews appearing on 5+ platforms, not concentrated on 1-2
- Average rating holding at 4.0+ across all directories
- Directory-sourced traffic week-over-week growth
- Competitive rank position improving on G2 and Capterra

## Instructions

### 1. Expand directory coverage

Using the `directory-review-generation` drill, extend listings and review asks to additional directories:

- **Tier 1 (must-have):** G2, Capterra, Product Hunt (should already be active from Baseline)
- **Tier 2 (add now):** TrustRadius, GetApp, SourceForge
- **Tier 3 (niche, if applicable):** StackShare, AlternativeTo, SaaSWorthy, industry-specific directories

For each new directory:
1. Create an optimized listing using `directory-listing-setup` patterns (UTM-tagged links, keyword-optimized copy, screenshots)
2. Build a new Loops review ask sequence specific to that directory
3. Add the directory to the n8n review monitoring workflow
4. Add the directory to the PostHog dashboard

### 2. Add multi-trigger review ask automation

Expand the Loops triggers from Baseline to cover every positive customer moment:

- **30-day active** (existing from Baseline): Enroll in G2 ask sequence
- **Post-positive-support** (existing): Enroll in Capterra ask sequence
- **Post-upgrade** (existing): Enroll in Product Hunt ask sequence
- **60-day active** (NEW): Enroll in TrustRadius ask sequence (different directory than 30-day)
- **Feature milestone** (NEW): Customer uses a key feature 50+ times. Enroll in GetApp ask sequence.
- **Post-NPS-promoter** (NEW): Customer submits NPS 9-10. Immediately enroll in the directory with the fewest reviews.
- **Annual renewal** (NEW): Customer renews or passes 12 months. Ask for a review update or new review on a different directory.
- **Post-case-study** (NEW): Customer completes a case study interview. Ask for a public review citing similar points.

**Rules:** Max 1 review ask per customer per quarter. If a customer has reviewed on one directory, wait 90 days before asking for a different directory. Never ask a customer with an open support ticket or recent complaint.

Build this logic in n8n using `directory-review-generation` drill patterns. The n8n workflow checks Attio for `last_review_asked_date` and `reviewed_on` before enrolling anyone.

### 3. A/B test ask copy and timing

Run the `ab-test-orchestrator` drill to systematically test review ask variables:

**Test 1 — Subject line (Week 1-2):**
- Control: "Would you share your experience on {directory}?"
- Variant A: "Quick favor? 3 minutes to help other {ICP_role}s"
- Variant B: "{first_name}, your {product} review would mean a lot"
- Metric: email open rate. Need 100+ sends per variant.

**Test 2 — Ask timing (Week 3-4):**
- Control: Ask at 30 days active
- Variant: Ask at 45 days active
- Metric: ask-to-review conversion rate. Need 50+ per variant.

**Test 3 — Email sender (Week 5-6):**
- Control: From founder name
- Variant: From customer success manager name
- Metric: click-through rate on review link.

**Test 4 — Incentive vs no incentive (Week 7-8):**
- Control: No incentive
- Variant: $10 Amazon gift card for leaving an honest review
- Metric: ask-to-review conversion rate and average rating (ensure incentive does not inflate ratings).

Log every test result in PostHog using feature flags. Implement winning variants immediately.

### 4. Launch incentive program (if Test 4 shows uplift)

If incentivized asks convert significantly better without inflating ratings:

- Set up incentive tracking in Attio: `review_incentive_offered`, `review_incentive_type`, `review_incentive_value`, `review_incentive_redeemed`
- Budget: $10-25 per review (gift card or account credit)
- **Compliance:** G2 and Capterra allow incentives but require disclosure. The reviewer must indicate they received an incentive. Never incentivize specific ratings.
- Cap at $500/month incentive budget
- Track cost per review: total incentive spend / reviews collected

### 5. Monitor cross-directory performance

Run the `directory-performance-monitor` drill with expanded scope:

Weekly automated report now covers:
- Review velocity per directory (target: 2-3 new reviews/week total)
- Rating trend per directory (flag any directory dropping below 4.0)
- Competitive rank movement on G2 and Capterra (are new reviews improving your rank?)
- Directory-sourced traffic and leads per directory
- Cost per review (if running incentives)
- A/B test results from active experiments

Set up alerts for:
- Any directory where you fall below 10 total reviews while competitors have 50+ (review gap alert)
- Competitor launches a review campaign (10+ reviews in a single week on G2)
- Your rank drops 5+ positions on any directory

### 6. Evaluate against threshold

After 2 months, measure against: **≥ 20 reviews across 5+ directories AND ≥ 15 inbound leads from directories**.

Calculate:
- Total reviews collected across all directories
- Directory coverage: number of directories with 3+ reviews each
- Average ask-to-review conversion rate
- Average rating (should be 4.0+)
- Total directory-sourced inbound leads
- Cost per review (including incentives if used)
- Cost per directory-sourced lead

If PASS: Proceed to Durable. Document: winning ask copy, best triggers, optimal timing, best-performing directories, incentive ROI.

If FAIL:
- Low volume -> not enough eligible customers being enrolled in sequences. Check trigger coverage — are all positive moments captured?
- Low conversion -> ask fatigue. Refresh copy based on A/B test winners. Try different directory targets.
- Reviews but no leads -> listings need optimization or directories chosen lack buyer traffic. Focus on G2 and Capterra for lead generation.

## Time Estimate

- Directory expansion (3-5 new directories): 6 hours
- Multi-trigger automation build: 8 hours
- A/B test design and implementation (4 tests): 12 hours
- Incentive program setup: 3 hours
- Weekly monitoring and reporting (8 weeks): 16 hours
- Review response management: 10 hours
- Threshold evaluation and documentation: 5 hours
- **Total: ~60 hours over 2 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| G2 | Review directory | Free basic; $299/mo Brand Starter for badges and enhanced profile (https://sell.g2.com/plans) |
| Capterra | Review directory + PPC | Free listing; PPC from $2/click, min $500/mo (https://www.capterra.com/vendors/) |
| Product Hunt | Review directory | Free; Pro $100/mo for analytics (https://www.producthunt.com/) |
| TrustRadius | Review directory | Free vendor profile (https://www.trustradius.com/vendors) |
| GetApp | Review directory | Free via Gartner Digital Markets (https://www.gartner.com/en/digital-markets) |
| Loops | Automated review ask sequences | $49/mo for 1,000+ contacts (https://loops.so/pricing) |
| PostHog | Tracking, dashboards, feature flags for A/B tests | Free up to 1M events/mo (https://posthog.com/pricing) |
| n8n | Multi-trigger automation | Free self-hosted; $20/mo cloud (https://n8n.io/pricing) |
| Attio | CRM for review candidate tracking | Free tier or $29/seat/mo (https://attio.com/pricing) |
| Review incentives | Gift cards or account credits | ~$100-500/mo budget |

**Estimated play-specific cost at Scalable: $150-1,000/mo** (Loops $49 + n8n $20 + review incentives $100-500 + optional G2 Brand Starter $299 + optional Capterra PPC $500)

## Drills Referenced

- `directory-review-generation` — expanded trigger automation and multi-directory review asks
- `directory-performance-monitor` — cross-directory KPI tracking and competitive monitoring
- `ab-test-orchestrator` — systematic testing of ask copy, timing, sender, and incentives
