---
name: reseller-affiliate-program-baseline
description: >
  Reseller & Affiliate Program — Baseline Run. First always-on automation:
  systematic affiliate recruitment via cold outreach, automated onboarding,
  and PostHog tracking to prove repeatable partner-sourced revenue.
stage: "Marketing > Solution Aware"
motion: "Partnerships & Warm Intros"
channels: "Other"
level: "Baseline Run"
time: "18 hours over 4 weeks"
outcome: "≥10 active partners and ≥8 partner-sourced paid conversions in 6 weeks"
kpis: ["Partner activation rate", "Click-to-paid conversion rate", "Revenue per active partner", "Commission ROI"]
slug: "reseller-affiliate-program"
install: "npx gtm-skills add marketing/solution-aware/reseller-affiliate-program"
drills:
  - affiliate-recruitment-outreach
---

# Reseller & Affiliate Program — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Other

## Outcomes

A systematic recruitment pipeline producing 10+ active affiliates/resellers who generate at least 8 paid conversions in 6 weeks. Automated onboarding handles partner activation without manual work. PostHog tracking attributes every click, signup, and conversion to the specific partner who referred it. This proves the affiliate channel generates repeatable revenue — not just one-off referrals from friends — before you invest in scaling.

## Leading Indicators

- Cold outreach to affiliate candidates achieves >15% positive reply rate (signal: the partnership pitch resonates beyond your warm network)
- >50% of onboarded partners generate their first click within 14 days (signal: onboarding automation is effective)
- At least 3 distinct partner types (SaaS resellers, content creators, customer-affiliates) produce conversions (signal: the program works across partner categories, not just one niche)
- Referred customers' 30-day retention rate matches or exceeds direct-acquisition customers (signal: partner-sourced leads are qualified, not just volume)

## Instructions

### 1. Scale affiliate recruitment beyond your network

Run the `affiliate-recruitment-outreach` drill at full scope:

- **Source 100 candidates** across 3 channels:
  - 40 complementary SaaS companies (use Clay company search with ICP overlap filters)
  - 40 content creators and consultants (newsletter authors, YouTube creators, LinkedIn influencers in your vertical)
  - 20 existing customers with audiences (consultants, agency owners, power users with blogs)
- **Enrich and qualify** using Clay: verified email, audience size estimate, content recency. Score on audience overlap, size, and activity. Keep candidates scoring 10+/15.
- **Run personalized cold outreach** via Instantly: 3-touch sequence for SaaS companies and content creators. Use Loops for warm sequences to existing customers.
- **Target**: 50 candidates contacted, 15-20 positive replies, 10+ partners onboarded.

### 2. Automate partner onboarding

Run the the affiliate onboarding automation workflow (see instructions below) drill to eliminate manual onboarding:

- Build the n8n workflow: when Attio status changes to "Onboarding," auto-create affiliate account in Rewardful, generate tracking link, send welcome email with onboarding kit via Loops.
- Deploy the 21-day enablement drip: Day 0 (welcome + link), Day 2 (marketing toolkit), Day 5 (how top partners promote), Day 10 (activation nudge), Day 21 (check-in).
- Set up activation milestone tracking: first click detection, first referral celebration, stale partner detection at 30 and 60 days.
- Configure the onboarding health dashboard in PostHog: track median time from onboarding to first click and activation rate.

### 3. Configure comprehensive tracking

Set up PostHog events to track the full affiliate funnel:

| Event | Fires When | Properties |
|-------|-----------|------------|
| `affiliate_link_click` | Visitor arrives via affiliate URL | `affiliate_slug`, `utm_source`, `landing_page` |
| `affiliate_signup` | Referred visitor creates account | `affiliate_slug`, `signup_method` |
| `affiliate_trial_start` | Referred visitor starts trial | `affiliate_slug`, `plan` |
| `affiliate_conversion` | Referred visitor converts to paid | `affiliate_slug`, `plan`, `revenue`, `mrr` |
| `affiliate_commission_earned` | Commission calculated | `affiliate_slug`, `commission_amount`, `commission_type` |

Tag all affiliate traffic with UTM parameters: `utm_source=affiliate&utm_medium=partner&utm_campaign=reseller-program&utm_content={affiliate_slug}`

### 4. Run the program for 4-6 weeks

- Week 1-2: Recruit and onboard partners. Monitor onboarding automation for errors.
- Week 2-4: Partners begin promoting. Monitor click volume and conversion rates per partner.
- Week 4-6: Evaluate performance. Identify top-performing partner types and promotion formats.

Track per-partner metrics weekly in Attio:
- Clicks generated
- Signups attributed
- Paid conversions
- Revenue generated
- Commissions earned
- Commission ROI (revenue / commissions)

### 5. Evaluate against threshold

After 6 weeks, measure:

- **Active partners**: Partners who generated at least 1 click in the last 30 days. Target: ≥10
- **Partner-sourced paid conversions**: Customers who converted to paid through an affiliate link. Target: ≥8
- **Commission ROI**: Total affiliate revenue / total commissions paid. Target: ≥3x

**Pass threshold: ≥10 active partners AND ≥8 partner-sourced paid conversions**

- **Pass**: Document which partner types (SaaS reseller, content creator, customer-affiliate) drive the highest ROI. Note which onboarding touchpoints correlate with faster activation. Proceed to Scalable.
- **Marginal**: 6-9 active partners or 4-7 conversions. Analyze: Is recruitment the bottleneck (not enough partners) or activation (partners not promoting)? Focus the fix accordingly.
- **Fail**: <6 active partners and <4 conversions. Diagnose: Is the commission structure competitive? Is the product easy to recommend? Do partners have a natural context to promote? Consider whether the affiliate model fits your product or if a different partnership format (co-selling, integrations) would work better.

## Time Estimate

- Recruitment campaign setup and execution: 6 hours
- Onboarding automation build: 4 hours
- PostHog tracking configuration: 2 hours
- Partner support and monitoring (weeks 2-6): 4 hours
- Analysis and evaluation: 2 hours

Total: ~18 hours of active work over 4-6 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Rewardful | Affiliate tracking and commissions | Starter: $49/mo ([rewardful.com/pricing](https://www.rewardful.com/pricing)) |
| Clay | Partner candidate research and enrichment | Launch: $185/mo ([clay.com/pricing](https://www.clay.com/pricing)) |
| Attio | Partner CRM and pipeline tracking | Free for up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Affiliate funnel tracking and analytics | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Instantly | Cold outreach to affiliate candidates | Growth: $30/mo ([instantly.ai/pricing](https://instantly.ai/pricing)) |
| Loops | Partner onboarding drip sequences | Free up to 1,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| Anthropic Claude | Outreach personalization and copywriting | ~$2-5/mo at this usage ([anthropic.com/pricing](https://anthropic.com/pricing)) |

**Estimated cost for this level: ~$80-265/mo** (Rewardful + Clay required; Instantly and Loops within free tiers for small volume)

## Drills Referenced

- `affiliate-recruitment-outreach` — systematic candidate sourcing, qualification, and cold/warm outreach sequences
- the affiliate onboarding automation workflow (see instructions below) — zero-touch partner onboarding, enablement drip, and activation tracking
