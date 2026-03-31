---
name: pr-earned-durable
description: >
  PR & Earned Placements — Durable Intelligence. Always-on AI agents monitor PR performance,
  detect anomalies, generate improvement hypotheses, run A/B experiments, and auto-implement winners.
  The autonomous optimization loop finds and maintains the local maximum for earned-media-driven
  referral traffic and leads.
stage: "Marketing > Unaware"
motion: "PREarnedMentions"
channels: "Email, Content"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving placements and referral clicks over 6 months; successive optimization experiments converge to <2% improvement, indicating local maximum reached."
kpis: ["Placements per month (4-week rolling)", "Referral clicks per month (4-week rolling)", "Leads from earned media per month", "Pitch-to-placement conversion rate", "Cost per placement", "Experiment win rate", "Optimization convergence rate"]
slug: "pr-earned"
install: "npx gtm-skills add marketing/unaware/pr-earned"
drills:
  - autonomous-optimization
---

# PR & Earned Placements — Durable Intelligence

> **Stage:** Marketing → Unaware | **Motion:** PREarnedMentions | **Channels:** Email, Content

## Outcomes

The earned media engine runs autonomously with AI agents continuously monitoring, diagnosing, experimenting, and optimizing. The `autonomous-optimization` drill creates the always-on loop that detects metric anomalies, generates improvement hypotheses, runs A/B experiments, evaluates results, and auto-implements winners. The `autonomous-optimization` drill provides the play-specific monitoring, placement-to-pipeline attribution, and reporting that feeds the optimization loop. Together, they find and maintain the local maximum -- the best possible PR performance given the current media landscape, story angles, and competitive environment.

Success = placements and referral clicks sustained at or above Scalable baseline for 6 months, with the optimization loop converging (successive experiments producing <2% improvement) indicating the local maximum is reached.

## Leading Indicators

- Autonomous optimization loop active: daily monitoring running, experiments in flight
- Weekly optimization briefs delivered (no gaps in reporting)
- Experiment cadence: 2-4 experiments per month
- Experiment win rate: >= 40% of experiments adopted (below 30% = hypotheses are poorly formed)
- Placement-to-pipeline attribution complete: every lead traced back to source placement
- No metric anomalies unresolved for >7 days
- Convergence tracking: when 3 consecutive experiments produce <2% improvement, local maximum is declared
- Journalist relationship scores trending upward (more score-3+ contacts over time)

## Instructions

### 1. Deploy the PR performance monitor

Run the `autonomous-optimization` drill to build the always-on monitoring system:

**Build the PostHog dashboard** with 5 panels:
1. Outreach Pipeline -- pitches sent per week by outlet type, pitch-to-reply-to-placement funnel, conversion rates, outstanding pitches by status
2. Placement Tracking -- placements published per week (4-week rolling), breakdown by outlet type and tier, cumulative placements, recent placement table
3. Referral Traffic -- referral clicks from earned media per week (4-week rolling), breakdown by outlet/placement, earned vs other channels comparison, top 10 placements by referral traffic all-time
4. Placement-to-Pipeline Attribution -- full funnel from placement_published to deal_created, pipeline value attributed to earned media per month, leads from earned media per week, placements that generated leads with outlet, URL, leads, and pipeline value
5. Media Relationship Health -- active media contacts, contacts by relationship score distribution, source requests answered per week, source request hit rate

**Configure anomaly detection** checking daily:
- Pitch-to-reply rate drops >30% vs 4-week rolling average -> trigger "pitch-reply-decline"
- Zero placements in 14 days when baseline is 1+/week -> trigger "placement-drought"
- Reply sentiment shifts negative (>20% negative replies in a week) -> trigger "pitch-quality-decline"
- Referral clicks from earned media drop >40% vs 4-week rolling average -> trigger "referral-decline"
- Zero leads from earned media in 14 days when baseline is 1+/week -> trigger "lead-drought"
- Source request answer rate drops below 50% -> trigger "response-lag"
- No new media targets added in 30 days -> trigger "list-stale"
- Competitor mention volume spikes >2x -> trigger "competitor-surge"

Each anomaly trigger automatically feeds into the `autonomous-optimization` drill's Phase 2 (Diagnose).

**Automate weekly and monthly reports:**
- Weekly report (Monday 9am): executive summary, key metrics vs 4-week average, new placements, outreach pipeline status, source request activity, anomalies, recommended experiments
- Monthly deep-dive (first Monday): outlet type performance ranking, pitch angle ranking, tier analysis, backlink domain authority tracking, share of voice vs competitors, cost per placement trend, experiment results summary

### 2. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the PR & Earned play:

