---
name: cold-dm-linkedin-twitter-scalable
description: >
  Cold DMs on LinkedIn/Twitter — Scalable Automation. Automate the engagement-to-DM pipeline
  with n8n workflows, LinkedIn automation tools, and PhantomBuster. A/B test message variants
  at volume. Target 500+ DMs/mo at >=1.5% meeting rate.
stage: "Marketing > ProblemAware"
motion: "OutboundFounderLed"
channels: "Social"
level: "Scalable Automation"
time: "40 hours over 2 months"
outcome: ">=1.5% meeting rate from >=500 DMs/mo sustained for 2 months"
kpis: ["Reply rate by channel", "Meeting rate", "DMs sent per month", "Cost per meeting", "A/B test win rate"]
slug: "cold-dm-linkedin-twitter"
install: "npx gtm-skills add marketing/problem-aware/cold-dm-linkedin-twitter"
drills:
  - follow-up-automation
  - tool-sync-workflow
  - ab-test-orchestrator
  - signal-detection
---

# Cold DMs on LinkedIn/Twitter — Scalable Automation

> **Stage:** Marketing > ProblemAware | **Motion:** OutboundFounderLed | **Channels:** Social

## Outcomes

Automate the cold DM pipeline to send 500+ DMs per month across LinkedIn and X without proportional time increase. Run systematic A/B tests on message copy, send timing, engagement duration, and ICP segments. Maintain >=1.5% meeting rate (>=7-8 meetings/mo) at scale.

**Pass threshold:** >=1.5% meeting rate from >=500 DMs/mo sustained for 2 consecutive months.

## Leading Indicators

- Automation uptime: >=95% (n8n workflows executing without errors)
- Prospect pipeline depth: >=300 prospects in engagement warm-up queue at any time
- A/B test velocity: >=2 completed experiments per month
- Reply rate stability: within +/-3pp of Baseline level despite higher volume
- Cost per meeting: <$100 (tool costs / meetings booked)

## Instructions

### 1. Automate LinkedIn outreach with Dripify or Expandi

Set up a LinkedIn automation tool to handle the engagement-to-DM pipeline at scale.

**Dripify setup (recommended for simplicity):**
1. Create a Dripify account ($39/mo annual, $59/mo monthly per user).
2. Connect your LinkedIn account.
3. Build a campaign sequence:
   - Step 1: View profile (Day 0)
   - Step 2: Like 2 recent posts (Day 1)
   - Step 3: Send connection request with note (Day 3)
   - Step 4: Wait for acceptance (up to 14 days)
   - Step 5: Send DM Message 1 (Day 1 after accept)
   - Step 6: Wait 5 days, check for reply
   - Step 7: If no reply, send DM Message 2 (Day 6 after accept)
   - Step 8: Wait 5 days
   - Step 9: If no reply, send DM Message 3 with CTA (Day 11 after accept)
4. Set daily limits: 20 connection requests/day, 50 messages/day.
5. Upload prospect lists from Clay CSV. Tag each batch with the ICP segment.

**Expandi alternative ($99/mo):**
Same sequence logic but uses dedicated IP per account and supports conditional branching (e.g., if prospect liked your post, skip to DM immediately).

**Daily limits to respect:**
- Connection requests: 20-25/day
- Messages: 50-75/day
- Profile views: 80-100/day

### 2. Automate X outreach with PhantomBuster + n8n

Build an automated X engagement-and-DM pipeline:

1. **PhantomBuster Twitter Auto Liker** ($56/mo Starter):
   - Upload a Google Sheet of target X profile URLs.
   - Configure: like 2-3 most recent posts per profile.
   - Schedule: 10 profiles per launch, 5 launches per day = 50 prospects/day engaged.

2. **n8n workflow for DM scheduling:**
   - Trigger: 5 days after a prospect enters the engagement queue (tracked in Attio).
   - Action: Call `twitter-x-dms` fundamental to send the DM via X API, or trigger PhantomBuster Twitter Message Sender.
   - Log the DM in Attio and fire `dm_sent` event to PostHog.

3. **n8n workflow for reply detection:**
   - Trigger: Poll X API every 30 minutes for new DM events (`GET /2/dm_events`).
   - Action: Classify reply sentiment (positive/neutral/negative) using Claude API.
   - Positive: Create deal in Attio, notify founder via Slack.
   - Negative: Tag prospect in Attio as "x-not-interested", remove from sequence.

### 3. Build automated follow-up workflows

Run the `follow-up-automation` drill. Configure n8n workflows for cross-channel follow-ups:

- **LinkedIn accepted, no DM reply after 10 days**: Send a different-angle follow-up DM on LinkedIn.
- **X DM sent, no reply after 7 days**: If prospect has a LinkedIn profile, send a LinkedIn connection request referencing the X interaction.
- **Positive reply on either channel**: Auto-create Attio deal, send founder a Slack alert with prospect context, and offer cal.com scheduling link.
- **Meeting booked, no-show**: Trigger a reschedule DM 2 hours after missed meeting.

Safety guardrails:
- Maximum 3 total DMs per prospect across both channels before moving to nurture list.
- Never send DMs on both platforms to the same prospect in the same week.
- Suppress prospects who replied negatively on any channel.

### 4. Connect your tool stack

