---
name: risk-assessment-discovery-scalable
description: >
  Risk & Concern Discovery -- Scalable Automation. 10x multiplier via continuous risk monitoring
  across all deal activity (not just discovery calls), predictive risk scoring per deal, pattern
  analysis across the pipeline, and automated mitigation content library expansion.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Scalable Automation"
time: "57 hours over 2 months"
outcome: "Risks discovered and mitigated on >=75% of opportunities at scale over 2 months with late-stage surprise rate <10%"
kpis: ["Risk discovery rate at scale", "Early risk identification rate (before proposal)", "Mitigation success rate", "Close rate improvement vs pre-play baseline", "Deal predictability score"]
slug: "risk-assessment-discovery"
install: "npx gtm-skills add sales/connected/risk-assessment-discovery"
drills:
  - risk-intelligence-monitor
  - risk-pattern-analysis
  - risk-mitigation-delivery
---

# Risk & Concern Discovery -- Scalable Automation

> **Stage:** Sales > Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Risk monitoring expands from discovery calls only to the entire deal lifecycle. Every call transcript, email exchange, and CRM update is scanned for risk signals. Predictive risk scoring flags at-risk deals before problems surface. Pattern analysis across the pipeline identifies which risks kill deals, which mitigations work, and where the content library has gaps. The 10x multiplier: risks are caught from all touchpoints (not just dedicated risk calls) and mitigations are delivered proactively based on predicted risks, not just discovered ones.

## Leading Indicators

- Risk signals are detected from demo calls, technical deep-dives, and email threads (not just discovery calls)
- Predictive risk scores correlate with actual deal outcomes (Red deals lose more often than Green)
- Late-stage surprise rate drops below 10% (surprises = risks first surfaced at proposal/negotiation stage)
- Mitigation content library is expanding based on gap analysis (content created for the most common unmitigatable risks)
- Risk prediction accuracy improves month-over-month (as pattern data accumulates)
- Close rate on risk-assessed deals exceeds close rate on unassessed deals by a measurable margin

## Instructions

### 1. Deploy the always-on risk intelligence monitor

Run the `risk-intelligence-monitor` drill to create three n8n workflows:

**Transcript scanner:** Fireflies webhook triggers risk extraction on ALL sales calls (not just discovery). The scanner compares new risks against existing risk data per deal and detects: new risks, escalated risks, and resolved risks. Alerts fire immediately for new Critical risks and risk escalations.

**Email scanner:** Attio webhook triggers on new email activity logged to a deal. Claude analyzes the email body for risk signals, hesitation language, competitor mentions, and disengagement patterns. Results feed into the same risk delta calculation and alert routing.

**Predictive scorer:** Daily n8n cron workflow scores every open deal's risk likelihood based on:
- Historical risk patterns for this segment (from pattern analysis)
- Deal age vs. average cycle time
- Number of stakeholders engaged (single-thread risk)
- Days since last activity (going dark risk)
- Pain-to-price ratio (weak value foundation risk)
- Champion identification status
- Existing unaddressed risks

Deals are classified Green (0-30), Yellow (31-60), Red (61+). Red deals get immediate Slack alerts.

### 2. Launch bi-weekly risk pattern analysis

Run the `risk-pattern-analysis` drill on a bi-weekly n8n schedule. This aggregates risk data across all deals and produces:

- **Risk frequency matrix:** Which categories appear most often, by segment
- **Mitigation effectiveness report:** Which assets resolve risks fastest, which have low success rates
- **Risk-to-loss pathway:** For lost deals, was the fatal risk discovered early or late? Was mitigation attempted?
- **Prediction accuracy tracking:** Pre-call predictions vs. actual risks, trending over time
- **Content gap analysis:** Which risk categories lack effective mitigation assets

Use the output to:
- Update the risk prediction prompts in `risk-discovery-call-prep` with new segment-specific risk patterns
- Prioritize mitigation content creation for the highest-frequency, lowest-success-rate gaps
- Refine the question bank: retire questions with low surface rates, add questions for underprobed categories

### 3. Scale the mitigation content library

Based on pattern analysis gaps, systematically build mitigation assets:

