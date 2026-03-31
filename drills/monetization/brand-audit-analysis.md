---
name: brand-audit-analysis
description: Analyze website brand presentation, messaging consistency, and conversion paths to produce a structured brand audit report
category: Conversion
tools:
  - Playwright
  - PostHog
  - Anthropic
  - Clay
fundamentals:
  - brand-audit-scrape
  - posthog-web-analytics
  - posthog-funnels
  - posthog-session-recording
  - hypothesis-generation
  - clay-company-search
---

# Brand Audit Analysis

Produce a structured brand audit by combining programmatic website analysis with behavioral analytics data. The output is an actionable audit document identifying messaging gaps, conversion blockers, and positioning opportunities — used as the foundation for brand refresh work.

## Input

- Target website URL (your own site for a refresh, or a competitor for benchmarking)
- PostHog project with at least 4 weeks of web analytics data
- ICP definition (who the brand should resonate with)
- 3-5 competitor URLs for comparison

## Steps

### 1. Crawl and extract brand elements

Using `brand-audit-scrape`, crawl all marketing pages (homepage, pricing, features, about, case studies). Extract:
- Every H1 and H2 headline
- Every CTA (text + destination URL)
- Meta titles and descriptions
- Above-fold screenshots of each page

Also crawl 3-5 competitor sites for comparison data.

### 2. Analyze messaging consistency

Using `hypothesis-generation` (Claude), pass all extracted headlines and CTAs:

```
You are auditing a B2B SaaS website's brand presentation. Here are all H1 headlines and CTAs from every marketing page:

[headlines and CTAs data]

Analyze for:
1. MESSAGING CONSISTENCY: Do all headlines reinforce the same core value proposition? Or does each page tell a different story?
2. CLARITY: Could a first-time visitor understand what the product does, who it's for, and why it's different within 5 seconds of any page?
3. DIFFERENTIATION: Do any headlines or CTAs also apply to competitors? (If yes, the messaging is commodity-level.)
4. CTA HIERARCHY: Is there a clear primary action? Or are there competing CTAs that confuse the visitor?
5. ICP ALIGNMENT: Given this ICP [{ICP definition}], does the messaging speak to their specific pain points and desired outcomes?

For each issue found, provide:
- The specific page and element
- What's wrong
- A concrete rewrite recommendation
```

### 3. Analyze conversion paths

Using `posthog-funnels`, build conversion funnels for the primary user journeys:
- Homepage > Features > Pricing > Signup
- Blog post > Homepage > Pricing > Signup
- Landing page > Form submit
- Any page > CTA click > Conversion

Using `posthog-web-analytics`, pull:
- Bounce rate by entry page (which pages lose visitors immediately?)
- Average session duration by source (are paid visitors more or less engaged than organic?)
- Top exit pages (where do visitors leave?)

Using `posthog-session-recording`, watch 10-20 recordings of visitors who bounced from key pages. Note: what did they look at? Where did they scroll? Did they hover over anything without clicking?

### 4. Competitive positioning analysis

Using `clay-company-search`, enrich competitor data: company size, funding, market positioning.

Pass competitor crawl data to Claude alongside your own:

```
Compare these 4 B2B SaaS websites' brand presentations:

OURS: [headlines, CTAs, value props from our site]
COMPETITOR A: [headlines, CTAs, value props]
COMPETITOR B: [headlines, CTAs, value props]
COMPETITOR C: [headlines, CTAs, value props]

Identify:
1. Where our messaging overlaps with competitors (commodity territory)
2. Where competitors claim territory we don't (gaps we should fill or concede)
3. Where we have a unique angle that no competitor claims (our differentiation)
4. What messaging patterns are table-stakes in this market (must-have claims)
```

### 5. Produce the brand audit report

Structure the output as a structured document:

```
## Brand Audit Report — {Company Name} — {Date}

### Executive Summary
- 3-sentence assessment: current state, biggest gap, highest-impact opportunity

### Messaging Audit
- Core value proposition (as stated vs. as perceived)
- Page-by-page messaging consistency score (1-5)
- Specific rewrites recommended

### Conversion Path Audit
- Primary funnel conversion rate: {%}
- Top 3 drop-off points with hypothesized causes
- Session recording insights

### Competitive Positioning
- Positioning map: where we sit vs. competitors
- Unique claims (ours alone)
- Commodity claims (everyone says this)
- Gaps (competitors claim, we don't)

### Recommended Actions (prioritized)
1. {Action} — Expected impact: {%} conversion lift — Effort: {hours}
2. {Action} — Expected impact: {%} — Effort: {hours}
3. {Action} — Expected impact: {%} — Effort: {hours}
```

Store the report in Attio as a note on the company record.

## Output

- Structured brand audit report (JSON and markdown)
- Page-by-page messaging audit with specific rewrites
- Conversion funnel analysis with drop-off diagnoses
- Competitive positioning map
- Prioritized action list for the brand refresh

## Triggers

- Run once at the start of a brand refresh play
- Re-run quarterly to measure brand evolution
