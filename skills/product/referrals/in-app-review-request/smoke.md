---
name: in-app-review-request-smoke
description: >
  G2/Capterra Review Requests — Smoke Test. Identify your happiest users via
  engagement scoring, send a single in-app review prompt at one product moment,
  and validate that at least 3 complete a G2 or Capterra review within 7 days.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=3 reviews submitted on G2 or Capterra from 20 prompted users"
kpis: ["Review ask show-to-click rate", "Review completion rate (click-to-submit)", "Average review rating"]
slug: "in-app-review-request"
install: "npx gtm-skills add product/referrals/in-app-review-request"
drills:
  - engagement-score-computation
  - threshold-engine
---

# G2/Capterra Review Requests — Smoke Test

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

Prove that product usage data can identify happy users and that a single in-app prompt can convert them into public reviewers. At least 3 out of 20 prompted users submit a review on G2 or Capterra within 7 days. This validates two assumptions: your engagement scoring model surfaces users with advocacy potential, and an in-app ask at the right moment produces reviews without manual outreach.

## Leading Indicators

- Engagement scoring model produces a clear separation between top-quartile users and the median (power users are identifiable, not random)
- At least 12 of 20 prompted users see the in-app review ask (prompt is triggering correctly)
- At least 6 of those who see the ask click the review link (show-to-click rate >=50%)
- At least 1 review appears within the first 3 days (fast signal that the mechanic works)
- Reviews submitted are 4+ stars and substantive (>50 words) — confirming you targeted genuinely happy users

## Instructions

### 1. Compute engagement scores to find your happiest users

Run the `engagement-score-computation` drill to build a per-user engagement score from PostHog usage data. For this Smoke test, you do not need the full daily pipeline — run it once manually:

- Query PostHog for all users active in the last 30 days
- Compute the four dimensions: frequency (30%), breadth (25%), depth (25%), recency (20%)
- Calculate composite scores (0-100 scale)
- Identify the top 20 users scoring >=80 ("Power User" tier)
- Sync these 20 users to an Attio list: "Review Request Smoke Candidates"

Review the list manually. Verify these are genuinely happy, active users — not test accounts, not users who filed support complaints recently, not users on free trials. Remove any who do not pass manual validation and replace with the next highest-scored user.

**Human action required:** Review the 20-user candidate list in Attio and validate each user. This step cannot be automated at Smoke level because you need to build intuition about which user profiles convert to reviewers.

### 2. Choose one trigger moment and build the in-app prompt

Select the single best product moment to show the review ask. Good trigger moments for reviews:

- **Post-milestone:** User completes their 100th workflow, ships their 10th project, or reaches a round-number usage milestone. The user is already feeling accomplished.
- **Post-positive-support:** User received a positive support resolution (CSAT 4-5) in the last 48 hours. Goodwill is fresh.
- **Usage streak:** User has been active for 5+ consecutive days. Habit is formed, sentiment is high.

Pick ONE trigger. At Smoke level, do not test multiple triggers — isolate one to learn from.

Configure the review ask as an Intercom in-app message:

- **Audience:** The 20 users in your Attio candidate list (upload as Intercom segment or filter by user IDs)
- **Trigger:** The product moment you selected
- **Copy:** Keep it under 40 words. Example: "You have been using [product] for [milestone]. Would you share your experience with a quick G2 review? It takes about 3 minutes and helps teams like yours find tools that work."
- **CTA:** Single button: "Leave a review on G2" linking to your G2 review submission page
- **Display:** Show once per user. Dismiss on close. Do not re-show to users who dismiss.

For the 20-user Smoke test, target G2 only (single platform keeps measurement clean).

### 3. Track ask impressions and clicks

Log all interactions in PostHog:

- `review_ask_shown`: the prompt displayed to the user. Properties: `trigger_type`, `platform_target: g2`, `user_engagement_score`
- `review_ask_clicked`: the user clicked the review link. Properties: same as above plus `time_to_click_seconds`
- `review_ask_dismissed`: the user closed the prompt without clicking. Properties: same as above

After 7 days, pull the funnel: shown -> clicked -> review submitted. Note where users drop off.

### 4. Monitor G2 for submitted reviews

Check your G2 seller dashboard daily for 7 days, or use the G2 API if configured:

- Match new reviews to your 20 candidate users by name/company
- Log in Attio: `reviewed_platform: g2`, `review_rating`, `review_date`, `review_word_count`
- Read each review — does the content indicate genuine satisfaction or did the user feel coerced? (Quality matters as much as quantity for Smoke validation.)

### 5. Evaluate against threshold

Run the `threshold-engine` drill to measure against the pass criteria:

- **Pass threshold:** >=3 of the 20 prompted users submit a G2 review
- **If PASS:** The engagement model identifies reviewable users, and the in-app prompt converts them. Proceed to Baseline to add event tracking, multiple trigger types, and always-on automation.
- **If FAIL but >=6 clicked:** The targeting is right but the review submission process has friction. Investigate: is the G2 review form too long? Did users start but not finish? Simplify the ask or offer a shorter format.
- **If FAIL and <6 clicked:** The prompt is not compelling or the timing is wrong. Try a different trigger moment (switch from milestone to post-support, for example) and re-run.

Document: which trigger moment did you use? What was the click rate? What did the submitted reviews say? What would you change?

## Time Estimate

- 1.5 hours: run engagement scoring, identify top 20 users, manual validation
- 1 hour: configure Intercom in-app message with targeting and copy
- 0.5 hours: set up PostHog event tracking for the prompt
- 0.5 hours: daily review monitoring over 7 days (5 min/day)
- 1.5 hours: pull results, evaluate threshold, document findings

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Engagement scoring queries, prompt event tracking, funnel analysis | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app review request prompt display and targeting | Starter $29/seat/mo; or use existing plan ([intercom.com/pricing](https://intercom.com/pricing)) |
| Attio | Candidate list management, review outcome tracking | Free tier: 3 seats ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated play-specific cost at this level:** Free (within free tiers for a 20-user manual test; Intercom cost only if not already in your stack)

## Drills Referenced

- `engagement-score-computation` — builds composite engagement scores from PostHog usage data to identify the happiest users for review targeting
- `threshold-engine` — evaluates the >=3 reviews pass/fail threshold and recommends next action based on funnel diagnostics
