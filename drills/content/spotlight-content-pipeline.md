---
name: spotlight-content-pipeline
description: Identify underused features, produce spotlight content for each, and deliver via email and in-app on a recurring cadence
category: Content
tools:
  - PostHog
  - Intercom
  - Loops
  - Attio
  - n8n
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - posthog-funnels
  - intercom-in-app-messages
  - loops-broadcasts
  - loops-sequences
  - attio-lists
  - n8n-scheduling
  - n8n-workflow-basics
---

# Spotlight Content Pipeline

This drill builds the repeatable system for selecting which features to spotlight, producing the spotlight content, and delivering it to the right users through email and in-app channels. It runs on a weekly cadence. Each spotlight targets users who would benefit from the feature but have not yet discovered or adopted it.

## Input

- Product with at least 5 features that have PostHog usage tracking
- PostHog tracking installed with feature-level events (`feature_used` with `feature: "{name}"` property)
- Intercom configured for in-app messaging
- Loops configured for email broadcasts and sequences
- n8n instance for scheduling the pipeline

## Steps

### 1. Build the feature usage matrix

Using `posthog-custom-events` and `posthog-cohorts`, build a matrix of features vs. users:

For each feature in the product:
- Query PostHog for `feature_used` events in the last 30 days
- Calculate: total unique users, percentage of active users, usage frequency per user
- Classify features by adoption:
  - **Saturated**: >70% of active users have used it in the last 30 days. No spotlight needed.
  - **Moderate**: 30-70% adoption. Spotlight to non-adopters who use related features.
  - **Underused**: <30% adoption. High spotlight priority — these are discovery opportunities.
  - **New**: Launched in the last 30 days. Spotlight to all active users.

Sort underused features by estimated value: features correlated with higher retention or upgrade rates get priority. Use `posthog-funnels` to check which features appear in retained-user funnels vs. churned-user funnels.

### 2. Select the next spotlight feature

From the prioritized list, pick the top feature for this week's spotlight. Selection criteria:

1. Not spotlighted in the last 8 weeks (avoid fatigue)
2. Has a clear, concrete benefit statement (not just "we have this feature")
3. Can be tried by the target audience without prerequisites (or the prerequisite is simple)
4. Has PostHog events to measure trial and adoption

Log the selection in Attio using `attio-lists` — maintain a "Spotlight Calendar" list with: feature name, spotlight date, target segment, and expected reach.

### 3. Identify the target audience

Using `posthog-cohorts`, build the spotlight's target cohort:

- **Include**: Active users (session in the last 14 days) who have NOT used this feature in the last 60 days
- **Exclude**: Users who received a spotlight in the last 2 weeks (prevent message fatigue)
- **Prioritize**: Users who actively use a related feature (they are most likely to find value in the spotlighted feature)

Calculate the target audience size. If the audience is fewer than 20 users, the feature may not be worth spotlighting — pick a different one.

### 4. Produce the spotlight content

Create the content package for this spotlight:

**Subject/headline**: Lead with the benefit, not the feature name. Format: "Did you know you can [specific outcome]?" or "[Specific outcome] in [time/clicks] — here's how."

**Body copy** (150 words max):
- One sentence describing the problem this feature solves
- One sentence explaining what the feature does (plain language, no jargon)
- One concrete example or use case showing the feature in action
- One CTA with a deep link directly into the feature (not to a help article, not to a generic dashboard)

**Visual**: A screenshot or GIF showing the feature. For email, a static image. For in-app, a GIF or short animation.

**PostHog tracking**: Define the events this spotlight will fire:
```
spotlight_delivered (feature, channel, cohort_id)
spotlight_opened (feature, channel)
spotlight_clicked (feature, channel)
spotlight_feature_tried (feature)
spotlight_feature_adopted (feature) — used again 7+ days later
```

### 5. Deliver the in-app spotlight

Using `intercom-in-app-messages`, create a targeted in-app message for the target cohort:

- **Format**: Banner or card (not a modal — spotlights should be informative, not interruptive)
- **Targeting**: The PostHog cohort from step 3, synced to Intercom
- **Timing**: Show on the user's next session after the spotlight goes live
- **Dismiss behavior**: Once dismissed, do not show again. Fire `spotlight_delivered` on show and `spotlight_clicked` on CTA click.
- **Frequency cap**: Maximum 1 in-app spotlight per user per 2 weeks

### 6. Deliver the email spotlight

Using `loops-broadcasts`, send a spotlight email to the target cohort members who have email opted in:

- **Subject line**: The benefit-led headline from step 4
- **Send time**: Tuesday or Wednesday at 10am in the user's timezone (or your best-performing send time)
- **Content**: The body copy + visual + CTA button with deep link
- **Tracking**: UTM parameters `utm_source=spotlight&utm_medium=email&utm_campaign={feature-slug}`

Using `posthog-custom-events`, fire `spotlight_delivered` with `channel: "email"` when the email is sent, and `spotlight_opened` when the email is opened (via Loops webhook to n8n).

### 7. Automate the weekly cadence

Using `n8n-scheduling` and `n8n-workflow-basics`, build a weekly n8n workflow:

1. **Monday (auto)**: Query PostHog for the feature usage matrix. Select the next spotlight feature based on priority and recency rules. Build the target cohort.
2. **Monday (human review)**: Agent drafts the content package and presents it for review. **Human action required:** Approve the feature selection and content before delivery.
3. **Tuesday (auto)**: Deploy the in-app message and send the email broadcast.
4. **Following Tuesday (auto)**: Pull 7-day results. Log `spotlight_feature_tried` and `spotlight_feature_adopted` counts. Update the Spotlight Calendar in Attio with results.

## Output

- Feature usage matrix updated weekly in PostHog
- Prioritized spotlight queue maintained in Attio
- Weekly spotlight content (in-app message + email) targeting non-adopters
- Full event tracking from delivery through adoption
- Automated cadence via n8n with human approval gate

## Triggers

The weekly cadence runs every Monday via n8n cron. Re-run the setup when adding new features to the product or when changing the spotlight format.
