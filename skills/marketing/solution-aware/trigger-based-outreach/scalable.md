---
name: trigger-based-outreach-scalable
description: >
  Trigger-based Outreach — Scalable Automation. Scale to 500+ trigger-based contacts
  per month across 5+ signal types, with automated list refresh, multi-channel
  cadences (email + LinkedIn), A/B testing of signal-specific messaging, n8n-automated
  reply routing, and weekly performance reporting by signal type. Find the 10x
  multiplier by expanding signal coverage and automating the full trigger-to-meeting
  pipeline.
stage: "Marketing > SolutionAware"
motion: "OutboundFounderLed"
channels: "Email, Social"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: "≥ 3% meeting rate sustained at 500+ trigger-based contacts/month over 3 months with ≤ 2 hours/week founder time"
kpis: ["Meeting rate (target ≥ 3%)", "Signal-to-outreach latency (target < 2 hours for high-priority)", "Cost per meeting booked", "Founder time per week (target ≤ 2 hours)", "Signal coverage rate (% of addressable signals detected)"]
slug: "trigger-based-outreach"
install: "npx gtm-skills add marketing/solution-aware/trigger-based-outreach"
drills:
  - build-prospect-list
  - cold-email-sequence
  - follow-up-automation
  - ab-test-orchestrator
  - tool-sync-workflow
---

# Trigger-based Outreach — Scalable Automation

> **Stage:** Marketing > SolutionAware | **Motion:** OutboundFounderLed | **Channels:** Email, Social

## Outcomes

Scale from 150 contacts (Baseline) to 500+ trigger-based contacts per month while maintaining meeting rate within 75% of the Baseline result. The 10x multiplier comes from three levers: expanding signal coverage (more signal types, more sources), adding LinkedIn as a parallel channel, and automating the entire trigger-to-meeting pipeline so the founder only takes meetings. Volume scales with signal availability, not with manual effort.

Pass: Meeting rate ≥ 3% sustained over 3 months at 500+ trigger-based contacts/month, with the founder spending ≤ 2 hours/week.
Fail: Meeting rate drops below 3% for 2 consecutive weeks, or the founder spends more than 4 hours/week.

## Leading Indicators

- Signal detection volume ≥ 150 new triggered prospects per week across all sources (pipeline supply is adequate)
- Signal-to-outreach latency under 2 hours for high-priority signals (speed advantage is maintained at scale)
- Positive reply rate stays ≥ 6% as volume increases (messaging quality is not degrading with automation)
- LinkedIn acceptance rate ≥ 25% for signal-triggered connection requests (social channel adds value)
- A/B test winners produce measurable lift at least once per month
- Cost per meeting stays below $120

## Instructions

### 1. Expand sending infrastructure and add LinkedIn

Add 2 more secondary domains (total: 4 domains, 8 sending accounts). Use the `instantly-account-setup` fundamental. Start warmup via `instantly-warmup`.

Calculate capacity: 8 accounts x 25 sends/day x 5 days/week = 1,000 emails/week max. Target 600-800/week to leave headroom.

**Add LinkedIn as a parallel channel:** Configure a LinkedIn automation tool (Dripify, Expandi, or HeyReach) to send connection requests with signal-specific notes to high-priority triggered prospects. LinkedIn is especially effective for job-change and new-hire signals because the prospect is actively using LinkedIn during transitions.

Build a multi-channel cadence for high-priority signals:
- Day 0: LinkedIn connection request with signal-specific note (under 300 characters)
- Day 1: Email 1 via Instantly
- Day 3: Email 2 via Instantly
- Day 5: LinkedIn follow-up message (if connected)
- Day 7: Email 3 via Instantly (final ask)

For medium-priority signals, use email-only cadence (saves LinkedIn daily limits for high-priority).

### 2. Expand signal coverage to 5+ types

Run the `build-prospect-list` drill as a recurring n8n workflow, extending the Baseline signal types:

