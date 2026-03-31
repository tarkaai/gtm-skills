---
name: workshop-series-educational-smoke
description: >
  Workshop Series — Smoke Test. Run one educational workshop (20-30 attendees)
  teaching a skill at the intersection of your expertise and your ICP's pain
  points. Attendees practice hands-on with your product or framework. Validate
  that you can drive registrations, achieve a viable show rate, and generate
  qualified leads from a single session.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events, Content"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=15 registrations, >=40% show rate, >=3 qualified leads from first workshop"
kpis: ["Registrations", "Show rate", "Exercise completion rate", "Qualified leads"]
slug: "workshop-series-educational"
install: "npx gtm-skills add marketing/solution-aware/workshop-series-educational"
drills:
  - icp-definition
  - threshold-engine
---

# Workshop Series — Smoke Test

> **Stage:** Marketing > SolutionAware | **Motion:** MicroEvents | **Channels:** Events, Content

## Outcomes

- Confirm that your target audience will register for a hands-on workshop on your chosen topic
- Achieve a show rate that proves registrant commitment (>=40% -- workshops attract more committed attendees than webinars)
- Get at least 60% of attendees to attempt the hands-on exercise
- Generate at least 3 qualified leads (attendees who request follow-up or book a call) within 2 weeks of the event
- Validate the topic-exercise-audience fit before investing in automation or recurring events

## Leading Indicators

- Registration page conversion rate >20% from direct traffic
- Registrations reach 15+ at least 3 days before the event
- At least 60% of attendees attempt the hands-on exercise
- At least 3 attendees ask questions or request help during exercises
- At least 2 attendees click the post-event CTA (book a call, start a trial, request a review session)

## Instructions

### 1. Define your workshop ICP and topic

Run the `icp-definition` drill to document who should attend. Then select a topic that meets four criteria: (a) it addresses a top-3 pain point for your ICP, (b) you have unique expertise or tooling for this skill, (c) attendees can practice the skill during the session using your product or a related framework, (d) completing the exercise creates a natural bridge to a deeper conversation about your product. Write a one-sentence outcome statement: "After this workshop, you will have built [specific deliverable]."

Choose a difficulty level (beginner, intermediate, or advanced) based on your ICP's current skill level. Beginner workshops attract the widest audience. Intermediate workshops attract higher-intent prospects.

### 2. Design the workshop curriculum

Run the the workshop pipeline workflow (see instructions below) drill to structure the session. Build a 60-90 minute workshop:

- **Introduction (10 min)**: Context on why this skill matters. Hook with a stat or problem statement relevant to the ICP.
- **Teaching block 1 (15 min)**: Core concept explanation with examples.
- **Hands-on exercise 1 (15 min)**: Attendees practice the concept. Provide step-by-step instructions. If using your product, have a sandbox or free-tier setup ready.
- **Teaching block 2 (15 min)**: Advanced technique or second concept building on exercise 1.
- **Hands-on exercise 2 (15 min)**: More complex application combining both concepts.
- **Wrap-up and Q&A (10 min)**: Key takeaways, resources to continue learning, and CTA.

Prepare all materials in advance: slides, a workbook or cheat sheet attendees can keep, exercise instructions as a standalone document, and any sample data or templates needed for exercises.

### 3. Set up the workshop infrastructure

Using the the workshop pipeline workflow (see instructions below) drill:

- Create a registration page with: outcome-focused headline ("Build [deliverable] in 60 minutes"), what attendees will learn (3 bullets), prerequisites (what to install or prepare), speaker bio, date/time with timezone, and a form collecting name, email, company, role, and skill level (beginner/intermediate/advanced).
- Set up a video platform: use Zoom free tier (100 participants, 40-min limit -- schedule as two consecutive meetings if needed) or Google Meet (no limit with Workspace). For recording, use Riverside ($19/mo Standard).
- Configure email confirmations and a prep sequence via Loops: confirmation with prerequisites on registration, reminder with setup instructions 1 day before, and a "starting in 1 hour" reminder with join link.
- Create an Attio list for registrants with fields: name, email, company, role, skill_level, registered_date, attended (boolean), exercise_completed (boolean), engaged (boolean).
- Cap attendance at 25-30 people. Larger groups make hands-on facilitation impossible.

### 4. Promote the workshop manually

**Human action required:** This is a smoke test -- promotion is manual, not automated.

