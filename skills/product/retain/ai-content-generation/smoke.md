---
name: ai-content-generation-smoke
description: >
  AI Content Assistant — Smoke Test. Instrument the AI content generation feature, run a single
  cohort through the experience, and validate that AI-generated content drives measurable
  engagement lift before investing in automation.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=30% of test cohort uses AI content feature and acceptance rate >=50%"
kpis: ["AI content generation rate (generations per active user per week)", "Acceptance rate (accepted / generated)", "Retention delta (7-day retention of AI users vs non-users)"]
slug: "ai-content-generation"
install: "npx gtm-skills add product/retain/ai-content-generation"
drills:
  - posthog-gtm-events
  - onboarding-flow
  - threshold-engine
---

# AI Content Assistant — Smoke Test

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Validate that the AI content generation feature produces content users actually accept and that using it correlates with higher engagement. Run a single manual test with a small cohort (20-50 active users). The agent instruments tracking, configures the initial experience, and measures whether the feature shows retention signal before investing in always-on automation.

Pass threshold: >=30% of the test cohort generates at least one piece of AI content, AND acceptance rate (content accepted or edited-then-accepted vs total generated) is >=50%.

This is a one-time manual run. No automation, no always-on pipelines. Proof of signal only.

## Leading Indicators

- PostHog events for the full AI content lifecycle are firing correctly (prompt submitted, generated, accepted, rejected, edited, regenerated)
- At least 3 of the 5 content types available produce a non-zero acceptance rate
- Users who generate AI content return to the product within 48 hours at a higher rate than users who do not
- Regeneration rate is below 40% (users are not hammering retry to get usable output)
- At least one user generates 3+ pieces of content (repeat usage signal)

## Instructions

### 1. Instrument AI content event tracking

Run the `posthog-gtm-events` drill to set up the AI content event taxonomy. Ensure these events are firing in PostHog:

```
ai_content_prompt_submitted    — user initiated a generation request
ai_content_generated           — system returned a result
ai_content_accepted            — user accepted/published the generated content
ai_content_rejected            — user discarded the generated content
ai_content_edited              — user edited before accepting
ai_content_regenerated         — user requested a new generation for the same prompt
```

Properties on each event: `user_id`, `content_type` (blog_post, email, social_post, product_description, help_article), `prompt_length`, `generation_time_ms`.

Verify by triggering each event manually and confirming it appears in PostHog's live events stream. Do not proceed until all 6 events fire correctly.

### 2. Configure the initial in-app experience

Run the `onboarding-flow` drill to create a minimal discovery path for the AI content feature:

1. Using `intercom-product-tours`, build a 3-step product tour that triggers the first time a user visits the content creation area:
   - Step 1: "Try AI-assisted writing" — point to the AI generate button
   - Step 2: "Pick a content type" — show the content type selector
   - Step 3: "Review and edit" — show the output area and edit controls

2. Using `loops-transactional`, send a single email to the test cohort introducing the feature: one sentence on what it does, one sentence on how to try it, one direct link to the content creation area. No marketing fluff.

**Human action required:** Select 20-50 active users for the test cohort. These should be users who create content in the product (not admins, not dormant accounts). Approve the product tour copy and email before launch.

### 3. Run the test cohort for 7 days

Launch the product tour and send the email. Over 7 days, do not intervene further. Let the cohort discover and use the feature organically after the initial nudge. Monitor PostHog daily for:

- How many cohort members triggered `ai_content_prompt_submitted` (adoption)
- How many generated content was accepted vs rejected (quality)
- Whether any user generated content multiple times (repeat signal)
- Whether generation time is acceptable (<10 seconds for short content, <30 seconds for long)

### 4. Evaluate against threshold

Run the `threshold-engine` drill to measure against the pass criteria:

1. **Adoption rate**: Count distinct users in the test cohort who fired `ai_content_prompt_submitted` at least once. Divide by total cohort size. Target: >=30%.
2. **Acceptance rate**: Count `ai_content_accepted` + `ai_content_edited` (edited then accepted). Divide by `ai_content_generated`. Target: >=50%.
3. **Retention delta**: Compare 7-day return rate of cohort members who used AI content vs those who did not. Any positive delta is a good signal at Smoke level.

If PASS on both adoption and acceptance: proceed to Baseline. If FAIL on adoption: the feature needs better discoverability or the value proposition is unclear. If FAIL on acceptance: the AI output quality needs improvement before scaling.

**Human action required:** Review the results. If the retention delta is negative (AI users retained worse), investigate whether the feature is creating frustration rather than value. Do not proceed to Baseline with a negative retention signal.

## Time Estimate

- 1 hour: Instrument PostHog events and verify they fire (step 1)
- 1.5 hours: Build the product tour and email (step 2)
- 0.5 hours: Launch and configure the test cohort (step 3)
- 2 hours: Monitor daily and evaluate results (steps 3-4)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnel analysis, cohort comparison | Free tier: 1M events/mo. https://posthog.com/pricing |
| Intercom | Product tour for feature discovery | Starter: ~$39/seat/mo. https://www.intercom.com/pricing |
| Loops | One-time introduction email to test cohort | Free tier: 1,000 contacts. https://loops.so/pricing |

## Drills Referenced

- `posthog-gtm-events` -- instruments the AI content event taxonomy in PostHog
- `onboarding-flow` -- builds the product tour and introductory email for feature discovery
- `threshold-engine` -- evaluates adoption and acceptance metrics against pass criteria
