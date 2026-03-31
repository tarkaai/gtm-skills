---
name: review-ask-to-early-users-baseline
description: >
  Review Ask to Early Users — Baseline Run. Automate review request sequences via Loops,
  configure PostHog tracking for directory attribution, and run always-on review collection.
stage: "Marketing > Product Aware"
motion: "Directories & Marketplaces"
channels: "Other"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 6 new reviews and ≥ 3 inbound leads from directories over 2 weeks"
kpis: ["Reviews published per week", "Inbound leads from directories", "Ask-to-review conversion rate", "Average review rating"]
slug: "review-ask-to-early-users"
install: "npx gtm-skills add marketing/product-aware/review-ask-to-early-users"
drills:
  - posthog-gtm-events
  - directory-review-generation
  - directory-performance-monitor
---

# Review Ask to Early Users — Baseline Run

> **Stage:** Marketing -> Product Aware | **Motion:** Directories & Marketplaces | **Channels:** Other

## Outcomes

Prove that automated review request sequences produce a steady stream of reviews and that directory-sourced inbound holds over a 2-week always-on period. Baseline transitions from founder-sent emails to Loops sequences with proper PostHog tracking. Success = 6+ published reviews and 3+ inbound leads in 2 weeks with the system running continuously.

## Leading Indicators

- Review ask sequence enrollment rate (target: all eligible customers enrolled automatically)
- Email open rate on review asks (target: 50%+)
- Review link click-through rate (target: 20%+)
- Time from ask to published review (target: median < 5 days)
- Directory profile views week-over-week (target: increasing)

## Instructions

### 1. Configure PostHog tracking for the review funnel

Run the `posthog-gtm-events` drill to set up the directory review event taxonomy:

- `review_ask_sent` — properties: `directory_name`, `ask_channel` (email), `customer_tenure_days`, `customer_plan`
- `review_ask_opened` — properties: same as above
- `review_ask_clicked` — properties: same plus `time_to_click_hours`
- `review_submitted` — properties: `directory_name`, `rating`, `reviewer_tenure_days`, `ask_channel`
- `directory_listing_view` — properties: `directory_name`, `listing_type` (organic)
- `directory_inquiry_submitted` — properties: `directory_name`, `inquiry_type` (signup/demo/pricing)

Verify UTM parsing is working: visit your site from each directory listing link and confirm events fire in PostHog.

### 2. Build automated review ask sequences in Loops

Run the `directory-review-generation` drill (Steps 1-3 — identify candidates, build sequences, set up triggers):

**Sequence A — G2 Review Ask (3 emails over 7 days):**

Email 1 (Day 0): Personal ask referencing their specific usage. Include direct G2 review link. Send from founder name.

Email 2 (Day 3, if no click): Shorter nudge. "Even 2-3 sentences helps other teams find us."

Email 3 (Day 7, if no click): Final ask. "No worries if reviews aren't your thing."

**Sequence B — Capterra Review Ask (same structure, different review link).**

**Sequence C — Product Hunt Review Ask (same structure, different review link).**

Using the `directory-review-generation` drill triggers, enroll customers automatically when they hit milestones:

- **30-day active trigger:** Customer reaches 30 days of product usage. Enroll in Sequence A (G2).
- **Post-positive-support trigger:** Customer gives CSAT 4+ after support interaction. Wait 24 hours, enroll in Sequence B (Capterra). Only if not already in a review sequence.
- **Post-upgrade trigger:** Customer upgrades plan or adds seats. Wait 7 days, enroll in Sequence C (Product Hunt).

**Rules:** A customer receives at most ONE review ask sequence per quarter. Once they submit a review on any directory, remove them from all review sequences immediately.

### 3. Set up review monitoring and response workflow

Run the `directory-review-generation` drill (Steps 4-6 — track submissions, manage incentives, respond):

Build an n8n workflow that runs daily:
1. Fetch new reviews from G2, Capterra, and Product Hunt using directory APIs
2. Match each reviewer to an Attio contact (by name + company)
3. Update Attio: `reviewed_on`, `review_rating`, `review_date`
4. Remove the contact from any active review ask sequences in Loops
5. If rating >= 4 stars, flag as case study candidate in Attio
6. If rating <= 2 stars, alert team in Slack for immediate response
7. Draft a response for each review (agent drafts, human approves and posts)

**Human action required:** Review and post vendor responses to each new review within 48 hours. The agent drafts responses following sentiment guidelines (see `directory-review-generation` Step 6), but a human must approve before posting.

### 4. Set up weekly directory performance monitoring

Run the `directory-performance-monitor` drill to track:

- Profile views per directory per week
- Clicks to website per directory per week
- Conversion: directory visitor to inquiry (signup/demo)
- Review count and average rating trend
- Category rank position on G2 and Capterra

Build a PostHog dashboard with these metrics. Set alerts for:
- Traffic drop >30% week-over-week on any directory
- Rating drop below 4.0
- Any 1-2 star review (immediate response needed)

### 5. Evaluate against threshold

After 2 weeks of always-on operation, measure against: **≥ 6 published reviews AND ≥ 3 inbound leads from directories**.

Calculate:
- Ask-to-review conversion rate (target: 15-30% of asks result in a published review)
- Review velocity: reviews per week
- Inbound attribution: leads from `utm_source` matching directory names
- Cost per review: $0 at Baseline (no paid campaigns yet)

If PASS: Proceed to Scalable. Document: best-performing directory, best ask channel (milestone vs support vs upgrade), optimal customer tenure for asking.

If FAIL: Diagnose:
- Low ask-to-review conversion -> ask copy is weak or timing is wrong. A/B test email subject lines and ask timing.
- Reviews coming in but no inbound -> listings need optimization. Rewrite listing copy, add more screenshots, improve category selection.
- Good metrics on one directory but not others -> consolidate effort to the working directory before scaling.

## Time Estimate

- PostHog event setup: 2 hours
- Loops sequence building (3 sequences): 3 hours
- n8n review monitoring workflow: 2 hours
- Directory performance dashboard: 1.5 hours
- Review response drafting (ongoing, ~15 min/day x 14 days): 3.5 hours
- **Total: ~12 hours over 2 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| G2 | Review directory | Free basic profile (https://sell.g2.com/plans) |
| Capterra | Review directory | Free basic listing (https://www.capterra.com/vendors/) |
| Product Hunt | Review directory | Free (https://www.producthunt.com/) |
| Loops | Automated review ask sequences | Free under 1,000 contacts; $49/mo from 1,000 contacts (https://loops.so/pricing) |
| PostHog | Event tracking and dashboards | Free up to 1M events/mo (https://posthog.com/pricing) |
| n8n | Review monitoring workflow | Free self-hosted; $20/mo cloud starter (https://n8n.io/pricing) |
| Attio | CRM tracking of review candidates | Free tier available (https://attio.com/pricing) |

**Estimated play-specific cost at Baseline: $0-69/mo** (Loops free tier or $49/mo + n8n $20/mo if on cloud)

## Drills Referenced

- `posthog-gtm-events` — define and implement the review funnel event taxonomy in PostHog
- `directory-review-generation` — build automated review ask sequences and review tracking
- `directory-performance-monitor` — track directory KPIs and set up weekly monitoring
