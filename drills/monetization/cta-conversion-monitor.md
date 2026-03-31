---
name: cta-conversion-monitor
description: Continuously monitor CTA and lead capture form conversion funnels across all surfaces and detect degradation
category: Conversion
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-funnels
  - posthog-anomaly-detection
  - posthog-custom-events
  - n8n-triggers
  - n8n-scheduling
  - attio-reporting
---

# CTA Conversion Monitor

This drill creates an always-on monitoring system for lead capture surface funnels. It tracks every stage of the conversion flow -- from CTA impression through interaction to lead capture -- and fires alerts when any stage degrades. Designed for plays that use forms, inline calendars, or chat widgets as the primary conversion surface.

## Input

- PostHog events flowing from all lead capture surfaces (pages with forms, calendar embeds, or chat widgets)
- At least 2 weeks of baseline data to establish normal conversion rates
- n8n instance for scheduled monitoring workflows
- Attio CRM for logging monitoring results

## Steps

### 1. Define the lead capture funnel stages

Using `posthog-custom-events`, ensure these events are captured across all lead capture surfaces:

| Event | Trigger | Key Properties |
|-------|---------|----------------|
| `cta_impression` | CTA container enters viewport | `page`, `surface_type`, `cta_variant`, `device_type` |
| `cta_clicked` | Visitor clicks or interacts with the CTA | `page`, `surface_type`, `cta_variant`, `device_type` |
| `form_field_focused` | Visitor focuses the first form field (form surfaces) | `page`, `field`, `surface_type` |
| `calendar_widget_loaded` | Cal.com embed fires `linkReady` (calendar surfaces) | `page`, `surface_type` |
| `chat_widget_opened` | Intercom Messenger opened (chat surfaces) | `page`, `surface_type` |
| `lead_captured` | Form submitted, meeting booked, or email collected | `page`, `surface_type`, `utm_source`, `cta_variant` |

### 2. Build the funnel in PostHog

Using `posthog-funnels`, create a saved funnel per surface type:

**Form funnel:** `cta_impression` -> `cta_clicked` -> `form_field_focused` -> `lead_captured`

**Calendar funnel:** `cta_impression` -> `cta_clicked` -> `calendar_widget_loaded` -> `lead_captured`

**Chat funnel:** `cta_impression` -> `chat_widget_opened` -> `lead_captured`

Break down each funnel by:
- `page` (which pages convert best)
- `cta_variant` (which CTA copy/placement converts best)
- `utm_source` (which traffic sources convert best)
- `device_type` (desktop vs mobile)

Save as: "Lead Capture Funnel - {Surface Type} - All Pages"

### 3. Establish baseline conversion rates

After 2+ weeks of data, record baseline rates for each funnel step:
- CTA click-through rate: `cta_clicked / cta_impression`
- Engagement rate: `form_field_focused / cta_clicked` (form) or `calendar_widget_loaded / cta_clicked` (calendar) or `chat_widget_opened / cta_impression` (chat)
- Completion rate: `lead_captured / cta_clicked`
- Overall conversion rate: `lead_captured / cta_impression`

Store baseline values in Attio as a campaign record note with the date recorded.

### 4. Build n8n monitoring workflows

Using `n8n-scheduling`, create a daily cron workflow that:

1. Queries PostHog for the last 7 days of funnel data via the PostHog API
2. Computes each conversion rate per surface and per page
3. Compares to baseline using `posthog-anomaly-detection` logic:
   - **Normal:** within +/- 15% of baseline
   - **Warning:** 15-30% below baseline for 3+ consecutive days
   - **Critical:** >30% below baseline for 2+ consecutive days, OR widget/form load fails (technical break)
4. For Warning/Critical: sends alert to Slack with specific degradation data, affected page, and probable cause

Using `n8n-triggers`, create event-triggered workflows:
- Form submission webhook -> update Attio deal -> fire PostHog `lead_captured` event with attribution
- Cal.com booking webhook -> update Attio deal -> fire PostHog `lead_captured` event with attribution

### 5. Build per-page breakdown reporting

Create a weekly n8n workflow that:

1. Pulls lead capture funnel data broken down by `page` property
2. Ranks pages by overall conversion rate and by total leads captured
3. Identifies:
   - Top 3 highest-converting pages (double down, add more traffic)
   - Bottom 3 pages (diagnose: wrong surface type? bad CTA copy? wrong audience?)
   - Any page where form/widget load fails > 5% of the time (technical issue)
   - Any page where mobile conversion is < 50% of desktop conversion (UX issue)
4. Outputs a ranked page report for the weekly optimization brief

### 6. Track conversion timing and drop-off patterns

Build PostHog insights that reveal:
- **Time to convert:** median time from `cta_impression` to `lead_captured` per page. If it exceeds 3 minutes, the surface has too much friction.
- **Form abandonment:** for form surfaces, track which field causes the most drop-off. If `form_field_focused` fires for field 1 but not field 2, field 2 is the problem.
- **Device split:** conversion rate by device type per page. Lead capture surfaces often underperform on mobile -- this identifies which pages need mobile optimization.
- **Traffic source quality:** conversion rate by `utm_source`. Some traffic sources bring visitors who browse but never convert -- this identifies where to cut spend.

## Output

- Real-time lead capture funnel with per-page and per-surface breakdown
- Daily automated monitoring with anomaly alerts
- Weekly page performance ranking
- Form abandonment analysis (form surfaces)
- Device and traffic source conversion splits
- Historical baseline tracking for long-term trend analysis

## Triggers

- Daily monitoring: runs every day at 9 AM via n8n cron
- Weekly page report: runs every Monday at 8 AM via n8n cron
- Event-triggered: fires on every form submission or booking webhook
