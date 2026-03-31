---
name: directory-review-generation
description: Systematically collect customer reviews on software directories using automated ask workflows and incentive tracking
category: Directories
tools:
  - Loops
  - Attio
  - n8n
  - G2
  - Capterra
fundamentals:
  - directory-review-monitoring
  - loops-sequences
  - attio-contacts
  - attio-automation
  - n8n-workflow-basics
  - n8n-triggers
---

# Directory Review Generation

This drill builds a systematic process for collecting customer reviews on software directories. Reviews are the single most important ranking factor on G2 and Capterra -- more reviews with higher ratings directly drive more listing views and higher category placement.

## Input

- Active directory listings (output from `directory-listing-setup` drill)
- Customer list in Attio with at least 10 active, satisfied customers
- Loops configured for transactional or lifecycle email

## Steps

### 1. Identify review candidates

Query Attio using the `attio-contacts` fundamental to build a review candidate list. Ideal candidates:

- **Active customers** for 30+ days (enough experience to write a substantive review)
- **High engagement** (regular product usage, responsive to emails)
- **Positive sentiment** (NPS promoters, positive support interactions, expansion revenue)
- **Has not reviewed yet** (check `reviewed_on` field in Attio -- if empty, they are a candidate)

Sort candidates by likelihood to leave a positive review. Start with your strongest advocates.

### 2. Build the review ask sequence

Using the `loops-sequences` fundamental, create a 3-email review request sequence:

**Email 1 (Day 0) -- The Ask:**
```
Subject: Quick favor? Share your experience on {directory}

Body:
Hi {first_name},

You've been using {product} for {days_active} days now. Would you be willing to share your experience with a quick review on {directory}?

It takes about 3 minutes and helps other teams like yours find tools that actually work.

[Leave a review on {directory}] -> {directory_review_url}

Thanks,
{sender_name}
```

**Email 2 (Day 3, if no click) -- The Nudge:**
```
Subject: Re: Quick favor?

Body:
Hi {first_name},

Just bumping this -- a short review on {directory} would mean a lot to us. Even 2-3 sentences about what you like most helps.

[Write a quick review] -> {directory_review_url}
```

**Email 3 (Day 7, if no click) -- The Last Ask:**
```
Subject: Last ask on this

Body:
Hi {first_name},

No worries if reviews aren't your thing. If you do have 3 minutes, here's the link one more time:

[Leave a review] -> {directory_review_url}

Either way, thanks for being a customer.
```

### 3. Set up review ask triggers

Using the `n8n-triggers` fundamental, build automated triggers for when to send review asks:

- **Post-milestone trigger:** Customer hits a usage milestone (e.g., 100 workflows run, 50 contacts enriched). Use PostHog event -> n8n webhook -> Loops sequence start.
- **Post-support trigger:** Customer gives a positive CSAT score after a support interaction. Wait 24 hours, then trigger review ask.
- **Post-expansion trigger:** Customer upgrades plan or adds seats. Trigger review ask 7 days after upgrade.
- **Quarterly cadence:** For customers who have not reviewed anywhere, send a review ask once per quarter (max).

### 4. Track review submissions

Using the `directory-review-monitoring` fundamental, monitor each directory for new reviews. When a new review appears:

1. Match the reviewer to the Attio contact (by name, email if available, or company)
2. Update Attio: set `reviewed_on` field to the directory name and date
3. Set `review_rating` field
4. Remove them from the review ask sequence to avoid repeat asks
5. If the review is 4+ stars, flag as a case study candidate

Using `n8n-workflow-basics`, build this as an automated workflow:
- Trigger: G2/Capterra webhook for new review
- Match: Search Attio by reviewer name + company
- Update: Set review fields
- Notify: Post to Slack with review text and rating

### 5. Manage review incentives (optional)

If using incentives (gift cards, account credits), track them in Attio:

- `review_incentive_offered`: boolean
- `review_incentive_type`: "gift_card" / "account_credit" / "swag"
- `review_incentive_value`: dollar amount
- `review_incentive_redeemed`: boolean

**Important:** G2 and Capterra allow incentives but require disclosure. The reviewer must indicate they received an incentive. Never incentivize specific ratings -- only the act of leaving an honest review.

### 6. Respond to every review

Using the `directory-review-monitoring` fundamental, respond to every review within 48 hours:

- **5 stars:** Thank specifically, mention what you plan to build next
- **4 stars:** Thank, address the specific improvement suggestion
- **3 stars:** Acknowledge the feedback, explain what you are doing about it, offer direct support
- **1-2 stars:** Apologize, offer to connect directly to resolve, do not argue

## Output

- Automated review ask sequences running in Loops
- Trigger-based review asks firing after key customer events
- New reviews tracked in Attio with attribution
- Response workflow ensuring every review gets a vendor reply within 48 hours

## Triggers

- Review ask sequences run automatically based on customer events
- Review monitoring runs continuously (daily webhook checks or weekly API poll)
- Quarterly manual audit: review velocity, average rating trend, directory coverage gaps
