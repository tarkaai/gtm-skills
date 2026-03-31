---
name: conference-speaking-program-baseline
description: >
  Conference Speaking — Baseline Run. Always-on CFP pipeline with bi-weekly discovery,
  automated proposal drafting, structured post-talk follow-up sequences, and lead attribution
  tracking. First continuous automation of the speaking program.
stage: "Marketing > ProblemAware"
motion: "MicroEvents"
channels: "Events, Social"
level: "Baseline Run"
time: "20 hours over 10 weeks"
outcome: "≥3 accepted talks and ≥30 attributed leads across all talks in 10 weeks"
kpis: ["CFP acceptance rate", "Leads per talk", "Post-talk email sequence open rate", "Cal.com booking rate", "Cost per lead"]
slug: "conference-speaking-program"
install: "npx gtm-skills add marketing/problem-aware/conference-speaking-program"
drills:
  - conference-cfp-pipeline
  - posthog-gtm-events
---

# Conference Speaking — Baseline Run

> **Stage:** Marketing → ProblemAware | **Motion:** MicroEvents | **Channels:** Events, Social

## Outcomes

Run the conference speaking program as a continuous pipeline -- not one-off submissions. Bi-weekly CFP discovery feeds a steady flow of proposals. Every accepted talk has structured lead capture and automated follow-up. Prove that the speaking program generates pipeline reliably over 10 weeks, not just once.

## Leading Indicators

- CFP discovery runs every 2 weeks, producing 5+ new scored CFPs per cycle
- 2+ proposals submitted per bi-weekly cycle (10+ total over 10 weeks)
- Acceptance rate holds at ≥25% (≥3 of 10+ submissions)
- Post-talk follow-up email sequence achieves ≥35% open rate and ≥8% click rate
- Companion page conversion rate (visitor to email signup or Cal.com booking) ≥15%

## Instructions

### 1. Establish the always-on CFP pipeline

Run the full `conference-cfp-pipeline` drill on a bi-weekly cadence:

1. Every 2 weeks, re-run Clay discovery to find new open CFPs matching your topic keywords
2. Score all new CFPs using the standard scoring formula (ICP density, topic fit, audience size, logistics, reputation)
3. Auto-update the Attio "CFP Pipeline" list with new entries
4. For all CFPs scoring 60+, auto-generate proposals using the `talk-proposal-generation` fundamental
5. Queue proposals for human review (Attio task or Slack notification)

**Human action required:** Review and approve/edit generated proposals before submission. Review cadence: twice per week, 15 minutes each.

### 2. Configure speaking event tracking

Run the `posthog-gtm-events` drill to establish the speaking event taxonomy:

Define these events and ensure they fire consistently:

| Event | When Fired | Key Properties |
|-------|-----------|----------------|
| `speaking_cfp_submitted` | Proposal submitted | conference_name, talk_title, cfp_score |
| `speaking_cfp_accepted` | Acceptance received | conference_name, talk_title |
| `speaking_cfp_rejected` | Rejection received | conference_name, talk_title |
| `speaking_talk_delivered` | Talk given | conference_name, audience_size, talk_format |
| `speaking_companion_page_viewed` | Companion page visit | conference_name, utm_source |
| `speaking_email_captured` | Form submission | conference_name, talk_title |
| `speaking_meeting_booked` | Cal.com booking | conference_name, talk_title |
| `speaking_talk_roi_calculated` | 30-day attribution | total_leads, meetings_booked, pipeline_value |

Build a PostHog funnel: submitted → accepted → delivered → leads_captured → meeting_booked

### 3. Deploy lead capture for every accepted talk

Run the the speaking lead capture workflow (see instructions below) drill for each accepted talk:

1. Create companion resource page with UTM-tagged links, Cal.com embed, and email capture form
2. Generate QR code for final talk slide
3. Configure 3-email post-talk follow-up sequence in Loops:
   - Email 1 (Day 0-1): "Thanks for catching my talk" + companion resource link
   - Email 2 (Day 3): Deep-dive on one key takeaway + soft CTA
   - Email 3 (Day 7): Q&A recap + direct Cal.com booking CTA
4. Set up Attio automation: when `speaking_meeting_booked` fires, create deal in Attio pipeline with source attribution

### 4. Run the cadence for 10 weeks

Execute the bi-weekly rhythm:

- **Week 1, 3, 5, 7, 9:** CFP discovery cycle — agent discovers, scores, and drafts proposals. Human reviews and submits.
- **Ongoing:** As acceptances arrive, deploy lead capture per talk. Deliver talks. Monitor follow-up sequence performance.
- **After each talk:** Wait 14 days, then run attribution calculation. Fire `speaking_talk_roi_calculated`.
- **Week 10:** Aggregate all results for threshold evaluation.

### 5. Evaluate against threshold

- **Pass threshold:** ≥3 accepted talks AND ≥30 total attributed leads across all talks
- **Pass:** Document: which conference types yield the highest acceptance rate, which talk topics generate the most leads, which lead capture channel (QR, email, Cal.com) converts best. Proceed to Scalable.
- **Marginal pass (3 talks, 20-29 leads):** Lead capture is working but yield per talk is low. Investigate: Is companion page discoverable enough? Is QR code visible during the talk? Are follow-up emails compelling? Optimize and re-run one more Baseline cycle.
- **Fail (<3 acceptances):** Proposal quality or conference targeting is the bottleneck. Review rejection patterns. Get feedback from organizers. Consider diversifying talk topics or targeting smaller/regional conferences with higher acceptance rates.

## Time Estimate

- 4 hours: Initial CFP pipeline setup and event tracking configuration
- 1 hour per bi-weekly cycle x 5 cycles: CFP discovery, scoring, proposal review = 5 hours
- 2 hours per accepted talk x 3 talks: Lead capture setup = 6 hours
- 5 hours: Monitoring, attribution, and analysis (spread across 10 weeks)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Bi-weekly CFP discovery and scoring | Launch: $185/mo (https://www.clay.com/pricing) |
| Anthropic API | Proposal generation (10+ proposals) | ~$0.90/quarter |
| Cal.com | Post-talk booking links | Free tier or Team: $12/user/mo (https://cal.com/pricing) |
| Loops | Post-talk email sequences | Free up to 1,000 contacts (https://loops.so/pricing) |
| Sessionize | Speaker profile, track submissions | Free for speakers (https://sessionize.com/pricing) |

**Total Baseline budget:** Clay $185/mo + Cal.com Free = ~$185/mo

## Drills Referenced

- `conference-cfp-pipeline` — always-on CFP discovery, scoring, proposal drafting, and submission tracking
- the speaking lead capture workflow (see instructions below) — post-talk lead capture infrastructure, follow-up sequences, and attribution
- `posthog-gtm-events` — speaking event taxonomy and funnel tracking in PostHog
