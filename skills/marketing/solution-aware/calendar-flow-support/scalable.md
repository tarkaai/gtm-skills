---
name: calendar-flow-support-scalable
description: >
  Calendar booking flow support — Scalable Automation. Expand inline calendar embeds to all
  solution-aware surfaces. Run A/B tests on embed placement, CTA copy, availability windows,
  and form fields. Automate the full booking-to-meeting pipeline. Scale booking volume 5-10x
  without proportional effort.
stage: "Marketing > SolutionAware"
motion: "LeadCaptureSurface"
channels: "Direct"
level: "Scalable Automation"
time: "50 hours over 2 months"
outcome: "≥ 8% booking completion rate sustained at 5-10x Baseline volume (≥ 75 bookings/mo) over 2 months"
kpis: ["Monthly bookings (target ≥ 75)", "Booking completion rate (target ≥ 8%)", "Show rate (target ≥ 80%)", "Cost per booked meeting", "Booking-to-opportunity conversion rate"]
slug: "calendar-flow-support"
install: "npx gtm-skills add marketing/solution-aware/calendar-flow-support"
drills:
  - ab-test-orchestrator
  - follow-up-automation
  - tool-sync-workflow
---

# Calendar Booking Flow Support — Scalable Automation

> **Stage:** Marketing > SolutionAware | **Motion:** LeadCaptureSurface | **Channels:** Direct

## Outcomes

Scale the inline calendar booking flow from 3-5 pages to every solution-aware surface in your marketing stack. Run systematic A/B tests to find the optimal embed configuration. Automate the entire pipeline: booking confirmation, pre-meeting prep, no-show recovery, post-meeting follow-up, and CRM lifecycle updates. Booking volume reaches 5-10x Baseline without the team spending proportionally more time.

Pass: Booking completion rate holds at ≥ 8% while monthly bookings reach ≥ 75 for 2 consecutive months. Show rate ≥ 80%. All bookings sync to CRM automatically.
Fail: Booking rate drops below 6% at scale, or monthly bookings fail to reach 75 for 2 consecutive months despite sufficient traffic.

## Leading Indicators

- A/B tests on CTA copy or placement produce a statistically significant winner at least once per month (the system is still finding improvements)
- Booking completion rate does not decay as volume increases (proves the funnel scales without degrading)
- No-show recovery automation reschedules ≥ 30% of no-shows (reduces wasted meetings)
- Mobile booking rate closes the gap with desktop (mobile-specific optimizations are working)
- Booking-to-opportunity conversion rate ≥ 40% (the calendar flow attracts qualified prospects, not tire-kickers)

## Instructions

### 1. Expand calendar embeds to all solution-aware surfaces

Deploy inline Cal.com embeds on every page where solution-aware prospects express intent. Build an inventory of surfaces and deploy systematically:

**Website pages:**
- Pricing page (already from Baseline)
- Book a Demo page (already from Baseline)
- Every comparison/alternative page ("YourProduct vs Competitor X")
- Case study pages (after reading proof, the prospect wants to talk)
- Integration pages (prospect evaluating your ecosystem fit)
- Documentation landing pages with "Need help?" CTAs

