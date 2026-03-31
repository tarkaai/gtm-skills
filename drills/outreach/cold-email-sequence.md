---
name: cold-email-sequence
description: Build and launch a multi-step cold email sequence using Instantly with personalized copy and tracking
category: Outreach
tools:
  - Instantly
  - Clay
  - Attio
  - PostHog
fundamentals:
  - instantly-campaign-setup
  - instantly-warmup
  - cold-email-copywriting
  - clay-enrichment-waterfall
  - posthog-event-tracking
---

# Cold Email Sequence

This drill walks you through building a cold email sequence from copy creation through launch and tracking. It produces a multi-step campaign in Instantly that is personalized using Clay enrichment data.

## Prerequisites

- Instantly account with warmed-up sending domains
- Clay table with enriched prospect data (run `enrich-and-score` drill first)
- Attio workspace with prospects loaded
- ICP definition complete

## Steps

### 1. Warm up sending infrastructure

Before sending a single cold email, verify your sending domains are healthy. Use the `instantly-warmup` fundamental to check domain reputation, SPF/DKIM/DMARC records, and warmup status. Each sending account needs at least 2 weeks of warmup. Aim for 30-50 emails per day per account to start.

### 2. Write the sequence copy

Using the `cold-email-copywriting` fundamental, draft a 3-5 step sequence. Each email has a specific role:

- **Email 1 (Day 0)**: Problem-aware opener. Lead with a pain point specific to their role or industry. No pitching. Under 80 words.
- **Email 2 (Day 3)**: Value angle. Share a relevant insight, data point, or mini case study. Still no hard ask.
- **Email 3 (Day 7)**: Soft CTA. Offer something low-friction: a 15-minute call, a relevant resource, or a quick audit.
- **Email 4 (Day 12)**: Breakup email. Acknowledge you might not be a fit, restate the core value, give a final easy CTA.

Personalize the first line of each email using Clay variables: company name, recent funding, job title, technology stack, or a signal you detected.

### 3. Build personalization variables in Clay

Open your enriched Clay table and create template columns that map to Instantly merge fields. Use the `clay-enrichment-waterfall` fundamental to fill any gaps. Common variables: first name, company, one-line personalization (built from signal data), competitor mention, industry-specific pain point.

### 4. Set up the campaign in Instantly

Using the `instantly-campaign-setup` fundamental, create a new campaign. Upload your prospect list from Clay. Map merge fields to your email copy variables. Set the sending schedule: weekdays only, 8am-11am in the prospect's timezone. Set daily send limits per account. Enable open and click tracking.

### 5. Configure reply handling

Set up Instantly to detect positive replies (interested, meeting request), negative replies (not interested, wrong person), and out-of-office responses. Route positive replies to Attio as hot leads with an "Interested" tag. Negative replies get marked in Attio to prevent re-contact.

### 6. Launch and monitor

Send to a test batch of 20-30 prospects first. Check deliverability, open rates, and that personalization renders correctly. If test metrics look healthy (open rate above 40%, no bounces), launch the full campaign.

### 7. Track results in PostHog

Using the `posthog-event-tracking` fundamental, log campaign-level events: emails sent, opens, clicks, replies, meetings booked. Track the full funnel from send to meeting to deal. Feed results back to refine your scoring model and copy.
