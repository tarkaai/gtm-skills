---
name: enrich-and-score
description: Run Clay enrichment waterfalls and apply lead scoring to prioritize outreach
category: Enrichment
tools:
  - Clay
  - Clearbit
  - People Data Labs
fundamentals:
  - clay-enrichment-waterfall
  - clay-scoring
  - clay-table-setup
---

# Enrich and Score Prospects

This drill takes a raw contact list and transforms it into a scored, prioritized queue using Clay's enrichment waterfalls and scoring formulas.

## Prerequisites

- Clay account with enrichment credits
- Raw contact list already imported into a Clay table
- ICP definition with weighted scoring criteria

## Steps

### 1. Audit your raw data

Open your Clay table and check data completeness. Identify which columns are missing: email, company size, funding stage, technology stack, LinkedIn URL. The gaps tell you which enrichment providers to prioritize.

### 2. Configure the enrichment waterfall

Using the `clay-enrichment-waterfall` fundamental, set up a multi-provider waterfall for each missing data point. For email: try Clearbit first, then Hunter, then People Data Labs. For firmographics: Clearbit first, then Crunchbase. For technographics: BuiltWith or Wappalyzer. The waterfall stops at the first successful response, conserving credits.

### 3. Run enrichment in batches

Process rows in batches of 50-100 to monitor credit usage and catch errors early. Check the first batch for data quality before running the full table. Look for obviously wrong matches (company name mismatches, outdated titles).

### 4. Build the scoring model

Create a formula column using the `clay-scoring` fundamental. Define your scoring rubric:

- **Company fit (40%)**: size range match, industry match, funding stage, revenue estimate
- **Contact fit (35%)**: title seniority, department match, decision-making authority
- **Timing signals (25%)**: recent funding, job change in last 90 days, hiring for relevant roles, technology adoption signals

Score each factor 0-100, then compute the weighted total.

### 5. Set score thresholds

Define three tiers: Hot (80+), Warm (60-79), Cold (below 60). Filter or color-code rows by tier. Hot leads go to immediate outreach. Warm leads go to nurture sequences. Cold leads get archived or recycled.

### 6. Validate scoring accuracy

Spot-check 10-15 prospects across all tiers. Do the Hot leads genuinely look like your best-fit prospects? If scoring feels off, adjust weights and re-run. Calibrate until your top 20% clearly matches your ICP.

### 7. Export scored results

Push scored and tiered prospects to Attio with their scores and tier labels attached. This feeds directly into outreach drills where sequence priority follows the score.
