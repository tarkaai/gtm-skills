---
name: account-based-cold-calling-durable
description: >
  Account-Based Cold Calling — Durable Intelligence. Always-on AI agents continuously optimize
  call scripts, signal targeting, call timing, and objection handling via the autonomous optimization
  loop. Agent detects metric anomalies, generates improvement hypotheses, runs A/B experiments,
  evaluates results, and auto-implements winners. Cold-call-specific transcript analysis extracts
  objection patterns and generates improved script variants. Weekly optimization briefs track
  convergence toward the local maximum. Converges when successive experiments produce <2% improvement.
stage: "Marketing > Solution Aware"
motion: "OutboundFounderLed"
channels: "Direct"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained call-to-meeting rate (>=2.5%) over 6 months via autonomous script optimization, signal targeting refinement, and objection handling improvement"
kpis: ["Sustained call-to-meeting rate", "Autonomous experiment win rate", "Script variant improvement trend", "Signal ROI trend", "Cost per meeting trend"]
slug: "account-based-cold-calling"
install: "npx gtm-skills add marketing/solution-aware/account-based-cold-calling"
drills:
  - autonomous-optimization
  - call-performance-reporting
---

# Account-Based Cold Calling — Durable Intelligence

> **Stage:** Marketing > Solution Aware | **Motion:** OutboundFounderLed | **Channels:** Direct

## Outcomes

The cold calling system runs autonomously. AI agents continuously monitor call performance, analyze transcripts for objection patterns, detect when scripts or signals decay, generate improvement hypotheses, run A/B experiments, and auto-implement winners. The `autonomous-optimization` drill runs the core loop: detect metric anomalies in call performance -> generate improvement hypotheses -> run A/B experiments -> evaluate results -> auto-implement winners. The the cold call script optimization workflow (see instructions below) drill adds the play-specific layer: transcript analysis, objection pattern extraction, script variant scoring, and data-driven script evolution. Weekly optimization briefs report what changed and why. The system converges when successive experiments produce <2% improvement, indicating the cold calling process has reached its local maximum for your market and ICP.

## Leading Indicators

- Autonomous optimization loop running daily, generating at least 1 experiment per month
- Call-to-meeting rate stable or improving above 2.5% over rolling 4-week window
- Transcript analysis pipeline processing 100% of connected calls within 24 hours
- Objection recovery rate improving or stable above 30% (founder successfully navigating past objections)
- Script variant leaderboard updated weekly with statistical significance
- At least 1 experiment adopted in the first month (script change, timing shift, signal reprioritization)
- Weekly optimization briefs posted to Slack with actionable recommendations
- Convergence detection active — system identifies when optimization has plateaued

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the account-based cold calling play. This creates the always-on agent loop with 5 phases:

**Phase 1 — Monitor (daily via n8n cron):**
The agent checks cold calling KPIs daily using `posthog-anomaly-detection`:
- Call-to-meeting rate (primary metric)
- Connect rate by time window
- Conversation rate (calls >60 seconds / connected)
- Meeting rate by signal type
- Script variant conversion rates
- Objection frequency and recovery rates
- Voicemail-to-callback rate
- Pre-call email open rate and its correlation with connect rate

Classify each metric: normal (within +/-10% of 4-week average), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase). If anomaly detected, trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
The agent gathers context from Attio (current script variants, signal configuration, call timing, cadence settings, ICP definition) and 8-week metric history from PostHog. Runs `hypothesis-generation` to produce 3 ranked hypotheses. Examples of cold-calling-specific hypotheses:

- "Connect rate dropped 25% this week. Hypothesis: prospects in the West Coast segment are being called at 8am ET (5am PT). Shift West Coast calls to 11am-1pm ET to match their 8-10am window."
- "Meeting rate from funding signals dropped from 5% to 2%. Hypothesis: Series A signals older than 60 days have decayed — funding announcement excitement fades. Tighten the funding recency filter from 90 days to 45 days."
- "Objection 'we already have something' increased from 15% to 30% of connected calls. Hypothesis: a new competitor entered the market and is closing deals in our ICP. Add a competitive displacement angle to the script — acknowledge the competitor and differentiate."
- "Average call duration dropped from 90s to 45s. Hypothesis: the current opener variant ('I noticed your team just raised a Series B') is no longer pattern-interrupting because too many SDRs use the same approach. Test a problem-first opener that skips the signal reference."
- "Pre-call email open rate dropped below 20%. Hypothesis: subject line fatigue. The current subject line has been running for 6 weeks. Test 3 new subject lines."

