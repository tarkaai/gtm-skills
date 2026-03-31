---
name: sandbox-environment-demo-scalable
description: >
  Sandbox Environment Demo — Scalable Automation. Auto-provision personalized sandboxes when
  deals reach Connected stage, with AI-generated configurations, A/B-tested onboarding, and
  predictive engagement scoring across 75%+ of qualified opportunities for 2 months.
stage: "Sales > Connected"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Scalable Automation"
time: "65 hours over 2 months"
outcome: "Automated sandboxes on ≥75% of qualified opportunities at scale over 2 months with ≥60% active usage rate and sandbox-to-close conversion ≥45%"
kpis: ["Sandbox provisioning automation rate", "Auto-provisioning success rate (>95%)", "Active usage rate", "Engagement score", "Sandbox-to-close conversion", "Deal velocity improvement"]
slug: "sandbox-environment-demo"
install: "npx gtm-skills add sales/connected/sandbox-environment-demo"
drills:
  - ab-test-orchestrator
---

# Sandbox Environment Demo — Scalable Automation

> **Stage:** Sales → Connected | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Automated sandbox provisioning fires for 75% or more of qualified opportunities with zero manual intervention for standard deals. Auto-provisioning success rate exceeds 95%. Active usage rate holds at 60% or above (no regression from Baseline). Sandbox-to-close conversion rate reaches 45% or higher. This proves the sandbox program scales without proportional effort.

## Leading Indicators

- Auto-provisioning success rate per week (target: >95%, track failure reasons)
- Time from deal reaching Connected to sandbox access email sent (target: <5 minutes)
- A/B test velocity (at least 1 experiment running at all times)
- Personalization quality score (track whether AI-configured sandboxes outperform generic ones)
- Engagement score distribution shift (more prospects in Hot/Champion tiers vs. Baseline period)

## Instructions

### 1. Deploy automated sandbox provisioning

Run the the sandbox auto provisioning workflow (see instructions below) drill to build the n8n workflow that fires when a deal reaches Connected stage in Attio:

1. **CRM trigger**: Configure the Attio webhook that fires on stage change to Connected.
2. **Context enrichment**: n8n calls Clay to enrich the prospect's company (industry, size, tech stack) and pulls discovery notes from Attio. Claude analyzes the combined context and selects the optimal sandbox persona, feature highlights, and success checklist.
3. **Auto-provision**: n8n calls the sandbox provisioning endpoint with the AI-determined configuration. Verify success, update Attio with sandbox metadata.
4. **Personalized kickoff**: Claude generates a personalized kickoff email body referencing the prospect's specific pain points and use cases. n8n sends via Loops with the sandbox URL, checklist, walkthrough video, and Cal.com link.
5. **Error handling**: Failed provisions retry once, then alert the deal owner with error details. Duplicate requests are caught (skip if sandbox already exists). Enterprise deals (>$50K or >500 employees) route to manual provisioning for custom configuration.

Validate the end-to-end flow by pushing 3-5 test deals through the pipeline and confirming sandboxes are provisioned, emails sent, and Attio updated within 60 seconds.

### 2. Run A/B tests on sandbox onboarding

Run the `ab-test-orchestrator` drill to systematically test sandbox experience variants:

**Experiment 1: Sample data personalization**
- Control: Generic sample data persona for all prospects
- Variant: AI-selected industry-matched persona based on Clay enrichment
- Primary metric: Milestone completion rate within 7 days
- Expected duration: 4 weeks (minimum 50 sandboxes per variant)

**Experiment 2: Kickoff email format**
- Control: Template email with placeholders filled
- Variant: Fully AI-generated personalized email referencing discovery pain points
- Primary metric: First login rate within 24 hours
- Expected duration: 4 weeks

**Experiment 3: Success checklist length**
- Control: 5-item success checklist
- Variant: 3-item focused checklist (only the most predictive milestones)
- Primary metric: Checklist completion rate
- Expected duration: 3 weeks

Use PostHog feature flags to allocate prospects to variants. Run one experiment at a time to avoid confounding results. Implement winners permanently before starting the next experiment.

### 3. Build predictive engagement scoring

Extend the engagement scoring model from Baseline with predictive capabilities:

