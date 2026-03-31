---
name: outbound-founder-email-scalable
description: >
  Outbound founder-led email — Scalable Automation. Scale to 500-1,000 emails/week
  across multiple ICP segments with automated list refresh, A/B testing of subject
  lines and proof points, n8n-automated reply routing, and weekly performance reporting.
  Find the 10x multiplier without proportional founder time.
stage: "Marketing > SolutionAware"
motion: "OutboundFounderLed"
channels: "Email"
level: "Scalable Automation"
time: "70 hours over 2 months"
outcome: "Meeting rate ≥ 1.6% sustained over 2 months at 500+ emails/week with ≤ 2 hours/week of founder time"
kpis: ["Meeting rate (target ≥ 1.6%)", "Positive reply rate (target ≥ 4%)", "Cost per meeting booked", "Founder time per meeting (target < 30 min)", "Domain health score across all sending accounts"]
slug: "outbound-founder-email"
install: "npx gtm-skills add marketing/solution-aware/outbound-founder-email"
drills:
  - build-prospect-list
  - enrich-and-score
  - cold-email-sequence
  - follow-up-automation
  - tool-sync-workflow
  - ab-test-orchestrator
---

# Outbound Founder-Led Email — Scalable Automation

> **Stage:** Marketing > SolutionAware | **Motion:** OutboundFounderLed | **Channels:** Email

## Outcomes

Scale from 100 contacts (Baseline) to 500-1,000 emails per week while keeping the meeting rate within 80% of the Baseline result. The key constraint: the founder's time must NOT scale linearly with volume. At Baseline the founder spent ~14 hours over 2 weeks for 100 contacts. At Scalable, the founder should spend no more than 2 hours per week despite 5-10x the volume. Automation handles list building, sending, reply routing, and reporting. The founder only handles final reply conversations and meeting prep.

Pass: Meeting rate ≥ 1.6% (80% of the 2% Baseline target) sustained over 2 months at 500+ emails/week, with the founder spending ≤ 2 hours/week on this play.
Fail: Meeting rate drops below 1.6% for 2 consecutive weeks, or the founder spends more than 4 hours/week.

## Leading Indicators

- Domain health scores stay above 90% across all sending accounts (deliverability is holding at volume)
- Positive reply rate stays ≥ 4% as volume increases (messaging quality is not degrading)
- A/B test winner selection produces measurable lift (optimization is working)
- Weekly list refresh produces ≥ 100 new scored prospects without manual intervention
- Cost per meeting stays below $150

## Instructions

### 1. Expand sending infrastructure

Add 2 more secondary domains (total: 4 domains, 8 sending accounts). Use the `instantly-account-setup` fundamental. Start warmup immediately via the `instantly-warmup` fundamental.

Calculate capacity: 8 accounts x 30 sends/day x 5 days/week = 1,200 emails/week max. Target 500-800/week to leave headroom for domain rotation if any account's health drops.

Configure Instantly to auto-rotate across all accounts evenly. If an account's warmup score drops below 85%, pause sending from it (keep warmup active) and redistribute volume to healthy accounts.

### 2. Automate weekly list building

Run the `build-prospect-list` drill, but configure it as a recurring workflow in n8n:

- **Weekly trigger (every Monday):** n8n workflow pulls new prospects from Apollo matching your ICP filters
- **Enrichment:** Route new prospects through Clay using the `enrich-and-score` drill fundamentals. Verify emails, enrich firmographics, score against ICP, add `likely_alternative` and `personalization_line` variables.
- **Deduplication:** Before pushing to Attio, check against existing contacts to avoid re-emailing anyone already in your pipeline, already a customer, or already contacted within the last 90 days.
- **Push to Instantly:** Qualified prospects (score ≥ 70, email verified) are pushed directly to the active Instantly campaign via the `tool-sync-workflow` drill.

Target: 150-200 new qualified contacts added to the pipeline every week without manual intervention.

### 3. Segment campaigns by ICP variant

At Baseline you ran one campaign to one ICP segment. At Scalable, split into 2-3 ICP segments based on what you learned from Baseline meetings:

- **Segment by likely alternative:** Prospects using Competitor A get different proof points than prospects using spreadsheets. Create separate Instantly campaigns per alternative, each with tailored Email 1 personalization and Email 2 proof points.
- **Segment by company size or stage:** Series A companies have different urgency than Series C. Adjust the tone — earlier-stage companies respond to speed/scrappiness, later-stage to risk reduction.

Run the the founder cold email copy workflow (see instructions below) drill once per segment to produce tailored 3-step sequences.

### 4. Build automated reply routing

Run the `follow-up-automation` drill to create n8n workflows that handle Instantly replies automatically:

