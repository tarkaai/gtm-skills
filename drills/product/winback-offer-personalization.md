---
name: winback-offer-personalization
description: Design segment-specific winback offers and messaging based on churn reason, recency, account value, and prior usage patterns
category: Product
tools:
  - Loops
  - Intercom
  - PostHog
  - Attio
  - Anthropic
fundamentals:
  - loops-sequences
  - loops-broadcasts
  - loops-ab-testing
  - intercom-in-app-messages
  - posthog-cohorts
  - attio-lists
  - attio-contacts
  - hypothesis-generation
---

# Winback Offer Personalization

This drill creates segment-specific winback offers and messaging for churned users. Instead of sending every churned user the same "we miss you" email, it analyzes why each user left, what they valued, and how long they have been gone — then designs the exact offer and copy most likely to bring them back.

## Input

- Attio with churned customer records including churn reason, churn date, previous plan, and lifetime value
- PostHog with pre-churn usage data (features used, engagement frequency, last actions before churn)
- At least 30 churned users to segment meaningfully
- Anthropic API key for Claude (offer generation)

## Steps

### 1. Segment churned users by churn reason

Using `attio-lists`, pull all churned customers. Using `posthog-cohorts`, enrich each record with their pre-churn behavior. Classify each churned user into exactly one primary segment:

- **Price churners:** Cancelled citing cost. Visited pricing page multiple times before churning. May have downgraded before cancelling. Signal: billing-related events in last 30 days before churn.
- **Missing feature churners:** Cancelled because the product lacked something they needed. Signal: feature request tickets, support conversations mentioning specific capabilities, or usage patterns showing they tried workarounds.
- **Competitor churners:** Switched to a competitor. Signal: mentioned competitor in cancellation survey, or stopped using the product abruptly (not gradual decline).
- **Poor experience churners:** Cancelled due to bugs, poor support, or frustration. Signal: high support ticket volume in last 30 days, error events in PostHog, or negative NPS score.
- **Inactive churners:** Never fully activated or gradually stopped using the product. Signal: low feature breadth, declining sessions for 8+ weeks, or never completed onboarding.
- **Business change churners:** Company closed, role changed, or project ended. Signal: account admin changes, domain MX record changes, or stated reason in exit survey.

### 2. Sub-segment by recency and value

Within each churn reason segment, further classify by:

- **Recency:** Fresh (0-30 days since churn), Mid (31-90 days), Stale (91-180 days), Cold (180+ days). Fresh churners remember the product and respond to specific improvements. Cold churners need re-education.
- **Account value:** High value (top 25% by previous MRR), Standard (middle 50%), Low value (bottom 25%). High-value accounts get personal outreach. Low-value accounts get automated sequences only.

Store segment assignments as Attio custom attributes and PostHog person properties.

### 3. Design offers per segment

Using `hypothesis-generation`, generate the optimal offer for each churn reason segment. Feed Claude the segment definition, churn reasons, and product updates since they left. The agent produces:

**Price churners:**
- Fresh + High value: Personal call offering a custom discount (15-25% for 3 months) or a new plan tier that fits their budget. Include ROI data from similar customers.
- Fresh + Standard: Email with a limited-time discount (20% for 2 months). Lead with "We've added a plan that might be a better fit."
- Mid/Stale: Email highlighting new pricing tiers or a free month to re-evaluate.
- Cold: Low priority. Add to re-education sequence only if new pricing exists.

**Missing feature churners:**
- Only contact when the requested feature has shipped or a close equivalent exists. Use Attio to match feature requests to shipped features.
- Fresh: "You asked for X — we built it. Here's a 14-day free pass to try it."
- Mid/Stale: Same message but add a walkthrough video or guide since they may have forgotten the product.

**Competitor churners:**
- Fresh: Share a specific comparison or differentiator that has improved since they left. No discount — lead with value.
- Mid: Share a customer story from someone who switched back. Include concrete results.
- Stale/Cold: Only reach out if you have shipped something the competitor does not have.

**Poor experience churners:**
- Acknowledge the issue directly. Never pretend it did not happen.
- Fresh: "We fixed [specific issue]. Here's what changed: [details]. Want a personal walkthrough?"
- Mid/Stale: Same but include a timeline of improvements made since they left.

**Inactive churners:**
- Re-educate on value. They never saw it the first time.
- Fresh: "Most teams like yours get the most value from [specific feature]. Here's a 5-minute guide."
- Mid/Stale: Share a case study from a similar company. Include a new onboarding flow offer.

**Business change churners:**
- Do not winback. Mark as "do not contact" unless they re-appear at a new company.

### 4. Build email sequences per segment

Using `loops-sequences`, create a 3-email winback sequence for each active segment (exclude business change):

- **Email 1 (trigger: segment assignment):** Acknowledge their departure without being desperate. Share the single most relevant improvement for their segment. No hard sell. Single CTA: learn more or try it.
- **Email 2 (7 days after email 1, if no engagement):** Social proof from a similar customer. Specific results, not generic testimonials. For price churners, include ROI data. For feature churners, include a usage example.
- **Email 3 (14 days after email 1, if no engagement):** Direct offer with a clear expiration. Discount, extended trial, or personal demo depending on segment. 14-day expiration on the offer.

### 5. Build in-app welcome-back flows

Using `intercom-in-app-messages`, create welcome-back messages for churned users who return to the site or log into an expired account:

- Detect returning churned users via PostHog cohort membership
- Show a personalized banner: "Welcome back. Here's what's new since [churn date]: [2-3 bullet points relevant to their segment]."
- One-click reactivation CTA. Pre-fill their previous plan. Offer to restore their data and settings.
- For users eligible for a discount, apply it automatically on reactivation.

### 6. Route high-value winbacks to personal outreach

For any churned user in the High Value sub-segment, automated email is supplementary, not primary. Create an Attio task for the account owner with:
- Churn reason and date
- Pre-churn usage summary (features used, engagement level)
- What has changed since they left (product improvements relevant to their churn reason)
- Recommended offer and talking points
- Link to their PostHog user profile

## Output

- Segment-specific offer definitions stored in Attio
- Loops sequences configured per segment with appropriate copy and offers
- Intercom welcome-back messages for returning churned users
- High-value winback tasks routed to account owners
- Segment assignment rules stored in PostHog as cohort definitions

## Triggers

- Run once at setup to segment and design initial offers
- Re-run monthly to update segments with newly churned users and refresh offers based on shipped features