- **Financial:** ROI calculator, TCO comparison, payment flexibility options, money-back guarantee terms
- **Technical:** Security whitepaper, SOC2/compliance documentation, integration architecture diagrams, migration playbooks, uptime SLA
- **Organizational:** Change management case studies, adoption timeline examples, training plan templates, internal champion toolkit
- **Timeline:** Implementation plan with milestones, phased rollout options, quick-win examples
- **Vendor:** Customer reference list (segmented by industry/size), product roadmap summary, support SLA documentation, company stability metrics

**Human action required:** Create 2-3 mitigation assets per category. The agent can draft outlines, but humans must validate accuracy, especially for security docs and legal commitments.

The `risk-mitigation-delivery` drill uses this expanded library to improve match quality and fill gaps.

### 4. Build the daily risk digest

Configure the `risk-intelligence-monitor` daily digest:
- Aggregates all risk events from the last 24 hours
- Groups by deal: new risks, escalations, resolutions
- Lists all Red deals with predictive scores and top risk factors
- Reports overall pipeline risk posture: total unaddressed Critical risks, average mitigation coverage

Post to a dedicated Slack channel. The founder reviews the digest each morning to prioritize which deals need attention.

### 5. Set guardrails

- **Late-stage surprise rate:** Track risks first surfaced at proposal or later vs. total risks. Must stay below 10%. If it rises, the discovery process is missing risks.
- **Mitigation response time:** 24-hour SLA for Medium+ risks. Track via PostHog: `hours_between_risk_identified_and_mitigation_sent`. Alert if SLA is missed.
- **False positive rate:** Track risk alerts where no actual risk existed. If above 20%, tighten extraction thresholds.
- **Coverage floor:** Risk data must exist on >= 75% of pipeline deals. If coverage drops, check for automation failures.

### 6. Evaluate at 2 months

Measure against threshold:
- Risk discovery rate: >= 75% of opportunities have risk data (from any source: calls, emails, predictive)
- Late-stage surprise rate: < 10% of risks first appear at proposal or later
- Close rate impact: compare close rate on risk-assessed deals vs. historical baseline (pre-play)
- Deal predictability: Red-scored deals should lose at >= 2x the rate of Green-scored deals

If PASS and metrics hold for 4+ consecutive weeks, proceed to Durable. If FAIL, focus on the weakest metric: coverage (automation issues), late-stage surprises (discovery gaps), or prediction accuracy (model needs more data).

## Time Estimate

- Risk intelligence monitor setup: 8 hours (3 n8n workflows: transcript, email, predictive)
- Pattern analysis configuration: 4 hours (bi-weekly cron, report generation)
- Content library expansion: 16 hours (2-3 assets x 5 categories, human creation with agent drafts)
- Daily digest setup: 2 hours (aggregation workflow + Slack integration)
- Guardrail configuration: 3 hours (PostHog alerts + n8n monitors)
- Ongoing monitoring: 2 hours/week x 8 weeks = 16 hours
- Pattern analysis review: 1 hour bi-weekly x 4 = 4 hours
- Evaluation: 2 hours
- Buffer: 2 hours

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Fireflies | Call transcription for all sales calls | Pro: $10/user/mo annual ([fireflies.ai/pricing](https://fireflies.ai/pricing)) |
| Clay | Prospect enrichment for risk prediction | Launch: $185/mo ([clay.com/pricing](https://www.clay.com/pricing)) |
| Anthropic (Claude) | Risk extraction, mitigation matching, pattern analysis | ~$15-40/mo at scale ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| Instantly | Mitigation email delivery at scale | Growth: $30/mo ([instantly.ai/pricing](https://instantly.ai/pricing)) |

**Total play-specific cost:** ~$240-465/mo

_Your CRM (Attio), PostHog, and automation platform (n8n) are standard stack -- not included._

## Drills Referenced

- `risk-intelligence-monitor` -- always-on scanning of transcripts, emails, and deal data for risk signals; predictive scoring; daily digest
- `risk-pattern-analysis` -- bi-weekly aggregation of risk data across pipeline; identifies patterns, mitigation effectiveness, and content gaps
- `risk-mitigation-delivery` -- automated matching and delivery of mitigation content (now using expanded library)
