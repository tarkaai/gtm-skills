---
name: hackathon-sponsorship-hosting-durable
description: >
  Hackathon Sponsorship -- Durable Intelligence. Always-on AI agents continuously optimize
  challenge design, recruitment targeting, prize structures, and nurture sequences. The
  autonomous-optimization drill runs the core loop: detect metric anomalies, generate improvement
  hypotheses, run A/B experiments, evaluate results, auto-implement winners. Weekly optimization
  briefs. Converges when successive experiments produce <2% improvement.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events, Communities"
level: "Durable Intelligence"
time: "160 hours over 12 months"
outcome: "Sustained >=35 qualified leads/quarter and growing developer community over 12 months via AI-optimized challenges, recruitment, and nurture"
kpis: ["Qualified leads per quarter", "AI experiment win rate", "Cost per qualified lead trend", "Community growth rate", "Product adoption rate from hackathons"]
slug: "hackathon-sponsorship-hosting"
install: "npx gtm-skills add Marketing/SolutionAware/hackathon-sponsorship-hosting"
drills:
  - autonomous-optimization
  - hackathon-performance-monitor
  - hackathon-optimization-reporting
---

# Hackathon Sponsorship -- Durable Intelligence

> **Stage:** Marketing > SolutionAware | **Motion:** MicroEvents | **Channels:** Events, Communities

## Outcomes

The hackathon series runs autonomously. AI agents continuously monitor series health, detect when recruitment or conversion metrics degrade, experiment with improved challenge designs, recruitment targeting, prize structures, and nurture sequences, and auto-implement winners. The `autonomous-optimization` drill runs the core loop: detect metric anomalies in hackathon performance -> generate improvement hypotheses -> run A/B experiments -> evaluate results -> auto-implement winners. Weekly optimization briefs report what changed and why. The developer community becomes a self-sustaining lead engine. The system converges when successive experiments produce <2% improvement, indicating the hackathon program has reached its local maximum for your market and developer audience.

## Leading Indicators

- Autonomous optimization loop running, generating at least 1 experiment per hackathon cycle
- Qualified leads per quarter sustained at 35+ or growing
- Cost per qualified lead trending downward or stable
- Developer community active ratio (% posting in last 30 days) sustained above 15%
- At least 1 experiment adopted in the first quarter (challenge design change, recruitment targeting adjustment, prize restructure, or nurture sequence improvement)
- Weekly optimization briefs being generated and posted to Slack
- Cross-hackathon A/B test synthesis report produced after every 2 events
- Convergence detection active -- system can identify when optimization has plateaued for each variable

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the hackathon sponsorship play. This creates the always-on agent loop with 5 phases:

**Phase 1 -- Monitor (weekly via n8n cron, plus post-event triggers):**
The agent checks hackathon play KPIs using `posthog-anomaly-detection`:
- Registrations per hackathon (vs 4-event rolling average)
- Submission rate (vs target 40%)
- Qualified leads per hackathon (vs target 10+)
- Post-hackathon product adoption rate (30-day retention)
- Cost per qualified lead (trending)
- Community growth rate and active ratio
- Repeat participation rate
- Recruitment channel yield by source

Classify each metric: normal (within +/-10% of rolling average), plateau (+/-2% for 2+ hackathons), drop (>20% decline), spike (>50% increase). If anomaly detected, trigger Phase 2.

**Phase 2 -- Diagnose (triggered by anomaly):**
The agent gathers context from Attio (current challenge themes, recruitment channels, prize structures, nurture sequences, community health) and metric history from PostHog. Runs `hypothesis-generation` to produce 3 ranked hypotheses. Examples of hackathon-specific hypotheses:

- "Registration declined because the challenge theme is too similar to the last 2 hackathons -- developer fatigue. Hypothesis: switch to a completely different product capability and target a new developer sub-segment."
- "Submission rate dropped from 42% to 28%. Hypothesis: the challenge was too difficult for the 1-week async format. Test a 2-week duration or provide more starter code."
- "Qualified lead conversion from nurture dropped. Hypothesis: Tier 2 email sequence is too generic. Test personalization based on specific product features each participant used."
- "Cost per qualified lead increased 40%. Hypothesis: Clay enrichment is targeting developers who register but do not submit. Refine enrichment criteria to weight GitHub activity more heavily."
- "Community active ratio dropped below 10%. Hypothesis: inter-event engagement is stale. Test weekly technical challenges or mini-hackathons between main events."

