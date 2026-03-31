---
name: case-study-content-program-smoke
description: >
  Case Study Content Program — Smoke Test. Manually create 3 customer case studies
  with real metrics and quotes, publish them on dedicated pages, and measure whether
  they generate page views and conversions. Validates that customer success stories
  attract product-aware visitors and drive next-step actions.
stage: "Marketing > ProductAware"
motion: "FounderSocialContent"
channels: "Content, Website"
level: "Smoke Test"
time: "10 hours over 4 weeks"
outcome: "≥ 300 total page views and ≥ 5 conversions from 3 published case studies in 4 weeks"
kpis: ["Total page views across 3 case studies (target ≥ 300)", "Conversions from case study pages (target ≥ 5)", "Average time on page (target ≥ 2.5 min)", "CTA click-through rate (target ≥ 5%)"]
slug: "case-study-content-program"
install: "npx gtm-skills add marketing/product-aware/case-study-content-program"
drills:
  - case-study-creation
  - threshold-engine
---

# Case Study Content Program — Smoke Test

> **Stage:** Marketing > ProductAware | **Motion:** LeadCaptureSurface | **Channels:** Content, Website

## Outcomes

Prove that customer success stories with real metrics attract product-aware visitors and convert them into leads. Product-aware visitors already know your product but need social proof to take the next step. This test creates 3 case studies manually and measures whether they generate meaningful traffic and conversions.

Pass: ≥ 300 total page views and ≥ 5 conversions (demo requests, signups, or contact form submissions) from the 3 case study pages within 4 weeks.
Fail: < 300 page views or < 5 conversions after 4 weeks, or unable to recruit 3 customers willing to participate.

## Leading Indicators

- At least 1 customer agrees to participate within the first week (your customer relationships support case study recruitment)
- First published case study receives ≥ 50 page views within 7 days of publication (the distribution channels work)
- Average time on page exceeds 2.5 minutes (visitors are reading the full story, not bouncing)
- At least 1 conversion comes from a visitor who found the case study organically (not someone you directly sent the link to)
- The customer tagged in a LinkedIn promotion engages with or reshares the post (co-marketing amplification works)

## Instructions

### 1. Identify and recruit 3 case study candidates

**Human action required:** Identify 3 happy customers with strong, quantifiable results. Look for customers who meet at least 3 of these criteria:

- They have been using the product for 60+ days
- They can cite specific metrics (revenue increase, time saved, efficiency gain)
- Their company name or job title would be recognizable to your target audience
- They have expressed satisfaction via NPS, support interactions, or direct feedback
- Their industry or use case matches your most common prospect profile

Reach out personally (not a mass email) with a specific, low-effort ask: "We would like to feature your team's success with [product]. It is a 30-minute conversation -- we handle the writing, you review the draft before we publish. We will link to your site and promote your team as industry leaders."

Offer a small incentive if needed: gift card, co-marketing post, early access to a new feature, or a feature on your homepage.

### 2. Create the 3 case studies

Run the `case-study-creation` drill for each customer. The drill covers:

1. **Interview preparation**: Write 8-10 open-ended questions following the Situation-Solution-Results arc. Share questions with the customer 2-3 days before the interview so they can gather data.

2. **Interview execution**: Schedule a 30-minute video call. Record and transcribe using the `fireflies-transcription` fundamental. Let the customer talk -- the best quotes come from unscripted moments when they describe specific outcomes.

