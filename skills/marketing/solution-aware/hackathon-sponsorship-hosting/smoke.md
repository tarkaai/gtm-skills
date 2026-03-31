---
name: hackathon-sponsorship-hosting-smoke
description: >
  Hackathon Sponsorship -- Smoke Test. Host or sponsor a single small hackathon to validate that
  developer-focused challenges generate qualified technical leads who engage meaningfully with your
  product. No always-on automation. Agent helps plan and prepare; human executes.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events, Communities"
level: "Smoke Test"
time: "12 hours over 2 weeks"
outcome: ">=50 developer registrations and >=5 qualified leads from first hackathon"
kpis: ["Registration count", "Submission rate", "Qualified leads generated", "Product API usage depth"]
slug: "hackathon-sponsorship-hosting"
install: "npx gtm-skills add Marketing/SolutionAware/hackathon-sponsorship-hosting"
drills:
  - hackathon-challenge-pipeline
  - threshold-engine
---

# Hackathon Sponsorship -- Smoke Test

> **Stage:** Marketing > SolutionAware | **Motion:** MicroEvents | **Channels:** Events, Communities

## Outcomes

Prove that hackathons generate qualified developer leads who actually engage with your product. After the first hackathon, at least 50 developers should register, at least 40% should submit a project, and at least 5 participants should qualify as leads (match ICP, used 3+ product features, and responded to follow-up). The smoke test validates that your product has enough API surface area and developer appeal to power a hackathon challenge before investing in automation.

## Leading Indicators

- Challenge document drafted and reviewed within first 2 days -- the challenge is specific enough to force product usage but open enough to inspire creative solutions
- At least 30 registrations within 1 week of announcement, without paid promotion
- At least 3 participants book mentor office hours during the event, indicating they are building something substantive
- At least 1 submission uses your product in a way you did not anticipate, proving developers see value beyond your assumed use cases
- Post-event, at least 2 participants reply to the follow-up email expressing interest in continued product usage

## Instructions

### 1. Design the hackathon challenge

Run the `hackathon-challenge-pipeline` drill, Step 1 only. Define a challenge that:

- Forces participants to use your product's core API or platform for a meaningful part of their project (not a superficial integration)
- Targets a problem domain your ICP cares about (e.g., if you sell a data API, the challenge should involve building something that processes real data, not a toy demo)
- Is achievable in 48 hours for a team of 2-4 developers with no prior exposure to your product
- Includes clear judging criteria weighted toward product usage depth (30% technical implementation)

Prepare supporting resources:
- Quickstart guide tailored to the hackathon (not your standard docs -- a streamlined 15-minute path to "hello world")
- 1-2 starter templates on GitHub so participants spend time building, not configuring
- A dedicated support channel (Discord server or Slack channel) with you available during event hours

**Human action required:** You design the challenge. The agent can research comparable hackathons and suggest challenge structures, but the human decides what product capabilities to showcase.

Estimated time: 3 hours.

### 2. Choose format and platform

For the smoke test, run a **virtual hackathon** to maximize reach with minimal logistics:

- **Duration**: 1 week asynchronous (participants build on their own schedule) with a live kickoff and live demo day
- **Platform**: Devpost (free for organizers, handles registration, team formation, and submission collection) or Luma (free tier, good for developer events)
- **Prize budget**: $500-1,000 total. Structure: 1st place $300, 2nd place $150, 3rd place $50. All submitters get extended free-tier product access.

Set up the event on the chosen platform. Follow `hackathon-challenge-pipeline` drill, Step 2.

Track registration with PostHog: fire `hackathon_page_viewed` and `hackathon_registered` events.

Estimated time: 1 hour.

### 3. Recruit participants through free channels

For the smoke test, use only free recruitment channels to test organic demand:

- Post the hackathon in 3-5 developer communities where your ICP hangs out (relevant Discord servers, Slack groups, subreddits like r/SideProject or domain-specific subs)
- Share on Hacker News (Show HN) and dev.to
- Post on your company's LinkedIn and Twitter
- Send a broadcast email to your existing developer contact list via Loops
- Ask your team to share personally on LinkedIn

