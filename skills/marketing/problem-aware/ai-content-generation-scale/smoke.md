---
name: ai-content-generation-scale-smoke
description: >
  AI Content Generation — Smoke Test. Generate 5 blog posts and 10 social posts using AI ghostwriting,
  publish manually, and prove that AI-generated content produces measurable traffic and conversions
  before investing in automation.
stage: "Marketing > Problem Aware"
motion: "FounderSocialContent"
channels: "Content"
level: "Smoke Test"
time: "6 hours over 3 weeks"
outcome: "≥300 page views and ≥3 conversions in 3 weeks"
kpis: ["Page views", "Time on page", "Conversion rate", "Content production velocity"]
slug: "ai-content-generation-scale"
install: "npx gtm-skills add marketing/problem-aware/ai-content-generation-scale"
drills:
  - founder-linkedin-content-batch
  - blog-seo-pipeline
  - threshold-engine
---

# AI Content Generation — Smoke Test

> **Stage:** Marketing → Problem Aware | **Motion:** FounderSocialContent | **Channels:** Content

## Outcomes

Prove that AI-generated content (blog posts + social posts) can produce real traffic and conversions for your audience. At Smoke, the agent drafts content and the founder reviews/publishes manually. No automation, no always-on systems. Success = 300+ page views and 3+ conversions (signup, download, or demo request) within 3 weeks from 5 blog posts and 10 social posts.

## Leading Indicators

- Blog posts published on schedule (5 in 3 weeks)
- Social posts published on schedule (10 in 3 weeks)
- Organic impressions trending up week over week
- At least 1 blog post exceeds 100 page views
- Social posts generating profile views and link clicks
- Time on page averaging 2+ minutes on blog content

## Instructions

### 1. Research keywords and topics for blog content

Run the `blog-seo-pipeline` drill (Steps 1-2 only: keyword research and prioritization). Identify 5 target keywords aligned with your ICP's problems. For each keyword, document: search volume, difficulty score, and the specific question your content will answer. Choose keywords with difficulty scores your domain authority can realistically rank for. New sites should target long-tail keywords (4+ words).

Output: 5 keyword-topic pairs with search intent documented.

### 2. Generate blog post drafts via AI

For each of the 5 topics, use the Anthropic API to generate a draft blog post:

```
POST https://api.anthropic.com/v1/messages
x-api-key: {ANTHROPIC_API_KEY}
anthropic-version: 2023-06-01

{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 4096,
  "system": "You are writing a blog post for {COMPANY_NAME}. Target audience: {ICP_DESCRIPTION}. Tone: educational, specific, opinionated. Rules: Include the target keyword in the title, H1, first paragraph, and 2-3 subheadings. Target 1,500-2,000 words. Use concrete examples, data, or screenshots. End with a clear CTA (signup, download, or demo). No fluff, no filler paragraphs.",
  "messages": [
    {
      "role": "user",
      "content": "Write a blog post targeting the keyword '{TARGET_KEYWORD}'. The searcher's intent is: {SEARCH_INTENT}. Cover these specific points: {KEY_POINTS}. Include a section comparing approaches or tools where relevant."
    }
  ]
}
```

Review each draft for factual accuracy, brand voice alignment, and SEO optimization (keyword in title, H1, meta description, and body).

**Human action required:** The founder reviews each draft for accuracy and voice. Edit any generic claims into specific data or experiences from the company.

### 3. Publish blog posts

Run the `blog-seo-pipeline` drill (Steps 4-5: publish and distribute). For each post:
- Publish to Ghost (or your CMS) with optimized metadata: SEO title under 60 characters, meta description under 155 characters with keyword, short URL slug
- Add 2-3 internal links to related pages on your site
- Add Open Graph image for social sharing
- Publish 1-2 posts per week over 3 weeks

### 4. Generate and publish social content batch

Run the `founder-linkedin-content-batch` drill to create 10 LinkedIn posts:
- 5 posts that promote the blog content (key insight from each blog post, reformatted as a LinkedIn post with a hook and link)
- 5 standalone posts on related ICP pain points using content pillar rotation

For each post, the drill produces: hook line, body, CTA, and suggested publish day. The founder reviews all 10 in a single batch session.

**Human action required:** The founder reviews, edits, and manually posts each piece of content on LinkedIn over the 3-week period. Engage with every comment within the first hour.

### 5. Track performance in PostHog

Set up basic PostHog tracking on your blog:
- Track `page_viewed` events with properties: `url`, `title`, `source` (organic, social, direct)
- Track conversion events: `signup_completed`, `resource_downloaded`, `demo_requested`
- Track `scroll_depth` and `time_on_page` for blog posts

Log social post performance manually in a spreadsheet: post URL, impressions, likes, comments, link clicks, profile views.

### 6. Evaluate against threshold

Run the `threshold-engine` drill. Query PostHog for the 3-week window:
- Total page views across all 5 blog posts: target ≥300
- Total conversions (signup + download + demo request): target ≥3

If PASS: document which topics, formats, and CTAs drove the most traffic and conversions. Proceed to Baseline.

If FAIL: diagnose. Check blog post rankings in Google Search Console after 2-3 weeks. If posts have impressions but low clicks, rewrite titles and meta descriptions. If social posts drove no traffic, test different hooks and CTA styles. Re-run with adjusted content.

## Time Estimate

- Keyword research and topic selection: 1 hour
- AI blog post generation + founder review: 2 hours (5 posts)
- Blog publishing and SEO optimization: 1 hour
- Social content batch generation + founder review: 1 hour
- Manual posting and engagement over 3 weeks: 45 minutes
- Performance tracking and evaluation: 15 minutes
- **Total: ~6 hours over 3 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Anthropic Claude API | Generate blog and social post drafts | ~$0.05/month at this volume (https://platform.claude.com/docs/en/about-claude/pricing) |
| Ghost | Blog publishing and hosting | Free (self-hosted) or $15/mo Starter (https://ghost.org/pricing/) |
| PostHog | Track page views and conversions | Free tier: 1M events/mo (https://posthog.com/pricing) |
| LinkedIn | Social content distribution | Free |

**Play-specific cost: Free** (assumes self-hosted Ghost or existing blog, PostHog free tier, Claude API cost negligible)

## Drills Referenced

- `founder-linkedin-content-batch` — generate a batch of LinkedIn posts in the founder's voice with AI assistance
- `blog-seo-pipeline` — research keywords, write, publish, and optimize blog content for organic search
- `threshold-engine` — evaluate pass/fail against the 300 page view / 3 conversion target
