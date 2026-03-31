---
name: technical-deep-dive-demo-scalable
description: >
  Technical Deep-Dive Demo — Scalable Automation. Find the 10x multiplier: n8n-orchestrated demo
  prep pipeline, A/B testing of demo module sequences, performance monitoring across the full
  discovery-to-POC funnel, and automated post-demo intelligence extraction from transcripts.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct, Product"
level: "Scalable Automation"
time: "64 hours over 2 months"
outcome: "Technical demos on ≥75% of technical opportunities at scale over 2 months with POC conversion ≥45% and demo-to-technical-validation time reduced by 30%"
kpis: ["Technical demo completion rate at scale", "POC conversion rate", "Technical validation speed (days)", "Demo module effectiveness score", "Solutions engineer leverage ratio"]
slug: "technical-deep-dive-demo"
install: "npx gtm-skills add sales/connected/technical-deep-dive-demo"
drills:
  - demo-performance-monitor
  - demo-prep-automation
  - ab-test-orchestrator
---
# Technical Deep-Dive Demo — Scalable Automation

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product

## Outcomes
Maintain technical demo coverage at 75%+ of technical opportunities while scaling to 3-5x Baseline volume. POC conversion rate holds at 45%+ and time from demo to technical validation drops by 30%. The agent orchestrates the entire demo pipeline: auto-generates prep, monitors the funnel for degradation, extracts intelligence from demo transcripts, and runs A/B experiments on demo module sequencing.

## Leading Indicators
- Demo prep generation time stays under 15 minutes per opportunity (agent efficiency)
- Demo transcript analysis surfaces reusable insights within 24 hours of each demo
- A/B test on module ordering produces a statistically significant winner within 4 weeks
- Pain-to-feature mapping accuracy improves as historical demo data feeds the model
- Post-demo follow-up package open rates exceed 70%

## Instructions

### 1. Deploy the full demo conversion funnel monitor
Run the `demo-performance-monitor` drill to create an always-on monitoring system for the technical demo pipeline. This builds:

- A PostHog funnel: `discovery_call_completed` -> `technical_demo_scheduled` -> `technical_demo_completed` -> `poc_started` -> `proposal_requested` -> `deal_closed_won`
- Breakdown by: attendee roles, modules shown, tech stack match quality, sandbox usage, demo duration
- A PostHog dashboard with panels: funnel conversion rates, demo-to-POC trend (weekly), module effectiveness scatter plot, time-to-demo histogram, demo duration vs outcome correlation, weekly volume
- n8n monitoring workflows: daily cron checks for conversion rate anomalies (warning at -15%, critical at -30%), event-triggered alerts when demos result in `no_interest`, follow-up reminders when recap engagement is high but no POC within 48 hours
- Weekly pain-to-feature effectiveness report: which demo modules and technical proof points drive the highest POC conversion, which ones to stop leading with

### 2. Scale demo prep with transcript-driven intelligence
Run the `demo-prep-automation` drill alongside `technical-demo-content-assembly` (already running from Baseline) to add transcript-driven intelligence:

- After each discovery call, Fireflies transcript is automatically processed
- Pain points, technical requirements, and BANT scores are extracted
- The demo prep agent combines transcript intelligence with tech stack data to generate an even more targeted demo script
- Pain-to-feature mapping draws on historical demo outcome data: "For prospects with {pain_category}, showing {module} first converts at {rate}%"

Configure n8n to chain these drills:
1. Fireflies transcript webhook triggers `demo-prep-automation` (pain extraction + feature mapping)
2. Output feeds into `technical-demo-content-assembly` (technical script generation)
3. Combined output stored in Attio as a unified demo prep document
4. Slack notification to founder with prep summary and recommended emphasis areas

### 3. Run A/B tests on demo module sequencing
Run the `ab-test-orchestrator` drill to test which demo module ordering produces the highest POC conversion. Set up experiments:

**Experiment 1: Architecture-first vs API-first**
- Control: Architecture overview -> API walkthrough -> Integration demo -> Security review
- Variant: API walkthrough -> Integration demo -> Architecture overview -> Security review
- Hypothesis: Engineer-heavy audiences convert better when they see working code before abstract architecture
- Minimum sample: 20 demos per variant (40 total)
- Success metric: POC conversion rate

**Experiment 2: Security timing**
- Control: Security review at the end (traditional)
- Variant: Security review after architecture (address compliance concerns early)
- Hypothesis: Enterprise prospects with security-sensitive industries convert faster when compliance is addressed upfront
- Segment: Only run on deals where attendees include security/compliance roles
- Minimum sample: 15 demos per variant
- Success metric: Days from demo to POC start

