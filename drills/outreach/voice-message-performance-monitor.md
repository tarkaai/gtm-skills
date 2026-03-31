---
name: voice-message-performance-monitor
description: Track voice message delivery, response, and conversion metrics across phone and LinkedIn channels with automated reporting
category: Outreach
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - posthog-anomaly-detection
  - posthog-funnels
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
---

# Voice Message Performance Monitor

This drill builds the monitoring and reporting layer for the outbound voice messages play. It tracks per-channel metrics (ringless voicemail vs LinkedIn voice note), cross-channel attribution, and generates automated weekly briefs. At Durable level, this feeds directly into the `autonomous-optimization` drill.

## Prerequisites

- PostHog tracking configured with voice message events (from `voice-message-delivery` drill)
- Attio with contacts and deals tracking voice outreach activity
- n8n instance running
- At least 1 week of voice message delivery data

## Steps

### 1. Define the voice message event taxonomy

Using the `posthog-custom-events` fundamental, verify these events are firing:

**Phone voicemail events:**
- `vm_phone_generated` -- properties: campaign_id, prospect_tier, script_variant, audio_duration
- `vm_phone_delivered` -- properties: campaign_id, delivery_time, caller_id, prospect_timezone
- `vm_phone_failed` -- properties: campaign_id, failure_reason (carrier_block, invalid_number, landline)
- `vm_phone_callback` -- properties: campaign_id, time_to_callback_hours, prospect_tier

**LinkedIn voice note events:**
- `vm_linkedin_sent` -- properties: campaign_id, prospect_tier, script_variant, audio_duration
- `vm_linkedin_listened` -- properties: campaign_id, listen_duration_pct, prospect_tier
- `vm_linkedin_replied` -- properties: campaign_id, sentiment (positive/neutral/negative), reply_type

**Follow-up email events:**
- `vm_followup_email_sent` -- properties: campaign_id, channel_referenced (phone/linkedin), subject_variant
- `vm_followup_email_opened` -- properties: campaign_id, open_count
- `vm_followup_email_replied` -- properties: campaign_id, sentiment

**Conversion events:**
- `vm_meeting_booked` -- properties: campaign_id, source_channel (phone_callback/linkedin_reply/email_reply), prospect_tier, first_touch_channel
- `vm_deal_created` -- properties: campaign_id, source_channel, deal_value, prospect_tier

### 2. Build the voice message dashboard

Using the `posthog-dashboards` fundamental, create a dashboard named "Outbound Voice Messages -- Performance" with these panels:

**Row 1 -- Volume & Delivery:**
- Weekly voice messages sent by channel (stacked bar: phone VM, LinkedIn voice note)
- Delivery success rate by channel (phone delivery rate, LinkedIn send success rate)
- Daily send volume heatmap (day of week x time of day)

**Row 2 -- Response Funnels:**
- Phone funnel: vm_delivered -> callback_received -> meeting_booked
- LinkedIn funnel: voice_note_sent -> listened -> replied -> meeting_booked
- Email follow-up funnel: followup_sent -> opened -> replied -> meeting_booked

**Row 3 -- Cross-Channel Performance:**
- Response rate by channel (callback rate for phone, reply rate for LinkedIn)
- Response rate by script variant (which scripts get the most callbacks/replies)
- Time to response distribution (hours from delivery to callback/reply)

**Row 4 -- Meeting Attribution:**
- Meetings by originating voice channel (phone callback vs LinkedIn reply vs email reply)
- Meetings by prospect tier
- Average touches to meeting (voice messages + follow-up emails before conversion)

**Row 5 -- Health Metrics:**
- Phone VM delivery rate trended weekly (target: >75%)
- LinkedIn voice note send success rate trended weekly
- Negative reply rate across channels (guardrail: <3%)
- Cost per meeting by channel

Add threshold indicators: response rate targets from each play level.

### 3. Configure anomaly detection

Using the `posthog-anomaly-detection` fundamental, set alerts for:

- Phone callback rate drops below 2% for 5 consecutive business days
- LinkedIn voice note reply rate drops below 5% for 1 week
- Phone VM delivery rate drops below 60% (carrier blocking issue)
- Meeting volume drops to zero for 5 consecutive business days
- Negative reply rate exceeds 3% on any channel
- Follow-up email bounce rate exceeds 3%

Route all alerts to Slack and log in Attio as campaign notes.

### 4. Build the weekly voice message brief

Create an n8n workflow using `n8n-scheduling` set to run every Monday at 8am:

1. Pull last 7 days of voice message events from PostHog API
2. Pull Attio deal data for pipeline created from voice outreach using `attio-reporting`
3. Calculate per-channel metrics:
   - Phone: VMs delivered, callbacks received, callback rate, avg time to callback
   - LinkedIn: voice notes sent, listened rate, reply rate, sentiment breakdown
   - Email follow-up: sent, opened, replied, contribution to meetings
4. Calculate cross-channel metrics:
   - Which channel combination produces the most meetings
   - Best day/time for delivery by channel
   - Top-performing script variants
5. Compare this week vs 4-week rolling average for each metric
6. Generate the weekly brief:
   - Channel-by-channel metrics summary with week-over-week delta
   - Top-performing prospect segments (by tier, industry, signal type)
   - Best-performing voice scripts with response rates
   - Script fatigue alert: flag any variant with declining response over 3 weeks
   - Specific action items for next week
7. Post to Slack and store in Attio

### 5. Build the script performance tracker

Voice message scripts decay faster than email copy because prospects in the same industry talk to each other. Track per-script metrics:

- Create a PostHog insight grouping all events by `script_variant`
- Track: sends, responses, response rate, meetings, meeting rate
- Flag scripts where response rate has declined >30% from their first 2 weeks
- Recommend script retirement when response rate drops below 50% of its peak

This data feeds into the `autonomous-optimization` drill for automated script variant testing.

### 6. Feed data to optimization loop

Ensure all metrics, anomalies, and weekly summaries are stored as structured PostHog events so the `autonomous-optimization` drill can consume them. Each weekly brief fires a `vm_weekly_summary` event with properties containing all computed metrics. This creates the data foundation for automated hypothesis generation and experiment design at Durable level.

## Output

- Live PostHog dashboard with real-time voice message metrics across both channels
- Weekly automated briefs with per-channel performance and script analysis
- Anomaly alerts that catch degradation before it compounds
- Script performance tracking with decay detection
- Structured data feed for the autonomous optimization loop

## Triggers

Weekly briefs fire every Monday via n8n cron. Dashboard refreshes with live data. Anomaly alerts check daily. Script performance tracker updates with each new batch of delivery data.
