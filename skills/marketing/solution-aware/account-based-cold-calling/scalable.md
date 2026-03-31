---
name: account-based-cold-calling-scalable
description: >
  Account-Based Cold Calling — Scalable Automation. The 10x multiplier: parallel dialing, automated
  multi-channel cadences (call + email + LinkedIn), A/B testing on scripts and call windows, and
  signal-prioritized call queues. Agent orchestrates the full pipeline from signal detection to call
  prep to follow-up without manual intervention. Founder's only job is being on the phone.
stage: "Marketing > Solution Aware"
motion: "OutboundFounderLed"
channels: "Direct"
level: "Scalable Automation"
time: "80 hours over 3 months"
outcome: ">=2.5% call-to-meeting rate sustained at 500+ calls/month for 3 months"
kpis: ["Monthly call volume", "Call-to-meeting rate", "Cost per meeting", "Signal-to-meeting rate", "A/B test win rate"]
slug: "account-based-cold-calling"
install: "npx gtm-skills add marketing/solution-aware/account-based-cold-calling"
drills:
  - signal-detection
  - follow-up-automation
  - ab-test-orchestrator
  - dashboard-builder
  - tool-sync-workflow
---

# Account-Based Cold Calling — Scalable Automation

> **Stage:** Marketing > Solution Aware | **Motion:** OutboundFounderLed | **Channels:** Direct

## Outcomes

Find the 10x multiplier for account-based cold calling. At Baseline, 150 calls/2 weeks required manual prospect sourcing and script prep. At Scalable, the agent autonomously sources signal-triggered prospects, ranks the call queue by conversion probability, orchestrates pre-call email and LinkedIn touches, generates scripts, and runs A/B experiments on every variable. Volume scales to 500+ calls/month while sustaining >=2.5% call-to-meeting rate — without proportional increase in founder effort. The founder's only job is making calls.

## Leading Indicators

- Signal detection pipeline running daily, producing 20+ new scored prospects per day
- Call queue automatically prioritized by signal strength + ICP fit + optimal call window
- Multi-channel cadence running: email Day 0, LinkedIn connection Day 1, call Day 3-5, follow-up email Day 7
- A/B experiments running on at least 2 variables simultaneously (script opener, call timing, signal type, voicemail variant)
- Weekly call performance report auto-generated and posted to Slack
- Meeting volume increasing month-over-month without proportional increase in founder hours
- Cost per meeting stable or decreasing as volume scales

## Instructions

### 1. Deploy signal-driven prospect sourcing

Run the `signal-detection` drill to build an always-on signal monitoring pipeline in Clay:

1. **Job change signals**: Configure Clay to detect new hires in buyer persona roles at target companies. Use LinkedIn and People Data Labs enrichment, refreshing daily. A new VP of Engineering at a Series B company is a Tier 1 signal.
2. **Funding signals**: Monitor Crunchbase for funding events in your target industries. Series A-C in last 90 days. Score by relevance to your product category.
3. **Hiring signals**: Scrape job boards for companies posting 3+ roles in your product's domain. Hiring = budget allocated = ready to buy tools.
4. **Technology signals**: Use BuiltWith to detect adoption of complementary or competing tools. A competitor install is a displacement opportunity; a complementary install is an integration sell.
5. **Content signals**: If available, track engagement with competitor content or solution-category content via intent data providers (Bombora, G2 buyer intent).

Configure n8n to route signals into the prospect pipeline:
- Tier 1 signals (funding + job change, or competitor churn): immediate call queue, call within 48 hours
- Tier 2 signals (single strong signal): pre-call email first, call Day 3
- Tier 3 signals (weak or stale signals): nurture sequence, call only if engagement detected

Estimated time: 6 hours.

### 2. Build multi-channel cadences

Run the `follow-up-automation` drill to create coordinated outreach sequences:

