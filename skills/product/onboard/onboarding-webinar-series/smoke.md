---
name: onboarding-webinar-series-smoke
description: >
  Live Onboarding Webinars — Smoke Test. Run one pilot webinar for 10-30
  new users. Manually plan, promote, execute, and follow up. Measure whether
  attendees activate at a higher rate than non-attendees.
stage: "Product > Onboard"
motion: "MicroEvents"
channels: "Product, Email, Events"
level: "Smoke Test"
time: "6 hours over 2 weeks"
outcome: ">=50% attendee activation rate AND activation rate lift >10pp vs non-attendees"
kpis: ["Registration rate", "Show rate", "Attendee activation rate", "Activation lift vs control"]
slug: "onboarding-webinar-series"
install: "npx gtm-skills add product/onboard/onboarding-webinar-series"
drills:
  - webinar-pipeline
  - threshold-engine
---

# Live Onboarding Webinars — Smoke Test

> **Stage:** Product > Onboard | **Motion:** Lead Capture Surface | **Channels:** Product, Email, Events

## Outcomes

Run one pilot webinar teaching new users a core product workflow. Invite 30-50 recent signups, aim for 10-30 attendees. Measure whether live, guided walkthroughs with Q&A accelerate activation compared to users who onboard without a webinar. Pass threshold: >=50% of attendees reach activation within 7 days AND attendees activate at a rate >10 percentage points higher than a matched control group of non-attendees.

## Leading Indicators

- Registration rate above 30% of invited users within 5 days of the invite — confirms the topic and framing resonate
- Show rate above 40% of registrants — confirms timing and reminder cadence work
- At least 3 attendees ask a question or engage in chat during the session — confirms the content is relevant and the format encourages participation
- At least 1 attendee who was stuck pre-activation completes their activation action within 48 hours of attending

## Instructions

### 1. Plan the webinar using the webinar-pipeline drill

Run the `webinar-pipeline` drill. For this smoke test, focus on these specifics:

**Topic selection:** Choose a single workflow that maps directly to your product's activation metric. Do not run a feature tour — pick the one action that, when completed, predicts 30-day retention. Examples: "Build your first [core object] in 20 minutes", "Set up [key integration] live, with help."

**Format:** Workshop (30-45 minutes). The host walks through the workflow live, screen-sharing inside the product. Attendees follow along in their own accounts. Reserve the last 15 minutes for Q&A.

**Scheduling:** Set the date 7-10 days out. Pick a time when your signups are most active (check PostHog session data for peak usage hours). Create a Cal.com event type for the webinar using the `calcom-event-types` fundamental.

**Registration page:** Build a simple landing page or use Cal.com's booking page. Collect: name, email, company, biggest challenge with onboarding (free text). Track `webinar_page_viewed` and `webinar_registered` events in PostHog.

### 2. Invite recent signups

Query your product database or Attio for users who signed up in the last 14 days and have NOT yet reached activation. These are your target invitees — they need the help most.

Split the list:
- **Invite group (30-50 users):** Will receive the webinar invitation
- **Control group (30-50 users):** Will NOT receive any webinar invitation, will onboard through existing flows

Log group assignment as a PostHog person property: `onboarding_webinar_cohort: "invited"` or `"control"`.

Send the invitation email through Loops. Subject line should lead with the outcome, not the format: "Get [product] set up in 30 minutes — live walkthrough this [day]" not "Join our onboarding webinar."

Send 2 reminders: 2 days before and 1 hour before. Each reminder should re-sell the value.

### 3. Execute the webinar

**Human action required:** The host must deliver the webinar live. The agent cannot do this.

Before the session:
- Set up Riverside or Zoom for recording
- Prepare a 3-slide intro (max): who you are, what attendees will accomplish today, and the single CTA at the end
- Open the product in a clean demo account ready to walk through the workflow

