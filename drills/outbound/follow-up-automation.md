---
name: follow-up-automation
description: Build n8n workflows that automate multi-touch follow-up sequences across channels
category: Outreach
tools:
  - n8n
  - Attio
  - Instantly
  - PostHog
fundamentals:
  - n8n-workflow-basics
  - n8n-triggers
  - attio-deals
  - posthog-custom-events
---

# Follow-Up Automation

This drill builds automated follow-up workflows in n8n that respond to prospect actions across email, LinkedIn, and your CRM. It ensures no prospect falls through the cracks while keeping outreach human and contextual.

## Prerequisites

- n8n instance running and connected to Attio and Instantly
- Active outreach campaigns (run `cold-email-sequence` or `linkedin-outreach` first)
- PostHog tracking set up for email and web events

## Steps

### 1. Map your follow-up triggers

Define the events that should trigger automated follow-up. Common triggers:

- Email opened 3+ times but no reply (high interest, needs nudge)
- Clicked a link in your email (engaged, ready for next step)
- Visited your website after receiving outreach (buying intent signal)
- Connected on LinkedIn but did not respond to message
- Meeting booked but no-show (needs reschedule)
- Positive reply but went cold after 5+ days

### 2. Build trigger workflows in n8n

Using the `n8n-triggers` fundamental, create webhook-based triggers for each event. Connect Instantly webhooks for email events, PostHog webhooks for website visits, and Attio webhooks for CRM status changes. Each trigger should include a delay node to prevent immediate robotic follow-up — wait at least 24 hours after the triggering event.

### 3. Design follow-up logic

Using the `n8n-workflow-basics` fundamental, build conditional workflows:

- **Email opener, no reply**: Send a shorter, different-angle follow-up 48 hours later. Reference that you shared something relevant (do not mention you know they opened it).
- **Link clicker**: Send a follow-up that goes deeper on the topic they clicked about. Offer a specific next step.
- **Website visitor**: If they visited your pricing page, fast-track to a meeting request. If they visited a blog post, share a related resource.
- **No-show**: Send a friendly reschedule message 2 hours after the missed meeting. Offer 2-3 new times.

### 4. Add safety guardrails

Every automated workflow needs limits. Set maximum touches per prospect (never exceed 8 total across all channels). Add a suppression check that skips prospects who replied negatively, unsubscribed, or are already in an active deal. Use the `attio-deals` fundamental to check CRM status before sending.

### 5. Connect to Attio for logging

Every automated action should update Attio: log the follow-up sent, update the last-touch date, and change the prospect's status. This gives your team visibility into what automation is doing.

### 6. Monitor and tune

Track automation-generated replies and meetings in PostHog using the `posthog-custom-events` fundamental. Review weekly: which triggers produce the most meetings? Which follow-up messages get the best response rates? Disable any workflow that produces low engagement or negative replies.
