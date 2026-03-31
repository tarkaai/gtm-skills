---
name: industry-research-production
description: End-to-end workflow for producing an original data-driven industry report from topic selection through final publication
category: Research
tools:
  - Anthropic
  - Clay
  - Typeform
  - Tally
  - Google Sheets
  - Ghost
fundamentals:
  - ai-content-ghostwriting
  - clay-claygent
  - clay-enrichment-waterfall
  - typeform-survey-setup
  - tally-form-setup
  - ghost-blog-publishing
  - news-signal-search
  - competitive-intel-aggregation
---

# Industry Research Production

This drill produces a single data-driven industry report from scratch: topic validation, data collection, analysis, writing, and publication. The output is a hosted, gated or ungated report ready for distribution. Designed for founder-led content plays targeting problem-aware audiences.

## Input

- ICP definition (from `icp-definition` drill): target titles, company sizes, pain points
- Founder's domain expertise and any proprietary data sources (product usage data, customer conversations, internal benchmarks)
- Competitive landscape: what reports competitors have already published
- Distribution plan: how and where the report will be promoted (feeds into `report-distribution-pipeline` drill)

## Steps

### 1. Identify the report topic

Use the `news-signal-search` fundamental to scan for trending industry topics in the last 90 days. Query news APIs and social listening for:
- Pain points your ICP mentions repeatedly on LinkedIn, Reddit, and industry forums
- Emerging trends without authoritative data (the gap you can fill)
- Regulatory, market, or technology shifts creating uncertainty

Use the `competitive-intel-aggregation` fundamental to audit existing reports from competitors and analysts:
- Search for "{industry} + report/benchmark/survey + {year}" on Google
- Document: who published it, what data they used, what conclusions they drew, what gaps remain
- Prioritize topics where existing reports are >12 months old, rely on anecdotal evidence, or miss your ICP's specific context

Select a topic that meets all three criteria: (a) your ICP actively cares about it, (b) no authoritative recent data exists, (c) you can collect original data.

### 2. Design the data collection methodology

Choose one or more data sources based on what you can access:

**Option A -- Survey-based (best for benchmarks and "state of" reports):**
Use the `typeform-survey-setup` or `tally-form-setup` fundamental to build a 10-15 question survey. Keep it under 5 minutes to complete. Structure:
- 3 demographic/firmographic questions (company size, role, industry)
- 5-8 quantitative questions (Likert scales, numeric ranges, multiple choice)
- 2-3 open-ended questions (qualitative insights for quotes)

Target: minimum 50 responses for statistical relevance. For niche B2B, 30-50 is acceptable if the respondent profile is well-defined.

**Option B -- Enrichment-based (best for landscape and market maps):**
Use the `clay-claygent` fundamental to research 100-200 companies matching your ICP. For each, ask Claygent structured questions about their approach to {topic}: tooling, team size, process maturity, public statements. Aggregate into quantitative patterns.

Use the `clay-enrichment-waterfall` fundamental to pull firmographic data (headcount, funding, tech stack) for each company. Cross-reference with the qualitative findings to identify correlations (e.g., "companies with >100 employees are 3x more likely to have a dedicated {function}").

**Option C -- Product data (best for benchmark reports):**
If your product generates usage data relevant to the topic, anonymize and aggregate it. Example: "We analyzed {N} accounts over {time period} and found {insight}." Even 20-50 data points create credibility when the methodology is transparent.

**Option D -- Public data scraping (best for market landscape reports):**
Use `clay-claygent` to pull data from public sources: job postings mentioning relevant skills/tools, G2/Capterra review trends, GitHub stars, app store rankings, or SEC filings. Structure the queries to produce comparable data across companies.

### 3. Collect and clean the data

Execute the collection method chosen in step 2:

For surveys:
- Distribute via email to existing contacts, LinkedIn posts, and relevant communities
- Use the `loops-broadcasts` fundamental to email your subscriber list with the survey link
- Offer incentive: early access to the report or an executive summary
- Run collection for 2-3 weeks minimum
- Clean data: remove incomplete responses, flag outliers, verify no duplicate submissions