Store hypotheses in Attio as notes on the campaign record. If risk = "high" (e.g., changing ICP definition or significantly altering the call framework), send Slack alert for human review. If risk = "low" or "medium" (e.g., testing a new opener variant or shifting call windows), proceed automatically.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
Design and run the experiment using PostHog feature flags:

- **Script experiments:** Create a feature flag that assigns new prospects to control (current best script) or variant (hypothesis-driven script). The agent generates the variant script and stores it in Attio. When the founder opens a prospect record, they see either the control or variant script. After 50+ calls per variant, compare meeting rate.
- **Timing experiments:** Create a feature flag that assigns prospects to different call windows. Route Tier 1 signals to the test window, Tier 2 to control. Compare connect rate and meeting rate per window.
- **Signal experiments:** Create a feature flag that changes signal scoring weights. Test whether tightening or loosening recency filters, or reprioritizing signal types, improves meeting rate per 100 calls.
- **Cadence experiments:** Test different pre-call email timing (Day 0 email -> Day 3 call vs. Day 0 email -> Day 5 call) to find the optimal warming window.
- **Voicemail experiments:** Test new voicemail scripts or lengths. Measure callback rate per variant.

Minimum experiment duration: 7 days or 50 calls per variant, whichever is longer. Log experiment start in Attio with: hypothesis, start date, expected duration, success metric, variant description.

**Phase 4 — Evaluate (triggered by experiment completion):**
Pull results from PostHog. Run `experiment-evaluation`:
- **Adopt:** Variant outperforms control by 5%+ with statistical confidence (p < 0.05). Update the live configuration: promote the winning script variant, adjust signal weights, change call timing. Log the change in Attio.
- **Iterate:** Results inconclusive or marginal. Generate a refined hypothesis building on the learnings. Return to Phase 2.
- **Revert:** Control outperforms variant. Disable variant. Log the failure with the reason. Return to Phase 1 monitoring.
- **Extend:** Insufficient data (fewer than 50 calls per variant). Run for another period.

Store full evaluation in Attio: decision, confidence level, reasoning, net metric impact.

**Phase 5 — Report (weekly via n8n cron):**
Generate weekly optimization brief:
```
## Cold Calling Optimization Brief — Week of {date}

### Call Performance
- Calls: {n} attempted | {n} connected ({pct}%) | {n} meetings ({pct}%)
- Week-over-week: volume {delta}%, connect rate {delta}%, meeting rate {delta}%
- 4-week rolling meeting rate: {pct}% (target: >=2.5%)

### Anomalies Detected
- {metric}: {classification} ({value} vs {4-week avg})

### Experiments Active
- {experiment_name}: {status}. {calls completed}/{target}. {preliminary results or days remaining}

### Decisions Made
- {experiment_name}: {decision}. Net impact: {metric change}

### Script Variant Leaderboard
| Variant | Calls | Connect Rate | Meeting Rate | Status |
|---------|-------|-------------|-------------|--------|
| {name}  | {n}   | {pct}%      | {pct}%      | {active/retired} |

### Signal ROI
| Signal Type | Calls | Meeting Rate | Cost/Meeting | Trend |
|-------------|-------|-------------|-------------|-------|
| {type}      | {n}   | {pct}%      | ${amt}      | {up/down/flat} |

### Objection Landscape
- Top objection: {category} ({pct}%) — recovery rate: {pct}%
- Emerging: {category} (up {pct}% this week)

### Convergence Status
- Consecutive experiments with <2% improvement: {count}/3
- Estimated distance from local maximum: {assessment}

### Recommended Focus Next Week
- {recommendation based on data}
```

Post to Slack and store in Attio.

Estimated time: 15 hours for setup. Then always-on.

### 2. Deploy cold-call-specific transcript optimization

Run the the cold call script optimization workflow (see instructions below) drill. This is the play-specific intelligence layer that the generic `autonomous-optimization` drill cannot provide:

