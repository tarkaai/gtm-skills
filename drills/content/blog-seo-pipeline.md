---
name: blog-seo-pipeline
description: Research, write, publish, and optimize blog content for organic search traffic
category: Content
tools:
  - Ghost
  - PostHog
  - Clay
fundamentals:
  - ghost-publishing
  - seo-keyword-research
  - seo-on-page-optimization
  - posthog-event-tracking
---

# Blog SEO Pipeline

This drill creates a repeatable workflow for publishing blog content that ranks in search and drives qualified organic traffic. It covers keyword research, writing, publishing, and ongoing optimization.

## Prerequisites

- Ghost or equivalent CMS set up and connected to your domain
- PostHog tracking installed on your blog
- Basic understanding of your ICP's search behavior

## Steps

### 1. Research keywords aligned to your ICP

Using the `seo-keyword-research` fundamental, identify keywords that your ICP actually searches when they have the problem you solve. Focus on bottom-of-funnel terms first (comparison queries, "how to solve X", "best tool for Y") because they convert better than top-of-funnel educational content. Build a keyword list of 20-30 targets with monthly search volume and difficulty scores.

### 2. Prioritize by impact

Rank keywords by a simple formula: search volume multiplied by conversion intent, divided by competition difficulty. Write the highest-impact articles first. Aim for keywords with difficulty scores you can realistically rank for given your domain authority. New sites should target long-tail keywords (4+ words) with lower competition.

### 3. Write the article

Structure every article for both readers and search engines using the `seo-on-page-optimization` fundamental:

- **Title**: Include the primary keyword naturally. Keep under 60 characters.
- **Introduction**: State the problem and promise the solution in the first 100 words.
- **Body**: Use H2 and H3 subheadings with related keywords. Answer the searcher's question thoroughly. Include original data, examples, or screenshots where possible.
- **Conclusion**: Summarize key takeaways and include a relevant CTA (signup, demo, related resource).

Target 1,500-2,500 words for competitive keywords. Quality and depth matter more than length alone.

### 4. Publish and optimize metadata

Using the `ghost-publishing` fundamental, publish the article with optimized metadata: SEO title, meta description (under 155 characters with keyword), URL slug (short, keyword-rich), and Open Graph image. Add internal links to 2-3 related articles on your site. Add external links to authoritative sources.

### 5. Distribute the article

Share on social channels (feed into `social-content-pipeline`), include in your newsletter (feed into `newsletter-pipeline`), and email it to relevant prospects in Attio who would find it valuable. The first 48 hours of traffic and engagement signal to search engines that the content is worth ranking.

### 6. Monitor and iterate

Using `posthog-event-tracking`, track organic traffic, time on page, scroll depth, and conversion events per article. After 30 days, check search rankings. If an article ranks on page 2, update it: add more depth, improve the intro, add FAQ sections. Refresh underperforming content quarterly.
