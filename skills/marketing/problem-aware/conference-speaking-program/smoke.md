---
name: conference-speaking-program-smoke
description: >
  Conference Speaking — Smoke Test. Submit proposals to 5 conferences, land 1 speaking slot,
  and capture at least 10 leads from the talk. Manual CFP discovery and proposal writing
  with agent assistance. No always-on automation.
stage: "Marketing > ProblemAware"
motion: "MicroEvents"
channels: "Events, Social"
level: "Smoke Test"
time: "8 hours over 3 weeks"
outcome: "≥1 accepted talk and ≥10 attributed leads from the delivered talk"
kpis: ["CFP submissions sent", "Acceptance rate", "Leads captured per talk", "QR code scan rate"]
slug: "conference-speaking-program"
install: "npx gtm-skills add marketing/problem-aware/conference-speaking-program"
drills:
  - conference-cfp-pipeline
  - threshold-engine
---

# Conference Speaking — Smoke Test

> **Stage:** Marketing → ProblemAware | **Motion:** MicroEvents | **Channels:** Events, Social

## Outcomes

Land 1 speaking slot at an industry conference where your ICP attends. Deliver the talk and capture at least 10 leads attributed to that specific talk. This proves that conference speaking generates pipeline for your business before investing in automation.

## Leading Indicators

- 5+ CFP submissions sent within the first week
- At least 2 CFPs score 60+ on the ICP-audience-density metric from the CFP pipeline scoring
- Proposal turnaround time under 2 hours per CFP (agent-assisted drafting is fast enough)
- At least 1 acceptance notification received within 3 weeks

## Instructions

### 1. Discover and score open CFPs

Run the `conference-cfp-pipeline` drill, steps 1-2 only:

1. Seed a Clay table with your talk topic keywords (3-5 topics aligned to your ICP's problems) and target regions
2. Run Claygent to scrape CFP aggregators: Papercall, Sessionize, confs.tech, cfpland.com, dev.events
3. Parse results into individual CFP rows with: conference name, date, CFP deadline, location, audience size, topics accepted
4. Filter out CFPs with deadlines < 7 days away and conferences with estimated audience < 50
5. Score each CFP on: ICP audience density (40%), topic fit (25%), audience size (15%), travel logistics (10%), conference reputation (10%)
6. Push scored CFPs to Attio as a "CFP Pipeline" list

Target: identify at least 8 open CFPs scoring 50+.

### 2. Draft talk proposals

For the top 5 scored CFPs, draft talk proposals. Use the `talk-proposal-generation` fundamental via Claude API:

1. Provide: conference name, audience description, accepted topics, talk format, your expertise, and 3-5 content pillars
2. Claude generates: title (under 80 chars), abstract (200-300 words), outline (5-7 sections), key takeaways (3), target audience, and speaker positioning
3. Review each proposal for specificity -- reject any that use vague phrases like "best practices" or "lessons learned" without concrete examples
4. Customize the "Why me" section with genuine personal experience

**Human action required:** Review and edit each proposal. The agent drafts but the speaker must ensure the proposal reflects talks they can actually deliver.

### 3. Submit proposals

For each of the 5 proposals:

1. Submit via the CFP platform (Papercall, Sessionize, Google Form, or email)
2. Log the submission in Attio: conference name, talk title, submission date, CFP deadline, expected notification date
3. Fire PostHog event `speaking_cfp_submitted` with properties: `conference_name`, `talk_title`, `conference_date`, `audience_size`, `cfp_score`

### 4. Prepare lead capture for accepted talk

When a talk is accepted:

1. Update Attio record status to "accepted"
2. Fire `speaking_cfp_accepted` in PostHog
3. Create a companion resource page with: talk key takeaways, Cal.com booking link (UTM-tagged), and email capture form
4. Generate a QR code pointing to the companion page: `https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={encoded_companion_url}`
5. Add the QR code to the final slide of the talk deck

**Human action required:** Build and deliver the talk. The agent prepares all lead capture infrastructure but the speaker presents.

### 5. Capture leads and measure

After delivering the talk:

1. Fire `speaking_talk_delivered` in PostHog with: `conference_name`, `talk_title`, `estimated_audience`, `talk_date`
2. Monitor companion page visits (attributed via UTM), Cal.com bookings, and email signups
3. For each lead captured, create an Attio contact tagged `source:conference-talk`, `conference:{name}`
4. After 14 days, count total attributed leads across all channels

### 6. Evaluate against threshold

Run the `threshold-engine` drill:

- **Pass threshold:** ≥1 accepted talk AND ≥10 attributed leads from that talk
- **Pass:** Document which conference type, talk topic, and lead capture channel worked best. Proceed to Baseline.
- **Marginal pass (1 talk, 5-9 leads):** Lead capture infrastructure may need improvement. Check QR code visibility, companion page conversion rate, and follow-up timeliness. Re-run at Smoke.
- **Fail (<1 acceptance from 5 submissions):** Review proposal quality. Are you targeting the right conferences? Is the topic specific enough? Get feedback from conference organizers if possible. Adjust and re-submit.

## Time Estimate

- 2 hours: CFP discovery and scoring (agent does 90% of this)
- 2 hours: Proposal drafting and review (agent drafts, human reviews)
- 1 hour: Submission and tracking setup
- 1 hour: Lead capture infrastructure (companion page, QR code, Cal.com link)
- 2 hours: Post-talk lead monitoring and attribution (spread over 2 weeks after the talk)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | CFP discovery via Claygent, conference scoring | Launch: $185/mo; Free tier: 100 credits |
| Sessionize | Speaker profile management, CFP submissions | Free for speakers; $499/event for organizers |
| Papercall | CFP discovery and submission | Free for speakers |
| Cal.com | Post-talk booking links | Free tier available |
| Loops | Email capture on companion page | Free up to 1,000 contacts |
| Anthropic API | Talk proposal generation | ~$0.09 per CFP (3 variants) |
| confs.tech / dev.events / cfpland.com | CFP aggregator sources | Free |

**Total Smoke budget:** Free (all speaker-side tools have free tiers)

## Drills Referenced

- `conference-cfp-pipeline` — discovers open CFPs, scores them for ICP fit, drafts proposals, and tracks submissions
- `threshold-engine` — evaluates results against pass/fail criteria and recommends next action
