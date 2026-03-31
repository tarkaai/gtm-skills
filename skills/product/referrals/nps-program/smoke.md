---
name: nps-program-smoke
description: >
  NPS Feedback System — Smoke Test. Deploy a one-time NPS survey to a small user cohort,
  collect responses, classify promoters/passives/detractors, and manually close the loop
  to validate that NPS produces actionable signal for this product.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥30% response rate from a 50-user cohort AND ≥3 actionable detractor themes identified"
kpis: ["NPS response rate", "NPS score", "Detractor theme count", "Promoter count"]
slug: "nps-program"
install: "npx gtm-skills add product/referrals/nps-program"
drills:
  - nps-feedback-loop
  - threshold-engine
---

# NPS Feedback System — Smoke Test

> **Stage:** Product > Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

A single NPS survey deployed to 50 users produces enough responses to calculate an NPS score and extract at least 3 actionable detractor themes. The agent confirms that NPS data correlates with observable product behavior (e.g., detractors have lower usage, promoters use specific features more).

## Leading Indicators

- Survey delivery confirmed (50 users received the survey)
- First 5 responses arrive within 48 hours of deployment
- Open-text responses contain specific, categorizable feedback (not just "good" or "bad")
- At least 1 promoter responds positively to a manual referral ask

## Instructions

### 1. Select the survey cohort

Using PostHog, identify 50 users who meet ALL of these criteria:
- Active in the last 14 days (they will actually see the survey)
- Signed up at least 30 days ago (not too new to have an opinion)
- Not currently in an active support conversation (biased timing)
- Have completed at least one core product workflow (have enough experience to rate)

Export the user list: user_id, email, plan, signup_date, last_active_date, core_actions_count.

### 2. Deploy the NPS survey

Run the `nps-feedback-loop` drill, specifically steps 1 and 2, to deploy the survey. For this smoke test:

- Use Intercom in-app survey for users active in the last 3 days (higher response rate)
- Use Loops transactional email for users active 4-14 days ago (catch less frequent users)
- Survey format: Question 1 "How likely are you to recommend [product] to a colleague?" (0-10 scale). Question 2 "What is the main reason for your score?" (required open text)
- Set the survey to run for 7 days, then close

**Human action required:** Review the survey copy and confirm it matches your brand voice before the agent deploys. Approve the 50-user cohort list.

### 3. Monitor response collection

Track responses daily for the 7-day survey window. Log each response in a structured format:

| user_id | score | segment | open_text | plan | tenure_days | usage_tier |
|---------|-------|---------|-----------|------|-------------|------------|

Classify each respondent: Promoter (9-10), Passive (7-8), Detractor (0-6).

### 4. Analyze and categorize responses

After 7 days, run the `nps-feedback-loop` drill step 3 to segment and analyze:

- Calculate overall NPS: ((Promoters - Detractors) / Total Responses) * 100
- Group detractor open-text by theme: missing feature, usability issue, performance, pricing, support quality, other
- Cross-reference scores with PostHog usage data: do promoters use specific features more? Do detractors have lower engagement?
- Identify the top 3 detractor themes by frequency

### 5. Manually close the loop

For this smoke test, manually execute the follow-up actions from `nps-feedback-loop` drill step 4:

- **Promoters:** Send a personal thank-you email. Ask one promoter if they would leave a G2/Capterra review. Note their response.
- **Passives:** Send a follow-up email sharing a resource relevant to their open-text feedback. Track if they engage.
- **Detractors:** Send a personal email from a real team member (not automated). Acknowledge their specific concern. Ask for a 15-minute call. Track response rate.

**Human action required:** A team member must personally respond to each detractor. This cannot be automated at smoke level.

### 6. Evaluate against threshold

Run the `threshold-engine` drill to measure:
- Response rate: count responses / 50 users. Pass threshold: ≥30%.
- Actionable themes: count distinct detractor themes with 2+ mentions. Pass threshold: ≥3 themes.
- NPS score: record the score. No threshold at smoke level (just establishing the baseline).

If PASS: document the NPS score, response rate, top themes, and promoter/detractor behavior patterns. Proceed to Baseline.
If FAIL on response rate: test a different survey channel (switch email users to in-app or vice versa) and re-run.
If FAIL on themes: the cohort may be too homogeneous. Widen the cohort criteria and re-run.

## Time Estimate

- Cohort selection and survey setup: 2 hours
- Survey deployment and monitoring: 1 hour (spread over 7 days)
- Analysis and categorization: 1.5 hours
- Manual follow-up and evaluation: 1.5 hours

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Intercom | In-app NPS survey delivery | Proactive Support Plus add-on: $99/mo for 500 messages. [Pricing](https://www.intercom.com/pricing) |
| PostHog | Cohort selection, usage data cross-reference | Surveys: 1,500 free responses/mo, then $0.10/response. [Pricing](https://posthog.com/pricing) |
| Loops | Email survey delivery, follow-up emails | From $49/mo for 1,000+ subscribers. Transactional email free on paid plans. [Pricing](https://loops.so/pricing) |
| Attio | Store response data, track follow-ups | Free for up to 3 users. Plus: $29/user/mo. [Pricing](https://attio.com/pricing) |

**Estimated play-specific cost at this level:** $0 if within free tiers (PostHog surveys free up to 1,500 responses). If using Intercom surveys, included in existing Proactive Support Plus add-on.

## Drills Referenced

- `nps-feedback-loop` — deploys the NPS survey, segments responses, and defines follow-up actions per segment
- `threshold-engine` — evaluates response rate and theme count against pass/fail criteria
