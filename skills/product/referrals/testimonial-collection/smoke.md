---
name: testimonial-collection-smoke
description: >
  Systematic Testimonial Collection — Smoke Test. Manually identify happy customers,
  send contextual testimonial requests, and collect at least 10 usable testimonials
  to prove the pipeline produces signal.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥10 testimonials with average quality score ≥3.0"
kpis: ["Collection rate", "Quality score", "Submission rate"]
slug: "testimonial-collection"
install: "npx gtm-skills add product/referrals/testimonial-collection"
drills:
  - testimonial-request-pipeline
  - threshold-engine
---
# Systematic Testimonial Collection — Smoke Test

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes
Collect at least 10 customer testimonials with an average quality score of 3.0 or higher. Prove that your user base contains willing, articulate advocates whose words can be used in marketing and sales.

## Leading Indicators
- Form open rate from request messages (target: ≥40%)
- Form completion rate (target: ≥50% of opens)
- At least 3 testimonials include a quantified impact metric

## Instructions

### 1. Build the testimonial collection form
Run the `testimonial-request-pipeline` drill, step 1 only. Create the Typeform with structured fields: role/company, problem before, outcome after, quantified impact, recommendation score, and quote permission. Configure the logic jump so users scoring <7 on the recommendation question are routed away from the testimonial flow. Set the webhook to POST to n8n (or manually export responses for Smoke).

**Human action required:** Review the form copy and test it yourself before sending to any customer. Ensure the questions are clear and the form takes under 4 minutes to complete.

### 2. Identify your first 30 testimonial candidates
Run the `testimonial-request-pipeline` drill, step 2. Manually pull a list from PostHog and Attio: users with account age ≥60 days, active in the last 14 days, and any positive signal (high NPS, frequent usage, successful support interactions, or verbal praise in support tickets). You do not need automated cohorts for Smoke — a manual query is sufficient.

Sort by likelihood of response: users who have already said something positive (in NPS, support, or email) go first.

### 3. Send contextual testimonial requests
For each candidate, send a personalized request via Intercom in-app message or Loops email. Reference something specific about their usage: "You have been using [Feature X] for [Y weeks] and completed [Z workflows]. Your experience could help others facing the same challenge."

Include a direct link to the Typeform. Do not batch-blast — send in waves of 10 over 3 days so you can adjust messaging based on early response rates.

**Human action required:** Write the first 5 request messages personally. After confirming the tone works (≥2 responses from first 5), template the approach for the remaining 25.

### 4. Process and score responses
As testimonials come in, run the quality scoring from `testimonial-request-pipeline` drill, step 6. Score each on specificity (1-5), quantification (1-5), attribution (1-5), and authority (1-5). Store the scores and full text in Attio as notes on each contact.

For testimonials scoring below 3.0, send a brief follow-up asking one clarifying question: "Could you share a specific number — hours saved, percentage improvement, or revenue impact?"

### 5. Evaluate against threshold
Run the `threshold-engine` drill to measure against: ≥10 testimonials with average quality score ≥3.0. If PASS, proceed to Baseline. If FAIL, diagnose: was the issue low response rate (adjust messaging or targeting) or low quality (adjust form questions or follow-up process)?

## Time Estimate
- 1 hour: build and test the Typeform
- 1 hour: pull candidate list and prioritize
- 2 hours: write and send personalized requests
- 1 hour: process responses, score quality, follow up

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| Typeform | Testimonial collection form | Free (10 responses/mo) or $25/mo Basic |
| PostHog | Identify candidates via usage data | Free tier (1M events/mo) |
| Attio | Store testimonials and contact metadata | Included in standard stack |
| Intercom | In-app testimonial requests | Included in standard stack |
| Loops | Fallback email requests | Included in standard stack |

**Play-specific cost:** Free (if under 10 responses) or ~$25/mo for Typeform Basic

## Drills Referenced
- `testimonial-request-pipeline` — form setup, candidate identification, request sending, quality scoring
- `threshold-engine` — pass/fail evaluation against ≥10 testimonials at ≥3.0 quality

---

## Pass threshold
**≥10 testimonials with average quality score ≥3.0**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/referrals/testimonial-collection`_
