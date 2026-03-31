---
name: ai-content-generation-scale-scalable
description: >
  AI Content Generation — Scalable Automation. Automate the full content pipeline with n8n workflows
  for daily multi-platform publishing, AI-driven SEO keyword expansion, A/B testing of content
  formats and CTAs, and content recycling — scaling output 5-10x while reducing founder time to
  30 minutes/week.
stage: "Marketing > Problem Aware"
motion: "FounderSocialContent"
channels: "Content"
level: "Scalable Automation"
time: "50 hours over 2 months"
outcome: "≥8,000 page views/month and conversion rate ≥1.0%"
kpis: ["Page views", "Time on page", "Conversion rate", "Content production velocity", "Organic traffic growth", "Cost per post"]
slug: "ai-content-generation-scale"
install: "npx gtm-skills add marketing/problem-aware/ai-content-generation-scale"
drills:
  - founder-content-scaling
  - ab-test-orchestrator
  - keyword-matrix-builder
---

# AI Content Generation — Scalable Automation

> **Stage:** Marketing → Problem Aware | **Motion:** FounderSocialContent | **Channels:** Content

## Outcomes

Scale content production 5-10x without proportional founder time. At Scalable, n8n workflows automate generation, scheduling, distribution, and engagement collection. The founder's role shrinks to a weekly 30-minute batch review. A/B testing systematically identifies winning content formats and CTAs. A keyword matrix drives programmatic blog content expansion. Success = 8,000+ page views/month with a conversion rate of 1.0% or higher.

## Leading Indicators

- Daily publishing cadence maintained (1 blog post + 2-3 social posts per day)
- Founder review time under 45 minutes/week
- AI draft approval rate above 80% on first pass
- Engagement rate within 80% of Baseline rate (quality holding at scale)
- Organic search traffic growing month over month
- A/B tests producing statistically significant winners within 2-week cycles
- Content recycling generating measurable re-engagement on refreshed posts

## Instructions

### 1. Build the keyword matrix for SEO expansion

Run the `keyword-matrix-builder` drill to systematically expand your blog content targets:

1. Identify 2-3 head term patterns from your Baseline data. Examples: "{your category} for {industry}", "how to {action} with {tool category}", "best {your category} alternatives".
2. Use Ahrefs API to expand each pattern to 50-200 modifier combinations.
3. Validate search demand: filter for volume ≥10/month and difficulty ≤60.
4. Score by priority: `(traffic_potential * 0.6) + ((100 - difficulty) * 0.3) + (cpc * 10 * 0.1)`.
5. Take the top 40-60 keywords as your 2-month content production queue.

Store the matrix in a structured format (JSON or Airtable) that feeds directly into the n8n content generation workflow.

### 2. Automate the content production pipeline

Run the `founder-content-scaling` drill to build the full automation:

**n8n Workflow 1 — Daily Blog Publisher:**
- Trigger: daily cron at 6am
- Pull the next keyword from the content queue (Airtable or Google Sheets)
- Generate a blog draft via Anthropic API using the keyword, content template, and SEO guidelines
- Run a quality check: verify keyword inclusion in title/H1/meta, minimum 1,500 words, no factual claims without sources
- Save to Ghost CMS as a draft
- Log `blog_draft_generated` event to PostHog

**n8n Workflow 2 — Daily Social Publisher:**
- Trigger: daily cron at the optimal posting time (from Baseline performance data)
- Pull the next approved social post from the content queue
- Post via Taplio API or Typefully API
- Log `social_post_published` event to PostHog with properties: pillar, format, hook_type

**n8n Workflow 3 — Engagement Collector:**
- Trigger: daily cron at 6pm
- Pull engagement metrics for all posts published in the last 48 hours
- Update the content queue with actual performance data
- Log `content_engagement_collected` event to PostHog

**n8n Workflow 4 — Content Repurposing Automation:**
- Trigger: when a blog post is published to Ghost (Ghost webhook)
- Generate 3-5 LinkedIn post derivatives via Anthropic API
- Generate 1 newsletter section
- Queue derivatives in the social content calendar, staggered across 2-3 weeks
- Log `content_repurposed` event to PostHog

**n8n Workflow 5 — High-Performer Alert:**
- Trigger: webhook from PostHog when a post exceeds 2x average engagement
- Send Slack alert with post URL and suggested follow-up actions
- Auto-generate a DM follow-up template for top commenters

**Human action required:** Founder reviews the weekly batch of blog drafts (30 minutes) and social posts (15 minutes). Mark each as: approve, edit (with specific changes), or reject. Rejected posts are regenerated. Target: 80%+ approval rate. If approval rate drops below 70%, update the voice profile document.

