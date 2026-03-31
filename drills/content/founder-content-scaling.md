---
name: founder-content-scaling
description: Scale founder content production 5-10x across LinkedIn, Twitter/X, and newsletter with AI-assisted batch generation and automated cross-platform distribution
category: Content
tools:
  - LinkedIn
  - Twitter/X
  - Anthropic Claude API
  - Taplio
  - Buffer
  - Typefully
  - n8n
  - PostHog
fundamentals:
  - ai-content-ghostwriting
  - linkedin-organic-scheduling
  - linkedin-organic-posting
  - linkedin-organic-analytics
  - linkedin-organic-formats
  - linkedin-organic-hooks
  - twitter-x-engagement
  - n8n-workflow-basics
  - n8n-scheduling
  - posthog-custom-events
---

# Founder Content Scaling

This drill takes a founder content program that works at 3-5 posts/week on LinkedIn (proven at Baseline) and scales it to daily multi-platform publishing with minimal founder time. The founder's review time drops from 2 hours/week to 30 minutes/week while output increases 5-10x.

## Input

- Founder voice profile document (from `ai-content-ghostwriting` fundamental, refined over 4+ weeks of Baseline posting)
- 30+ published posts with engagement data (which topics, formats, and hooks performed best)
- Content pillars (3-5 topics) validated by engagement data
- PostHog tracking active for social content events

## Steps

### 1. Analyze top-performing content patterns

Query PostHog for the last 30 days of content performance data. For each published post, pull: impressions, engagement rate, comments, DMs generated, leads captured. Rank all posts by engagement rate and lead generation.

Extract the patterns:
- Which content pillars produce the most leads (not just engagement)?
- Which post formats (list, story, contrarian, how-to) get the highest engagement rate?
- Which hooks (question, statistic, bold claim, story opener) produce the most impressions?
- What posting times produce the best results?
- What post length range performs best?

Store these patterns as a "content performance profile" that feeds into AI generation.

### 2. Build the AI batch generation pipeline

Using the `ai-content-ghostwriting` fundamental, create a weekly batch generation workflow:

1. **Input assembly**: Combine the founder voice profile, content performance profile, content pillars, and this week's industry news/events into a single prompt context.

2. **Generate 14-21 post drafts per batch**:
   - 7 LinkedIn posts (1 per day, rotating across top-performing pillars and formats)
   - 7 Twitter/X posts (adapted from LinkedIn — shorter, punchier, no hashtags)
   - 3-5 cross-platform variations (same core insight, different format per platform)
   - 2-3 reactive slots left empty for timely content

3. **Each generated post includes**:
   - Platform (LinkedIn or Twitter/X)
   - Hook (first line)
   - Body
   - CTA
   - Suggested publish date and time (based on performance data)
   - Content pillar tag
   - Format tag

4. **Quality filter**: Reject any draft where the hook does not create curiosity or tension in the first 10 words. Reject any draft that uses generic advice instead of specific founder experience. Regenerate rejected posts.

### 3. Streamline founder review

**Human action required:** The founder reviews the batch in a single 30-minute session.

Present all drafts in a structured format (spreadsheet, Notion, or Airtable). For each draft, the founder marks: approve, edit (with specific changes), or reject. Edited posts go back through the LLM with the founder's feedback for a second pass. Rejected posts are replaced with new generations.

Target: 80%+ approval rate on first pass. If approval rate is below 70%, the voice profile needs updating.

### 4. Build the n8n distribution automation

Using `n8n-workflow-basics` and `n8n-scheduling`, create the following workflows:

**Workflow 1: Daily LinkedIn Publisher**
- Trigger: Daily cron at the optimal posting time (from performance data)
- Action: Pull the next approved LinkedIn post from the content queue (Airtable, Google Sheets, or Attio)
- Post via Taplio API, Buffer API, or Typefully API using `linkedin-organic-posting`
- Log the publish event to PostHog: `linkedin_post_published` with properties: pillar, format, hook_type, scheduled_time

**Workflow 2: Daily Twitter/X Publisher**
- Trigger: Daily cron offset 2 hours from LinkedIn post time
- Action: Pull the next approved Twitter/X post from the content queue
- Post via Typefully API or Buffer API
- Log: `twitter_post_published` event to PostHog

**Workflow 3: Engagement Collector**
- Trigger: Daily cron at 6pm
- Action: Pull engagement metrics for all posts published in the last 48 hours using `linkedin-organic-analytics`
- Update the content queue with actual performance data
- Log: `content_engagement_collected` event to PostHog with per-post metrics

**Workflow 4: Lead Alert**
- Trigger: Webhook from Taplio/Shield when a post exceeds 2x average engagement rate
- Action: Send Slack alert to founder with the post URL and suggested DM follow-up for top commenters
- This ensures the founder engages on high-performing posts even when publishing is automated

### 5. Implement content recycling

Top-performing posts (top 10% by engagement) enter a recycling queue. After 60 days, the AI generates a refreshed version of the post: same core insight, new hook, updated examples. This extends the life of proven content without repeating it verbatim.

Using `n8n-scheduling`, schedule a monthly recycling review:
1. Query PostHog for top 10% posts from 60+ days ago
2. Generate refreshed versions via `ai-content-ghostwriting`
3. Add refreshed posts to the content queue for the next batch

### 6. Cross-platform content adaptation

Each original LinkedIn post should produce at least 2 derivative pieces:

- **LinkedIn to Twitter/X**: Extract the core insight. Compress to 280 characters or a 3-5 tweet thread. Remove line breaks used for LinkedIn formatting. Make the tone more conversational and direct.
- **LinkedIn to newsletter snippet**: Take the week's best-performing post and expand it into a 300-500 word newsletter section with additional depth, data, or personal context.

Build this adaptation into the batch generation step (Step 2) so all versions are generated together and reviewed in the same founder session.

### 7. Track scaling metrics

Using `posthog-custom-events`, track weekly:
- Total posts published across all platforms
- Average engagement rate per platform (should stay within 80% of Baseline rate)
- Leads generated per post (should stay stable or improve)
- Founder time spent on content (target: <45 minutes/week at full scale)
- AI draft approval rate (target: >80% first pass)

**Guardrail**: If average engagement rate drops below 60% of Baseline for 2 consecutive weeks, reduce posting frequency and investigate. Scaling should not sacrifice quality.

## Output

- 14-21 posts per week scheduled across LinkedIn and Twitter/X
- Automated daily publishing and engagement collection
- Founder review time reduced to 30 minutes/week
- Content performance tracking flowing to PostHog
- Content recycling system extending the life of proven posts

## Triggers

Run the batch generation weekly (Friday or Monday). Daily publishing and engagement collection run automatically via n8n. Monthly recycling review runs on the first Monday of each month.
