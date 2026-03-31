---
name: outbound-founder-email-durable
description: >
  Outbound founder-led email — Durable Intelligence. Autonomous AI agents manage
  the entire outbound pipeline: signal-based list refresh, automatic copy rotation
  when metrics decay, continuous A/B testing, deliverability monitoring, and weekly
  performance optimization. The founder's only role is taking meetings. Meeting rate
  sustains or improves over 6 months.
stage: "Marketing > SolutionAware"
motion: "OutboundFounderLed"
channels: "Email"
level: "Durable Intelligence"
time: "250 hours over 6 months"
outcome: "Meeting rate sustained at ≥ 1.6% for 6 consecutive months with ≤ 1 hour/week founder involvement"
kpis: ["Meeting rate trend (flat or improving over 6 months)", "Cost per meeting trend (flat or decreasing)", "Message fatigue index (reply rate decay per sequence variant)", "Domain health composite score", "Signal-to-meeting conversion rate"]
slug: "outbound-founder-email"
install: "npx gtm-skills add marketing/solution-aware/outbound-founder-email"
drills:
  - autonomous-optimization
  - signal-detection
  - ab-test-orchestrator
  - dashboard-builder
  - follow-up-automation
  - tool-sync-workflow
  - threshold-engine
---

# Outbound Founder-Led Email — Durable Intelligence

> **Stage:** Marketing > SolutionAware | **Motion:** OutboundFounderLed | **Channels:** Email

## Outcomes

The outbound founder email system runs autonomously. AI agents detect buying signals, build lists, rotate copy variants, run A/B tests, monitor deliverability, and generate weekly optimization recommendations. The founder takes meetings and occasionally approves major copy changes. Meeting rate holds at or above the Scalable baseline for 6 consecutive months despite market changes, message fatigue, and seasonal variation.

Pass: Meeting rate ≥ 1.6% sustained for 6 consecutive months with the founder spending ≤ 1 hour/week.
Fail: Meeting rate drops below 1.6% for 3 consecutive weeks despite automated interventions, or the system requires more than 2 hours/week of founder time.

## Leading Indicators

