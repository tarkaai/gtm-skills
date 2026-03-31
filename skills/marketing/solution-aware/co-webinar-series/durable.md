---
name: co-webinar-series-durable
description: >
  Co-Webinar Series — Durable Intelligence. Always-on AI agents monitor
  co-webinar funnel health, partner portfolio performance, and audience quality.
  The autonomous-optimization drill detects metric anomalies, generates
  improvement hypotheses, runs A/B experiments on topics, formats, promotion
  strategies, and nurture sequences, and auto-implements winners. Weekly
  optimization briefs. Converges when successive experiments produce <2%
  improvement.
stage: "Marketing > Solution Aware"
motion: "Partnerships & Warm Intros"
channels: "Events, Email"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving registrations and qualified leads over 6 months; qualified-lead-per-event rate at or above Scalable peak; agents detect topic fatigue, partner audience decay, promotion channel saturation, and format staleness, adapting automatically."
kpis: ["Qualified leads per event", "Show rate", "Partner contribution ratio", "Meetings booked per event", "Repeat attendance rate", "Partner audience conversion rate", "Experiment win rate"]
slug: "co-webinar-series"
install: "npx gtm-skills add marketing/solution-aware/co-webinar-series"
drills:
  - autonomous-optimization
  - co-webinar-performance-monitor
---

# Co-Webinar Series — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Events, Email

## Outcomes

An always-on optimization system that manages the co-webinar series and partner portfolio autonomously. The `autonomous-optimization` drill runs the core loop: detect metric anomalies across events, partners, topics, formats, and nurture sequences, generate improvement hypotheses, run A/B experiments, evaluate results, and auto-implement winners. Weekly optimization briefs summarize what changed and why. The system converges when successive experiments produce <2% improvement — the play has reached its local maximum.

