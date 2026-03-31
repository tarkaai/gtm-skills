---
name: cold-call-framework
description: Structure and execute cold calls using a signal-based script framework with CRM logging
category: Outreach
tools:
  - Attio
  - Clay
  - PostHog
fundamentals:
  - attio-deals
  - clay-enrichment-waterfall
  - posthog-custom-events
---

# Cold Call Framework

This drill provides a structured framework for making effective cold calls. It covers pre-call research, scripting, objection handling, and systematic logging so you can measure and improve over time.

## Prerequisites

- Prospect list scored and enriched (run `enrich-and-score` drill first)
- Attio workspace with phone numbers populated
- Signal data available per prospect (funding, hiring, job changes)

## Steps

### 1. Build your call list

Pull the top-tier prospects from your scored list. Prioritize based on signal strength — prospects with recent triggers (new role, funding round, competitor churn) should be called first. Use the `clay-enrichment-waterfall` fundamental to fill in direct phone numbers if missing. Aim for a daily call block of 20-30 prospects.

### 2. Pre-call research (60 seconds per prospect)

Before each call, scan three things: their LinkedIn headline (current role and priorities), the signal that triggered outreach (funding, hire, tech adoption), and any prior touchpoints in Attio (emails sent, content downloaded). Write a one-sentence reason for calling that ties to their specific situation.

### 3. Structure the call script

Use this framework — not a rigid script, but a structure:

- **Opener (10 seconds)**: State your name, company, and a pattern interrupt. Reference the signal: "I noticed your team just closed a Series B — congrats."
- **Permission (5 seconds)**: "Did I catch you at an okay time?" Respect the answer.
- **Problem statement (15 seconds)**: Describe the problem you solve in their language. Make it specific to their role and signal.
- **Question (10 seconds)**: Ask an open-ended question about how they handle the problem today. Listen more than you talk.
- **Bridge (15 seconds)**: If there is interest, briefly explain how you help. One sentence, not a pitch deck.
- **CTA (10 seconds)**: Suggest a 15-minute follow-up call at a specific time.

### 4. Handle objections

Prepare responses for the top 5 objections: "not interested," "we already have something," "send me an email," "bad timing," and "who are you again?" For each, acknowledge their concern, ask one clarifying question, and either pivot or gracefully exit.

### 5. Log every call in Attio

Using the `attio-deals` fundamental, log call outcome immediately after hanging up: connected/voicemail/gatekeeper, duration, outcome (meeting set, follow-up requested, not interested, call back later), and any notes on their situation. Tag calls with the signal that triggered them.

### 6. Track and improve

Log call metrics in PostHog using the `posthog-custom-events` fundamental: calls made, connect rate, conversation rate, meeting rate. Review weekly. Benchmark: 20% connect rate, 10% meaningful conversation rate, 3-5% meeting rate from cold calls.
