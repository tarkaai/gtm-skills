---
name: poc-management-framework-scalable
description: >
  POC Management Framework — Scalable Automation. Predictive POC health monitoring
  across a portfolio of 15-25+ concurrent POCs with automated risk scoring,
  targeted interventions, and auto-provisioning.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Product, Email"
level: "Scalable Automation"
time: "68 hours over 2 months"
outcome: "POCs on ≥75% of qualified opportunities at scale over 2 months with ≥55% close rate and predictive risk scoring in place"
kpis: ["POC completion rate", "Success criteria achievement rate", "POC-to-close conversion", "Average POC duration", "Intervention effectiveness rate"]
slug: "poc-management-framework"
install: "npx gtm-skills add sales/aligned/poc-management-framework"
drills:
  - sandbox-auto-provisioning
---

# POC Management Framework — Scalable Automation

> **Stage:** Sales > Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product, Email

## Outcomes

A single rep manages 15-25+ concurrent POCs without losing visibility into any of them. Sandbox provisioning is fully automated. Every POC has a real-time risk score updated daily. Automated interventions fire when POCs go off-track. A portfolio dashboard shows the health of all active POCs at a glance. Target: POCs on 75%+ of qualified opportunities with 55%+ close rate.

## Leading Indicators

- Auto-provisioned sandboxes ready within 60 seconds of deal qualifying
- Predictive risk scores updating daily for every active POC
- Automated interventions triggering within 6 hours of risk signal detection
- Intervention effectiveness rate above 40% (prospect re-engages within 48 hours)
- Weekly portfolio brief generating with actionable per-deal recommendations
- Risk score Green-to-Yellow transitions detected within 24 hours

## Instructions

### 1. Deploy auto-provisioning

Run the `sandbox-auto-provisioning` drill. This builds an n8n workflow that:

1. Triggers when a deal reaches Aligned and passes POC qualification.
2. Enriches the prospect context via Clay (industry, company size, tech stack, funding stage).
3. Calls Claude to select the optimal sandbox configuration: sample data persona, features to highlight, success checklist items.
4. Provisions the sandbox via the product API.
5. Generates a personalized kickoff email via Claude.
6. Sends access via Loops with the custom email body, sandbox URL, and Cal.com kickoff link.
7. A/B tests sandbox configurations: industry-matched vs. generic data, personalized vs. template kickoff email, 3 vs. 5 success checklist items.

The workflow should handle edge cases: missing discovery data (provision with generic persona and alert deal owner), duplicate sandboxes (skip and send reminder), enterprise deals over $50K (route to manual provisioning).

Verify the auto-provisioning success rate exceeds 95% by checking the n8n execution logs after the first 2 weeks.

### 2. Deploy POC health monitoring

Run the the poc health monitoring workflow (see instructions below) drill. This builds the real-time monitoring layer:

**Portfolio dashboard:** A single PostHog dashboard showing all active POCs by health status, criteria progress matrix, engagement trends, conversion funnel, and intervention effectiveness.

**Predictive risk model:** An n8n workflow that runs daily and:
- Pulls historical POC outcome data from PostHog (won vs. lost cohorts)
- Identifies the behavioral signals that predict success vs. failure (time to first login, session count, criterion velocity, own data upload, engagement trajectory)
- Scores every active POC against these signals (0-100 risk score)
- Classifies each POC: Green (low risk), Yellow (moderate risk), Red (high risk)
- Updates the risk score and classification in Attio

**Automated interventions:** n8n workflows that fire on specific risk signals:
- No login within 24 hours: In-app message + email with walkthrough
- Declining engagement: Alert deal owner with session data
- Milestone behind by 3+ days: Targeted help email with Cal.com booking
- Green-to-Yellow transition: Deal owner alert with recommended action
- Yellow-to-Red transition: Escalate to deal owner AND manager

**Intervention tracking:** Every intervention fires a PostHog event. Track whether the intervention produced a response within 48 hours. Feed effectiveness data back into intervention selection.

### 3. Scale POC volume

Increase concurrent POCs from the Baseline level (5-10) to 15-25+:

1. Ensure auto-provisioning handles the volume without queuing delays.
2. Verify the daily risk scoring workflow completes for all active POCs within its cron window.
3. Confirm milestone check-in emails scale without Loops rate limit issues.
4. Check that Slack alert volume does not cause alert fatigue. If more than 5 alerts/day, consolidate into a daily digest.

### 4. Optimize POC configurations based on data

After 4 weeks of scaled operation:

1. Pull A/B test results from PostHog for sandbox configuration experiments.
2. Identify winning variants: which data persona, email style, and checklist length produce highest first-login rates and criterion completion.
3. Promote winning variants as defaults. Start new experiments on the next variable.
4. Analyze POC duration impact: calculate win rate by duration and deal segment. If shorter POCs close at the same rate, reduce default duration to compress the sales cycle.

### 5. Set guardrails

Configure n8n workflows to enforce:
- **POC completion rate guardrail**: If completion rate drops below 75% of Baseline level for 2 consecutive weeks, alert and diagnose.
- **POC-to-close conversion guardrail**: If conversion drops below 45%, pause new POC starts and investigate root cause (criteria too easy? wrong deals qualifying?).
- **Intervention volume guardrail**: If Red-classified POCs exceed 30% of active portfolio, escalate to leadership. The issue is systemic, not per-deal.

### 6. Evaluate against threshold

After 2 months:
- Calculate: POC qualification rate, completion rate, criteria achievement rate, close rate, average duration, intervention effectiveness
- Compare against: 75% of qualified opportunities running POCs, 55% close rate, predictive scoring operational
- Evaluate portfolio management capacity: can one rep effectively manage 20+ concurrent POCs with this system?

If PASS, proceed to Durable. If FAIL, focus on the weakest metric: if close rate is low, refine criteria; if completion rate is low, improve interventions; if qualification is low, adjust the qualification workflow.

## Time Estimate

- Auto-provisioning setup: 12 hours
- Health monitoring deployment: 16 hours
- Scaling and testing: 8 hours
- A/B test analysis and optimization: 8 hours
- Weekly monitoring and adjustments: 3 hours/week x 8 weeks = 24 hours
- Total: ~68 hours over 2 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM, deal tracking, risk scores, stakeholder data | Pro from $29/user/mo |
| PostHog | Event tracking, dashboards, A/B tests, cohort analysis | Free up to 1M events/mo; Growth for experiments |
| n8n | Auto-provisioning, health monitoring, interventions | Cloud from $24/mo; self-hosted free |
| Clay | Prospect enrichment for auto-provisioning | Explorer from $149/mo |
| Loops | Check-in sequences, intervention emails | Starter from $49/mo |
| Intercom | In-app messages during sandbox usage | Starter from $39/mo |
| Cal.com | Check-in and kickoff scheduling | Team from $12/user/mo |
| Anthropic API | Sandbox config, email generation, risk analysis | ~$5-15/mo at this volume |

## Drills Referenced

- the poc health monitoring workflow (see instructions below) — real-time portfolio monitoring with predictive risk scoring, automated interventions, and weekly briefs
- `sandbox-auto-provisioning` — fully automated sandbox provisioning triggered by CRM stage changes with AI-personalized configuration