- Send personal emails or LinkedIn messages to 30-50 people in your network who match the ICP. Emphasize the hands-on component: "You will leave with [specific deliverable], not just slides."
- Post on LinkedIn with a hook that leads with the skill gap, not the event. Example: "Most [ICP role] struggle with [skill X]. I'm running a 60-minute hands-on workshop where you will build [deliverable] from scratch. Only 25 spots."
- If you have an existing email list, send one targeted invitation via Loops to the most relevant segment.
- Mention prerequisites in every promotion touchpoint. This self-selects for higher-intent registrants and improves show rate.

### 5. Execute the workshop

**Human action required:** You deliver the content and facilitate exercises live.

- Start on time. Open with the outcome promise: "By the end of this session, you will have [deliverable]."
- Walk through exercises step by step. Share your screen. Pause frequently: "How is everyone doing? Anyone stuck?" Have a co-facilitator handle chat questions and troubleshoot technical issues while you teach.
- Monitor exercise completion. Ask attendees to share their progress in chat or via a quick poll when each exercise concludes.
- Encourage questions throughout, not just during Q&A. Workshop attendees expect interaction.
- End with a clear CTA: "If you want help applying what you built today to your specific [use case], book a 15-minute review session." Share the Cal.com link in chat and in the follow-up email.

### 6. Execute basic follow-up

Within 24 hours of the workshop:

- Send an email to attendees: recording link, slides, workbook, exercise materials, and the CTA link. Reference their participation: "You built [deliverable] during the session -- here are the files to keep iterating."
- Send an email to no-shows: recording link + exercise materials with "Follow along at your own pace" framing. Include the CTA.
- For attendees who completed exercises or asked questions, send a personal email or LinkedIn message referencing their specific work and offering a review session.

Log all follow-up actions in Attio. Tag attendees by engagement tier: exercise_completed, attended_only, no_show.

### 7. Evaluate against the threshold

Run the `threshold-engine` drill to measure:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Registrations | >=15 | Count of Attio registrant list |
| Show rate | >=40% | Attendees / Registrations |
| Exercise completion rate | >=60% | Attendees who completed at least 1 exercise / Attendees |
| Qualified leads | >=3 | Attendees who booked a call, requested follow-up, or replied to nurture within 14 days |

**PASS**: All four metrics met. Proceed to Baseline. The topic, exercise format, and audience fit work -- now add automation and nurture sequences.

**FAIL**: Diagnose which metric missed:
- Low registrations (<15): Topic not compelling or prerequisite barrier too high. Try a different topic or lower the skill level. Remove prerequisites if they are blocking registrations.
- Low show rate (<40%): Prep emails not landing, or event time suboptimal. Check: did registrants receive and open the prep emails? Was the timezone convenient? Was the prerequisite clear enough that they felt ready?
- Low exercise completion (<60%): Exercises too difficult, instructions unclear, or insufficient facilitation. Simplify exercises, add more step-by-step guidance, or add a co-facilitator.
- Low qualified leads (<3): Attendees engaged but CTA not compelling. Review: is the CTA a natural next step from the exercise? Does the review session offer clear value beyond the workshop?

## Time Estimate

- ICP definition and topic selection: 30 minutes
- Curriculum design and materials preparation: 2 hours
- Registration page and infrastructure setup: 45 minutes
- Promotion (manual outreach): 30 minutes
- Workshop delivery: 75 minutes
- Follow-up emails and logging: 30 minutes
- Evaluation: 15 minutes
- **Total: ~6 hours over 1 week**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Zoom | Workshop platform | Free tier: 100 participants, 40-min limit |
| Google Meet | Workshop platform (alternative) | Free with Google Workspace |
| Riverside | Recording + production (optional) | $19/mo Standard -- [riverside.com/pricing](https://riverside.com/pricing) |
| Cal.com | Meeting booking CTA | Free: 1 user, unlimited event types -- [cal.com/pricing](https://cal.com/pricing) |
| Loops | Confirmation + prep + reminder emails | Free tier: 1,000 contacts, 4,000 sends/mo -- [loops.so/pricing](https://loops.so/pricing) |
| Attio | Registrant tracking | Free tier: up to 3 users -- [attio.com](https://attio.com) |

**Estimated play-specific cost at Smoke: $0-19/mo** (free if using Zoom/Meet + free tiers)

## Drills Referenced

- `icp-definition` -- define who should attend and what skills to teach
- the workshop pipeline workflow (see instructions below) -- design curriculum, set up registration, deliver the session, and execute follow-up
- `threshold-engine` -- evaluate pass/fail against registration, show rate, exercise completion, and qualified lead targets
