---
name: demo-storytelling-framework-durable
description: >
  Demo Storytelling Framework — Durable Intelligence. Always-on AI agents continuously optimize story
  selection, narrative structure, and delivery patterns. The autonomous-optimization drill runs the core
  loop: detect metric anomalies in storytelling KPIs, generate improvement hypotheses, run A/B
  experiments, evaluate results, and auto-implement winners. Weekly optimization briefs track convergence
  toward the local maximum of demo engagement and conversion.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Product"
level: "Durable Intelligence"
time: "130 hours over 6 months"
outcome: "Sustained or improving demo-to-proposal conversion (>=12% lift) over 6 months with <2% variance in successive optimization cycles, indicating convergence at the local maximum of story-driven demo effectiveness"
kpis: ["Demo-to-proposal conversion lift (sustained)", "Autonomous experiment win rate", "Story matching prediction accuracy", "Engagement score trend", "Optimization convergence rate"]
slug: "demo-storytelling-framework"
install: "npx gtm-skills add sales/connected/demo-storytelling-framework"
drills:
  - autonomous-optimization
  - story-intelligence-reporting
---

# Demo Storytelling Framework — Durable Intelligence

> **Stage:** Sales → Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Product

## Outcomes

Always-on AI agents finding the local maximum. The storytelling demo program runs itself: story matching, narrative generation, engagement analysis, and effectiveness reporting all execute autonomously. The `autonomous-optimization` drill runs the core loop: detect metric anomalies in storytelling KPIs, generate improvement hypotheses, run A/B experiments, evaluate results, and auto-implement winners. Weekly optimization briefs track convergence. The program converges when successive experiments produce <2% improvement — at that point, story-driven demos have reached their optimal performance given the current story library, prospect mix, and market conditions.

**Pass threshold:** Sustained or improving demo-to-proposal conversion (>=12% lift) over 6 months with <2% variance in successive optimization cycles, indicating convergence at the local maximum of story-driven demo effectiveness.

## Leading Indicators

- Autonomous optimization loop runs daily without manual intervention
- Weekly optimization briefs are generated and posted to Slack
- At least 2 experiments per month are initiated, evaluated, and decided
- Story matching prediction accuracy improves over time (AI-selected stories correlate with strong engagement)
- Convergence signal: last 3 experiments produced <2% improvement each

## Instructions

### 1. Deploy Autonomous Optimization

Run the `autonomous-optimization` drill configured for the storytelling demo program. This is the drill that makes Durable fundamentally different from Scalable.

**Configure the optimization loop:**

