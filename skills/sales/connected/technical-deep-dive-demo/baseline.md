---
name: technical-deep-dive-demo-baseline
description: >
  Technical Deep-Dive Demo — Baseline Run. First always-on automation for technical deep-dive demos:
  auto-generate demo prep from discovery transcripts, track demo-to-POC funnel in PostHog, and
  configure sandbox environments for every technical evaluation.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Product"
level: "Baseline Run"
time: "20 hours over 2 weeks"
outcome: "Technical demos on ≥80% of technically complex opportunities over 2 weeks with ≥50% converting to POC or proposal"
kpis: ["Technical demo coverage rate", "Demo-to-POC conversion rate", "Technical validation speed (days from demo to POC start)", "Technical follow-up package engagement rate"]
slug: "technical-deep-dive-demo"
install: "npx gtm-skills add sales/connected/technical-deep-dive-demo"
drills:
  - posthog-gtm-events
  - technical-demo-content-assembly
  - sandbox-provisioning-workflow
---
# Technical Deep-Dive Demo — Baseline Run

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product

## Outcomes
Run technical deep-dive demos on at least 80% of opportunities with technical stakeholders over 2 weeks. At least 50% of demos must convert to POC or proposal. Demo prep is automated (agent generates scripts from discovery transcripts), sandbox environments are provisioned for every technical evaluation, and the full funnel is tracked in PostHog.

## Leading Indicators
- Demo prep documents are generated within 2 hours of discovery call completion
- Sandbox environments are provisioned within 24 hours of demo scheduling
- Prospects engage with technical follow-up packages (open rate > 60%)
- Time from demo to POC start decreases compared to Smoke baseline
- Technical questions per demo increase (deeper engagement signal)

## Instructions

### 1. Set up PostHog event tracking for the technical demo funnel
Run the `posthog-gtm-events` drill to define and implement the event taxonomy for this play. Configure these events:

| Event | Trigger | Key Properties |
|-------|---------|----------------|
| `technical_demo_prepped` | Demo script generated | `deal_id`, `modules_prepared`, `tech_stack_detected`, `integration_targets` |
| `technical_demo_scheduled` | Cal.com booking confirmed | `deal_id`, `attendee_roles`, `days_since_discovery` |
| `sandbox_provisioned` | Sandbox created for demo | `deal_id`, `sandbox_id`, `industry_persona`, `features_enabled` |
| `technical_demo_completed` | Demo finished and logged | `deal_id`, `outcome`, `modules_shown`, `questions_asked`, `blockers_identified`, `duration_minutes` |
| `technical_followup_sent` | Follow-up package shared | `deal_id`, `docs_included`, `code_samples_included` |
| `technical_followup_opened` | Prospect opens package | `deal_id`, `sections_viewed`, `time_spent_seconds` |
| `poc_started` | POC begins | `deal_id`, `days_since_demo`, `poc_scope` |
| `proposal_requested` | Prospect requests proposal | `deal_id`, `days_since_demo`, `deal_value` |

Connect PostHog to Attio via n8n webhook so deal stage changes from technical demo outcomes are tracked automatically.

### 2. Automate demo prep generation
Configure the `technical-demo-content-assembly` drill to run automatically when a technical deep-dive demo is scheduled. Set up an n8n workflow triggered by Cal.com booking webhooks:

1. Cal.com fires webhook when a booking tagged `technical-demo` is confirmed
2. n8n matches the booking to an Attio deal record (by attendee email)
3. n8n triggers `technical-demo-content-assembly` with the deal ID
4. The drill generates the full demo script, integration code, and follow-up package
5. n8n stores all outputs as Attio notes on the deal
6. n8n sends a Slack notification to the founder: "Demo prep ready for {company_name} — review before {demo_date}"

**Human action required:** Review each generated demo prep document before the demo. Verify the demo script matches what you want to show. Adjust module ordering or emphasis based on your intuition about the deal.

