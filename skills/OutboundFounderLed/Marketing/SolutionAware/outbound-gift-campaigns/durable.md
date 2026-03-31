---
name: outbound-gift-campaigns-durable
description: >
  Outbound Gift Campaigns — Durable Intelligence. AI agents autonomously optimize gift
  campaigns by detecting metric anomalies, generating improvement hypotheses, running A/B
  experiments on gift type/value/timing, and auto-implementing winners. Finds and maintains
  the local maximum of gift-driven pipeline generation.
stage: "Marketing > SolutionAware"
motion: "OutboundFounderLed"
channels: "Direct"
level: "Durable Intelligence"
time: "20 hours setup + 2 hours/week ongoing over 12 months"
outcome: "Sustained gift conversion (≥ 20% response rate) over 12 months via AI-driven gift selection, timing, and personalization optimization"
kpis: ["Sustained response rate", "AI experiment win rate", "Cost per meeting trend", "Pipeline per gift dollar", "Convergence score"]
slug: "outbound-gift-campaigns"
install: "npx gtm-skills add OutboundFounderLed/Marketing/SolutionAware/outbound-gift-campaigns"
drills:
  - autonomous-optimization
  - dashboard-builder
---

# Outbound Gift Campaigns — Durable Intelligence

> **Stage:** Marketing > SolutionAware | **Motion:** OutboundFounderLed | **Channels:** Direct

## Outcomes

The gift campaign channel runs on autopilot with AI agents continuously finding the local maximum. The `autonomous-optimization` drill monitors response rates, cost per meeting, and pipeline generated; when metrics plateau or drop, it generates hypotheses, designs gift experiments via the the gift ab testing workflow (see instructions below) drill, evaluates results, and auto-implements winners. The `autonomous-optimization` drill provides the daily anomaly detection and weekly reporting that feeds the optimization loop. The system converges when successive experiments produce less than 2% improvement — the play has reached its optimal performance given current market conditions.

## Leading Indicators

- Weekly optimization loop running without human intervention
- At least 1 experiment running at all times (or convergence declared)
- Response rate stable or improving month-over-month
- Cost per meeting trending flat or down
- Weekly optimization briefs delivered to Slack on schedule
- Experiment win rate ≥ 30% (at least 1 in 3 experiments improves the metric)
- AI gift selection confidence trending up (the model learns what works)

## Instructions

### 1. Build the gift campaign performance dashboard

Run the `dashboard-builder` drill to create a PostHog dashboard with these panels:

**Real-time panels:**
- Gifts sent this week / this month (trend line by gift type)
- Delivery success rate (delivered / sent) — target ≥ 90% physical, ≥ 98% digital
- Response rate (30-day attributed responses / delivered) — trend line with Scalable baseline marked
- Response breakdown by type (email reply, meeting booked, LinkedIn reply, URL visit) — stacked bar
- Response rate by signal type (job change, funding, hiring, competitor, content engaged) — compare segments
- eGift redemption rate — trend line

**Unit economics panels:**
- Average gift value per send (trend line)
- Cost per response (trend line)
- Cost per meeting (trend line with $75 target)
- Pipeline generated per month (bar chart)
- ROI: pipeline generated / total gift spend (should be ≥ 5x)
- Pipeline per gift dollar by gift type (which gifts generate the most pipeline?)

**Optimization panels:**
- Active experiments (count and description)
- Experiment history (last 10: hypothesis, result, confidence, adopted/reverted)
- Winning variant adoption log
- Convergence tracker: % improvement from last 3 experiments (converging when <2%)
- AI gift selection confidence distribution (histogram)

### 2. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for gift campaigns. This is the core of Durable — the always-on agent loop that finds and maintains the local maximum.

**Configure the optimization loop with these gift-campaign-specific parameters:**

**Monitored KPIs:**
- Primary: Response rate (30-day attributed)
- Secondary: Cost per meeting, pipeline generated per gift dollar

**Anomaly detection thresholds:**
- Normal: response rate within ±10% of 4-week rolling average
- Plateau: ±2% change for 3+ consecutive weeks
- Drop: >20% decline from 4-week average
- Spike: >50% increase (investigate — may be a high-value batch or attribution anomaly)

