---
name: nps-feedback-loop
description: Run NPS surveys, analyze responses, and close the feedback loop with customers
category: Product
tools:
  - Intercom
  - PostHog
  - Loops
  - Attio
fundamentals:
  - intercom-surveys
  - posthog-cohort-analysis
  - loops-transactional-emails
  - attio-list-management
---

# NPS Feedback Loop

This drill implements a Net Promoter Score survey system that goes beyond collecting scores to actually acting on feedback. The goal is not just measurement — it is turning detractors into passives, passives into promoters, and promoters into advocates.

## Prerequisites

- Intercom configured with survey capability
- PostHog tracking user segments and usage patterns
- Loops configured for automated email responses
- At least 50 active users (below this, NPS is statistically unreliable)

## Steps

### 1. Design the survey trigger

Do not survey everyone at once. Using the `intercom-surveys` fundamental, trigger the NPS survey based on product milestones: after 30 days of active use, after completing a major workflow, or quarterly for long-term customers. Never survey during onboarding (too early) or right after a support ticket (biased). Show the survey in-app for highest response rates.

### 2. Configure the two-question format

Question 1: "How likely are you to recommend [product] to a colleague?" (0-10 scale). Question 2: "What's the main reason for your score?" (open text). Keep it to these two questions only. Every additional question reduces completion rate. Make the open text field required — the score is useless without context.

### 3. Segment and analyze responses

Using the `posthog-cohort-analysis` fundamental, cross-reference NPS scores with usage data. Group respondents:

- **Promoters (9-10)**: Who are they? What features do they use most? What plan are they on?
- **Passives (7-8)**: What is holding them back from being promoters? What are they not using?
- **Detractors (0-6)**: What specific problems are they citing? Is there a pattern by cohort, plan, or feature?

Look for trends: are detractors concentrated in a specific segment, plan, or signup cohort?

### 4. Close the loop with each segment

Using `loops-transactional-emails`, send tailored follow-ups within 48 hours:

- **Promoters**: Thank them. Ask if they would be willing to leave a review, do a case study, or refer a colleague. Feed their names into the `referral-program` drill.
- **Passives**: Acknowledge their feedback. Share a specific resource or feature that addresses their stated concern. Offer a call to understand what would make them a promoter.
- **Detractors**: Respond personally (not automated). Apologize for the experience. Ask for a 15-minute call to understand the issue. Log their feedback in Attio using `attio-list-management` and assign follow-up to the account owner.

### 5. Route actionable feedback to product

Aggregate open-text responses and categorize by theme: missing feature, usability issue, performance problem, pricing concern, support quality. Share a monthly NPS report with the product team. The most common detractor themes should directly influence the product roadmap.

### 6. Track NPS over time

Monitor NPS monthly as a trailing metric. Track it by cohort, plan, and segment. A rising NPS means your product and customer experience are improving. A declining NPS in a specific segment is an early warning. Set a threshold: if NPS drops below 30, trigger a deeper investigation.