Store hypotheses in Attio. If risk = "high" (e.g., fundamentally changing the hackathon format), send Slack alert for human review. If risk = "low" or "medium", proceed automatically.

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
Design and run the experiment. Hackathon experiments are unique because you typically cannot A/B test within a single event -- instead, you test across events:

- **Challenge design experiments:** Apply the variant to the next hackathon. Compare results to the previous 2 hackathons (control). Requires 2+ hackathons with the variant to reach confidence.
- **Recruitment experiments:** These CAN be A/B tested within a single hackathon. Split the Clay enrichment list into control and variant targeting criteria. Compare registration-to-submission rates.
- **Prize structure experiments:** Apply variant to next hackathon. Compare submission rate and quality to control.
- **Nurture sequence experiments:** Use PostHog feature flags to split participants into control and variant nurture sequences. Measure reply rate, meeting rate, and adoption rate.
- **Format experiments:** Test duration, team structure, or mentorship model changes. Cross-event comparison required.

Log experiment start in Attio with: hypothesis, hackathon slug(s), start date, expected evaluation date, success criteria.

**Phase 4 -- Evaluate (triggered by experiment completion):**
Pull results from PostHog. Run `experiment-evaluation`:
- **Adopt:** Variant outperforms control by 5%+ with sufficient data. Update the default configuration. Log the change.
- **Iterate:** Results inconclusive. Generate a refined hypothesis. Return to Phase 2.
- **Revert:** Control outperforms variant. Restore previous approach. Log the failure. Return to Phase 1.
- **Extend:** Insufficient data (common for cross-event experiments). Run for another hackathon cycle.

Store full evaluation in Attio with decision, confidence, reasoning.

**Phase 5 -- Report (weekly via n8n cron):**
Generate weekly optimization brief via the `hackathon-optimization-reporting` drill.

Estimated time for setup: 12 hours. Then always-on.

### 2. Maintain hackathon performance monitoring

Continue running the `hackathon-performance-monitor` drill from Scalable. At Durable level, enhance it:

- **Cross-event pattern detection:** When 2+ consecutive hackathons show the same metric degradation (e.g., declining submission rate), flag it as a systemic issue rather than a single-event anomaly. Feed this into the autonomous optimization loop as a high-priority signal.
- **Predictive registration modeling:** Use historical data to predict registration counts and submission rates for upcoming hackathons based on: theme similarity to past events, time of year, promotion budget, and community size. Alert if predictions fall below targets so the team can boost recruitment before the event.
- **Developer lifecycle tracking:** Map the full journey from first hackathon registration to product adoption to paid conversion. Identify the typical timeline and which touchpoints accelerate conversion. Use this to optimize the nurture sequences and community engagement strategies.

Estimated time: 8 hours enhancement, then always-on.

### 3. Deploy hackathon-specific optimization reporting

Run the `hackathon-optimization-reporting` drill. This adds the play-specific reporting layer on top of the generic autonomous optimization:

- **Weekly optimization briefs** with hackathon-specific context: funnel health, community pulse, active experiments, convergence status
- **Monthly developer community health reports**: size, active ratio, alumni retention, organic project sharing, community-to-customer pipeline
- **Cross-hackathon A/B test synthesis**: after every 2 hackathons, compile all experiment results, identify which variables have the highest optimization ROI, and flag unexplored variables
- **Product adoption funnel deep-dive**: quarterly analysis comparing hackathon-sourced users to other acquisition channels on activation, retention, and expansion metrics

Estimated time: 6 hours setup, then always-on.

### 4. Guardrails (CRITICAL)

The autonomous optimization loop must respect these constraints:

- **Rate limit:** Maximum 2 active experiments at a time (1 cross-event experiment + 1 within-event experiment). Never stack multiple cross-event experiments testing the same variable.
- **Revert threshold:** If qualified leads per hackathon drop >40% compared to the series average, auto-revert the most recent experiment and alert the team.
- **Human approval required for:**
  - Prize budget changes >30%
  - Switching from virtual to in-person or vice versa
  - Challenge themes that target a completely new developer audience
  - Any experiment the hypothesis generator flags as "high risk"
  - Community strategy changes that affect all members
