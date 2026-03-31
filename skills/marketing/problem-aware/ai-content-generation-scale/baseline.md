---
name: ai-content-generation-scale-baseline
description: >
  AI Content Generation — Baseline Run. Scale from 5 blog posts to 15-20 over 6 weeks with a
  content repurposing system, structured PostHog event tracking, and a multi-platform distribution
  cadence that proves repeatable traffic and conversion growth.
stage: "Marketing > Problem Aware"
motion: "FounderSocialContent"
channels: "Content"
level: "Baseline Run"
time: "18 hours over 6 weeks"
outcome: "≥2,000 page views and ≥20 conversions over 6 weeks"
kpis: ["Page views", "Time on page", "Conversion rate", "Content production velocity", "Social shares"]
slug: "ai-content-generation-scale"
install: "npx gtm-skills add marketing/problem-aware/ai-content-generation-scale"
drills:
  - content-repurposing
  - social-content-pipeline
  - posthog-gtm-events
---

# AI Content Generation — Baseline Run

> **Stage:** Marketing → Problem Aware | **Motion:** FounderSocialContent | **Channels:** Content

## Outcomes

Prove that AI-generated content production is repeatable and can sustain traffic growth over 6 weeks. At Baseline, the agent runs the content generation pipeline continuously while the founder reviews batches weekly. Content repurposing multiplies output across channels. Success = 2,000+ page views and 20+ conversions from 15-20 blog posts plus repurposed social content over 6 weeks.

## Leading Indicators

- Content velocity: 3-4 new blog posts published per week
- Social posts generated per blog post: 3-5 derivative pieces each
- Week-over-week page view growth (organic + social referral)
- Social engagement rate holding steady or improving vs Smoke
- At least 3 blog posts exceeding 200 page views individually
- Newsletter subscriber growth from content CTAs
- Profile views and connection requests trending up on LinkedIn

## Instructions

### 1. Set up content event tracking

Run the `posthog-gtm-events` drill to implement a complete event taxonomy for content performance. Define and instrument these events:

- `blog_post_published` — properties: `url`, `title`, `target_keyword`, `word_count`, `content_pillar`, `publish_date`
- `blog_post_viewed` — properties: `url`, `title`, `source` (organic/social/direct/email), `time_on_page`, `scroll_depth`
- `social_post_published` — properties: `platform`, `pillar`, `format`, `source_blog_url`, `post_url`
- `social_post_engagement` — properties: `platform`, `post_url`, `impressions`, `likes`, `comments`, `shares` (collected 48h post-publish)
- `content_conversion` — properties: `url`, `conversion_type` (signup/download/demo), `source_channel`, `content_pillar`
- `content_lead_captured` — properties: `source_url`, `lead_email`, `lead_title`, `lead_company`

Build a PostHog funnel: `blog_post_viewed` -> `content_conversion` -> `content_lead_captured`, broken down by content pillar.

### 2. Build the content repurposing system

Run the `content-repurposing` drill to create a repeatable system that transforms each blog post into multiple derivative assets:

For each published blog post, extract:
- 3-4 key insights (each becomes a LinkedIn post)
- 1-2 frameworks or lists (each becomes a carousel or list post)
- 5-6 quotable lines (each becomes a standalone social quote)
- 1 core argument (becomes a newsletter section)

Use the Anthropic API to generate derivatives in batch:

```
POST https://api.anthropic.com/v1/messages
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 4096,
  "system": "You are repurposing a blog post into social media content for {FOUNDER_NAME}. Voice profile: {VOICE_PROFILE}. Rules: Each derivative must stand alone without the source post. Rewrite for the format, do not excerpt. LinkedIn posts: 150-300 words with a hook in the first line. Newsletter sections: 300-500 words, more personal and opinionated.",
  "messages": [
    {
      "role": "user",
      "content": "Source blog post:\n\n{BLOG_POST_TEXT}\n\nGenerate:\n1. Three LinkedIn posts (different angles from the source)\n2. One newsletter section\n3. Five standalone social quotes\n\nFor each LinkedIn post, provide: hook, body, CTA, suggested publish day."
    }
  ]
}
```

