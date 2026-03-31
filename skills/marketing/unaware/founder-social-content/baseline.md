---
name: founder-social-content-baseline
description: >
  Founder Social & Content — Baseline Run. First always-on content system: automated scheduling,
  PostHog tracking, content repurposing across formats, and systematic lead capture from engagement.
stage: "Marketing > Unaware"
motion: "FounderSocialContent"
channels: "Social"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 1 meeting per week sustained over 2 weeks"
kpis: ["Impressions per post", "Engagement rate", "Profile visits", "Leads captured per week", "Meetings booked per week"]
slug: "founder-social-content"
install: "npx gtm-skills add marketing/unaware/founder-social-content"
drills:
  - posthog-gtm-events
  - content-repurposing
  - linkedin-lead-capture
---

# Founder Social & Content — Baseline Run

> **Stage:** Marketing → Unaware | **Motion:** FounderSocialContent | **Channels:** Social

## Outcomes

Transition from manual posting to a repeatable, always-on content system. Automated scheduling replaces daily manual posting. PostHog tracking replaces spreadsheet logging. Content repurposing multiplies output from each original piece. Lead capture becomes systematic. Success = at least 1 meeting per week sustained over 2 consecutive weeks from content-attributed leads.

## Leading Indicators

- Publishing cadence held at 3-5 posts/week for full 2-week period (no missed days)
- PostHog receiving all content events (post published, engagement, lead captured)
- Content repurposing producing 2-3 derivative pieces per original post
- Lead capture workflow running daily (manual or semi-automated)
- Profile views sustained at 50+/week
- Engagement rate holding within 80% of Smoke test levels

## Instructions

### 1. Set up content analytics tracking

Run the `posthog-gtm-events` drill to implement the social content event taxonomy:

Define and start tracking these events:
- `social_post_published` — properties: platform (linkedin), pillar, format, hook_type, post_url
- `social_engagement_received` — properties: post_url, likes, comments, shares, impressions (collected 48h after publish)
- `social_profile_visit` — properties: visitor_count (daily from LinkedIn Analytics or Taplio)
- `social_dm_received` — properties: sender_title, sender_company, buying_signal (boolean)
- `social_lead_captured` — properties: lead_name, source_post_url, signal_type, lead_title
- `social_meeting_booked` — properties: lead_name, source_post_url, days_from_first_engagement

Connect LinkedIn analytics to PostHog via n8n webhooks. Use Taplio API or Shield API (see `linkedin-organic-analytics` fundamental) to pull post-level metrics daily and send to PostHog. This replaces the manual spreadsheet from Smoke.

### 2. Build the content repurposing pipeline

Run the `content-repurposing` drill to multiply output from each original post:

For each LinkedIn post published:
1. Extract the core insight as an atomic unit.
2. Adapt to Twitter/X: compress to 280 characters or a 3-5 tweet thread. More conversational tone, no line-break formatting.
3. If the post performs well (top 25% by engagement after 48 hours), flag it for newsletter expansion — expand the insight into a 300-500 word piece with additional context and data.
4. Accumulate 3-4 high-performing posts for a monthly blog roundup or long-form article.

Target: each original LinkedIn post produces 2-3 derivative pieces across other formats. This brings total content output to 9-15 pieces/week from 3-5 original posts.

### 3. Set up scheduled publishing

Move from manual daily posting to scheduled batches:

1. Use Taplio, Buffer, or Typefully to schedule the week's content in advance.
2. Run the `founder-linkedin-content-batch` drill weekly (Friday or Monday) to generate next week's content.
3. Schedule LinkedIn posts for optimal times identified during Smoke (default: Tue-Thu at 8am in ICP timezone).
4. Schedule Twitter/X adaptations for 2 hours after the LinkedIn post goes live.

**Human action required:** The founder still reviews and approves all content before scheduling. Target: 1.5 hours per week for batch review and approval. The founder still personally replies to comments and sends DMs — engagement is not automated at this level.

### 4. Implement systematic lead capture

Run the `linkedin-lead-capture` drill to build the lead capture system:

**Daily lead capture process:**
1. Review DMs, comments, and connection requests for buying signals.
2. Classify each engager by intent level: Very High (DM about product), High (comment describing a problem you solve), Medium (multiple engagements from same person), Low (single like from ICP match).
3. For High and Very High intent: create a lead record in Attio with source attribution (social_content, source_post_url, signal_type).
4. For Medium intent: add to a watch list. Continue engaging with their content. Upgrade to lead if they show a stronger signal within 2 weeks.

**Weekly review (Friday):**
- Total leads captured this week
- Leads by signal type (which signals produce the most meetings?)
- Leads by content pillar (which topics attract buyers?)
- Pipeline: leads -> DM conversations -> meetings booked
- Compare to threshold: ≥ 1 meeting per week

### 5. Evaluate against threshold

At the end of 2 weeks, measure:

**Pass threshold:** ≥ 1 meeting per week sustained over 2 weeks (minimum 2 meetings total)

Meetings must be attributable to social content: the prospect engaged with your content (liked, commented, DMed, or visited your profile from content) before the meeting was booked.

If PASS: document the working system — which pillars drive leads, which formats get engagement, which engagement signals predict meetings. Proceed to Scalable.

If FAIL: diagnose —
- Publishing cadence broken? Scheduling failed or content batch was not prepared. Fix the weekly batch habit.
- Good engagement but no leads? Content attracts audience but not buyers. Shift pillars toward more specific ICP problems.
- Leads but no meetings? DM follow-up is weak or too slow. Respond to buying signals within 4 hours.
- PostHog events not flowing? Fix tracking first. Cannot optimize what is not measured.

Re-run for another 2-week cycle with adjustments.

## Time Estimate

- PostHog event setup: 2 hours (one-time)
- Weekly content batch generation and review: 1.5 hours x 2 weeks = 3 hours
- Content repurposing setup: 1.5 hours (one-time)
- Daily engagement and lead capture (10 days x 25 min): 4 hours
- Weekly reviews (2 x 30 min): 1 hour
- Evaluation: 30 minutes
- **Total: ~12 hours over 2 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn (free account) | Publishing, engagement, DMs | Free |
| Taplio | LinkedIn analytics + scheduling | ~$49/mo (https://taplio.com/pricing) |
| PostHog | Event tracking and analytics | Free up to 1M events/mo (https://posthog.com/pricing) |
| Anthropic Claude API | Content generation | ~$0.05/week (https://www.anthropic.com/pricing) |
| n8n (self-hosted) | Workflow automation | Free self-hosted (https://n8n.io/pricing) |

## Drills Referenced

- `posthog-gtm-events` — implement social content event tracking in PostHog
- `content-repurposing` — multiply each original post into 2-3 derivative pieces across formats
- `linkedin-lead-capture` — systematically convert engagement into CRM leads with source attribution
