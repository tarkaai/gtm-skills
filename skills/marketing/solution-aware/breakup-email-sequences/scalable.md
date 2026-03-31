---
name: breakup-email-sequences-scalable
description: >
  Breakup Email Sequences — Scalable Automation. Automated pipeline that detects when
  prospects go silent across any outbound sequence, waits the optimal cool-off period,
  enriches with fresh signals, generates personalized breakup emails, and sends via
  Instantly with A/B testing on breakup angles. Find the 10x multiplier by turning
  every stalled outbound sequence into a breakup re-engagement opportunity.
stage: "Marketing > SolutionAware"
motion: "OutboundFounderLed"
channels: "Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥ 4% re-engagement rate sustained at 400+ breakup emails/month with ≤ 1 hour/week founder time"
kpis: ["Re-engagement rate (target ≥ 4%)", "Meetings booked per month from breakup replies", "Signal lift (target ≥ 1.8x)", "Pool throughput (silent prospects entering and exiting breakup pipeline)", "Cost per re-engaged prospect"]
slug: "breakup-email-sequences"
install: "npx gtm-skills add marketing/solution-aware/breakup-email-sequences"
drills:
  - follow-up-automation
  - ab-test-orchestrator
---

# Breakup Email Sequences — Scalable Automation

> **Stage:** Marketing > SolutionAware | **Motion:** OutboundFounderLed | **Channels:** Email

## Outcomes

Transform breakup emails from a manual batch process into an always-on pipeline. Every prospect who completes any outbound sequence without replying automatically enters the breakup pipeline: cool-off period, signal enrichment, personalized breakup copy, conditional send, and reply routing — all without the founder touching it until a positive reply arrives. The 10x multiplier comes from connecting breakup sequences to ALL outbound plays (not just one sequence) and from A/B testing breakup angles to find the optimal re-engagement framing for each ICP segment.

Pass: 4% or higher re-engagement rate sustained over 2 months at 400+ breakup emails per month, with the founder spending no more than 1 hour/week on breakup-related tasks.
Fail: Re-engagement rate drops below 4% for 2 consecutive weeks, or the founder spends more than 2 hours/week.

## Leading Indicators

- Automated pipeline processes 100+ new silent prospects per week without errors
- Signal detection coverage stays above 25% (at least 1 in 4 silent prospects has a detectable signal)
- A/B tests produce at least one significant winner per month
- Reply routing correctly classifies 90%+ of replies (spot-check weekly)
- No sending account's health drops below 85%
- Cost per re-engaged prospect stays below $20

## Instructions

### 1. Build the automated silent-prospect pipeline

Create an n8n workflow triggered by Attio status changes. When any prospect's status changes to "Sequence Completed - No Reply" in Attio (from any outbound play), the workflow:

1. Records the prospect's details: contact ID, original sequence slug, last touch date, ICP segment
2. Calculates the cool-off date: last touch date + 35 days (the sweet spot from Baseline data — adjust based on your results)
3. Creates a scheduled trigger for the cool-off date
4. On the cool-off date: enriches the prospect via Clay (signal detection, email re-verification)
5. If email is no longer valid: mark as "Stale — Do Not Breakup" in Attio, exit
6. If valid: segment as signal-detected or no-signal, push to the appropriate Instantly breakup campaign

This means the breakup pipeline is fed automatically by every outbound play you run. More outbound volume = more breakup opportunities, with zero manual list building.

Using the `follow-up-automation` drill, configure the n8n workflow with these safety checks:
- **De-duplication:** Never send a breakup to someone who already received one in the last 180 days
- **Active deal check:** Skip prospects who entered a deal pipeline since going silent (someone else re-engaged them)
- **Suppression list check:** Skip Do Not Contact, unsubscribed, or bounced-in-prior-campaign prospects
- **Volume throttle:** Cap at 30 breakup sends per day per sending account

### 2. Scale signal detection

At Baseline, signal detection was one-time enrichment. At Scalable, run it as a recurring pipeline:

Configure Clay with a scheduled enrichment table that refreshes weekly for all prospects in the cool-off queue:

- **Job change monitoring:** People Data Labs + LinkedIn (check monthly for the cool-off cohort)
- **Company funding:** Crunchbase enrichment (check on cool-off date)
- **Hiring signals:** Job board monitoring for roles in your product's domain
- **Content engagement:** LinkedIn post and engagement monitoring for problem-space keywords
- **Competitor signals:** G2 review monitoring, competitor mentions on social

