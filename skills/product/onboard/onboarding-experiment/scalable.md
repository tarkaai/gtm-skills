---
name: onboarding-experiment-scalable
description: >
  Onboarding A/B Tests — Scalable Automation. Run an automated experiment
  pipeline that continuously tests onboarding variations across multiple
  surfaces and personas, targeting >= 12% activation lift sustained at 500+ users.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "40 hours over 2 months"
outcome: "Activation rate >= 12% above Baseline winner sustained over 500+ users, with >= 6 experiments completed"
kpis: ["Activation rate by variant and persona", "Experiment throughput (completed per month)", "Cumulative lift from adopted experiments", "Per-persona activation rate convergence", "Experiment win rate"]
slug: "onboarding-experiment"
install: "npx gtm-skills add product/onboard/onboarding-experiment"
drills:
  - experiment-pipeline-automation
  - onboarding-experiment-orchestration
  - onboarding-persona-scaling
  - ab-test-orchestrator
---

# Onboarding A/B Tests — Scalable Automation

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Run an automated experiment pipeline that continuously tests onboarding variations without manual orchestration. Scale from testing one generic onboarding flow to testing per-persona onboarding paths across tours, emails, empty states, and in-app nudges simultaneously. Complete at least 6 experiments in 2 months. Achieve >= 12% activation lift above the Baseline winner, sustained across 500+ users.

## Leading Indicators

- Experiment pipeline automation fully operational: experiments auto-launch from backlog, auto-monitor for completion, and auto-collect results within the first week of setup
- At least 3 experiments completed in month 1 (pipeline is running at target velocity)
- Per-persona activation funnels show at least 1 persona where activation rate improved by >= 20% from a persona-specific experiment (the 10x leverage of personalized testing)
- Experiment backlog stays populated with >= 3 queued hypotheses at all times (hypothesis generation keeps pace with experiment throughput)
- Guardrail metrics (support tickets, error rates) remain flat despite higher experiment velocity

## Instructions

### 1. Automate the experiment pipeline

Run the `experiment-pipeline-automation` drill. This produces:
- An n8n workflow that checks Attio daily for the next queued hypothesis and auto-launches it as a PostHog experiment with feature flag and variant allocation
- A completion monitor that checks daily whether running experiments have reached sample size, exceeded max duration, or breached guardrails
- Auto-result collection that pulls PostHog experiment data into Attio when complete
- Auto-queue logic that promotes the next backlog hypothesis when the current experiment ends
- A pipeline dashboard showing experiments in flight, completed this month, and backlog depth

After setup, the pipeline runs continuously. One experiment is always active if the backlog is populated. No manual intervention required for the standard experiment lifecycle.

### 2. Scale to per-persona onboarding experiments

Run the `onboarding-persona-scaling` drill. This produces:
- 5+ persona-specific onboarding paths (tours + emails + in-app messages)
- Automated persona classification assigning new signups to personas without manual tagging
- Per-persona activation funnels in PostHog
- Comparative dashboard showing activation rate by persona

With per-persona paths in place, the experiment pipeline can now test variations scoped to specific personas. This is the 10x multiplier: instead of testing one onboarding flow for all users, test persona-specific variations where the activation gap is largest.

### 3. Run per-persona experiments

Using the `onboarding-experiment-orchestration` drill, configure experiments scoped to specific personas:
- PostHog feature flag filters: only users with `persona_type = [target persona]` are enrolled
- Hypothesis targets the specific persona's activation path (e.g., "If we change the Team Lead tour to show team activity feed before task creation, team lead activation will increase by 15%")
- Sample size calculations use persona-specific signup volume, not total volume

Prioritize experiments for the lowest-performing persona first. A 20% lift for a persona at 25% activation has more absolute impact than a 5% lift for a persona at 55% activation.

### 4. Run multi-surface experiments

Using the `ab-test-orchestrator` drill, design experiments that test coordinated changes across multiple onboarding surfaces:
- Test A: Changed tour + unchanged emails vs unchanged tour + unchanged emails (isolate tour impact)
- Test B: Unchanged tour + changed emails vs unchanged tour + unchanged emails (isolate email impact)
- Test C: Changed tour + changed emails vs unchanged everything (test combined impact, only after A and B show individual wins)

Never test A, B, and C simultaneously — run them sequentially. Stacking experiments creates interaction effects that make results uninterpretable.

### 5. Maintain the hypothesis backlog

Feed the experiment pipeline by generating new hypotheses monthly:
- Run `experiment-hypothesis-design` after every 3 completed experiments
- Use results from completed experiments to generate follow-up hypotheses (e.g., "Tour shortening increased completion — what if we shorten further to 2 steps?")
- Incorporate anomaly data from per-persona monitoring (a persona's activation rate dropping triggers a new hypothesis)
- Review session recordings for 10 users per month to identify qualitative friction signals that quantitative data misses

### 6. Evaluate cumulative result

After 2 months and >= 6 completed experiments:

- **Pass:** Current activation rate is >= 12% above the Baseline winner, sustained across 500+ users who went through the optimized onboarding. At least 3 persona-specific paths are optimized. Experiment pipeline is self-running.
- **Marginal (8-12% lift):** Pipeline is working but hypotheses are not bold enough. Generate higher-impact hypotheses (structural changes, not copy tweaks). Run for 1 more month.
- **Fail (< 8% lift after 6 experiments):** Investigate whether onboarding optimization has hit diminishing returns. The remaining activation gap may require product changes (simpler core workflow, better empty states, faster time-to-value) rather than flow optimization. Document findings for product team.

## Time Estimate

- 8 hours: Experiment pipeline automation setup (n8n workflows, Attio configuration, pipeline dashboard)
- 8 hours: Persona scaling (classification logic, per-persona tours/emails/messages, per-persona funnels)
- 12 hours: Running 6+ experiments (2 hours each: hypothesis refinement, variant build, result review)
- 6 hours: Hypothesis generation and backlog management (2 hours x 3 cycles)
- 4 hours: Session recording review and qualitative analysis
- 2 hours: Final evaluation and Durable planning

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, per-persona funnels, cohort analysis, session recordings | Free tier: 1M events/mo, 1M flag requests/mo, 5K recordings/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | Per-persona product tours, in-app nudge messages, contextual tooltips | Essential: $29/seat/mo + Proactive Support Plus: $99/mo for 500 messages — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Per-persona email sequences, behavioral trigger emails | Starter: $49/mo for 5,000 contacts with unlimited sends — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Experiment pipeline automation, persona classification, completion monitoring | Self-hosted: free; Cloud: from $24/mo — [n8n.io/pricing](https://n8n.io/pricing) |

**Estimated monthly cost at this level:** $128-201/mo (Intercom Proactive Support Plus $99/mo + Loops Starter $49/mo if > 1,000 contacts; PostHog and n8n free tiers likely sufficient)

## Drills Referenced

- `experiment-pipeline-automation` — automates the full experiment lifecycle: backlog prioritization, PostHog experiment creation, completion monitoring, result collection, and next-experiment queuing
- `onboarding-experiment-orchestration` — designs and runs each individual onboarding A/B test with per-variant tracking and evaluation criteria
- `onboarding-persona-scaling` — scales from 2-3 personas to 5+ with automated classification, per-persona tours/emails/messages, and comparative activation funnels
- `ab-test-orchestrator` — provides the statistical framework for multi-surface experiments: sample size calculation, significance testing, and peeking discipline
