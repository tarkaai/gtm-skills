---
name: paid-social-audience-builder
description: Build and refine paid social audiences on LinkedIn and Meta targeting problem-aware prospects who match your ICP
category: Paid
tools:
  - LinkedIn Ads
  - Meta Ads
  - Clay
  - Attio
fundamentals:
  - linkedin-ads-audience-targeting
  - meta-ads-audiences
  - clay-people-search
  - clay-scoring
  - attio-lists
---

# Paid Social Audience Builder

This drill builds targeted audiences on LinkedIn and Meta for problem-aware paid social campaigns. Problem-aware prospects know they have a pain point but have not started evaluating solutions. Your audiences must reflect this: target by job function, seniority, and industry (proxy for having the problem), not by intent signals like competitor website visits (that is solution-aware).

## Prerequisites

- ICP defined (run `icp-definition` drill if needed)
- LinkedIn Campaign Manager with Marketing API access
- Meta Business Manager with Marketing API access
- Clay account for enrichment (optional but recommended)
- Attio CRM with at least some closed-won customer data

## Input

- ICP document: firmographic criteria (company size, industry, funding stage) and buyer persona (title, seniority, department)
- Closed-won customer list from Attio (for lookalike audiences on Meta)
- Any existing website visitor data in PostHog

## Steps

### 1. Extract audience signals from your ICP

Pull your ICP criteria from the `icp-definition` drill output. Translate each criterion into platform-specific targeting parameters:

| ICP Criterion | LinkedIn Targeting | Meta Targeting |
|---|---|---|
| Company size 20-200 | `companySize: SIZE_11_50, SIZE_51_200` | Interest-based (no direct firmographic) |
| SaaS / Software industry | `industry: SOFTWARE, INTERNET` | Interest: "SaaS", "Software as a service" |
| VP/Director Engineering | `jobFunction: ENGINEERING, seniority: VP, DIRECTOR` | Custom audience from Clay export |
| Series A-C funded | Not directly available; use company size as proxy | Not available; use lookalike from customer list |

LinkedIn is stronger for B2B firmographic targeting. Meta is stronger for retargeting and lookalikes.

### 2. Build LinkedIn audiences

Using the `linkedin-ads-audience-targeting` fundamental, create 3 audience segments:

**Segment A — Core ICP (tight):**
- Job function + seniority + industry + company size
- Expected size: 20,000-80,000
- This is your highest-quality segment; bid highest here

**Segment B — Adjacent ICP (broader):**
- Same job function and seniority, broader industry or company size range
- Expected size: 80,000-200,000
- Tests whether adjacent markets respond

**Segment C — Title-based (experimental):**
- Specific job titles that your best customers hold (pull from Attio)
- Cross-reference with Clay using `clay-people-search` to validate these titles exist in volume on LinkedIn
- Expected size: varies

For all segments, exclude: your company's employees, existing customers (upload from Attio using `attio-lists`), and competitors.

### 3. Build Meta audiences

Using the `meta-ads-audiences` fundamental, create 3 audience types:

**Custom Audience — Website visitors:**
- Create from Meta Pixel data: visitors to your blog, landing pages, or product pages in the last 30 days who did NOT convert
- These people have shown interest but need another touch

**Lookalike Audience — Best customers:**
- Export your top 20% customers (by deal value or retention) from Attio
- Upload to Meta as a source audience (hash emails with SHA-256)
- Create 1% lookalike for quality, 3% for reach
- Apply geographic and age filters to refine

**Interest-based Audience:**
- Target interests related to the problem your product solves (not the solution category)
- Example: if you sell deploy automation, target "DevOps", "Continuous Integration", "Site Reliability Engineering" — these indicate someone who deals with the problem space
- Layer with demographics: age 25-55, manager+ roles

### 4. Score and validate audience quality

Before spending ad budget, validate that your audiences actually contain ICP-matching people:

- Using `clay-people-search`, sample 50 profiles from your LinkedIn audience criteria. Score them against your ICP using `clay-scoring`. If fewer than 60% score as ICP matches, tighten the audience.
- For Meta lookalikes, you cannot preview members. Instead, run a $50 test for 3 days and check the quality of leads that come in against your ICP criteria.

### 5. Set up audience exclusions

Critical to avoid wasted spend:
- Exclude current customers (Attio export uploaded to both platforms)
- Exclude recent converters (people who submitted a lead form in the last 30 days)
- Exclude disqualified leads (from Attio, if tagged)
- On LinkedIn: exclude your own employees and competitor employees by company name
- On Meta: exclude your custom audience of converters

Refresh exclusion lists weekly via n8n automation.

### 6. Plan audience rotation

Audiences fatigue. Plan a rotation schedule:
- Week 1-2: Run Segment A (core ICP) and Meta Lookalike 1%
- Week 3-4: Add Segment B (adjacent) and Meta Lookalike 3%
- Week 5-6: Test Segment C (title-based) and Meta interest-based
- After 6 weeks: retire exhausted audiences, build new ones based on what converted

Track audience-level performance in PostHog to identify which segments produce the best leads, not just the most clicks.

## Output

- 3 LinkedIn audience segments configured in Campaign Manager
- 3 Meta audience types configured in Ads Manager
- Exclusion lists uploaded and scheduled for weekly refresh
- Audience rotation calendar for 6 weeks
- Validation data: ICP match rate per audience segment