When a signal is detected during the cool-off period, ACCELERATE the breakup: reduce the cool-off period to 21 days (the signal creates a natural re-engagement moment). Update the `recent_signal` and `signal_relevance` variables in Clay.

### 3. Expand the breakup copy library

At Baseline you had 2 variants (signal and no-signal). At Scalable, expand to test multiple angles within each segment. Run the the breakup email copy workflow (see instructions below) drill to create:

**No-signal variants (4 Email 1 variants):**
- Variant A: "Closing your file" — the original loss-aversion framing
- Variant B: "Quick update" — brief note that your product has improved since they last heard from you, followed by the close
- Variant C: "One question" — ask a single diagnostic question about their current solution (engagement play)
- Variant D: "Thought of you" — tie to an industry trend or market shift, then close

**Signal-detected variants (3 Email 1 variants):**
- Variant A: Signal-referenced close — the original format
- Variant B: Signal + peer reference — "[Similar company] just went through the same [signal event] and here's what they did"
- Variant C: Signal + contrarian insight — share a non-obvious take on what their signal means for their category

**Email 2 variants (3 low-friction asset types):**
- Variant A: 90-second video walkthrough relevant to their ICP segment
- Variant B: Benchmark data point comparing their company size/industry to peers
- Variant C: Case study one-pager from a similar company

### 4. Launch A/B testing on breakup angles

Run the `ab-test-orchestrator` drill. Breakup emails have enough volume at Scalable to test one variable at a time:

**Test 1 (Weeks 1-3): Subject line.**
- Control: "closing your file"
- Variant: "last note from me"
- Measure by: open rate (since breakup response depends heavily on the email being opened)
- Minimum sample: 200 per variant

**Test 2 (Weeks 3-5): No-signal Email 1 angle.**
- Rotate through Variants A-D
- Measure by: re-engagement rate (positive replies / sends)
- Run as a multi-arm test with 150+ per variant

**Test 3 (Weeks 5-7): Signal-detected Email 1 angle.**
- Rotate through Variants A-C
- Measure by: re-engagement rate
- 100+ per variant (smaller pool)

**Test 4 (Weeks 7-8): Email 2 asset type.**
- Test the 3 asset variants
- Measure by: "send it" reply rate
- Only test among Email 1 openers (conditional send)

Apply winners after each test. Retire losing variants. Document results in PostHog.

### 5. Automate reply routing and classification

Using the `follow-up-automation` drill, extend the n8n reply routing to handle breakup-specific reply patterns:

- **"Actually, let's talk" / meeting interest:** Create deal in Attio at "Meeting Booked" with tags `source: breakup-email-sequences`, `breakup_variant: [variant ID]`, `original_sequence: [slug]`. Notify founder via Slack with context: "Breakup reply from [Name] at [Company] — originally contacted via [original sequence] on [date]. Signal: [signal or 'none']. Reply: [full text]." Remove from all active sequences.
- **"Send it" / asset request:** Auto-send the matched asset via n8n (email with the asset attached or linked). Create a follow-up task in Attio for 3 days later. If no meeting books within 14 days of asset delivery, mark as "Asset Sent — No Conversion."
- **"Not now" / timing reply:** Log in Attio with status "Breakup — Maybe Later." Set 90-day automated reminder. Do not send another breakup — they responded.
- **"Remove me" / unsubscribe:** Add to global suppression in Instantly. Update Attio to "Do Not Contact." Immediate, no exceptions.
- **Negative / hostile:** Log in Attio. Suppress from all future outreach for this play. Do not respond.
- **Out of office:** Re-queue for breakup send 7 days after OOO end date.

AI classification: Use Claude API via n8n to classify reply sentiment and type. Spot-check 10 classifications per week manually. If accuracy drops below 90%, retrain the prompt with misclassified examples.

### 6. Build the performance reporting pipeline

Create an n8n workflow that runs weekly (Friday):

1. Pull from PostHog: breakup sends, opens, positive replies (by segment and variant), meetings booked, assets sent
2. Pull from Attio: deals created from breakup source, deal values, pipeline progression
3. Pull from Clay: signal detection coverage rate, new signals detected this week
4. Compute: blended re-engagement rate, signal lift, asset conversion rate, cost per re-engaged prospect, pool throughput (new silent prospects entering vs. breakup sends going out)
5. Compare to Baseline rates and 4-week rolling average
6. Generate report and post to Slack

The report should flag: any variant whose reply rate dropped >25% from its peak (fatigue), any week where pool inflow < breakup send rate (sustainability concern), and any A/B test reaching statistical significance.

