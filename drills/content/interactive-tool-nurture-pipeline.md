---
name: interactive-tool-nurture-pipeline
description: Automated post-completion nurture sequence that personalizes follow-up based on interactive tool results and score tiers
category: Content
tools:
  - n8n
  - Loops
  - Anthropic
  - Attio
  - PostHog
fundamentals:
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-scheduling
  - loops-sequences
  - loops-audience
  - anthropic-api-patterns
  - attio-contacts
  - attio-deals
  - attio-lead-scoring
  - posthog-custom-events
  - posthog-cohorts
---

# Interactive Tool Nurture Pipeline

This drill builds the automated follow-up system that converts interactive tool completions into meetings and pipeline. Instead of sending the same generic nurture to every tool user, it personalizes follow-up content and cadence based on what the user's tool results revealed about their situation.

## Input

- One or more live interactive tools with email capture (from `interactive-tool-build` drill)
- Tool result data flowing to n8n via webhook (tool type, primary result, result tier, all inputs)
- Loops account configured for email sequences
- Attio CRM with deal records for tool leads

## Steps

### 1. Define result-based segments

Map tool results into segments that determine nurture strategy:

| Result Tier | Criteria | Nurture Strategy | Urgency |
|------------|----------|-----------------|---------|
| High-value | Result indicates significant pain/opportunity (e.g., ROI >5x, maturity score <30) | Fast-track to meeting. Short sequence, 3 emails over 5 days. | High |
| Medium-value | Result indicates moderate pain/opportunity (e.g., ROI 2-5x, maturity score 30-60) | Educate then convert. 5 emails over 14 days. Build urgency. | Medium |
| Low-value | Result indicates low pain (e.g., ROI <2x, maturity score 60+) | Long nurture. 4 emails over 30 days. Share content, build relationship. | Low |

### 2. Build the segmentation workflow in n8n

Using `n8n-triggers`, create a workflow triggered by the interactive tool completion webhook:

1. **Parse the payload**: Extract email, tool type, primary result, result tier, all input values
2. **Score the lead**: Using the result tier mapping from step 1, assign a segment (high/medium/low)
3. **Enrich**: Use `attio-contacts` to check if this person already exists in CRM. If yes, merge data and check existing deal status. If no, create new records.
4. **Route**:
   - High-value → enroll in "Tool Lead — Fast Track" Loops sequence + create Attio deal at "High-Intent Tool Lead" stage + send Slack alert to sales
   - Medium-value → enroll in "Tool Lead — Education" Loops sequence + create Attio deal at "Tool Lead" stage
   - Low-value → enroll in "Tool Lead — Long Nurture" Loops sequence + create Attio contact (no deal yet)

### 3. Build the email sequences in Loops

Using `loops-sequences`, create three sequences. Each email references the user's specific tool results.

**Sequence: Tool Lead — Fast Track (high-value)**

Use `loops-audience` to pass these Loops contact properties: `tool_type`, `primary_result`, `result_tier`, `company_name`, all relevant input values.

- **Email 1 (immediate)**: Subject: "Your {tool_type} results — and what they mean"
  - Body: Recap their primary result. Provide 1-2 personalized insights based on their inputs. Include one industry benchmark for context. CTA: "Let's discuss your results — book 15 minutes" → Cal.com link.
- **Email 2 (day 2)**: Subject: "How {similar_company} solved the same problem"
  - Body: Relevant case study or example matching their result tier. Show before/after metrics. CTA: Same booking link.
- **Email 3 (day 5)**: Subject: "Your {tool_type} results expire in 7 days"
  - Body: Create urgency with expiring link to results. Offer a personal walkthrough. CTA: Booking link + "Reply to this email with questions."

**Sequence: Tool Lead — Education (medium-value)**

- **Email 1 (immediate)**: Results recap + personalized insights + link to related content
- **Email 2 (day 3)**: Deep-dive content on their weakest area (based on tool inputs)
- **Email 3 (day 7)**: Case study relevant to their score tier
- **Email 4 (day 10)**: ROI framing specific to their result ("Based on your numbers, here's what improvement looks like")
- **Email 5 (day 14)**: Direct CTA: "Ready to improve your score?" → booking link

**Sequence: Tool Lead — Long Nurture (low-value)**

- **Email 1 (immediate)**: Results recap + congratulations on strong score
- **Email 2 (day 7)**: Advanced content: "What separates the top 10% in {area}"
- **Email 3 (day 14)**: Invite to retake assessment quarterly to track progress
- **Email 4 (day 30)**: New tool or content relevant to their profile + soft CTA

### 4. Generate personalized email content with AI

Using `anthropic-api-patterns`, build an n8n node that generates personalized email body content for each lead:

```
POST https://api.anthropic.com/v1/messages

System: "You are writing a follow-up email to someone who just completed a {TOOL_TYPE}. Their results: {PRIMARY_RESULT}. Their inputs: {INPUT_SUMMARY}. Their result tier: {RESULT_TIER}. Write a 3-paragraph email that:
1. References their specific result and what it means
2. Provides one actionable insight they can implement immediately (this builds trust)
3. Includes a natural CTA to book a call — framed as helping them improve, not selling
Keep it under 150 words. Write in the voice of a helpful expert, not a salesperson."
```

Store the generated content in Loops contact properties so each email dynamically includes their personalized insight.

### 5. Configure re-engagement triggers

Using `posthog-cohorts` and `n8n-scheduling`, set up triggers for re-engagement:

- **Tool result page revisit**: If a tool lead returns to their results page (tracked via PostHog), immediately notify sales in Slack. This signals active evaluation.
- **Website visit after tool**: If a tool lead visits pricing or product pages within 14 days, upgrade their Attio deal stage and send a targeted Loops email: "I noticed you're exploring — want a walkthrough?"
- **Retake trigger**: 90 days after completion, send an email inviting them to retake the tool. Compare new results to old results. Improvement = validation. Decline = new pain point to address.

### 6. Track nurture performance

Using `posthog-custom-events`, track:

| Event | Trigger | Properties |
|-------|---------|-----------|
| `nurture_email_sent` | Loops sends email | `sequence`, `step`, `tool_type`, `result_tier` |
| `nurture_email_opened` | Email opened | `sequence`, `step`, `tool_type`, `result_tier` |
| `nurture_cta_clicked` | CTA link clicked | `sequence`, `step`, `cta_type` |
| `nurture_meeting_booked` | Meeting booked from nurture email | `sequence`, `step`, `tool_type`, `result_tier` |
| `nurture_reply_received` | Lead replies to nurture email | `sequence`, `step`, `sentiment` |

Build a PostHog funnel: `tool_completed` → `nurture_email_opened` → `nurture_cta_clicked` → `nurture_meeting_booked`. Segment by result tier and tool type.

## Output

- Three Loops sequences (fast-track, education, long-nurture) with personalized content
- n8n workflow routing tool leads to the correct sequence based on result tier
- AI-generated personalized email content for each lead
- Re-engagement triggers for high-intent behavior detection
- PostHog funnel tracking nurture-to-meeting conversion

## Triggers

Set up once at Baseline level. Refine and add sequences at Scalable level. At Durable level, the `autonomous-optimization` drill monitors and improves sequence performance.