Schedule derivatives across 2-3 weeks per source post. Week 1: blog post + 1 social post. Week 2: 2 social posts + newsletter mention. Week 3: remaining social posts. This prevents audience fatigue.

### 3. Execute a 6-week content calendar

Run the `social-content-pipeline` drill to establish the weekly cadence:

**Blog content (3-4 posts/week):**
- Generate drafts via Anthropic API using the prompt template refined at Smoke
- Map each post to a content pillar and customer journey stage (problem-aware, solution-aware, product-aware)
- Founder reviews in a single weekly batch session (1 hour)
- Publish to Ghost with full SEO optimization

**Social content (10-15 posts/week across LinkedIn):**
- 5-8 posts repurposed from blog content
- 3-5 original LinkedIn posts from the weekly batch
- 2-3 reactive posts responding to industry news or trending topics

**Human action required:** The founder reviews all blog drafts weekly and approves or edits social posts in batch. At this level, the founder still triggers publishing manually or uses basic scheduling (Typefully or Buffer).

### 4. Analyze performance by content pillar

After 3 weeks, query PostHog to answer:
- Which content pillars drive the most page views?
- Which content pillars drive the most conversions (not just traffic)?
- What is the average time on page by pillar? (Indicates content quality)
- Which social post formats (list, story, contrarian, how-to) drive the most link clicks?
- What is the blog-to-social amplification ratio? (social views per blog post)

Double down on the top 2 performing pillars. Reduce or retire the bottom performer. Adjust the content calendar for weeks 4-6 based on data.

### 5. Optimize content-to-conversion paths

For blog posts with high traffic but low conversions:
- Test different CTAs: inline signup form vs end-of-post CTA vs content upgrade (downloadable PDF)
- Check if the content matches the CTA. A problem-aware blog post should CTA to a guide or newsletter, not a demo request.
- Add exit-intent content upgrades on top-performing posts

For social posts with high engagement but low link clicks:
- Test adding the link in a comment vs in the post body
- Test different value propositions in the CTA line

### 6. Evaluate against threshold

Query PostHog for the 6-week window:
- Total page views across all blog posts: target ≥2,000
- Total conversions: target ≥20
- Average time on page: target ≥2 minutes

If PASS: document content pillar performance rankings, best-performing formats, and the repurposing workflow. Proceed to Scalable.

If FAIL: diagnose by funnel stage. If traffic is low, SEO and distribution need work. If traffic is adequate but conversions are low, CTAs and content-conversion alignment need optimization. Adjust and re-run weeks 4-6.

## Time Estimate

- PostHog event setup: 2 hours
- Weekly blog generation + founder review (6 weeks x 1.5 hours): 9 hours
- Content repurposing system setup: 1 hour
- Weekly social content generation + scheduling (6 weeks x 30 min): 3 hours
- Mid-point analysis (week 3): 1 hour
- CTA optimization: 1 hour
- Final evaluation: 1 hour
- **Total: ~18 hours over 6 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Anthropic Claude API | Generate blog drafts and social derivatives | ~$0.50/mo at this volume (https://platform.claude.com/docs/en/about-claude/pricing) |
| Ghost | Blog publishing and hosting | Free (self-hosted) or $15/mo Starter (https://ghost.org/pricing/) |
| PostHog | Event tracking, funnels, content analytics | Free tier: 1M events/mo (https://posthog.com/pricing) |
| Typefully | Schedule LinkedIn and Twitter/X posts | Free or $8/mo Starter (https://typefully.com/pricing) |
| LinkedIn | Social distribution | Free |

**Play-specific cost: ~$8-23/mo** (Typefully Starter + Ghost Starter if not self-hosted; Claude API cost negligible)

## Drills Referenced

- `content-repurposing` — transform each blog post into 5-10 derivative social and newsletter assets
- `social-content-pipeline` — plan, create, schedule, and track social content across LinkedIn
- `posthog-gtm-events` — implement standardized event taxonomy for content performance tracking
