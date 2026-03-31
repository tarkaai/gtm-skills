---
name: ai-content-generation-durable
description: >
  AI Content Assistant — Durable Intelligence. The autonomous optimization loop monitors
  content quality, adoption, and retention impact, detects anomalies, generates improvement
  hypotheses, runs prompt and UX experiments, and auto-implements winners. The agent finds
  the local maximum of AI content feature performance and maintains it as user behavior,
  model capabilities, and product context evolve.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving AI content adoption >=35% and acceptance rate >=60% over 6 months via autonomous agent optimization"
kpis: ["AI content adoption rate (trailing 14-day, monthly)", "Acceptance rate (trailing 30-day, monthly)", "Retention lift stability (AI users vs non-users delta sustained or growing)", "Experiment velocity (experiments completed per month)", "AI lift (cumulative acceptance rate improvement from agent-driven prompt tuning vs original prompts)", "Convergence status (consecutive low-improvement experiments)"]
slug: "ai-content-generation"
install: "npx gtm-skills add product/retain/ai-content-generation"
drills:
  - autonomous-optimization
---

# AI Content Assistant — Durable Intelligence

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The AI content generation system operates autonomously. An always-on agent loop monitors content quality metrics, adoption rates, and retention impact. When metrics plateau or degrade, the agent diagnoses root causes, generates improvement hypotheses, runs controlled experiments on system prompts and UX, evaluates results, and auto-implements winners. The system self-corrects as user behavior evolves, AI model capabilities change, and the product ships new content types.

Over 6 months, the agent maintains or improves:
- AI content adoption at 35%+ of active users (trailing 14-day window, measured monthly)
- Acceptance rate at 60%+ (trailing 30-day window, measured monthly)
- Retention lift: AI content users retain at a measurably higher rate than non-users, with the delta sustained or growing
- Model convergence: when 3 consecutive monthly optimization cycles produce <2% improvement across all metrics, the system has found its local maximum

The Durable level is fundamentally different from Scalable because the agent optimizes the system itself -- not just the outputs. It changes system prompts, UX flows, intervention timing, and content type priorities based on measured outcomes. No human decides which experiment to run next; the agent identifies the highest-leverage opportunity from the data and acts.

## Leading Indicators

- The `autonomous-optimization` loop fires daily monitoring checks without human intervention
- Weekly optimization briefs are generated and posted to Slack with metric deltas and next actions
- At least 1 experiment per month is designed, run, and evaluated by the agent
- When the agent detects acceptance rate or adoption drops, it generates hypotheses and initiates corrective experiments within 48 hours
- Prompt version registry grows: each adopted experiment adds a new entry with measured improvement
- Convergence detection: the agent identifies when successive experiments produce <2% improvement and shifts to maintenance mode

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the AI content generation play:

**Phase 1 -- Monitor (daily via n8n cron):**
1. Use `posthog-anomaly-detection` to check the play's primary KPIs: adoption rate, acceptance rate, retention lift, regeneration rate, satisfaction score
2. Compare the last 2 weeks against the 4-week rolling average
3. Classify: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
4. If normal, log to Attio. No action needed.
5. If anomaly detected, trigger Phase 2.

