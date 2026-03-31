---
name: hackathon-sponsorship-hosting-baseline
description: >
  Hackathon Sponsorship -- Baseline Run. Run 2 hackathons in 8 weeks with structured recruitment,
  tiered post-event nurture, and full funnel tracking. First always-on automation for participant
  segmentation and follow-up sequences.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events, Communities"
level: "Baseline Run"
time: "30 hours over 8 weeks"
outcome: ">=150 registrations and >=15 qualified leads across 2 hackathons in 8 weeks"
kpis: ["Registration-to-submission rate", "Qualified leads per hackathon", "Post-hackathon product adoption rate", "Cost per qualified lead"]
slug: "hackathon-sponsorship-hosting"
install: "npx gtm-skills add Marketing/SolutionAware/hackathon-sponsorship-hosting"
drills:
  - hackathon-challenge-pipeline
  - hackathon-attendee-nurture
  - threshold-engine
---

# Hackathon Sponsorship -- Baseline Run

> **Stage:** Marketing > SolutionAware | **Motion:** MicroEvents | **Channels:** Events, Communities

## Outcomes

Prove that hackathons produce repeatable qualified leads at a sustainable cost. Run 2 hackathons in 8 weeks (one every 4 weeks). Across both events, generate at least 150 total registrations and at least 15 qualified leads. Establish the post-hackathon nurture system so participant follow-up is automated rather than manual. Validate that different challenge themes can attract the same quality of developer audience.

## Leading Indicators

- First hackathon hits 75+ registrations with targeted recruitment via Clay-enriched outreach
- Second hackathon uses a different challenge theme but achieves similar or better registration numbers, proving theme versatility
- Automated nurture sequences trigger within 24 hours of event close for all participant tiers
- At least 3 participants from the first hackathon return for the second (repeat participation signal)
- Post-hackathon product adoption rate: at least 20% of submitters continue using the product 14 days after the event
- At least 2 meetings booked from Tier 1 (winner) or Tier 2 (strong submitter) nurture sequences per hackathon

## Instructions

### 1. Plan the 2-hackathon series

Design two hackathons with different challenge themes that showcase different product capabilities. This tests whether your hackathon appeal is broad or limited to one use case.

Run the `hackathon-challenge-pipeline` drill, Step 1, for both hackathons:

- **Hackathon 1** (Week 1-4): Use a challenge theme adjacent to what worked in the Smoke test. Iterate on the challenge design based on Smoke learnings: if participants found workarounds that avoided your product, tighten the requirements. If submissions were low quality, simplify the challenge.
- **Hackathon 2** (Week 5-8): Use a different challenge theme that exercises a different product feature set. This tests breadth of developer appeal.

For both, prepare updated quickstart guides, starter templates, and support channel infrastructure.

Estimated time: 4 hours (2 hours per challenge design).

### 2. Build structured recruitment with Clay enrichment

Expand recruitment beyond free channels. For each hackathon:

Using Clay (referenced in the `hackathon-challenge-pipeline` drill, Step 3):

1. Build a Clay table of developers matching the challenge theme:
   - Search for contributors to open-source projects in the relevant tech stack via `clay-people-search`
   - Find developers who posted about the problem domain on dev.to, LinkedIn, or Twitter in the last 90 days via `clay-claygent`
   - Filter for ICP match: company size, role, and technology stack
2. Enrich each developer with email and company data via `clay-enrichment-waterfall`
3. Import to Loops audience segment: "Hackathon {Slug} Prospects" via `loops-audience`
4. Send a personalized invite email that references why they specifically would enjoy this challenge (e.g., "You contributed to {repo} -- this challenge involves building something similar with {your product}")

Target: 200 enriched developer prospects per hackathon, supplementing the free channels from Smoke.

Continue using free channels (communities, social, existing list) alongside the targeted outreach. Track registration source attribution in PostHog.

Estimated time: 3 hours per hackathon (6 hours total).

### 3. Execute both hackathons

Run each hackathon following the full `hackathon-challenge-pipeline` drill (Steps 2-5):

- Virtual format, 1-week duration with live kickoff and demo day
- Mentor office hours via Cal.com (5 slots per hackathon)
- Full PostHog tracking: page views, registrations, kickoff attendance, submissions, API usage
- Judge submissions using the defined criteria

For the second hackathon, apply learnings from the first:
- If kickoff attendance was low, experiment with different timing or a shorter format
- If submissions were shallow, provide better starter templates or mid-event check-in support
- If certain recruitment channels outperformed, increase investment in those channels

