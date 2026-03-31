---
name: demo-follow-up-sequence-scalable
description: >
  Demo Follow-Up Sequence — Scalable Automation. n8n workflows auto-trigger personalized follow-up
  sequences when demos complete, adapt cadence based on real-time prospect behavior, and run
  structured A/B tests on timing, content, and CTAs to find the 10x multiplier.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Email, Direct"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "Automated demo follow-up on >=90% of demos with >=55% next-step rate maintained at 3x+ volume, plus >=2 A/B test winners adopted"
kpis: ["Automation coverage rate", "Response rate", "Next step conversion rate", "Demo-to-proposal rate", "Experiment win rate"]
slug: "demo-follow-up-sequence"
install: "npx gtm-skills add sales/connected/demo-follow-up-sequence"
drills:
  - follow-up-automation
---

# Demo Follow-Up Sequence — Scalable Automation

> **Stage:** Sales → Connected | **Motion:** OutboundFounderLed | **Channels:** Email, Direct

## Outcomes

Remove the founder from the critical path. When a demo ends, n8n workflows detect the transcript, the agent generates the recap and full cadence, and the sequence launches with one-click approval (or auto-sends for deals matching proven patterns). Behavioral signals — email opens, link clicks, website visits, video views — dynamically adjust what gets sent and when. Structured A/B tests find the highest-converting combination of timing, content, and CTAs.

**Pass threshold:** Automated demo follow-up on >=90% of demos with >=55% next-step rate maintained at 3x+ Baseline volume, plus >=2 A/B test winners adopted.

## Leading Indicators

- Recap generation completes within 15 minutes of transcript availability for >=95% of demos
- Founder review time per sequence drops to <5 minutes (automation handles content generation)
- Behavioral triggers fire correctly: website visit follow-ups, video view escalations, calendar booking cancellations all working
- A/B experiments reaching statistical significance within planned duration
- No degradation in response rate or next-step rate as volume scales

## Instructions

### 1. Build the Automated Demo-to-Follow-Up Pipeline

Run the the demo follow up automation workflow (see instructions below) drill to create the n8n workflow layer:

