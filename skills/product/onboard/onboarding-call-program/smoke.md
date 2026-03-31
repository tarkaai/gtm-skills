---
name: onboarding-call-program-smoke
description: >
  High-Touch Onboarding Calls — Smoke Test. Run 10-20 structured 1:1 onboarding calls
  with new users to validate that personal call-based onboarding accelerates activation
  and surfaces actionable product feedback.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Direct"
level: "Smoke Test"
time: "8 hours over 2 weeks"
outcome: "≥70% of call recipients reach activation milestone within 7 days"
kpis: ["Call booking rate", "Call completion rate", "Post-call 7-day activation rate", "Average call score"]
slug: "onboarding-call-program"
install: "npx gtm-skills add product/onboard/onboarding-call-program"
drills:
  - meeting-booking-flow
  - onboarding-call-script
---
# High-Touch Onboarding Calls — Smoke Test

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Direct

## Outcomes

Run 10-20 structured 1:1 onboarding calls with new users. Prove that a personal call accelerates activation compared to self-serve onboarding. Collect qualitative feedback on product friction.

**Pass threshold:** ≥70% of users who complete an onboarding call reach the activation milestone within 7 days.

## Leading Indicators

- Users are booking calls when invited (booking rate ≥30%)
- Call no-show rate stays below 25%
- Users complete the activation milestone *during* the call (≥40%)
- Call scores average ≥7/12 (engaged users providing useful feedback)

## Instructions

### 1. Set up scheduling

Run the `meeting-booking-flow` drill to configure Cal.com for onboarding calls:

- Create a "1:1 Onboarding Call" event type (30 minutes, 15-minute buffer)
- Add booking form questions: "What is your primary goal with [product]?" and "Have you started using [product] yet?"
- Connect Cal.com to Attio via an n8n webhook so each booking creates or updates a CRM record
- Add PostHog tracking for the `meeting_booked` event

**Human action required:** Choose your availability windows. Recommend offering 4-6 slots per day during business hours for the 2-week test period.

### 2. Design the call structure

Run the `onboarding-call-script` drill to create the complete call framework:

- Build the 30-minute timed agenda (3 min welcome, 7 min discovery, 12 min guided walkthrough, 5 min Q&A, 3 min close)
- Write the 5-7 discovery questions with scoring rubrics
- Map the guided walkthrough to your product's activation milestone
- Build the post-call scoring rubric (4-12 scale across activation progress, engagement, feedback quality, expansion signal)
- Create the pre-call prep checklist

### 3. Set up call recording and transcription

Configure Fireflies to auto-join onboarding calls:

- Connect Fireflies to your calendar
- Set it to auto-join meetings with "Onboarding" in the title
- Configure the AI note-taker display name
- Set up the Fireflies webhook for transcript completion

### 4. Manually select and invite 10-20 users

At Smoke level, do not automate qualification. Manually identify 10-20 recent signups who:

- Signed up in the last 7 days
- Have not yet reached the activation milestone
- Are on a paid plan or trial

**Human action required:** Send each user a personal email with the Cal.com booking link. Use a simple template: "I am [name] from [product]. I would like to help you get set up with a 30-minute onboarding call. Pick a time: [Cal.com link]."

### 5. Run the calls and score each one

For each call:

1. Run the pre-call prep checklist from the `onboarding-call-script` drill (pull usage data from PostHog, CRM record from Attio)
2. **Human action required:** Conduct the call following the structured agenda
3. After the call, retrieve the Fireflies transcript and extract action items
4. Score the call using the post-call scoring rubric
5. Log the score, summary, and action items in Attio
6. Send a follow-up email within 1 hour with the recap and next steps

### 6. Track post-call activation

For each user who completed a call:

- Monitor PostHog for 7 days: did they fire the activation milestone event?
- If not activated after 48 hours, send one nudge email referencing the specific action item from the call
- Record the days-to-activation in Attio

### 7. Evaluate against threshold

After all 10-20 calls are complete and the 7-day monitoring window has passed:

- Calculate: what percentage of users who completed a call reached the activation milestone within 7 days?
- If ≥70%: PASS. Proceed to Baseline.
- If <70%: Analyze call scores and transcripts. Identify the top blocker. Revise the call script and run another batch of 10 calls.

Also capture:
- Average call score (target: ≥7/12)
- Most common blockers surfaced during calls
- Feature requests and product feedback themes
- Whether activation happened during the call vs after

## Time Estimate

- 2 hours: Cal.com setup, call script design, Fireflies configuration
- 5 hours: Running 10-20 calls at 30 minutes each (including prep and follow-up)
- 1 hour: Data analysis and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Cal.com | Scheduling onboarding calls | Free for 1 user ([cal.com/pricing](https://cal.com/pricing)) |
| Fireflies | Call recording and transcription | Free: 800 min/mo; Pro: $10/user/mo annually ([fireflies.ai/pricing](https://fireflies.ai/pricing)) |

**Estimated play-specific cost:** Free (Cal.com free plan + Fireflies free tier covers 10-20 calls)

## Drills Referenced

- `meeting-booking-flow` — sets up Cal.com scheduling, CRM sync, and booking analytics
- `onboarding-call-script` — designs the call agenda, discovery questions, walkthrough framework, and scoring rubric
