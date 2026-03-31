---
name: outbound-voice-messages-scalable
description: >
  Outbound Voice Messages -- Scalable Automation. Fully automated voice message
  pipeline generating and delivering 500+ personalized messages per month via
  AI voice cloning, ringless voicemail, and LinkedIn voice notes with A/B testing
  across scripts, timing, and channel mix.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Direct, Social"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: ">=5% response rate at 500+ voice messages/month sustained over 3 months"
kpis: ["Monthly volume", "Response rate by channel", "Cost per meeting", "Script variant win rate", "Automation uptime"]
slug: "outbound-voice-messages"
install: "npx gtm-skills add marketing/solution-aware/outbound-voice-messages"
drills:
  - voice-message-delivery
  - voice-message-performance-monitor
  - ab-test-orchestrator
  - follow-up-automation
---

# Outbound Voice Messages -- Scalable Automation

> **Stage:** Marketing > Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Direct, Social

## Outcomes

Scale voice message outreach to 500+ messages per month while maintaining response rates at or above Baseline levels. The entire pipeline -- prospect enrichment, script generation, AI voice synthesis, multi-channel delivery, follow-up emails, and response routing -- runs as an automated n8n workflow with human oversight. A/B testing identifies winning scripts, delivery windows, and channel allocations.

## Leading Indicators

- Automated pipeline processes 25+ prospects per day without manual intervention
- AI voice generation batch completes in under 10 minutes for 50 messages
- Ringless voicemail delivery rate holds above 75% at increased volume
- LinkedIn voice note daily volume stays within safety limits (20-25/day per account)
- No LinkedIn account restrictions for 30+ consecutive days
- Script A/B tests produce a statistically significant winner within 2 weeks (100+ sends per variant)
- Cost per meeting stays below $100

## Instructions

### 1. Build the automated prospect pipeline

Create an n8n workflow that runs daily:

1. **Source trigger**: Pull new prospects matching ICP criteria from Apollo or Clay. Target 25-30 new prospects per day.
2. **Enrichment**: Run Clay enrichment waterfall to fill phone numbers, LinkedIn URLs, company signals, and trigger events.
3. **Scoring**: Apply lead scoring formula. Filter to prospects above score threshold (calibrated from Baseline data).
4. **Script assignment**: Randomly assign each prospect to a script variant for A/B testing. Store the assignment in Attio.
5. **Voice generation**: Call ElevenLabs API with the personalized script. Save audio files to cloud storage. Map audio URL to prospect record.
6. **Quality gate**: Run an automated check on audio duration (reject if under 15 sec or over 45 sec) and file size (reject if corrupted/empty). Queue rejected messages for manual review.
7. **Delivery queue**: Push prospect + audio to the delivery queue for next-day execution.

The workflow fires every morning at 6am. By 7am, today's delivery batch is queued and ready.

### 2. Scale delivery across channels

Run the `voice-message-delivery` drill at scale:

**Phone voicemail pipeline:**
- n8n triggers VoiceDrop.ai batch delivery at 9am in each prospect's timezone
- 15-20 ringless VMs per day, 5 days per week = 75-100/week
- Rotate through 3-4 local caller IDs to avoid carrier flagging
- Automatically retry failed deliveries once on a different day/time

**LinkedIn voice note pipeline:**
- lemlist or Expandi processes LinkedIn voice notes at 10am
- 15-20 LinkedIn voice notes per day, 5 days per week = 75-100/week
- If using multiple LinkedIn accounts (via HeyReach), distribute evenly across accounts
- Auto-pause any account that receives a LinkedIn warning

**Follow-up email pipeline:**
Run the `follow-up-automation` drill to configure Instantly:
- Automated follow-up email fires 2 hours after each voice message delivery
- Second follow-up email 3 days later for non-responders: "Did you get a chance to listen to the voicemail I left?"
- Breakup email at Day 7: "Last note from me -- the voicemail I left covers it, but happy to chat if {pain_point} becomes a priority."

**Cross-channel coordination:**
- n8n checks Attio before each delivery: if the prospect has responded on any channel, cancel all pending touches
- If a prospect receives both phone VM and LinkedIn voice note, space them 3+ days apart
- If a prospect replies negatively on one channel, stop all channels immediately

### 3. Launch A/B testing on scripts and timing

Run the `ab-test-orchestrator` drill:

**Script variant testing:**
- Run 3-4 script variants simultaneously, randomly assigned to prospects
- Each variant must reach 100+ sends before evaluation
- Track: response rate, callback rate, meeting conversion rate per variant
- Declare a winner when one variant leads by >2 percentage points with >90% confidence
- Replace the losing variant with a new challenger and continue testing

**Delivery timing testing:**
- Test morning (9-11am) vs midday (12-2pm) delivery windows for ringless voicemail
- Test day-of-week: Tuesday vs Wednesday vs Thursday
- Track callback rate by delivery window

**Channel mix testing:**
- Compare response rates: phone VM only, LinkedIn voice note only, both channels
- For prospects with both phone + LinkedIn: test phone-first vs LinkedIn-first sequencing
- Measure incremental value of adding the second channel

