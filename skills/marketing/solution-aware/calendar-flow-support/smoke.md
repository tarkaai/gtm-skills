---
name: calendar-flow-support-smoke
description: >
  Calendar booking flow support — Smoke Test. Embed an inline Cal.com scheduling widget on one
  high-intent page and send solution-aware prospects to it. Validate whether removing booking
  friction (no redirect, no email back-and-forth) increases speed-to-meeting.
stage: "Marketing > SolutionAware"
motion: "LeadCaptureSurface"
channels: "Direct"
level: "Smoke Test"
time: "4 hours over 1 week"
outcome: "≥ 3 meetings booked via inline calendar from ≤ 30 CTA impressions in 7 days"
kpis: ["Booking completion rate (target ≥ 10%)", "Time from CTA click to confirmed booking (target < 5 min)", "Show rate (target ≥ 80%)"]
slug: "calendar-flow-support"
install: "npx gtm-skills add marketing/solution-aware/calendar-flow-support"
drills:
  - meeting-booking-flow
  - threshold-engine
---

# Calendar Booking Flow Support — Smoke Test

> **Stage:** Marketing > SolutionAware | **Motion:** LeadCaptureSurface | **Channels:** Direct

## Outcomes

Prove that embedding a Cal.com inline calendar widget directly in a CTA surface converts solution-aware prospects into booked meetings faster and at a higher rate than a standalone booking link or contact form. Solution-aware prospects already know they need a solution like yours — the bottleneck is scheduling friction. This test removes it.

Pass: 3 or more meetings booked through the inline calendar from up to 30 CTA impressions within 7 days.
Fail: Fewer than 3 bookings from 30+ impressions after 7 days.

## Leading Indicators

- First booking arrives within 48 hours of deploying the inline embed (the surface is discoverable and the availability is attractive)
- At least 1 booking comes from a prospect you did not directly point to the page (organic discovery signal)
- Time from CTA click to confirmed booking is under 5 minutes (proves the inline flow removes friction vs. redirect)
- Widget load rate is above 95% (the embed is technically healthy)

## Instructions

### 1. Configure the Cal.com event type and booking flow

Run the `meeting-booking-flow` drill. Specifically:
- Use the `calcom-event-types` fundamental to create a "Discovery Call" event type (30 min) with 15-min buffers, 24-hour minimum notice, and 14-day booking window.
- Add 2-3 booking form questions: "Company name", "What are you evaluating?", "How did you find us?". Keep it short — every extra field reduces completion rate.
- Use `calcom-crm-sync` to build an n8n workflow that creates an Attio Person, Company, and Deal at "Meeting Booked" stage when a booking comes through.
- Use `calcom-booking-links` to generate the booking link with UTM parameters: `?utm_source=website&utm_medium=inline-embed&utm_campaign=smoke-test`.

### 2. Embed the calendar inline on one high-intent page

Choose the single highest-intent page you have: pricing page, "Book a Demo" page, or a comparison page where solution-aware prospects land. Do not scatter across multiple pages — Smoke tests one surface.

Use the `calcom-inline-embed` fundamental to add the inline widget. Place it:
- Below the primary value proposition or pricing table
- Above the fold if possible, or immediately after the first scroll
- With a clear heading: "Pick a time — 30-minute discovery call" (not "Contact us" or "Get in touch")

Test the embed: load the page, verify the calendar renders with available slots, book a test meeting yourself, confirm the n8n webhook fires and creates the Attio record.

### 3. Add lightweight tracking

Manually track impressions and conversions in a spreadsheet or Attio notes for the Smoke test. For each day:
- Count unique visitors to the page (check your analytics or server logs)
- Count `meeting_booked` events from the Cal.com webhook in Attio
- Note the time elapsed between page load and booking confirmation for each booking

If you already have PostHog on the page, add the `calendar_widget_loaded` and `meeting_booked` capture calls from the `calcom-inline-embed` fundamental. This is optional at Smoke — the goal is to validate the channel, not build a measurement system.

### 4. Drive 30 solution-aware prospects to the page

**Human action required:** You need to send solution-aware prospects to the page with the inline calendar. Options:
- Email your existing pipeline contacts who have not booked: "I added a way to grab time directly — [link to page]"
- Post the page link in relevant communities where you are already active
- Add the page link to your email signature for 1 week
- If running any outbound, replace the Calendly/Cal.com standalone link in your CTA with a link to this page

Target: 30 unique visitors who match your ICP within 7 days. These should be solution-aware (they know the problem category and are evaluating solutions), not cold traffic.

### 5. Evaluate results after 7 days

Run the `threshold-engine` drill to measure against the pass threshold.

Count: total page visitors, total bookings via inline calendar, show rate for booked meetings. Compute booking completion rate (bookings / visitors).

- **PASS (≥ 3 bookings from ≤ 30 impressions):** The inline calendar converts solution-aware traffic. Document the page, embed placement, and conversion rate. Proceed to Baseline.
- **MARGINAL (1-2 bookings):** Check: Were the visitors actually solution-aware? Was the availability attractive (enough time slots, reasonable hours)? Was the embed visible without excessive scrolling? Fix the weakest link and re-run with 30 fresh visitors.
- **FAIL (0 bookings):** Diagnose: Did the widget load correctly (check browser console for errors)? Did visitors scroll to the embed? Did anyone click a time slot but not complete the form? If the widget worked but nobody booked, the page or audience may be the issue, not the calendar flow.

## Time Estimate

- Cal.com event type setup and n8n webhook: 1 hour
- Embed installation and testing: 1 hour
- Driving traffic over 7 days: 1 hour total (composing emails/posts)
- Monitoring and evaluation: 1 hour
- Total: ~4 hours of active work spread over 1 week

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Cal.com | Inline scheduling embed + event types | Free plan ([cal.com/pricing](https://cal.com/pricing)) |
| Attio | CRM — log bookings and create deals | Free up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| n8n | Webhook from Cal.com to Attio | Free self-hosted or Starter €24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |

**Estimated monthly cost for Smoke:** $0 (all tools on free tiers)

## Drills Referenced

- `meeting-booking-flow` — configure Cal.com event types, booking links with UTM tracking, CRM sync via n8n, and post-booking automation
- `threshold-engine` — evaluate booking rate against the pass threshold and recommend next action