**Phase 1 -- Monitor (daily via n8n cron):**
1. Pull the play's primary KPIs from PostHog: placement rate, referral clicks per week, pitch-to-reply rate, leads from earned media.
2. Compare last 2 weeks against 4-week rolling average.
3. Classify: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase).
4. If normal: log to Attio, no action.
5. If anomaly detected: trigger Phase 2.

**Phase 2 -- Diagnose (triggered by anomaly):**
1. Gather context from PostHog: 8-week PR performance history broken down by outlet type, pitch angle, journalist tier, outreach timing, and source request platform.
2. Pull current PR configuration from Attio: active pitch angles, target list composition, outreach cadence, monitoring keywords.
3. Run `hypothesis-generation` with the anomaly data and context.
4. Receive 3 ranked hypotheses. Example hypotheses for this play:
   - "Placement rate declined because the 'AI agents replacing SDRs' angle has saturated -- journalists have covered it extensively. Switch to the 'data from 200 companies shows X' angle for the next 3 weeks."
   - "Referral clicks dropped because recent placements landed in outlets with low ICP overlap. Shift 60% of pitch effort from general tech blogs to vertical-specific newsletters."
   - "Pitch-to-reply rate declined because outreach expanded to Tier 3 journalists with no prior relationship. Reduce Tier 3 volume by 50% and reallocate to Tier 1 relationship nurturing."
   - "Source request conversion dropped because response drafts have become formulaic. Refresh the Claude prompt with recent successful responses and add industry-specific data points."
5. Store hypotheses in Attio. If top hypothesis is high-risk (affects >50% of outreach or requires targeting changes to Tier 1 relationships), send Slack alert for human review and STOP.
6. If low or medium risk: proceed to Phase 3.

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
1. Take the top-ranked hypothesis.
2. Design the experiment using PostHog experiments: split outreach between control (current approach) and variant (hypothesis change).
3. Implement the variant. Examples of PR experiments:
   - **Pitch angle rotation**: Send 50% of pitches with current winning angle and 50% with proposed new angle. Compare placement rate.
   - **Outlet type rebalancing**: Shift pitch allocation between newsletters, podcasts, and journalists. Compare referral clicks per placement.
   - **Personalization depth**: Test Tier 2 targets with full hand-personalization vs template + merge fields. Compare reply rate and placement rate.
   - **Source request response style**: Alternate between data-heavy responses and narrative/anecdote responses. Compare selection rate.
   - **Follow-up timing**: Test 3-day vs 7-day follow-up intervals. Compare incremental reply rate.
   - **Reactive vs proactive mix**: Shift effort allocation between reactive PR (responding to journalist requests and trends) and proactive pitching. Compare placements per hour invested.
4. Set experiment duration: minimum 14 days or until 20+ pitches per variant, whichever is longer. PR experiments need sufficient volume because placement outcomes are lower-frequency than web conversion events.
5. Log experiment start in Attio: hypothesis, start date, expected duration, success metric, control and variant definitions.

**Phase 4 -- Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog.
2. Run `experiment-evaluation` comparing control vs variant on the primary metric.
3. Decision:
   - **Adopt**: Variant outperformed control with >= 90% confidence (lower threshold than web experiments due to smaller sample sizes). Update the live PR workflow to use the winning approach permanently. Log the change.
   - **Iterate**: Results suggest a direction but are not conclusive. Generate a refined hypothesis. Return to Phase 2.
   - **Revert**: Variant underperformed or no significant difference. Restore control. Log the failure and the learning.
   - **Extend**: Insufficient data. Continue the experiment for another 14 days.
4. Store the full evaluation in Attio: decision, confidence level, impact on primary metric, reasoning.

**Phase 5 -- Report (weekly via n8n cron):**
1. Aggregate all optimization activity for the week: anomalies detected, hypotheses generated, experiments running, decisions made.
2. Calculate: net metric change from all adopted changes this week.
3. Generate a weekly optimization brief:
   - What changed and why
   - Net impact on placements per month and referral clicks per month
   - Current distance from estimated local maximum
   - Recommended focus for next week
4. Post to Slack and store in Attio.

### 3. Implement play-specific optimization targets

Beyond the generic optimization loop, configure these PR-specific optimization areas:

**Pitch angle lifecycle management:**
- Track placement rate by pitch angle over time. When an angle's placement rate drops below 50% of its peak for 4 consecutive weeks, it has saturated. Propose retiring it.
- When a new industry trend, product launch, or data release creates a fresh angle, propose adding it to the rotation.
- Maintain a minimum of 3 active pitch angles at all times. If one is retired, a replacement must be ready.

**Outlet type ROI optimization:**
- Monthly: compare leads per hour invested by outlet type (newsletters vs podcasts vs journalists).
- If one outlet type produces 3x more leads per unit effort, propose shifting 60% of effort to that type.
- If all outlet types produce similar results, maintain diversity for audience reach.

