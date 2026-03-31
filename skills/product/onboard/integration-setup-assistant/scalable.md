---
name: integration-setup-assistant-scalable
description: >
  Integration Setup Assistant -- Scalable Automation. Personalize the integration
  wizard by persona, A/B test setup flows systematically, expand to all integrations,
  and maintain >=60% completion at 500+ users/month. The 10x multiplier is
  persona-based wizard variants that serve different user types without manual effort.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=60% integration completion rate at 500+ new users/month"
kpis: ["Integration completion rate at scale", "Per-persona completion rate", "Per-integration success rate", "Time to first integration (p50 and p90)", "Rescue recovery rate", "Post-integration 7-day retention by persona"]
slug: "integration-setup-assistant"
install: "npx gtm-skills add product/onboard/integration-setup-assistant"
drills:
  - ab-test-orchestrator
  - onboarding-persona-scaling
  - dashboard-builder
---

# Integration Setup Assistant -- Scalable Automation

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

>=60% integration completion rate sustained at 500+ new users per month. Persona-specific wizard variants serve different user types automatically. Systematic A/B testing identifies the highest-performing wizard configuration per persona.

## Leading Indicators

- Per-persona wizard completion rates all above 55%
- No single integration's failure rate exceeds 25%
- Rescue workflow recovering >30% of stalled users
- A/B test velocity: 2+ experiments completed per month
- Time to first integration p50 <8 minutes across all personas

## Instructions

### 1. Build persona-specific wizard variants

Run the `onboarding-persona-scaling` drill to create differentiated integration wizards for each user persona:

1. Query PostHog to identify distinct user segments by `signup_source`, `plan_type`, `company_size`, or `role`. Look for segments with meaningfully different integration patterns -- for example, technical users might prefer API-key integrations while non-technical users prefer OAuth.

2. Create 2-4 persona definitions based on the data. Each persona gets:
   - A different integration priority ranking (which 3 integrations appear in their checklist)
   - Different setup guidance copy (technical personas get API documentation links; non-technical personas get step-by-step screenshots)
   - Different Intercom bot conversation flows (technical: shorter, assumes knowledge; non-technical: more hand-holding)

3. Build separate Intercom checklists for each persona. Use Intercom audience rules to show the right checklist based on user properties:
   - Rule: `persona_type` equals `technical` -> show "Developer Setup" checklist with API-first integrations
   - Rule: `persona_type` equals `business_user` -> show "Quick Connect" checklist with OAuth-first integrations
   - Rule: `persona_type` equals `team_admin` -> show "Team Setup" checklist emphasizing team-wide integrations

4. Update the n8n failure recovery and rescue workflows to include `persona_type` in all messages, so troubleshooting guidance matches the user's technical level.

5. Update the Loops email sequences to branch by persona: technical users get integration documentation links; business users get video walkthroughs.

**Human action required:** Review each persona's checklist copy and bot flow before deploying. Verify that the persona classification logic assigns users correctly by spot-checking 20 recent signups.

### 2. Run systematic A/B tests on wizard configuration

Run the `ab-test-orchestrator` drill to test variations of the wizard. Run experiments sequentially (one at a time), each for at least 7 days or 200+ users per variant:

**Experiment 1: Wizard timing**
- Control: Checklist appears on first login immediately
- Variant: Checklist appears after the user completes one other onboarding action (e.g., creates their first project)
- Hypothesis: Showing the wizard after the user has invested effort increases completion because they are more committed
- Primary metric: `integration_wizard_completed` rate
- Secondary metrics: overall activation rate, time to first integration

**Experiment 2: Checklist length**
- Control: 3 integrations in checklist
- Variant A: 1 integration (only the highest-impact one)
- Variant B: 5 integrations
- Hypothesis: Fewer steps increase completion rate but reduce total integrations connected
- Primary metric: % completing at least 1 integration
- Secondary metric: average integrations connected per user

