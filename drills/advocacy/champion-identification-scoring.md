---
name: champion-identification-scoring
description: Build a composite scoring model from community contribution data to identify users who help others, answer questions, and share knowledge
category: Advocacy
tools:
  - PostHog
  - Attio
  - Slack API
  - Discord API
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - posthog-funnels
  - attio-lists
  - attio-custom-attributes
  - slack-api-read
  - discord-api-read
  - community-engagement-tracking
  - n8n-scheduling
  - n8n-workflow-basics
---

# Champion Identification Scoring

This drill builds a scoring model that identifies community champions: users who actively help others, answer questions, share knowledge, and create content that benefits the community. This is distinct from `power-user-scoring` which measures product usage depth. Champion scoring measures contribution to others.

## Prerequisites

- Active community channels (Slack, Discord, forum, or social) with at least 30 days of activity
- PostHog tracking community-related events (from `community-engagement-tracking`)
- Attio configured with user contact records
- Access to read community channel data via API or bot

## Steps

### 1. Define the champion scoring dimensions

Community champions are identified by their contribution behavior, not their product usage. Build the composite score from five dimensions, each weighted 0-100:

**Helpfulness (weight: 35%)**
Using `slack-api-read` or `discord-api-read`, extract:
- Questions answered: messages that are replies to questions from other users in help/support channels
- Solution acceptance: replies that received a thumbs-up, check-mark reaction, or "thanks" response from the question asker
- Thread participation: distinct threads where the user contributed a substantive reply (>50 characters)
- Help channel activity ratio: percentage of the user's messages that appear in help/support channels vs general chat

Score formula: `(questions_answered / max_answers) * 0.4 + (solutions_accepted / max(questions_answered, 1)) * 0.3 + min(thread_participation / 20, 1) * 0.2 + help_ratio * 0.1`

**Content creation (weight: 25%)**
Track contributions that create lasting community value:
- Original posts or threads started that generated 5+ replies (sparked discussion)
- Shared resources: messages containing links to tutorials, guides, templates, or code snippets they created
- Long-form contributions: messages over 200 characters that provide explanations, walkthroughs, or how-tos
- External content: blog posts, videos, or social posts about the product shared in community channels

Score formula: `min(discussion_posts / 5, 1) * 0.3 + min(resources_shared / 10, 1) * 0.3 + min(longform_count / 15, 1) * 0.2 + min(external_content / 3, 1) * 0.2`

**Consistency (weight: 20%)**
Champions contribute reliably, not just in bursts:
- Active weeks out of total weeks since joining (consistency ratio)
- Current streak: consecutive weeks with at least 3 community interactions
- Time span: days since first community contribution
- Recency: days since last community contribution (inverse weight: more recent is better)

Score formula: `consistency_ratio * 0.4 + min(current_streak / 8, 1) * 0.3 + min(days_since_first / 90, 1) * 0.2 + max(1 - (days_since_last / 14), 0) * 0.1`

**Community reach (weight: 10%)**
Measure how many distinct community members the champion has helped or interacted with:
- Distinct users who received a reply from this champion
- Distinct threads where their message was the most-reacted message
- Mentions by other users (people tagging them for help)

Score formula: `min(distinct_users_helped / 20, 1) * 0.5 + min(top_reactions / 5, 1) * 0.3 + min(mentions_by_others / 10, 1) * 0.2`

**Product expertise signal (weight: 10%)**
Cross-reference community contribution with product usage to identify champions who are also knowledgeable users:
- Features mentioned in their help responses (breadth of product knowledge)
- Accuracy: do the users they help actually succeed? (Track if helped users complete the action within 48 hours)
- Integration or advanced feature references in their contributions

Score formula: `min(features_mentioned / 10, 1) * 0.5 + min(helped_user_success_rate, 1) * 0.3 + min(advanced_references / 5, 1) * 0.2`

**Composite score**: `helpfulness * 0.35 + content * 0.25 + consistency * 0.20 + reach * 0.10 + expertise * 0.10`

### 2. Implement the data extraction pipeline

Using `n8n-scheduling`, create a weekly workflow that runs every Sunday evening:

1. Pull community data for the trailing 30 days:
   - Slack: use `slack-api-read` to read messages from help channels, support channels, and general channels. Extract user IDs, message text, timestamps, reactions, thread metadata.
   - Discord: use `discord-api-read` to read messages from the same channel types. Extract the same data points.
   - Forum/social: if applicable, use platform APIs or Common Room integration to pull data.

2. For each active community member (at least 3 messages in 30 days):
   - Compute each dimension score using the formulas above
   - Compute the composite champion score
   - Classify: Champion (>=75), Strong Contributor (50-74), Active Member (25-49), Lurker (<25)

3. Fire a PostHog event using `posthog-custom-events`:

```javascript
posthog.capture('champion_score_computed', {
  composite_score: 82,
  helpfulness_score: 90,
  content_score: 75,
  consistency_score: 85,
  reach_score: 60,
  expertise_score: 78,
  tier: 'champion',
  questions_answered_30d: 34,
  distinct_users_helped_30d: 18,
  percentile: 96
});
```

### 3. Create champion cohorts

Using `posthog-cohorts`, define tiered cohorts:

- **Champions** (score >= 75, top ~5%): the core group. These users shape the community. They answer more questions than they ask, they create content, and they show up consistently.
- **Strong Contributors** (score 50-74, top ~15%): regular helpers who have not yet reached champion level. Nurture them toward champion status.
- **Active Members** (score 25-49): participate but mostly consume rather than contribute. Not champion candidates yet.
- **Lurkers** (score < 25): minimal community contribution. Not scored.

### 4. Sync scored members to CRM

Using `attio-custom-attributes`, create attributes on contacts:
- `champion_score`: integer 0-100
- `champion_tier`: Champion / Strong Contributor / Active Member / Lurker
- `champion_score_date`: last computation date
- `champion_helpfulness_score`: integer 0-100
- `champion_content_score`: integer 0-100
- `champion_questions_answered_30d`: integer
- `champion_distinct_users_helped_30d`: integer

Using `attio-lists`, create a "Community Champion Candidates" list filtered to score >= 50. This list feeds the recognition pipeline.

### 5. Build the champion leaderboard dashboard

Build a PostHog dashboard with:
- Distribution histogram of champion scores (identifying the natural tiers)
- Tier breakdown: count and percentage in each tier
- Top 20 champions ranked by composite score with dimension breakdown
- Score trend over time: is the champion population growing or shrinking?
- Rising contributors: users with the highest month-over-month score increase
- Helpfulness heat map: which channels have the most champion activity?

### 6. Validate and calibrate

Review the top 20 scored members manually:
- Are these the people you would recognize as community champions?
- Are any obvious community heroes missing? Check dimension weights.
- Are any low-contribution users scoring high? Look for gaming (e.g., many short "me too" replies inflating thread count).
- Cross-reference with any existing community recognition (badges, moderator roles) to validate.

Adjust weights until the top 20 matches your intuition. Lock weights and document the calibration.

## Output

- Composite champion score computed weekly for all active community members
- 4-tier classification system in PostHog
- Scored member list synced to Attio with tier labels and dimension scores
- Champion leaderboard dashboard in PostHog
- Calibrated and documented scoring weights

## Triggers

Run the scoring pipeline weekly via n8n cron. Re-calibrate weights quarterly or when community dynamics change significantly (new channels, platform migration, etc.).