**Press release timing optimization:**
- For major announcements (product launches, funding, research reports), evaluate whether wire distribution (PR Newswire, EIN Presswire) produces incremental placements beyond direct pitching.
- Track cost-per-incremental-placement for wire distribution. If wire produces placements at >3x the cost of direct pitching, limit wire to genuinely major news.

**Journalist relationship deepening:**
- Monthly: identify the 5 highest-value journalist relationships (score 3+) and assign specific nurture actions: share exclusive data, offer early access to announcements, provide expert commentary for their upcoming stories.
- Track whether proactive relationship investment correlates with lower pitch-to-placement effort (journalists who know you = fewer pitches needed per placement).

### 4. Maintain convergence tracking

Track the optimization loop's progress toward the local maximum:

- After each adopted experiment, record the percentage improvement on the primary metric (placements per month or referral clicks per month).
- When 3 consecutive experiments produce <2% improvement, declare convergence.
- At convergence:
  1. The play has reached its local maximum for the current media landscape, pitch angles, and competitive environment.
  2. Reduce monitoring frequency from daily to weekly.
  3. Reduce experiment cadence from 2-4/month to 1/month (maintenance experiments).
  4. Report: "PR & Earned play is optimized. Current performance: [X placements/month, Y referral clicks/month, Z leads/month]. Further gains require strategic changes (new product launch creating fresh news, entering a new market, major industry shift) rather than tactical optimization."

### 5. Handle media landscape shifts

Earned media has a unique challenge: the media landscape changes. Journalists change beats, publications fold, new outlets launch, and industry narratives shift.

Configure the agent to detect landscape shift signals:
- Placement rate declining despite stable outreach quality (3+ weeks of steady decline)
- Multiple Tier 1 journalists changing outlets or beats in the same quarter
- New competitor getting significantly more coverage (competitor mention volume growing while yours is flat)
- Industry narrative shifting away from your core pitch angles

When a landscape shift is detected, the agent should propose strategic interventions:
- Refresh the media target list: remove stale contacts, add journalists from new outlets
- Develop new pitch angles tied to emerging industry narratives
- Commission original research or data analysis that creates a fresh story hook
- Evaluate whether press release distribution should be added or expanded for a specific announcement

**Human action required:** Strategic pivots in PR direction require founder approval. The agent proposes, the founder decides.

## Time Estimate

- PR performance monitor setup: 10 hours (one-time)
- Autonomous optimization loop configuration: 8 hours (one-time)
- Weekly monitoring and report review (24 weeks x 30 min): 12 hours
- Experiment design and implementation (12-16 experiments x 3 hours): 36-48 hours
- Monthly deep-dive reviews (6 x 2 hours): 12 hours
- Journalist relationship nurturing (24 weeks x 30 min): 12 hours
- Strategic intervention reviews (as needed): 6 hours
- Convergence documentation: 2 hours
- **Total: ~100 hours active work over 6 months** (budget allows 200 hours including agent compute and iteration)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Tracked pitch sending with sequences | From $37/mo (https://instantly.ai/pricing) |
| Clay | Contact enrichment at scale | From $149/mo (https://www.clay.com/pricing) |
| Mention | Brand and competitor media monitoring | From $41/mo Solo (https://mention.com/en/pricing/) |
| Qwoted | Journalist source requests | Pro ~$50/mo (https://qwoted.com) |
| Featured.com | Expert quote placements | Pro ~$99/mo (https://featured.com/pricing) |
| PostHog | Event tracking, experiments, anomaly detection | Free up to 1M events/mo (https://posthog.com/pricing) |
| n8n (self-hosted) | Automation: monitoring, optimization loop, reporting | Free self-hosted (https://n8n.io/pricing) |
| Attio | CRM + optimization audit trail | Free up to 3 users (https://attio.com/pricing) |
| Anthropic Claude API | Hypothesis generation, experiment evaluation, pitch drafting | ~$10-25/mo (https://www.anthropic.com/pricing) |
| PR Newswire | Press release distribution (occasional) | ~$300-1,000/release (https://www.prnewswire.com/products/online-membership.html) |
| EIN Presswire | Budget press release distribution | From $99.95/release (https://www.einpresswire.com/pricing) |
| Buffer or Typefully | Social post scheduling | ~$12-25/mo (https://buffer.com/pricing) |

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics -> detect anomalies -> generate hypotheses -> run A/B experiments -> evaluate results -> auto-implement winners -> weekly optimization briefs
- `autonomous-optimization` — play-specific dashboard, anomaly detection, PR event taxonomy, placement-to-pipeline attribution, and weekly/monthly reporting
