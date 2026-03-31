---
name: proactive-support-outreach-baseline
description: >
  Proactive Support Outreach — Baseline Run. Automate struggle detection and
  contextual outreach so at-risk users receive help without manual intervention.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Email, Direct"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥50% engagement rate, ≥15pp retention lift vs. non-outreached baseline"
kpis: ["Outreach engagement rate", "Resolution rate", "30-day retention lift", "Ticket deflection"]
slug: "proactive-support-outreach"
install: "npx gtm-skills add product/retain/proactive-support-outreach"
drills:
  - struggle-signal-detection
  - proactive-outreach-pipeline
  - posthog-gtm-events
---

# Proactive Support Outreach — Baseline Run

> **Stage:** Product → Retain | **Motion:** LeadCaptureSurface | **Channels:** Email, Direct

## Outcomes

The Smoke test proved struggling users respond to contextual help. Now automate it. The agent builds the full detection-to-outreach pipeline: struggle signals are scored every 6 hours, contextual help is generated and routed automatically, and outcomes are tracked. This runs always-on without manual effort.

Success = at least 50% outreach engagement rate sustained over 2 weeks, AND a measurable retention lift of at least 15 percentage points for outreached users compared to baseline.

## Leading Indicators

- Struggle detection pipeline running on schedule (every 6 hours) without errors
- Outreach messages being delivered within 6 hours of struggle detection
- Users engaging with in-app tips and help links (click-through rate)
- Struggle scores dropping within 48 hours of outreach delivery
- Support ticket volume decreasing for workflows covered by proactive outreach
- No increase in unsubscribes or negative feedback from outreach recipients

## Instructions

### 1. Configure full event tracking

Run the `posthog-gtm-events` drill to set up comprehensive tracking for the play. Beyond the basic struggle events from Smoke, add these play-specific events:

- `proactive_outreach_sent` — properties: person_id, struggle_tier, outreach_channel, stuck_workflow, struggle_score
- `proactive_outreach_engaged` — properties: person_id, outreach_channel, engagement_type, time_to_engage_hours
- `proactive_outreach_resolved` — properties: person_id, stuck_workflow, resolution_type, days_to_resolve, struggle_score_before, struggle_score_after
- `proactive_outreach_failed` — properties: person_id, stuck_workflow, days_to_churn, outreach_attempts

Build a PostHog funnel: `struggle_detected` -> `proactive_outreach_sent` -> `proactive_outreach_engaged` -> `proactive_outreach_resolved`. This is the play's core conversion funnel.

### 2. Deploy automated struggle detection

Run the full `struggle-signal-detection` drill (all 8 steps). This builds:

- The scoring query that runs every 6 hours via n8n
- PostHog cohorts for each struggle tier (mild, moderate, severe, critical)
- Struggle context extraction (stuck workflow, failure mode, error patterns)
- Support ticket correlation (suppress outreach if ticket already open)
- Attio records enriched with struggle data
- Webhook trigger to fire when users enter moderate+ tiers

Validate that the pipeline runs cleanly for 48 hours before enabling outreach. Check: are users being scored? Are the cohorts populating? Is the context extraction producing useful data (specific workflows and failure modes, not generic)?

### 3. Deploy automated outreach

Run the full `proactive-outreach-pipeline` drill (all 8 steps). This builds:

- Routing logic that matches outreach intensity to struggle tier
- In-app message templates in Intercom (contextual tip for moderate, detailed help for severe, urgent help for critical)
- Email templates in Loops (proactive tip email, personal email for critical tier)
- A 2-email follow-up sequence for non-responders
- Human routing via Attio for critical-tier users
- Cooldown enforcement (14-day per-user, suppress during open tickets, suppress during onboarding)

**Human action required:** Before enabling automated outreach, review the in-app message templates and email templates. Verify:
- Tone is helpful and specific, not surveillance-like
- Help article links resolve correctly
- Deep links go to the right product areas
- The workflow-to-help-resource mapping covers the top 5 most common struggle workflows from your Smoke test data

Enable outreach for moderate tier first. Run for 3 days. If engagement is above 30%, enable severe and critical tiers.

### 4. Build the baseline measurement

Create a PostHog cohort of users who were flagged moderate+ but did NOT receive outreach (either from the pre-launch period or from cooldown-suppressed users). This is your control group for measuring retention lift.

Compare 30-day retention:
- **Outreached users:** Users who received proactive outreach after being flagged
- **Baseline (no outreach):** Users with similar struggle scores who were not outreached

The difference is your retention lift. Target: ≥15 percentage points.

Also measure ticket deflection: compare the support ticket filing rate for outreached users vs. non-outreached users with similar struggle profiles. Outreached users should file fewer tickets.

### 5. Evaluate against threshold

Measure against: ≥50% engagement rate AND ≥15pp retention lift. Engagement counts: clicked help link, replied to email, watched video walkthrough, completed previously-stuck workflow within 48 hours, opened support chat from outreach CTA.

If PASS: The automated pipeline works. Proceed to Scalable.
If FAIL on engagement: Review which outreach messages are being ignored. Check: is the struggle context accurate? Are the help resources actually solving the problem? Are messages being delivered at the right time?
If FAIL on retention: The outreach engages users but does not retain them. The underlying product issues may be too severe for a help message to fix. Review which workflows have high engagement but low resolution — those need product fixes, not better help content.

## Time Estimate

- 3 hours: Set up PostHog event tracking and funnel
- 4 hours: Deploy full struggle-signal-detection pipeline (n8n workflow, PostHog cohorts, Attio sync)
- 4 hours: Deploy full proactive-outreach-pipeline (Intercom templates, Loops templates, n8n routing, help resource mapping)
- 2 hours: Review and approve templates, enable outreach
- 3 hours: Monitor for 2 weeks, evaluate results, document findings

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Struggle detection, session recordings, funnel analysis, cohorts | Free tier: 1M events/mo; Paid: from $0 — https://posthog.com/pricing |
| Intercom | In-app contextual help messages | Starter: $74/mo; Pro varies by seats — https://www.intercom.com/pricing |
| Loops | Triggered outreach emails and follow-up sequences | Free tier: 1K contacts; Starter: $49/mo — https://loops.so/pricing |
| n8n | Scheduling detection runs, routing logic, webhook processing | Free (self-hosted); Cloud: from $24/mo — https://n8n.io/pricing |

## Drills Referenced

- `struggle-signal-detection` — Full automated pipeline detecting users struggling with the product every 6 hours
- `proactive-outreach-pipeline` — Automated contextual help delivery matched to struggle tier and stuck workflow
- `posthog-gtm-events` — Set up play-specific event tracking and funnels
