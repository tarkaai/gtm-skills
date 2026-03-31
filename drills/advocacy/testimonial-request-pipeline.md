---
name: testimonial-request-pipeline
description: Identify high-satisfaction users, send contextual testimonial requests, collect structured responses, and store in CRM
category: Advocacy
tools:
  - PostHog
  - Attio
  - Intercom
  - Loops
  - Typeform
  - n8n
fundamentals:
  - posthog-cohorts
  - posthog-custom-events
  - attio-lists
  - attio-contacts
  - attio-custom-attributes
  - attio-notes
  - intercom-in-app-messages
  - loops-transactional
  - typeform-survey-setup
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-scheduling
---

# Testimonial Request Pipeline

This drill builds the end-to-end workflow for identifying testimonial candidates, sending contextual requests timed to moments of delight, collecting structured responses, and storing them in the CRM with metadata for downstream use. It works both as a one-time batch (Smoke) and as an always-on automation (Baseline+).

## Prerequisites

- PostHog tracking core product events for at least 30 days
- Attio configured with contact records and a `testimonial_status` custom attribute
- Intercom Messenger installed for in-app prompts
- Loops configured for transactional email
- Typeform or Tally account for the testimonial collection form

## Steps

### 1. Build the testimonial collection form

Using `typeform-survey-setup`, create a testimonial form with these fields:

- **Role and company** (short text): "What is your role and company name?"
- **Problem before** (long text): "What problem were you trying to solve before using [Product]?"
- **Outcome after** (long text): "What specific result have you achieved since using [Product]?"
- **Quantified impact** (short text): "Can you share a number? (e.g., saved 10 hours/week, increased revenue 30%)"
- **Recommendation** (opinion scale 1-10): "How likely are you to recommend [Product] to a peer?"
- **Quote permission** (multiple choice): "Can we use your words on our website, in sales materials, or both?"
- **Photo upload** (file upload, optional): "Upload a headshot for your testimonial"
- **Video option** (multiple choice): "Would you be willing to record a 60-second video testimonial?"

Add logic jumps: if recommendation score < 7, skip to a "What could we improve?" field and end the form (do not collect a testimonial from unhappy users -- route them to support instead). If score >= 9, show the video option. If 7-8, skip the video option.

Set the thank-you screen to acknowledge their contribution: "Thank you for sharing your experience. We will follow up within 48 hours."

Configure the Typeform webhook to POST responses to n8n.

### 2. Define testimonial candidate criteria

Using `posthog-cohorts`, create a "Testimonial Candidates" cohort with these conditions:

- Account age >= 60 days (enough time to have real results)
- Active in the last 14 days (currently engaged, not lapsed)
- Has completed at least 1 core workflow successfully in the last 30 days
- NPS score >= 8 (if NPS data exists) OR power_user_score >= 50
- Has NOT been asked for a testimonial in the last 90 days (check `testimonial_requested` person property)
- Has NOT already submitted a testimonial (check `testimonial_submitted` person property)

Using `attio-lists`, create a synced "Testimonial Candidates" list that mirrors this cohort.

### 3. Identify trigger moments

Configure testimonial requests to fire at moments of delight, not randomly. Using `posthog-custom-events`, define trigger events:

- `workflow_success`: user completes a major workflow with a successful outcome
- `milestone_reached`: user hits a usage milestone (100th session, 50th project, etc.)
- `nps_submitted`: user submits an NPS score of 9 or 10
- `subscription_renewed`: user renews or upgrades their plan
- `team_expanded`: user invites 3+ teammates in one week

Using `n8n-triggers`, create an event-driven workflow: when any trigger event fires for a user in the Testimonial Candidates cohort, initiate the request sequence.

### 4. Send the testimonial request

Using `intercom-in-app-messages`, send a contextual in-app message within 24 hours of the trigger event. The message must reference the specific trigger:

- After workflow success: "You just [completed X]. Your experience could help others facing the same challenge. Would you share a quick testimonial?"
- After milestone: "Congratulations on [milestone]. You have been using [Product] for [duration]. Mind sharing what it has meant for your work?"
- After high NPS: "Thanks for the kind score. Would you put those feelings into words? It takes 3 minutes."

Include a direct link to the Typeform. Do not ask them to "click here to learn more" -- the CTA must go directly to the form.

For users who do not interact with the in-app message within 48 hours, fall back to email using `loops-transactional`. Send one email with the same contextual framing. If no response after 7 days, mark the user as `testimonial_requested_no_response` in Attio and do not ask again for 90 days.

### 5. Process incoming testimonials

Using `n8n-triggers`, listen for the Typeform webhook. When a response arrives:

1. Parse the response fields
2. Using `attio-contacts`, update the contact: set `testimonial_status = submitted`, `testimonial_date = now`, `testimonial_quote = [their outcome text]`, `testimonial_permission = [website/sales/both]`
3. Using `attio-notes`, create a note on the contact with the full response text
4. Using `posthog-custom-events`, fire `testimonial_submitted` with properties: `trigger_event`, `recommendation_score`, `has_quantified_impact`, `willing_to_video`
5. Set `testimonial_submitted = true` as a PostHog person property (prevents re-asking)
6. If `willing_to_video = yes`, create a follow-up task in Attio for a team member to schedule a video recording session

### 6. Quality scoring

Score each testimonial 1-5 on these dimensions:

- **Specificity** (1-5): Does it name a concrete problem and outcome? "Great product" = 1. "Reduced our onboarding time from 3 weeks to 2 days" = 5.
- **Quantification** (1-5): Does it include a measurable number? No number = 1. Percentage or dollar figure = 5.
- **Attribution** (1-5): Does it clearly credit your product? Vague = 1. "Since switching to [Product], we..." = 5.
- **Authority** (1-5): Is the person's role/company compelling for your ICP? Unknown role = 1. VP at a recognizable company = 5.

Composite quality score = average of all four. Store in Attio as `testimonial_quality_score`. Testimonials scoring >= 3.5 are ready for marketing use. Below 3.5, flag for follow-up to ask clarifying questions.

## Output

- Typeform testimonial collection form with logic jumps
- PostHog cohort for testimonial candidates
- Trigger-based request workflow in n8n
- In-app and email request sequences
- Automated processing and CRM storage
- Quality scoring system

## Triggers

For Smoke: run as a manual batch -- pull the candidate list and send requests once. For Baseline+: the n8n workflow runs always-on, firing requests when trigger events occur. Process incoming responses immediately via webhook.
