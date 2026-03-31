---
name: affiliate-program-design
description: Design an affiliate/reseller program — commission structure, terms, onboarding kit, and tracking setup
category: Partnerships
tools:
  - Rewardful
  - FirstPromoter
  - Attio
  - Anthropic
fundamentals:
  - affiliate-program-setup
  - affiliate-commission-configuration
  - affiliate-link-generation
  - attio-lists
  - attio-custom-attributes
---

# Affiliate Program Design

This drill takes you from zero to a fully configured affiliate/reseller program. It defines the economics, sets up the tracking platform, builds the partner terms, and prepares the onboarding kit — everything needed before you recruit your first affiliate.

## Input

- Your product's pricing tiers and margins
- Target CAC (customer acquisition cost) ceiling
- ICP definition (who your ideal referred customer is)
- Decision: affiliate model (referral link commission) vs. reseller model (partners sell directly at a margin) vs. hybrid

## Steps

### 1. Define the commission economics

Calculate the maximum commission you can pay while staying below target CAC:

```
max_commission_per_customer = target_CAC - overhead_per_acquisition
commission_as_pct_of_ACV = max_commission_per_customer / annual_contract_value * 100
```

Use Claude to model scenarios:

**Prompt to Claude:**
```
I run a SaaS product priced at ${ACV}/year with a target CAC of ${target_CAC}.
My gross margin is {margin}%. My current blended CAC from other channels is ${current_CAC}.

Model 3 affiliate commission structures:
1. One-time flat fee per conversion
2. Percentage of first-year revenue (non-recurring)
3. Recurring percentage for 12 months

For each, calculate: max sustainable commission rate, break-even months, and impact on unit economics.
Compare to industry benchmarks (B2B SaaS affiliate programs typically pay 15-30% recurring for 12 months).
```

Store the chosen commission structure. Proceed to configuration.

### 2. Set up the affiliate platform

Run the `affiliate-program-setup` fundamental to create and configure the tracking platform. Choose based on your payment processor:

- Stripe users: Rewardful (simplest integration) or FirstPromoter
- Paddle users: Rewardful or Tapfiliate
- Custom billing: PartnerStack or Tapfiliate (more flexible webhook integrations)

### 3. Configure commissions and payouts

Run the `affiliate-commission-configuration` fundamental with the commission structure from step 1. Configure:

- Commission rate and type (percentage or flat)
- Recurring vs. one-time
- Tier structure if applicable (higher commission for higher-volume partners)
- Cookie duration (90 days recommended for B2B)
- Payout minimum ($50), frequency (monthly), and delay (30 days)

### 4. Draft the partner agreement

Use Claude to generate the partner terms document:

**Prompt to Claude:**
```
Draft a concise affiliate/reseller partner agreement for a B2B SaaS company. Include:
- Commission structure: {commission_details}
- Cookie duration: {days} days
- Payout terms: Monthly, minimum ${min}, 30-day delay
- Prohibited activities: brand bidding on paid search, spam, misleading claims
- Termination: Either party can terminate with 30 days notice; earned commissions still paid
- Brand usage: Partners may use approved logos and copy only
- Non-exclusivity: Partners can promote competing products

Keep it under 1,500 words. Plain language, no legalese. Format as markdown.
```

Store the agreement. Partners will accept it during onboarding.

### 5. Build the partner onboarding kit

Create a resource package that new affiliates receive upon acceptance:

**Assets to prepare:**
- Partner agreement (from step 4)
- Product one-pager (value prop, ICP, key differentiators)
- Approved marketing copy (3-5 email blurbs, 3-5 social posts, 2-3 blog snippets)
- Brand assets (logo files, color codes, screenshot library)
- FAQ document (how tracking works, how payouts work, what support is available)
- Affiliate portal login instructions

Use Claude to generate the marketing copy variants:

**Prompt to Claude:**
```
Write affiliate marketing copy for {product_name}. The product {product_description}.
Target audience: {ICP_description}.

Generate:
- 3 email blurbs (60-100 words each, different angles: problem-agitation-solution, social proof, feature highlight)
- 3 social media posts (LinkedIn-style, 150 words max each)
- 2 blog paragraph inserts (200 words each, educational tone that naturally mentions the product)

Each must include a placeholder for the affiliate's tracking link: {AFFILIATE_LINK}
```

### 6. Configure CRM tracking

Using the `attio-lists` and `attio-custom-attributes` fundamentals:

Create an Attio list called "Affiliate Partners" with fields:
- Partner name, email, company
- Affiliate platform ID
- Commission tier (Standard / Silver / Gold)
- Signup date
- Total referrals (lifetime)
- Total revenue generated
- Total commissions earned
- Total commissions paid
- Status (Applied / Approved / Active / Paused / Churned)
- Last referral date
- Partner health score

### 7. Generate initial test links

Run the `affiliate-link-generation` fundamental to create 2-3 test affiliate accounts (your own email, a teammate, etc.) and verify the full tracking flow:

1. Click an affiliate link
2. Verify the cookie is set
3. Complete a test signup/purchase
4. Verify the referral and commission appear in the affiliate platform
5. Verify the event fires in PostHog with correct UTM attribution

**Human action required:** Complete a test purchase through the affiliate link to verify end-to-end tracking.

## Output

- Configured affiliate platform with tracking installed
- Commission structure aligned to unit economics
- Partner agreement document
- Onboarding kit with marketing assets
- CRM list and fields for partner tracking
- Verified end-to-end tracking flow

## Triggers

Run once during Smoke Test setup. Revisit commission structure quarterly based on performance data.
