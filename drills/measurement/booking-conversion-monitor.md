---
name: booking-conversion-monitor
description: Continuously monitor calendar booking funnel conversion rates and detect degradation across embed surfaces
category: Measurement
tools:
  - PostHog
  - n8n
  - Cal.com
  - Attio
fundamentals:
  - posthog-funnels
  - posthog-anomaly-detection
  - posthog-custom-events
  - n8n-triggers
  - n8n-scheduling
  - calcom-crm-sync
---

# Booking Conversion Monitor

This drill creates an always-on monitoring system for calendar booking funnels. It tracks every stage of the booking flow -- from CTA impression through widget load, time-slot selection, to confirmed booking -- and fires alerts when any stage degrades.

Designed for plays that use inline calendar embeds as the primary conversion surface (e.g., `calendar-flow-support`).

## Input

- PostHog events flowing from all booking surfaces (pages with Cal.com inline embeds)
- Cal.com webhook data flowing to n8n via `calcom-crm-sync`
- At least 2 weeks of baseline data to establish normal conversion rates

## Steps

### 1. Define the booking funnel stages

Using `posthog-custom-events`, ensure these events are captured across all booking surfaces:

| Event | Trigger | Key Properties |
|-------|---------|----------------|
| `cta_impression` | CTA element enters viewport | `page`, `cta_variant`, `source` |
| `cta_clicked` | Prospect clicks CTA that reveals calendar | `page`, `cta_variant`, `source` |
| `calendar_widget_loaded` | Cal.com embed fires `linkReady` | `page`, `event_type` |
| `timeslot_selected` | Prospect clicks a time slot | `page`, `event_type`, `day_of_week`, `time_of_day` |
| `booking_form_submitted` | Prospect submits booking form | `page`, `event_type`, `source` |
| `meeting_booked` | Cal.com webhook confirms booking | `event_type`, `source`, `lead_email`, `utm_source` |
| `meeting_attended` | Meeting marked as completed in CRM | `event_type`, `source`, `deal_stage` |

### 2. Build the funnel in PostHog

Using `posthog-funnels`, create a saved funnel:

`cta_impression` -> `cta_clicked` -> `calendar_widget_loaded` -> `timeslot_selected` -> `meeting_booked`

Break down by:
- `page` (which pages convert best)
- `cta_variant` (which CTA copy/placement converts best)
- `utm_source` (which traffic sources convert best)
- `device_type` (desktop vs mobile -- inline embeds often underperform on mobile)

Save as: "Calendar Booking Funnel - All Surfaces"

### 3. Establish baseline conversion rates

After 2+ weeks of data, record baseline rates for each funnel step:
- CTA click-through rate: `cta_clicked / cta_impression`
- Widget load rate: `calendar_widget_loaded / cta_clicked` (should be ~95%+; low rate = embed broken)
- Slot selection rate: `timeslot_selected / calendar_widget_loaded` (measures availability attractiveness)
- Booking completion rate: `meeting_booked / timeslot_selected` (measures form friction)
- Overall funnel rate: `meeting_booked / cta_impression`
- Show rate: `meeting_attended / meeting_booked`

Store baseline values as PostHog annotations or in Attio as a campaign record note.

### 4. Build n8n monitoring workflows

Using `n8n-scheduling`, create a daily cron workflow that:

1. Queries PostHog for the last 7 days of funnel data via the PostHog API
2. Computes each conversion rate
3. Compares to baseline using `posthog-anomaly-detection` logic:
   - **Normal:** within +/- 15% of baseline
   - **Warning:** 15-30% below baseline for 3+ consecutive days
   - **Critical:** >30% below baseline for 2+ consecutive days OR widget load rate drops below 90% (indicates broken embed)
4. For Warning/Critical: sends alert to Slack with specific degradation data and probable cause

Using `n8n-triggers`, create event-triggered workflows:
- Cal.com booking webhook -> update Attio deal -> fire PostHog `meeting_booked` event
- PostHog webhook for `meeting_booked` -> calculate time-from-first-touch for the contact -> log to Attio

### 5. Build per-surface breakdown reporting

Create a weekly n8n workflow that:

1. Pulls booking funnel data broken down by `page` property
2. Ranks pages by overall conversion rate and by total bookings
3. Identifies:
   - Top 3 highest-converting surfaces (double down)
   - Bottom 3 surfaces (diagnose or remove calendar embed)
   - Any surface where widget load rate < 95% (technical issue)
   - Any surface where mobile conversion is < 50% of desktop conversion (UX issue)
4. Outputs a ranked surface report for the weekly optimization brief

### 6. Track booking timing patterns

Build a PostHog insight that groups `timeslot_selected` events by `day_of_week` and `time_of_day`. This reveals:
- Which days/times prospects prefer to book (optimize availability windows)
- Whether certain time slots never get selected (remove them to simplify the widget)
- Peak booking hours (ensure the embed loads fast during these windows)

## Output

- Real-time booking funnel with per-surface breakdown
- Daily automated monitoring with anomaly alerts
- Weekly surface performance ranking
- Booking timing heatmap for availability optimization
- Historical baseline tracking for long-term trend analysis

## Triggers

- Daily monitoring: runs every day at 9 AM via n8n cron
- Weekly surface report: runs every Monday at 8 AM via n8n cron
- Event-triggered: fires on every Cal.com booking webhook