**Human action required:** The founder reviews the weekly Slack report (2 minutes) and responds to positive replies. All other operations are automated. Target: ≤ 1 hour/week total.

### 7. Monitor pool sustainability

Breakup sequences have a unique scaling constraint: the prospect pool is finite. You can only send breakups to people who completed a prior sequence and went silent. Track:

- **Pool inflow rate:** How many new silent prospects enter the breakup queue each week (driven by total outbound volume across all plays)
- **Pool outflow rate:** How many breakup emails you send per week + prospects who re-engage + prospects who bounce/stale
- **Net pool growth:** Inflow - outflow. If negative for 3+ consecutive weeks, you are depleting the pool faster than it refills.

If the pool is shrinking:
- Reduce breakup send volume to match inflow
- Expand the cool-off window to 45-60 days (processes the pool more slowly)
- Increase total outbound volume in feeding plays (more cold emails = more eventual silent prospects)

Do NOT compromise on the 30-day minimum cool-off to speed up pool throughput. Sending breakups too soon destroys the psychological framing.

### 8. Evaluate after 2 months

Compute over the full 2-month period:
- Average monthly breakup send volume
- Average re-engagement rate (blended and by segment)
- Total meetings booked from breakup-recovered prospects
- Signal lift (signal vs. no-signal re-engagement rate ratio)
- Cost per re-engaged prospect (Clay + Instantly pro-rated costs / positive replies)
- Founder hours per week on this play
- Pool sustainability (net pool growth trend)

- **PASS (≥ 4% re-engagement rate, ≤ 1 hour/week founder time, pool net growth ≥ 0):** Scalable is proven. The breakup pipeline runs autonomously and sustainably. Proceed to Durable.
- **MARGINAL (3-3.9% re-engagement rate OR pool slowly depleting):** Performance is close but either rates are soft or the pool is not sustainable. Tighten: improve signal detection coverage to lift the blended rate, or work with upstream outbound plays to increase total volume. Re-run for 1 more month.
- **FAIL (< 3% re-engagement rate OR > 2 hours/week founder time):** The play does not scale. Diagnose: Is the automated copy losing the personal touch? Is signal detection producing false positives? Is reply classification routing too many false positives to the founder? Fix the root cause or accept that breakup emails work best as a periodic manual batch (Baseline level) and redirect automation budget elsewhere.

## Time Estimate

- Automated silent-prospect pipeline in n8n: 8 hours (Week 1)
- Scaled signal detection in Clay: 4 hours (Week 1)
- Expanded copy library with the breakup email copy workflow (see instructions below) drill: 3 hours (Week 1)
- A/B test setup with `ab-test-orchestrator` drill: 4 hours (Week 2)
- Reply routing automation: 5 hours (Week 2)
- Performance reporting pipeline: 3 hours (Week 2)
- Pool sustainability monitoring setup: 2 hours (Week 2)
- Setup subtotal: 29 hours
- Weekly monitoring and A/B test management: 2 hours/week x 8 weeks = 16 hours
- Founder reply time: 1 hour/week x 8 weeks = 8 hours
- Final evaluation: 3 hours
- Ongoing subtotal: 27 hours
- Total: ~56-60 hours over 2 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Breakup email delivery, conditional steps, A/B sending, reply detection | Growth plan $37/mo ([instantly.ai/pricing](https://instantly.ai/pricing)) |
| Clay | Signal detection, enrichment, email re-verification, weekly pipeline refresh | Launch plan $185/mo or Growth plan $495/mo for higher volume ([clay.com/pricing](https://clay.com/pricing)) |
| Attio | CRM, deal attribution, reply logging, pipeline tracking | Free-Plus plan $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Event tracking, funnel analysis, A/B test measurement | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Pipeline automation, reply routing, reporting, signal orchestration | Pro plan $60/mo or self-host free ([n8n.io/pricing](https://n8n.io/pricing)) |
| Cal.com | Meeting booking for re-engaged prospects | Free plan ([cal.com/pricing](https://cal.com/pricing)) |
| Claude API | Reply sentiment classification | ~$5-15/mo at this volume ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |

**Estimated monthly cost for Scalable:** ~$330-630/mo (shares sending infrastructure with primary outbound plays)

## Drills Referenced

- the breakup email copy workflow (see instructions below) — expanded copy library with 4 no-signal variants, 3 signal variants, and 3 asset types for A/B testing
- `follow-up-automation` — automated pipeline from silent-prospect detection through cool-off, enrichment, send, and reply routing
- `ab-test-orchestrator` — structured A/B testing on subject lines, breakup angles, signal framing, and asset types
