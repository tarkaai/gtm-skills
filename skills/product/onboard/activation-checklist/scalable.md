---
name: activation-checklist-scalable
description: >
  Onboarding Checklist Workflow — Scalable Automation. Run systematic A/B tests on
  checklist variants, deploy milestone celebrations with strategic CTAs, and build
  churn prevention for users stalling mid-checklist. Maintain ≥ 60% completion at 500+ users/month.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥ 60% checklist completion rate sustained at 500+ new signups per month"
kpis: ["Checklist completion rate at scale (target ≥ 60%)", "Completion rate by segment (plan, source, persona)", "Experiment win rate (target ≥ 30% of tests produce winners)", "Stalled-user re-engagement rate (target ≥ 25%)", "Median time to activation"]
slug: "activation-checklist"
install: "npx gtm-skills add product/onboard/activation-checklist"
drills:
  - ab-test-orchestrator
  - usage-milestone-rewards
  - churn-prevention
---

# Onboarding Checklist Workflow — Scalable Automation

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Scale the activation checklist from a single variant serving all users to a segmented, experimentally optimized system handling 500+ signups per month. This level finds the 10x multiplier: not just one checklist that works, but the right checklist for each user segment, with automated interventions for stalled users and milestone celebrations that drive expansion.

Pass: ≥ 60% checklist completion rate sustained over 2 months at 500+ new signups per month.
Fail: Completion rate drops below 55% as volume scales, or volume never reaches 500/month.

## Leading Indicators

- First A/B test reaches statistical significance within 14 days (sufficient traffic for experimentation)
- At least 1 experiment produces a ≥ 5pp lift in completion rate (there is room to optimize)
- Segment-level completion rates vary by < 15pp across segments (the checklist works for diverse users, not just one persona)
- Stalled-user intervention re-engages ≥ 25% of users who paused mid-checklist (the churn prevention catches them)
- Milestone celebrations achieve ≥ 10% CTA click-through rate (the celebrations drive engagement beyond the checklist)

## Instructions

### 1. Launch systematic checklist experiments

Run the `ab-test-orchestrator` drill to test variations of the checklist experience. Use PostHog feature flags (`posthog-feature-flags` fundamental) to split traffic between variants.

**Experiment queue** (run sequentially, one at a time, 7-14 days each):

**Experiment 1 — Checklist length:**
- Hypothesis: "If we reduce the checklist from [N] steps to [N-2] steps by combining related actions, then completion rate will increase by ≥ 5pp, because fewer steps reduce perceived effort."
- Control: Current checklist (from Baseline).
- Variant: Shortened checklist with combined steps.
- Primary metric: `activation-checklist_converted` rate.
- Secondary metrics: time-to-activation, 7-day retention.
- Sample size: ≥ 200 per variant.

**Experiment 2 — Step ordering:**
- Hypothesis: "If we move the easiest step to position 1 (instead of the current order), then step-1 completion will increase by ≥ 10pp, because early success creates momentum."
- Control: Current step order.
- Variant: Reordered with easiest step first.
- Same metrics and sample size as above.

**Experiment 3 — Email nudge timing:**
- Hypothesis: "If we send the first nudge email at 12 hours instead of 24 hours after signup, then step-2 completion will increase by ≥ 5pp, because users are still in the consideration window."
- Control: 24-hour first nudge.
- Variant: 12-hour first nudge.
- Primary metric: step-2 completion rate within 48 hours.

**Experiment 4 — In-app guidance format:**
- Hypothesis: "If we replace the tooltip tour with a persistent sidebar checklist, then completion rate will increase by ≥ 5pp, because the checklist is always visible."
- Control: Intercom tooltip-based tour.
- Variant: Intercom in-app message as persistent sidebar.

For each experiment:
1. Use `posthog-feature-flags` to create the flag and allocate 50/50 traffic.
2. Use `posthog-experiments` to define the experiment with primary and secondary metrics.
3. Run for the planned duration (minimum 7 days or 200+ per variant).
4. Analyze using `posthog-experiments`: check statistical significance at 95% confidence.
5. **Adopt** winners permanently. **Revert** losers. **Iterate** on inconclusive results with a modified hypothesis.
6. Document every experiment: hypothesis, variants, sample size, result, confidence level, decision.

### 2. Deploy milestone celebrations with strategic CTAs

Run the `usage-milestone-rewards` drill. Design celebrations for each checklist step and attach expansion CTAs:

**Step-level celebrations** (using `intercom-in-app-messages`):

| Step Completed | Celebration | CTA |
|---------------|-------------|-----|
| Step 1 (profile) | Progress badge: "1 of N complete -- you're off to a great start" | "Next: [Step 2 action] -- takes 2 minutes" |
| Step 2 (first action) | Confetti animation + "First [action] created -- nice work" | "Tip: Try [related feature] to get even more from it" |
| Step 3 (value moment) | Achievement banner: "You just [accomplished outcome] -- this is why teams use [product]" | "Invite a teammate to collaborate" (expansion CTA) |
| Final step | Full celebration: "Onboarding complete -- you're all set" + usage summary | "Explore advanced features" or "Upgrade for [premium capability]" |