**Add new signal sources:**
- **Website visitor identification:** Use an intent data provider (RB2B, Clearbit Reveal, or Leadfeeder) to identify companies visiting your website. If a company matching your ICP visits 2+ pages in a session, treat it as a signal. Use `website-visitor-identification` fundamental.
- **Third-party intent data:** Use Bombora, G2 Buyer Intent, or 6sense to identify companies researching your category. Use `third-party-intent-api` fundamental.
- **Technology adoption/removal:** Use BuiltWith or Wappalyzer enrichment in Clay to detect when ICP companies add or remove technologies in your ecosystem.
- **Content engagement:** Track when target accounts engage with your own content (blog visits from ICP companies, webinar registrations, resource downloads) via PostHog.

Configure all signal sources to feed into a unified Clay table via webhooks. Each signal gets:
- Signal type, source, timestamp, freshness score
- Company and contact data
- Signal strength score: weighted by type (from Baseline conversion data), freshness, and signal intensity (multiple signals from one account = higher score)

**Priority routing via n8n:**
- Score ≥ 80 (multi-signal or high-value signal): immediate outreach via multi-channel cadence
- Score 50-79 (single medium signal): email-only cadence within 24 hours
- Score < 50: add to watch list, re-evaluate if additional signals appear within 14 days

### 3. Build automated reply routing and CRM sync

Run the `follow-up-automation` drill to create n8n workflows handling the entire reply lifecycle:

- **Positive reply detected:** n8n receives Instantly webhook, AI classifies sentiment via Claude API, creates deal in Attio at "Meeting Requested" stage with signal type attribution, sends Slack notification to founder with reply text and signal context, removes contact from all active sequences and LinkedIn cadences.
- **"Not now" reply:** Log in Attio with "Nurture" status and signal type. Set 45-day follow-up. If the original signal is still active at follow-up time, re-engage with updated context.
- **Negative reply or unsubscribe:** Global suppression in Instantly and LinkedIn tool. Update Attio to "Do Not Contact."
- **LinkedIn acceptance (no reply):** If the prospect accepts the connection but does not reply after 48 hours, send a short follow-up message referencing the signal.
- **Out of office:** Pause sequence, resume 3 days after OOO end date.

Run the `tool-sync-workflow` drill to connect all data into PostHog:
- Every signal detection, outreach send, reply, LinkedIn action, and meeting booking flows into PostHog as events with consistent properties (signal_type, signal_freshness, campaign_id, channel).
- Attio deal stages update in real-time based on PostHog events.

### 4. Launch structured A/B testing by signal type

Run the `ab-test-orchestrator` drill. At 500+ contacts/month, you have enough volume to test one variable per signal type per month:

**Month 1: Test messaging angles per signal type.**
- Funding signals: test "congratulations + ROI" vs. "congratulations + similar company story"
- Job-change signals: test "first 90 days" angle vs. "what [previous company] was missing" angle
- Split 50/50 within each signal type. Minimum 100 sends per variant.

**Month 2: Test outreach timing relative to signal.**
- Test sending within 24 hours of signal vs. 3-5 days after signal (for funding signals, some companies need a few days to digest before evaluating tools)
- Test morning vs. afternoon sends for hiring-spree signals

**Month 3: Test channel mix.**
- Test email-first vs. LinkedIn-first for job-change signals
- Test 2-step vs. 3-step email sequence for competitor-churn signals

Track all tests in PostHog using `posthog-custom-events`. Apply winners after each test reaches statistical significance (95% confidence, 100+ per variant).

### 5. Build weekly performance reporting

Build an n8n workflow that runs every Friday and produces a performance report:

**Report sections:**
1. **Signal pipeline health:** signals detected this week by type and source. Compare to 4-week average. Flag any source that dropped >30%.
2. **Outreach volume:** emails sent and LinkedIn messages sent, by signal type. Signal-to-outreach latency by priority tier.
3. **Conversion funnel by signal type:** signal -> outreach -> reply -> meeting. Identify which signal types are above/below the 3% meeting rate target.
4. **Channel performance:** email vs. LinkedIn reply rates for multi-channel cadences. Which channel produces the first positive touch?
5. **A/B test status:** active tests, interim results, completed tests with winners.
6. **Cost efficiency:** cost per meeting by signal type (factor in Clay credits per signal type, Instantly per-email cost, LinkedIn tool cost).

Route the report to Slack with a one-line summary and one recommended action.

### 6. Monitor and optimize for 3 months

