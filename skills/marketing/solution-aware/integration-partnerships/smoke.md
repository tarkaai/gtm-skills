---
name: integration-partnerships-smoke
description: >
  Integration Partnerships — Smoke Test. Identify 3-5 complementary products, assess integration feasibility,
  build one lightweight integration, and co-market it to validate that partner-sourced leads convert.
stage: "Marketing > SolutionAware"
motion: "PartnershipsWarmIntros"
channels: "Product, Content, Email"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥1 integration partnership and ≥5 leads from first partner in 4 weeks"
kpis: ["Partner response rate", "Integration activation count", "Partner-sourced lead count"]
slug: "integration-partnerships"
install: "npx gtm-skills add marketing/solution-aware/integration-partnerships"
drills:
  - warm-intro-request
  - threshold-engine
---

# Integration Partnerships — Smoke Test

> **Stage:** Marketing → SolutionAware | **Motion:** PartnershipsWarmIntros | **Channels:** Product, Content, Email

## Outcomes

One signed integration partnership with a complementary product and at least 5 leads attributed to the partner's audience within 4 weeks of launch. This validates that your product is valuable enough in a partner context to generate inbound interest from their users.

## Leading Indicators

- Partner response rate on outreach (target: ≥30% reply rate from 10 outreach attempts)
- At least 3 partners agree to an exploratory call within 2 weeks
- At least 1 partner agrees to a co-marketing launch within 3 weeks
- Integration landing page receives ≥50 visits from partner-sourced traffic

## Instructions

### 1. Discover and qualify integration partner candidates

Run the the integration partner discovery workflow (see instructions below) drill to identify 10-15 complementary products whose users overlap your ICP. The drill scores each candidate on audience overlap, technical feasibility, and co-marketing potential. Focus on partners with:
- API maturity score ≥ 3 (documented API with at least webhook support)
- Integration type = "Light" (1-2 days to build)
- Audience overlap score ≥ 6/10

Select your top 5 candidates for outreach.

### 2. Reach out to partner candidates

Run the `warm-intro-request` drill to find mutual connections with each partner candidate. Where warm intros are not available, send a direct email to the partnerships/BD contact identified during discovery.

**Human action required:** Send personalized outreach to 5-10 partner candidates. In each message:
- Reference a specific way their users would benefit from the integration
- Propose a concrete first step (e.g., "We could build a webhook integration in 2 days that syncs X data between our products")
- Offer to build the integration on your side with minimal effort required from them
- Log all outreach and responses in Attio

### 3. Build the first integration

Once a partner agrees, build a lightweight integration (webhook listener, API sync, or n8n connector). Keep it minimal:
- One data flow direction (your product -> partner OR partner -> your product)
- One use case (the single most valuable workflow for shared users)
- One setup method (documented in 3 steps or fewer)

**Human action required:** Develop and test the integration. Create a simple landing page explaining what it does, how to set it up, and a CTA to activate.

### 4. Co-market the integration

Write a short announcement for both audiences:
- Your side: email your users who match the partner's product category, post on your blog/social
- Partner side: ask the partner to mention the integration in their newsletter, changelog, or social channels

Track all links with UTM parameters: `utm_source={partner-slug}&utm_medium=integration&utm_campaign=launch-{partner-slug}`

### 5. Evaluate against threshold

Run the `threshold-engine` drill to measure against: ≥1 integration partnership signed AND ≥5 leads from the partner's audience in 4 weeks. If PASS, proceed to Baseline. If FAIL, diagnose: was the integration not useful enough (low activation), or was partner distribution insufficient (low traffic)?

## Time Estimate

- Partner discovery and scoring: 2 hours
- Partner outreach and follow-up: 1 hour
- Integration build (lightweight): 2 hours
- Co-marketing setup and tracking: 1 hour

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Partner research and enrichment | Free tier: 100 credits/mo; Pro: $149/mo (https://www.clay.com/pricing) |
| Attio | CRM for partner tracking | Free tier: 3 users; Plus: $29/user/mo (https://attio.com/pricing) |
| PostHog | Track integration events | Free tier: 1M events/mo (https://posthog.com/pricing) |

## Drills Referenced

- the integration partner discovery workflow (see instructions below) — find and score complementary products as integration candidates
- `warm-intro-request` — map mutual connections and request introductions to partner contacts
- `threshold-engine` — evaluate pass/fail against the play's outcome targets
