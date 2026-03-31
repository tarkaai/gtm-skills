---
name: partner-marketplace-review-generation
description: Systematically generate and manage reviews on partner marketplace listings to improve ranking and conversion
category: Partner Marketplaces
tools:
  - Attio
  - Loops
  - n8n
  - PostHog
fundamentals:
  - partner-marketplace-review-api
  - attio-contacts
  - attio-lists
  - loops-sequences
  - loops-audience
  - n8n-workflow-basics
  - n8n-scheduling
  - posthog-custom-events
---

# Partner Marketplace Review Generation

This drill builds a systematic review generation and management workflow for partner marketplace listings. Reviews are the single highest-leverage factor in marketplace search ranking and listing conversion rate. A listing with 10+ positive reviews converts 2-4x higher than one with 0.

## Input

- Active partner marketplace listings (output from `partner-marketplace-listing-setup` drill)
- Customer data in Attio with: integration usage status, tenure, NPS/satisfaction signal
- Loops account for email sequences (or Instantly for cold-style outreach)
- At least 10 customers actively using the specific integration

## Steps

### 1. Build the review candidate list

Query Attio using `attio-contacts` and `attio-lists` to find ideal review candidates:

**Filter criteria (all must be true):**
- Customer for 30+ days
- Actively using the specific partner integration (e.g., "HubSpot integration: active")
- Has not been asked for a marketplace review in the last 90 days
- Has not churned or filed an open support ticket
- Ideally: has given positive NPS (7+) or positive feedback in support interactions

Create an Attio list: "Review Candidates - {marketplace_name} - {date}"

**Scoring (optional):**
Rank candidates by review impact potential:
- Decision-maker title (VP+) = +3 points (their review carries more weight)
- Recognizable company logo = +2 points (social proof for other buyers)
- Active integration user (daily/weekly) = +2 points (credible reviewer)
- Positive NPS or CSAT = +1 point

### 2. Build the review request sequence

Using `loops-sequences` and `loops-audience`, create a 2-touch review request sequence:

**Email 1 (Day 0) -- Personal ask:**
```
Subject: Quick favor? ({marketplace_name} review)
From: {founder_name} or {cs_manager_name}

Hey {first_name},

I noticed your team has been using our {marketplace_name} integration for {tenure_days} days.

Would you mind leaving a quick review on {marketplace_name}? It takes about 2 minutes and helps other {marketplace_name} users find us.

Direct link: {review_url}

Honest feedback only -- if something isn't working, I'd rather hear about it directly so we can fix it.

Thanks,
{sender_name}
```

**Email 2 (Day 5, only if no review detected) -- Gentle reminder:**
```
Subject: Re: Quick favor? ({marketplace_name} review)

Hey {first_name},

Just a quick follow-up on the review request below. No worries if you're busy -- but if you have 2 minutes, it would genuinely help:

{review_url}

Thanks either way.
{sender_name}
```

Tag contacts in Loops: `review_requested_{marketplace}`, `review_requested_date`.

### 3. Track review submissions

Using `partner-marketplace-review-api`, set up monitoring:

1. Query the review API daily for new reviews
2. Match new reviews to the review request list by author name/company
3. Track: requests sent, reviews posted, conversion rate (requests -> reviews)
4. Log results in Attio: mark contacts who left reviews with `review_posted_{marketplace}: true`

Using `posthog-custom-events`, track the review request funnel:

| Event | Trigger | Properties |
|-------|---------|-----------|
| `review_request_sent` | Email sent via Loops | `marketplace`, `customer_id`, `sequence_step` |
| `review_link_clicked` | UTM-tagged click on review URL | `marketplace`, `customer_id` |
| `review_posted` | New review detected via API | `marketplace`, `customer_id`, `rating`, `word_count` |

### 4. Respond to all reviews

Using `partner-marketplace-review-api`, respond to every review within 48 hours:

**For 4-5 star reviews:**
- Thank the reviewer by name
- Reference something specific from their review
- Keep it brief (2-3 sentences)

**For 1-3 star reviews:**
- Acknowledge the issue
- Provide a specific action you're taking or have taken
- Offer a direct support channel
- Respond within 24 hours (urgency signals you care)

**Never:**
- Use template responses (marketplace readers can tell)
- Argue with negative reviews
- Ask the reviewer to update their rating (violates most marketplace TOS)

### 5. Set up the ongoing review cadence

Using `n8n-scheduling` and `n8n-workflow-basics`, automate the weekly review request pipeline:

**n8n workflow (runs weekly, Tuesday 9am):**
1. Query Attio for new review candidates (passed the filter criteria in step 1)
2. Select top 5 candidates by score
3. Enroll them in the Loops review request sequence
4. Log the enrollment in Attio
5. Post a summary to Slack: "{X} review requests sent for {marketplace} this week. Current review count: {Y}, avg rating: {Z}"

**Cadence rules:**
- Maximum 5 review requests per marketplace per week (avoid triggering spam filters)
- Rotate across marketplaces: week 1 = AppExchange, week 2 = HubSpot, etc.
- Never ask the same customer for reviews on multiple marketplaces in the same month
- Stop requesting when a listing reaches 50+ reviews (diminishing returns on ranking impact)

## Output

- Systematic review generation producing 2-4 new reviews per marketplace per month
- All reviews responded to within 48 hours
- Review request funnel tracked in PostHog
- Weekly automated review cadence via n8n

## Triggers

- Set up at Baseline level once listings are live and have 10+ active integration users
- Weekly cadence runs continuously at Baseline and Scalable levels
- Review response monitoring runs daily
