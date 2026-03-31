---
name: guest-posting-scale-baseline
description: >
  Guest Posting at Scale — Baseline Run. First always-on guest posting operation: weekly blog
  discovery, 30-40 pitches via Instantly, AI-assisted article writing, and PostHog conversion
  tracking over 6 weeks.
stage: "Marketing > Solution Aware"
motion: "PR & Earned Mentions"
channels: "Content, Email"
level: "Baseline Run"
time: "25 hours over 6 weeks"
outcome: "≥6 published guest articles and ≥300 referral visits with measurable conversion rate"
kpis: ["Pitch acceptance rate (target ≥15%)", "Articles published", "Referral traffic from guest posts", "Backlinks acquired (dofollow)", "Conversion rate from guest post referrals"]
slug: "guest-posting-scale"
install: "npx gtm-skills add marketing/solution-aware/guest-posting-scale"
drills:
  - guest-post-blog-discovery
  - guest-post-pitch-outreach
  - guest-post-article-pipeline
  - posthog-gtm-events
  - threshold-engine
---

# Guest Posting at Scale — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** PR & Earned Mentions | **Channels:** Content, Email

## Outcomes

Establish a repeatable guest posting operation that runs continuously. Prove that guest posts can sustain referral traffic and drive measurable conversions over 6 weeks, not just a one-off burst.

## Leading Indicators

- Consistent pitch-to-reply rate ≥15% across 6 weeks (pitch quality holds at volume)
- At least 1 article published per week by weeks 3-6 (pipeline is flowing)
- Guest post referral visitors convert at ≥1% (traffic quality validated)
- New referring domains from guest posts increase your Ahrefs domain rating

## Instructions

### 1. Expand the blog target list

Run the `guest-post-blog-discovery` drill at Baseline scale (target: 50 blogs). Beyond the Smoke approach:

1. Run all five Ahrefs Content Explorer query variants across 10-15 niche keywords
2. Add competitor guest post cross-referencing: find where 2-3 competitors have published, extract those blog domains
3. Categorize blogs into three tiers: Tier 1 (DA 50+, strong ICP overlap), Tier 2 (DA 30-50, decent overlap), Tier 3 (DA 20-30, moderate overlap)
4. Enrich editor contacts via Clay waterfall (Clay > Hunter.io > Apollo > manual LinkedIn)
5. Push the full scored list to Attio

### 2. Configure tracking before outreach begins

Run the `posthog-gtm-events` drill to implement guest-post-specific event tracking:

- `guest_post_referral_visit`: fires when referrer matches a blog domain from your target list
- `guest_post_engagement`: fires on scroll >50% or time on page >30s from guest post referral
- `guest_post_conversion`: fires on signup, demo request, or other conversion from guest post referral
- Properties on all events: `source_blog`, `source_article_url`, `landing_page`, `utm_campaign`

Set up a PostHog funnel: `guest_post_referral_visit` → `guest_post_engagement` → `guest_post_conversion`

### 3. Execute 6-week pitch campaign

Run the `guest-post-pitch-outreach` drill at Baseline scale (30-40 pitches over 6 weeks):

**Weeks 1-2:** Pitch 15 blogs (8 Tier 1, 5 Tier 2, 2 Tier 3)
1. Generate 2 pitch angles per blog via Anthropic API
2. Populate merge fields from Clay enrichment data
3. **Human action required:** Review all Tier 1 pitches before sending (verify personalization quality)
4. Send via Instantly campaign: `guest-post-pitch-batch-1`
5. Schedule: Tue-Thu, 9am-11am editor timezone, 10/day limit
6. Set 1 automated follow-up at Day 7

**Weeks 3-4:** Pitch 15 more blogs. Process replies from batch 1.
**Weeks 5-6:** Pitch remaining 10 blogs. Process replies from batch 2. Focus on article writing and submission.

### 4. Write and submit articles for accepted pitches

For each accepted pitch, run the `guest-post-article-pipeline` drill:

1. Analyze the target blog's style from 3-5 recent articles
2. Generate draft via Anthropic API with 2-3 strategic backlinks
3. Run AI editorial review for quality check
4. **Human action required:** Author reviews, adds personal insights, approves for submission
5. Submit within 48-72 hours of acceptance (editors expect fast turnaround)
6. Handle editorial feedback and revisions promptly

Build a content template library as you go: save structural patterns that earn acceptances for reuse across future pitches.

### 5. Track and monitor results

Track these metrics weekly in PostHog and Attio:

- Pitches sent this week / cumulative
- Reply rate and acceptance rate (per tier)
- Articles published this week / cumulative
- Referral traffic from guest posts (per blog)
- Conversion rate from guest post referrals
- New backlinks acquired (via Ahrefs, check manually weekly)

Use Ahrefs to verify backlink status weekly: are published backlinks dofollow? Are they still live?

### 6. Evaluate against threshold

Run the `threshold-engine` drill at week 6 to measure:
- ≥6 articles published across target blogs
- ≥300 cumulative referral visits from guest posts
- Measurable conversion rate (≥1%) from guest post referral visitors

If PASS: Calculate ROI — time invested vs. referral traffic, backlinks, and conversions. Document which blog tiers, topics, and pitch angles performed best. Save pitch templates and article templates. Proceed to Scalable.

If FAIL: Analyze by tier — are Tier 1 blogs converting but Tier 2/3 are not? Is the issue pitch volume, acceptance rate, or post-publication traffic? Adjust targeting and re-run 4 more weeks.

## Time Estimate

- Blog discovery and enrichment (50 blogs): 4 hours
- Tracking setup: 1 hour
- Pitch writing and campaign management (40 pitches over 6 weeks): 8 hours
- Article writing and submission (6-8 articles): 9 hours
- Monitoring and reporting: 3 hours

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Ahrefs | Blog discovery, DA scoring, backlink monitoring | Standard $199/mo (https://ahrefs.com/pricing) |
| Clay | Editor enrichment and merge field population | Starter $149/mo (https://clay.com/pricing) |
| Instantly | Pitch email sending with sequences | Growth $30/mo (https://instantly.ai/pricing) |
| PostHog | Referral traffic and conversion tracking | Free up to 1M events (https://posthog.com/pricing) |
| Attio | Pitch pipeline and blog relationship CRM | Free for small teams (https://attio.com/pricing) |
| Anthropic API | Pitch angle + article draft generation | ~$0.05/article, ~$1/month total (https://anthropic.com/pricing) |

## Drills Referenced

- `guest-post-blog-discovery` — find, score, and enrich 50 target blogs
- `guest-post-pitch-outreach` — send 30-40 personalized pitches via Instantly over 6 weeks
- `guest-post-article-pipeline` — write, review, and submit articles for each accepted pitch
- `posthog-gtm-events` — implement guest-post-specific event tracking and conversion funnels
- `threshold-engine` — evaluate published articles and referral traffic against pass criteria