**Hypothesis generation context:** When an anomaly is detected, the agent should consider these optimization variables specific to gift campaigns:

1. **Gift type variables:** eGift card vs. book vs. gourmet vs. branded swag vs. experiential. Different prospect segments may respond to different gift types. The agent should test switching the default gift type for underperforming segments.

2. **Gift value variables:** $25 vs. $50 vs. $75 vs. $100. Test whether higher values produce proportionally higher response rates for different seniority levels. C-suite may require $75+ while Director-level may respond equally to $25.

3. **Personalization depth variables:** Signal-personalized note vs. deep-research note vs. AI-generated-with-human-review. Test the ROI of deeper personalization — does a note that references a specific LinkedIn post convert 2x better than one that references only the job change?

4. **Timing variables:** Time from signal detection to gift send. Test 24 hours, 3 days, 7 days, and 14 days. Some signals (job changes) may perform best with immediate sends; others (funding) may need a week for the news to settle.

5. **Follow-up variables:** Email follow-up timing (3 days vs. 5 days vs. 7 days after delivery). Follow-up channel (email first vs. LinkedIn first). Number of follow-up touches (1, 2, or 3). Subject line approach (reference the gift explicitly vs. lead with value proposition).

6. **Platform variables:** Tremendous vs. Sendoso vs. Reachdesk. Test whether branded Sendoso packaging outperforms Tremendous's simpler eGift delivery for the same gift value.

7. **Gift selection model variables:** AI confidence threshold for auto-sending (0.6 vs. 0.7 vs. 0.8). Prompt engineering for gift selection (different prompt structures may produce better matches).

**Experiment execution:** When the optimization loop selects a hypothesis, it runs the the gift ab testing workflow (see instructions below) drill:
1. Designs the experiment with control and treatment variants
2. Creates the PostHog experiment and feature flag
3. Splits the next 4 weeks of sends between control and treatment
4. Waits for the 30-day attribution window
5. Evaluates results and decides: adopt, iterate, or revert

**Guardrails for gift campaign experiments:**
- Never test more than 1 variable at a time
- Minimum 25 gifts per variant per experiment
- Never exceed the per-gift budget ceiling by more than 20% (gift costs are real money)
- If response rate drops below 10% for 2 consecutive weeks, pause new experiments and alert the founder
- Maximum 2 experiments per month (30-day attribution windows mean experiments take 6-8 weeks end-to-end)
- Never send a second gift to the same prospect within 90 days (even across experiments)

### 3. Deploy the gift performance monitor

Run the `autonomous-optimization` drill. This provides the daily anomaly detection and weekly reporting that feeds the autonomous optimization loop.

**Daily monitoring (8am via n8n):**
- Check gift delivery status updates from platform webhooks
- Count responses in the last 24 hours
- Compare trailing 7-day response rate against 28-day rolling average
- If anomaly detected, push data to the autonomous optimization loop

**Weekly report (Monday 9am via n8n):**
The weekly gift campaign optimization brief includes:

```
GIFT CAMPAIGN OPTIMIZATION BRIEF — Week of {{date}}

SENDS & DELIVERY
- Gifts sent: {{count}} ({{egift_count}} eGifts, {{physical_count}} physical)
- Delivery rate: {{rate}}%
- eGift redemption rate: {{rate}}%

RESPONSES (30-day attributed)
- Response rate: {{rate}}% (vs. {{4_week_avg}}% 4-week avg)
- Meetings booked this week: {{count}}
- Response breakdown: {{email_replies}} email, {{linkedin_replies}} LinkedIn, {{meetings}} meetings

UNIT ECONOMICS
- Total spend: ${{amount}}
- Cost per response: ${{amount}} (target: ≤$75)
- Cost per meeting: ${{amount}} (target: ≤$75)
- Pipeline generated: ${{amount}}
- ROI: {{ratio}}x (target: ≥5x)

SEGMENTS
- Best gift type: {{type}} — {{rate}}% response
- Best signal type: {{signal}} — {{rate}}% response
- Best seniority: {{level}} — {{rate}}% response

OPTIMIZATION
- Active experiment: {{description}} ({{sample_size}}/{{target_size}} per variant)
- Last completed: {{experiment_name}} — {{result}} ({{confidence}}% confidence)
- Convergence status: last 3 experiments averaged {{delta}}% improvement

AGENT RECOMMENDATION
{{ai_recommendation}}
```

