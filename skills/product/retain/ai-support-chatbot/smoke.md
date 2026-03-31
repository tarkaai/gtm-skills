---
name: ai-support-chatbot-smoke
description: >
  AI In-App Support — Smoke Test. Deploy an AI chatbot to handle support questions
  inside your product and validate that at least 50% of users engage with it and
  30% of conversations are resolved without human intervention.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥50% of support-seeking users engage chatbot; ≥30% AI resolution rate"
kpis: ["Chatbot engagement rate", "AI resolution rate", "CSAT for AI-resolved conversations"]
slug: "ai-support-chatbot"
install: "npx gtm-skills add product/retain/ai-support-chatbot"
drills:
  - threshold-engine
---

# AI In-App Support — Smoke Test

> **Stage:** Product → Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

Prove the concept: can an AI chatbot inside your product resolve real support questions without human help? Deploy Fin AI to a small test group, connect your existing help articles, and measure whether users engage with it and whether it can resolve at least 30% of conversations autonomously. No always-on automation. One agent run, one test cohort, one week of data.

## Leading Indicators

- Fin AI connects to your Help Center and returns answers for 80%+ of your top 20 support questions (knowledge coverage)
- At least 10 unique users initiate a chatbot conversation in the first 3 days (adoption signal)
- Escalation reasons are distributed across multiple categories, not dominated by a single failure mode (bot is attempting to help, not blanket-failing)

## Instructions

### 1. Prepare your knowledge base

Before deploying the chatbot, audit your Intercom Help Center. List your top 20 support questions from the last 90 days of support tickets. For each question, verify a published article exists with a clear, direct answer.

If fewer than 15 of the 20 questions have articles, write and publish the missing articles first. Each article: question as the title, 1-2 sentence direct answer, then step-by-step instructions. Keep under 400 words.

### 2. Deploy the AI chatbot

Run the the ai chatbot deployment workflow (see instructions below) drill to:
- Enable Fin AI on your Intercom workspace
- Connect your Help Center as the primary knowledge source
- Add your docs site as an external URL source
- Create 5 custom answers for your most-asked questions
- Configure escalation rules (user requests human, low confidence, max 4 bot replies, sensitive topics)
- Instrument PostHog tracking events: `chatbot_conversation_started`, `chatbot_resolved_by_ai`, `chatbot_escalated_to_human`, `chatbot_csat_submitted`, `chatbot_article_suggested`
- Deploy behind a PostHog feature flag to 10-20% of users (your test cohort)

### 3. Run the test for 7 days

Monitor daily:
- How many users in the test cohort initiated a conversation?
- What % did Fin resolve without handoff?
- What topics caused the most escalations?
- Any user complaints about the bot?

Do not tune or fix during the first 3 days. Collect clean baseline data. After day 3, if a single topic is causing >50% of escalations, add a custom answer for it and continue.

**Human action required:** Monitor the Intercom inbox for escalated conversations. Respond to them normally. Note any cases where Fin gave an incorrect answer — these need knowledge base fixes.

### 4. Evaluate against threshold

Run the `threshold-engine` drill to measure:
- **Engagement rate**: Of users in the test cohort who visited a page with the Messenger widget, what % initiated a chatbot conversation? Pass: ≥50%.
- **AI resolution rate**: Of conversations started, what % were resolved by Fin without human handoff? Pass: ≥30%.
- **CSAT**: Average satisfaction rating for AI-resolved conversations. Minimum acceptable: ≥3.5/5.

If PASS on all three, proceed to Baseline. If engagement is low, the chatbot may not be visible enough — check Messenger placement and proactive triggers. If resolution rate is low, audit the top escalation topics and add knowledge base content. If CSAT is low, review AI-resolved conversations for incorrect answers.

## Time Estimate

- 1.5 hours: audit knowledge base and write missing articles
- 1.5 hours: deploy Fin AI, configure escalation rules, instrument tracking
- 0.5 hours: set up feature flag and launch test cohort
- 1 hour: daily monitoring (10 min/day for 7 days)
- 0.5 hours: evaluate metrics and document findings

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Intercom (Essential) | Messenger + Fin AI agent | $29/seat/mo base + $0.99/resolution — [intercom.com/pricing](https://www.intercom.com/pricing) |
| PostHog | Event tracking, feature flags, funnels | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |

**Estimated cost for Smoke: Free–$80** (Intercom Essential $29 + ~$50 in Fin resolutions for a small test cohort; PostHog free tier)

## Drills Referenced

- the ai chatbot deployment workflow (see instructions below) — deploys Fin AI, connects knowledge sources, instruments tracking, launches behind feature flag
- `threshold-engine` — evaluates engagement rate, resolution rate, and CSAT against pass thresholds
