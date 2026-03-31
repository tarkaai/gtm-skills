---
name: podcast-launch-distribution-durable
description: >
  Branded Podcast Launch — Durable Intelligence. Always-on AI agents autonomously optimize topic selection,
  guest targeting, promotion mix, and episode format to sustain listener growth and lead generation.
stage: "Marketing > Problem Aware"
motion: "Founder Social Content"
channels: "Content, Social"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained listener growth (>=15% QoQ) and >=25 qualified leads/quarter over 12 months via AI-driven topic selection and promotion"
kpis: ["Sustained listener growth rate (QoQ)", "AI experiment win rate", "Downloads per episode trend", "Lead quality score", "Cost per lead trend"]
slug: "podcast-launch-distribution"
install: "npx gtm-skills add marketing/problem-aware/podcast-launch-distribution"
drills:
  - autonomous-optimization
  - dashboard-builder
---
# Branded Podcast Launch — Durable Intelligence

> **Stage:** Marketing -> Problem Aware | **Motion:** Founder Social Content | **Channels:** Content, Social

## Outcomes
Always-on AI agents finding the local maximum. The `autonomous-optimization` drill runs the core loop: detect metric anomalies in podcast performance, generate improvement hypotheses, run A/B experiments, evaluate results, and auto-implement winners. The agent autonomously adjusts topic selection, promotion timing, clip selection, CTA placement, and guest targeting. Weekly optimization briefs report what changed and why. The loop converges when successive experiments produce <2% improvement.

## Leading Indicators
- Autonomous optimization loop running on schedule (daily monitoring, weekly experiments)
- At least 2 experiments running per month
- Experiment win rate >=30% (at least 1 in 3 experiments produces a measurable improvement)
- No manual intervention required for standard episode production and distribution
- Convergence signal: 3 consecutive experiments producing <2% improvement indicates local maximum reached

---

## Budget

**Play-specific tools & costs**
- Podcast hosting (Buzzsprout/Transistor): $18-49/mo
- Recording (Riverside): $24/mo
- Editing and clips (Descript + Opus Clip): $33-52/mo
- Show notes automation (Castmagic): $23/mo
- Anthropic API (Claude for hypothesis generation and content optimization): ~$20-50/mo based on usage
- Agent compute (n8n workflows): variable

**Total play-specific:** ~$120-200/mo
**Agent compute:** Variable based on monitoring frequency

_Your CRM, PostHog, and automation platform are not included -- standard stack paid once._

---

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for podcast metrics. This is the core of Durable and what makes it fundamentally different from Scalable.

**Configure the monitoring targets:**

| Metric | Source | Anomaly Threshold |
|--------|--------|-------------------|
| Downloads per episode (7-day) | Hosting platform API | Drop >20% vs 4-week rolling average |
| Podcast UTM traffic | PostHog (utm_source=podcast) | Drop >15% week-over-week |
| Episode-to-lead conversion rate | PostHog funnel | Drop >25% or plateau for 3+ weeks |
| Guest amplification rate | Attio (guest shared? field) | Drop below 40% for 4+ episodes |
| Subscriber growth rate | Hosting platform + RSS | Growth <5% month-over-month |
| Content repurposing engagement | PostHog + LinkedIn analytics | Average clip views drop >30% |

**Configure the experiment variables the agent can test:**

- **Topic selection**: The agent analyzes which topic categories (pain points, tactics, industry trends, founder stories) correlate with highest downloads and leads. It proposes shifting the upcoming episode mix toward higher-performing categories.
- **Episode title and description copy**: Test different title formats (question vs statement vs number-driven) by alternating across episodes and measuring 7-day downloads.
- **Promotion timing**: Test different publish days/times and social post schedules. Shift the automation triggers based on what drives highest initial download velocity.
- **Clip selection criteria**: Test whether clips featuring the guest's most surprising statement outperform clips with actionable tactics. Measure by clip engagement rate on LinkedIn.
- **CTA optimization**: Test different CTAs across episodes (free resource vs demo vs newsletter signup). Rotate CTAs and measure which drives the highest podcast-to-lead conversion.
- **Guest tier mix**: Test whether increasing Tier 1 guest frequency (at the cost of more outreach effort) produces proportionally more downloads and leads than Tier 2-3 guests.

**Guardrails (from the autonomous-optimization drill):**
- Maximum 1 active experiment at a time
- Auto-revert if primary metric drops >30% during an experiment
- Human approval required for: changes to recording format, changes to podcast branding/positioning, guest booking criteria changes affecting >50% of the pipeline
- Maximum 4 experiments per month
- If 4 consecutive experiments fail, pause and flag for human strategic review

### 2. Build the Durable podcast dashboard

Run the `dashboard-builder` drill to create a comprehensive PostHog dashboard for long-term podcast health:

**Panel 1 — Download trend (12-month view)**
Line chart of downloads per episode with a trendline. This is the single most important chart -- sustained growth means the play is working.

**Panel 2 — Podcast lead funnel (quarterly)**
Funnel: podcast UTM visit -> lead -> meeting -> deal. Breakdown by quarter. Shows whether podcast listeners convert and at what rate.

