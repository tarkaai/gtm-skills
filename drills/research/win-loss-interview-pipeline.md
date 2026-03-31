---
name: win-loss-interview-pipeline
description: End-to-end workflow from deal close to completed win/loss interview with transcript
category: Research
tools:
  - Attio
  - Cal.com
  - Fireflies
  - Typeform
  - Loops
  - n8n
fundamentals:
  - attio-deals
  - attio-lists
  - calcom-booking-links
  - calcom-event-types
  - fireflies-transcription
  - typeform-win-loss-survey
  - loops-sequences
  - n8n-triggers
  - n8n-workflow-basics
---

# Win/Loss Interview Pipeline

This drill builds the system that detects newly closed deals, reaches out to the buyer or lost prospect, schedules a win/loss interview, records and transcribes it, and collects structured survey data. The output is a completed interview transcript plus survey response linked back to the CRM deal.

## Prerequisites

- Attio CRM with deals being tracked through pipeline stages (Closed Won and Closed Lost)
- Cal.com account with at least one event type for interviews
- Fireflies.ai account for automatic transcription
- Typeform account for the fallback survey
- Loops account for outreach emails
- n8n instance for automation
- At least 5 recently closed deals (won or lost) to start with

## Input

- Deal records in Attio with status "Closed Won" or "Closed Lost"
- Primary contact email and name for each deal
- Deal close date (interviews should happen within 14 days of close for best recall)

## Steps

### 1. Identify interview candidates

Using the Attio MCP, query deals that moved to "Closed Won" or "Closed Lost" in the past 14 days and have NOT been tagged "winloss-outreach-sent". Create an Attio list called "Win/Loss Interview Queue" using the `attio-lists` fundamental. Add each qualifying deal's primary contact to this list with properties: deal_id, outcome (won/lost), deal_value, close_date, competitor (if known).

Filter criteria:
- Deal closed within last 14 days
- Primary contact has a valid email
- Deal value above your minimum threshold (skip tiny deals — they rarely yield useful insights)
- Contact has not been interviewed in the past 6 months

### 2. Create the interview event type

Using the `calcom-event-types` fundamental, create a Cal.com event type specifically for win/loss interviews:
- Title: "Quick feedback call — 20 min"
- Duration: 20 minutes (shorter gets higher acceptance)
- Description: "We'd love to learn from your experience evaluating [Product]. This is a brief, confidential conversation to help us improve."
- Buffer: 10 minutes before and after
- Availability: Weekday mornings and afternoons only
- Questions: None (keep booking friction zero)

### 3. Build the outreach sequence

Using the `loops-sequences` fundamental, create two email sequences:

**Won deal sequence (3 emails over 7 days):**
- Email 1 (Day 0): Subject: "Quick question about your experience with [Product]". Body: Thank them for choosing you. Ask for a 20-min call to understand what worked. Include Cal.com booking link. Tone: grateful, brief.
- Email 2 (Day 3): Subject: "Re: Quick question". Body: One-line follow-up. "If a call doesn't work, a 3-minute survey works too." Include both Cal.com link and Typeform survey link.
- Email 3 (Day 7): Subject: "Last ask". Body: Final nudge with survey link only. "Even 3 minutes of your feedback would help."

**Lost deal sequence (3 emails over 7 days):**
- Email 1 (Day 0): Subject: "Can I ask you something honest?". Body: Acknowledge they went another direction. No sales pitch. Ask for 20-min feedback call. Include Cal.com booking link. Tone: humble, genuinely curious.
- Email 2 (Day 3): Subject: "Re: honest question". Body: One-line follow-up. Include survey fallback link.
- Email 3 (Day 7): Subject: "3 minutes — that's it". Body: Survey link only. "Your honest take helps us get better."

Personalize each email using hidden fields: {contact_name}, {deal_outcome}, {product_name}.

### 4. Build the automation workflow

Using `n8n-triggers` and `n8n-workflow-basics`, create an n8n workflow:
- **Trigger:** Attio webhook — fires when a deal's status changes to "Closed Won" or "Closed Lost"
- **Step 1:** Check if the deal meets interview criteria (value threshold, valid email, not recently interviewed)
- **Step 2:** Generate personalized Typeform link with hidden fields (deal_id, contact_name, outcome, close_date)
- **Step 3:** Generate Cal.com booking link with UTM: `?utm_source=winloss&utm_campaign={deal_id}`
- **Step 4:** Enroll the contact in the appropriate Loops sequence (won or lost) with the Cal.com and Typeform links as merge fields
- **Step 5:** Tag the deal in Attio as "winloss-outreach-sent" with the outreach date
- **Step 6:** When a Cal.com booking is confirmed (via Cal.com webhook), tag the deal as "winloss-interview-scheduled" and ensure Fireflies is set to join that calendar event

### 5. Conduct the interview

**Human action required:** The founder or product lead conducts the 20-minute interview. Fireflies joins automatically to record and transcribe. Follow this structure:
- Minutes 0-2: Thank them, explain this is confidential and for internal improvement only
- Minutes 2-5: "Walk me through your evaluation process. How did you first hear about us?"
- Minutes 5-10: "What were the top 3 factors in your decision?" (probe each)
- Minutes 10-15: "What competitors did you evaluate? What did they do better/worse?"
- Minutes 15-18: "If you could change one thing about our product/process, what would it be?"
- Minutes 18-20: "Anything else I should know?" + thank them

### 6. Close the loop

After the interview or survey completion:
- Tag the deal in Attio as "winloss-interview-completed" or "winloss-survey-completed"
- Store the Fireflies transcript ID on the deal record
- Send a thank-you email via Loops transactional: "Thanks for your time. Your feedback is already being discussed internally."
- Remove the contact from the outreach sequence if still active

## Output

For each completed interview, you should have:
- A full transcript in Fireflies linked to the deal in Attio
- The deal tagged with interview status and completion date
- Contact removed from further outreach

For each survey completion, you should have:
- Structured survey responses in Typeform linked via hidden fields to the deal
- The deal tagged with survey status and completion date

## Triggers

- **Automated:** n8n workflow fires on every deal stage change to Closed Won/Lost
- **Manual backlog:** For deals closed before the automation was set up, run the Attio list query manually and enroll contacts in bulk
