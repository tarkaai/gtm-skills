---
name: comparison-page-creation
description: Write, format, and publish a single comparison or alternative page targeting a competitor keyword with structured feature data and conversion CTAs
category: SEO
tools:
  - Anthropic
  - Firecrawl
  - Webflow
  - PostHog
fundamentals:
  - competitor-page-scraping
  - competitive-positioning-generation
  - webflow-cms
  - webflow-landing-pages
  - posthog-custom-events
  - og-meta-generation
  - sitemap-generation
---

# Comparison Page Creation

This drill produces a single, high-quality comparison page (or alternative page) that targets a specific competitor keyword. Each page is built from real competitive data, structured for SEO, and includes a lead capture CTA. This drill runs once per page at Smoke level and feeds into `programmatic-page-generator` at Scalable level.

## Input

- One row from the `competitor-keyword-research` output: target keyword, competitor name, page type, content angle, related keywords
- Your product's feature list and pricing
- Competitor's public product/pricing data (or scraped via `competitor-page-scraping`)

## Steps

### 1. Gather competitor data

Use `competitor-page-scraping` to extract structured data from the competitor's website:

- **Pricing page**: plan names, prices, feature lists per plan
- **Features page**: feature names, descriptions, integrations
- **Homepage**: positioning statement, target audience claims

If the competitor blocks scraping, fall back to publicly available data: G2 profile, Capterra listing, or their documentation site. Manually review the extracted data for accuracy — never publish unverified competitor claims.

**Human action required:** Verify all competitor data for accuracy before publishing. Do not publish pricing or feature claims you cannot substantiate from a public source.

### 2. Generate page content

Use Claude (Anthropic API) to generate the page content. The prompt varies by page type:

**For 1:1 comparison pages (`{competitor} vs {your brand}`):**

```
System prompt: Write a comparison page for "{target_keyword}". This page will be published
at {url_slug} and targets solution-aware buyers evaluating these two products.

Our product: {your_product_name}
Our features: {your_features_json}
Our pricing: {your_pricing_json}

Competitor: {competitor_name}
Their features: {competitor_features_json}
Their pricing: {competitor_pricing_json}

Content angle: {content_angle}
Related keywords to include naturally: {related_keywords}

Write the page with these sections:
1. **Introduction** (100-150 words): Acknowledge both products fairly. State what the reader
   will learn. Include the target keyword in the first sentence.
2. **Quick comparison table**: HTML table with rows for each major feature/capability.
   Columns: Feature, {your_product}, {competitor}. Use checkmarks, X marks, and brief notes.
   Be honest — mark features the competitor has that you lack.
3. **Where {your_product} is stronger** (200-300 words): 3-4 specific advantages with
   concrete details, not marketing claims. Tie each to a buyer pain point.
4. **Where {competitor} is stronger** (100-200 words): 1-2 areas where the competitor
   genuinely excels. This builds credibility.
5. **Pricing comparison** (100-150 words): Side-by-side pricing. Highlight TCO differences
   if applicable (hidden costs, required add-ons, implementation fees).
6. **Who should choose {your_product}** (100 words): Specific buyer profiles or use cases.
7. **Who should choose {competitor}** (50-100 words): Honest recommendation for when
   they are the better fit.
8. **FAQ**: 4-5 questions from "People Also Ask" for this keyword. Answers in 2-3 sentences.
   Format with FAQ structured data (JSON-LD).

Output as HTML. Target 1,200-1,800 words total. Tone: factual, fair, helpful.
Do NOT trash the competitor. Readers trust pages that acknowledge tradeoffs.
```

**For alternatives pages (`{competitor} alternatives`):**

```
System prompt: Write an alternatives page for "{target_keyword}". List 5-8 alternatives
to {competitor_name}, with your product as the top recommendation.

For each alternative, include:
- Product name and one-line description
- Top 3 differentiators vs {competitor}
- Pricing starting point
- Best for (specific use case or buyer type)

Lead with your product. Be honest about the others. Include the target keyword in the
H1 and first paragraph. Add a comparison table summarizing all alternatives.
FAQ section with 3-4 questions. Output as HTML. Target 1,500-2,000 words.
```

### 3. Build the feature comparison table

Separately from the generated content, build a structured HTML comparison table:

| Category | Feature | {Your Product} | {Competitor} |
|----------|---------|-----------------|--------------|
| Core     | {Feature 1} | {Yes/No/Details} | {Yes/No/Details} |
| Core     | {Feature 2} | ... | ... |
| Pricing  | Starting price | ... | ... |
| Pricing  | Free tier | ... | ... |
| Support  | Response time | ... | ... |

Use CSS classes for easy styling: `.feature-yes`, `.feature-no`, `.feature-partial`. This table is the most valuable element on the page — visitors scan it before reading anything.

### 4. Add SEO metadata

Use `og-meta-generation` to create:

- **Title tag** (under 60 chars): `{Competitor} vs {Your Product}: Honest Comparison (2026)`
- **Meta description** (under 155 chars): Include the target keyword, a benefit, and a call to action
- **H1**: Match or closely mirror the title tag
- **URL slug**: `compare/{competitor-slug}-vs-{your-slug}` or `compare/{competitor-slug}-alternatives`
- **Schema markup**: FAQ structured data (JSON-LD) for the FAQ section, Product structured data for both products

### 5. Add lead capture CTA

Every comparison page needs exactly one CTA. Place it:
- After the comparison table (primary placement)
- At the bottom of the page (secondary placement)

CTA options (choose one):
- **Inline calendar embed**: "See how {your product} compares — book a 15-min walkthrough"
- **Free trial button**: "Try {your product} free — no credit card required"
- **Demo video**: "Watch {your product} in action (3 min)"

Track with `posthog-custom-events`:
- `comparison_page_viewed`: on page load, with properties `competitor`, `page_type`, `target_keyword`
- `comparison_table_scrolled`: when feature table enters viewport
- `comparison_cta_clicked`: when CTA is clicked

### 6. Publish

Using `webflow-cms` (for CMS-managed pages) or `webflow-landing-pages` (for standalone):

- Create the page with all content, metadata, and tracking
- Set canonical URL to avoid duplicate content issues
- Add internal links: link from your homepage, pricing page, or related blog posts to this comparison page
- After publishing, use `sitemap-generation` to update your sitemap and submit to Google Search Console

## Output

- One published comparison page targeting a specific competitor keyword
- SEO metadata, FAQ schema, and feature comparison table
- PostHog events tracking views, table engagement, and CTA clicks
- Internal links pointing to the new page

## Triggers

- Run once per comparison page target (Smoke level: 3-5 pages; Baseline: 10-20 pages)
- Re-run when competitor pricing or features change significantly
- Re-run when your product ships features that change the comparison
