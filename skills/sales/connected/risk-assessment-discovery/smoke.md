---
name: risk-assessment-discovery-smoke
description: >
  Risk & Concern Discovery -- Smoke Test. Run structured risk probing on 8-10 discovery calls
  to surface Financial, Technical, Organizational, Timeline, and Vendor concerns. Agent prepares
  per-call risk question guides, human executes calls, agent extracts and logs risk data post-call.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "Risks identified and addressed with >=8 opportunities in 1 week with >=70% having documented mitigation plans"
kpis: ["Risk discovery completion rate", "High-severity risk identification count", "Mitigation plan creation rate", "Risk category distribution"]
slug: "risk-assessment-discovery"
install: "npx gtm-skills add sales/connected/risk-assessment-discovery"
drills:
  - risk-discovery-call-prep
  - risk-discovery-call
  - threshold-engine
---

# Risk & Concern Discovery -- Smoke Test

> **Stage:** Sales > Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Surface hidden risks, concerns, and implementation fears during 8-10 discovery calls. Each call should probe all five risk categories (Financial, Technical, Organizational, Timeline, Vendor). At least 70% of opportunities should have documented mitigation plans for every high-severity risk identified.

## Leading Indicators

- Risk questions are surfacing concerns the prospect would not have volunteered unprompted
- At least 2 risk categories are covered per call
- Prospects are sharing specific fears (not just "no concerns")
- Seller has mitigation responses ready for the most common risks
- Late-stage surprise rate begins to decline compared to deals without risk discovery

## Instructions

### 1. Prepare risk-probing question guides for upcoming calls

For each of your next 8-10 scheduled discovery calls, run the `risk-discovery-call-prep` drill. This will:
- Pull the deal context from Attio (company, contact, industry, deal value)
- Enrich the prospect via Clay (tech stack, recent news, org size, regulatory environment)
- Generate predicted risks by category using Claude
- Produce a structured risk-probing question guide stored as an Attio note

Do this 24 hours before each call so you have time to review the prep.

### 2. Execute risk discovery on each call

**Human action required:** Run the discovery calls. During each call, after initial pain discovery:

- Transition to risk probing: "I want to make sure we address any concerns upfront so nothing catches us off guard later."
- Use the universal openers first:
  - "What concerns do you have about making this change?"
  - "What would need to be true for you to feel confident this will succeed?"
  - "What has gone wrong with past vendor decisions?"
- Then probe the 2 predicted decision-blocking categories from the prep doc
- For each risk surfaced: acknowledge it, probe for severity ("On a scale of 1-10, how worried are you?"), and note whether it blocks the decision
- Capture exact quotes -- they power the mitigation messaging later
- Close: "Is there anything else that would prevent this from being successful?"

### 3. Process each call post-conversation

After each call, run the `risk-discovery-call` drill. This will:
- Retrieve the Fireflies transcript
- Extract all risks with category, severity, likelihood, and supporting quotes
- Score each risk (severity x likelihood)
- Compare actual risks against the pre-call predictions
- Log structured risk data to the Attio deal record
- Fire PostHog tracking events
- Route: flag high-risk deals for immediate follow-up, queue medium-risk for mitigation content

### 4. Address identified risks within 48 hours

For each high-severity risk (score >= 50), prepare a mitigation response manually:
- Financial risks: draft an ROI calculation or cost comparison
- Technical risks: prepare an integration architecture diagram or security documentation
- Organizational risks: share a change management case study or adoption timeline
- Timeline risks: provide a realistic implementation plan with milestones
- Vendor risks: offer a reference call with a similar customer

**Human action required:** Send the mitigation material to the prospect via email. Reference their exact words: "You mentioned you were concerned about [exact quote] -- here is how we address that."

### 5. Evaluate against threshold

Run the `threshold-engine` drill to evaluate results:
- Did you complete risk discovery on >= 8 opportunities this week?
- Do >= 70% have documented mitigation plans for all high-severity risks?
- Were risks logged in Attio with category, severity, and likelihood scores?

If PASS, proceed to Baseline. If FAIL, diagnose: Were risk questions too vague? Did prospects not open up? Were certain categories consistently missed? Adjust the question bank and re-run.

## Time Estimate

- Call prep: 15 min per call x 8-10 calls = 2-2.5 hours (agent does enrichment and question generation; human reviews)
- Risk probing during calls: 15-20 min per call (incremental time within existing discovery calls)
- Post-call processing: 10 min per call x 8-10 calls = 1.5 hours (agent extracts and logs)
- Mitigation prep: 15 min per high-severity risk (human drafts or selects content)
- Threshold evaluation: 15 min

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Fireflies | Call transcription and risk extraction | Free plan: 800 min/mo; Pro: $10/user/mo annual ([fireflies.ai/pricing](https://fireflies.ai/pricing)) |
| Clay | Prospect enrichment for risk prediction | Free plan: 100 credits/mo ([clay.com/pricing](https://www.clay.com/pricing)) |
| Anthropic (Claude) | Risk extraction from transcripts, question generation | Pay-per-use, ~$0.01-0.05 per call extraction ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |

**Total play-specific cost:** Free (using free tiers of Fireflies and Clay, minimal Claude API usage)

_Your CRM (Attio), PostHog, and automation platform (n8n) are standard stack -- not included._

## Drills Referenced

- `risk-discovery-call-prep` -- generates per-call risk-probing question guides from enrichment data
- `risk-discovery-call` -- post-call processing: extract risks, score, log to CRM, route mitigations
- `threshold-engine` -- evaluates pass/fail against the 8-opportunity, 70%-mitigation threshold