### 4. Handle convergence

When the optimization loop detects convergence (3 consecutive experiments each producing <2% improvement):

1. Declare the gift campaign optimized at its local maximum
2. Reduce monitoring frequency from daily to weekly
3. Reduce experiment cadence from 2/month to 1 every 2 months (maintenance mode)
4. Generate a convergence report:
   - Final optimized response rate and cost per meeting
   - Total experiments run and win rate
   - All adopted changes (the accumulated improvements)
   - Optimal gift configuration by segment (gift type, value, timing, personalization depth)
   - Recommendation: "Further gains require strategic changes (new ICP segments, new gift categories, new follow-up channels) rather than tactical optimization"
5. Shift agent focus to monitoring for market changes:
   - Prospect fatigue (competitors also sending gifts to your ICP)
   - Gift platform pricing changes (Tremendous adding fees, Sendoso changing plans)
   - Seasonal patterns (response rates may spike around holidays, dip in summer)
   - ICP shifts (new buyer personas emerging, existing ones leaving)

### 5. Continuous market adaptation

Even after convergence, the agent should:
- Monitor for external changes weekly (competitor gifting activity, platform changes, market shifts)
- Re-run the full optimization loop if response rate drops >15% from converged baseline
- Test 1 new hypothesis every 2 months in maintenance mode
- Refresh gift selection prompts quarterly — update the AI with new learnings about what gift types resonate
- Refresh prospect enrichment data — signals go stale, job changes happen, companies evolve
- Watch for new gifting platforms or features that could improve economics (e.g., a new platform with no fees and better international coverage)

## Time Estimate

- 8 hours: Dashboard creation and configuration (one-time)
- 6 hours: Autonomous optimization loop configuration and testing (one-time)
- 4 hours: Gift performance monitor setup (one-time)
- 2 hours: Guardrails, convergence criteria, and brief template setup (one-time)
- 2 hours/week: Review weekly briefs, approve high-risk experiments, strategic adjustments
- Total: ~20 hours setup + 2 hours/week ongoing (~120 hours over 12 months)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Tremendous | Send eGift cards at scale (no platform fee) | Free — pay only gift face value. https://www.tremendous.com/pricing |
| Sendoso | Send physical gifts, books, swag (for A/B testing vs. eGifts) | From ~$20,000/yr. https://www.sendoso.com/compare-plans |
| Reachdesk | International gifting alternative | From ~$20,000/yr. https://www.reachdesk.com/pricing |
| Clay | Signal detection, enrichment, scoring | From $249/mo (Pro). https://www.clay.com/pricing |
| Attio | CRM — contacts, campaigns, experiment logs | Pro from $29/seat/mo. https://attio.com/pricing |
| PostHog | Analytics, experiments, anomaly detection, dashboards | Free up to 1M events/mo. https://posthog.com/pricing |
| n8n | Optimization loop scheduling, webhook processing | Free (self-hosted) or from $24/mo. https://n8n.io/pricing |
| Anthropic API | Hypothesis generation, experiment evaluation, gift selection | ~$10-$30/mo at this level. https://www.anthropic.com/pricing |
| Instantly | Follow-up email sequences | From $30/mo. https://instantly.ai/pricing |

**Estimated total monthly cost at 50 gifts/month (eGift path):**
- Gifts: 50 x $25-50 = $1,250-$2,500
- Tools: ~$350/mo
- **Total: ~$1,600-$2,850/mo**

**12-month projected cost:** ~$19,200-$34,200 in gifts + tools. At ≥5x ROI, this should generate $96,000-$171,000 in pipeline.

## Drills Referenced

- `autonomous-optimization` — The core always-on loop: monitor metrics, detect anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, and report weekly
- the gift ab testing workflow (see instructions below) — Execute the A/B experiments proposed by the optimization loop on gift type, value, timing, and personalization
- `autonomous-optimization` — Daily anomaly detection and weekly performance reports specific to gift campaigns
- `dashboard-builder` — Build the PostHog dashboard for real-time gift campaign performance monitoring
