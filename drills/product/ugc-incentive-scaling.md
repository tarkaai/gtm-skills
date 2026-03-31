---
name: ugc-incentive-scaling
description: Design and automate tiered incentive programs that scale UGC production without proportional cost
category: Product
tools:
  - PostHog
  - n8n
  - Intercom
  - Loops
  - Attio
fundamentals:
  - posthog-feature-flags
  - posthog-custom-events
  - posthog-cohorts
  - n8n-workflow-basics
  - n8n-scheduling
  - n8n-triggers
  - intercom-in-app-messages
  - loops-sequences
  - loops-transactional
  - attio-lists
  - attio-contacts
  - attio-custom-attributes
---

# UGC Incentive Scaling

This drill designs the incentive mechanics that multiply UGC production: contests, recognition programs, creator tiers, and reward systems that motivate users to create content repeatedly without requiring linear increases in budget or manual effort. The 10x comes from making content creation self-reinforcing.

## Prerequisites

- UGC collection and amplification pipelines running for at least 4 weeks (baseline UGC volume established)
- PostHog tracking all UGC events (submission, moderation, amplification)
- Attio with UGC Contributors list populated
- Intercom and Loops configured

## Steps

### 1. Analyze baseline creator behavior

Before designing incentives, understand current creator patterns:

Query PostHog and Attio for:
- How many unique creators submitted content in the last 30 days?
- What percentage are repeat contributors (2+ submissions)?
- Which trigger moments produce the most submissions?
- What content types are submitted most vs. least?
- What is the average time between a user's first and second submission?
- What is the correlation between power user score and UGC likelihood?

These baselines tell you what to incentivize: if repeat rate is low, incentivize second submissions. If certain content types are missing, incentivize those specifically.

### 2. Design the creator tier system

Using `attio-custom-attributes`, add UGC-specific attributes to contact records:

**Tier 1 — First-time Creator:**
- Entry: first approved submission
- Reward: public thank-you in community channel + "Contributor" badge in product
- Goal: get them to submit a second piece within 30 days

**Tier 2 — Active Creator (3+ approved pieces):**
- Entry: 3rd approved submission
- Reward: "Creator" badge visible to other users + featured creator spotlight in newsletter + 1 month of free feature credit or plan upgrade
- Goal: sustain 1+ piece per month

**Tier 3 — Featured Creator (5+ pieces with avg quality score >= 4):**
- Entry: 5th approved submission AND average quality score >= 4.0
- Reward: permanent "Featured Creator" badge + co-marketing opportunity (guest blog, webinar) + direct line to product team + annual swag package
- Goal: become a long-term brand advocate producing flagship content

Using `posthog-feature-flags`, gate creator badges by tier. The badge appears in the product UI next to the user's name in collaborative features.

### 3. Build contest mechanics

Design recurring UGC contests that create urgency and friendly competition:

**Monthly themed contest:**
- Theme rotates: "Best workflow automation" -> "Most creative use case" -> "Best tip for new users" -> "Video walkthrough challenge"
- Submission window: 2 weeks open, 1 week judging
- Prizes: Winner gets featured blog post + $100 credit. Top 3 get social amplification. All participants get a badge.
- Promotion: Intercom in-app banner during contest window + Loops email announcement

Using `n8n-scheduling`, automate the contest lifecycle:
1. Day 1: send announcement email and show in-app banner
2. Day 7: send "1 week left" reminder to users who haven't submitted
3. Day 14: close submissions, run AI moderation on all entries
4. Day 15-21: human judges rank the top 10 AI-approved entries
5. Day 22: announce winner via email, social post, and in-app message
6. Day 23: send prizes and update creator tiers

Track contest events:
- `ugc_contest_announced` — contest goes live
- `ugc_contest_entered` — user submits for contest
- `ugc_contest_winner_selected` — judging complete
- `ugc_contest_reward_delivered` — prize sent

### 4. Deploy social proof loops

Make UGC visible to other users to create a flywheel:

**In-product UGC showcase:**
Using `intercom-in-app-messages`, create a "Community creations" widget or message series showing recent approved UGC to non-creators. Show content from users in similar roles or industries. Include a CTA: "Share your story too."

**Creator leaderboard:**
Build a PostHog dashboard or in-product page showing:
- Top creators this month (by approved submissions)
- Total UGC pieces created by the community
- Latest featured content

The leaderboard creates status motivation: users see others getting recognition and want to participate.

**Social proof in prompts:**
Update the UGC prompts (from `ugc-prompt-design`) to include social proof: "47 users shared their setup this month. Join them." This makes creating content feel normal, not exceptional.

### 5. Automate reward delivery

Using `n8n-triggers`, listen for tier promotion events and deliver rewards automatically:

**Badge delivery:**
When a user crosses a tier threshold, the n8n workflow:
1. Updates `attio-contacts` with the new tier
2. Enables the appropriate `posthog-feature-flags` badge flag
3. Sends a congratulatory `intercom-in-app-messages` with the new badge and benefits
4. Fires `ugc_creator_promoted` PostHog event

**Credit/perk delivery:**
When an Active Creator earns a feature credit:
1. If your billing supports API credits: apply via billing API
2. If manual: create an Attio task for the team to apply the credit within 48 hours
3. Send confirmation via `loops-transactional`

**Swag delivery (Featured Creators):**
1. Create an Attio task: "Ship swag to [Creator Name], [address]"
2. **Human action required:** Team fulfills swag order

### 6. Track incentive program performance

Fire PostHog events for the full incentive lifecycle:

| Event | Properties |
|-------|-----------|
| `ugc_creator_promoted` | from_tier, to_tier, total_submissions, avg_quality |
| `ugc_contest_entered` | contest_theme, content_type, submitter_tier |
| `ugc_reward_delivered` | reward_type, creator_tier, reward_value |
| `ugc_leaderboard_viewed` | viewer_tier, viewer_has_submissions |
| `ugc_social_proof_shown` | proof_type, viewer_tier |
| `ugc_social_proof_clicked` | proof_type, viewer_converted_to_creator |

Key metrics to track:
- Repeat creator rate (target: 30%+ of creators submit 2+ pieces)
- Tier promotion rate (target: 20%+ of First-timers reach Active Creator)
- Contest participation rate (target: 5%+ of eligible users enter)
- Social proof conversion (target: 3%+ of users shown UGC create their own)

## Output

- 3-tier creator program with automated enrollment and promotion
- Monthly contest framework with automated lifecycle management
- Social proof loops (in-product showcase, leaderboard, proof-enhanced prompts)
- Automated reward delivery for badges, credits, and swag tasks
- Full PostHog event tracking for incentive performance

## Triggers

Creator tier checks run daily via n8n cron. Contest lifecycle runs on the monthly schedule. Social proof content refreshes weekly. Reward delivery fires on tier promotion events. All workflows are always-on.