Track which channel each registration comes from (UTM parameters on the registration link). Add all registrants to Attio with tag `source: hackathon-smoke-{slug}`.

Target: 50+ registrations from free channels. If you cannot reach 50 without paid promotion, that is a signal about organic developer demand for your product.

Estimated time: 2 hours.

### 4. Execute the hackathon

Follow `hackathon-challenge-pipeline` drill, Steps 4 and 5:

- Host a 30-minute live kickoff: introduce the challenge, walk through the quickstart guide, demo a sample project, and answer questions
- Keep the support channel active during the event. Respond to questions within 2 hours during business hours.
- Set up 3-5 mentor office hours slots via Cal.com (30 minutes each) for participants who want live help
- Send a 48-hour warning and a 24-hour warning before the submission deadline
- Collect submissions through the platform. Review and score each submission using the judging criteria.
- Host a 30-minute live demo day where the top 3-5 teams present. Record this for content.

**Human action required:** You run the kickoff, answer questions in the support channel, judge submissions, and host demo day. The agent prepares materials, sends reminders, and processes data.

Estimated time: 4 hours (spread across the event week).

### 5. Process results and follow up

After the hackathon closes:

- Extract all participant data from the platform
- Score each participant's product usage depth by checking API logs: how many endpoints did they call, how many features did they use, how much data did they process?
- Classify participants into tiers (see `hackathon-attendee-nurture` drill for tier definitions)
- Send a personal thank-you email to all submitters with: the demo day recording, winning project highlights, and an offer of extended free-tier access
- For the top 5-10 participants (winners + strong submitters): send a personal email referencing their specific project, offering a 1-on-1 call to discuss their use case

Track all follow-up engagement in Attio. Log in PostHog: `hackathon_submission_received`, `hackathon_api_usage`, `hackathon_followup_replied`.

Estimated time: 2 hours.

### 6. Evaluate against threshold

Run the `threshold-engine` drill to evaluate results against the pass threshold: >=50 developer registrations and >=5 qualified leads from first hackathon.

A "qualified lead" for this play means: matches ICP (developer role at a company in your target segment), submitted a project that used 3+ product features, AND responded to follow-up (replied to email or booked a call).

Also assess qualitatively:
- Did the challenge design force meaningful product usage, or did participants find workarounds that avoided your product?
- Was the submission quality high enough to demonstrate real interest, or were submissions low-effort?
- Did any participant express interest in using your product beyond the hackathon?
- Were the prize amounts and structure effective at motivating participation?

If PASS, proceed to Baseline. If FAIL, review: Was the challenge too hard or too easy? Were you recruiting in the wrong communities? Is your product's developer experience good enough to support a hackathon? Adjust and re-run.

## Time Estimate

- Challenge design and resource preparation: 3 hours
- Platform setup and registration configuration: 1 hour
- Participant recruitment (community posts, emails): 2 hours
- Event execution (kickoff, support, judging, demo day): 4 hours
- Post-event processing and follow-up: 2 hours

**Total: ~12 hours over 2 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Devpost | Hackathon platform -- registration, submissions, judging | Free for organizers. [devpost.com](https://devpost.com) |
| Luma | Event registration and communication (alternative to Devpost) | Free tier: unlimited events. Plus: $59/mo annual. [luma.com/pricing](https://luma.com/pricing) |
| Attio | CRM -- participant records, lead tracking | Standard stack (excluded from play budget) |
| PostHog | Event tracking for registration and engagement funnel | Standard stack (excluded from play budget) |
| Loops | Email broadcasts for recruitment and follow-up | Standard stack (excluded from play budget) |
| Cal.com | Mentor office hours booking | Standard stack (excluded from play budget) |
| Discord or Slack | Participant support channel during the event | Free |

**Play-specific cost: $500-1,000** (prize budget only; all tools are free tier)

## Drills Referenced

- `hackathon-challenge-pipeline` -- complete hackathon lifecycle from challenge design through judging and lead capture
- `threshold-engine` -- evaluates results against pass/fail threshold and recommends next action