### 3. Provision sandbox environments for technical evaluations
Run the `sandbox-provisioning-workflow` drill to set up the sandbox provisioning pipeline. For every deal that reaches the technical demo stage:

1. Qualify the sandbox request (deal at Connected stage, discovery complete, technical stakeholder identified)
2. Design the sandbox configuration based on discovery notes (industry persona, feature set, success checklist)
3. Provision the environment with prospect-relevant sample data
4. Prepare kickoff materials (access email, walkthrough video, success checklist)
5. Send sandbox access before the demo so the prospect can follow along or explore afterward

Configure sandbox provisioning to run automatically when a demo is scheduled (n8n workflow triggered by the same Cal.com webhook as step 2). The sandbox should be ready at least 24 hours before the demo.

### 4. Execute demos at volume with standardized process
For each demo over the 2-week period:

1. Review the auto-generated demo prep 1 hour before the call
2. Confirm sandbox is provisioned and accessible
3. Execute the demo following the generated script modules
4. Log the outcome immediately after (PostHog event fires automatically via the n8n workflow)
5. Send the technical follow-up package within 2 hours of demo completion

**Human action required:** Deliver the demos. The agent handles all prep, tracking, and follow-up packaging. You focus on the live conversation with the technical stakeholders.

### 5. Track funnel conversion and identify patterns
After 2 weeks, review the PostHog funnel:

`technical_demo_scheduled` -> `technical_demo_completed` -> `poc_started` OR `proposal_requested`

Break down by:
- `modules_shown` — which demo modules correlate with POC conversion
- `attendee_roles` — which stakeholder mix produces the best outcomes
- `tech_stack_detected` vs not — does tech stack personalization improve conversion
- `sandbox_provisioned` vs not — does having a sandbox improve POC start rate
- `days_since_discovery` — does demo timing affect conversion

Evaluate against pass threshold: technical demos on ≥80% of technically complex opportunities with ≥50% converting to POC or proposal.

If PASS, document the winning patterns (best module order, optimal attendee mix, sandbox impact) and proceed to Scalable. If FAIL, diagnose:
- Low demo coverage → scheduling or qualification problem
- Low conversion → demo content not resonating (check which modules underperform)
- Slow POC start → follow-up package not compelling (check engagement rates)

---

## Time Estimate
- PostHog event setup and n8n workflow configuration: 6 hours
- Sandbox provisioning pipeline setup: 4 hours
- Demo prep review and customization: 5 hours (15 min per demo)
- Demo execution: 5 hours (30-40 min per demo, ~12 demos)

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal records, contacts, notes, demo outcome tracking | Plus $29/user/mo |
| PostHog | Event tracking, funnel analysis, demo effectiveness measurement | Free up to 1M events/mo |
| n8n | Automation — Cal.com webhook triggers, demo prep orchestration, sandbox provisioning | Starter €24/mo (2,500 executions) |
| Clay | Tech stack detection and account enrichment for demo prep | Launch $185/mo (2,500 credits) |
| Fireflies | Discovery call transcription feeding demo prep | Pro $10/user/mo (annual) |
| Anthropic Claude API | Demo script and content generation | Sonnet 4.6: $3/$15 per 1M tokens (~$6/mo at 12 demos) |
| Cal.com | Scheduling with webhook triggers for automation | Free (1 user); Teams $15/user/mo |

**Play-specific cost:** ~$50-100/mo (n8n Starter + Clay credits consumed + Claude API usage; CRM, PostHog, and scheduling are standard stack)

## Drills Referenced
- `posthog-gtm-events` — defines and implements the event taxonomy for the technical demo funnel in PostHog
- `technical-demo-content-assembly` — auto-generates prospect-customized demo scripts, integration code, and follow-up packages from discovery data and tech stack enrichment
- `sandbox-provisioning-workflow` — provisions sandbox environments with industry-relevant data, sends access with onboarding materials, and schedules follow-up touchpoints
