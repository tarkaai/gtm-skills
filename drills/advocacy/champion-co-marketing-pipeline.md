---
name: champion-co-marketing-pipeline
description: Scale co-marketing with community champions through guest content, social amplification, and joint events
category: Advocacy
tools:
  - PostHog
  - n8n
  - Loops
  - Attio
  - Intercom
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - n8n-scheduling
  - n8n-triggers
  - n8n-workflow-basics
  - loops-sequences
  - loops-transactional
  - attio-lists
  - attio-contacts
  - attio-notes
  - intercom-in-app-messages
---

# Champion Co-Marketing Pipeline

This drill scales the co-marketing relationship with community champions. Instead of one-off asks, it creates a systematic pipeline of co-marketing opportunities: guest blog posts, social media amplification, webinar appearances, case studies, and community event co-hosting. The pipeline matches champions to opportunities based on their strengths and interests, tracks conversion from co-marketing content to signups, and maintains the relationship without burning out champions.

## Prerequisites

- Champion recognition pipeline active with at least 10 Champions enrolled (run `champion-recognition-pipeline`)
- Attio with champion tier data and contribution dimension scores
- Content calendar or editorial process for blog/social content
- Ability to host webinars or community events

## Steps

### 1. Build the opportunity matching engine

Not every champion is suited for every co-marketing activity. Using champion dimension scores from `champion-identification-scoring`, match champions to opportunities:

| Opportunity | Best Match | Champion Signal |
|-------------|-----------|-----------------|
| Guest blog post | High content creation score (>=60) | Already writes long-form community contributions |
| Social media amplification | High community reach score (>=50) | Interacts with many distinct users, active on social |
| Webinar co-host | High helpfulness score (>=70) + high expertise score (>=60) | Explains concepts clearly, deep product knowledge |
| Case study interview | High consistency score (>=70) | Long tenure, reliable engagement, compelling usage story |
| Community event co-host | High helpfulness score (>=80) + high reach score (>=60) | Known community figure, helps many people |

Using `attio-lists`, create 5 segmented lists corresponding to each opportunity type. Populate them using champion dimension scores. A champion can appear on multiple lists.

### 2. Automate the opportunity cadence

Using `n8n-scheduling`, create a monthly workflow that manages the co-marketing pipeline:

1. Query Attio for all Champions (tier = Champion) with their dimension scores and last co-marketing activity date
2. Filter: exclude champions who completed a co-marketing activity in the last 30 days (prevent burnout), exclude champions who declined the last 2 invitations (they are not interested right now)
3. For each opportunity type, rank eligible champions by fit score (dimension match) and select the top 3 candidates
4. Queue the invitations:
   - Blog: send a Loops email with a topic suggestion based on their most common help topics and a writing brief template
   - Social amplification: send a Loops email with a pre-written post they can customize and share, plus their referral link embedded
   - Webinar: send a Loops email with the proposed topic, date, and time commitment (30 min prep + 45 min live)
   - Case study: send a Loops email with 5 interview questions and an estimate of time (20 min async written or 30 min call)
   - Community event: send a Loops email with the event concept and their proposed role

5. Log each invitation in Attio using `attio-notes`: opportunity type, date sent, champion name, topic
6. Track responses: accepted, declined, no response after 7 days

### 3. Automate content amplification tracking

When a champion creates or co-creates content, track its impact through the full funnel:

Using `posthog-custom-events`, fire events at each stage:

```javascript
posthog.capture('champion_content_published', {
  champion_id: 'usr_123',
  content_type: 'guest_blog',
  topic: 'how-i-automated-my-workflow',
  publish_url: 'https://yoursite.com/blog/champion-post',
  champion_referral_link_embedded: true
});

posthog.capture('champion_content_engaged', {
  champion_id: 'usr_123',
  content_type: 'guest_blog',
  engagement_type: 'page_view',
  source: 'champion_social_share'
});

posthog.capture('champion_content_converted', {
  champion_id: 'usr_123',
  content_type: 'guest_blog',
  conversion_type: 'signup',
  referee_id: 'usr_456'
});
```

Build a PostHog funnel per content piece: published -> viewed -> engaged (scroll depth >50%) -> CTA clicked -> signed up -> activated.

### 4. Build the social amplification kit

For champions who match the social amplification profile, automate the creation and distribution of shareable content:

Using `n8n-scheduling`, create a biweekly workflow:

1. Pull the latest product content (new features, blog posts, case studies, community highlights)
2. For each content piece, generate 3 social post variants: LinkedIn professional tone, Twitter conversational tone, community channel casual tone
3. Embed each champion's unique referral link in the post
4. Using `loops-transactional`, send each champion a personalized social kit: "Here are 3 posts you can share this week. Each includes your personal referral link. Just copy, customize if you want, and post."
5. Track which champions share, which posts perform best, and which generate signups

### 5. Manage the co-marketing relationship lifecycle

Champions burn out when over-asked. Using `attio-contacts` and `n8n-scheduling`, enforce relationship guardrails:

- **Maximum ask frequency**: no more than 1 co-marketing invitation per champion per month
- **Cool-down after completion**: 30 days after completing a co-marketing activity before the next ask
- **Decline tracking**: after 2 consecutive declines, pause co-marketing asks for 90 days (continue recognition perks)
- **Gratitude loop**: after every completed co-marketing activity, send a personalized thank-you via `loops-transactional` with their content's impact stats (views, signups, revenue attributed)
- **Annual recognition**: at year-end, send top co-marketing champions a personalized impact report: "Your 4 blog posts generated 230 views and 12 signups. Your referral link brought in 8 new users. Thank you."

### 6. Build the co-marketing dashboard

Create a PostHog + Attio reporting layer:

- **Pipeline health**: invitations sent -> accepted -> published -> measured
- **Content performance by type**: blog, social, webinar, case study, event. Rank by signups per content piece.
- **Champion leaderboard**: total co-marketing activities completed, total signups attributed, total revenue attributed
- **Champion capacity**: how many champions are available (not in cool-down or declined) for each opportunity type
- **ROI**: total signups and revenue from co-marketing / total cost of champion perks and content production
- **Burnout risk**: champions with 3+ activities in 90 days, champions with declining engagement after co-marketing asks

## Output

- Opportunity matching engine based on champion dimension scores
- Monthly automated invitation cadence with burnout guardrails
- Social amplification kit delivered biweekly with personalized referral links
- Content-to-signup tracking for every co-marketing piece
- Relationship lifecycle management with cool-downs and gratitude loops
- Co-marketing dashboard with ROI tracking

## Triggers

Monthly opportunity matching runs on the 1st of each month. Social amplification kits deploy biweekly. Tracking and gratitude are event-driven. All workflows are always-on after initial setup.