For enrichment/scraping:
- Run Clay tables and verify output quality on first 10 rows before scaling
- Flag data points that seem anomalous and verify manually
- Structure all data in a consistent schema (Google Sheets or CSV)

### 4. Analyze the data

Load cleaned data into Google Sheets or a pandas notebook. Produce:

- **Summary statistics**: mean, median, distribution for each quantitative variable
- **Cross-tabulations**: break metrics by company size, industry, maturity level
- **Key findings**: 5-8 data-backed insights that surprised you or contradict conventional wisdom
- **Quotable statistics**: 3-5 headline numbers that are shareable on social media (e.g., "72% of B2B teams still do X manually")
- **Visualizations**: 4-6 charts (bar charts, pie charts, scatter plots) suitable for embedding in the report and extracting as social graphics

Use the Anthropic API to assist with analysis:
```
POST https://api.anthropic.com/v1/messages

System: "You are a data analyst reviewing survey/research results for an industry report. Identify the 5 most surprising or actionable findings. For each, provide: the specific data point, why it matters to {ICP_DESCRIPTION}, and a one-sentence headline suitable for social media."

User: "Here is the raw data summary: {DATA_SUMMARY}. Here are the cross-tabulations: {CROSS_TABS}."
```

### 5. Write the report

Using the `ai-content-ghostwriting` fundamental, generate the report via the Anthropic API:

```
POST https://api.anthropic.com/v1/messages

System: "You are writing an industry report authored by {FOUNDER_NAME}, founder of {COMPANY}. The report targets {ICP_DESCRIPTION} who are problem-aware about {PAIN_POINT}. Write in the founder's voice: {VOICE_PROFILE}. Requirements:
- Executive summary (200 words): headline findings and why they matter
- Methodology section (100 words): how data was collected, sample size, limitations
- 5-8 findings sections: each with a headline stat, supporting data, chart reference, and actionable recommendation
- Conclusion: what this means for the reader's business
- Soft CTA: single mention of {PRODUCT} as relevant context, not a pitch
- Total length: 2,000-4,000 words depending on findings depth"

User: "Key findings: {FINDINGS}. Raw data summary: {DATA_SUMMARY}. Charts available: {CHART_LIST}. Competing reports and their gaps: {COMPETITOR_ANALYSIS}."
```

**Human action required:** Founder reviews the full draft. Key checks:
- Are all data points accurate and sourced correctly?
- Do the conclusions follow from the data (not AI hallucination)?
- Does the report contain at least one genuinely surprising insight?
- Does it read as the founder's perspective, not generic analyst language?
- Remove any hedging language ("it appears that", "one might consider") -- be direct

### 6. Design and publish

Format the report:
- **PDF version**: Clean, branded layout. Include charts inline. Add a cover page with title, author, and date. No heavy design -- founder-authored quality, not agency-produced.
- **Web version**: Using the `ghost-blog-publishing` fundamental, publish a landing page version with gated or ungated access. If gated, keep the form minimal (email + company name). If ungated, add an email capture CTA for "future reports."
- **Social graphics**: Extract 4-6 charts and quotable stats as standalone images sized for LinkedIn (1200x627) and Twitter (1600x900).

Host at a memorable URL: `{yourdomain}.com/reports/{report-slug}`

Configure PostHog tracking on the landing page:
- `report_page_viewed` -- properties: report_slug, source, utm params
- `report_downloaded` -- properties: report_slug, email (if gated)
- `report_shared` -- properties: report_slug, platform

## Output

- One published industry report (PDF + web version)
- 4-6 social graphics with quotable stats
- Landing page with PostHog tracking configured
- Raw data set for future analysis and report updates
- Distribution brief: key findings, shareable quotes, and suggested social posts (feeds into `report-distribution-pipeline`)

## Triggers

Run this drill once per quarter at Scalable/Durable levels. At Smoke level, run once to validate the concept. At Baseline, run 1-2 times over 30 days. Total production time per report: 8-15 hours depending on data collection method.
