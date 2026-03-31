---
name: programmatic-page-generator
description: Generate and publish SEO-optimized pages at scale from a keyword matrix and content templates
category: SEO
tools:
  - Webflow
  - Anthropic
  - n8n
fundamentals:
  - webflow-cms-bulk
  - sitemap-generation
  - n8n-workflow-basics
  - n8n-scheduling
---

# Programmatic Page Generator

This drill takes a keyword matrix (from `keyword-matrix-builder`) and a content template, then generates and publishes hundreds of unique, SEO-optimized pages via the Webflow CMS API.

## Input

- Keyword matrix: structured dataset with one row per page (target_keyword, slug, modifier, category, related_keywords, internal_link_targets)
- Content template: an HTML/rich-text template with variable placeholders
- Webflow collection ID for the target CMS collection
- Webflow API token

## Steps

### 1. Design the page template

Create a Webflow CMS collection template that renders every page. The template is a single Webflow page bound to CMS fields. Key sections:

- **Hero**: H1 bound to `h1-heading` field. Subheading bound to `meta-description` field.
- **Body content**: Rich text bound to `body-content` field. This is where the unique, keyword-specific content goes.
- **Related pages**: A section listing 3-5 related pages from `internal-links` field.
- **CTA**: A lead capture form or demo booking widget. CTA text bound to `cta-text` field.
- **FAQ**: Structured FAQ section with schema markup for rich snippets.

**Human action required:** Design and build the Webflow CMS template page once. This is a visual design task. Keep the template clean, fast-loading, and mobile-responsive. Once built, all pages inherit this layout.

### 2. Generate unique content per page

For each row in the keyword matrix, generate body content using Claude (Anthropic API):

```
System prompt: You are an SEO content writer. Write a comprehensive, original page
about {target_keyword}. The audience is {icp_description}. Include:
- An introduction explaining what {modifier} specifically needs from {category}
- 3-5 sections addressing specific pain points and solutions
- Concrete examples, data points, or comparisons where possible
- A FAQ section with 3-5 questions searchers ask about {target_keyword}
- Natural inclusion of related keywords: {related_keywords}
- Avoid generic filler. Every paragraph must provide specific value.
Output as HTML with proper h2, h3, p, ul, and ol tags.
```

Rules for content generation:
- Each page MUST be substantially unique. Never generate the same content with only the modifier swapped.
- Include the target keyword in the first 100 words, in at least one H2, and in the conclusion.
- Target 800-1,500 words per page. Enough depth to rank, short enough to generate at scale.
- Generate FAQ structured data (JSON-LD) for each page to qualify for rich snippets.

### 3. Quality-check generated content

Before publishing, run each page through validation:

- **Uniqueness check**: Compare against all other pages in the batch. If content similarity >40% between any two pages, regenerate the more generic one with more specific instructions.
- **Keyword inclusion**: Verify target keyword appears in H1, first paragraph, at least one H2, and meta description.
- **Length check**: Reject pages under 600 words. Flag pages over 2,000 words for trimming.
- **Link check**: Verify all internal link targets exist in the matrix or on the live site.

### 4. Publish pages via Webflow CMS API

Using `webflow-cms-bulk`, create CMS items for each validated page:

- Set `isDraft: false` for immediate publishing
- Respect the 60 requests/minute rate limit
- For a 500-page batch at 1 request/second: approximately 8 minutes to create all items
- After all items are created, trigger a site publish via the Webflow API

### 5. Generate and submit sitemap

Using `sitemap-generation`:

- If Webflow auto-generates sitemaps for the CMS collection, verify the sitemap includes all new pages
- If using a custom sitemap, regenerate it to include all new page URLs
- Submit the updated sitemap to Google Search Console using `google-search-console-api`

### 6. Build the n8n automation (for Baseline+ levels)

Using `n8n-workflow-basics` and `n8n-scheduling`, create a workflow that:

1. Triggers on a schedule (e.g., weekly for new pages, monthly for content refreshes)
2. Reads new rows from the keyword matrix (Clay table or Airtable)
3. Generates content via Anthropic API
4. Runs quality checks
5. Creates Webflow CMS items
6. Publishes the site
7. Submits updated sitemap
8. Logs results to PostHog and Attio

## Output

- Published pages on the live site, each targeting a specific long-tail keyword
- Updated sitemap submitted to Google Search Console
- Logs of pages created: URL, target keyword, word count, publish timestamp

## Triggers

- Initial batch: run once to publish the first set of pages (50-200)
- Ongoing: run weekly to publish new pages from the expanding keyword matrix
- Content refresh: run monthly to update underperforming pages (feeds from `content-refresh-pipeline`)
