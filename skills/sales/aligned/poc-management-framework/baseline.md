---
name: poc-management-framework-baseline
description: >
  POC Management Framework — Baseline Run. First always-on POC management automation:
  qualification workflows, milestone check-in sequences, blocker escalation, and daily
  progress tracking across all active POCs.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Product, Email"
level: "Baseline Run"
time: "24 hours over 4 weeks"
outcome: "POCs running on ≥80% of qualified opportunities over 4 weeks with ≥65% achieving success criteria and ≥50% converting to closed-won"
kpis: ["POC qualification accuracy", "Success criteria achievement rate", "POC-to-close conversion", "Time from POC to decision", "POC engagement score"]
slug: "poc-management-framework"
install: "npx gtm-skills add sales/aligned/poc-management-framework"
drills:
  - poc-governance-automation
  - posthog-gtm-events
---

# POC Management Framework — Baseline Run

> **Stage:** Sales > Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product, Email

## Outcomes

POC governance runs as always-on automation. Deals are auto-qualified for POC, check-in emails fire on schedule, blockers escalate automatically, and every POC's health status is visible in the CRM daily. Target: POCs running on 80%+ of qualified opportunities with 65%+ achieving success criteria and 50%+ converting to closed-won.

## Leading Indicators

- POC qualification workflow fires within 1 hour of deal reaching Aligned stage
- 90%+ of POC milestone check-in emails send on schedule
- Blocker escalation triggers within 6 hours of detection
- Daily CRM updates show accurate POC health status for every active POC
- POC completion email with results summary sends within 24 hours of POC end date

## Instructions

### 1. Establish the POC event taxonomy

Run the `posthog-gtm-events` drill to define and implement the POC-specific event taxonomy in PostHog. Configure these events:

- `poc_qualified` — deal assessed for POC eligibility
- `poc_scoped` — success criteria document generated
- `poc_kickoff_completed` — kickoff call finished
- `poc_criterion_met` — individual criterion achieved
- `poc_milestone_achieved` — milestone completed
- `poc_blocker_identified` — blocker detected
- `poc_checkin_sent` — check-in email delivered
- `poc_intervention_triggered` — automated intervention fired
- `poc_health_updated` — daily health status synced to CRM
- `poc_completed` — POC reached end date with results

Each event must carry `deal_id`, `company_name`, `poc_duration_days`, and event-specific properties. Build PostHog funnels for the core POC flow: `poc_scoped` -> `poc_kickoff_completed` -> `poc_milestone_achieved` (3+) -> `poc_completed` (pass).

### 2. Deploy POC governance automation

Run the `poc-governance-automation` drill. This builds 5 n8n workflows:

**Qualification workflow:** When a deal moves to Aligned in Attio, auto-assess POC eligibility. Check: discovery completed, champion identified, deal value above threshold. Route by priority: high-priority deals get auto-provisioned, medium gets an alert, low gets a self-service trial link.

**Milestone check-in sequence:** Loops sends check-in emails at key POC moments: 48 hours after kickoff (milestone 1 reminder), mid-point review invite, 48 hours before end (final status), and post-completion results summary. Each email references the specific POC's criteria and progress.

**Blocker escalation workflow:** n8n monitors for risk signals every 6 hours: no login after 48 hours, milestone missed by 2+ days, error spikes, champion silence for 5+ days. Each blocker triggers a specific intervention and updates the deal in Attio.

**Daily progress tracker:** n8n runs daily and syncs each active POC's status to Attio: criteria met count, milestones achieved, days remaining, health classification (on-track / at-risk / stalled).

**Completion workflow:** When a POC reaches its end date, auto-generate a results summary, email it to the champion, and update the deal stage based on outcome.

### 3. Standardize POC templates by segment

Based on Smoke test learnings, create standardized POC configurations for your most common deal segments:

1. Pull Smoke test results from Attio: which success criteria, durations, and milestone structures produced the best outcomes.
2. Create 2-3 POC templates stored as reusable configurations:
   - **Quick evaluation** (7 days, 3 criteria): For deals $5K-15K where the prospect needs basic validation
   - **Standard POC** (14 days, 5 criteria): For deals $15K-50K with integration requirements
   - **Enterprise POC** (21 days, 5+ criteria): For deals $50K+ with security review and multiple stakeholders
3. Store templates in Attio as reference notes. The `poc-scoping-workshop` drill should select the appropriate template based on deal characteristics and customize from there.

### 4. Monitor automation health

Check weekly:
- Are qualification workflows firing reliably? (Check n8n execution logs for errors)
- Are check-in emails sending on schedule? (Check Loops delivery reports)
- Are blocker escalations reaching the right people? (Check Slack message logs)
- Is the daily progress tracker updating Attio accurately? (Spot-check 3 deals)

Fix any automation failures immediately. A missed blocker escalation can cost a deal.

### 5. Evaluate against threshold

After 4 weeks, run the threshold evaluation:
- Pull all POC deals from Attio with their outcomes
- Calculate: qualification rate, criteria achievement rate, POC-to-close conversion rate
- Compare against: 80% of qualified opportunities running POCs, 65% achieving criteria, 50% converting to closed-won

If PASS, document the POC template performance data and proceed to Scalable.
If FAIL, diagnose: Is the qualification workflow too permissive (running POCs on wrong deals)? Are criteria too aggressive? Is the support model insufficient?

## Time Estimate

- Event taxonomy setup: 3 hours
- n8n workflow building: 8 hours (5 workflows)
- POC template creation: 2 hours
- Weekly monitoring and fixes: 2 hours/week x 4 weeks = 8 hours
- Threshold evaluation: 3 hours
- Total: ~24 hours over 4 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM deal tracking, POC metadata, health status | Pro from $29/user/mo |
| PostHog | POC event tracking, funnels, engagement data | Free up to 1M events/mo |
| n8n | POC governance workflows (qualification, tracking, escalation) | Free self-hosted; Cloud from $24/mo |
| Loops | Milestone check-in email sequences | Free up to 1,000 contacts; Starter from $49/mo |
| Cal.com | Check-in call scheduling | Free tier; Team from $12/user/mo |
| Anthropic API | Results summary generation | ~$1-3/mo at this volume |

## Drills Referenced

- `poc-governance-automation` — builds the 5 n8n workflows that automate POC qualification, check-ins, escalation, progress tracking, and completion
- `posthog-gtm-events` — defines and implements the POC event taxonomy in PostHog