Run the system for 12 weeks. The agent's weekly responsibilities:
1. Review Friday performance report
2. Verify all n8n workflows executed without errors
3. Confirm signal detection is producing ≥ 150 new prospects/week
4. Check no domain health scores dropped below 85%
5. Apply A/B test winners when tests conclude
6. Retire signal types that consistently convert below 1% (they are noise, not signal)
7. Expand top-performing signal types (add more sources or widen filters)

**Human action required:** The founder responds to positive replies (Slack notifications) and takes meetings. Target: ≤ 2 hours/week.

### 7. Evaluate after 3 months

Compute over the full 3-month period:
- Average monthly meeting rate (overall and per signal type)
- Total meetings booked
- Cost per meeting (overall and per signal type)
- Founder hours per week
- Signal type ranking by ROI (meetings per dollar spent on that signal type)
- Multi-channel lift: did adding LinkedIn improve meeting rate vs. email-only?

- **PASS (≥ 3% meeting rate, ≤ 2 hours/week founder time):** Scalable is proven. Document: winning signal types ranked by ROI, optimal channel mix per signal type, best message variants, and cost per meeting. Proceed to Durable.
- **MARGINAL (2-2.9% meeting rate):** Volume may be diluting signal quality. Try: raise the signal score threshold to 60+, focus on top 3 signal types only, or improve personalization quality for lower-performing signal types.
- **FAIL (< 2% meeting rate OR > 4 hours/week founder time):** The play does not scale. Diagnose: Are new signal sources lower quality than original Baseline sources? Is the personalization degrading at volume? Is LinkedIn automation hurting deliverability or brand? Fix the root cause or accept that this play works best at Baseline volume with tighter signal targeting.

## Time Estimate

- Sending infrastructure expansion + LinkedIn tool setup: 4 hours (Week 1)
- New signal source configuration (website visitors, intent data, tech adoption): 8 hours (Weeks 1-2)
- Multi-channel cadence design and configuration: 4 hours (Week 2)
- Reply routing and CRM sync automation: 5 hours (Week 2)
- A/B test framework setup: 3 hours (Week 2)
- Weekly performance reporting: 3 hours (Week 3)
- Setup subtotal: 27 hours
- Weekly agent monitoring: 2 hours/week x 12 weeks = 24 hours
- Founder reply time: 2 hours/week x 12 weeks = 24 hours
- Total: ~75 hours over 3 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Email sequencing, warmup, A/B testing, reply detection | Hypergrowth plan $97/mo ([instantly.ai/pricing](https://instantly.ai/pricing)) |
| Clay | Signal detection, enrichment, personalization, daily list refresh | Growth plan $495/mo ([clay.com/pricing](https://clay.com/pricing)) |
| Attio | CRM, deal tracking, signal attribution | Plus plan $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Signal-to-meeting funnel, A/B test measurement | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Reply routing, signal pipeline, reports, CRM sync | Pro plan $60/mo or self-host free ([n8n.io/pricing](https://n8n.io/pricing)) |
| Dripify or HeyReach | LinkedIn automation (connection requests, messages) | Dripify $79/mo ([dripify.io/pricing](https://dripify.io/pricing)) or HeyReach $79/mo ([heyreach.io/pricing](https://heyreach.io/pricing)) |
| Cal.com | Meeting booking | Free plan ([cal.com/pricing](https://cal.com/pricing)) |
| Secondary domains (x4) | Sending infrastructure | ~$50/year total |
| Google Workspace (x4) | Sending accounts | ~$28/mo total ($7/user/mo) |

**Estimated monthly cost for Scalable:** ~$790-870/mo + ~$50/year for domains

## Drills Referenced

- `build-prospect-list` — recurring n8n workflow expanding signal sources (website visitors, intent data, tech adoption)
- `cold-email-sequence` — signal-specific multi-channel cadences across email and LinkedIn
- `follow-up-automation` — automated reply routing, sentiment classification, and CRM sync via n8n
- `ab-test-orchestrator` — structured A/B tests on messaging angles, timing, and channel mix per signal type
- `tool-sync-workflow` — unified data pipeline connecting Clay, Instantly, LinkedIn tool, Attio, and PostHog
