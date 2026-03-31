---
name: conference-booth-sponsorship-smoke
description: >
  Conference Booth & Sponsorship — Smoke Test. Sponsor one conference with a
  booth, capture leads via badge scanning and structured conversations, and
  validate that in-person booth engagement generates qualified pipeline for
  solution-aware prospects.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events"
level: "Smoke Test"
time: "8 hours over 3 weeks"
outcome: ">=40 badge scans, >=8 qualified leads (Tier 1+2), >=3 meetings booked within 14 days of conference"
kpis: ["Badge scans", "Qualified lead rate", "Meetings booked"]
slug: "conference-booth-sponsorship"
install: "npx gtm-skills add marketing/solution-aware/conference-booth-sponsorship"
drills:
  - icp-definition
  - conference-sponsorship-pipeline
  - booth-lead-capture
  - threshold-engine
---

# Conference Booth & Sponsorship — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** MicroEvents | **Channels:** Events

## Outcomes

- Confirm that your ICP attends the selected conference in sufficient density to justify sponsorship cost
- Validate that booth conversations produce qualified leads with real pain points and timelines
- Generate at least 3 booked meetings from a single conference booth sponsorship
- Gather baseline data on badge-to-meeting conversion rate, cost per qualified lead, and which demo track resonates

## Leading Indicators

- Pre-event outreach to known attendees gets >20% response rate (audience is relevant)
- Booth visitors self-identify pain points your product addresses (not just swag collectors)
- At least 20% of badge scans result in a Tier 1 or Tier 2 qualification (booth attracts ICP)
- At least 2 visitors book meetings on the spot via Cal.com QR code (high intent present)

## Instructions

### 1. Define your conference ICP and select a conference

Run the `icp-definition` drill to document the target attendee profile: which titles, company sizes, industries, and pain points should the conference audience have?

Then run the `conference-sponsorship-pipeline` drill at minimum scope: identify 3-5 candidate conferences in the next 60-90 days. Score each on ICP density, attendee volume, sponsorship value, and logistics. Select the one highest-scoring conference.

For the Smoke test, select the lowest-cost sponsorship tier that includes:
- A booth or table (even a small one — you need a physical presence)
- Lead retrieval or badge scanning access (this is non-negotiable; if the tier does not include it, ask if you can add it for an extra fee, or use the manual Tally form fallback)

**Human action required:** Contact the conference organizer, review the sponsorship prospectus, sign the agreement, and pay. The agent can draft the initial outreach email but you need to complete the purchase.

### 2. Prepare booth operations

Run the `conference-sponsorship-pipeline` drill's pre-event preparation steps:

- Prepare 3 demo tracks: 2-minute overview (for browsing visitors), 5-minute focused demo (for interested visitors), 15-minute deep dive (for high-intent prospects)
- Configure the lead capture system using the `badge-scan-lead-import` fundamental: install the conference's lead retrieval app OR build a mobile Tally/Typeform form as fallback with fields: name, email, company, title, interest tier (1-4), pain point mentioned, agreed next step, demo given (y/n)
- Generate a Cal.com QR code for on-the-spot meeting booking. Print 2-3 copies.
- If the conference shares a registrant or attendee list, import into Clay and run `event-attendee-enrichment` to build a priority target list. Send 20-30 pre-event outreach messages to high-score targets: "Visiting {conference}? Stop by booth #{number} — we built {product} specifically for {their pain point}."

**Human action required:** Pack hardware (laptop, tablet, charger, hotspot), print QR codes, set up the booth on event day.

### 3. Execute booth lead capture

Run the `booth-lead-capture` drill on each day of the conference:

- Scan every visitor's badge (or log via manual form)
- Qualify each conversation using the 4-tier framework during the conversation, not after
- Give demos to Tier 1-2 visitors. Skip demos for Tier 3-4.
- Book meetings on the spot for Tier 1 via Cal.com QR code
- Log notes immediately after each conversation — do not wait until end of day

**Human action required:** You are at the booth, having conversations, giving demos. The agent handles pre-event prep and post-event data processing. During the event, you are the human element.

### 4. Execute same-day enrichment and basic follow-up

Run the `booth-lead-capture` drill's same-day enrichment steps each evening:

- Export badge scan data and import to Attio
- Tag all contacts with conference name, date, and interest tier
- Create Attio deals for Tier 1 contacts
- Send personal follow-up emails to Tier 1 contacts within 12 hours (reference the specific conversation, attach relevant resource, include Cal.com link if meeting not yet booked)
- Send a simple thank-you email to Tier 2 contacts within 48 hours with a relevant resource and Cal.com link

At Smoke level, follow-up is manual and personal — not automated sequences. The agent drafts the emails; you review and send.

### 5. Evaluate against the threshold

Run the `threshold-engine` drill 14 days after the conference to measure:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Badge scans | >=40 | Total scans in Attio conference list |
| Qualified leads (Tier 1+2) | >=8 | Tier 1 + Tier 2 contacts in Attio |
| Meetings booked | >=3 | Cal.com bookings within 14 days of conference |

Also calculate (for baseline data, not pass/fail):
- Cost per qualified lead: sponsorship cost / Tier 1+2 count
- Cost per meeting: sponsorship cost / meetings booked
- Qualified lead rate: (Tier 1+2) / total scans
- Most-discussed pain points (from booth notes)
- Which demo track was given most often

**PASS**: All three metrics met. Proceed to Baseline. In-person booth engagement works for your ICP at this conference type.

**FAIL**: Diagnose which metric missed:
- Low badge scans (<40): Conference attendance was lower than expected, or booth location was poor, or the conference audience does not match your ICP. Try a different conference with higher ICP density.
- Low qualified rate (<8 Tier 1+2): Visitors were not ICP matches. Reassess conference selection — the audience does not have the pain points you solve.
- Low meetings (<3): Leads were qualified but did not commit to next steps. Review your closing technique — are you asking for the meeting directly? Is the Cal.com QR code visible and easy to use?

## Time Estimate

- Conference selection and scoring: 2 hours
- Pre-event preparation (demo, lead capture setup, target list): 2 hours
- Booth execution: included in conference attendance (not counted as play time)
- Same-day enrichment and follow-up: 2 hours
- Analysis and threshold evaluation: 2 hours
- **Total: ~8 hours over 3 weeks** (1 week prep, conference days, 2 weeks follow-up)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Conference scoring + attendee enrichment | $149/mo Explorer (1,200 credits) — [clay.com/pricing](https://www.clay.com/pricing) |
| Attio | Lead tracking + deal creation | Free tier: 3 users — [attio.com](https://attio.com) |
| Cal.com | On-the-spot meeting booking | Free tier: 1 user — [cal.com/pricing](https://cal.com/pricing) |
| PostHog | Event tracking | Free tier: 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Tally | Manual lead capture form (if no badge scanner) | Free — [tally.so](https://tally.so) |

**Estimated play-specific cost at Smoke: $149/mo + sponsorship cost** (sponsorship typically $1,000-5,000 for small/mid-tier conferences)

## Drills Referenced

- `icp-definition` — define the target attendee profile to guide conference selection
- `conference-sponsorship-pipeline` — evaluate, score, and select the conference to sponsor
- `booth-lead-capture` — execute booth operations, capture and qualify leads, same-day enrichment
- `threshold-engine` — evaluate pass/fail against badge scan, qualified lead, and meeting targets