**Phase 2 -- Diagnose (triggered by anomaly):**
1. Pull 8-week metric history from PostHog using the `autonomous-optimization` dashboard
2. Identify which KPI is anomalous. Common root causes for this play:
   - Acceptance rate drop: AI model quality degraded, user expectations shifted, new content type launched without prompt tuning
   - Adoption rate drop: in-app discovery surfaces stale or dismissed by most users, competing feature launched that pulls attention
   - Retention lift narrowing: non-AI-users are being retained by other product improvements (good but reduces the AI feature's marginal impact)
   - Regeneration rate spike: model latency increased (users retry thinking it failed) or output quality dropped for a specific content type
3. Run `hypothesis-generation` with the anomaly context, metric history, and content type breakdown
4. Receive 3 ranked hypotheses with expected impact and risk level
5. If top hypothesis is high risk (requires changing prompts for content types affecting >50% of generations), send Slack alert for human review and STOP
6. If low or medium risk, proceed to Phase 3

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
1. If the hypothesis targets content quality: run the the ai content prompt optimization workflow (see instructions below) drill to design a prompt A/B test
   - Create a PostHog feature flag splitting generations between current prompt (control) and modified prompt (variant)
   - Primary metric: clean acceptance rate for the affected content type
   - Minimum 100 generations per variant, minimum 7 days
2. If the hypothesis targets discovery or adoption: design a UX experiment
   - Use PostHog feature flags to test a new discovery surface, tooltip placement, or onboarding flow variant
   - Primary metric: first-generation rate for non-adopters exposed to the variant
   - Minimum 200 users per variant, minimum 14 days
3. If the hypothesis targets retention: design an intervention experiment
   - Use PostHog feature flags to test a new re-engagement message, content recommendation, or usage prompt
   - Primary metric: 14-day return rate for at-risk users
   - Minimum 100 users per variant, minimum 14 days
4. Log experiment start in Attio with: hypothesis, variant description, start date, expected duration, success criteria

**Phase 4 -- Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog
2. Run `experiment-evaluation`:
   - **Adopt:** Update the live configuration. If prompt experiment: deploy the new system prompt and add to the prompt version registry. If UX experiment: roll out the winning variant to 100%. If intervention: update the n8n intervention workflow. Log the change in Attio.
   - **Iterate:** The result showed a signal but not statistical significance. Generate a refined hypothesis building on this result. Return to Phase 2.
   - **Revert:** The variant performed worse. Disable it, restore control. Log the failure and reasoning. Return to Phase 1 monitoring.
3. Store full evaluation in Attio (decision, confidence, reasoning, metric deltas, prompt version if applicable)

**Phase 5 -- Report (weekly via n8n cron):**
1. Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
2. Calculate net metric change from all adopted changes this week
3. Generate weekly optimization brief:
   - Current adoption rate, acceptance rate, retention lift, and trend direction
   - Active experiments and their status
   - Adopted changes and their measured impact
   - Cumulative AI lift (acceptance rate improvement from all agent-driven prompt changes vs original prompts)
   - Current distance from estimated local maximum
   - Recommended focus for next week
4. Post to Slack and store in Attio

### 2. Deploy the AI content health monitoring layer

Run the `autonomous-optimization` drill to create the measurement infrastructure the optimization loop depends on:

1. Build the 8-panel AI content health dashboard in PostHog (generation volume, acceptance rate, edit rate, regeneration rate, satisfaction score, generation-to-publish funnel, content type breakdown, retention lift)
2. Create the 5 health cohorts (AI Power Users, AI Experimenters, AI Churned, AI Frustrated, AI Non-Adopters)
3. Deploy the weekly health check n8n workflow that compares trailing 7-day metrics to 4-week rolling averages and fires Slack alerts for critical degradation
4. Configure retention correlation tracking: maintain the weekly comparison of 30/60/90-day retention between AI content users and non-users

This dashboard is the agent's primary observation layer. Every Phase 1 monitoring check reads from these panels.

### 3. Maintain the prompt optimization pipeline

Run the the ai content prompt optimization workflow (see instructions below) drill in maintenance mode:

1. Keep the prompt version registry up to date: every adopted prompt change gets a new entry with content type, change description, before/after acceptance rate, and date
2. When new content types are added to the product, the agent proactively generates baseline prompts using existing high-performing prompts as templates, then runs an initial optimization cycle
3. When the AI model is upgraded (e.g., new model version deployed), the agent immediately runs acceptance rate checks across all content types and initiates optimization if any content type shows >5pp regression
4. Monthly: review the full prompt registry. If any content type's acceptance rate has stagnated for 2+ months, the agent generates new hypotheses specifically targeting that content type

### 4. Implement convergence detection

Configure the agent to detect when the AI content system has reached its local maximum:

1. Track the acceptance rate improvement from each prompt optimization experiment
2. Track the adoption improvement from each UX or discovery experiment
3. Track the retention improvement from each intervention experiment
4. When 3 consecutive experiments across all categories produce <2% improvement:
   - The play has converged. Log: "AI content generation feature is optimized. Current adoption: [X]%. Acceptance rate: [Y]%. Retention lift: [Z]pp. Further improvement requires strategic changes (new AI models, new content types, fundamental product UX changes) rather than tactical optimization."
   - Reduce monitoring frequency from daily to weekly
   - Reduce experiment cadence from monthly to quarterly
   - Shift agent focus to anomaly detection and maintaining current performance
   - Continue generating weekly briefs but flag them as "maintenance mode"

### 5. Evaluate sustainability

This level runs continuously. Monthly review:

1. Is adoption still >=35% at the current user base size?
2. Is acceptance rate still >=60%?
3. Is the retention lift delta sustained or growing?
4. Are weekly optimization briefs being generated? Are they actionable?
5. Has the system converged? If so, is it maintaining performance in maintenance mode?

If metrics sustain or improve over 6 months via agent-driven optimization, the play is durable.

If metrics decay despite agent optimization, the system needs strategic input:
- **Model upgrade**: The current AI model may have hit its quality ceiling for certain content types. Evaluate newer models.
- **New content types**: Users may need AI assistance for content types not yet supported. Analyze manual content creation patterns to identify gaps.
- **UX redesign**: The feature's discoverability surfaces may have fatigued. Users have dismissed all tooltips and announcements. A deeper product integration (AI suggestions inline in the editor) may be needed.
- **Competitive pressure**: If users are generating content in external tools instead, investigate what those tools do better and feed findings to the product team.

## Time Estimate

- 20 hours: Deploy and configure the autonomous optimization loop (step 1)
- 10 hours: Build the health monitoring dashboard and cohorts (step 2)
- 10 hours: Configure the prompt optimization maintenance pipeline (step 3)
- 5 hours: Convergence detection configuration (step 4)
- 105 hours: Ongoing agent monitoring, experiment cycles, brief generation, and evaluation over 6 months (step 5)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Health dashboard, experiments, feature flags, anomaly detection, cohorts | Free tier: 1M events/mo. https://posthog.com/pricing |
| n8n | Daily monitoring cron, weekly reporting, health check automation | Free (self-hosted) or $20/mo (cloud). https://n8n.io/pricing |
| Attio | Experiment logging, prompt version registry, optimization audit trail | Free tier: 3 users. https://attio.com/pricing |
| Intercom | In-app discovery surfaces, re-engagement messages, expansion prompts | Starter: ~$39/seat/mo. https://www.intercom.com/pricing |
| Loops | Re-engagement emails, intervention emails | Free tier: 1,000 contacts. https://loops.so/pricing |
| Anthropic API | Hypothesis generation, experiment evaluation, weekly optimization briefs | Pay-per-use: ~$3/MTok input, ~$15/MTok output (Claude Sonnet). https://www.anthropic.com/pricing |

## Drills Referenced

- `autonomous-optimization` -- the core detect-diagnose-experiment-evaluate-report loop that makes Durable fundamentally different from Scalable
- the ai content prompt optimization workflow (see instructions below) -- analyzes rejection patterns, generates prompt improvement hypotheses, runs prompt A/B tests, and maintains the prompt version registry
- `autonomous-optimization` -- the measurement layer providing the dashboards, cohorts, and alerts the optimization loop reads from