**Email celebrations** (using `loops-transactional`):

- Send a milestone email 1-2 hours after each mid-checklist step with a recap and the next step link.
- Send the final celebration email immediately on checklist completion with a usage summary: "You [specific achievements]. Here's what to try next."
- For the final celebration, segment by plan: free users get an upgrade CTA, paid users get a feature deepening CTA.

Track celebration performance with PostHog events:
- `milestone_celebration_shown` with `{step, cta_type}`
- `milestone_celebration_cta_clicked` with `{step, cta_type, cta_destination}`

### 3. Build churn prevention for stalled users

Run the `churn-prevention` drill adapted for onboarding. Build a detection and intervention system for users who start the checklist but stall:

**Define stall signals** (using `posthog-cohorts`):
- **Early stall:** Completed step 1 but no activity for 48+ hours
- **Mid stall:** Completed 2+ steps but no progress for 72+ hours
- **Dismiss stall:** Dismissed the checklist with < 50% steps complete
- **Ghost:** Signed up but never triggered `activation-checklist_impression` (never saw the checklist)

**Build the detection workflow** (using `n8n-triggers` + `n8n-scheduling`):

```
Cron: every 12 hours
  -> Query PostHog for users matching each stall cohort
  -> Score urgency: ghost > dismiss stall > early stall > mid stall
  -> Route to appropriate intervention
```

**Design tiered interventions:**

| Stall Type | Intervention | Channel | Timing |
|-----------|-------------|---------|--------|
| Ghost | "Looks like you haven't started setup yet -- here's a 60-second walkthrough" | Intercom in-app message + Loops email | 48 hours after signup |
| Early stall | "Quick question: did you get stuck on [step name]? Here's how to finish it" | Loops email with deep link to the stalled step | 48 hours after last activity |
| Mid stall | "You're [X]% through setup -- here's what you'll unlock when you finish" | Intercom in-app message showing progress + email with social proof | 72 hours after last activity |
| Dismiss stall | "We noticed you paused setup. Would a 5-minute walkthrough call help?" | Loops email with Cal.com booking link | 24 hours after dismiss |

Track intervention results:
- `stall_intervention_sent` with `{stall_type, intervention_channel}`
- `stall_intervention_reengaged` with `{stall_type, steps_completed_after}`
- Calculate re-engagement rate: users who complete ≥ 1 more step after intervention / total interventions sent.

### 4. Evaluate at scale over 2 months

Track weekly:
- Overall completion rate (target: ≥ 60%)
- Completion rate by segment (signup source, plan type, user persona)
- Experiment results (track cumulative lift from all adopted experiments)
- Stalled-user re-engagement rate (target: ≥ 25%)
- Milestone celebration CTA performance

Decision after 2 months:
- **PASS (≥ 60% completion at 500+ users/month, sustained for 2 months):** The checklist scales. Document: all experiment results and cumulative lift, per-segment performance, intervention effectiveness, and the current best-performing checklist configuration. Proceed to Durable.
- **MARGINAL (55-59% or volume < 500):** If completion is close but volume is low, focus on traffic. If completion is low at high volume, focus on the lowest-performing segment. Run targeted experiments for that segment.
- **FAIL (< 55% sustained):** The checklist may not scale as-is. Check: Are new user demographics changing as you scale? Is the checklist optimized for your original users but not newer segments? Consider persona-based checklist variants (different steps for different user types).

## Time Estimate

- Experiment design and setup (4 experiments): 12 hours
- Milestone celebration design and implementation: 10 hours
- Churn prevention system (detection + interventions): 15 hours
- Ongoing monitoring and experiment management (2 months): 15 hours
- Analysis and documentation: 8 hours
- Total: ~60 hours over 2 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, cohorts, funnels | Free 1M events; paid ~$0.00005/event above free tier ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app checklist, celebrations, stall interventions | Essential $29/seat/mo; Proactive Support add-on $349/mo if needed for outbound ([intercom.com/pricing](https://intercom.com/pricing)) |
| n8n | Stall detection, intervention routing, experiment automation | Pro €60/mo for 10,000 executions ([n8n.io/pricing](https://n8n.io/pricing)) |
| Loops | Behavioral emails, celebration emails, stall nudges | $49/mo for paid plan ([loops.so/pricing](https://loops.so/pricing)) |
| Attio | CRM -- activation and stall tracking | Free up to 3 users; Plus $29/user/mo if needed ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated monthly cost for Scalable:** $138-487 depending on Intercom add-ons and volume. Base: Intercom $29 + n8n $60 + Loops $49. Add Intercom Proactive Support ($349) if outbound in-app messaging volume exceeds included limits.

## Drills Referenced

- `ab-test-orchestrator` -- design, run, and analyze A/B tests on checklist length, step order, email timing, and guidance format
- `usage-milestone-rewards` -- deploy celebrations at each checklist step with strategic expansion CTAs
- `churn-prevention` -- detect stalled users via PostHog cohorts and trigger tiered re-engagement interventions
