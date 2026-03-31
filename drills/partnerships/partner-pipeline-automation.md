---
name: partner-pipeline-automation
description: Automate partner outreach, scheduling, blurb delivery, and performance tracking at scale
category: Partnerships
tools:
  - n8n
  - Attio
  - PostHog
  - Loops
  - Instantly
fundamentals:
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-scheduling
  - n8n-crm-integration
  - n8n-email-integration
  - attio-automation
  - attio-deals
  - posthog-custom-events
  - loops-sequences
---

# Partner Pipeline Automation

This drill builds the n8n automation layer that manages a portfolio of 20+ newsletter partners: tracking who is due for outreach, scheduling placements, delivering blurb copy, and routing performance data back to your CRM. Without this automation, managing more than 5 partners simultaneously becomes a manual bottleneck.

## Input

- Active partner list in Attio (from `partner-prospect-research` drill, status: "Active")
- n8n instance configured with Attio, PostHog, Loops, and Instantly integrations
- Blurb templates from previous `newsletter-shoutout-copy` runs

## Steps

### 1. Build the partner outreach sequence

Using the `n8n-workflow-basics` and `n8n-email-integration` fundamentals, create an n8n workflow for initial partner outreach:

- **Trigger**: New partner added to the "Newsletter Partners" list in Attio with status "Prospect"
- **Action 1**: Enrich partner contact (pull LinkedIn URL, company info from Attio)
- **Action 2**: Send personalized outreach email via Instantly (template: propose newsletter co-marketing, reference their audience overlap, suggest a low-commitment first test)
- **Action 3**: If no reply after 5 days, send one follow-up via Instantly
- **Action 4**: If reply received (Instantly webhook), update Attio status to "In Conversation"
- **Action 5**: If positive reply detected (Instantly intent classification), create an Attio deal in the "Partnerships" pipeline

### 2. Build the placement scheduling workflow

Using the `n8n-scheduling` fundamental, create a recurring workflow that manages placement timing:

- **Trigger**: Weekly cron (Monday 9am)
- **Action 1**: Query Attio for active partners where "Next Placement Date" is within the next 14 days
- **Action 2**: For each upcoming placement, check if a blurb has been approved (Attio field: "Blurb Status")
- **Action 3**: If no blurb approved, send a Slack/email alert: "Blurb needed for {partner} by {date}"
- **Action 4**: If blurb approved but not yet sent to partner, auto-send the blurb to the partner contact via email with the tracked CTA link
- **Action 5**: Update Attio: "Blurb Delivered" with timestamp

### 3. Build the performance tracking workflow

Using the `n8n-triggers` and `posthog-custom-events` fundamentals, create a webhook-triggered workflow:

- **Trigger**: PostHog webhook fires when a `co_marketing_click` event occurs with a `utm_source` matching a partner slug
- **Action 1**: Look up the partner in Attio by slug
- **Action 2**: Increment the partner's "Total Leads" counter in Attio
- **Action 3**: Create a new lead record in Attio linked to the partner (source: co-marketing, partner: {name})
- **Action 4**: If this is the partner's first lead, send a celebratory Slack notification

### 4. Build the partner nurture sequence

Using the `loops-sequences` fundamental, create a Loops sequence for partners (not prospects, but the partners themselves):

- **Day 0**: Welcome email after first successful placement (thank them, share initial click data)
- **Day 7**: Share full performance report from first placement
- **Day 14**: Propose the next placement with an updated blurb
- **Day 30**: Monthly partnership summary (total clicks, leads, and value generated for both sides)

This keeps partners engaged and increases the likelihood of repeat placements.

### 5. Build the partner health monitoring workflow

Using the `n8n-scheduling` fundamental, create a monthly health check:

- **Trigger**: Monthly cron (1st of month)
- **Action 1**: Query Attio for all active partners
- **Action 2**: For each partner, pull PostHog data: clicks and leads in the last 30 days
- **Action 3**: Calculate: cost per lead (if any budget spent), lead quality (did leads convert?), partner responsiveness (time from blurb sent to placement confirmed)
- **Action 4**: Flag partners with zero leads in 2+ months as "At Risk"
- **Action 5**: Flag partners with consistent high performance as "Expand" candidates
- **Action 6**: Output a monthly partner report to Slack and store in Attio

## Output

- Automated partner outreach pipeline (prospect → conversation → active partner)
- Scheduled placement management (never miss a placement window)
- Real-time lead attribution to specific partners
- Partner nurture sequence keeping relationships warm
- Monthly health scoring for portfolio optimization

## Triggers

Build these workflows once at the start of Scalable level. They run continuously. Review and tune monthly based on the partner health report.