3. **Writing the case study**: Structure each story as Challenge (150-200 words in the customer's language), Solution (200-250 words on how they implemented your product), Results (150-200 words leading with the biggest metric and a direct quote). Add a summary box: company name, industry, company size, key metric, and pull quote.

4. **Customer approval**: Send the draft to the customer for review. Address any confidentiality concerns. Secure written permission to publish their name, company logo, and quotes. Allow 5-7 business days for review.

5. **Publication**: Publish using the `ghost-blog-publishing` fundamental on dedicated pages optimized for SEO with keywords like "[your category] case study" and "[industry] success story". Include clear CTAs (demo request button, signup link, or contact form) on each page.

6. **Derivative assets**: From each case study, produce 3-4 social media posts with the strongest quote and metric, an email snippet for sales to include in outreach, and a one-line testimonial for your homepage.

### 3. Set up PostHog tracking

Using the `posthog-custom-events` fundamental (referenced in the `case-study-creation` drill), instrument each case study page:

- `case_study_page_viewed` with properties: `case_study_id`, `company_name`, `industry`, `traffic_source`
- `case_study_cta_clicked` with properties: `case_study_id`, `cta_type` (demo, signup, contact)
- `case_study_converted` with properties: `case_study_id`, `conversion_type`
- `case_study_scroll_depth` with properties: `case_study_id`, `depth_percent` (25, 50, 75, 100)

This gives you visibility into which case studies drive engagement and at what point visitors decide to take action.

### 4. Distribute the case studies

**Human action required:** Promote each case study through available channels:

- **LinkedIn**: Post about each case study and tag the customer's company. Lead with their result, not your product. Example: "[Customer] achieved [metric] by [approach]. Here is how they did it: [link]"
- **Sales outreach**: Add the case study link and a 2-sentence summary to active email sequences for prospects in the same industry
- **Website**: Feature the 3 case studies on your homepage or product page with pull quotes and company logos
- **Email**: Send a "new customer story" email to your existing subscriber list via Loops

### 5. Evaluate after 4 weeks

Run the `threshold-engine` drill to measure against the pass threshold.

Aggregate across all 3 case study pages:
- Total unique page views (from PostHog)
- Total conversions (demo requests, signups, contact form submissions)
- Conversion rate per case study (conversions / views)
- Average time on page
- Top traffic source per case study

- **PASS (≥ 300 views and ≥ 5 conversions):** Document your interview template, writing process, and which distribution channels drove the most traffic. Note which case study converted best and why (industry match, stronger metrics, better story). Proceed to Baseline.
- **MARGINAL (150-299 views or 2-4 conversions):** Diagnose: Did you distribute enough? Check traffic sources -- if most views came from one channel, try others. Check time on page -- if it is under 1 minute, the story is not compelling enough. Rewrite the weakest case study or replace the customer with one who has stronger results.
- **FAIL (< 150 views or 0-1 conversions):** Check: Are the case study pages indexed and accessible? Did you actually distribute them (check referral sources in PostHog)? Are the CTAs visible and specific? If the stories are solid but traffic is the problem, the issue is distribution, not content.

## Time Estimate

- Customer recruitment outreach: 1.5 hours
- 3 interviews (30 min each + prep): 3 hours
- Writing 3 case studies: 3 hours (using AI to generate first drafts from transcripts, then editing)
- Customer review coordination: 30 minutes
- Publication and SEO setup: 1 hour
- Distribution (LinkedIn posts, sales email updates, website placement): 1 hour
- Total: ~10 hours of active work spread over 4 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Fireflies.ai | Interview recording and transcription | Free: 800 min/mo; Pro ~$10/user/mo annual ([fireflies.ai/pricing](https://fireflies.ai/pricing)) |
| Ghost | Case study page publishing and CMS | Free self-hosted; Pro $9/mo ([ghost.org/pricing](https://ghost.org/pricing)) |
| PostHog | Page view tracking, scroll depth, CTA clicks | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | Log case study candidates and track outreach | Free up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated monthly cost for Smoke:** $0 (all tools on free tiers)

## Drills Referenced

- `case-study-creation` — end-to-end process for identifying candidates, conducting interviews, writing the case study, creating derivative assets, and distributing strategically to influence active deals
- `threshold-engine` — evaluate page views and conversions against the pass threshold and recommend next action (advance, iterate, or pivot)
