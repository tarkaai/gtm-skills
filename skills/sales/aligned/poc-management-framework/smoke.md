---
name: poc-management-framework-smoke
description: >
  POC Management Framework — Smoke Test. Run a structured proof-of-concept on your
  first 5 deals with defined success criteria, milestones, stakeholder alignment, and
  decision frameworks to validate that managed POCs accelerate close decisions.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Product, Email"
level: "Smoke Test"
time: "10 hours over 2 weeks"
outcome: "Structured POCs completed on ≥5 opportunities in 2 weeks with ≥60% meeting success criteria and progressing to proposal"
kpis: ["POC completion rate", "Success criteria achievement rate", "POC-to-proposal conversion", "Time from POC to decision"]
slug: "poc-management-framework"
install: "npx gtm-skills add sales/aligned/poc-management-framework"
drills:
  - poc-scoping-workshop
  - threshold-engine
---

# POC Management Framework — Smoke Test

> **Stage:** Sales > Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product, Email

## Outcomes

Run structured POCs on at least 5 aligned deals in 2 weeks. Each POC has defined success criteria, a milestone schedule, named stakeholders, and a decision framework. At least 60% of completed POCs meet their success criteria and progress to a proposal.

## Leading Indicators

- POC success criteria documents created for each deal within 24 hours of deciding to POC
- Champion and economic buyer identified and named in every POC plan
- Kickoff calls scheduled and completed within 48 hours of scoping
- Prospects logging into sandbox within 24 hours of receiving access
- At least 1 milestone achieved per POC within the first 3 days

## Instructions

### 1. Identify 5-6 deals that need a POC

Review your Attio pipeline for deals at the Aligned stage where the prospect requires hands-on evaluation before committing. Pull the deal list using the `attio-deals` fundamental. Select deals where:
- Discovery call is completed (Fireflies transcript exists)
- Champion is identified
- Prospect has expressed interest in trying the product
- Deal value justifies a managed POC (vs. self-service trial)

### 2. Scope each POC

For each deal, run the `poc-scoping-workshop` drill. This extracts discovery context from Fireflies transcripts, generates a structured POC success criteria document using Claude, maps stakeholders, determines POC duration, and schedules the kickoff call.

Review each generated success criteria document before sending to the prospect. Verify:
- Every must-have criterion maps to a stated pain point from discovery
- Targets are specific and measurable (contains a number or binary threshold)
- Milestones are achievable within the timeline
- The decision maker and decision date are explicitly named

**Human action required:** Review and approve each POC success criteria document before sharing with the prospect. Adjust criteria based on your product knowledge and relationship context.

### 3. Provision and configure POC environments

For each POC, provision a sandbox using the `sandbox-environment-provision` fundamental. Configure it with prospect-specific data and instrumentation using the `poc-environment-configuration` fundamental. Ensure:
- Sample data matches the prospect's industry and use cases
- Success criteria tracking events are instrumented in PostHog
- Milestone tracking events fire correctly
- Check-in calls are scheduled in Cal.com

### 4. Run the kickoff calls

**Human action required:** Lead each POC kickoff call. Use the agenda from the scoping workshop output:
- Review and confirm success criteria with the prospect (10 min)
- Walk through the POC environment and sample data (15 min)
- Confirm the milestone schedule and check-in cadence (10 min)
- Identify potential blockers and assign owners (10 min)

After each kickoff, fire a `poc_kickoff_completed` PostHog event with the deal ID.

### 5. Monitor POC progress manually

During the 2-week window, check each POC daily:
- Review PostHog for sandbox login events and feature usage
- Check criterion progress (any `poc_criterion_met` events?)
- Review milestone status (on-track or behind?)
- Note blockers and address them directly

Log observations in Attio as notes on each deal. This manual monitoring will inform what to automate at the Baseline level.

### 6. Conduct mid-point and final review calls

**Human action required:** Run the scheduled check-in calls:
- **Mid-point review**: Review criteria progress, address blockers, adjust scope if needed
- **Final review**: Present results criterion-by-criterion, discuss decision, propose next steps

After each completed POC, update the deal in Attio with: `poc_result` (pass/fail), `poc_criteria_met_count`, `poc_decision` (proceed/decline/extend).

### 7. Evaluate against threshold

Run the `threshold-engine` drill to evaluate results against the pass threshold: structured POCs completed on 5+ opportunities in 2 weeks with 60%+ meeting success criteria and progressing to proposal.

The threshold engine pulls data from Attio and PostHog, compares against targets, and returns PASS or FAIL.

If PASS, document what worked (which POC structures, criteria, and durations produced the best results) and proceed to Baseline.
If FAIL, diagnose: Was the issue scoping (criteria too ambitious), execution (prospects not engaging), or qualification (wrong deals selected for POC)?

## Time Estimate

- POC scoping per deal: 45 min (agent-assisted) + 15 min human review = 1 hour
- Environment provisioning per deal: 30 min
- Kickoff call per deal: 45 min
- Daily monitoring (all POCs): 15 min/day x 10 days = 2.5 hours
- Check-in calls: 30 min each x 2 per deal = 1 hour/deal
- Total: ~10 hours over 2 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal tracking, POC metadata, stakeholder mapping | Free tier available; Pro from $29/user/mo |
| PostHog | POC event tracking, criterion/milestone events | Free up to 1M events/mo |
| Fireflies | Discovery call transcripts, action item extraction | Free tier (limited); Pro $10/user/mo |
| Cal.com | POC kickoff and check-in scheduling | Free tier available; Team from $12/user/mo |
| Anthropic API | Success criteria generation | ~$0.50-2.00 per POC scoping |

## Drills Referenced

- `poc-scoping-workshop` — generates POC success criteria, milestones, stakeholder map, and decision framework from discovery data
- `threshold-engine` — evaluates POC results against pass/fail threshold
