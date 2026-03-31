---
name: sandbox-environment-demo-baseline
description: >
  Sandbox Environment Demo — Baseline Run. Instrument sandbox usage tracking, build
  engagement scoring, and deploy usage-based interventions to maintain ≥65% active usage
  and ≥50% success checklist completion across 80%+ of qualified opportunities over 2 weeks.
stage: "Sales > Connected"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: "Sandboxes on ≥80% of qualified opportunities over 2 weeks with ≥65% active usage and ≥50% completing success checklist"
kpis: ["Sandbox provisioning rate", "Active usage rate", "Success checklist completion rate", "Engagement score distribution", "Sandbox-to-close conversion"]
slug: "sandbox-environment-demo"
install: "npx gtm-skills add sales/connected/sandbox-environment-demo"
drills:
  - sandbox-usage-monitoring
  - posthog-gtm-events
---

# Sandbox Environment Demo — Baseline Run

> **Stage:** Sales → Connected | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Provision sandboxes for at least 80% of qualified opportunities over 2 weeks. At least 65% of provisioned sandboxes must show active usage. At least 50% of sandboxes must have 3 or more success checklist milestones completed. This proves the sandbox program works consistently, not just for the first batch, and that usage-based interventions maintain engagement.

## Leading Indicators

- Engagement score trend across all active sandboxes (target: >50% in Warm or above)
- Intervention trigger rate (how often low-usage interventions fire — lower is better over time)
- Time to first milestone completion (target: <48 hours)
- Deal owner response time to sandbox alerts (target: <4 hours during business hours)

## Instructions

### 1. Set up the sandbox event taxonomy

Run the `posthog-gtm-events` drill to establish the sandbox-specific event taxonomy in PostHog. Configure events for every sandbox lifecycle stage:

- `sandbox_provisioned`, `sandbox_first_login`, `sandbox_session_started`
- `sandbox_feature_used`, `sandbox_workflow_completed`, `sandbox_data_uploaded`
- `sandbox_error_encountered`, `sandbox_help_requested`, `sandbox_milestone_achieved`
- `sandbox_expired`

Attach standard properties to every event: `sandbox_id`, `deal_id`, `industry`, `persona`, `days_since_provisioned`. Verify events are flowing by provisioning a test sandbox and walking through the complete user journey.

### 2. Deploy the sandbox usage monitoring system

Run the `sandbox-usage-monitoring` drill to build the always-on monitoring infrastructure:

1. **Engagement scoring pipeline**: n8n workflow that runs every 6 hours, queries PostHog for sandbox events, computes engagement scores, and writes them to Attio on each deal record.
2. **Usage-based interventions**: n8n workflows triggered by specific usage patterns:
   - No login within 48 hours → reminder email via Loops
   - Logged in but explored <2 features → Intercom in-app message suggesting the most relevant feature
   - No session for 5+ days → personal email from deal owner
   - 3+ workflows completed → Slack alert to deal owner
   - Own data uploaded → immediate high-intent alert
   - All milestones completed → auto-draft proposal invitation
3. **Error interventions**: Error detection and routing to support and deal owner.
4. **Sandbox analytics dashboard**: PostHog dashboard with provisioning velocity, time to first login, session depth, feature heatmap, milestone funnel, and engagement score distribution.

### 3. Provision sandboxes for all qualified opportunities

Continue using the `sandbox-provisioning-workflow` drill (from Smoke level) to provision sandboxes. The target is now 80%+ of qualified opportunities — not just a handpicked batch. Identify any bottlenecks in the provisioning process:

- Does provisioning take too long? Streamline the persona selection or sample data configuration.
- Are some deals missing discovery data? Flag incomplete discovery as a blocker for sandbox access.
- Are kickoff emails getting low open rates? Test subject lines and send times.

**Human action required:** Continue conducting walkthrough calls when prospects book them. Review intervention emails before they send during the first week (once validated, let them run unattended).

### 4. Build the sandbox content library

Create reusable assets that reduce provisioning effort:

- 3-5 industry-specific walkthrough videos (Loom) that can be assigned based on prospect persona
- Email templates for each intervention type (reminder, check-in, congratulations, re-engagement)
- Success checklist templates by industry/use case (pre-built milestone sets)
- Troubleshooting guide for common sandbox errors

Store all assets in a shared location accessible to the provisioning workflow and monitoring system.

### 5. Analyze sandbox-to-outcome correlation

After 2 weeks, pull deal data from Attio and sandbox data from PostHog. Analyze:

- Do prospects with higher engagement scores advance to Proposed at a higher rate?
- Which specific usage patterns (features, milestones, sessions) correlate most with deal progression?
- Does time to first login predict overall engagement?
- Do walkthroughs (video or call) improve milestone completion rates?

Document findings. These become the basis for the predictive model at Scalable level.

### 6. Evaluate against threshold

Measure against the pass criteria:

- **Primary**: Sandboxes on ≥80% of qualified opportunities over 2 weeks
- **Secondary**: ≥65% active usage rate
- **Tertiary**: ≥50% completing 3+ success checklist milestones

If PASS, proceed to Scalable. If FAIL, diagnose which criterion was missed. If provisioning rate is low, simplify the process. If usage rate is low, improve kickoff materials or intervention timing. If milestone completion is low, revisit checklist design.

## Time Estimate

- 4 hours: Set up event taxonomy and verify event flow
- 6 hours: Deploy monitoring system (engagement scoring, interventions, dashboard)
- 3 hours: Build content library (templates, videos, checklists)
- 3 hours: Provision sandboxes and monitor over 2 weeks
- 2 hours: Analyze correlation data and evaluate threshold

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loom | Industry-specific walkthrough videos | $12.50/creator/mo (Business, annual) — [loom.com/pricing](https://www.loom.com/pricing) |
| Loops | Kickoff emails, intervention sequences | Free up to 1,000 contacts or $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| Intercom | In-app messages for sandbox users | $29/seat/mo (Essential, annual) — [intercom.com/pricing](https://www.intercom.com/pricing) |

**Estimated play-specific cost:** ~$50-90/mo (Loom Business + Loops Free/Starter + Intercom Essential 1 seat)

_CRM (Attio), analytics (PostHog), and automation (n8n) are standard stack — not included in play budget._

## Drills Referenced

- `sandbox-usage-monitoring` — builds the engagement scoring pipeline, usage-based interventions, error handling, and analytics dashboard
- `posthog-gtm-events` — establishes the sandbox event taxonomy in PostHog with consistent naming, properties, and funnels