### 3. Launch systematic A/B testing

Run the `ab-test-orchestrator` drill to test content variables:

**Test 1 (weeks 1-2): Hook styles**
- Control: question-based hooks ("Have you ever...")
- Variant: statistic-based hooks ("73% of startups fail at...")
- Metric: engagement rate per post
- Sample: 10+ posts per variant

**Test 2 (weeks 3-4): CTA types**
- Control: comment CTA ("What's your experience?")
- Variant: link CTA ("Read the full breakdown here")
- Metric: conversions per post
- Sample: 10+ posts per variant

**Test 3 (weeks 5-6): Blog post length**
- Control: 1,500-2,000 words
- Variant: 2,500-3,500 words (comprehensive guides)
- Metric: time on page and conversion rate
- Sample: 5+ posts per variant

**Test 4 (weeks 7-8): Content format**
- Control: text-only LinkedIn posts
- Variant: carousel-style LinkedIn posts (using document upload)
- Metric: impressions and engagement rate
- Sample: 10+ posts per variant

For each test, use PostHog feature flags to track variant assignment. Do not peek at results mid-test. Analyze only when sample size is reached. Implement winners permanently and document learnings.

### 4. Implement content recycling

Build an n8n workflow that identifies and refreshes proven content:

1. Monthly cron trigger: query PostHog for top 10% performing posts published 60+ days ago
2. For each qualifying post, generate a refreshed version via Anthropic API: same core insight, new hook, updated examples and data
3. Add refreshed posts to the content queue
4. Track refresh performance: does the refreshed version match or exceed the original's engagement?

This extends the life of proven content without repeating verbatim.

### 5. Monitor quality guardrails

Set automated guardrails in n8n:

- **Engagement guardrail:** If average engagement rate drops below 60% of Baseline for 2 consecutive weeks, reduce posting frequency by 50% and alert the founder
- **Conversion guardrail:** If conversion rate drops below 0.7% for 2 consecutive weeks, pause blog auto-publishing and review content-CTA alignment
- **Volume guardrail:** Never exceed 2 blog posts/day or 5 social posts/day to prevent audience fatigue
- **Quality guardrail:** If AI draft rejection rate exceeds 30%, pause generation and update the voice profile and prompt templates

### 6. Evaluate against threshold

After 2 months, query PostHog:
- Monthly page views (month 2): target ≥8,000
- Overall conversion rate: target ≥1.0%
- Compare: cost per post at scale vs Baseline (should be lower due to automation)
- Calculate: total time spent / total conversions = hours per conversion

If PASS: document the n8n pipeline configuration, prompt templates, A/B test results, and content performance profile. Proceed to Durable.

If FAIL: analyze which bottleneck is limiting growth. If organic traffic is stalling, the keyword matrix needs expansion or difficulty targets need lowering. If social traffic is plateauing, test new platforms (Twitter/X, newsletter) or new content formats. If conversion rate is below target, focus A/B tests on CTAs and landing page optimization.

## Time Estimate

- Keyword matrix build: 4 hours
- n8n workflow setup (5 workflows): 12 hours
- Weekly founder review (8 weeks x 45 min): 6 hours
- A/B test setup and analysis (4 tests): 8 hours
- Content recycling system: 4 hours
- Guardrail configuration: 2 hours
- Mid-point analysis (week 4): 2 hours
- Final evaluation and documentation: 2 hours
- Ongoing monitoring and adjustments: 10 hours
- **Total: ~50 hours over 2 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Anthropic Claude API | Generate blog drafts, social derivatives, refreshed content | ~$5-10/mo at this volume (https://platform.claude.com/docs/en/about-claude/pricing) |
| Ghost | Blog CMS with API for automated publishing | $15/mo Starter (https://ghost.org/pricing/) |
| PostHog | Analytics, funnels, feature flags, experiments | Free tier or $0/mo up to 1M events (https://posthog.com/pricing) |
| Taplio | LinkedIn scheduling and analytics | $39/mo Starter (https://taplio.com/pricing) |
| Ahrefs | Keyword research and rank tracking | $29/mo Starter (https://ahrefs.com/pricing) |
| n8n | Workflow automation (5 workflows) | Standard stack (excluded) |

**Play-specific cost: ~$88-93/mo** (Taplio $39 + Ahrefs $29 + Ghost $15 + Claude API ~$5-10)

## Drills Referenced

- `founder-content-scaling` — scale founder content 5-10x with AI batch generation, automated cross-platform distribution, and content recycling
- `ab-test-orchestrator` — design, run, and analyze A/B tests on content hooks, CTAs, formats, and lengths
- `keyword-matrix-builder` — build a structured keyword matrix for systematic blog content expansion
