---
name: trade-show-presence-smoke
description: >
  Trade Show Presence — Smoke Test. Attend one industry trade show with a
  booth to validate that your ICP attends these events, your demo converts
  booth traffic into conversations, and you can generate qualified leads
  from in-person interactions. One show, manual ops, no automation.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events"
level: "Smoke Test"
time: "20 hours over 3 weeks"
outcome: ">=50 booth conversations, >=10 demos given, >=3 meetings booked within 14 days of show"
kpis: ["Booth conversations", "Demo-to-conversation rate", "Meetings booked"]
slug: "trade-show-presence"
install: "npx gtm-skills add marketing/solution-aware/trade-show-presence"
drills:
  - icp-definition
  - event-scouting
  - threshold-engine
---

# Trade Show Presence — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** MicroEvents | **Channels:** Events

## Outcomes

- Confirm that your ICP attends industry trade shows in sufficient density to justify booth investment
- Validate that your product demo converts booth visitors into meaningful conversations
- Generate at least 3 qualified meetings from a single trade show
- Collect enough data to decide whether to invest in repeatable trade show operations

## Leading Indicators

- Pre-show outreach to target attendees gets >=20% reply rate (right audience, right show)
- At least 30% of booth conversations result in a demo (messaging resonates)
- Interest level distribution skews toward 3+ (audience is solution-aware, not just browsing)
- At least 2 people book a meeting on-site via Cal.com QR code (product-market signal)

## Instructions

### 1. Select the right trade show

Run the `event-scouting` drill to identify a trade show worth testing. Score candidate shows on:

- **ICP density**: How many published attendees, speakers, and exhibitors match your ICP? Use Clay to cross-reference the attendee list against your firmographic criteria. A show where >=20% of attendees match your ICP is worth the investment.
- **Show size**: Sweet spot for a first show is 500-3,000 attendees. Smaller shows mean too few prospects. Larger shows mean more competition for attention and higher booth costs.
- **Booth cost**: For a smoke test, target shows with booth packages under $5,000. Many regional industry events offer 10x10 booths for $1,500-3,000.
- **Timing**: Choose a show 4-8 weeks out. You need enough lead time for pre-show outreach but not so far out that you lose momentum.

**Human action required:** Final show selection and booth booking. The agent researches and scores shows; you decide and purchase.

### 2. Define your booth ICP and demo strategy

Run the `icp-definition` drill to document who you want to attract at the booth. Then design your demo approach:

- Write a one-sentence booth hook: the problem you solve, stated in terms the visitor recognizes. This goes on your booth signage and is the opening line for every conversation.
- Prepare 3 demo paths (60-second elevator, 3-minute guided, 10-minute deep dive) as defined in the the trade show booth operations workflow (see instructions below) drill. Each path should address a specific ICP pain point and end with a clear next step.
- Define your qualification criteria: what makes someone a Tier 1 (hot) vs Tier 2 (warm) vs Tier 3 (curious) lead? Write it down so every booth staff member applies the same standard.

### 3. Prepare booth infrastructure

Run the the trade show booth operations workflow (see instructions below) drill to set up:

- **Pre-show target list**: Extract the attendee list, enrich with Clay, and identify the top 25-50 ICP-match targets. Send personal outreach inviting them to the booth.
- **Lead capture**: Create a mobile-friendly Tally form for booth staff to log every conversation. Fields: name, email, company, title, interest level (1-5), demo path given, key pain point, agreed next step, notes.
- **Meeting booking**: Generate a Cal.com QR code for on-site meeting booking. Print and display at the booth. Save on every staff member's phone.
- **Demo environment**: Load product on 2+ devices. Test offline functionality. Prepare backup screenshots in case WiFi fails.

**Human action required:** Booth design, material shipping, travel booking. The agent handles targeting, forms, and demo prep.

### 4. Execute at the show

**Human action required:** You and your team work the booth.

Follow the execution framework from the the trade show booth operations workflow (see instructions below) drill:

- Station a qualifier at the booth entrance. Their job: greet, ask one qualifying question, and route to the right demo path or politely disengage.
- Demo-givers run the appropriate demo path based on the visitor's pain point.
- Log every conversation in the Tally form within 5 minutes of it ending. Do not batch at end of day.
- Between traffic peaks, proactively seek out pre-identified targets on the show floor.
- At end of each day, run the same-day lead import from the the trade show booth operations workflow (see instructions below) drill: sync Tally form submissions and badge scan exports to Attio.

### 5. Execute basic follow-up (within 48 hours)

This is a smoke test — follow-up is manual, not automated:

- **Tier 1 leads (interest 4-5)**: Personal email from the booth staff member who spoke with them. Reference the specific conversation, share something relevant (case study, one-pager), include Cal.com link. Send within 24 hours.
- **Tier 2 leads (interest 3)**: Email within 48 hours. Reference the show and their interest area. Share a resource. Offer to continue the conversation.
- **Tier 3+ leads (interest 1-2)**: LinkedIn connection request only. Add to general nurture list.

Log all follow-up actions in Attio. Tag contacts with follow-up status.

### 6. Evaluate against the threshold

Run the `threshold-engine` drill to measure:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Booth conversations | >=50 | Count of Tally form submissions |
| Demos given | >=10 | Tally submissions where demo_path is not "none" |
| Meetings booked | >=3 | Cal.com bookings + manually scheduled meetings within 14 days |

**PASS**: All three metrics met. Proceed to Baseline. The trade show motion works for your ICP — now add automation and measurement.

**FAIL**: Diagnose which metric missed:
- Low booth conversations (<50): Wrong show (low ICP density), poor booth location, or weak booth signage. Try a different show or negotiate a better booth spot.
- Low demos (<10): Qualification too tight, or booth hook not compelling. Loosen criteria or rewrite the opening line.
- Low meetings (<3): Demos are good but CTA is weak. Review the meeting ask — are you offering clear value for the follow-up meeting?

## Time Estimate

- Show selection and research: 4 hours
- ICP and demo strategy: 2 hours
- Pre-show target research and outreach: 4 hours
- Booth infrastructure setup (forms, Cal.com, demo prep): 3 hours
- Show execution: included in show hours (agent prep, not agent execution)
- Same-day lead import: 1 hour per day x 2 days = 2 hours
- Follow-up emails and logging: 3 hours
- Threshold evaluation: 2 hours
- **Total: ~20 hours over 3 weeks** (excludes travel and show-floor time, which are human hours)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Attendee enrichment + ICP scoring | $185/mo Launch (2,500 credits) — [clay.com/pricing](https://www.clay.com/pricing) |
| Tally | Booth lead capture form | Free tier: unlimited forms and submissions — [tally.so/pricing](https://tally.so/pricing) |
| Cal.com | Meeting booking QR code | Free tier: 1 user, unlimited event types — [cal.com/pricing](https://cal.com/pricing) |
| Attio | Lead tracking + deal creation | Free tier: up to 3 users — [attio.com](https://attio.com) |

**Estimated play-specific cost at Smoke: $185/mo** (Clay for pre-show enrichment; everything else is free tier)

Note: Booth rental, travel, and materials are show-specific costs not included above. Budget $2,000-5,000 for a first trade show (booth + travel for 2 people).

## Drills Referenced

- `icp-definition` — define who you want to attract at the booth and what pain points to address
- `event-scouting` — research and score candidate trade shows by ICP density, size, and cost
- the trade show booth operations workflow (see instructions below) — pre-show target research, lead capture setup, demo prep, and show-day execution
- `threshold-engine` — evaluate pass/fail against conversation, demo, and meeting targets