**Trigger workflow:** Configure n8n to detect demo completion via one of:
- Fireflies webhook (transcript ready for a meeting tagged "demo")
- Attio webhook (deal's `last_meeting_type` set to "demo")
- Cal.com webhook (Product Demo event type completed)

**Recap generation workflow:** When triggered:
1. Fetch the Fireflies transcript (with retry logic for transcript availability delay)
2. Extract demo signals via Claude (features, questions, concerns, interest signals, stakeholders, suggested next step)
3. Pull deal context from Attio (deal value, stage history, previous touches)
4. Generate the full cadence: recap email + 4 follow-up touch content
5. Store everything in Attio
6. Send a Slack notification to the founder with the recap preview and "Approve" / "Edit" buttons
7. On approval: send the recap via Loops and start the cadence scheduler

**Cadence execution workflow:** After recap sends:
1. Day 1 check-in: n8n delay node fires, checks Attio for replies first, generates and sends if no response
2. Day 3 value asset: same pattern — check, generate, send with tracked links
3. Day 5-7 engagement-based touch: pull engagement data from PostHog/Loom/Instantly, branch on engagement level, send appropriate variant
4. Day 10 momentum check: final touch if no response

**Reply detection workflow:** Webhook listener on Instantly/Loops reply events:
1. Classify reply sentiment via Claude (positive/neutral/negative/question/OOO)
2. Pause or cancel remaining cadence touches
3. Route by classification: positive → update deal stage, negative → close sequence, question → notify founder

**Behavioral signal workflow:** PostHog webhooks trigger real-time reactions:
- Pricing page visit → fast-track next-step proposal
- Recap video watched >75% → escalate engagement status
- Cal.com booking → cancel all remaining touches
- New person from same company views content → flag multi-thread opportunity

### 2. Configure Auto-Approval Rules

After 2-3 weeks of reviewing every sequence manually, identify patterns where the agent's output consistently requires zero edits. Create auto-approval rules in n8n:

- **Auto-approve if:** deal value is within the typical range AND urgency is medium or high AND the agent confidence score is >=80%
- **Require review if:** deal value is >2x typical OR urgency is low OR the agent flagged concerns OR it's the first demo with a new industry/persona

Start with 30% auto-approval, increase to 70% as confidence builds. Never auto-approve 100% — keep the founder in the loop on high-value and edge-case deals.

Log which sequences were auto-approved vs reviewed. Compare outcomes to validate that auto-approval doesn't degrade quality.

### 3. Launch A/B Testing Program

Run the the follow up ab testing workflow (see instructions below) drill to systematically optimize the follow-up sequence:

**Month 1 experiments (pick 2):**
- Recap timing: send within 1 hour vs within 4 hours of demo
- Day 3 content type: case study vs integration guide vs Loom walkthrough
- CTA format: Cal.com embed link vs "reply with availability" vs specific proposed time

**Month 2 experiments (pick 2):**
- Check-in timing: Day 1 vs Day 2
- Subject line strategy: reference demo topic vs prospect's pain point vs question-based
- Personalization depth: light (name + company) vs deep (demo-specific pain quotes)

For each experiment:
1. Generate hypothesis with expected impact using Claude
2. Create PostHog feature flag for variant assignment (50/50 split)
3. Wire into the follow-up automation: at each touch, check the flag and select the appropriate variant
4. Monitor daily: sample size progress, guardrail checks (variant not >30% worse than control)
5. When statistical significance reached: evaluate, adopt winner, update the default cadence

### 4. Build the Follow-Up Performance Dashboard

Create a PostHog dashboard with:

1. **Automation funnel:** demo_completed → recap_generated → recap_approved → sequence_started → response_received → next_step_booked
2. **Touch effectiveness:** response rate by touch number (bar chart)
3. **Asset performance:** click-through rate by asset type (table)
4. **Timing analysis:** hours from demo to recap send vs next-step booking rate (scatter)
5. **Experiment status:** running experiments with current sample sizes and preliminary lift
6. **Volume trend:** demos per week and sequences per week (line chart)
7. **Auto-approval rate:** percentage of sequences auto-approved vs reviewed, with outcome comparison

### 5. Scale Volume

Increase demo volume to 3x+ Baseline level. The automation should handle this without proportional increase in founder time. Monitor:

- Founder time per demo should stay flat or decrease (target: <5 min per demo at scale)
- Response rate should not decline >15% as volume increases
- Next-step booking rate should stay >=55%
- Automation error rate should stay <5% (stuck workflows, failed sends, missed triggers)

If metrics degrade at scale:
- Response rate drops → investigate deliverability (sending reputation, email frequency to same domains)
- Next-step rate drops → check if personalization quality degrades with higher throughput
- Errors increase → review n8n workflow logs for failure patterns

### 6. Evaluate Against Threshold

After 2 months:

1. Calculate automation coverage: what percentage of demos got an automated follow-up sequence?
2. Calculate next-step rate: of completed sequences, what percentage booked a next step?
3. Calculate volume: is this >=3x Baseline volume?
4. Count A/B test winners adopted: did at least 2 experiments produce winners that were incorporated?
5. Compare founder time investment: is per-demo time lower than Baseline?

If PASS: The follow-up system runs at scale with maintained conversion. Proceed to Durable for autonomous optimization.
If FAIL: Identify the weakest metric. If coverage is low, fix workflow reliability. If conversion dropped, investigate personalization quality at scale. If experiments didn't produce winners, review experiment design.

## Time Estimate

- 20 hours: Build and test n8n workflows (trigger, recap, cadence, reply detection, behavioral signals)
- 10 hours: Configure auto-approval rules and monitoring
- 15 hours: Set up and run 4 A/B experiments
- 10 hours: Dashboard creation and ongoing monitoring
- 5 hours: Threshold evaluation and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Fireflies | Demo transcription (auto-triggered) | $18/user/mo Pro — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| Attio | CRM — deal pipeline, cadence storage, signal tracking | $29/user/mo Plus — [attio.com/pricing](https://attio.com/pricing) |
| PostHog | Event tracking, experiments, feature flags, dashboards | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Workflow automation (trigger, cadence, reply, behavioral) | Self-hosted free or $24/mo Starter cloud — [n8n.io/pricing](https://n8n.io/pricing) |
| Loops | Transactional email delivery | $49/mo (5K contacts) — [loops.so/pricing](https://loops.so/pricing) |
| Instantly | Alternative: sequenced email at scale | $97/mo Hypergrowth — [instantly.ai/pricing](https://instantly.ai/pricing) |
| Anthropic | Claude API for recap generation and signal extraction | Usage-based, ~$3-15/mo at this volume — [anthropic.com/pricing](https://www.anthropic.com/pricing) |
| Cal.com | Booking links in every follow-up | Free or $12/user/mo — [cal.com/pricing](https://cal.com/pricing) |
| Loom | Recap videos with engagement tracking | $15/user/mo Business — [loom.com/pricing](https://www.loom.com/pricing) |

**Estimated play-specific cost this level:** ~$130-200/mo. Core: Fireflies Pro ($18) + n8n ($24) + Loops ($49) + Anthropic API (~$10) + Loom ($15). Optional: Instantly Hypergrowth ($97) if using instead of Loops.

## Drills Referenced

- the demo follow up automation workflow (see instructions below) — n8n workflows that auto-trigger recap generation, execute the follow-up cadence, detect replies, and react to behavioral signals
- the follow up ab testing workflow (see instructions below) — structured A/B experiments on follow-up timing, content, subject lines, and CTAs using PostHog experiments