**The cold call cadence (per prospect):**
1. Day 0: Pre-call email via Instantly (signal-referenced, under 60 words)
2. Day 1: LinkedIn connection request with personalized note via automation
3. Day 2: LinkedIn follow-up message if connection accepted
4. Day 3-5: Phone call via dialer. If no answer, leave voicemail and retry Day 6.
5. Day 7: Follow-up email referencing the voicemail or call attempt
6. Day 10: Second call attempt at a different time of day
7. Day 14: Breakup email or re-queue for next month if signal is still active

Build this as an n8n workflow that automatically advances prospects through the cadence. The workflow:
- Enrolls a prospect when they enter the Attio call queue
- Triggers Instantly emails at the right time
- Triggers LinkedIn connection via automation tool
- Surfaces the prospect in the dialer queue at the right call window
- Detects replies/engagement and adjusts the cadence (if prospect replies to email, skip to call immediately)
- Logs every touchpoint in Attio and fires PostHog events

Run the `tool-sync-workflow` drill to ensure Instantly replies, LinkedIn acceptances, call outcomes, and Attio deal changes all sync bidirectionally. No data siloed in any single tool.

Estimated time: 8 hours.

### 3. Launch A/B testing

Run the `ab-test-orchestrator` drill to set up experiments on every variable in the cold calling pipeline:

**Script experiments:**
- Opener variants: signal-first vs. problem-first vs. question-first
- CTA variants: specific time proposal vs. open-ended "would it make sense to chat?"
- Objection handling variants: acknowledge-and-pivot vs. question-back

**Timing experiments:**
- Morning (8-10am) vs. afternoon (3-5pm) vs. lunch (11:30am-1pm)
- Tuesday/Wednesday vs. Thursday/Friday
- Same-day-as-email vs. 3-days-after-email

**Signal experiments:**
- Funding signal vs. hiring signal vs. tech signal as the primary call trigger
- Recency: signals from last 30 days vs. 30-90 days

**Voicemail experiments:**
- Signal-specific voicemail vs. generic problem voicemail
- 15-second vs. 25-second voicemail

Use PostHog feature flags to randomly assign variants. Minimum 50 calls per variant before evaluating. Run each experiment for at least 2 weeks. The `ab-test-orchestrator` drill manages experiment lifecycle: start, monitor, evaluate, declare winner, roll out.

Estimated time: 4 hours setup, ongoing management automatic.

### 4. Scale call volume to 500/month

With signal-driven sourcing producing 20+ prospects/day and multi-channel cadences pre-warming them, scale to 25 calls per day (500/month). Infrastructure to support this:

- **Dialer upgrade**: If using Aircall, ensure local presence is configured for all target geographies. If volume justifies it, upgrade to Orum parallel dialer ($250/user/mo) to attempt 5 calls simultaneously and only connect when a human answers — increases effective calls per hour by 3-5x.
- **Call queue management**: Build an n8n workflow that generates the daily call queue each morning. Sort by: (1) Tier 1 signals first, (2) callback requests, (3) second attempts, (4) Tier 2 signals. Show estimated optimal call window per prospect.
- **Script pre-load**: For each call in the queue, the agent pre-generates and attaches the script to the Attio record. Founder opens the record, sees the script, clicks to dial.
- **Post-call automation**: After each call, the n8n workflow auto-processes: fires PostHog events, updates Attio disposition, enrolls in follow-up cadence if needed, and updates the call queue.

**Human action required:** Founder makes the calls. At 25 calls/day with a dialer, this is ~1.5-2 hours of call time per business day. Everything else is automated.

Estimated time: 4 hours setup, then ~30 hours/month of founder calling time.

### 5. Build performance reporting

Run the `dashboard-builder` drill to create:

- Live PostHog dashboard: call volume, connect rate, meeting rate, cost per meeting, pipeline value
- Weekly automated brief: per-signal performance, best call windows, script variant winners, cadence effectiveness, channel attribution (which touch in the multi-channel sequence triggered the meeting)
- Anomaly detection: alerts when connect rate drops below 12%, meeting rate drops below 2%, or call volume drops below 60% of target
- Monthly trend report: cost per meeting trend, pipeline velocity, ICP segment performance

