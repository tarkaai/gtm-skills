---
name: affiliate-recruitment-outreach
description: Find, qualify, and recruit resellers and affiliates through targeted outreach campaigns
category: Partnerships
tools:
  - Clay
  - Attio
  - Instantly
  - Loops
  - Crossbeam
fundamentals:
  - clay-company-search
  - clay-people-search
  - clay-enrichment-waterfall
  - crossbeam-account-mapping
  - attio-lists
  - attio-contacts
  - instantly-campaign
  - loops-sequences
  - affiliate-link-generation
---

# Affiliate Recruitment Outreach

This drill builds and executes a systematic campaign to recruit qualified affiliates and resellers. It identifies candidates from multiple sources, qualifies them on audience fit and reach, and runs personalized outreach sequences to convert them into active partners.

## Input

- ICP definition (who your ideal referred customer is)
- Affiliate program details (commission structure, onboarding kit from `affiliate-program-design`)
- Target number of recruited affiliates (default: 10 for Smoke, 50 for Baseline)
- Existing network contacts who could be early partners

## Steps

### 1. Source affiliate candidates from multiple channels

**Channel A: Complementary SaaS companies**

Use the `clay-company-search` fundamental to find companies that serve the same buyer but are not competitors:

- Same industry vertical as your ICP
- 10-500 employees (big enough to have a partner program, small enough to care about commission revenue)
- Active blog or newsletter (evidence they reach your audience)
- Exclude direct competitors

Pull 100 candidates. These become potential reseller partners.

**Channel B: Content creators and consultants**

Use the `clay-people-search` fundamental to find individuals who create content for your ICP:

- Newsletter authors in your space (Substack, Ghost, ConvertKit creators)
- YouTube creators covering your product category
- Consultants and agencies serving your ICP (implementation partners, strategy consultants)
- Podcast hosts in your vertical
- LinkedIn creators with 5,000+ followers in your industry

Pull 100 candidates. These become potential affiliate partners.

**Channel C: Existing customers with audiences**

Query Attio for current customers who also have an audience:

- Customers with active blogs or newsletters
- Customers who are consultants or agency owners
- Customers who have made introductions before (high NPS, referral history)

Pull 20-50 candidates. These are your highest-conversion recruitment targets because they already use the product.

**Channel D: Crossbeam account overlap (if available)**

Use the `crossbeam-account-mapping` fundamental to find partners with the highest overlap between their customer base and your target accounts. Partners with high overlap can directly introduce your product to warm prospects.

### 2. Enrich and qualify candidates

Use the `clay-enrichment-waterfall` fundamental to add:
- Contact email (verified) and LinkedIn URL for the partnerships/BD/marketing lead
- Company website and social links
- Estimated audience size (newsletter subscribers, social followers, monthly site traffic)
- Content recency (when was the last blog post, newsletter, or video published?)

Score each candidate on a 1-5 scale across three dimensions:

| Dimension | 5 (Excellent) | 3 (Good) | 1 (Poor) |
|-----------|---------------|----------|----------|
| Audience overlap with ICP | >80% overlap | 40-80% | <40% |
| Audience size | >10K reach | 1K-10K | <1K |
| Content activity | Published weekly | Published monthly | Dormant >60 days |

Keep candidates scoring 10+ out of 15. Add qualified candidates to Attio using `attio-lists`.

### 3. Personalize outreach messaging

Use Claude to generate personalized outreach for each candidate tier:

**For SaaS companies (reseller pitch):**
```
Prompt: Write a cold email to {contact_name} at {company_name}, a {company_description}.
Propose a reseller/referral partnership where they earn {commission_rate}% recurring commission
for referring customers to {our_product}. Their product {overlap_reason} complements ours because
{reason}. Reference their {specific_content_or_product} to show research. Keep it under 120 words.
Include a clear CTA: 15-minute call to discuss the partnership.
```

**For content creators (affiliate pitch):**
```
Prompt: Write a cold email to {creator_name}, who runs {newsletter/channel/blog}.
Propose an affiliate partnership where they earn {commission_rate}% for every subscriber they refer.
Reference their recent piece "{content_title}" and explain why their audience would benefit from
{our_product}. Keep it under 100 words. CTA: reply to get their unique affiliate link.
```

**For existing customers (warm referral pitch):**
```
Prompt: Write a warm email to {customer_name} who has been using {our_product} for {duration}.
Mention their usage (e.g., "You've {specific_value_they_got}"). Introduce the partner program:
earn {commission_rate}% for every referral. Since they already know the product, they can
authentically recommend it. Keep it under 80 words. CTA: reply "interested" to get started.
```

### 4. Execute outreach sequences

**For cold outreach (SaaS companies, content creators):**

Use the `instantly-campaign` fundamental to run a 3-touch email sequence:

- **Email 1** (Day 0): Personalized pitch from step 3
- **Email 2** (Day 5): Follow-up with a specific data point ("Partners earn an average of $X/month in commissions")
- **Email 3** (Day 10): Breakup email ("Last note — happy to set this up whenever timing is right")

**For warm outreach (existing customers):**

Use the `loops-sequences` fundamental to send a single warm email. Customers don't need a hard sell — one clear ask is enough.

### 5. Handle responses and onboard

When a candidate replies positively:

1. Use `affiliate-link-generation` to create their affiliate account and tracking link
2. Send the onboarding kit (from `affiliate-program-design`)
3. Update Attio status from "Prospect" to "Onboarding"
4. Schedule a 15-minute partner kickoff call (for resellers) or send async onboarding (for affiliates)

When a candidate replies with questions:
- Route to FAQ document first
- If the question is about commission rates or terms, respond directly with specifics

When a candidate declines:
- Log reason in Attio ("Not interested — wrong timing", "Commission too low", etc.)
- Move to a 90-day re-approach list unless they asked not to be contacted

### 6. Track recruitment funnel

Log every stage in Attio:

```
Sourced → Contacted → Replied → Interested → Onboarding → Active
```

Track conversion rates between each stage to optimize future recruitment campaigns.

## Output

- Qualified list of 50-200 affiliate/reseller candidates in Attio
- Personalized outreach sequences running via Instantly (cold) and Loops (warm)
- Response handling workflow with onboarding integration
- Recruitment funnel metrics in Attio

## Triggers

Run at Smoke level (small batch, 10-20 candidates). Scale at Baseline (50-100 candidates). Automate at Scalable (continuous recruitment pipeline).