**Experiment 3: Live API calls vs pre-recorded**
- Control: Execute live API calls during the demo
- Variant: Show pre-recorded API call videos with voiceover, saving live time for Q&A
- Hypothesis: More Q&A time increases engagement and conversion
- Minimum sample: 20 demos per variant
- Success metric: Technical questions asked AND POC conversion rate

Use PostHog feature flags to assign each demo to a variant. Log the variant in the `technical_demo_completed` event properties. Run each experiment for at least 4 weeks before evaluating.

### 4. Build the demo intelligence library
Create an n8n workflow that runs after every demo:

1. Pull the Fireflies transcript of the demo call
2. Use Claude to extract: questions asked (with answers given), objections raised, features that generated the most discussion, competitor mentions, technical blockers identified, verbal commitments made
3. Score the demo on 4 dimensions: pain coverage (did the demo address stated pains), technical depth (were questions substantive), engagement (prospect talk time ratio), and close attempt (was a next step proposed and agreed)
4. Store the scored transcript analysis as an Attio note tagged `demo-intelligence`
5. Aggregate across all demos monthly: build a ranked list of most effective technical proof points, most common objections, and most frequent technical blockers

This intelligence feeds back into demo prep generation: the agent uses historical patterns to recommend which modules to emphasize and which objections to prepare for.

### 5. Scale to 3-5x volume
With automated prep, monitoring, and A/B testing running, increase technical demo throughput:

- Target 30-50 technical demos over the 2-month period (vs ~12 at Baseline)
- Agent handles all prep, transcript analysis, follow-up packaging, and funnel monitoring
- Founder focuses exclusively on delivering the live demo and building the technical relationship
- If volume exceeds founder capacity, use the demo intelligence library to onboard a solutions engineer: the library provides demo scripts, common questions, proven module ordering, and scored examples of effective demos

### 6. Evaluate against threshold
After 2 months, run the threshold evaluation:

- Demo coverage ≥75% of technical opportunities
- POC conversion ≥45%
- Demo-to-technical-validation time reduced ≥30% vs Baseline
- A/B test results: at least 1 statistically significant winner implemented

**Guardrails:** If POC conversion drops below 40% for 2 consecutive weeks, the `demo-performance-monitor` fires an alert. Pause scaling and diagnose: check if demo quality is degrading at volume, if new prospect segments behave differently, or if the market shifted.

If all metrics hold, proceed to Durable.

---

## Time Estimate
- Demo performance monitor setup: 8 hours
- Transcript-driven prep pipeline: 6 hours
- A/B test design and configuration: 8 hours
- Demo execution at scale: 30 hours (~50 demos x 35 min average)
- Intelligence library build and analysis: 6 hours
- Monthly review and optimization: 6 hours

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal pipeline, contact management, demo intelligence storage | Plus $29/user/mo |
| PostHog | Funnel tracking, feature flags for A/B tests, dashboards, anomaly detection | Free up to 1M events/mo; paid $0.00005/event beyond |
| n8n | Orchestration — demo prep pipeline, monitoring crons, transcript processing, A/B routing | Pro €60/mo (10,000 executions) |
| Clay | Tech stack detection and enrichment at volume | Launch $185/mo or Growth $495/mo if credit usage high |
| Fireflies | Transcription for discovery calls and demo calls | Pro $10/user/mo (annual); Business $29/user/mo for video |
| Anthropic Claude API | Demo script generation, transcript analysis, intelligence extraction | Sonnet 4.6: $3/$15 per 1M tokens (~$25/mo at 50 demos + transcript analysis) |
| Cal.com | Scheduling with webhook triggers | Free or Teams $15/user/mo |

**Play-specific cost:** ~$150-350/mo (n8n Pro + Clay credits + Claude API usage + Fireflies Business; scales with demo volume)

## Drills Referenced
- `demo-performance-monitor` — always-on monitoring of the discovery-to-demo-to-deal funnel with anomaly alerts, pain-to-feature effectiveness ranking, and demo quality scoring from transcripts
- `demo-prep-automation` — auto-generates personalized demo prep from discovery call transcripts with pain-to-feature mapping, ROI calculations, and structured demo flow
- `ab-test-orchestrator` — designs, runs, and evaluates A/B experiments on demo module sequencing using PostHog feature flags
