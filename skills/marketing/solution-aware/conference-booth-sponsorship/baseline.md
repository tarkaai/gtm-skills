---
name: conference-booth-sponsorship-baseline
description: >
  Conference Booth & Sponsorship — Baseline Run. Sponsor 2-3 conferences over
  8-10 weeks with automated post-event nurture, PostHog funnel tracking, and
  structured cross-conference comparison to validate repeatable ROI from booth
  sponsorship.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events"
level: "Baseline Run"
time: "20 hours over 10 weeks"
outcome: ">=100 badge scans total, >=20 qualified leads (Tier 1+2), >=8 meetings booked, cost per meeting below 3x sponsorship-per-conference average"
kpis: ["Qualified leads per conference", "Meetings booked", "Cost per meeting", "Follow-up reply rate", "Badge-to-meeting conversion rate"]
slug: "conference-booth-sponsorship"
install: "npx gtm-skills add marketing/solution-aware/conference-booth-sponsorship"
drills:
  - posthog-gtm-events
  - threshold-engine
---

# Conference Booth & Sponsorship — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** MicroEvents | **Channels:** Events

## Outcomes

- Prove that booth sponsorship ROI is repeatable across 2-3 conferences (not a one-event fluke)
- Establish automated post-event follow-up nurture that converts booth leads to pipeline without manual email drafting
- Build the PostHog event tracking foundation for all conference booth measurement and optimization
- Identify which conference types, booth tactics, and follow-up approaches produce the best results
- Establish baseline cost-per-meeting and cost-per-qualified-lead benchmarks

## Leading Indicators

- Second conference produces qualified leads at a rate within 20% of the first conference (consistency)
- Automated Tier 2 nurture sequence achieves >12% reply rate (follow-up works without manual effort)
- At least 2 meetings booked from automated follow-up sequences (not just on-the-spot bookings)
- Qualified lead rate stays above 15% across all conferences (you are selecting the right events)
- Pre-event outreach response rate improves from conference 1 to conference 2 (learning applied)

## Instructions

### 1. Configure conference booth event tracking

Run the `posthog-gtm-events` drill to implement the full booth sponsorship event taxonomy in PostHog:

- `booth_badge_scanned` — badge scan at booth (properties: conference_name, day, interest_tier)
- `booth_demo_given` — product demo delivered (properties: conference_name, demo_track, duration_minutes, interest_tier)
- `booth_meeting_booked` — meeting booked on the spot (properties: conference_name, interest_tier, days_to_meeting)
- `booth_deal_created` — deal created in CRM (properties: conference_name, deal_value_estimate, interest_tier)
- `booth_followup_sent` — follow-up email sent (properties: conference_name, tier, sequence_step, has_loom)
- `booth_followup_replied` — recipient replied to follow-up (properties: conference_name, tier, reply_sentiment)
- `booth_followup_meeting_booked` — meeting booked from follow-up (properties: conference_name, tier, days_since_conference)
- `booth_conference_roi_calculated` — post-conference ROI report (properties: conference_name, total_scans, qualified_leads, meetings_booked, cost_per_meeting, pipeline_value)

Build a PostHog funnel: `booth_badge_scanned` -> `booth_demo_given` -> `booth_meeting_booked` -> `booth_deal_created`

Build a second funnel for follow-up: `booth_followup_sent` -> `booth_followup_replied` -> `booth_followup_meeting_booked`

### 2. Select and prepare for 2-3 conferences

Using the conference pipeline from Smoke (or running `conference-sponsorship-pipeline` again with updated scoring based on Smoke learnings), select 2-3 conferences spaced over 8-10 weeks.

Apply learnings from Smoke:
- If Smoke showed a specific demo track converted best, lead with that track at the next conference
- If Smoke showed a specific pain point resonated, prepare more depth on that topic
- If badge scan quality was low (too many Tier 3-4), select a more ICP-dense conference or upgrade the sponsorship tier to get a better booth location

For each conference, run the full pre-event preparation from `conference-sponsorship-pipeline`:
- Score and enrich attendees
- Build target lists
- Send pre-event outreach
- Prepare booth operations

### 3. Execute booth operations at each conference

Run the the booth lead capture workflow (see instructions below) drill at each conference with the same process as Smoke, but now with PostHog tracking firing on every interaction:

- Scan every badge, qualify every conversation, log notes in real time
- Give demos to Tier 1-2 visitors using the demo track that performed best at Smoke
- Book meetings on the spot for Tier 1 contacts
- Run same-day CRM enrichment each evening

