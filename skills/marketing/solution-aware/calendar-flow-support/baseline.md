---
name: calendar-flow-support-baseline
description: >
  Calendar booking flow support — Baseline Run. Deploy inline Cal.com embeds on 3-5 high-intent
  pages with full PostHog funnel tracking. First always-on automation: n8n routes bookings to CRM,
  fires tracking events, and sends pre-meeting prep. Validate that booking rate holds at ≥ 8%
  across pages over 2 weeks.
stage: "Marketing > SolutionAware"
motion: "LeadCaptureSurface"
channels: "Direct"
level: "Baseline Run"
time: "12 hours over 2 weeks"
outcome: "≥ 8% booking completion rate sustained across 3-5 pages over 2 weeks with ≥ 15 total bookings"
kpis: ["Booking completion rate per page (target ≥ 8%)", "Widget load rate (target ≥ 95%)", "Avg time from CTA click to confirmed booking", "Show rate (target ≥ 80%)", "CRM deal creation accuracy (target 100%)"]
slug: "calendar-flow-support"
install: "npx gtm-skills add marketing/solution-aware/calendar-flow-support"
drills:
  - posthog-gtm-events
  - landing-page-pipeline
  - meeting-booking-flow
---

# Calendar Booking Flow Support — Baseline Run

> **Stage:** Marketing > SolutionAware | **Motion:** LeadCaptureSurface | **Channels:** Direct

## Outcomes

Expand the inline calendar embed from 1 page (Smoke) to 3-5 high-intent pages. Build full PostHog event tracking so every stage of the booking funnel is measured. Prove the conversion rate holds across multiple surfaces and that the n8n automation pipeline (booking -> CRM -> pre-meeting prep) runs reliably without manual intervention.

Pass: Booking completion rate ≥ 8% across all pages combined, with ≥ 15 total bookings over 2 weeks. All bookings automatically create Attio deals.
Fail: Booking rate below 8% after 2 weeks, or automation fails to sync bookings to CRM.

## Leading Indicators

- Widget load rate stays above 95% on all pages (no broken embeds)
- Booking rate on the original Smoke page does not drop when traffic sources diversify
- At least 2 of the 3-5 pages produce bookings (not all traffic concentrated on one page)
- Pre-meeting prep emails send automatically for every booking (automation is reliable)
- Time from CTA click to confirmed booking stays under 5 minutes

## Instructions

### 1. Set up full booking funnel tracking

Run the `posthog-gtm-events` drill to implement the booking funnel event taxonomy. Configure these events on every page that will have an inline calendar:

| Event | Trigger | Properties |
|-------|---------|------------|
| `cta_impression` | Calendar embed section enters viewport | `page`, `cta_variant`, `device_type` |
| `calendar_widget_loaded` | Cal.com embed fires `linkReady` callback | `page`, `event_type` |
| `timeslot_selected` | Prospect clicks a time slot in the widget | `page`, `event_type`, `day_of_week`, `time_of_day` |
| `meeting_booked` | Cal.com booking webhook fires | `event_type`, `source`, `lead_email`, `utm_source`, `utm_campaign` |

Use the `calcom-inline-embed` fundamental's embed event listeners to capture `calendar_widget_loaded` and `meeting_booked` client-side. Use the Cal.com webhook via n8n (from `calcom-crm-sync`) as the server-side source of truth for `meeting_booked`.

Build a PostHog funnel: `cta_impression` -> `calendar_widget_loaded` -> `timeslot_selected` -> `meeting_booked`. Save as "Calendar Booking Funnel - Baseline". Break down by `page` to compare surface performance.

### 2. Deploy inline embeds on 3-5 high-intent pages

Run the `landing-page-pipeline` drill to identify and prepare the pages. For each page:

1. Select pages where solution-aware prospects land with booking intent: pricing page, "Book a Demo" page, comparison/alternative pages, high-intent blog posts, case study pages.
2. Use the `calcom-inline-embed` fundamental to add the widget. Place below the primary value proposition or call-to-action section — the embed should appear where the prospect's next logical action is "talk to us."
3. Set a distinct `utm_campaign` per page so PostHog can attribute bookings to specific surfaces: `?utm_campaign=pricing-page`, `?utm_campaign=demo-page`, etc.
4. Add the PostHog event capture code from step 1 to each page.

