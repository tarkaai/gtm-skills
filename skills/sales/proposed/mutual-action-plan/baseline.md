---
name: mutual-action-plan-baseline
description: >
  Mutual Action Plan (MAP) — Baseline Run. Auto-generate MAPs when deals reach proposal stage,
  track milestone progress with automated daily checks, and send weekly progress updates to
  prospects. First always-on MAP automation across 10-15 active deals.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Baseline Run"
time: "20 hours over 2 weeks"
outcome: ">=70% MAP adoption and >=30% faster close time with >=20% higher win rate for MAP deals over 2 weeks"
kpis: ["MAP adoption rate", "Deal velocity (MAP vs non-MAP)", "Win rate (MAP vs non-MAP)", "Milestone adherence rate"]
slug: "mutual-action-plan"
install: "npx gtm-skills add sales/proposed/mutual-action-plan"
drills:
  - map-auto-generation
  - map-milestone-tracking
  - posthog-gtm-events
---

# Mutual Action Plan (MAP) — Baseline Run

> **Stage:** Sales > Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Expand MAPs from 3 manual deals to 10-15 active deals with automated generation and tracking. When a deal enters Proposed stage, the system auto-generates a personalized MAP from the correct template, sends it for rep review, and delivers it to the prospect. A daily n8n workflow monitors milestone progress, and weekly updates go to prospects automatically.

Pass: >= 70% of proposal-stage deals have active MAPs, AND MAP deals close >= 30% faster with >= 20% higher win rate vs non-MAP deals over 2 weeks.
Fail: MAP adoption below 70%, or MAP deals do not significantly outperform non-MAP deals on velocity or win rate.

## Leading Indicators

- Auto-generated MAPs require < 5 minutes of rep review before sending to prospect (generation quality is high)
- >= 80% of prospects respond to the MAP delivery email within 48 hours (engagement is strong)
- Daily milestone checker correctly identifies overdue milestones (automation accuracy)
- Weekly updates trigger prospect responses or milestone completions within 3 days (updates drive action)
- Milestone adherence rate >= 70% across all active MAPs (prospects are following the plan)
- Escalation emails produce responses within 48 hours (the nudge system works)

## Instructions

### 1. Deploy MAP auto-generation

Run the `map-auto-generation` drill to build the n8n workflow that triggers when a deal moves to Proposed stage in Attio.

The workflow:
1. Detects the stage change via Attio webhook
2. Classifies the deal type (SMB/Mid-Market/Enterprise) based on deal value and stakeholder count
3. Retrieves the matching milestone template from Attio
4. Uses Claude API to personalize milestones with deal-specific dates, named stakeholders, and context
5. Stores the MAP as an Attio note with all tracking attributes populated
6. Sends the draft MAP to the rep for review before prospect delivery

**Configuration specifics:**
- Set the Attio webhook to fire on any deal status change to "Proposed"
- Configure Claude API with your Anthropic key in n8n credentials
- Set the rep notification channel (email or Slack)
- Configure the prospect delivery email template in the workflow

**Test the workflow:** Manually move a test deal to Proposed stage. Verify the MAP is generated correctly, the Attio note is created, and the rep notification arrives. Check that dates are calculated correctly from the expected close date.

### 2. Deploy milestone tracking automation

Run the `map-milestone-tracking` drill to build the monitoring and communication system.

**Daily milestone checker (n8n cron, 9 AM):**
- Queries all deals where `map_status` = "Active"
- Parses milestone dates from each MAP note
- Classifies each MAP: on track, at risk, overdue, or stalled
- Updates `map_completion_pct`, `map_at_risk`, and `map_stall_count` in Attio
- Fires PostHog events for overdue milestones and stalls

**Weekly prospect updates (n8n cron, Monday 10 AM):**
- For each active MAP, generates a progress summary
- Sends the update email to the prospect champion
- Logs the update in PostHog and Attio

**Escalation workflow:**
- Level 1 (1-2 days overdue): Gentle nudge email to milestone owner + Slack notification to rep
- Level 2 (5+ days overdue): Direct email requesting timeline update + rep alert with recommended actions
- Level 3 (2+ milestones overdue): Deal flagged as stalled, rep receives diagnosis with intervention options

**Human action required:** Level 3 stalls require rep decision on intervention strategy. The agent surfaces the stall, provides context, and recommends actions but does not execute without approval.

### 3. Configure PostHog event tracking

Run the `posthog-gtm-events` drill to set up the MAP event taxonomy:

| Event | Properties | Fires When |
|-------|-----------|------------|
| `map_created` | deal_id, deal_type, milestone_count, expected_close | MAP activated |
| `map_milestone_completed` | deal_id, milestone_name, owner, days_early_late | Milestone marked done |
| `map_milestone_overdue` | deal_id, milestone_name, owner, days_overdue | Due date passed |
| `map_update_sent` | deal_id, update_type, recipient | Progress email sent |
| `map_stall_detected` | deal_id, stall_reason, consecutive_overdue_count | 2+ milestones delayed |
| `map_completed` | deal_id, total_days, on_time_pct, outcome | All milestones done or deal closed |

Build a PostHog funnel: `map_created` -> `map_milestone_completed` (first) -> `map_milestone_completed` (50%) -> `map_completed`. This shows the MAP completion journey.

Create a PostHog insight comparing deal velocity: average days from `map_created` to `deal_won` for MAP deals vs average days from proposal stage entry to won for non-MAP deals.

### 4. Expand to 10-15 active deals

With automation running, expand MAP coverage:
- Enable the auto-generation trigger for all new deals entering Proposed stage
- Backfill MAPs for existing proposal-stage deals: manually trigger the generation workflow for each
- Target >= 70% adoption: all proposal-stage deals should get a MAP unless the rep explicitly opts out (log opt-outs with reason)

Monitor the first week:
- Check that auto-generated MAPs are accurate (rep review should catch errors)
- Verify milestone dates are realistic (not weekends, not holidays)
- Confirm prospect delivery emails are sending correctly
- Watch for edge cases: deals with no contacts, no close date, or no deal value

### 5. Monitor and iterate for 2 weeks

Daily:
- Review the milestone checker results: are overdue milestones being correctly identified?
- Check that escalation emails are firing at the right levels
- Spot-check Attio: are `map_completion_pct` and `map_at_risk` updating correctly?

Weekly:
- Review PostHog funnel data: what percentage of MAPs reach 50% completion? 100%?
- Compare MAP deal velocity vs non-MAP deals
- Check milestone adherence: which milestones are most often delayed? (Buyer legal review? Executive alignment?)
- Identify template improvements: are milestone durations accurate? Are there missing milestones?

### 6. Evaluate against threshold

After 2 weeks, run the `threshold-engine` drill:

**Metrics to compare:**
- MAP adoption rate: (deals with active MAP / total proposal-stage deals) >= 70%
- Deal velocity: average days in pipeline for MAP deals vs non-MAP deals, MAP should be >= 30% faster
- Win rate: (MAP deals won / MAP deals total) vs (non-MAP deals won / non-MAP deals total), MAP should be >= 20% higher
- Milestone adherence: percentage of milestones completed on time >= 60%

If **PASS:** Automated MAP management meaningfully improves deal outcomes. Proceed to Scalable to add risk scoring, MAP-based forecasting, and template optimization.

If **FAIL:** Diagnose:
- **Low adoption (< 70%):** Auto-generation may be producing low-quality MAPs that reps reject. Review rejection reasons. Improve the Claude prompt or template matching logic.
- **No velocity improvement:** MAPs may not be changing prospect behavior. Check: Are prospects engaging with the weekly updates? Are they completing their milestones? If not, the problem may be champion strength, not MAP mechanics.
- **Low win rate lift:** MAPs may be surfacing deals that would have been won anyway. Check if MAP creation correlates with deal quality.
- **Low milestone adherence:** Milestone dates may be unrealistic. Adjust templates based on actual completion data.

## Time Estimate

- MAP auto-generation workflow setup: 4 hours
- Milestone tracking workflow setup: 4 hours
- PostHog event configuration: 2 hours
- Backfilling existing deals: 2 hours
- Testing and debugging workflows: 3 hours
- Monitoring and iteration (2 weeks): 4 hours
- Threshold evaluation: 1 hour
- **Total: ~20 hours over 2 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal records, MAP storage, custom attributes, milestone data | Plus $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| n8n | Automation — MAP generation trigger, daily milestone checks, weekly updates, escalation workflows | Starter $24/mo or Pro $60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| PostHog | Analytics — MAP event tracking, funnels, velocity comparison | Free (1M events/mo) ([posthog.com/pricing](https://posthog.com/pricing)) |
| Claude API | MAP personalization — generating customized milestone plans from templates | Sonnet: $3/$15 per M input/output tokens ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| Loops | Email — prospect MAP delivery and weekly update emails | Free (< 1K contacts); Starter $49/mo ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated play-specific cost at Baseline:** ~$50-120/mo (n8n Pro + Claude API usage for MAP generation; Attio, PostHog, Loops likely within free tiers at 10-15 deals)

## Drills Referenced

- `map-auto-generation` — Auto-generate personalized MAPs when deals reach Proposed stage, classify deal type, personalize milestones, and deliver for rep review
- `map-milestone-tracking` — Daily milestone health checks, weekly prospect updates, 3-level escalation system for overdue milestones
- `posthog-gtm-events` — Configure MAP event taxonomy for tracking creation, completion, delays, and stalls
