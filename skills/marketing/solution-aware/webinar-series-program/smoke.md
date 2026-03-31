---
name: webinar-series-program-smoke
description: >
  Educational Webinar Series — Smoke Test. Run a single educational webinar to
  validate that your ICP will register, attend, and convert into qualified leads.
  No recurring commitment — one event, proof of signal.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events, Content, Email"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥25 registrations and ≥3 qualified leads from first webinar"
kpis: ["Registration count", "Show rate", "Qualified leads generated", "Post-event reply rate"]
slug: "webinar-series-program"
install: "npx gtm-skills add marketing/solution-aware/webinar-series-program"
drills:
  - icp-definition
  - webinar-pipeline
  - threshold-engine
---

# Educational Webinar Series — Smoke Test

> **Stage:** Marketing → SolutionAware | **Motion:** MicroEvents | **Channels:** Events, Content, Email

## Outcomes

Run a single educational webinar and prove that your ICP registers, attends, and converts. Pass threshold: ≥25 registrations AND ≥3 qualified leads (defined as: replied to follow-up email, booked a meeting, or asked a question during the webinar that signals buying intent).

## Leading Indicators

- Registration page conversion rate >20% of page visitors
- At least 50 unique page views to the registration page within the promotion window
- Confirmation email open rate >70% (indicates real registrants, not spam)
- Day-before reminder click-through >40% (predicts show rate)

## Instructions

### 1. Define the webinar ICP and topic

Run the `icp-definition` drill. From the ICP output, extract the top pain point that your product addresses. The webinar topic must sit at the intersection of this pain point and your unique expertise. Frame the topic as a "how to" or "why X fails" — educational, not promotional.

Document in Attio:
- Target audience: titles, company size, industry
- Hypothesis: "If we run a [format] webinar on [topic], [ICP persona] will register because [pain point reason]"
- Success criteria: ≥25 registrations, ≥3 qualified leads

### 2. Build the webinar and registration funnel

Run the `webinar-pipeline` drill. This creates: a registration landing page with form (name, email, company, role), Cal.com event scheduling for the live session, Loops confirmation and reminder email sequence (confirmation, 1-day before, 1-hour before), and an Attio list for tracking registrants.

Configure PostHog tracking on the registration page: `webinar_page_viewed` and `webinar_registered` events.

Set the event date 3 weeks from now to allow promotion time.

### 3. Promote the webinar

Execute these promotion steps within the `webinar-pipeline` drill's promotion workflow:

1. Send a targeted email via Loops to your existing subscriber list, segmented by ICP relevance. Do not blast your entire list.
2. Post on LinkedIn: one announcement post with the registration link. Write a hook that leads with the pain point, not the event details.
3. Send personal invitations from Attio to 10-20 high-value prospects. A webinar invite is lower friction than a sales meeting and can re-engage stalled conversations.
4. If you have an Intercom install base, use in-app messages to promote to existing users who match the topic.

**Human action required:** Deliver the webinar live. The agent prepares everything — topic, registration, promotion, reminders — but a human presents the content and answers questions.

### 4. Execute post-webinar follow-up

Within 4 hours after the webinar ends:

1. Export the attendee list from your webinar platform (Zoom, Riverside, or Google Meet).
2. Tag all registrants in Attio: `attended`, `registered-no-show`, or `asked-question`.
3. Send two follow-up emails via Loops:
   - **Attendees**: Recording link + 3 key takeaways + CTA to book a meeting.
   - **No-shows**: Recording link + "Sorry we missed you" framing + same CTA.
4. For anyone who asked a question during the webinar, send a personal reply (from Attio or email) that answers their question and offers a 1:1 conversation.

### 5. Evaluate against threshold

Run the `threshold-engine` drill 7 days after the webinar. Measure:

- Total registrations (target: ≥25)
- Show rate (benchmark: 30-50%)
- Qualified leads generated (target: ≥3 — defined as replied to follow-up, booked meeting, or asked buying-intent question)
- Post-webinar follow-up reply rate

**PASS → Baseline**: Hit both thresholds. Document what topic, format, and promotion channels worked.
**MARGINAL → Re-run**: Close but missed (e.g., 20 registrations, 2 leads). Adjust topic or promotion and run one more event at Smoke level.
**FAIL → Pivot**: Fundamentally missed (e.g., <10 registrations). Your ICP may not respond to webinars. Try a different play.

## Time Estimate

- ICP definition and topic selection: 1 hour
- Registration page and email setup: 1.5 hours
- Promotion (emails, posts, personal outreach): 1 hour
- Webinar delivery (human): 1 hour
- Post-event follow-up: 1 hour
- Threshold evaluation: 0.5 hours

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Zoom / Google Meet | Webinar platform | Free tier (40 min limit on Zoom free; Google Meet free with Workspace) |
| Cal.com | Registration scheduling | Free tier — https://cal.com/pricing |
| Loops | Email confirmations and follow-ups | Free up to 1,000 contacts — https://loops.so/pricing |
| Attio | CRM for registrant tracking | Free up to 3 seats — https://attio.com/pricing |
| PostHog | Registration page analytics | Free up to 1M events — https://posthog.com/pricing |

**Estimated play-specific cost: $0** (all tools within free tiers for a single webinar)

## Drills Referenced

- `icp-definition` — defines the target audience and pain points that determine webinar topic selection
- `webinar-pipeline` — builds the full webinar lifecycle: registration, promotion, reminders, execution, follow-up
- `threshold-engine` — evaluates final metrics against pass/fail criteria and recommends next action