- Message fatigue index stays below 2x decay (no single sequence variant's reply rate drops more than 50% from its peak before it is rotated out)
- Signal-to-meeting conversion rate ≥ 3% (signal-detected prospects convert at a higher rate than cold list prospects)
- Domain health composite score stays above 88% across all accounts
- A/B tests produce a winner at least once per month (the system is still finding improvements)
- Cost per meeting trends flat or downward over the 6-month period

## Instructions

### 1. Deploy signal-based list targeting

Run the `signal-detection` drill to move from systematic list building (Scalable) to signal-triggered prospecting. Configure Clay to continuously monitor for buying signals:

**High-priority signals (trigger immediate outreach):**
- New VP/C-level hire matching your buyer persona at a target company (job change = budget unlock, new priorities)
- Funding round closed in last 30 days at a company matching your ICP (new money seeking ROI)
- Company posted 3+ job openings in your product's domain in the last 30 days (building a team, need tools)

**Medium-priority signals (add to next weekly batch):**
- Competitor's customer posted a negative review or complained publicly (switching intent)
- Company adopted a complementary tool in your integration ecosystem (expansion opportunity)
- Key contact at a target company engaged with your content or visited your website (awareness signal)

Build an n8n workflow that:
1. Receives signals from Clay via webhook (daily scan)
2. Scores each signal by type and recency
3. High-priority signals: immediately enrich the contact, generate a personalized Email 1 referencing the signal, and add to a dedicated "signal-triggered" Instantly campaign
4. Medium-priority signals: add to the weekly enrichment batch for standard processing

For signal-triggered emails, customize the Email 1 personalization line to reference the signal directly: "Congrats on the Series B — when [similar company] raised theirs, they used the first 90 days to [specific outcome your product enabled]."

### 2. Build the copy rotation engine

Message fatigue is the primary threat to Durable performance. Every email variant eventually decays as more prospects in your market see similar messaging.

Create a copy library with at least 6 variants of each email step:
- 6 Email 1 variants (different personalization angles: tech stack, recent hire, competitor pain, industry trend, funding event, company milestone)
- 4 Email 2 variants (different proof points from different customers)
- 3 Email 3 variants (different CTAs: calendar link, resource offer, specific question)

Build an n8n workflow that tracks each variant's reply rate over a rolling 30-day window via PostHog. When a variant's reply rate drops below 70% of its peak rate (message fatigue threshold), the workflow:
1. Pauses the variant
2. Alerts the agent to draft a replacement
3. Rotates in the next variant from the library
4. Logs the rotation event in PostHog for analysis

Run the the founder cold email copy workflow (see instructions below) drill to generate new variants as needed. The founder reviews and approves new variants once per month.

**Human action required:** Founder reviews and approves new copy variants once per month (~30 minutes). The agent drafts variants based on recent meeting conversations and market changes.

### 3. Deploy continuous A/B testing

Run the `ab-test-orchestrator` drill in continuous mode. The system always has one active test running:

**Test rotation (6-month plan):**
- Months 1-2: Test new subject line formulas (2 tests per month, 200+ sends per variant)
- Month 2-3: Test proof point framing (metric vs. narrative vs. question)
- Month 3-4: Test sequence timing (day gaps between steps)
- Month 4-5: Test ICP segment expansion (adjacent verticals or company sizes)
- Month 5-6: Test re-engagement (prospects who did not reply 90+ days ago with entirely new messaging)

Build an n8n workflow that:
1. Receives A/B test results from PostHog weekly
2. When a test reaches statistical significance (95% confidence, minimum 200 per variant), declares a winner
3. Applies the winner to the live campaign
4. Starts the next test in the rotation
5. Logs all test results and decisions for the monthly review

### 4. Build the performance dashboard and alert system

Run the `dashboard-builder` drill to create a PostHog dashboard specifically for this play:

**Dashboard panels:**
- Weekly meeting rate trend (8-week rolling, with Scalable baseline line at 1.6%)
- Reply rate by variant (identify which copy is performing and which is fatiguing)
- Signal-to-meeting funnel (signals detected -> contacted -> replied -> meeting booked)
- Domain health scores across all sending accounts
- Cost per meeting trend
- Active A/B test status and interim results
- Sent volume by ICP segment

**Alerts (via n8n):**
- Meeting rate drops below 1.6% for 2 consecutive weeks -> alert + auto-diagnostic
- Any domain health score drops below 85% -> pause that account, redistribute volume
- Bounce rate exceeds 3% on any campaign -> pause campaign, investigate list quality
- Unsubscribe rate exceeds 1% on any campaign -> pause campaign, review messaging
- No new signals detected for 3 consecutive days -> check Clay integrations

Run the `threshold-engine` drill to configure guardrails:
- **Volume guardrail:** Never exceed 40 sends/day per account
- **Quality guardrail:** If negative reply rate exceeds 5% on any campaign, pause and review
- **Compliance guardrail:** Unsubscribe rate above 0.5% triggers messaging review
- **Budget guardrail:** Cost per meeting exceeding $200 triggers an efficiency review

### 5. Automate the weekly optimization cycle

Build an n8n workflow that runs every Friday and produces a weekly optimization report:

1. **Data pull:** Retrieve the last 7 days of events from PostHog (sends, replies, meetings, bounces, unsubscribes), domain health from Instantly API, and list quality metrics from Clay
2. **Comparison:** Compare this week's metrics to the prior 4-week average and to the Scalable baseline
3. **Diagnosis:** If any metric dropped >10% from the 4-week average, identify the probable cause:
   - Reply rate dropped: check which variants decayed, check if list source changed
   - Meeting rate dropped but reply rate held: check if positive replies are not converting (reply quality issue, or booking friction)
   - Bounce rate spiked: check Clay verification and list recency
   - Domain health dropped: check Instantly warmup status
4. **Recommendation:** Generate one specific action item for the coming week (e.g., "Rotate Email 1 Variant C — reply rate has decayed 40% from peak. Draft replacement focusing on [industry trend].")
5. **Delivery:** Send the report to the founder via Slack with a one-line summary and the recommended action

**Human action required:** The founder reads the weekly Slack summary (2 minutes) and approves the recommended action if it involves copy changes. All other actions (domain rotation, variant rotation, volume adjustments) execute automatically.

### 6. Run monthly deep review

Build an n8n workflow that runs on the 1st of each month:

1. Pull 30-day aggregate metrics
2. Compare to prior month and to Scalable baseline
3. Identify: best-performing ICP segment, best-performing signal type, winning A/B test variants, and any metric that worsened
4. Generate a monthly brief with recommendations:
   - Which ICP segments to expand or contract
   - Which signal types to add or retire
   - Which copy angles are working and which are fatigued
   - Budget efficiency (cost per meeting relative to LTV)
5. Flag if any structural change is needed (e.g., "Consider adding a 4th email step" or "Test LinkedIn parallel touch")

**Human action required:** The founder reviews the monthly brief (~30 minutes) and decides on any strategic changes (new ICP segments, new competitive positioning, budget adjustments).

### 7. Sustain for 6 months

The system runs continuously. The agent's responsibilities:
- Ensure all n8n workflows execute daily/weekly without errors
- Respond to alerts within 4 hours
- Rotate copy variants when fatigue threshold is triggered
- Apply A/B test winners when tests conclude
- Generate weekly and monthly reports
- Maintain the copy library with fresh variants

The founder's responsibilities:
- Respond to positive replies in Slack (delegatable to an EA or sales hire at this stage)
- Take meetings
- Approve new copy variants once per month
- Review monthly brief and make strategic decisions

### 8. Evaluate sustainability after 6 months

Compute over the full 6-month period:
- Monthly meeting rate for each of the 6 months
- Meeting rate trend (is it stable, improving, or decaying?)
- Total cost / total meetings = cost per meeting
- Total founder hours / total meetings = founder time per meeting
- Number of A/B tests run and number that produced significant improvements
- Signal-to-meeting conversion rate vs. cold-list conversion rate

- **PASS (meeting rate ≥ 1.6% for all 6 months, founder ≤ 1 hour/week):** The play is durable. It runs autonomously and produces consistent pipeline. Consider: increasing volume further, delegating the founder role to a sales hire using the same playbook, or applying the system to new markets.
- **DECLINING (meeting rate held for 4+ months then decayed below 1.6%):** Market saturation or message fatigue outpacing the rotation engine. Options: expand to a new ICP segment, change the competitive positioning (if the market shifted), or reduce volume and increase quality (tighter scoring, more personalization).
- **FAIL (meeting rate below 1.6% for 3+ consecutive weeks at any point):** The automated system is not adapting fast enough. Diagnose: Is the copy rotation engine catching fatigue in time? Are the A/B tests producing winners? Is the signal detection adding value? Fix the specific broken component or accept that this play requires more manual oversight than Durable allows.

## Time Estimate

- Signal detection setup: 8 hours (Month 1)
- Copy rotation engine: 6 hours (Month 1)
- Continuous A/B testing setup: 4 hours (Month 1)
- Dashboard and alert system: 6 hours (Month 1)
- Weekly optimization workflow: 4 hours (Month 1)
- Monthly review workflow: 3 hours (Month 1)
- Setup subtotal: 31 hours
- Weekly agent monitoring: 3 hours/week x 24 weeks = 72 hours
- Weekly founder time: 1 hour/week x 24 weeks = 24 hours
- Monthly founder review: 30 min x 6 months = 3 hours
- Copy variant generation (ongoing): 4 hours/month x 6 months = 24 hours
- Ongoing subtotal: ~123 hours agent + ~27 hours founder
- Grand total: ~250 hours over 6 months (180 agent, 27 founder, 43 buffer/troubleshooting)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Email sequencing, warmup, A/B testing, reply detection, domain rotation | Hypergrowth plan $97/mo ([instantly.ai/pricing](https://instantly.ai/pricing)) |
| Clay | Signal detection, enrichment, personalization, weekly list refresh | Growth plan $495/mo ([clay.com/pricing](https://clay.com/pricing)) |
| Attio | CRM, deal tracking, contact management | Plus plan $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Dashboards, funnel analysis, A/B test measurement, alerting | Free tier: 1M events/mo, usage-based beyond ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | All automation: reply routing, list refresh, reports, copy rotation, alerts | Pro plan $60/mo or self-host free ([n8n.io/pricing](https://n8n.io/pricing)) |
| Cal.com | Meeting booking link | Free plan ([cal.com/pricing](https://cal.com/pricing)) |
| Secondary domains (x4) | Sending infrastructure | ~$50/year total |
| Google Workspace (x4) | Sending accounts | ~$28/mo total ($7/user/mo) |

**Estimated monthly cost for Durable:** ~$710-740/mo + ~$50/year for domains

## Drills Referenced

- `signal-detection` — continuous monitoring for buying signals that trigger prioritized outreach
- `ab-test-orchestrator` — continuous A/B testing rotation across subject lines, proof points, timing, and segments
- `dashboard-builder` — PostHog dashboard with weekly/monthly reporting panels and threshold lines
- `follow-up-automation` — automated reply classification, routing, and CRM updates via n8n
- `tool-sync-workflow` — unified data pipeline connecting Instantly, Clay, Attio, PostHog, and n8n
- `threshold-engine` — guardrails for volume, quality, compliance, and budget that auto-pause when breached