During the session:
- Start on time. Open with the outcome: "By the end of this session, you will have [activation action] completed in your account."
- Walk through the workflow step-by-step. Pause every 3-5 minutes and ask: "Has everyone reached this point? Drop a thumbs up in chat."
- When attendees hit errors, troubleshoot live — this is the highest-value part. Note every friction point.
- In the Q&A, prioritize questions about getting stuck. Every unstuck user is a potential activation.
- End with one clear CTA: complete the activation action in your account by end of day. Share a help link for those who need more time.

After the session:
- Export the attendee list. Tag each registrant in Attio: `attended`, `no_show`, or `asked_question`.
- Log PostHog events: `webinar_attended`, `webinar_question_asked`, `webinar_completed` with properties `{webinar_slug: "onboarding-pilot-1", attendee_email: "..."}`.

### 4. Follow up within 24 hours

Send two emails through Loops:

**To attendees:** Recording link, a 3-bullet summary of what was covered, and a direct link to complete the activation action if they did not finish during the session. Subject: "Recording + your next step."

**To no-shows:** Recording link with "Sorry we missed you" framing. Highlight the one thing attendees accomplished during the session. Subject: "Here's what you missed — 20-minute recording."

Track email opens and clicks in PostHog: `webinar_followup_opened`, `webinar_followup_clicked`.

### 5. Measure activation over 7 days

After 7 days from the webinar date, pull activation data from PostHog:

- **Attendee activation rate:** Of users who attended, what % reached the activation event within 7 days?
- **No-show activation rate:** Of registrants who did not attend but received the recording, what %?
- **Control activation rate:** Of the control group (no webinar invite), what %?
- **Registration rate:** Registrations / invitations sent
- **Show rate:** Attendees / registrations

### 6. Evaluate against threshold

Run the `threshold-engine` drill with these criteria:

- **Attendee activation rate >= 50%** — the webinar directly helps at least half of attendees activate
- **Activation lift > 10 percentage points** — attendees activate at a meaningfully higher rate than the control group (e.g., 55% vs 40%)

If PASS: The webinar format accelerates activation. Proceed to Baseline to automate the series.

If FAIL on activation rate: The content did not drive the right action. Review: was the workshop focused on the actual activation metric? Were attendees able to follow along in their own accounts? Were the friction points addressed during Q&A?

If FAIL on activation lift: Attendees activated but so did the control group at a similar rate. The webinar may not be adding value above existing onboarding. Review: is the control group receiving strong onboarding already? Is the webinar topic redundant with in-app guidance?

**Human action required:** Review the Q&A questions from the session. These are direct signals about where new users get stuck. Document the top 3 friction points and share with the product team regardless of pass/fail.

## Time Estimate

- 1 hour: Plan topic, build registration page, set up PostHog events
- 1 hour: Write invitation email, select cohort, split groups, send invites and reminders
- 1 hour: Prepare webinar content and demo account
- 1 hour: Deliver the webinar (human action)
- 30 minutes: Send follow-up emails, tag attendees in Attio
- 30 minutes: Pull metrics after 7 days, run threshold evaluation
- 1 hour: Document findings — friction points, Q&A themes, activation patterns

Total: ~6 hours spread over 2 weeks.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Cal.com | Registration and scheduling | Free for 1 user. [Pricing](https://cal.com/pricing) |
| Loops | Invitation emails, reminders, follow-up | Free up to 1,000 contacts. [Pricing](https://loops.so/pricing) |
| PostHog | Event tracking, activation measurement, cohort comparison | Free up to 1M events/mo. [Pricing](https://posthog.com/pricing) |
| Riverside | Webinar recording | Free plan: 2 hours recording. Standard: $19/mo. [Pricing](https://riverside.com/pricing) |

**Estimated cost for smoke test: $0** (all tools have free tiers sufficient for a single webinar with 10-30 attendees)

## Drills Referenced

- `webinar-pipeline` — plans the webinar topic, builds the registration funnel, promotes, and structures post-event follow-up
- `threshold-engine` — evaluates attendee activation rate and lift against pass/fail criteria
