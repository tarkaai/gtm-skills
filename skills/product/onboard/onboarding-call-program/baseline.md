---
name: onboarding-call-program-baseline
description: >
  High-Touch Onboarding Calls — Baseline Run. Automate call routing, invitations,
  and post-call follow-up so onboarding calls run always-on for qualified new users.
  Prove the program sustains activation lift over 4 weeks.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Direct"
level: "Baseline Run"
time: "20 hours over 4 weeks"
outcome: "≥75% post-call activation rate sustained over 4 weeks; ≥15pp activation lift vs no-call cohort"
kpis: ["Call booking rate", "Call completion rate", "Post-call 7-day activation rate", "Activation lift vs no-call", "No-show rate"]
slug: "onboarding-call-program"
install: "npx gtm-skills add product/onboard/onboarding-call-program"
drills:
  - onboarding-call-routing
  - onboarding-call-follow-up
  - onboarding-sequence-design
---
# High-Touch Onboarding Calls — Baseline Run

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Direct

## Outcomes

Automate the end-to-end onboarding call pipeline: qualification, invitation, booking, post-call follow-up, and activation tracking. Run always-on for 4 weeks and prove the program delivers sustained activation lift over self-serve onboarding.

**Pass threshold:** ≥75% post-call 7-day activation rate sustained over 4 weeks AND ≥15 percentage point activation lift compared to eligible users who did not take a call.

## Leading Indicators

- Automated invitations reaching qualified users within 24 hours of signup
- Booking rate from invitations ≥25%
- No-show rate below 20%
- Follow-up emails sending within 1 hour of call completion
- Post-call nudge emails triggering for non-activated users at 48 hours

## Instructions

### 1. Automate call routing and invitations

Run the `onboarding-call-routing` drill to build the automated pipeline:

- Define qualification criteria in PostHog (plan type, company size, signup source, early engagement)
- Create the PostHog cohort "Onboarding Call Eligible"
- Build the in-app invitation via Intercom (banner with booking CTA, triggered for qualified users within 7 days of signup)
- Build the 3-email invitation sequence in Loops (Day 1, Day 3, Day 5 for users who have not booked)
- Connect Cal.com bookings to Attio via n8n (auto-create CRM records, update contact attributes)
- Set up no-show and cancellation handling (re-booking emails, 2-strike exit rule)

Track all routing events in PostHog: `onboarding_call_eligible`, `onboarding_call_invitation_clicked`, `onboarding_call_booked`, `onboarding_call_no_show`, `onboarding_call_cancelled`.

### 2. Automate post-call follow-up

Run the `onboarding-call-follow-up` drill to automate everything after the call ends:

- Trigger on Fireflies transcript completion webhook
- Extract action items, blockers, feature requests, and key quotes from the transcript
- Score the call automatically using the transcript data (speaking turn ratio, activation during call, feedback item count, expansion mentions)
- Log the structured summary, score, and action items to Attio
- Send a personalized follow-up email within 1 hour (generated from transcript, not a generic template)
- Start the 7-day activation monitoring: check PostHog daily, nudge at 48 hours if not activated, flag at 7 days if still not activated
- Aggregate team action items into a weekly insights report

### 3. Design the email sequence for non-call onboarding

Run the `onboarding-sequence-design` drill to build a parallel email onboarding sequence for users who do not take a call. This becomes the control group:

- Map the activation milestone and intermediate steps
- Write a 5-7 email sequence with behavioral triggers
- Set up audience segmentation in Loops
- Deploy the sequence for users who are NOT in the onboarding call cohort

This sequence ensures non-call users still receive onboarding support while creating a clean comparison group.

### 4. Run calls for 4 weeks

**Human action required:** Conduct the onboarding calls following the script from the Smoke level. At Baseline, the agent handles everything before and after the call. The human only needs to show up and run the 30-minute session.

Target: 15-30 calls over 4 weeks (depending on signup volume and qualification rate).

### 5. Evaluate against threshold

After 4 weeks:

1. Calculate the post-call 7-day activation rate across all call recipients
2. Calculate the 7-day activation rate for the no-call cohort (eligible users who did not book or complete a call)
3. Compare: is the lift ≥15 percentage points?
4. Check weekly consistency: did the activation rate hold steady each week, or did it decline?

**Pass:** ≥75% post-call activation rate AND ≥15pp lift vs no-call. Proceed to Scalable.
**Fail:** If activation rate is below 75%, analyze call scores and transcripts to identify the failure point. If lift vs no-call is below 15pp, the calls may not be adding enough value over self-serve onboarding — consider restructuring the call around a different activation milestone.

Also capture:
- Booking funnel conversion (eligible → invited → booked → completed)
- Most effective invitation channel (in-app vs email 1 vs email 2 vs email 3)
- Average call score trend (should be stable or improving)
- Top blockers and feature requests from call transcripts

## Time Estimate

- 6 hours: Routing automation setup (qualification rules, invitation flows, CRM sync)
- 4 hours: Follow-up automation setup (transcript processing, scoring, email templates, monitoring)
- 2 hours: Email sequence design for the control group
- 8 hours: Running 15-30 calls at 30 minutes each over 4 weeks (including prep time)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Cal.com | Scheduling onboarding calls | Free for 1 user; $15/user/mo for Teams ([cal.com/pricing](https://cal.com/pricing)) |
| Fireflies | Call recording, transcription, action item extraction | Pro: $10/user/mo billed annually ([fireflies.ai/pricing](https://fireflies.ai/pricing)) |
| Intercom | In-app call invitation messages | Essential: $29/seat/mo billed annually ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Invitation email sequence + follow-up emails | Free up to 1,000 contacts; $49/mo for 5,000 ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated play-specific cost:** $40-95/mo (Fireflies Pro + Loops free or starter; Intercom and Cal.com are standard stack or free tier)

## Drills Referenced

- `onboarding-call-routing` — automates qualification, multi-channel invitations, booking flow, and no-show handling
- `onboarding-call-follow-up` — automates transcript processing, call scoring, CRM logging, follow-up emails, and activation monitoring
- `onboarding-sequence-design` — builds the email-only onboarding sequence for the no-call control group