- **Positive reply detected:** n8n receives Instantly webhook, AI classifies sentiment (use Claude API or Instantly's built-in classifier), creates a deal in Attio at "Meeting Requested" stage, sends Slack notification to the founder with the reply text, and removes the contact from all other active sequences.
- **"Not now" reply detected:** Log in Attio with status "Nurture", set a 60-day follow-up reminder, remove from active sequences.
- **Negative reply or unsubscribe:** Add to Instantly global suppression list, update Attio status to "Do Not Contact."
- **Out of office:** Pause the sequence for that contact, resume 3 days after the OOO end date (if detectable), otherwise resume after 7 days.

This means the founder only sees positive replies in Slack and responds directly. No manual triage.

### 5. Launch A/B testing

Run the `ab-test-orchestrator` drill. At Scalable volume, you have enough sends to test one variable at a time:

**Test 1 (Weeks 1-2): Subject line.** Test the Email 1 subject line. Variant A: question format ("Quick question about [company's] [process]"). Variant B: direct format ("[Founder first name] from [your company] — re: [likely_alternative]"). Split 50/50 across 200+ sends per variant. Measure by positive reply rate.

**Test 2 (Weeks 3-4): Proof point.** Test Email 2's customer story. Variant A: metric-focused ("cut pipeline review from 3 hours to 20 minutes"). Variant B: outcome-focused ("closed 40% more deals in Q1"). Split 50/50. Measure by reply rate on Email 2 specifically.

**Test 3 (Weeks 5-6): Send timing.** Test morning (7:30-9:30am) vs. lunch (11:30am-1pm) sends. Measure by positive reply rate.

**Test 4 (Weeks 7-8): Sequence length.** Test 3-step vs. 2-step (drop Email 2). Measure by meeting rate.

Apply winners after each test. Document every test result in PostHog with the `posthog-custom-events` fundamental.

### 6. Build weekly performance reporting

Run the `tool-sync-workflow` drill to ensure all data flows into PostHog. Build a weekly automated report (n8n workflow, runs every Friday):

- Total emails sent this week (by segment)
- Positive reply rate (by segment)
- Meeting rate (by segment)
- Cost per meeting (Instantly + Clay + domain costs / meetings booked)
- Domain health scores (from Instantly API)
- Active A/B test status and interim results
- Comparison to Baseline rates

Route the report to the founder via Slack or email. Include a one-line recommendation: "Continue as-is", "Segment X underperforming — consider pausing", or "Test Y has a winner — apply it."

### 7. Monitor and maintain for 2 months

Run the system for 8 weeks. The agent's weekly checklist:
1. Review the Friday performance report
2. Check all n8n workflows executed without errors
3. Verify weekly list refresh produced ≥ 100 new prospects
4. Confirm no domain health scores dropped below 85%
5. Apply A/B test winners when tests conclude
6. Flag any metric that dropped 20%+ from the prior week

**Human action required:** The founder responds to positive replies (Slack notifications) and takes meetings. Target: ≤ 2 hours/week on this play.

### 8. Evaluate after 2 months

Compute over the full 2-month period:
- Average weekly meeting rate
- Total meetings booked
- Cost per meeting
- Founder hours per week on this play

- **PASS (≥ 1.6% meeting rate, ≤ 2 hours/week founder time):** Scalable is proven. Document: winning variants from A/B tests, best-performing ICP segments, optimal send time, and cost per meeting. Proceed to Durable.
- **MARGINAL (1.2-1.59% meeting rate):** Volume may be diluting quality. Try: tighten ICP scoring threshold to 80+, reduce volume to the best-performing segment only, or strengthen proof points with data from Scalable meetings.
- **FAIL (< 1.2% meeting rate OR > 4 hours/week founder time):** The play does not scale. Diagnose: Is the messaging degrading at volume (personalization too thin)? Is the list quality declining (scraping deeper into lower-fit prospects)? Is the founder bottleneck on replies? Fix the root cause or accept that this play works best at Baseline volume and redirect Scalable budget to a different motion.

## Time Estimate

- Sending infrastructure expansion: 3 hours (Week 1)
- n8n automated list building workflow: 6 hours (Week 1)
- Campaign segmentation and copywriting: 4 hours (Week 2)
- Reply routing automation: 5 hours (Week 2)
- A/B test setup: 4 hours (Week 2)
- Weekly performance reporting setup: 3 hours (Week 2)
- Ongoing weekly monitoring: 2 hours/week x 8 weeks = 16 hours
- Founder reply time: 2 hours/week x 8 weeks = 16 hours
- Final evaluation: 3 hours
- Setup subtotal: 25 hours, Ongoing subtotal: 35 hours, Total: ~60-70 hours over 2 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Email sequencing, warmup, A/B testing, reply detection | Hypergrowth plan $97/mo ([instantly.ai/pricing](https://instantly.ai/pricing)) |
| Clay | Enrichment, personalization, email verification, weekly list refresh | Launch plan $185/mo or Growth plan $495/mo if >2,500 credits/mo ([clay.com/pricing](https://clay.com/pricing)) |
| Attio | CRM, deal tracking, reply logging | Free for up to 3 users, Plus $29/user/mo if team grows ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Event tracking, funnel analysis, A/B test measurement | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Reply routing, list building automation, weekly reports | Starter $24/mo or self-host free ([n8n.io/pricing](https://n8n.io/pricing)) |
| Cal.com | Meeting booking link | Free plan ([cal.com/pricing](https://cal.com/pricing)) |
| Secondary domains (x4) | Sending infrastructure | ~$50/year total |
| Google Workspace (x4) | Sending accounts | ~$28/mo total ($7/user/mo) |

**Estimated monthly cost for Scalable:** ~$350-650/mo depending on Clay plan + ~$50/year for domains

## Drills Referenced

- `build-prospect-list` — automated weekly list sourcing from Apollo/Clay
- `enrich-and-score` — enrichment waterfall, email verification, ICP scoring
- the founder cold email copy workflow (see instructions below) — segment-specific email sequences in the founder's voice
- `cold-email-sequence` — campaign setup and configuration in Instantly
- `follow-up-automation` — n8n workflows for automated reply routing and classification
- `tool-sync-workflow` — connect Instantly, Attio, Clay, and PostHog into a unified data pipeline
- `ab-test-orchestrator` — structured A/B tests on subject lines, proof points, timing, and sequence length
