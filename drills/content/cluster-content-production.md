---
name: cluster-content-production
description: Batch-produce cluster articles and pillar pages from a topic cluster map using AI content generation and CMS publishing
category: SEO
tools:
  - Ghost
  - Anthropic
  - Ahrefs
  - PostHog
fundamentals:
  - ghost-blog-publishing
  - ai-content-ghostwriting
  - ahrefs-keyword-research
  - posthog-custom-events
---

# Cluster Content Production

This drill takes the output of `topic-cluster-mapping` (a prioritized list of cluster subtopics with keyword data and linking instructions) and produces finished, published articles. It covers writing, SEO optimization, internal linking, and publishing.

## Input

- Cluster map from `topic-cluster-mapping`: pillar topic, subtopic list with keywords, intent types, linking map
- ICP description and product positioning
- Brand voice guidelines or founder voice profile
- CMS access (Ghost, Webflow, WordPress, or equivalent)

## Steps

### 1. Write the pillar page first

The pillar page is the anchor. Generate it using the Anthropic API:

```
POST https://api.anthropic.com/v1/messages
x-api-key: {ANTHROPIC_API_KEY}
anthropic-version: 2023-06-01

{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 8192,
  "system": "You are an expert SEO content writer. Write a comprehensive pillar page about {pillar_topic} for {icp_description}. The page must:\n- Target the keyword '{pillar_keyword}' (volume: {volume}, difficulty: {kd})\n- Be 3,000-5,000 words\n- Include a table of contents\n- Cover each of these subtopics with a 200-300 word summary section:\n{subtopic_list_with_h2s}\n- Each subtopic section ends with a contextual link placeholder: [LINK: /blog/{subtopic_slug}]\n- Include a FAQ section with 5-8 questions from People Also Ask\n- Include a lead capture CTA after the introduction and before the conclusion\n- Write in a clear, authoritative tone. No fluff. Every paragraph must provide specific value.\n- Output as HTML with proper h2, h3, p, ul, ol tags.",
  "messages": [{"role": "user", "content": "Write the pillar page now."}]
}
```

### 2. Batch-produce cluster articles

For each cluster subtopic, generate an article. Process in batches of 5-10:

```
For each subtopic in batch:

System prompt:
"Write an in-depth article about '{subtopic_keyword}' for {icp_description}.
- Target keyword: '{subtopic_keyword}' (volume: {volume}, KD: {kd})
- Intent type: {intent_type}
- Word count: 1,200-2,000 words for informational, 1,500-2,500 words for comparative
- Include the target keyword in the first 100 words, in at least one H2, and in the conclusion
- Include related keywords naturally: {related_keywords}
- Structure: introduction (state the problem, promise the answer), 3-5 H2 sections, practical examples, FAQ (3-5 questions), conclusion with CTA
- Internal links to include:
  - Link back to pillar page: [LINK: /blog/{pillar_slug}] (in introduction or conclusion)
  - Link to adjacent cluster articles: [LINK: /blog/{adjacent_slug_1}], [LINK: /blog/{adjacent_slug_2}]
- Write for readers who are solution-aware: they know the category exists, they are evaluating options
- Output as HTML"
```

### 3. Quality-check each article before publishing

For every generated article, verify:

- **Keyword inclusion**: target keyword in H1, first 100 words, at least one H2, meta description
- **Length**: meets minimum word count for intent type
- **Uniqueness**: no two cluster articles share more than 30% content similarity (compare first 500 words)
- **Internal links**: all [LINK: ...] placeholders are present and correct
- **Readability**: no paragraphs longer than 4 sentences, no walls of text without subheadings
- **CTA**: every article ends with a relevant call-to-action (contextual, not generic)

Reject and regenerate any article that fails quality checks.

### 4. Resolve internal link placeholders

Before publishing, replace all `[LINK: /blog/{slug}]` placeholders with actual HTML links:

```html
<a href="/blog/{slug}">{anchor_text}</a>
```

Use natural anchor text derived from the target keyword of the linked article. Do NOT use generic anchors like "click here" or "read more."

If a linked article has not been published yet (later in the batch), note it for post-publish link insertion.

### 5. Set SEO metadata per article

For each article, generate via the Anthropic API:

- `meta_title`: target keyword + benefit, under 60 characters
- `meta_description`: summarize the article's value proposition, include target keyword, under 155 characters
- `slug`: target keyword as URL-friendly slug (lowercase, hyphens, no stop words)
- `tags`: pillar topic name + intent type + 1-2 category tags

### 6. Publish via CMS

Using `ghost-blog-publishing`:

1. Create each article as a draft first (`status: "draft"`)
2. Verify formatting renders correctly via the Ghost preview URL
3. Publish the pillar page first
4. Publish cluster articles in priority order (highest priority score first)
5. Space publishing: 2-3 articles per day maximum to avoid triggering spam filters in search engines

### 7. Track content events

Using `posthog-custom-events`, fire events for each published article:

- `cluster_article_published`: properties `url`, `pillar_topic`, `target_keyword`, `intent_type`, `word_count`, `publish_date`
- `cluster_pillar_published`: properties `url`, `pillar_topic`, `cluster_count`, `total_word_count`

## Output

- Published pillar page (3,000-5,000 words)
- Published cluster articles (8-12 per batch, 1,200-2,500 words each)
- All internal links connected (pillar <-> clusters, cluster <-> adjacent clusters)
- SEO metadata set for every page
- PostHog events logged for tracking

## Triggers

- Initial batch: run once at Smoke level to publish pillar + first 5 cluster articles
- Expansion: run at Baseline level to publish remaining cluster articles
- Ongoing: run monthly at Scalable level when `topic-cluster-mapping` identifies new subtopics