**Panel 3 — Experiment log**
Table of all autonomous optimization experiments: hypothesis, variable changed, result (win/lose/inconclusive), net metric impact. Shows the cumulative effect of optimization.

**Panel 4 — Topic performance heatmap**
Episodes grouped by topic category. Color-coded by: downloads (size), lead conversion rate (color intensity). Shows which topics to double down on.

**Panel 5 — Guest ROI ranking**
Table ranking all guests by: downloads their episode generated, leads attributed, social shares, repeat listener impact. Informs future guest targeting.

**Panel 6 — Channel attribution**
Breakdown of how listeners find the podcast: Apple Podcasts, Spotify, YouTube, website, social, cross-promotion partner. Shows where growth is coming from and where to invest.

Set up weekly email/Slack delivery of this dashboard to the founder.

### 3. Run the podcast performance monitor continuously

Run the `autonomous-optimization` drill in always-on mode:

1. **Weekly automated report**: Downloads, leads, guest pipeline health, upcoming experiment status, optimization brief
2. **Monthly deep analysis**: Topic trends, audience growth patterns, long-tail episode value (which old episodes are still generating traffic?), content repurposing ROI
3. **Quarterly strategic review**: Is the podcast still the right channel? Compare podcast CAC to other channels. Recommend: expand investment, maintain, or wind down.

The agent generates each report automatically. The founder reviews and provides strategic input on quarterly reviews.

### 4. Autonomous content calendar optimization

The agent maintains the episode calendar 8 weeks out:
1. Analyze recent episode performance to identify trending topics and declining ones
2. Propose the next 4 episode topics based on: what is performing best, what gaps exist in topic coverage, what is trending in your ICP's conversations (pulled from community monitoring or social listening)
3. Match proposed topics to the guest pipeline -- which booked or prospected guests fit these topics best?
4. Present the proposed calendar to the founder for approval weekly

**Human action required:** The founder reviews and approves the proposed episode calendar weekly. The agent handles topic research, guest matching, and scheduling. The founder retains editorial control.

### 5. Evergreen episode lifecycle management

The agent monitors the back catalog:
- Identify "evergreen" episodes that continue generating traffic 90+ days after publish
- Re-promote evergreen episodes with fresh clips and social posts quarterly
- Identify "spent" episodes (traffic < 1 visit/week) and stop re-promoting them
- Propose "sequel" episodes for topics where the original performed well but the landscape has changed

### 6. Evaluate sustainability

This level runs continuously. Monthly check: are downloads and leads sustaining or growing?

**Convergence detection:** When 3 consecutive autonomous experiments produce <2% improvement, the podcast has reached its local maximum. At convergence:
1. Reduce monitoring frequency from daily to weekly
2. Reduce experiments from 4/month to 1/month (maintenance mode)
3. Report: "This play is optimized. Current performance: [X downloads/episode, Y leads/quarter]. Further gains require strategic changes: new podcast format, new distribution channels, or expanding to video-first production."

**Non-convergence escalation:** If metrics are declining despite optimization, the agent flags this for strategic review. Possible causes: market saturation, audience fatigue, competitive entry, or topic exhaustion. The agent proposes strategic pivots (new format, new audience segment, podcast network partnership) for human decision.

---

## Time Estimate
- Autonomous optimization setup: 4 hours (one-time)
- Dashboard build: 3 hours (one-time)
- Performance monitor configuration: 2 hours (one-time)
- Weekly founder review of calendar and reports: 1 hour/week
- Monthly strategic review: 2 hours/month
- Episode recording (ongoing, batch format): 4 hours/month
- Agent compute (autonomous): runs continuously without human time

Setup: 9 hours. Ongoing founder time: ~8 hours/month. Agent runs autonomously.

---

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Buzzsprout/Transistor | Hosting, analytics API | $18-49/mo |
| Riverside | Batch recording | $24/mo |
| Descript + Opus Clip | Editing, clips | $33-52/mo |
| Castmagic | Automated show notes and social content | $23/mo |
| PostHog | Analytics, experiments, dashboards | Free: 1M events/mo |
| n8n | Optimization loop, distribution, monitoring | Self-hosted free or $20/mo cloud |
| Anthropic (Claude API) | Hypothesis generation, content optimization, experiment evaluation | ~$20-50/mo |
| Clay | Guest pipeline enrichment | $149/mo |
| Attio | Episode tracking, guest pipeline, experiment log | Free tier available |
| Loops | Episode notifications and subscriber growth | Free: 1K contacts. $25/mo: 5K |

---

## Drills Referenced
- `autonomous-optimization` -- the core always-on loop: monitor metrics, generate hypotheses, run experiments, evaluate results, auto-implement winners, report weekly
- `autonomous-optimization` -- continuous analytics, weekly reports, monthly deep analysis, quarterly strategic review
- `dashboard-builder` -- PostHog dashboard with download trends, lead funnels, topic heatmaps, guest ROI, and channel attribution
