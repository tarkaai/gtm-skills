---
name: multi-year-proposal-automation
description: Automate multi-year proposal generation and delivery — trigger on deal stage, generate options, deliver comparison docs, and track responses
category: Deal Management
tools:
  - n8n
  - Attio
  - Anthropic
  - Instantly
  - PostHog
fundamentals:
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-scheduling
  - attio-deals
  - attio-automation
  - deal-term-modeling
  - contract-comparison-generation
  - instantly-campaign
  - posthog-custom-events
---

# Multi-Year Proposal Automation

This drill automates the end-to-end flow from deal stage change to multi-year proposal delivery. When a deal enters the Proposed stage and meets qualification criteria, the agent generates deal term options, builds a comparison document, delivers it to the prospect, and tracks the response — all without manual intervention.

## Input

- n8n instance with Attio and PostHog integrations
- Attio deals pipeline with stage triggers configured
- Product pricing and discount parameters stored in n8n environment variables
- Anthropic API key for deal term generation
- Email delivery tool (Instantly or direct SMTP)

## Steps

### 1. Build the qualification trigger

Using `n8n-triggers`, create a workflow triggered by Attio webhook when a deal's stage changes to "Proposed":

Filter criteria (all must be true to proceed):
- Deal ACV >= $10,000 (multi-year negotiation overhead isn't worth it below this)
- Pain-to-price ratio >= 5x (strong value foundation needed)
- Champion identified (someone to receive the comparison doc)
- No existing multi-year proposal on this deal (`multi_year_status` = "not_proposed")

If any criteria fail, log why in Attio as a note: "Multi-year proposal skipped: {reason}". Fire `multiyear_proposal_skipped` PostHog event.

### 2. Generate deal terms automatically

Using `n8n-workflow-basics`, chain these steps in the n8n workflow:

1. Pull full deal context from Attio: ACV, champion, economic buyer, pain data, competitive intel, budget cycle
2. Call `deal-term-modeling` via the Anthropic API with the deal context
3. Validate the response: check TCV math, discount ranges, and option completeness
4. Store the 3 options in Attio as a note on the deal
5. Fire `multiyear_proposal_generated` PostHog event

### 3. Generate and deliver the comparison document

Continuing the n8n workflow:

1. Call `contract-comparison-generation` with the deal term options
2. Format the comparison as an HTML email (table layout with savings highlighted)
3. Using `instantly-campaign` or direct SMTP, send the comparison doc to the champion:
   - Subject: "{Company} — Contract options for your team"
   - From: The deal owner's email (not a generic address)
   - Body: The comparison document with a clear CTA ("Let's discuss which option works best — here's my calendar: {link}")
4. Update Attio: set `multi_year_status` = "proposed", log the proposal sent date
5. Fire `multiyear_proposal_sent` PostHog event

### 4. Build the follow-up sequence

Using `n8n-scheduling`, schedule follow-up checks:

**Day 3:** If no response to the comparison email:
- Send a follow-up: "Wanted to make sure this landed — any questions on the options I shared?"
- Fire `multiyear_followup_sent` event

**Day 7:** If still no response:
- Log in Attio: "No response to multi-year proposal after 7 days"
- **Human action required:** Alert the deal owner to follow up via phone/LinkedIn. Provide the negotiation brief from the deal modeling step.

**Day 14:** If still no response:
- Update `multi_year_status` to "stalled"
- Fire `multiyear_proposal_stalled` event

### 5. Handle responses

Using `n8n-triggers`, create response handlers:

**Positive response (prospect wants to discuss):**
- Update `multi_year_status` = "negotiating"
- Fire `multiyear_counter_received` if they propose different terms
- Alert the deal owner with the negotiation brief

**Negative response (prospect declines multi-year):**
- Update `multi_year_status` = "reverted_annual"
- Fire `multiyear_deal_reverted_annual` with the reason
- Log the revert reason for pattern analysis

**Counter-offer (prospect wants different terms):**
- Parse the counter-terms from the email
- Update Attio with the counter-offer details
- Fire `multiyear_counter_received` event
- Alert the deal owner with the original negotiation brief + counter-offer context

## Output

- Automated pipeline from deal stage change to proposal delivery
- Follow-up sequence with escalation to human
- Response handlers for all prospect paths
- Full event tracking for every step

## Triggers

Fires automatically when a deal enters the Proposed stage and meets qualification criteria. Follow-up sequence runs on schedule. Response handlers fire on email reply webhooks.