**Daily transcript analysis:**
- Ingest all new call transcripts from Fireflies
- Extract: opener used, signal referenced, objections raised, objection handling outcome, talk ratio, meeting outcome
- Store as structured PostHog events for the optimization loop to consume

**Objection pattern tracking:**
- Track objection frequency distribution and trends over time
- Detect emerging objections (new category appearing in >10% of calls = market shift)
- Monitor recovery rate per objection category (if recovery rate drops below 20%, flag for script update)
- Correlate objections with signals (certain signals may trigger specific objections — the agent learns which)

**Script variant scoring:**
- Maintain a leaderboard of all script variants ranked by meeting conversion rate
- Minimum 20 calls per variant before ranking (statistical significance)
- Auto-retire variants that underperform the best variant by >50% after 50 calls

**Weekly script improvement proposals:**
- Analyze the best-performing transcripts (high talk ratio + meeting booked)
- Compare against the worst-performing transcripts (short duration + no meeting)
- Generate 1-2 new script variant proposals with specific language changes, rationale, and expected impact
- Post to Slack for founder review before activation

**Human action required:** The founder approves new script variants before they enter the experiment rotation. The agent generates and recommends; the founder decides.

**Script version history:**
- Every variant stored in Attio with: creation date, hypothesis, performance metrics, status (active/testing/retired)
- Prevents the optimization loop from re-testing approaches that already failed
- Creates institutional memory of what works for this specific market and ICP

Estimated time: 8 hours setup. Then always-on.

### 3. Maintain call performance reporting at scale

Continue running the `call-performance-reporting` drill from Scalable. At Durable level, enhance it:

- **Cross-period pattern detection:** When meeting rates drop for 2+ consecutive weeks across all script variants and signals, flag as a systemic issue (market shift, seasonal pattern, competitor action) rather than a script/signal problem. Feed into the autonomous optimization loop as a high-priority external anomaly requiring strategic review.
- **Predictive call timing:** Use 3+ months of historical data to build a per-prospect-segment model of optimal call windows. Instead of generic "Tuesday 8-10am," predict that "Series B DevTools CTOs" pick up at different times than "Series A FinTech VPs." Route call queue ordering based on predicted connect probability.
- **Signal decay tracking:** Monitor how signal conversion rates change with signal age. Automatically tighten or loosen recency filters based on observed decay curves. If funding signals convert at 5% when 0-30 days old but 1% when 60-90 days old, auto-adjust the pipeline to prioritize fresher signals.
- **Cost efficiency modeling:** Track cost per meeting trend over time. Factor in all variable costs (Clay credits per prospect, dialer cost per call minute, Instantly cost per email, Fireflies per transcript). Alert when cost per meeting rises above a threshold (e.g., $200) and recommend cost reduction experiments.

Estimated time: 6 hours enhancement. Then always-on.

### 4. Guardrails (CRITICAL)

The autonomous optimization loop must respect these constraints:

- **Rate limit:** Maximum 1 active experiment per variable category at a time. Never test a new script opener AND a new call timing window simultaneously — isolate variables.
- **Revert threshold:** If call-to-meeting rate drops >30% during any experiment (comparing to 4-week pre-experiment baseline), auto-revert immediately and alert the founder.
- **Human approval required for:**
  - ICP definition changes (adding or removing target segments)
  - Script changes that alter the core value proposition or product positioning
  - Signal weight changes that affect >50% of the prospect pipeline
  - Any experiment the hypothesis generator flags as "high risk"
  - Budget changes >20% (e.g., upgrading from Aircall to Orum)
- **Cooldown:** After a failed experiment (revert), wait 7 days before testing a new hypothesis on the same variable. This prevents thrashing.
- **Maximum experiments per month:** 4. If all 4 fail in a single month, pause optimization and flag for human strategic review. The issue is likely not tactical (script, timing) but strategic (ICP, market, product).
- **Never optimize what is not measured:** If a call outcome dimension does not have PostHog tracking (e.g., call quality score), fix tracking first using `posthog-gtm-events` before running experiments on it.
- **Minimum data:** Do not run experiments with fewer than 50 calls per variant. Wait for sufficient volume.
- **Founder override:** The founder can manually override any auto-adopted change by flagging it in Attio. The system reverts and logs the override reason.

### 5. Convergence detection

The optimization loop runs indefinitely but should detect convergence — when the cold calling system has reached its local maximum:

- Track the improvement percentage of each successive adopted experiment
- When 3 consecutive experiments produce <2% improvement on their target metric, declare convergence for that variable category
- At convergence for all categories (script, timing, signals, cadence, voicemail):
  1. Reduce monitoring frequency from daily to weekly
  2. Reduce experiment frequency to 1 per quarter (maintenance mode)
  3. Report: "Cold calling is optimized. Current performance: {meeting rate}% from {volume} calls/month. Cost per meeting: ${amount}. Best signals: {signals}. Best windows: {times}. Further gains require strategic changes (new market segment, product repositioning, new channel addition) rather than tactical optimization."
- Continue watching for market shifts that could break convergence:
  - New competitor entering the market (objection pattern shift)
  - ICP company behavior change (connect rate degradation)
  - Signal source quality change (enrichment provider data decay)
  - Seasonal patterns (holiday periods, budget cycles, fiscal year boundaries)

### 6. Evaluate sustainability

Measure against threshold: Sustained call-to-meeting rate (>=2.5%) over 6 months via autonomous optimization.

Monthly review checklist:
- Call-to-meeting rate: still at or above 2.5% on a rolling 4-week basis?
- Cost per meeting: stable or decreasing?
- Signal ROI: are the top signals still producing? Any signals decayed?
- Script performance: is the current best variant still winning, or has it plateaued?
- Objection landscape: any new objections emerging that are not being handled?
- Autonomous optimization: experiments running and producing results?
- Convergence: how close to the local maximum? How many variable categories converged?
- Pipeline impact: are meetings converting to deals downstream? (Quality, not just quantity)

This level runs continuously. If metrics sustain or improve, the play is durable. If metrics decay despite optimization experiments, diagnose whether the issue is market saturation (exhausted the ICP), message fatigue (every competitor uses the same playbook), competitive displacement (a new entrant is winning deals), or product-market fit drift (the problem you solve matters less now).

## Time Estimate

- Autonomous optimization setup: 15 hours
- Cold-call-script-optimization setup: 8 hours
- Call performance reporting enhancement: 6 hours
- Ongoing experiment review and strategic oversight: ~5 hours/month x 6 months = 30 hours
- Founder calling time: ~30 hours/month x 6 months = 180 hours (separate from play agent hours)

**Total: ~150 hours of agent/setup work over 6 months** (excluding ~180 hours of founder calling time)

Note: Founder calling time is intentionally excluded from the play hour count. This is a founder-led motion — the founder's time on calls is the core execution. The play's agent work is everything that supports, optimizes, and improves those calls.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — contact records, call logging, experiment logs, script version history | Standard stack (excluded) |
| PostHog | Dashboards, anomaly detection, feature flags, experiments, funnels | Standard stack (excluded) |
| n8n | Orchestration — optimization loop, transcript pipeline, reporting, cadence | Standard stack (excluded) |
| Clay | Signal-driven enrichment, phone waterfall, prospect scoring | Growth: $495/mo. [clay.com/pricing](https://www.clay.com/pricing) |
| Aircall | Cloud dialer with local presence, recording, voicemail drop, CRM sync | Professional: $50/user/mo. [aircall.io/pricing](https://aircall.io/pricing/) |
| Orum (optional) | Parallel dialer if volume >500 calls/month | Launch: $250/user/mo. [orum.com/pricing](https://www.orum.com/pricing) |
| Instantly | Pre-call and follow-up email sequences | Growth: $37/mo. [instantly.ai/pricing](https://instantly.ai/pricing) |
| Fireflies.ai | Call transcription for transcript analysis pipeline | Pro: $18/user/mo. [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Anthropic API | Claude for optimization loop (hypothesis generation, transcript analysis, experiment evaluation, weekly briefs) | ~$50-150/mo at Durable volume. [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Play-specific cost: ~$155-455/mo** (Aircall $50 or Orum $250 + Instantly $37 + Fireflies $18 + Anthropic ~$50-150)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics, diagnose anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, generate weekly briefs
- the cold call script optimization workflow (see instructions below) — play-specific transcript analysis, objection pattern tracking, script variant scoring, and data-driven script evolution with founder approval
- `call-performance-reporting` — enhanced at Durable with cross-period pattern detection, predictive call timing, signal decay tracking, and cost efficiency modeling