### 4. Deploy automated follow-up nurture

Run the the booth follow up nurture workflow (see instructions below) drill to replace the manual follow-up from Smoke with automated sequences:

- **Tier 1 (Hot)**: Agent drafts personalized emails referencing booth conversation notes, rep reviews and sends within 12 hours. If rep has Loom, include a 60-second personalized video.
- **Tier 2 (Warm)**: Automated 3-email Loops sequence fires within 24 hours. Emails reference the conference and include relevant resources. Sequence runs over 8 days.
- **Tier 3 (Curious)**: Single automated email on Day 2 with product overview and Cal.com link. If no engagement, add to general marketing nurture.

Configure n8n triggers: when a Tier 2 contact replies positively, auto-create an Attio deal and notify the rep via Slack.

### 5. Cross-conference comparison analysis

After the follow-up windows close on all conferences (14 days after the last conference), compare:

| Metric | Conference 1 | Conference 2 | Conference 3 | Target |
|--------|-------------|-------------|-------------|--------|
| Badge scans | ? | ? | ? | >=100 total |
| Qualified leads (Tier 1+2) | ? | ? | ? | >=20 total |
| Qualified lead rate | ? | ? | ? | >=15% |
| Demos given | ? | ? | ? | — |
| Meetings booked (on-spot) | ? | ? | ? | — |
| Meetings booked (follow-up) | ? | ? | ? | — |
| Total meetings | ? | ? | ? | >=8 total |
| Tier 2 nurture reply rate | ? | ? | ? | >=12% |
| Cost per qualified lead | ? | ? | ? | — |
| Cost per meeting | ? | ? | ? | Benchmark |
| Pipeline value generated | ? | ? | ? | — |

Identify:
- Which conference type produced the best ROI?
- Which demo track generated the most meetings?
- Which follow-up tier drives the most pipeline?
- What pain points came up most frequently across conferences?
- Is cost per meeting consistent or does it vary significantly by conference?

### 6. Evaluate against the threshold

**PASS** (all metrics met): >=100 total badge scans, >=20 qualified leads, >=8 meetings booked, cost per meeting below 3x the per-conference average. Proceed to Scalable. Booth sponsorship is repeatable.

**FAIL**: Diagnose by metric:
- Low badge scans: Conference selection needs improvement — switch to higher-attendance events or better booth locations. Ask organizers about foot traffic patterns before committing.
- Low qualified leads: The audience is not your ICP. Try more vertical-specific conferences instead of broad industry events.
- Low meetings: Follow-up is the bottleneck. Review nurture email copy, test different subject lines, add Loom videos to Tier 2 sequence.
- High cost per meeting: Sponsorship tier is too expensive for the return. Negotiate smaller booth packages or try conferences with lower sponsorship costs.

## Time Estimate

- PostHog event tracking setup: 2 hours
- Conference selection and preparation (x3): 3 hours
- Booth execution per conference (enrichment + follow-up setup): 3 hours x 3 = 9 hours
- Follow-up nurture automation setup (Loops sequences, n8n triggers): 3 hours
- Cross-conference analysis: 3 hours
- **Total: ~20 hours over 10 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Conference scoring + attendee enrichment | $149/mo Explorer — [clay.com/pricing](https://www.clay.com/pricing) |
| Attio | Lead tracking, deals, conference records | Free tier (3 users) or $29/user/mo Plus — [attio.com](https://attio.com) |
| PostHog | Event tracking + funnels | Free tier: 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Loops | Automated follow-up nurture sequences | Free tier (1,000 contacts) or $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Follow-up automation triggers | Self-hosted free or Cloud Starter EUR24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Cal.com | Meeting booking | Free tier — [cal.com/pricing](https://cal.com/pricing) |
| Loom | Personalized follow-up videos (optional) | Free (25 videos, 5 min) or $12.50/mo — [loom.com/pricing](https://www.loom.com/pricing) |

**Estimated play-specific cost at Baseline: $149-240/mo + sponsorship costs** (sponsorship typically $1,000-5,000 per conference)

## Drills Referenced

- `posthog-gtm-events` — implement the conference booth event taxonomy for full funnel measurement
- the booth lead capture workflow (see instructions below) — execute booth operations with structured lead capture at each conference
- the booth follow up nurture workflow (see instructions below) — automated post-conference tier-segmented follow-up sequences
- `threshold-engine` — evaluate pass/fail against badge scan, qualified lead, meeting, and cost targets
