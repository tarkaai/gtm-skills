---
name: partner-prospect-research
description: Find, audit, and qualify newsletter partners whose audiences overlap your ICP
category: Partnerships
tools:
  - Clay
  - Attio
  - Crossbeam
fundamentals:
  - clay-company-search
  - clay-enrichment-waterfall
  - partner-newsletter-audit
  - crossbeam-account-mapping
  - attio-lists
---

# Partner Prospect Research

This drill identifies companies with newsletters whose audiences overlap your ICP, audits their newsletters for fit and reach, and produces a ranked partner prospect list ready for outreach.

## Input

- Your ICP definition (firmographics, buyer persona, pain points)
- Minimum audience size threshold (default: 1,000 subscribers)
- Target number of qualified partners (default: 20)

## Steps

### 1. Source partner candidates from Clay

Use the `clay-company-search` fundamental to find companies that share your ICP's audience but are not competitors. Search for:
- Companies in adjacent categories (complementary products, not substitutes)
- Companies serving the same buyer persona (same titles, same industries)
- Companies at a similar or larger stage (their newsletter needs to have meaningful reach)

Set Clay filters: industry overlap with your ICP, employee count 10-500, and exclude companies in your direct competitive set. Pull 100-200 candidates.

### 2. Enrich partner candidates

Use the `clay-enrichment-waterfall` fundamental to add:
- Company domain and website
- LinkedIn company URL
- Employee count and funding stage
- Contact info for the partnerships/marketing lead (name, email, LinkedIn)

### 3. Audit each partner's newsletter

For the top 50 candidates (sorted by company fit), run the `partner-newsletter-audit` fundamental. For each partner, assess:
- Does the newsletter exist and is it active?
- What is the estimated subscriber count?
- Does the audience match your ICP?
- Do they already feature partner content?

Score each newsletter on the 1-5 scale across four dimensions (audience overlap, audience size, engagement quality, co-marketing friendliness). Keep partners scoring 14+ out of 20.

### 4. Check account overlap with Crossbeam

If you have Crossbeam configured, use the `crossbeam-account-mapping` fundamental to check which partners share the most overlapping target accounts. Partners with high account overlap are the highest-value co-marketing targets because their readers are literally your prospects.

### 5. Build the ranked partner list in Attio

Use the `attio-lists` fundamental to create a list called "Newsletter Partners — {date}". Add qualified partners with fields:
- Company name and domain
- Newsletter name and signup URL
- Estimated subscriber count
- Newsletter score (out of 20)
- Account overlap count (from Crossbeam, if available)
- Contact name, email, and LinkedIn URL for the partnerships/marketing lead
- Status: "Prospect" (initial state)

Sort by newsletter score descending. The top 10-20 are your outreach targets.

## Output

- Ranked list of 10-20 qualified newsletter partners in Attio
- Each partner scored on newsletter quality, audience fit, and account overlap
- Contact info for the right person at each partner company
- Ready for outreach via the `warm-intro-request` or `cold-email-sequence` drill

## Triggers

Run this drill once at Smoke level, then quarterly at Baseline+ to refresh the partner pipeline.
