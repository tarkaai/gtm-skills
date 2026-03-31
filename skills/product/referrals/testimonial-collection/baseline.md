---
name: testimonial-collection-baseline
description: >
  Systematic Testimonial Collection — Baseline Run. Automate the testimonial
  request pipeline with trigger-based timing, always-on collection, and structured
  event tracking to sustain ≥25 testimonials over 2 weeks.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥25 testimonials with average quality ≥3.5 and ≥40% submission rate"
kpis: ["Collection rate", "Quality score", "Submission rate", "Form open rate"]
slug: "testimonial-collection"
install: "npx gtm-skills add product/referrals/testimonial-collection"
drills:
  - posthog-gtm-events
  - testimonial-request-pipeline
  - nps-feedback-loop
---
# Systematic Testimonial Collection — Baseline Run

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes
Establish an always-on testimonial collection pipeline that triggers requests at moments of delight. Collect 25+ testimonials with an average quality score of 3.5+ and a submission rate of 40%+ from form opens. The pipeline runs continuously without manual intervention.

## Leading Indicators
- Trigger events firing correctly (≥5 per week across all trigger types)
- In-app message delivery rate ≥90%
- Form open rate from requests ≥40%
- At least 5 testimonials include quantified impact and score ≥4.0

## Instructions

### 1. Configure testimonial event tracking
Run the `posthog-gtm-events` drill to set up the full event taxonomy for this play:

- `testimonial_candidate_identified` — user enters the eligible cohort
- `testimonial_requested` — in-app message or email sent (properties: `trigger_event`, `channel`, `user_tier`)
- `testimonial_form_opened` — user clicks through to the Typeform
- `testimonial_form_abandoned` — user opens form but does not submit (track via Typeform partial responses)
- `testimonial_submitted` — user completes the form (properties: `recommendation_score`, `has_quantified_impact`, `willing_to_video`, `quality_score`)
- `testimonial_published` — testimonial approved and deployed to website or sales materials

Build a PostHog funnel: `testimonial_requested` → `testimonial_form_opened` → `testimonial_submitted` → `testimonial_published`. This funnel is the core measurement for all optimization going forward.

### 2. Automate the request pipeline
Run the full `testimonial-request-pipeline` drill (all 6 steps). This converts the manual Smoke process into always-on automation:

- PostHog cohort auto-identifies eligible candidates daily
- n8n workflow listens for trigger events (workflow_success, milestone_reached, nps_submitted, subscription_renewed, team_expanded)
- When a trigger fires for an eligible candidate, n8n sends a contextual Intercom in-app message within 24 hours
- If no in-app engagement after 48 hours, n8n sends a Loops email as fallback
- Typeform webhook fires on submission, n8n processes the response, updates Attio, and scores quality automatically

**Human action required:** Review the first 10 automated requests to confirm the contextual copy reads naturally. Adjust the message templates if any feel generic or robotic.

### 3. Feed NPS promoters into the pipeline
Run the `nps-feedback-loop` drill to connect NPS data to testimonial collection. Configure the NPS follow-up logic:

- Promoters (9-10): immediately add to the testimonial candidates list if they are not already there. Their NPS submission IS the trigger event — fire `testimonial_requested` within 24 hours of their NPS response.
- Passives (7-8): do not request a testimonial. Focus on moving them to promoter status first.
- Detractors (0-6): route to support. Never request testimonials from unhappy users.

This ensures that every expression of satisfaction is captured as a testimonial opportunity.

### 4. Evaluate against threshold
Measure against: ≥25 testimonials with average quality ≥3.5 and ≥40% submission rate. If PASS, proceed to Scalable. If FAIL, diagnose which funnel stage has the biggest drop-off:

- Low request volume: not enough trigger events firing. Lower candidate criteria or add more trigger types.
- Low form open rate: request copy is weak or timing is off. Test different message variants.
- Low submission rate: form is too long or too hard. Test a shorter variant.
- Low quality: form questions are not extracting specific enough answers. Add examples and prompts.

## Time Estimate
- 4 hours: configure event tracking and build PostHog funnels
- 6 hours: build the full n8n automation (trigger detection, message sending, response processing)
- 3 hours: connect NPS pipeline and test end-to-end
- 3 hours: monitor, review first automated outputs, adjust templates

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| Typeform | Testimonial collection form with logic | $25/mo Basic (100 responses/mo) |
| PostHog | Event tracking, funnels, cohorts | Free tier (1M events/mo) |
| n8n | Automation workflows for request pipeline | Self-hosted free or $20/mo cloud |
| Attio | Store testimonials, contact metadata, quality scores | Included in standard stack |
| Intercom | In-app testimonial requests | Included in standard stack |
| Loops | Fallback email requests, NPS follow-up | Included in standard stack |

**Play-specific cost:** ~$25-45/mo (Typeform + n8n cloud if not self-hosted)

## Drills Referenced
- `posthog-gtm-events` — full testimonial event taxonomy and funnel setup
- `testimonial-request-pipeline` — automated candidate identification, trigger-based requests, response processing, quality scoring
- `nps-feedback-loop` — feed NPS promoters into the testimonial pipeline as high-priority candidates

---

## Pass threshold
**≥25 testimonials with average quality ≥3.5 and ≥40% submission rate**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add product/referrals/testimonial-collection`_