- **Cooldown:** After a failed cross-event experiment, wait 1 full hackathon cycle before testing a new hypothesis on the same variable.
- **Maximum experiments per quarter:** 4. If all 4 fail, pause optimization and flag for human strategic review.
- **Never optimize what is not measured:** If a metric does not have PostHog tracking, fix tracking first before running experiments on it.
- **Minimum data:** Do not evaluate cross-event experiments with fewer than 2 hackathons per variant.

### 5. Convergence detection

The optimization loop runs indefinitely at Durable level but should detect convergence -- when the hackathon program has reached its local maximum:

- Track the improvement percentage of each successive adopted experiment
- When 3 consecutive experiments produce <2% improvement on their target metric, declare convergence for that variable category
- At convergence for all variable categories:
  1. Reduce monitoring frequency from weekly to bi-weekly
  2. Reduce experiment frequency to 1 per 2 hackathons (maintenance mode)
  3. Report: "Hackathon program is optimized. Current performance: {metrics}. Qualified leads per quarter: {N}. Cost per lead: ${X}. Community size: {N} ({X}% active). Further gains require strategic changes (new developer segment, new product capabilities, co-marketing partnerships, geographic expansion) rather than tactical optimization."
- Continue watching for market shifts that could break convergence: new competitor hackathons, changes in developer preferences, product updates that open new challenge possibilities

### 6. Evaluate sustainability

Measure against threshold: Sustained >=35 qualified leads/quarter and growing developer community over 12 months.

Monthly review checklist:
- Qualified leads this quarter: on track for 35+?
- Cost per qualified lead: stable or declining?
- Community growth: positive trend?
- Community active ratio: above 15%?
- Product adoption from hackathons: sustained at 25%+ 30-day retention?
- Autonomous optimization: experiments running and producing results?
- Developer sentiment: post-hackathon NPS above 60?

This level runs continuously. If metrics sustain or improve, the play is durable. If metrics decay, diagnose whether the issue is developer audience saturation, challenge fatigue, competitive hackathon landscape changes, or product-market fit drift.

## Time Estimate

- Autonomous optimization setup: 12 hours
- Performance monitoring enhancement: 8 hours
- Optimization reporting setup: 6 hours
- Hackathon execution (4 per year x 6 hours): 24 hours
- Ongoing monitoring, experiment review, community management, and strategic oversight: ~110 hours over 12 months (~2-3 hours/week)

**Total: ~160 hours over 12 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Devpost or Luma | Hackathon platform -- registration, submissions, judging | Devpost: Free. Luma Plus: $59/mo annual. [devpost.com](https://devpost.com) / [luma.com/pricing](https://luma.com/pricing) |
| Clay | Developer prospect enrichment at scale | Growth: $495/mo (15,000 actions). [clay.com/pricing](https://www.clay.com/pricing) |
| Riverside | Recording kickoffs and demo days | Standard: $19/mo annual. [riverside.com/pricing](https://riverside.com/pricing) |
| Attio | CRM -- participant records, experiment logs, community tracking, pipeline | Standard stack (excluded) |
| PostHog | Dashboards, funnels, feature flags, experiments, anomaly detection | Standard stack (excluded) |
| n8n | Orchestration -- optimization loop, health monitor, reporting, recruitment | Standard stack (excluded) |
| Loops | Nurture sequences and recruitment broadcasts | Standard stack (excluded) |
| Cal.com | Mentor office hours booking | Standard stack (excluded) |
| Anthropic API | Claude for optimization loop (hypothesis generation, experiment evaluation, weekly briefs, content generation) | ~$80-150/mo at Durable volume. [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Play-specific cost: ~$750-1,100/mo** (Clay $495 + Luma $59 + Riverside $19 + Anthropic ~$115 + prizes ~$1,000/quarter amortized + promotion ~$100-300/mo)

## Drills Referenced

- `autonomous-optimization` -- the core always-on loop: monitor metrics, diagnose anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, generate weekly briefs
- `hackathon-performance-monitor` -- enhanced at Durable with cross-event pattern detection, predictive registration modeling, and developer lifecycle tracking
- `hackathon-optimization-reporting` -- weekly optimization briefs, monthly community health reports, cross-hackathon A/B test synthesis, and product adoption funnel analysis
