---
name: risk-assessment-discovery-baseline
description: >
  Risk & Concern Discovery -- Baseline Run. First always-on automation: every discovery call
  automatically triggers risk extraction, CRM logging, and mitigation content delivery. Covers
  35-50 opportunities over 2 weeks with risk severity scoring and automated mitigation matching.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Baseline Run"
time: "14 hours over 2 weeks"
outcome: "Risks identified and documented on >=80% of opportunities over 2 weeks with >=60% of high-severity risks mitigated before proposal"
kpis: ["Risk discovery rate across pipeline", "Risk mitigation success rate", "Close rate impact vs unassessed deals", "Late-stage surprise reduction"]
slug: "risk-assessment-discovery"
install: "npx gtm-skills add sales/connected/risk-assessment-discovery"
drills:
  - risk-discovery-call-prep
  - risk-discovery-call
  - risk-mitigation-delivery
  - posthog-gtm-events
---

# Risk & Concern Discovery -- Baseline Run

> **Stage:** Sales > Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Automated risk discovery pipeline running on every discovery call. Agent automatically prepares risk guides before calls, extracts risks from transcripts after calls, and delivers targeted mitigation content within 24 hours. Risk coverage across 80%+ of the pipeline. High-severity risks addressed before deals reach proposal stage.

## Leading Indicators

- Risk extraction runs automatically after every recorded call (no manual trigger needed)
- Mitigation content is delivered within 24 hours of risk identification
- Risk data is populated on 80%+ of active deals in Attio
- Prospects respond positively to mitigation content ("this addresses my concern")
- Fewer surprises at proposal stage compared to pre-play baseline
- Risk prediction accuracy (pre-call vs. actual) is trending upward

## Instructions

### 1. Configure automated call prep

Set up an n8n workflow that triggers `risk-discovery-call-prep` automatically when a Cal.com booking event fires for a discovery or evaluation call:

- Trigger: Cal.com webhook on new booking
- Filter: only calls tagged as "discovery," "evaluation," or "demo"
- Action: run the full prep drill -- enrich prospect, predict risks, generate question guide, store as Attio note
- Notify the caller via Slack: "Risk prep ready for {company_name} call tomorrow. Review: {attio_note_link}"

### 2. Configure automated post-call risk extraction

Set up an n8n workflow triggered by Fireflies transcript completion:

- Trigger: Fireflies webhook on transcript ready
- Match: transcript to Attio deal record by attendee email
- Action: run `risk-discovery-call` drill -- extract risks, score, compare to predictions, log to CRM
- Route: if unaddressed Medium+ risks detected, trigger step 3

### 3. Set up automated mitigation delivery

Connect the risk extraction output to the `risk-mitigation-delivery` drill:

- For each unaddressed risk with score >= 25 (Medium+), automatically match to mitigation content
- Draft a personalized email referencing the prospect's exact concern quotes
- Auto-send for Medium and High risks; queue for human review for Critical risks
- Schedule 3-day follow-up if no response

**Human action required:** Review and approve Critical-risk mitigation emails before sending. Build the initial mitigation content library: at minimum, one asset per risk category (ROI calculator for Financial, security doc for Technical, change management guide for Organizational, implementation timeline for Timeline, customer reference list for Vendor).

### 4. Configure comprehensive event tracking

Run the `posthog-gtm-events` drill to set up tracking for the full risk discovery funnel:

- `risk_prep_generated` -- pre-call question guide created
- `risk_discovery_call_completed` -- post-call extraction finished
- `risk_identified` -- individual risk logged (with category, severity, likelihood)
- `risk_mitigation_delivered` -- mitigation content sent to prospect
- `risk_mitigation_opened` -- prospect opened the mitigation email
- `risk_mitigation_asset_viewed` -- prospect clicked the asset link
- `risk_mitigation_resolved` -- risk marked as resolved
- `risk_mitigation_failed` -- prospect still concerned after mitigation attempt
- `deal_risk_level_changed` -- deal's overall risk level changed

Connect PostHog to Attio via webhook so deal risk updates flow bidirectionally.

### 5. Build a risk severity scoring rubric

Create a standardized rubric in Attio for consistent risk assessment:

| Likelihood \ Severity | Low (1-3) | Medium (4-6) | High (7-10) |
|----------------------|-----------|--------------|-------------|
| Low (1-3) | Accept (1-9) | Monitor (4-18) | Mitigate (7-30) |
| Medium (4-6) | Monitor (4-18) | Mitigate (16-36) | Escalate (28-60) |
| High (7-10) | Mitigate (7-30) | Escalate (28-60) | Block (49-100) |

Store this as a reference document. The agent uses it to auto-classify risks and route mitigations.

### 6. Execute for 2 weeks and monitor

Let the automation run. Monitor daily:
- Are transcripts being processed? (check n8n execution logs)
- Is risk data appearing on deal records? (spot-check 3-5 deals)
- Are mitigation emails being sent within 24 hours?
- Are prospects engaging with mitigation content? (check open/click rates)

Adjust mid-flight:
- If risk extraction is returning too many false positives, tighten the severity threshold
- If mitigation emails have low open rates, test subject lines
- If certain risk categories never appear, check if question guides are probing them

### 7. Evaluate against threshold

After 2 weeks, measure:
- Risk discovery coverage: >= 80% of opportunities have risk data logged
- High-severity mitigation rate: >= 60% of risks with score >= 50 have been mitigated before proposal stage
- Prediction accuracy: pre-call risk predictions vs. actual risks surfaced

If PASS, proceed to Scalable. If FAIL, diagnose: Is the issue automation failures (transcripts not processing), content gaps (no mitigation assets for common risks), or discovery quality (risks not being surfaced on calls)?

## Time Estimate

- Automation setup: 4 hours (n8n workflows for prep, extraction, mitigation delivery)
- Content library creation: 3 hours (one mitigation asset per risk category)
- Event tracking setup: 1.5 hours (PostHog events and Attio webhooks)
- Daily monitoring: 15 min/day x 10 business days = 2.5 hours
- Mitigation review for Critical risks: ~30 min/week x 2 weeks = 1 hour
- Threshold evaluation: 1 hour
- Buffer: 1 hour

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Fireflies | Call transcription (auto-join all calls) | Pro: $10/user/mo annual ([fireflies.ai/pricing](https://fireflies.ai/pricing)) |
| Clay | Prospect enrichment for risk prediction | Free or Launch: $185/mo ([clay.com/pricing](https://www.clay.com/pricing)) |
| Anthropic (Claude) | Risk extraction + mitigation matching | ~$3-8/mo at this volume ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| Instantly | Mitigation email delivery | Growth: $30/mo ([instantly.ai/pricing](https://instantly.ai/pricing)) |

**Total play-specific cost:** ~$40-225/mo depending on Clay tier

_Your CRM (Attio), PostHog, and automation platform (n8n) are standard stack -- not included._

## Drills Referenced

- `risk-discovery-call-prep` -- auto-generates per-call risk question guides (triggered by Cal.com booking)
- `risk-discovery-call` -- auto-processes post-call transcripts: extract risks, score, log, route
- `risk-mitigation-delivery` -- matches risks to content and delivers personalized mitigation emails
- `posthog-gtm-events` -- configures the full risk discovery event tracking funnel