Use PostHog feature flags to randomly assign prospects to test groups.

### 4. Set up performance monitoring

Run the `voice-message-performance-monitor` drill to build:

- Live PostHog dashboard tracking daily volume, delivery rates, response rates, and meeting conversions
- Weekly automated briefs comparing channel performance, script variants, and delivery timing
- Anomaly alerts: response rate drop >20% from 4-week average, delivery rate drop below 60%, negative reply rate above 3%
- Script decay tracking: flag variants with response rates declining for 3+ consecutive weeks

### 5. Optimize based on data

Monthly optimization cycle:
1. Review the weekly briefs for the month. Identify the top-performing script, channel, and timing.
2. Retire scripts that have decayed below 50% of their peak response rate.
3. Write 1-2 new script variants informed by the scripts that worked and the objections heard in callbacks.
4. Adjust channel allocation: shift volume toward the channel with the lower cost per meeting.
5. Update ICP targeting: add segments where response rates are highest, remove segments where response rates are consistently below 2%.

### 6. Monitor guardrails

Set up n8n alerts for:
- **Volume guardrails**: Never exceed 25 ringless VMs/day or 25 LinkedIn voice notes/day per account
- **Budget guardrail**: Monthly tool spend stays within 120% of allocated budget
- **Quality guardrail**: If negative reply rate exceeds 3%, auto-pause for 48 hours
- **LinkedIn safety**: If any LinkedIn account receives a restriction, pause that account for 7 days and redistribute volume
- **Delivery health**: If phone VM delivery rate drops below 60% for 3 days, switch to a different caller ID or investigate carrier blocking

### 7. Evaluate against threshold

At the end of each month, run the `threshold-engine` drill. Measure against: **>=5% response rate at 500+ voice messages/month sustained over 3 months**.

Calculate:
- Monthly response rate by channel
- Cost per meeting by channel
- A/B test win rate (how many experiments produced a statistically significant winner)
- Automation uptime: % of business days where the pipeline ran without manual intervention
- Total pipeline value generated from voice message outreach

- **PASS** (3 consecutive months at or above threshold): Proceed to Durable.
- **FAIL**: Identify the bottleneck. If volume is the issue, add LinkedIn accounts or caller IDs. If response rate is the issue, focus on script quality and prospect targeting. If cost is the issue, optimize channel mix toward the cheaper converting channel.

## Time Estimate

- Month 1 -- Pipeline build and launch: 30 hours
  - n8n automated pipeline: 8 hours
  - VoiceDrop.ai + lemlist campaign scaling: 6 hours
  - PostHog dashboard and monitoring: 5 hours
  - A/B test setup: 4 hours
  - Daily monitoring and tuning: 7 hours (30 min/day)
- Month 2 -- Optimization: 22 hours
  - Script variant creation and testing: 4 hours
  - Channel mix optimization: 3 hours
  - A/B test evaluation and iteration: 4 hours
  - Daily monitoring: 7 hours
  - Pipeline maintenance: 4 hours
- Month 3 -- Steady state: 23 hours
  - Continued A/B testing: 4 hours
  - Monthly deep analysis: 3 hours
  - Pipeline maintenance and scaling: 5 hours
  - Daily monitoring: 7 hours
  - Threshold evaluation and documentation: 4 hours

Total: ~75 hours over 3 months.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| ElevenLabs | AI voice generation at scale | Pro: $99/mo for 500K chars (~1,250 messages) (https://elevenlabs.io/pricing) |
| VoiceDrop.ai | Ringless voicemail delivery | Growth: $495/mo for ~2,500 VMs (https://www.voicedrop.ai/pricing) |
| lemlist | LinkedIn voice note automation | Multichannel Expert: $99/user/mo (https://www.lemlist.com/pricing) |
| Clay | Enrichment and automated script generation | Pro: $149/mo (https://www.clay.com/pricing) |
| Instantly | Follow-up email sequences | Growth: $30/mo (https://instantly.ai/pricing) |
| Attio | CRM for full pipeline tracking | Plus: $29/user/mo (https://attio.com/pricing) |
| PostHog | Dashboards, funnels, A/B tests | Free tier covers this volume (https://posthog.com/pricing) |
| n8n | Pipeline orchestration | Self-hosted: free; Cloud: $20/mo (https://n8n.io/pricing) |

**Estimated play-specific cost: ~$700-900/mo** (ElevenLabs Pro + VoiceDrop Growth + lemlist + Clay + Instantly)

## Drills Referenced

- `voice-message-delivery` -- automated multi-channel delivery pipeline (phone VM + LinkedIn voice notes + follow-up emails)
- `voice-message-performance-monitor` -- dashboards, weekly briefs, anomaly alerts, and script decay tracking
- `ab-test-orchestrator` -- A/B testing across scripts, delivery timing, and channel mix
- `follow-up-automation` -- automated follow-up email sequences coordinated with voice delivery