Sustained or improving registration and qualified lead volume over 6 months. Qualified-lead-per-event rate at or above the Scalable peak. The agent detects and adapts to topic fatigue (declining registrations for similar topics), partner audience decay (a partner's audience stops converting after repeated co-webinars), promotion channel saturation (email open rates declining, LinkedIn engagement dropping), format staleness (the same format producing lower engagement over time), and seasonal patterns (conference season, holiday lulls, budget cycles).

## Leading Indicators

- Anomaly detection fires within 24 hours of a metric shift (signal: monitoring is working)
- At least 1 experiment runs per 3-week period (signal: optimization loop is active)
- Experiment win rate >= 30% (signal: hypotheses are well-targeted)
- No partner's audience conversion rate drops below 50% of their historical average for 2+ consecutive events without a corrective action firing (signal: partner health detection works)
- Weekly optimization brief posts on time every Friday (signal: reporting pipeline is stable)
- Time between anomaly detection and experiment launch <72 hours (signal: the loop is tight)
- Partner portfolio maintains 6+ active partners with no single partner driving >35% of total pipeline (signal: portfolio is diversified)
- Repeat attendance rate continues to grow or holds above 20% (signal: the series is building a recurring audience)

## Instructions

### 1. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill configured for this play's specific metrics and levers:

**Monitor phase (daily via n8n cron):**
- Pull co-webinar KPIs from PostHog: registrations, show rate, engagement rate, qualified leads, meetings booked — all broken down by partner, topic, format, and promotion channel
- Compare last 2 events against 4-event rolling average
- Classify each metric as: normal (within +/-10%), plateau (+/-2% for 3+ events), drop (>20% decline), or spike (>50% increase)
- Per-partner anomaly detection: flag any partner whose audience conversion rate dropped >25% from their rolling average
- Per-topic anomaly detection: flag declining registrations for similar topic categories
- Promotion channel monitoring: flag if email open rates or LinkedIn engagement decline >15% from rolling average
- Format monitoring: compare engagement rate across formats (panel vs workshop vs fireside) — flag if any format's engagement rate drops >20%
- If anomaly detected, trigger the Diagnose phase

**Diagnose phase (triggered by anomaly):**
- Gather context: which events, partners, topics, or channels are affected? What has changed recently? What is the historical trend?
- Pull 8-event metric history from PostHog
- Run hypothesis generation with the anomaly data. Common hypotheses for this play:
  - "Topic fatigue — registrations for [topic category] have declined 30% over the last 3 events covering similar ground. Prescribe: pivot to a new topic category or approach the topic from a different angle."
  - "Partner X's audience is saturated — their audience has seen 4 co-webinars in 6 months and conversion is declining. Prescribe: extend the interval between events with this partner to quarterly, or co-create a fundamentally different format (e.g., switch from panel to hands-on workshop)."
  - "Promotion channel saturation — email open rates dropped 20% over 4 events, suggesting list fatigue. Prescribe: test a different subject line framework, reduce email frequency, or add a new promotion channel (paid social, community posts, partner newsletter mention)."
  - "Format staleness — engagement rate for panels has dropped 25% while workshop engagement remains high. Prescribe: shift the default format to workshop or test a new format (AMA, live demo, roundtable)."
  - "Show rate decline — registrants are signing up but not showing up. Prescribe: test different event times, shorten the event duration, or improve reminder cadence/copy."
  - "Follow-up decay — nurture email reply rate dropped. Prescribe: A/B test new follow-up copy, faster follow-up timing, or a different CTA (resource download vs meeting request)."
  - "Partner promotional free-riding — Partner Y's contribution ratio dropped below 20% for 2 consecutive events. Prescribe: have a direct conversation about promotional expectations or replace with a more committed partner."
  - "Seasonal effect — January ramp-up, summer lull, conference season distraction. Prescribe: adjust cadence and expectations rather than over-reacting."
- Store hypotheses in Attio. If risk = "high" (e.g., retiring a top partner, changing the series format entirely, or pausing the series for a month), alert for human review.

**Experiment phase (triggered by hypothesis acceptance):**
- Design the experiment. For this play, the primary experiment types are:
  1. **Topic A/B test**: Schedule 2 co-webinars in the same week with similar partners but different topic angles. Compare registrations, show rate, and qualified leads. Track by event slug.
  2. **Format A/B test**: Run a panel format with Partner A and a workshop format with similar Partner B. Compare engagement rate and meeting booking rate. Requires partners with similar audience size and overlap.
  3. **Promotion A/B test**: For the same event, split your promotion list. Half gets subject line A, half gets subject line B. Measure email open rate and registration conversion per variant.
  4. **Nurture sequence A/B test**: For attendees of a single event, split into two groups. Group A gets the standard tiered nurture. Group B gets a modified sequence (different timing, different CTA, different copy angle). Measure reply rate and meeting booking rate.
  5. **Partner rotation test**: Replace an underperforming partner with a new prospect from the pipeline. Compare the new partner's first event metrics against the replaced partner's last 2 events.
  6. **Event timing test**: Test Tuesday 11am vs Thursday 2pm across similar events. Measure show rate and engagement rate.
  7. **Registration page test**: Use PostHog feature flags to show different landing page variants. Test headlines, value propositions, or social proof elements. Measure registration conversion rate.
- Minimum experiment duration: 2 events (for event-level tests) or 7 days (for within-event tests like nurture A/B).
- Log experiment design, start date, expected duration, and success criteria in Attio.

**Evaluate phase (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run experiment evaluation:
  - **Adopt**: Winning variant becomes the new default. Update templates, formats, or cadence. Log the change in Attio with full reasoning.
  - **Iterate**: Result was inconclusive or showed a promising direction. Generate a refined hypothesis and design a follow-up experiment.
  - **Revert**: Variant performed worse. Restore the control configuration. Wait until the next experiment slot (respect the 1-experiment-at-a-time guardrail).
  - **Extend**: Insufficient data (too few events in the test period). Keep the experiment running for another cycle.
- Store the full evaluation in Attio with decision, confidence level, and reasoning.

**Report phase (weekly, Friday 3pm via n8n cron):**
- Aggregate all optimization activity for the week
- Calculate net metric change from adopted experiments
- Generate the weekly optimization brief (see step 2)

### 2. Deploy play-specific monitoring and reporting

Run the `co-webinar-performance-monitor` drill to build the monitoring layer specific to this play:

**Co-webinar dashboard in PostHog:**
- Registrations by event, colored by partner (bar chart, last 90 days)
- Qualified leads by event (bar chart, last 90 days)
- Show rate trend (line chart, last 12 events)
- Partner contribution ratio by event (stacked bar)
- Partner audience conversion rate comparison (table, sorted descending)
- Topic performance heatmap (topic category vs qualified lead rate)
- Format performance comparison (panel vs workshop vs fireside — engagement and conversion)
- Promotion channel effectiveness over time (stacked area chart)
- Repeat attendee growth (cumulative line chart)
- Co-webinar funnel: page_viewed → registered → reminded → attended → engaged → nurture_reply → meeting_booked

**Weekly co-webinar optimization brief (automated, Friday 3pm):**
```
## Co-Webinar Weekly Brief — {date}

**This week**: {total_regs} registrations, {total_leads} qualified leads, {total_meetings} meetings booked
**vs 4-event avg**: {change_pct}% {up/down}
**Events this week**: {count} | **Active partners**: {active_count}

### Event Performance
| Event | Partner | Regs | Show Rate | Qualified Leads | Meetings |
|-------|---------|------|-----------|-----------------|----------|
| {topic} | {partner} | {n} | {pct}% | {n} | {n} |

### Partner Portfolio Health
- Top partners by qualified leads: {ranked list}
- Partners declining: {list with trend data}
- Partners in cooldown or approaching fatigue: {list}
- Concentration risk: {top partner}% of pipeline — {GREEN/YELLOW/RED}

### Anomalies Detected
- {event/partner/metric}: {description} — {hypothesis generated}

### Experiments This Week
- {experiment}: {status} — {result or ETA}

### Adopted Changes
- {change}: {impact on metrics}

### Series Health
- Topic freshness: {assessment}
- Repeat attendance trend: {rate}% (target: 20%+)
- Promotion channel health: {assessment}
- Format engagement trend: {assessment}

### Convergence Status
{distance from local maximum estimate}
{recommended focus for next week}
```

**Per-partner ROI tracking in Attio:**
- Total co-webinars, registrations driven, qualified leads, meeting rate, audience conversion rate, promotional effort score, partner health status
- Updated after every event by n8n automation

**Performance alerts:**
- Partner audience conversion drops >50% event-over-event: investigate fatigue or audience composition shift
- Registrations for a topic category decline for 3 consecutive events: flag for topic rotation
- Show rate drops below 25% for 2 consecutive events: investigate timing, reminder quality, or topic appeal
- Total qualified leads drop below Scalable baseline for 2 consecutive events: trigger autonomous optimization investigation
- Repeat attendance rate declines: investigate whether the series is becoming stale for recurring attendees
- Any partner's contribution ratio drops below 15%: flag for promotional conversation or replacement

### 3. Manage partner portfolio health

The agent autonomously manages the co-webinar partner portfolio:

- **Partner audience fatigue detection**: If a partner's audience conversion rate declines for 2 consecutive co-webinars, the agent extends the interval to quarterly and tests with a fundamentally different topic or format. If the third attempt also shows fatigue, retire the partner from co-webinars and source a replacement.
- **Partner graduation**: Partners consistently producing >5 qualified leads per event get escalated to deeper partnerships (joint content creation, product integration, co-selling, shared customer case studies). Log the recommendation in Attio for human review.
- **Partner replacement**: When a partner is retired, the agent triggers the `co-webinar-partner-matching` drill to source a replacement. Maintain 6+ active partners and 10+ prospects in the pipeline.
- **Seasonal adjustment**: The agent learns seasonal patterns and adjusts cadence: reduce to monthly during slow periods (December, August), increase to weekly during high-engagement periods (January, September). Do not flag expected seasonal dips as anomalies.
- **Promotional accountability**: If a partner's contribution ratio drops below 20% for 2 consecutive events, the agent drafts a "promotional expectations" message for human review. If the partner does not improve, reduce cadence or replace.
- **Format rotation intelligence**: The agent tracks which formats work best with which partner types and audiences. Over time, it matches partners to their best-performing format automatically rather than defaulting to the same format for every event.

### 4. Guardrails

- **Maximum 1 active experiment at a time.** Never stack a topic test with a format test simultaneously. Isolate variables.
- **Revert threshold**: If qualified leads drop >40% during an experiment period compared to the 4-event rolling average, auto-revert immediately.
- **Human approval required for:**
  - Retiring a partner that produces >25% of total qualified leads
  - Changing the series cadence (e.g., moving from bi-weekly to monthly)
  - Any experiment the hypothesis generator flags as "high risk"
  - Proposing partnership escalation (joint content, co-selling, product integration)
  - Budget increases for promotion spend
- **Cooldown**: After a failed experiment, wait until the next event cycle before testing the same variable.
- **Maximum 4 experiments per month.** If all 4 fail, pause optimization and flag for human strategic review.
- **Never retire more than 1 partner per month** without human approval (prevent portfolio collapse).
- **Protect the series brand**: Never schedule more than 3 co-webinars per month. If experiment design requires more, defer experiments rather than fatiguing the audience.

### 5. Convergence detection

The optimization loop runs continuously. It detects convergence when:
- 3 consecutive experiments produce <2% improvement in the primary metric (qualified leads per event)
- The play has reached its local maximum

At convergence:
1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment frequency to 1 per month (maintenance mode)
3. Report: "Co-webinar series has converged. Current performance: {metrics per event}. Anchor partners: {list}. Repeat attendance rate: {rate}. Further gains require strategic changes (new partner categories, new audience segments, different event formats like in-person workshops or virtual summits, paid promotion, or product integration partnerships) rather than tactical optimization of topics, formats, and nurture sequences."

## Time Estimate

- Autonomous optimization setup: 25 hours
- Co-webinar performance monitor setup: 12 hours
- Initial monitoring and tuning (month 1): 20 hours
- Ongoing oversight (months 2-6, ~6 hours/month): 30 hours
- Experiment design and evaluation: 40 hours
- Partner portfolio management: 30 hours
- Strategic reviews and course corrections: 43 hours

Total: ~200 hours over 6 months (heavily front-loaded; agent handles most ongoing work after month 1)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Analytics, experiments, anomaly detection, dashboards | Free up to 1M events; paid from $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Optimization loop orchestration, scheduling, alerts | Cloud Pro: ~EUR 60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Partner CRM, experiment logs, per-partner ROI tracking | Plus: $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Anthropic Claude | Hypothesis generation, experiment evaluation, weekly briefs | Sonnet: ~$15-30/mo at this volume ([docs.anthropic.com/en/docs/about-claude/models](https://docs.anthropic.com/en/docs/about-claude/models)) |
| Loops | Nurture sequences, promotion emails, reminder series | Paid from $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Riverside | Webinar hosting and recording | Business: $24/mo ([riverside.fm/pricing](https://riverside.fm/pricing)) |
| Clay | Partner enrichment, net-new prospect sourcing | Launch: $185/mo ([clay.com/pricing](https://www.clay.com/pricing)) |
| Crossbeam | Partner account overlap (ongoing portfolio optimization) | Free tier: 3 seats; Connector from ~$400/mo ([crossbeam.com/pricing](https://www.crossbeam.com/pricing)) |

**Estimated cost for this level: ~$250-450/mo** (n8n Pro + Attio Plus + Anthropic API + Loops + Riverside + Clay required; Crossbeam and PostHog within free tiers for most usage)

## Drills Referenced

- `autonomous-optimization` — the core monitor → diagnose → experiment → evaluate → implement loop that finds the local maximum
- `co-webinar-performance-monitor` — per-partner dashboards, event post-mortems, monthly series reports, partner health tracking, and alerts specific to the co-webinar series
