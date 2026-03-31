---
name: thought-leadership-content-audit
description: Audit existing founder content across platforms, identify high-performers, define content pillars and voice profile for systematic thought leadership
category: Thought Leadership
tools:
  - Clay
  - Attio
  - Anthropic Claude API
  - LinkedIn
  - Twitter/X
fundamentals:
  - linkedin-organic-analytics
  - clay-table-setup
  - clay-scoring
  - ai-content-ghostwriting
  - attio-notes
---

# Thought Leadership Content Audit

This drill produces a baseline assessment of the founder's existing content footprint and defines the strategic inputs (pillars, voice profile, audience mapping) needed to run a thought leadership program. Without this audit, subsequent content creation drills operate blind.

## Input

- Founder's LinkedIn profile URL
- Founder's Twitter/X handle (if active)
- Company blog URL (if the founder has published posts)
- ICP definition: job titles, industries, company sizes, pain points
- List of 2-3 competitors whose founders are active content creators

## Steps

### 1. Pull existing content inventory

Use the `linkedin-organic-analytics` fundamental to export the founder's last 90 days of LinkedIn posts. For each post, capture:
- Post date
- Post text (first 300 characters minimum)
- Format (text, carousel, image, video, poll, document)
- Impressions
- Engagement count (likes + comments + shares)
- Engagement rate (engagement / impressions)
- Comment count
- Top 3 commenter job titles (if visible)

If the founder posts on Twitter/X, repeat the process manually: pull their last 50 tweets, record impressions, likes, replies, and retweets from Twitter Analytics.

If the founder has blog posts, list the 10 most recent with title, publish date, and traffic data (from PostHog or Google Analytics).

### 2. Build the audit table in Clay

Use the `clay-table-setup` fundamental to create a table called "TL Content Audit - {founder name} - {date}" with columns:

| Column | Type | Notes |
|--------|------|-------|
| platform | Select | linkedin / twitter / blog |
| post_date | Date | When published |
| post_text_preview | Text | First 200 characters |
| format | Select | text / carousel / image / video / poll / document |
| topic | Text | Agent-assigned topic label |
| pillar | Select | Assigned after pillar definition |
| impressions | Number | |
| engagement_rate | Number | Decimal (0.025 = 2.5%) |
| comments | Number | |
| icp_comments | Number | Comments from people matching ICP titles |
| link_clicks | Number | If available |
| score | Number | Composite score (step 4) |

Import all content from step 1.

### 3. Classify topics and identify patterns

For each post in the table, use Claude API to classify the topic into a candidate pillar. Prompt:

```
You are analyzing a founder's LinkedIn/Twitter content. For each post below, assign a topic label (3-5 words, e.g., "hiring remote engineers", "product-led growth tactics", "founder mental health"). Also flag the hook type: personal story, data insight, contrarian take, tactical how-to, industry commentary, or question.

Posts:
{post_text_preview for all posts}
```

Write the topic and hook type back to the Clay table.

### 4. Score each post

Use the `clay-scoring` fundamental:
- **Engagement rate (40%):** Normalize engagement rate within the dataset to 1-5
- **ICP resonance (30%):** Ratio of ICP-matching commenters to total commenters (1-5)
- **Comment depth (20%):** Posts with 3+ multi-sentence comments score higher (1-5)
- **Link performance (10%):** If link clicks available, normalize to 1-5. Otherwise use engagement rate as proxy.

Composite score = weighted average. Sort descending.

### 5. Define content pillars

Analyze the scored posts to identify 3-5 content pillars:
1. Group posts by topic classification from step 3
2. For each topic group, calculate: average score, total posts, average engagement rate
3. Select 3-5 pillars that meet ALL of:
   - Average score >= 3.5
   - At least 3 posts in the topic
   - Aligns with an ICP pain point
4. If fewer than 3 pillars meet criteria, add pillars based on ICP pain points that the founder has expertise in but has not yet written about

For each pillar, document:
- Pillar name (e.g., "Engineering hiring in the AI era")
- ICP pain point it addresses
- Evidence: top 3 posts in this pillar with scores
- Content formats that work best for this pillar
- Target posting frequency (1-2x/week per pillar)

### 6. Build the voice profile

Use the `ai-content-ghostwriting` fundamental's voice profiling process:
1. Select the top 10 scoring posts from the audit
2. Feed them to Claude API with the prompt: "Analyze these posts and produce a voice profile document: vocabulary patterns, sentence structure, tone (formal/casual scale 1-10), use of personal anecdotes (frequency), data usage, humor style, rhetorical devices, typical post length, and hook patterns."
3. Store the voice profile in Attio as a note on the founder's contact record using the `attio-notes` fundamental

### 7. Map the competitive content landscape

For each competitor founder:
1. Pull their last 20 LinkedIn posts
2. Classify topics and formats
3. Identify gaps: topics your founder covers that competitors do not (differentiation opportunities)
4. Identify overlaps: topics both cover (need for sharper angles)

Log competitive findings in Attio notes.

## Output

- Scored content inventory in Clay (every post ranked)
- 3-5 defined content pillars with evidence and ICP alignment
- Founder voice profile document stored in Attio
- Competitive content landscape map
- Recommended posting cadence per pillar

## Triggers

- Run once at play start (Smoke level)
- Re-run quarterly to refresh pillars and update the voice profile as the founder's style evolves
