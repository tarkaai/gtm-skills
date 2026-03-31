---
name: experiment-pipeline-automation
description: Automate the experiment lifecycle from backlog prioritization through launch, monitoring, and result collection
category: Experimentation
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-experiments
  - posthog-feature-flags
  - posthog-custom-events
  - n8n-workflow-basics
  - n8n-scheduling
  - n8n-triggers
  - attio-notes
  - attio-automation
---

# Experiment Pipeline Automation

This drill automates the experiment lifecycle so experiments run continuously without manual orchestration. It connects the hypothesis backlog to PostHog experiments, monitors for completion, collects results, and queues the next experiment. The goal is to remove the human bottleneck from experiment throughput — the agent manages the pipeline, humans review results.

## Prerequisites

- Experiment backlog populated by the `experiment-hypothesis-design` drill (at least 3 queued hypotheses in Attio)
- PostHog with experiments and feature flags enabled
- n8n instance for workflow automation
- Attio with experiment records configured

## Input

- Attio experiment backlog (hypotheses with status "queued" or "next")
- PostHog project with sufficient traffic for the target experiments
- n8n credentials for PostHog, Attio, and notification channels (Slack or email)

## Steps

### 1. Build the experiment launcher workflow (n8n)

Using `n8n-workflow-basics` and `n8n-triggers`, create a workflow triggered by either:
- A cron schedule (daily at 09:00 UTC) that checks if any experiment slot is open
- An Attio webhook that fires when an experiment's status changes to "completed" or "reverted"

The workflow logic:
1. Query Attio for experiments with status "running" — if any exist, check if they have reached their planned sample size via PostHog API
2. If no experiments are running, query Attio for the top-ranked "next" experiment
3. If a "next" experiment exists, proceed to launch sequence

### 2. Automate experiment creation in PostHog

When the launcher identifies a "next" experiment, it:

1. Reads the hypothesis details from Attio (target metric, variants, sample size, duration)
2. Uses `posthog-feature-flags` to create the feature flag for variant allocation (50/50 split by default)
3. Uses `posthog-experiments` to create the experiment: primary metric, secondary metrics, expected sample size, and planned end date
4. Updates the Attio record: status = "running", start_date = today, posthog_experiment_id = [id]
5. Sends a notification: "Experiment launched: [hypothesis] — expected duration [X] days"

### 3. Build the completion monitor workflow (n8n)

Using `n8n-scheduling`, create a daily check workflow:

1. Query PostHog for all running experiments
2. For each experiment, check:
   - Has it reached the required sample size? (both variants have N+ observations)
   - Has it exceeded the maximum duration? (28 days hard cap)
   - Has any guardrail metric been breached? (error rate spike, unsubscribe spike, crash rate increase)
3. If sample size reached → mark experiment as "ready-for-evaluation" in Attio
4. If guardrail breached → auto-disable the feature flag, mark as "reverted-guardrail", send urgent notification
5. If maximum duration exceeded without reaching sample size → mark as "underpowered", send notification with options (extend or abandon)

### 4. Automate result collection

When an experiment reaches "ready-for-evaluation":

1. Pull full results from PostHog: control vs variant for primary and all secondary metrics, confidence intervals, p-values
2. Store raw results in the Attio experiment record
3. Use `posthog-custom-events` to log an `experiment_completed` event with metadata for long-term tracking
4. Trigger the evaluation step (either automated via `experiment-evaluation` fundamental at Durable level, or human notification at Scalable level)

### 5. Build the auto-queue workflow

After an experiment completes (evaluated or reverted):

1. Check the backlog in Attio for the next highest-priority "queued" hypothesis
2. If one exists, promote it to "next" status
3. The launcher workflow (Step 1) picks it up on the next cycle
4. If no hypotheses remain queued, send a notification: "Experiment backlog empty — run experiment-hypothesis-design drill to generate new hypotheses"

This creates a continuous pipeline: as one experiment ends, the next begins automatically.

### 6. Build the pipeline dashboard

Using `posthog-custom-events`, track pipeline health metrics:
- `experiment_launched`, `experiment_completed`, `experiment_reverted`, `experiment_abandoned`
- Time from hypothesis creation to experiment launch
- Time from launch to result
- Backlog depth (queued hypotheses)

Create a PostHog dashboard showing: experiments completed this month, current experiment status, backlog depth, average experiment cycle time.

## Output

- Automated experiment pipeline that launches, monitors, and collects results without manual intervention
- Pipeline dashboard showing throughput and health
- Notifications for launches, completions, guardrail breaches, and empty backlogs
- Continuous experiment velocity: one experiment always running if backlog is populated

## Triggers

This is an always-on automation. The n8n workflows run on daily cron schedules and Attio webhooks. No manual trigger needed after initial setup.
