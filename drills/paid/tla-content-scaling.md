---
name: tla-content-scaling
description: Scale Thought Leader Ad content production by combining organic post batching with systematic ad rotation and creative testing
category: Paid
tools:
  - LinkedIn
  - LinkedIn Ads
  - Anthropic API
  - Taplio
  - n8n
  - PostHog
fundamentals:
  - ai-content-ghostwriting
  - linkedin-organic-hooks
  - linkedin-organic-formats
  - linkedin-organic-posting
  - linkedin-organic-analytics
  - linkedin-ads-thought-leader-setup
  - linkedin-ads-measurement
  - n8n-scheduling
  - n8n-workflow-basics
  - posthog-custom-events
---

# TLA Content Scaling

This drill builds the content engine that feeds your Thought Leader Ad campaigns at scale. The core insight: TLAs require a constant supply of fresh organic posts from the thought leader's profile, and those posts must perform well both organically and as ads. This drill systematizes the publish-measure-promote cycle to sustain 10x the volume of Baseline without proportional time from the thought leader.

## Prerequisites

- Thought Leader Ads running at Baseline level for at least 4 weeks (performance data available)
- Thought leader's voice profile and content pillars established (from `founder-linkedin-content-batch` drill)
- Taplio or equivalent scheduling tool connected
- PostHog and LinkedIn analytics tracking active
- n8n instance for automation

## Input

- Baseline TLA performance data: which posts, pain points, formats, and hooks performed best
- ICP pain point matrix (from Baseline learnings)
- Thought leader's availability for content review (target: 1-2 hours/week)
- Monthly TLA budget (determines how many fresh posts per cycle)

## Steps

### 1. Analyze Baseline Winners to Build the Content Playbook

From your Baseline data, extract the content patterns that work:

1. Pull all promoted posts' performance data using `linkedin-ads-measurement`
2. For each post, tag: hook type (question/stat/story/contrarian), pain point addressed, format (text/image/video/carousel), post length, CTA type
3. Rank by composite metric: (0.4 x engagement rate) + (0.3 x CTR) + (0.3 x conversion rate)
4. Identify the top 3 patterns -- these become your "content templates"

Example output:
- Template A: Personal story about [pain point], 150-200 words, text-only, ends with question CTA. Avg engagement: 2.8%, avg CPC: $3.20
- Template B: Data point + contrarian take on [industry trend], single image with stat overlay, 100-150 words. Avg engagement: 3.5%, avg CPC: $2.10
- Template C: "Here's what I learned after [specific experience]" framework, 200-300 words, carousel format. Avg engagement: 2.1%, avg CPC: $4.50

### 2. Build the Content Production Pipeline

Using the `ai-content-ghostwriting` fundamental, set up a weekly batch production process:

**Week rhythm (ongoing):**
- **Monday:** Agent generates 5-7 draft posts using the winning templates + ICP pain points
- **Tuesday:** Thought leader reviews drafts (target: 30 min). Approves 4-5, provides feedback on the rest
- **Wednesday-Friday:** Schedule 3-4 posts via `linkedin-organic-posting` using Taplio
- **Following week:** Measure organic performance, select top performers for TLA promotion

**Draft generation prompt structure:**
```
You are ghostwriting LinkedIn posts for [thought leader name], [title] at [company].

Voice profile: [paste voice profile]

Write [N] posts using these templates:
- Template A: [description + example]
- Template B: [description + example]

Each post must:
1. Address one of these ICP pain points: [list]
2. Use a specific story, data point, or experience (not generic advice)
3. Open with a hook that creates curiosity in the first line
4. End with a CTA that invites comments (questions perform best for TLA engagement)
5. Be [word count range] words
6. NOT mention [product name] or pitch any solution

Output format: hook | body | CTA | template used | pain point addressed
```

### 3. Automate the Organic-to-Paid Promotion Cycle

Build an n8n workflow using `n8n-scheduling` and `n8n-workflow-basics` that automates the post selection pipeline:

**Workflow: TLA Auto-Promote (runs every Monday)**

1. **Pull last week's organic post performance** via Taplio or Shield API (using `linkedin-organic-analytics`)
2. **Score each post** against the TLA selection criteria from `tla-post-selection` drill:
   - Engagement rate vs profile average
   - ICP comment signals (check for target titles in commenters)
   - Pain point alignment score
3. **Auto-select posts scoring above threshold** (composite score >= 14/20)
4. **Send a Slack notification** with the recommended posts for promotion
5. **Human action required:** Campaign manager reviews the recommendation and adds selected posts to the live TLA campaign in Campaign Manager

Over time, as confidence builds, step 5 can shift from human approval to human veto (auto-promote unless human objects within 24 hours).

### 4. Implement Creative Rotation

TLA creative fatigues faster than company-page ads because the audience sees the same person repeatedly. Build a rotation system:

**Rotation rules:**
- No single post runs as an ad for more than 3 weeks
- Minimum 4 active ads per campaign at all times
- Retire an ad when its engagement rate drops 30% from its first-week average
- Replace retired ads with the next top-scoring organic post from the auto-promote queue

**n8n workflow: TLA Fatigue Monitor (runs daily)**
1. Pull per-ad performance from LinkedIn Marketing API via `linkedin-ads-measurement`
2. Calculate each ad's current-week engagement rate vs first-week engagement rate
3. If decline >= 30%: flag for replacement, send Slack alert
4. If any campaign has fewer than 4 active ads: escalate -- content production needs to accelerate

### 5. Scale the Thought Leader Pool

At scale, a single thought leader becomes a bottleneck. Expand the program:

1. Identify 2-3 additional thought leaders at your company (head of product, lead engineer, customer success lead)
2. Run `tla-post-selection` drill for each new thought leader
3. Grant TLA permissions for each new thought leader
4. Create separate campaign groups per thought leader (different audiences may resonate with different voices)
5. Compare per-thought-leader performance: CPC, engagement rate, conversion rate

This expands your content supply from 3-4 posts/week to 8-12 posts/week without increasing per-person time investment.

### 6. Track Content Velocity Metrics

Using `posthog-custom-events`, track the content pipeline health:

- `tla_posts_published_weekly`: organic posts published by all thought leaders
- `tla_posts_eligible_weekly`: posts that pass the TLA eligibility filter
- `tla_posts_promoted_weekly`: posts added to campaigns
- `tla_posts_retired_weekly`: posts removed due to fatigue
- `tla_content_lead_time_days`: average days between publish and promotion

Set guardrails:
- If `tla_posts_promoted_weekly` drops below 2, content production is falling behind -- increase batch size
- If `tla_content_lead_time_days` exceeds 14, posts are going stale -- accelerate the selection cycle

## Output

- Content production pipeline: 5-7 drafts/week generated, 3-4 published
- Automated organic-to-paid selection workflow in n8n
- Creative rotation system with fatigue detection
- Multi-thought-leader program (2-3 voices)
- Content velocity dashboard in PostHog

## Triggers

- Content batch generation: weekly (Monday)
- Organic-to-paid selection: weekly (following Monday)
- Fatigue monitoring: daily
- Content velocity review: weekly
