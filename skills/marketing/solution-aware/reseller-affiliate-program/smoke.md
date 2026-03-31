---
name: reseller-affiliate-program-smoke
description: >
  Reseller & Affiliate Program — Smoke Test. Set up affiliate tracking, recruit
  3-5 partners from your existing network, and validate that partner-referred
  traffic converts to signups before investing in a scaled program.
stage: "Marketing > Solution Aware"
motion: "Partnerships & Warm Intros"
channels: "Other"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥3 active partners and ≥2 partner-sourced signups in 2 weeks"
kpis: ["Partner recruitment rate", "Affiliate link clicks", "Click-to-signup conversion rate"]
slug: "reseller-affiliate-program"
install: "npx gtm-skills add marketing/solution-aware/reseller-affiliate-program"
drills:
  - affiliate-program-design
  - affiliate-recruitment-outreach
---

# Reseller & Affiliate Program — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Other

## Outcomes

A configured affiliate tracking platform with 3-5 active partners from your existing network. At least 2 partner-sourced signups within 2 weeks of partner activation. This proves that your product's value proposition translates through partners — that someone other than you can describe the product and drive conversions — before you invest in building a scaled program.

## Leading Indicators

- At least 3 out of 5 recruited partners generate their first affiliate link click within 7 days (signal: the onboarding kit is clear enough for partners to take action)
- At least 1 partner shares their link without being prompted after the initial pitch (signal: genuine enthusiasm, not just compliance)
- Click-to-signup conversion rate from affiliate traffic exceeds 5% (signal: partner audiences contain qualified prospects)
- At least 1 partner asks about commission rates or payment timing (signal: they see this as a real revenue opportunity)

## Instructions

### 1. Design and configure the affiliate program

Run the `affiliate-program-design` drill with a minimal scope:

- Choose a commission model: start with 20% recurring for 12 months (standard B2B SaaS benchmark). You can adjust after the smoke test.
- Set up Rewardful (if you use Stripe) or FirstPromoter. Both have free trials — no cost for the smoke test.
- Install the tracking snippet on your marketing site and signup flow.
- Create the partner onboarding kit: partner agreement, product one-pager, 3 approved email blurbs, and affiliate portal login instructions.
- Run a test purchase through a test affiliate link to verify end-to-end tracking.

**Human action required:** Complete a test purchase through the affiliate link to verify the tracking works before recruiting real partners.

### 2. Recruit 5 partners from your network

Run the `affiliate-recruitment-outreach` drill with a reduced scope — warm outreach only, no cold:

- Source 5-10 candidates from your existing network: current customers who are consultants or agency owners, founders of complementary products you have a relationship with, advisors or investors with relevant audiences.
- Personalize each outreach. Reference your existing relationship and explain the specific value prop: "You already know [product] — now earn [commission%] for every customer you refer."
- Create an affiliate account and tracking link for each partner who accepts.
- Send them the onboarding kit.

**Human action required:** Personally reach out to 5-10 potential partners. Warm intros and direct outreach only — no cold email at this stage. Log all outreach in Attio.

### 3. Track partner activation

Monitor in Rewardful/FirstPromoter and PostHog:

- Which partners have clicked their own link (testing it)?
- Which partners have generated clicks from their audience?
- Which clicks have converted to signups?
- Which signups have converted to paid?

Log every interaction in Attio: outreach sent, partner accepted, link generated, first click, first referral.

### 4. Evaluate against threshold

After 2 weeks, measure:

- **Active partners**: How many of the recruited partners generated at least 1 click? Target: ≥3
- **Partner-sourced signups**: How many signups came through affiliate links? Target: ≥2

**Pass threshold: ≥3 active partners AND ≥2 partner-sourced signups**

- **Pass**: Document which partner types drove the most value (customer-affiliates vs. SaaS resellers vs. content creators). Note which onboarding kit assets partners actually used. Proceed to Baseline.
- **Marginal**: 2 active partners or 1 signup. Diagnose: Was the commission unappealing? Was the onboarding kit confusing? Did partners not have a natural way to promote? Adjust and re-test with 5 more partners.
- **Fail**: <2 active partners and 0 signups. The product may not be "referrable" yet — partners need a clear, compelling reason to recommend it. Consider: Is the product differentiated enough? Is the ICP too narrow for partners to identify prospects?

## Time Estimate

- Affiliate platform setup and configuration: 2 hours
- Onboarding kit creation: 1 hour
- Partner outreach (5-10 contacts): 1 hour (human action)
- Monitoring and partner support: 1 hour
- Evaluation and documentation: 1 hour

Total: ~6 hours of active work over 1-2 weeks (waiting for partner activation)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Rewardful | Affiliate tracking and commission management | 14-day free trial; Starter $49/mo ([rewardful.com/pricing](https://www.rewardful.com/pricing)) |
| Attio | Partner CRM tracking | Free for up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Click and conversion tracking | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Anthropic Claude | Onboarding kit copywriting | Pay-per-use, ~$0.50 total ([anthropic.com/pricing](https://anthropic.com/pricing)) |

**Estimated cost for this level: Free** (Rewardful free trial covers the smoke test period; all other tools within free tiers)

## Drills Referenced

- `affiliate-program-design` — set up affiliate tracking platform, configure commissions, build onboarding kit
- `affiliate-recruitment-outreach` — source and recruit partners from your existing network (warm outreach only at this level)
