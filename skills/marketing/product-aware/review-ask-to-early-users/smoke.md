---
name: review-ask-to-early-users-smoke
description: >
  Review Ask to Early Users — Smoke Test. Manually request reviews from 5-10 early users on G2,
  Capterra, or Product Hunt and measure whether new reviews correlate with inbound leads.
stage: "Marketing > Product Aware"
motion: "Directories & Marketplaces"
channels: "Other"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: "≥ 3 new reviews published and ≥ 1 inbound lead attributed to a directory within 2 weeks"
kpis: ["Reviews published", "Inbound leads from directories", "Review ask response rate"]
slug: "review-ask-to-early-users"
install: "npx gtm-skills add marketing/product-aware/review-ask-to-early-users"
drills:
  - directory-listing-setup
  - directory-review-generation
  - threshold-engine
---

# Review Ask to Early Users — Smoke Test

> **Stage:** Marketing -> Product Aware | **Motion:** Directories & Marketplaces | **Channels:** Other

## Outcomes

Prove that asking early users to leave reviews on software directories produces published reviews AND that directory presence with fresh reviews correlates with at least one inbound lead. At Smoke, the founder personally asks 5-10 customers for reviews with agent assistance for preparation. Success = 3+ published reviews and 1+ inbound lead within 2 weeks.

## Leading Indicators

- Review ask emails opened (target: 60%+ open rate since these are warm customers)
- Review link clicks (target: 30%+ of opens click through to the directory)
- Partial review starts on the directory platform (some directories expose this)
- Directory profile views trending up after reviews publish

## Instructions

### 1. Identify target directories and ensure listings exist

Run the `directory-listing-setup` drill (Steps 1-3 only — identify directories and create/verify listings). For Smoke, focus on 2-3 directories maximum:

- **G2** — highest buyer intent, strongest SEO, most trusted by B2B buyers
- **Capterra** — strong PPC traffic, high-intent category searches
- **Product Hunt** — good for dev tools and early-stage products, drives awareness

Verify each listing has: complete profile, screenshots, pricing, UTM-tagged links (`?utm_source={directory}&utm_medium=directory&utm_campaign=listing`). If listings do not exist, create them. This takes 30-60 minutes per directory.

**Human action required:** Claim and verify your profile on each directory. Most require domain ownership verification or a company email address.

### 2. Build a review candidate list

Run the `directory-review-generation` drill (Step 1 only — identify review candidates). Query Attio for customers who meet ALL criteria:

- Active customer for 30+ days
- Has used the product in the last 14 days (check product usage data or PostHog)
- Has not been asked for a review before (`review_ask_count` is 0 or null)
- No open support tickets or recent complaints

Sort by engagement level. Pick your top 5-10 strongest advocates — people who have replied positively to emails, given good NPS scores, or expressed satisfaction directly.

### 3. Send personal review ask emails

Draft a personal email for each candidate. Do NOT use a mass email tool at Smoke level — send from the founder's email client directly.

**Email template (personalize each one):**

```
Subject: Would you share your experience on {directory}?

Hi {first_name},

You've been using {product} for {days} days now, and I've noticed {specific positive thing — e.g., "you've run 50+ workflows" or "your team onboarded 3 more users last month"}.

Would you be willing to spend 3 minutes leaving a review on {directory}? It helps other teams like yours discover us.

{directory_review_url}

No pressure at all — I appreciate you being a customer either way.

{founder_name}
```

**Human action required:** The founder sends each email personally. Personalize the `{specific positive thing}` for each recipient — generic asks convert at 10%, personalized asks convert at 30-40%.

Log each ask in Attio: set `review_ask_count` to 1, `last_review_asked_date` to today, `review_ask_directory` to the target directory name.

### 4. Follow up on non-responders after 3 days

For anyone who did not click the review link within 3 days, send one follow-up:

```
Subject: Re: Would you share your experience on {directory}?

Hi {first_name},

Just bumping this — even 2-3 sentences about what you like most would be hugely helpful. Here's the link again:

{directory_review_url}

Thanks either way.
```

Do not send more than one follow-up at Smoke level.

### 5. Monitor for published reviews

Check each directory daily for new reviews. Use the `directory-review-generation` drill (Step 4 — track review submissions):

- Match each new review to the Attio contact who submitted it
- Update Attio: set `reviewed_on` to the directory name and date, `review_rating` to their star rating
- Respond to every review within 48 hours (thank them, address specific feedback)

### 6. Track inbound leads from directories

Add UTM parameters to all directory listing links if not already done. Monitor PostHog or your website analytics for visitors arriving via `utm_source=g2`, `utm_source=capterra`, or `utm_source=producthunt`. Log any form submissions, demo requests, or signups from directory-sourced traffic in Attio.

### 7. Evaluate against threshold

Run the `threshold-engine` drill to measure against: **≥ 3 published reviews AND ≥ 1 inbound lead from a directory within 2 weeks**.

If PASS: Proceed to Baseline. Document which directories, which ask approach, and which customer segments produced the best results.

If FAIL: Diagnose. Common failure modes:
- Low response rate on asks -> candidates were not warm enough, or timing was wrong (ask after a positive moment, not randomly)
- Reviews started but not published -> the directory review form was too long or confusing (switch directories)
- Reviews published but no inbound -> listings need better copy, or the directories you chose do not have enough buyer traffic (switch to higher-traffic directories)

## Time Estimate

- Directory listing setup/verification: 1 hour
- Review candidate identification in Attio: 15 minutes
- Personal email drafting and sending (5-10 emails): 45 minutes
- Follow-up emails: 15 minutes
- Daily review monitoring (5 min x 10 days): 50 minutes
- Threshold evaluation: 15 minutes
- **Total: ~3.5 hours over 1-2 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| G2 | Review directory listing | Free basic profile (https://sell.g2.com/plans) |
| Capterra | Review directory listing | Free basic listing (https://www.capterra.com/vendors/) |
| Product Hunt | Review/upvote directory listing | Free to submit (https://www.producthunt.com/) |
| Attio | Track review candidates and asks | From $0/seat free tier (https://attio.com/pricing) |
| PostHog | Track directory-sourced traffic | Free up to 1M events/mo (https://posthog.com/pricing) |

**Estimated play-specific cost at Smoke: $0** (all free tiers)

## Drills Referenced

- `directory-listing-setup` — verify listings exist with UTM tracking on target directories
- `directory-review-generation` — identify candidates and track review submissions
- `threshold-engine` — evaluate pass/fail against 3 reviews + 1 inbound lead target