**Human action required:** Host kickoffs, manage support channels, judge submissions, and host demo days for both hackathons.

Estimated time: 8 hours per hackathon (16 hours total).

### 4. Deploy automated post-hackathon nurture

Run the `hackathon-attendee-nurture` drill for each hackathon. This is the first always-on automation for this play:

Set up the automated tier segmentation and nurture sequences:

1. **Automated tier assignment**: Build an n8n workflow that, on hackathon close, pulls participant data from the platform, matches against submissions and API usage logs, and assigns each participant to Tier 1-5 in Attio.
2. **Automated sequence enrollment**: When a participant is tagged with their tier, automatically enroll them in the corresponding Loops nurture sequence.
3. **High-intent escalation**: When a Tier 1 or Tier 2 participant replies or books a meeting, automatically create a deal in Attio and notify the team.

For Hackathon 1, set up the automation manually (2 hours) and validate it works. For Hackathon 2, the automation should trigger without manual intervention.

Personalization for each tier:
- Winners: congratulations + co-marketing opportunity + developer advisory board invite
- Strong submitters: extended product access + tutorials for features they used
- Basic submitters: getting-started content for features they missed
- Registered-only: event recording + quickstart guide + invite to next hackathon
- Mentors/judges: thank you + partnership exploration

Estimated time: 4 hours (setup for first hackathon; runs automatically for second).

### 5. Track full funnel performance

Build PostHog tracking across both hackathons:

- Registration funnel: `hackathon_page_viewed` -> `hackathon_registered` -> `hackathon_kickoff_attended` -> `hackathon_submission_received`
- Nurture funnel: `hackathon_nurture_email_sent` -> `hackathon_nurture_email_opened` -> `hackathon_nurture_reply_received` -> `hackathon_nurture_meeting_booked`
- Product adoption: `hackathon_api_usage` -> `product_signup` -> `product_activated` -> `product_retained_14d`

Compare metrics between the two hackathons to identify what drove differences.

### 6. Evaluate against threshold

Run the `threshold-engine` drill to evaluate results against the pass threshold: >=150 registrations and >=15 qualified leads across 2 hackathons in 8 weeks.

A "qualified lead" at Baseline means: matches ICP, submitted a project using 3+ product features, AND either replied to nurture email, booked a meeting, or continued using the product 14 days post-event.

Also assess:
- Did the second hackathon perform as well as the first? If significantly worse, theme versatility may be limited.
- Is the automated nurture producing replies and meetings without manual intervention?
- What is the cost per qualified lead? (Total spend on prizes + Clay + any paid promotion) / qualified leads
- Are hackathon-sourced leads progressing through the sales pipeline?

If PASS, proceed to Scalable. If FAIL, review: Are the challenges compelling enough? Is the developer experience smooth enough for a hackathon? Are you reaching the right developer communities? Iterate and run a third hackathon before deciding.

## Time Estimate

- Challenge design for 2 hackathons: 4 hours
- Recruitment (Clay enrichment + outreach) for 2 hackathons: 6 hours
- Hackathon execution (kickoff, support, judging, demo day) x 2: 16 hours
- Nurture automation setup and validation: 4 hours

**Total: ~30 hours over 8 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Devpost or Luma | Hackathon platform -- registration, submissions, judging | Devpost: Free. Luma: Free tier or Plus $59/mo. [devpost.com](https://devpost.com) / [luma.com/pricing](https://luma.com/pricing) |
| Clay | Developer prospect enrichment for targeted recruitment | Launch: $185/mo (2,500 credits). [clay.com/pricing](https://www.clay.com/pricing) |
| Attio | CRM -- participant records, deal tracking, tier segmentation | Standard stack (excluded) |
| PostHog | Full-funnel tracking: registration, engagement, nurture, adoption | Standard stack (excluded) |
| Loops | Nurture sequences and recruitment broadcasts | Standard stack (excluded) |
| n8n | Automation -- tier assignment, sequence triggers, deal creation | Standard stack (excluded) |
| Cal.com | Mentor office hours booking | Standard stack (excluded) |
| Anthropic API | Personalized nurture content generation | ~$10-20/mo at Baseline volume. [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Play-specific cost: ~$250-350/mo** (Clay $185 + prizes ~$500-1,000/event amortized + Anthropic ~$15)

## Drills Referenced

- `hackathon-challenge-pipeline` -- complete hackathon lifecycle from challenge design through judging and lead capture
- `hackathon-attendee-nurture` -- tiered post-hackathon nurture with automated segmentation and sequence enrollment
- `threshold-engine` -- evaluates results against pass/fail threshold and recommends next action
