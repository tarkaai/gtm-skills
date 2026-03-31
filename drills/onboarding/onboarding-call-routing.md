---
name: onboarding-call-routing
description: Automatically identify high-value signups, trigger onboarding call invitations via in-app and email, and route bookings to the right team member
category: Onboarding
tools:
  - PostHog
  - Intercom
  - Loops
  - Cal.com
  - n8n
  - Attio
fundamentals:
  - posthog-cohorts
  - posthog-custom-events
  - intercom-in-app-messages
  - loops-sequences
  - calcom-event-types
  - calcom-booking-links
  - calcom-inline-embed
  - calcom-crm-sync
  - n8n-triggers
  - n8n-workflow-basics
  - attio-contacts
  - attio-lists
---

# Onboarding Call Routing

This drill builds the automated pipeline that detects which new users should receive an onboarding call invitation, delivers the invitation through in-app and email channels, and routes the booking to the right person. It connects signup data (PostHog + Attio) to scheduling (Cal.com) with automation (n8n).

## Prerequisites

- PostHog tracking signup events and user properties (plan type, company size, signup source)
- Cal.com account with an "Onboarding Call" event type configured (see `calcom-event-types`)
- Intercom installed in the product for in-app messaging
- Loops configured for lifecycle emails
- n8n instance running
- Attio CRM with contact records syncing from your product

## Steps

### 1. Define the call qualification criteria

Not every new user needs an onboarding call. Using `posthog-cohorts`, define the criteria for who gets invited. Start with criteria that predict high-value users:

| Signal | Source | Threshold | Weight |
|--------|--------|-----------|--------|
| Plan type | PostHog user property | Paid plan or trial of paid plan | Required |
| Company size | Attio enrichment | 10+ employees | High |
| Signup source | PostHog UTM | Demo request, sales referral, partner referral | High |
| Role | PostHog user property or signup form | Manager+, founder, decision-maker | Medium |
| Early engagement | PostHog events | Completed 2+ onboarding steps within 24 hours | Medium |

Create a PostHog cohort called "Onboarding Call Eligible" that matches users meeting the required signal plus at least 1 high-weight signal.

At Smoke level, skip automated qualification and manually select 10-20 users. At Baseline and above, automate this criteria.

### 2. Set up the Cal.com onboarding call event type

Using `calcom-event-types`, create a dedicated event type:

- Title: "1:1 Onboarding Call"
- Duration: 30 minutes
- Buffer: 15 minutes before and after
- Availability: Match your team's onboarding call hours (recommend 4-6 slots per day)
- Booking form questions: "What is your primary goal with [product]?", "Have you started using [product] yet?"
- Minimum notice: 4 hours (onboarding calls should be fast to schedule)
- Max advance booking: 7 days

Using `calcom-booking-links`, generate the booking link with UTM tracking: `cal.com/team/onboarding?utm_source=onboarding-routing&utm_medium=in-app`

### 3. Build the in-app call invitation

Using `intercom-in-app-messages`, create a targeted in-app message that appears for qualified users:

- **Trigger:** User matches "Onboarding Call Eligible" cohort AND has not booked a call AND signed up within last 7 days
- **Format:** Banner or chat-style message, not a modal (less intrusive)
- **Copy:** "Welcome to [product]. Want to get set up in 30 minutes with a personalized onboarding call? We will walk through your specific use case." CTA: "Book your call" linking to the Cal.com booking page.
- **Frequency:** Show once per session, max 3 times total. After 3 dismissals, stop showing.
- **Dismissal tracking:** Fire a PostHog event `onboarding_call_invitation_dismissed` on dismiss. Fire `onboarding_call_invitation_clicked` on CTA click.

### 4. Build the email invitation sequence

Using `loops-sequences`, create a 3-email sequence for qualified users who have not booked via the in-app message:

**Email 1 (Day 1 after qualification, if no booking):**
- Subject: "Your personal onboarding call is ready"
- Body: Brief explanation of what happens on the call (walkthrough of their use case, answers to questions, help reaching first milestone). Include the Cal.com inline embed or booking link.
- CTA: "Pick a time that works"

**Email 2 (Day 3, if still no booking):**
- Subject: "Quick question about getting started"
- Body: Ask if they are stuck or need help. Mention a specific feature relevant to their plan type. Include the booking link.
- CTA: "Let us help you get set up"

**Email 3 (Day 5, if still no booking):**
- Subject: "Last chance for your onboarding call"
- Body: Social proof (X% of users who take the onboarding call activate within the first week). Final CTA.
- CTA: "Book before your slot fills up"

Exit condition: User books a call (detected via Cal.com webhook) or completes the activation milestone (detected via PostHog).

### 5. Connect the booking to CRM

Using `calcom-crm-sync`, build an n8n workflow triggered by the Cal.com `BOOKING_CREATED` webhook:

1. Parse the booking payload: user email, selected time, answers to booking form questions
2. Look up the user in Attio using `attio-contacts`
3. Update the Attio contact record: set `onboarding_call_booked` = true, `onboarding_call_date` = scheduled time
4. Add the contact to an Attio list called "Onboarding Calls This Week" using `attio-lists`
5. Fire a PostHog event: `onboarding_call_booked` with properties: `booking_source` (in-app vs email vs direct), `days_since_signup`, `user_plan`
6. Trigger the pre-call prep (see `onboarding-call-script` drill, Step 6)

### 6. Handle no-shows and cancellations

Build an n8n workflow triggered by Cal.com `BOOKING_CANCELLED` and `BOOKING_NO_SHOW` webhooks (use `n8n-triggers`):

- **Cancellation:** Update Attio record. Send a single re-booking email via Loops: "No worries. Here is a new link to reschedule."
- **No-show:** Update Attio record. Wait 2 hours, then send: "We missed you. Want to reschedule?" Include a fresh booking link.
- **Track in PostHog:** `onboarding_call_cancelled` or `onboarding_call_no_show` events.
- After 2 no-shows or cancellations, stop inviting and add to Attio list "Call Routing - Declined" for email-only onboarding.

### 7. Route to team members (Scalable level)

At scale with multiple team members running calls, use Cal.com round-robin assignment:
- Configure a Cal.com team event type with round-robin scheduling across onboarding team members
- Optionally route based on user attributes: enterprise users to senior team members, specific use cases to product specialists
- Track which team member handles which calls for performance comparison

## Output

- Automated qualification of new signups for onboarding calls
- Multi-channel invitation (in-app + email) with appropriate cadence
- Cal.com booking flow connected to CRM
- No-show and cancellation handling
- PostHog event tracking for the full routing funnel
- Team routing logic for scale
