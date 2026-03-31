---
name: poc-governance-automation
description: Automate POC qualification, check-in scheduling, milestone tracking emails, and blocker escalation via n8n workflows
category: Demos
tools:
  - n8n
  - Attio
  - PostHog
  - Loops
  - Cal.com
fundamentals:
  - n8n-triggers
  - n8n-workflow-basics
  - n8n-crm-integration
  - n8n-error-handling
  - attio-deals
  - attio-notes
  - attio-automation
  - attio-custom-attributes
  - posthog-custom-events
  - posthog-funnels
  - loops-sequences
  - loops-transactional
  - calcom-booking-links
  - calcom-crm-sync
---

# POC Governance Automation

This drill builds the always-on automation layer that governs active POCs: qualifying whether a deal should get a POC, sending milestone check-in emails, escalating blockers, and tracking POC progress in the CRM. It replaces manual POC management with structured workflows.

## Input

- Attio pipeline with deals at Aligned stage
- POC success criteria stored on deals (from `poc-scoping-workshop` drill)
- PostHog tracking configured for POC events
- n8n instance with Attio, Loops, and Cal.com integrations
- Loops account for automated email sequences

## Steps

### 1. Build the POC qualification workflow

Create an n8n workflow using `n8n-triggers` and `n8n-crm-integration` that fires when a deal moves to Aligned stage:

1. **Trigger**: Attio webhook on deal stage change to "Aligned."
2. **Check qualification criteria**:
   - Discovery call completed? (Check for Fireflies transcript linked to deal)
   - Champion identified? (Check `poc_champion` attribute)
   - Deal value above POC threshold? (Configurable; default: $5K+ ARR)
   - Competitor active? (Check deal notes for competitor mentions)
3. **Score the POC priority**:
   - High: Deal > $25K, competitor active, champion engaged
   - Medium: Deal $5K-$25K, champion identified
   - Low: Deal < $5K (recommend async trial instead of managed POC)
4. **Route the result**:
   - High priority: Auto-trigger sandbox provisioning + POC scoping
   - Medium priority: Alert deal owner to initiate POC scoping
   - Low priority: Send the prospect a self-service trial link instead

Update the deal with `poc_qualified`, `poc_priority`, and `poc_qualification_reason` using `attio-custom-attributes`.

Fire PostHog event: `poc_qualified` with `deal_id`, `priority`, `qualification_reason`.

### 2. Build the milestone check-in sequence

Create a Loops sequence using `loops-sequences` that sends milestone reminder and check-in emails:

**Email 1 — 48 hours after POC start (Milestone 1 reminder):**
- Subject: "Quick check: how's the first {milestone_1_name} going?"
- Body: Reference the specific milestone, link to sandbox, offer a 15-min help call via Cal.com
- Trigger: `poc_kickoff_completed` PostHog event

**Email 2 — Mid-point review reminder (auto-calculated from POC duration):**
- Subject: "Halfway through your POC — let's review progress"
- Body: Milestone progress summary (pull from Attio), link to mid-point review Cal.com booking
- Trigger: n8n cron at POC duration / 2

**Email 3 — 48 hours before POC end:**
- Subject: "Your POC wraps up in 2 days — here's where things stand"
- Body: Final criteria status summary, link to final review Cal.com booking, reminder of decision framework
- Trigger: n8n cron at POC end date minus 2 days

**Email 4 — POC completion + results summary:**
- Subject: "POC results: {X} of {Y} criteria met"
- Body: Criterion-by-criterion results, recommendation, next steps
- Trigger: `poc_completed` PostHog event or POC end date

Connect each email's send event to PostHog: `poc_checkin_sent` with `deal_id`, `checkin_type`, `day_of_poc`.

### 3. Build the blocker escalation workflow

Create an n8n workflow that monitors for POC blockers:

1. **No login within 48 hours of kickoff**: Send a gentle reminder via Loops. If still no login after 72 hours, alert the deal owner via Slack.
2. **Milestone missed by 2+ days**: Alert the deal owner with the specific milestone and suggest a check-in call. Auto-generate a Cal.com booking link.
3. **Error spike**: If PostHog reports 3+ `sandbox_error_encountered` events in 24 hours, alert both the deal owner and support team.
4. **Champion goes silent**: If no sandbox activity and no email reply for 5+ days, escalate to deal owner: "POC at {company} appears stalled. Recommend direct outreach to {champion_name}."

Each escalation updates the Attio deal with a `poc_blocker` note including: blocker type, date detected, recommended action.

### 4. Build the POC progress tracker

Create an n8n workflow that runs daily and updates each active POC deal in Attio:

1. Query PostHog for all `poc_criterion_met` and `poc_milestone_achieved` events for each active POC.
2. Calculate: criteria met (count and list), milestones achieved, days remaining, engagement score.
3. Update the deal in Attio with: `poc_criteria_met_count`, `poc_milestones_achieved`, `poc_days_remaining`, `poc_health_status` (on-track / at-risk / stalled).
4. For each deal, classify health:
   - **On-track**: Milestones on schedule, engagement score > 30
   - **At-risk**: 1+ milestone missed or engagement score declining
   - **Stalled**: No activity for 3+ days or 2+ milestones missed

Fire PostHog event: `poc_health_updated` with `deal_id`, `health_status`, `criteria_met`, `days_remaining`.

### 5. Build the POC completion workflow

Create an n8n workflow that fires when a POC reaches its end date:

1. Pull final results from PostHog: criteria met, milestones achieved, total sessions, features used.
2. Generate a results summary using the Anthropic API: criterion-by-criterion assessment, overall recommendation, suggested next steps.
3. Store the results summary in Attio as a note on the deal.
4. Send the results summary email to the champion via `loops-transactional`.
5. If all must-have criteria met: update deal stage to next stage, alert deal owner to send proposal.
6. If criteria partially met: recommend a brief extension or adjusted scope. Alert deal owner.
7. If criteria failed: log the failure reasons, update deal with loss risk, recommend a debrief call.

Fire PostHog event: `poc_completed` with `deal_id`, `criteria_met_count`, `total_criteria`, `pass_fail`, `duration_actual`.

## Output

- POC qualification workflow with automatic routing by priority
- Milestone check-in email sequence with progress summaries
- Blocker detection and escalation with recommended actions
- Daily POC progress tracking synced to CRM
- Automated POC completion workflow with results generation

## Triggers

- Qualification: Fires when deal moves to Aligned stage
- Check-ins: Fires on POC milestone dates
- Blocker detection: Runs continuously (n8n cron every 6 hours)
- Progress tracker: Runs daily
- Completion: Fires on POC end date
