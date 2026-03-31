---
name: prospect-content-discovery
description: Find and curate a daily queue of ICP-prospect posts to comment on for the comment-to-DM motion
category: Content
tools:
  - LinkedIn
  - Taplio
  - n8n
fundamentals:
  - linkedin-organic-feed-search
  - linkedin-organic-analytics
  - attio-lists
---

# Prospect Content Discovery

This drill builds the system that fills your daily comment queue -- the posts by ICP prospects and industry voices where your comments earn familiarity and eventual DM access. Without a reliable discovery system, you either comment on the wrong posts or skip days entirely.

## Input

- ICP definition (from `icp-definition` drill): target titles, company sizes, industries, pain points
- List of 20-50 target LinkedIn profiles (prospects, peers, influencers with ICP audiences)
- Attio workspace with prospect records

## Steps

### 1. Build your comment target list

Create three tiers of accounts to monitor:

**Tier 1 -- Direct prospects (10-20 profiles):**
People who could buy your product. Match your ICP exactly: right title, right company size, right industry. These are the accounts you want to DM eventually.

**Tier 2 -- Industry peers (5-10 profiles):**
Other founders, operators, or thought leaders whose audience overlaps your ICP. Commenting on their posts puts your name in front of your prospects without engaging the prospect directly.

**Tier 3 -- Big accounts (5-10 profiles):**
Influencers in your space with 10K+ followers. Your thoughtful comments on their posts get seen by thousands, including your ICP prospects.

Store this list in Attio using the `attio-lists` fundamental. Tag each contact with their tier and the topic areas they typically post about.

### 2. Set up feed monitoring

Using the `linkedin-organic-feed-search` fundamental, configure monitoring for your target list:

**Option A (Manual -- Smoke level):**
1. Turn on LinkedIn bell notifications for all Tier 1 prospects
2. Follow Tier 2 and Tier 3 accounts
3. Each morning, check your LinkedIn notifications tab for new posts
4. Browse the LinkedIn feed for 10 minutes to find additional commentable posts

**Option B (Semi-automated -- Baseline level):**
1. Add all target profiles to Taplio CRM with appropriate tags
2. Check Taplio's "People" section daily for new posts from tracked profiles
3. Use LinkedIn hashtag search for 2-3 pain-point hashtags to find new prospects posting about your topics

**Option C (Automated -- Scalable/Durable levels):**
1. Build an n8n workflow that aggregates posts from Taplio CRM and Shield tracking
2. Apply relevance scoring: topic match + author tier + post freshness + engagement level
3. Deliver a ranked top-10 daily comment queue via Slack or email each morning

### 3. Curate the daily comment queue

Each morning, select 5-10 posts to comment on. Selection criteria:

- **Freshness**: Post is 1-24 hours old (your comment still gets seen)
- **Relevance**: Post topic relates to problems you solve or your domain expertise
- **Author engagement**: Author replies to comments (your comment starts a dialogue)
- **Comment count**: 5-50 existing comments (enough traction but not buried)
- **Strategic value**: Commenting on this person's post moves you closer to a DM opportunity

Record your daily queue: post URL, author name, author tier, and why you chose this post. This log feeds your tracking system.

### 4. Refresh the target list weekly

Every Friday:
1. Review which profiles from your list actually posted this week
2. Remove profiles that have not posted in 3+ weeks (inactive)
3. Add new profiles discovered through this week's feed browsing
4. Promote or demote profiles between tiers based on engagement patterns
5. Update Attio records with any new information learned from their posts

## Output

- A daily queue of 5-10 curated posts to comment on
- A maintained and refreshed target list of 30-50 LinkedIn profiles in Attio
- A weekly log of which posts were discovered and which were commented on

## Triggers

Run this drill every morning before commenting. At Smoke/Baseline: 10-15 minutes manually. At Scalable/Durable: automated delivery via n8n + 5 minutes to review and select.