Run the `tool-sync-workflow` drill. Build n8n sync workflows:

- **Clay > Attio**: New enriched prospects push to Attio automatically.
- **Dripify/Expandi > Attio**: LinkedIn activity syncs to contact records (connection status, message sent, reply received).
- **PhantomBuster > Attio**: X engagement and DM activity syncs to contact records.
- **PostHog > Attio**: Product usage events update contact properties (if prospect visits your site after DM).
- **Attio > PostHog**: Deal stage changes fire PostHog events for funnel analysis.

### 5. Launch A/B testing

Run the `ab-test-orchestrator` drill. Set up systematic experiments:

**Month 1 experiments:**
- **Test 1: LinkedIn message length.** Variant A: 3-message sequence (current). Variant B: 2-message sequence (skip the value-add, go directly to CTA). Measure: meeting rate. Minimum 100 per variant.
- **Test 2: X DM timing.** Variant A: DM after 5-day engagement warm-up. Variant B: DM after 3-day warm-up. Measure: reply rate. Minimum 100 per variant.

**Month 2 experiments:**
- **Test 3: ICP segment comparison.** Split by job title tier (VP+ vs Director vs Manager). Measure: meeting rate per tier across both channels.
- **Test 4: Personalization depth.** Variant A: reference a specific post. Variant B: reference their company's recent news. Measure: reply rate.

Use PostHog feature flags to randomly assign prospects to variants. Run each test for minimum 2 weeks or until 100 per variant, whichever is longer. Document every test result in Attio.

### 6. Deploy signal-based prioritization

Run the `signal-detection` drill. Configure Clay to monitor for buying signals and prioritize outreach:

- **Job changes**: New hire in your buyer persona role = fast-track to DM (skip normal queue, send within 48 hours of detection).
- **Funding events**: Series A/B closed = add to top of engagement queue.
- **Competitor mentions**: Prospect tweeting about a competitor or related pain = immediate engagement.

Build an n8n workflow: Clay signal webhook > score the signal > if high-score, inject prospect into the DM pipeline at the appropriate stage > tag in Attio with signal type.

### 7. Scale volume

With automation in place, ramp to target volume:
- Month 1: 300 DMs (150 LinkedIn + 150 X). Validate automation is working correctly.
- Month 2: 500+ DMs (250+ LinkedIn + 250+ X). Full scale.

Monitor weekly: automation error rates, reply rates by channel, meeting conversion, and cost per meeting. If reply rates drop as volume increases, reduce volume and improve targeting before scaling again.

### 8. Evaluate against threshold

At the end of month 2, evaluate:
- Total DMs sent per month (target: >=500)
- Meeting rate (target: >=1.5%)
- Cost per meeting (target: <$100)
- A/B test results: how many experiments completed, which variants won

**Pass:** >=1.5% meeting rate from >=500 DMs/mo for 2 consecutive months.
**Fail:** Meeting rate <1.5% or unable to sustain 500 DMs/mo.

If PASS: the play scales. Document the winning configurations and proceed to Durable.
If FAIL: diagnose. Volume bottleneck = list exhaustion (expand ICP or add new sources). Rate bottleneck = message fatigue (rotate variants faster) or targeting drift (re-validate ICP).

## Time Estimate

- Automation setup (Dripify/Expandi + PhantomBuster + n8n): 8 hours
- Tool sync configuration: 4 hours
- A/B test design and setup: 4 hours
- Signal detection configuration: 3 hours
- Weekly monitoring and optimization (2 hr/week x 8 weeks): 16 hours
- Monthly review and experiment analysis (2.5 hr x 2): 5 hours
- **Total: ~40 hours over 2 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn Sales Navigator | Advanced search, InMail credits | $119.99/mo ([pricing](https://business.linkedin.com/sales-solutions/compare-plans)) |
| Dripify | LinkedIn automation (connection + message sequences) | $39-59/mo per user ([pricing](https://dripify.io/pricing)) |
| PhantomBuster | X engagement automation + DM sending | $56/mo Starter ([pricing](https://phantombuster.com/pricing)) |
| X API | DM sending and reply detection via API | $200/mo Basic ([pricing](https://developer.x.com/en/products)) |
| Clay | Prospect enrichment + signal detection | $149/mo Explorer ([pricing](https://www.clay.com/pricing)) |
| Attio | CRM, deal tracking, reporting | Free tier up to 3 users ([pricing](https://attio.com/pricing)) |
| PostHog | Event tracking, experiments, feature flags | Free tier: 1M events/mo ([pricing](https://posthog.com/pricing)) |
| n8n | Workflow automation (syncs, follow-ups, alerts) | Free self-hosted / $20/mo cloud ([pricing](https://n8n.io/pricing)) |

**Total play-specific cost: ~$585-785/mo** (LinkedIn + Dripify + PhantomBuster + X API + Clay are the primary costs)

## Drills Referenced

- `follow-up-automation` -- automated cross-channel follow-up workflows in n8n
- `tool-sync-workflow` -- keep Clay, Dripify, PhantomBuster, Attio, and PostHog in sync
- `ab-test-orchestrator` -- design and run A/B tests on DM copy, timing, and ICP segments
- `signal-detection` -- monitor buying signals and fast-track signal-triggered outreach