**Email surfaces:**
- Add a "Book time" CTA with the Cal.com link (not inline embed — email clients don't support JS) to: outbound email sequences (final step), newsletter CTAs, lifecycle emails for solution-aware segments

**Other surfaces:**
- Intercom messenger: add a "Book a call" action that opens the Cal.com booking page
- LinkedIn profile Featured section: link to the demo page with inline embed
- Blog post CTAs on solution-aware content: embed inline calendar at the bottom of high-intent posts

Use the `calcom-inline-embed` fundamental for every new embed. Tag each surface with a distinct `utm_campaign` so PostHog attributes bookings to specific surfaces.

Run the `tool-sync-workflow` drill to ensure all new surfaces send events to PostHog and that Cal.com webhooks flow to Attio. Verify: every new embed fires `calendar_widget_loaded`, every booking creates an Attio deal, every PostHog funnel includes the new surface.

### 2. Run systematic A/B tests

Run the `ab-test-orchestrator` drill. Test one variable at a time across your highest-traffic pages. Each test needs ≥ 200 impressions per variant for statistical significance.

**Month 1 tests:**
- **CTA heading copy:** Test "Pick a time that works" vs "Book a 30-min discovery call" vs "Schedule your demo" above the inline embed. Measure: `cta_impression` -> `meeting_booked` rate per variant.
- **Embed placement:** Test the calendar above the fold vs below social proof vs at the very bottom. Use PostHog feature flags to randomize placement per visitor. Measure: booking completion rate per variant.

**Month 2 tests:**
- **Booking form length:** Test 2-field (name + email) vs 4-field (name + email + company + "What are you evaluating?"). Measure: `timeslot_selected` -> `meeting_booked` drop-off per variant. Shorter forms may convert more but produce less-qualified bookings — check booking-to-opportunity rate for both variants.
- **Availability window:** Test showing 5 days of availability vs 10 days vs 14 days. More days means more visual choice (possible decision paralysis). Fewer days means less flexibility. Measure: `calendar_widget_loaded` -> `timeslot_selected` rate.

For each test, log the hypothesis, variants, sample size, result, and decision in PostHog annotations and Attio campaign notes. Apply the winner immediately. Move to the next test.

### 3. Build the complete follow-up automation stack

Run the `follow-up-automation` drill to create n8n workflows for every post-booking scenario:

**Immediate post-booking (fires within 1 minute of booking):**
- Send booking confirmation via Loops with: meeting details, prep instructions ("Here are 3 things that will make our call more productive"), and a link to reschedule if needed
- Create or update the Attio deal at "Meeting Booked" stage
- Fire PostHog event: `meeting_booked` with all properties

**Pre-meeting prep (fires 2 hours before meeting):**
- Pull company data from Clay enrichment (if available) or Attio company record
- Generate a 1-paragraph meeting brief: prospect name, company, what they're evaluating (from booking form), the page they booked from, and any prior touchpoints logged in Attio
- Send the brief to the meeting host via Slack

**No-show recovery (fires 30 minutes after meeting end if not marked completed):**
- Wait 2 hours, then send a reschedule email via Loops: "I missed you — here's a fresh link to rebook: [Cal.com link]"
- If no rebook within 48 hours, send one more follow-up with 3 specific time slots
- Update Attio: deal stage = "No-Show", activity note = "Reschedule sequence initiated"
- Track recovery rate in PostHog: `noshow_reschedule_sent` -> `meeting_rebooked`

**Post-meeting follow-up (fires 1 hour after meeting marked completed):**
- Send a thank-you email via Loops with a summary of next steps (agent drafts from Attio meeting notes or Fireflies transcript if available)
- Update Attio deal stage based on meeting outcome: "Qualified", "Not Qualified", or "Follow-Up Needed"

### 4. Monitor weekly and optimize

Track these metrics weekly in PostHog:
- Total bookings by surface (which pages drive the most meetings?)
- Booking completion rate by surface (which pages convert best?)
- Mobile vs desktop booking rate per surface
- A/B test progress (is the current test reaching statistical significance on schedule?)
- No-show rate and recovery rate
- Booking-to-opportunity conversion rate

Focus optimization effort on the top 3 surfaces by booking volume. For surfaces producing < 2 bookings/month, either improve the page's traffic or remove the embed to reduce maintenance.

### 5. Evaluate after 2 months

Compute over the full 2-month period:
- Total bookings per month (target: ≥ 75)
- Booking completion rate across all surfaces (target: ≥ 8%)
- Show rate (target: ≥ 80%)
- Cost per booked meeting (Cal.com + n8n + team time)
- Booking-to-opportunity conversion rate (target: ≥ 40%)
- Number of A/B tests completed and their cumulative improvement

- **PASS (≥ 75 bookings/mo at ≥ 8% rate for 2 months):** The calendar flow scales. Document the winning embed configuration, CTA copy, form fields, and surface ranking. Proceed to Durable.
- **DECLINING (rate held month 1 but dropped month 2):** Diagnose: Did traffic quality change? Did a top surface break? Did mobile conversion drop? Fix the specific issue and run 1 more month.
- **FAIL (< 75 bookings/mo or < 6% rate):** Check: Is there enough solution-aware traffic across all surfaces? If traffic is sufficient but conversion is low, the inline calendar may not be the right conversion surface for your audience. Test a popup embed or a traditional form + follow-up call flow as an alternative.

## Time Estimate

- Expand embeds to all surfaces: 8 hours (Month 1)
- A/B test setup and management: 6 hours/month x 2 = 12 hours
- Follow-up automation stack: 10 hours (Month 1)
- Tool sync verification: 4 hours (Month 1)
- Weekly monitoring: 2 hours/week x 8 weeks = 16 hours
- Total: ~50 hours over 2 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Cal.com | Inline scheduling embeds across all surfaces | Free plan — or Teams $15/user/mo for round-robin ([cal.com/pricing](https://cal.com/pricing)) |
| PostHog | Funnel analytics, A/B test measurement, feature flags | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | CRM — deal lifecycle, contact management | Plus $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| n8n | All automation: booking sync, prep, follow-up, no-show recovery | Pro €60/mo or self-host free ([n8n.io/pricing](https://n8n.io/pricing)) |
| Loops | Booking confirmation, no-show recovery, follow-up emails | Free tier or Starter $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Clay | Pre-meeting company enrichment | Starter $149/mo ([clay.com/pricing](https://clay.com/pricing)) |

**Estimated monthly cost for Scalable:** $150-350/mo depending on team size and volume

## Drills Referenced

- `ab-test-orchestrator` — design, run, and evaluate A/B tests on CTA copy, embed placement, form length, and availability window using PostHog feature flags
- `follow-up-automation` — build n8n workflows for booking confirmation, pre-meeting prep, no-show recovery, and post-meeting follow-up
- `tool-sync-workflow` — connect all booking surfaces to PostHog events and Attio CRM via n8n to maintain a single source of truth