1. Pull historical data: all closed sandbox deals (won and lost) with their complete usage event histories from PostHog.
2. Identify the 3-5 usage signals that most strongly predict close (e.g., "uploaded own data within 5 days", "completed 3+ workflows", "3+ sessions in first week").
3. Build a scoring model that weights these signals and produces a close probability for each active sandbox.
4. Update close probabilities in Attio daily via n8n. Flag deals where probability changed significantly (>15 points in either direction).
5. Alert deal owners when a sandbox crosses from "Needs attention" to "Likely to close" or vice versa.

### 4. Implement smart intervention timing

Replace the fixed-schedule interventions from Baseline with data-driven timing:

1. Analyze which intervention timings produced the best outcomes in Baseline (e.g., did the 48-hour reminder work better than a 24-hour reminder?).
2. Configure n8n to send interventions at optimal times based on prospect behavior:
   - If prospect logged in and used 1 feature but stopped → wait 4 hours, then send "Here's what to try next" targeting the feature most correlated with conversion.
   - If prospect completed 2+ milestones in one session → send congratulations within 1 hour with a Cal.com link.
   - If prospect's engagement score starts declining after initial engagement → trigger re-engagement within 24 hours of the score drop.

### 5. Build the scaling dashboard

Create a PostHog dashboard tracking the program at scale:

- Auto-provisioning volume and success rate (weekly trend)
- Average time from deal stage change to sandbox access sent
- A/B test results (running and completed experiments)
- Close probability distribution across active sandboxes
- Sandbox-to-close conversion rate (weekly cohorts)
- Deal velocity: average days from sandbox provision to proposal for sandbox vs. non-sandbox deals
- ROI: incremental revenue attributable to sandbox program (sandbox deal close rate vs. non-sandbox)

### 6. Set guardrails and evaluate

Define guardrails that trigger alerts if breached:

- Active usage rate drops below 55% for 2 consecutive weeks (regressed from Baseline)
- Sandbox-to-close conversion drops below 40% (below target)
- Auto-provisioning failure rate exceeds 10% (infrastructure issue)
- Average time to sandbox access exceeds 5 minutes (pipeline bottleneck)

Evaluate against the pass threshold after 2 months:

- **Primary**: Automated sandboxes on ≥75% of qualified opportunities
- **Secondary**: Active usage rate ≥60%
- **Tertiary**: Sandbox-to-close conversion ≥45%

If PASS, proceed to Durable. If FAIL, diagnose: is it a provisioning problem (low automation rate), an engagement problem (low usage), or a conversion problem (usage doesn't predict closes)? Fix the weakest link and extend the Scalable run.

## Time Estimate

- 20 hours: Build and validate auto-provisioning workflow (n8n, Attio trigger, Clay enrichment, AI config, Loops send)
- 15 hours: Set up and run 3 A/B experiments over 2 months
- 15 hours: Build predictive scoring model and smart intervention timing
- 10 hours: Dashboard, guardrails, and ongoing monitoring
- 5 hours: Threshold evaluation and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loom | Walkthrough videos (default + industry-specific) | $12.50/creator/mo (Business, annual) — [loom.com/pricing](https://www.loom.com/pricing) |
| Loops | Kickoff emails, intervention sequences at scale | $49/mo (paid plan, unlimited sends) — [loops.so/pricing](https://loops.so/pricing) |
| Intercom | In-app messages and contextual guidance in sandboxes | $29/seat/mo (Essential) to $85/seat/mo (Advanced for automation) — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Clay | Prospect company and contact enrichment for AI config | ~$150-350/mo depending on volume — [clay.com/pricing](https://www.clay.com/pricing) |
| Anthropic API | AI-generated sandbox configs and personalized emails | ~$20-50/mo at this volume — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost:** ~$260-550/mo (Loops + Intercom + Clay + Anthropic + Loom)

_CRM (Attio), analytics (PostHog), and automation (n8n) are standard stack — not included in play budget._

## Drills Referenced

- the sandbox auto provisioning workflow (see instructions below) — builds the n8n workflow that auto-provisions sandboxes on CRM stage change with AI-personalized configuration, error handling, and edge case routing
- `ab-test-orchestrator` — designs, runs, and analyzes A/B tests on sandbox onboarding variants using PostHog experiments