**Experiment 3: Rescue message channel**
- Control: Intercom in-app message for stalled users
- Variant: Loops email for stalled users
- Hypothesis: Email reaches users who have left the product; in-app only reaches users who return
- Primary metric: rescue recovery rate (% of stalled users who complete after intervention)

**Experiment 4: Bot guidance depth**
- Control: Current bot flow (step-by-step guidance)
- Variant: Simplified bot (one message with a help article link instead of multi-step flow)
- Hypothesis: Shorter bot interactions reduce friction for users who know what they are doing
- Primary metric: integration success rate on first attempt

After each experiment, implement the winner permanently. Document the result (variant, sample size, effect size, confidence) in Attio.

### 3. Deploy continuous integration health monitoring

Run the `dashboard-builder` drill to set up always-on monitoring:

1. Build the PostHog "Integration Setup Health" dashboard with panels for: overall completion rate trend, per-integration success rates, time to connect distributions, failure rate by error type, rescue effectiveness, and wizard abandonment funnel

2. Configure the daily n8n monitoring workflow that checks all metrics against anomaly thresholds and sends critical alerts within hours of detection

3. Configure the weekly health report workflow that generates a per-persona, per-integration breakdown every Monday

4. Build integration-specific failure cohorts in PostHog for targeted interventions

5. Set up third-party integration change detection to catch OAuth or API changes from integration partners

This monitoring infrastructure is critical for the Durable level -- it feeds directly into the autonomous-optimization loop.

### 4. Expand to all integrations

Once the top 3 integrations are optimized and stable:

1. Add integrations 4-6 to the wizard (new checklist steps per persona)
2. For each new integration, build the contextual Intercom bot and failure recovery workflow
3. Run a 1-week test with each new integration to verify success rates >50% before including it in the default checklist
4. If an integration's success rate is <50%, either simplify its setup flow or keep it out of the default wizard and make it discoverable via a secondary "More Integrations" path

### 5. Evaluate at scale

After 2 months, verify the threshold:

- **Primary metric:** Integration completion rate across all users
- **Pass threshold:** >=60% at 500+ new users per month
- **Per-persona check:** No persona below 50% completion
- **Per-integration check:** No integration in the default wizard below 50% success rate
- **Scale check:** Completion rate has not degraded as volume increased

If PASS: Document the final configuration (persona definitions, winning experiment variants, per-integration performance). Proceed to Durable.

If FAIL: If overall rate is close but one persona drags it down, focus all optimization on that persona. If rate degrades at scale, investigate whether the user mix is shifting (cohort drift) or whether n8n workflows are hitting capacity limits.

## Time Estimate

- 16 hours: Persona variant build and deployment (Step 1)
- 20 hours: A/B testing -- 4 experiments at ~5 hours each including setup, monitoring, analysis (Step 2)
- 8 hours: Health monitoring setup (Step 3)
- 8 hours: Integration expansion (Step 4)
- 8 hours: Scale evaluation and documentation (Step 5)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Funnels, experiments, feature flags, cohorts, dashboards | Free tier: 1M events/mo; paid: usage-based from $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Per-persona checklists, bots, in-app messages | Advanced: $85/seat/mo for advanced automation ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| n8n | Rescue workflows, monitoring, event sync | Cloud Pro: $60/mo for 10K executions ([n8n.io/pricing](https://n8n.io/pricing/)) |
| Loops | Per-persona email sequences | Starter: $49/mo ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated play-specific cost at Scalable:** ~$150-300/mo (Intercom Advanced seat + n8n Pro + Loops, depending on volume)

## Drills Referenced

- `ab-test-orchestrator` -- designs, runs, and analyzes A/B tests on wizard timing, length, rescue channel, and bot guidance depth
- `onboarding-persona-scaling` -- creates differentiated wizard variants for each user persona
- `dashboard-builder` -- continuous monitoring with anomaly alerts, weekly reports, and third-party change detection