Test each page: verify the widget loads, book a test meeting, confirm the PostHog events fire, confirm the n8n webhook creates an Attio record.

### 3. Build the booking automation pipeline

Extend the `meeting-booking-flow` drill to add Baseline-level automation in n8n:

**Booking -> CRM workflow:**
- Cal.com webhook fires -> n8n receives booking data -> search Attio for existing contact by email -> if found, update deal stage to "Meeting Booked" and add a note; if not found, create Person + Company + Deal at "Meeting Booked" stage -> fire `meeting_booked` event to PostHog with all properties

**Pre-meeting prep workflow:**
- Trigger: 1 hour before scheduled meeting time (n8n cron checks upcoming meetings daily)
- Action: Send the meeting host a Slack message with: prospect name, company, booking form answers ("What are you evaluating?"), the page they booked from (utm_campaign), and any existing Attio notes on the contact
- This ensures every meeting starts with context, not cold

**No-show follow-up workflow:**
- Trigger: 30 minutes after scheduled meeting end time, if meeting status is not marked "completed"
- Action: Send a templated reschedule email via Loops with a fresh Cal.com booking link. Update Attio deal stage to "No-Show — Reschedule Sent"

### 4. Monitor the funnel weekly

At the end of week 1, pull the PostHog funnel data. Check:
- Per-page booking rate: which pages convert best?
- Widget load rate: any page below 95% has a technical issue — fix it immediately
- Timeslot selection -> booking completion rate: if prospects select slots but don't complete the form, the form has too many fields or a UX issue
- Show rate: if below 80%, add a reminder email at booking + 24 hours

Adjust embed placement or page copy for underperforming pages. Do not add new pages — optimize the existing 3-5 first.

### 5. Evaluate after 2 weeks

Run the `threshold-engine` drill. Compute across all pages:

- Total CTA impressions, total bookings, booking completion rate
- Per-page breakdown: rate, volume, show rate
- Automation reliability: did every booking create an Attio deal? (Target: 100%)
- Avg time from CTA click to confirmed booking

- **PASS (≥ 8% booking rate, ≥ 15 bookings, 100% CRM sync):** The calendar flow works as an always-on conversion surface. Document top-performing pages and proceed to Scalable.
- **MARGINAL (5-8% booking rate or 10-14 bookings):** Identify the weakest funnel step. If widget loads but few select time slots: availability or page placement issue. If time slots selected but bookings don't complete: form friction. Fix and run 1 more week.
- **FAIL (< 5% booking rate or < 10 bookings):** The inline calendar is not outperforming other conversion paths. Check: are these pages actually receiving solution-aware traffic? Is the Cal.com availability showing attractive time slots? Is mobile rendering broken?

## Time Estimate

- PostHog event setup and funnel creation: 3 hours
- Embed deployment on 3-5 pages: 3 hours
- n8n automation (CRM sync, prep, no-show): 3 hours
- Weekly monitoring and optimization: 2 hours
- Final evaluation: 1 hour
- Total: ~12 hours over 2 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Cal.com | Inline scheduling embeds on multiple pages | Free plan ([cal.com/pricing](https://cal.com/pricing)) |
| PostHog | Funnel tracking, event analytics | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | CRM — deal creation and contact management | Free up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| n8n | Booking -> CRM sync, prep emails, no-show follow-up | Free self-hosted or Starter €24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Loops | No-show reschedule email | Free tier ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated monthly cost for Baseline:** $0-24/mo (all tools within free tiers at this volume, n8n cloud optional)

## Drills Referenced

- `posthog-gtm-events` — implement the booking funnel event taxonomy and build conversion funnels in PostHog
- `landing-page-pipeline` — select and prepare high-intent pages for calendar embed deployment
- `meeting-booking-flow` — extend the Cal.com -> n8n -> Attio pipeline with pre-meeting prep and no-show automation