**Phase 1 — Monitor (daily via n8n cron):**
- Use `posthog-anomaly-detection` to check storytelling KPIs:
  - Demo-to-proposal conversion rate (storytelling demos)
  - Average engagement score (from Gong analysis)
  - Story connection rate (% of demos where prospect related to story)
  - Story matching accuracy (% of top-matched stories that produced engagement >=60)
  - Emotional connection rate
  - Story library coverage (% of demos with match score >=50)
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within +-10%), plateau (+-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Gather context from Attio: current story library, recent matching results, narrative structures in use, experiment history
- Pull 8-week metric history from PostHog
- Run `hypothesis-generation` with the anomaly data and context
- Example hypotheses the system might generate:
  - "Engagement scores dropped 18% over 3 weeks. Hypothesis: The top-used story (Acme onboarding) is fatigued after 3 months of heavy use. Test rotating in a newer story for the same segment."
  - "Demo-to-proposal rate plateaued at 35%. Hypothesis: The closing bridge question is too soft. Test a direct proposal offer vs current open-ended question."
  - "Story matching accuracy declined to 55%. Hypothesis: Pain overlap scoring weight is too low relative to industry match. Increase pain_overlap weight from 30 to 40 and reduce industry_match from 25 to 15."
  - "Emotional connection rate spiked +40% this month. Hypothesis: The new backward-storytelling variant (results-first) is producing stronger emotional peaks. Adopt as default for all segments where it's been tested."
- Store hypotheses in Attio. If risk = "high", alert human. If "low" or "medium", proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Use `posthog-experiments` to create a feature flag splitting traffic between control and variant
- Implement the variant using the appropriate mechanism:
  - If testing story selection: modify the matching prompt or weights for the variant group
  - If testing narrative structure: generate variant prep docs with the new structure
  - If testing closing technique: modify the closing bridge section of the prep doc template
  - If testing story freshness: rotate in a new story for the variant group
- Set experiment duration: minimum 7 days or 15+ demos per variant, whichever is longer
- Log experiment in Attio with: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run `experiment-evaluation` to determine: Adopt, Iterate, Revert, or Extend
- If Adopt: update the live configuration (matching weights, narrative template, or story rotation). Log the change. Move to Phase 5.
- If Iterate: generate a new hypothesis building on this result. Return to Phase 2.
- If Revert: restore control configuration. Log the failure with reasoning. Return to Phase 1.
- Store the full evaluation (decision, confidence, reasoning) in Attio

**Phase 5 — Report (weekly via n8n cron):**
- Generate weekly optimization brief:
  - Anomalies detected this week
  - Experiments running, completed, decided
  - Net impact on storytelling KPIs
  - Current distance from estimated local maximum
  - Story library health (gaps, fatigued stories, rising stories)
  - Recommended focus for next week
- Post to Slack, store in Attio

### 2. Maintain Story Intelligence Reporting

Continue running the `story-intelligence-reporting` drill from Scalable. The reporting layer provides the data substrate that the optimization loop reads. Enhancements for Durable:

- Add a "Story Lifecycle" panel to the dashboard: time since creation, usage trend, effectiveness trend per story. Detect when stories enter decline phase automatically.
- Add a "Narrative Pattern" panel: which narrative structures (4-phase, backward, quote-first) are currently winning, and what the optimizer is testing.
- Add a "Convergence Tracker" panel: magnitude of improvement from each adopted experiment over time. When the last 3 produce <2%, show convergence status.

### 3. Configure Optimization Guardrails

Apply the guardrails from the `autonomous-optimization` drill to the storytelling program:

- **Rate limit:** Maximum 1 active experiment at a time on the storytelling program
- **Revert threshold:** If demo-to-proposal conversion drops below 5% lift (vs pre-storytelling baseline) during any experiment, auto-revert immediately
- **Human approval required for:**
  - Retirement of any story from the library (stories are customer relationships — don't auto-retire)
  - Changes to story matching that affect which customer stories are shown to enterprise prospects (brand sensitivity)
  - Any change the hypothesis generator flags as "high risk"
  - New narrative structures that fundamentally alter the demo format (e.g., eliminating the story entirely for a segment)
- **Cooldown:** After a failed experiment, wait 7 days before testing the same variable
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for human strategic review
- **Never optimize what isn't measured:** All storytelling events must have PostHog tracking before experiments can target them

### 4. Build Predictive Story Matching

As the optimization loop accumulates data over months, enhance the matching model with prediction:

- Train on historical data: which story + prospect combinations (by industry, size, pain themes, stakeholder role) produced the highest engagement and conversion?
- Track `story_match_prediction_accuracy`: % of demos where the AI-selected story produced engagement score >=60
- If accuracy < 60%, the matching model needs recalibration — the optimizer should generate a hypothesis about which scoring dimensions or weights to adjust
- Eventually, the model should predict: "For {industry} prospects at {size} companies with {pain theme}, use {Story X} with {narrative structure Y}. Expected engagement score: {Z}."
- Feed prediction confidence into the prep doc: if confidence is high, present one story. If confidence is low (similar scores for multiple stories), present 2 options and let the rep choose.

Log prediction accuracy as a PostHog metric so the optimizer can track and improve it over time.

### 5. Automated Story Generation Pipeline

As the program matures, automate the creation of new stories:

- When the optimizer detects a story gap (segment with no matching story and declining match scores), trigger an automated pipeline:
  1. Query Attio for customers in the gap segment who have strong usage metrics and high NPS
  2. If a recent Fireflies transcript exists (QBR, check-in), extract a story automatically using the `story-library-curation` drill
  3. Score the extracted story for quality: does it have quantified results? Direct quotes? Clear challenge-solution-result arc?
  4. If quality passes: add to the library as a draft and flag for human review
  5. If no transcript exists: schedule a brief customer call and notify the team

This keeps the story library fresh without manual curation effort.

### 6. Monitor Convergence

The optimization loop should detect when the storytelling program has reached its local maximum:

- Track the magnitude of improvement from each adopted experiment
- If the last 3 consecutive experiments each produced <2% improvement:
  1. The program is converged — current performance is near-optimal
  2. Reduce monitoring frequency from daily to weekly
  3. Reduce experiment frequency from 4/month to 1/month (maintenance mode)
  4. Generate a convergence report:
     ```
     Storytelling Demo Program — Converged

     Current demo-to-proposal lift: {X}% (vs pre-storytelling baseline)
     Current average engagement score: {Y}/100
     Current story matching accuracy: {Z}%
     Best-performing story: {title} ({conversion_rate}% proposal rate)
     Best-performing narrative structure: {structure_name}

     The program has reached its local maximum. Further gains require
     strategic changes (new product capabilities, new market segments,
     or fundamentally different demo formats) rather than tactical
     story and narrative optimization.
     ```
  5. Post the convergence report to Slack and store in Attio

### 7. Handle Strategic Shifts

When external conditions change (new product launch, new market entry, competitive disruption), the optimizer should detect the shift via metric anomalies and recommend a strategic review:

- If engagement scores drop >25% across all stories: market conditions or product positioning may have shifted. Stories referencing old capabilities need updating.
- If a new competitor enters and prospects start asking about them during demos: the stories need competitive positioning elements. The optimizer should hypothesize adding a "why they chose us over {competitor}" element to the narrative.
- If the company launches a new product line: new stories are needed immediately. Trigger the automated story generation pipeline for the new product.
- In all cases: alert the founder that tactical optimization is insufficient and strategic review is needed. Provide the data to support the diagnosis.

## Time Estimate

- 15 hours: Autonomous optimization setup (n8n workflows, PostHog experiments, guardrails)
- 8 hours: Enhanced story intelligence dashboard and convergence tracking
- 5 hours: Predictive matching model calibration
- 5 hours: Automated story generation pipeline
- 80 hours: Ongoing optimization over 6 months (~3 hours/week for monitoring, experiment design, evaluation)
- 10 hours: Monthly strategic reviews (human reviews optimization brief, approves changes)
- 7 hours: Convergence analysis and maintenance mode transition

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — story library, deal tracking, experiment logging | $29/user/mo (Plus) or $59/user/mo (Pro) — [attio.com/pricing](https://attio.com/pricing) |
| PostHog | Analytics — dashboards, experiments, anomaly detection, feature flags | Free up to 1M events, then usage-based — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Automation — optimization loop, story refresh, intelligence workflows | $60/mo (Pro, 10K executions) — [n8n.io/pricing](https://n8n.io/pricing) |
| Gong | Conversation intelligence — engagement scoring | $100-150/user/mo — [gong.io/pricing](https://www.gong.io/pricing/) |
| Fireflies | Transcription — discovery calls, story extraction | $18/user/mo (Pro) — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Anthropic API | AI — story matching, narrative generation, hypothesis generation, evaluation | Usage-based, ~$20-50/mo — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** ~$300-550/mo. Primary cost drivers: Gong ($100-150), n8n Pro ($60), Anthropic API (~$40), Fireflies ($18).

## Drills Referenced

- `autonomous-optimization` — the core optimization loop: detect anomalies in storytelling KPIs, generate hypotheses, run A/B experiments, evaluate results, and auto-implement winners. Weekly optimization briefs. Converges when successive experiments produce <2% improvement.
- `story-intelligence-reporting` — track story effectiveness, build performance dashboards, generate intelligence briefs, and provide the data substrate the optimization loop reads from.