The weekly brief is the primary input that tells the founder what is working and what to adjust.

Estimated time: 3 hours.

### 6. Evaluate against threshold

Measure against: >=2.5% call-to-meeting rate sustained at 500+ calls/month for 3 months.

Monthly evaluation via the `dashboard-builder` dashboard:
- Call-to-meeting rate: meetings / total attempts (target: >=2.5% = 12-13 meetings/month from 500 calls)
- Cost per meeting: (Aircall/Orum + Clay + Instantly + Fireflies) / meetings
- Signal ROI: which signals produce the highest meeting rate per credit spent
- Multi-channel lift: compare meeting rate for prospects who received email + LinkedIn + call vs. call-only
- A/B test velocity: how many experiments completed and how much cumulative improvement

If PASS across 3 months: Document the optimized configuration — winning script variants, best signals, optimal call windows, effective cadence. Proceed to Durable.

If FAIL: Use the weekly briefs and A/B test data to diagnose:
- Volume fine but conversion dropping: message fatigue or market saturation in target segment. Test new ICP segments.
- Conversion fine but volume not scaling: prospect pipeline bottleneck. Add new signal sources or widen ICP.
- Cost per meeting increasing: dialer costs not justified. Evaluate whether Aircall vs. Orum is the right choice for your volume.

## Time Estimate

- Signal detection pipeline: 6 hours
- Multi-channel cadence + tool sync: 8 hours
- A/B testing setup: 4 hours
- Volume scaling infrastructure: 4 hours
- Performance reporting: 3 hours
- Founder calling time: ~30 hours/month x 3 months = 90 hours
- Ongoing optimization review: 2 hours/month x 3 months = 6 hours

**Total: ~80 hours of agent/setup work + ~90 hours of founder calling time over 3 months**

(The "80 hours" reflects setup and agent work. Founder calling time is the core execution that does not scale down at this level — Durable addresses that via optimization.)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — contact records, call logging, pipeline, cadence orchestration | Standard stack (excluded) |
| PostHog | Event tracking, dashboards, A/B test feature flags, anomaly detection | Standard stack (excluded) |
| n8n | Automation — signal routing, cadence orchestration, call queue, reporting | Standard stack (excluded) |
| Clay | Continuous signal-driven enrichment, phone waterfall, scoring | Growth: $495/mo. [clay.com/pricing](https://www.clay.com/pricing) |
| Aircall | Cloud dialer with local presence, recording, voicemail drop, CRM sync | Professional: $50/user/mo. [aircall.io/pricing](https://aircall.io/pricing/) |
| Orum (optional) | Parallel dialer for 3-5x call throughput if volume justifies cost | Launch: $250/user/mo. [orum.com/pricing](https://www.orum.com/pricing) |
| Instantly | Pre-call email and follow-up sequences | Growth: $37/mo. [instantly.ai/pricing](https://instantly.ai/pricing) |
| Fireflies.ai | Call transcription for performance analysis | Pro: $18/user/mo. [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Cal.com | Meeting scheduling | Standard stack (excluded) |

**Play-specific cost: ~$105-305/mo** (Aircall $50 or Orum $250 + Instantly $37 + Fireflies $18)

## Drills Referenced

- `signal-detection` — always-on buying signal monitoring via Clay with tier-based routing
- `follow-up-automation` — multi-channel cadence orchestration (email, LinkedIn, call, follow-up)
- `ab-test-orchestrator` — experiment lifecycle management for scripts, timing, signals, voicemails
- `dashboard-builder` — live dashboard, weekly briefs, anomaly detection, monthly trends
- `tool-sync-workflow` — bidirectional sync between Instantly, LinkedIn, Aircall, Attio, and PostHog
