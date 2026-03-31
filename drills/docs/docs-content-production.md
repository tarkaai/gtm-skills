---
name: docs-content-production
description: Research, write, and publish SEO-targeted documentation pages — tutorials, guides, and API references — optimized for organic search
category: Docs
tools:
  - Mintlify / GitBook / ReadMe / Docusaurus / Fumadocs
  - Anthropic
  - Ahrefs
  - Google Search Console
fundamentals:
  - docs-platform-publishing
  - ai-content-ghostwriting
  - ahrefs-keyword-research
  - google-search-console-api
---

# Docs Content Production

This drill produces documentation pages specifically optimized for organic search traffic. Unlike internal-only docs, these pages are designed to rank for keywords your ICP searches and include conversion paths that turn readers into leads.

## Input

- Target keyword list (from `docs-site-seo-audit` gap analysis or `ahrefs-keyword-research`)
- Product capabilities and API surface area
- ICP description (who searches for these topics, what they need to accomplish)
- Docs platform and repository access

## Steps

### 1. Categorize and prioritize pages to write

For each target keyword, classify the page type:

- **Getting Started Guide:** For queries like "how to set up {product}", "getting started with {category}". Structure: prerequisites, step-by-step walkthrough, expected result, next steps. Target 1,500-2,500 words.
- **How-To Tutorial:** For queries like "how to {action} with {tool}". Structure: problem statement, solution overview, step-by-step with code examples, common pitfalls, variations. Target 1,200-2,000 words.
- **API Reference:** For queries like "{product} {endpoint} API", "{product} webhook payload". Structure: endpoint description, authentication, request/response schema, code examples in 3+ languages, error codes. Target 800-1,500 words.
- **Integration Guide:** For queries like "{product} + {other_tool} integration", "connect {product} to {platform}". Structure: what the integration does, prerequisites, setup steps, configuration options, testing, troubleshooting. Target 1,500-2,500 words.
- **Troubleshooting/FAQ:** For queries like "{product} error {code}", "{product} not working". Structure: error description, cause, fix steps, related errors. Target 600-1,200 words.

Prioritize by: `(search_volume * intent_relevance) / keyword_difficulty`. Write the highest-impact pages first.

### 2. Generate the page content

For each page, use the Anthropic API:

```
POST https://api.anthropic.com/v1/messages
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 8192,
  "system": "You are writing a documentation page for {product_name}. The page targets the keyword '{target_keyword}' (monthly search volume: {volume}).\n\nPage type: {page_type}\nICP: {icp_description}\nProduct capability: {capability_description}\n\nRequirements:\n- Include the target keyword in the H1, first paragraph, and at least one H2\n- Include related keywords naturally: {related_keywords}\n- Every code example must be syntactically correct and copy-pasteable\n- Include at minimum 2 code examples showing real usage\n- Write for practitioners who want to accomplish a task, not academics who want theory\n- End with a clear next-step CTA: link to a related guide, link to signup, or link to API key generation\n- Output as MDX with proper frontmatter (title, description, keywords)\n- Include a 'Prerequisites' section listing what the reader needs before starting\n- Include a 'Common Issues' section addressing 2-3 frequent mistakes",
  "messages": [{"role": "user", "content": "Write the documentation page now."}]
}
```

### 3. Quality-check each page

Before publishing, verify:

- **Keyword inclusion:** Target keyword in title, first 100 words, at least one H2, meta description
- **Code correctness:** Every code block specifies a language. Every API call uses the correct endpoint and payload structure. Every code example could be copy-pasted and run.
- **Completeness:** Prerequisites listed. Steps numbered. Expected output shown. Error handling covered.
- **Conversion path:** Page ends with a CTA relevant to the content (e.g., tutorial ends with "Get your API key to try this" linking to signup)
- **Internal links:** Links to 2+ related docs pages. Uses descriptive anchor text.
- **Length:** Meets minimum word count for page type
- **Frontmatter:** `title`, `description`, `keywords` are all set and optimized

Reject and regenerate any page that fails quality checks.

### 4. Publish via docs platform

Using `docs-platform-publishing`:

1. Create each page as a draft or in a branch
2. Verify rendering: check that code blocks render with syntax highlighting, tables display correctly, images load
3. Update navigation/sidebar to include the new pages in logical positions
4. Publish: merge the branch or set status to published
5. Submit new URLs to Google Search Console for indexation

### 5. Set up basic tracking per page

For each published page, ensure tracking fires:

- `docs_page_viewed`: page load with properties `url`, `target_keyword`, `page_type`, `referrer`
- `docs_cta_clicked`: CTA interaction with properties `url`, `cta_type` (signup, api_key, demo, next_guide), `cta_text`

## Output

- Published documentation pages, each targeting a specific keyword
- All pages SEO-optimized with proper metadata and internal links
- Tracking events configured for traffic and conversion measurement
- URLs submitted to GSC for indexation

## Triggers

- Initial batch at Smoke level: 5-8 pages targeting highest-priority keywords
- Expansion at Baseline level: 10-20 additional pages
- Ongoing at Scalable level: automated weekly production triggered by gap analysis
