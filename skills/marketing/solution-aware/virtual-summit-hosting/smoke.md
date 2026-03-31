---
name: virtual-summit-hosting-smoke
description: >
  Virtual Summit Hosting — Smoke Test. Run one multi-session virtual summit to
  validate that your ICP will register, attend multiple sessions, and convert
  into qualified leads. No recurring commitment — one summit, proof of signal.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events, Content, Email"
level: "Smoke Test"
time: "20 hours over 8 weeks"
outcome: "≥150 registrations, ≥50 attendees, and ≥8 qualified leads from first summit"
kpis: ["Registration count", "Show rate", "Multi-session attendance rate", "Qualified leads generated", "Post-summit reply rate"]
slug: "virtual-summit-hosting"
install: "npx gtm-skills add marketing/solution-aware/virtual-summit-hosting"
drills:
  - icp-definition
  - summit-pipeline
  - threshold-engine
---

# Virtual Summit Hosting — Smoke Test

> **Stage:** Marketing → SolutionAware | **Motion:** MicroEvents | **Channels:** Events, Content, Email

## Outcomes

Run a single multi-session virtual summit (4-6 sessions, half-day format) and prove that your ICP registers, attends multiple sessions, and converts into qualified pipeline. Pass threshold: ≥150 registrations AND ≥50 attendees AND ≥8 qualified leads (defined as: replied to post-summit follow-up, booked a meeting, or asked a buying-intent question during a session).

## Leading Indicators

- Registration page conversion rate >15% of page visitors
- At least 500 unique page views to the registration page within the 8-week promotion window
- Confirmation email open rate >70% (indicates real registrants)
- Day-before reminder click-through >40% (predicts show rate)
- Speaker promotion generates ≥20% of total registrations (validates speaker selection)
- At least 3 speakers confirmed within 4 weeks of outreach (validates theme appeal to speakers)

## Instructions

### 1. Define the summit ICP and theme

Run the `icp-definition` drill. From the ICP output, identify the top 2-3 pain points your product addresses. The summit theme must unify these pain points under a single narrative — something like "The State of [Industry Problem]" or "How [ICP Role] Teams Are Solving [Pain Point] in 2026."

Document in Attio:
- Target audience: titles, company size, industry, geography
- Hypothesis: "If we host a [half-day/full-day] virtual summit on [theme], [ICP persona] will register because [pain point reason]. We expect [N] registrations based on our list size of [N] and estimated reach of [N] through speakers."
- Success criteria: ≥150 registrations, ≥50 attendees, ≥8 qualified leads
- Summit format: 4-6 sessions, session types (keynote, panel, workshop, fireside chat)
- Target date: 8 weeks from today (Tuesday, Wednesday, or Thursday)

### 2. Build the summit and registration funnel

Run the `summit-pipeline` drill. This creates:

- A registration landing page with: summit theme and value proposition, full agenda with session titles and speaker bios, date/time with timezone, registration form (name, email, company, role, company size), and social proof (speaker company logos).
- Cal.com event scheduling for speaker prep calls.
- Loops confirmation and reminder email sequence (confirmation, 1-week, 1-day, 1-hour reminders).
- Attio list for tracking registrants with fields: registration date, company, role, source channel.
- PostHog tracking: `summit_page_viewed`, `summit_registered`, `summit_agenda_expanded` events.

Configure 4-6 sessions across a half-day format (4 hours including breaks):
- Session 1: Keynote (20 min) — set the theme, establish the problem
- Sessions 2-3: Panels or fireside chats (30 min each) — explore specific aspects of the problem
- Session 4: Workshop or live demo (40 min) — show solutions in action
- Sessions 5-6 (optional): Lightning talks or AMA

Recruit 6-10 speakers following the `summit-pipeline` drill's speaker recruitment process. Prioritize: 2-3 customer speakers (most credible), 2-3 industry experts (draw registrations), 1-2 internal speakers (your unique perspective).

### 3. Promote the summit

Execute the `summit-pipeline` drill's promotion engine:

1. Send a targeted email via Loops to your subscriber list, segmented by ICP relevance. Lead with the pain point, not the event logistics.
2. Post on LinkedIn: announcement post with the registration link. Write a hook that leads with the problem the summit addresses.
3. Activate speaker promotion: provide each speaker with a pre-written social post they can customize and share. Track which speakers drive the most registrations.
4. Send personal invitations from Attio to 20-40 high-value prospects. A summit invite is lower friction than a sales meeting and re-engages stalled pipeline.
5. If you have an Intercom user base, promote via in-app messages to users who match the summit audience.

**Human action required:** Moderate the summit live. The agent handles all preparation, speaker coordination, promotion, and reminders, but a human moderates sessions, manages Q&A, handles technical issues, and delivers any internal sessions.

### 4. Execute post-summit follow-up

Within 4 hours of the summit closing, execute the post-summit nurture steps from the `summit-pipeline` drill:

1. Export session-level attendance data from the event platform (Riverside, Zoom).
2. Tag all registrants in Attio by tier: Tier 1 (attended 4+ sessions + engaged), Tier 2 (2-3 sessions + engaged), Tier 3 (1-2 sessions passive), Tier 4 (no-show).
3. Send tier-appropriate follow-up emails via Loops:
   - **Tier 1**: Personal thank-you + all recordings + direct meeting CTA referencing their engagement.
   - **Tier 2**: Recordings + key takeaways + meeting CTA.
   - **Tier 3**: All recordings + highlight of the best session + soft meeting CTA.
   - **Tier 4**: "Sorry we missed you" + all recordings.
4. For anyone who asked a question during a session, send a personal reply that answers their question and offers a 1:1 conversation.

### 5. Evaluate against threshold

Run the `threshold-engine` drill 14 days after the summit. Measure:

- Total registrations (target: ≥150)
- Show rate (target: ≥35%)
- Multi-session attendance rate (target: ≥40% of attendees attend 2+ sessions)
- Qualified leads generated (target: ≥8 — defined as replied to follow-up, booked meeting, or asked buying-intent question)
- Post-summit follow-up reply rate by tier
- Promotion channel attribution (which channels drove the most registrations)

**PASS → Baseline**: Hit all three primary thresholds. Document what theme, speaker lineup, format, and promotion channels worked.
**MARGINAL → Re-run**: Close but missed (e.g., 120 registrations, 5 leads). Adjust theme, speaker lineup, or promotion and run one more summit at Smoke level.
**FAIL → Pivot**: Fundamentally missed (e.g., <60 registrations). Your ICP may not respond to summits. Consider a smaller format (webinar series, roundtables) instead.

## Time Estimate

- ICP definition and theme selection: 2 hours
- Speaker recruitment and coordination: 6 hours
- Registration page and email setup: 2 hours
- Promotion (emails, posts, personal outreach): 3 hours
- Speaker prep calls and production setup: 3 hours
- Summit moderation (human): 4 hours
- Post-summit follow-up: 2 hours
- Threshold evaluation: 1 hour

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Riverside | Multi-session summit hosting and recording | Free tier (2 hr/mo recording); $15/mo Standard for longer summits — https://riverside.fm/pricing |
| Cal.com | Speaker prep call scheduling | Free tier — https://cal.com/pricing |
| Loops | Email confirmations, reminders, and follow-ups | Free up to 1,000 contacts — https://loops.so/pricing |
| Attio | CRM for registrant and speaker tracking | Free up to 3 seats — https://attio.com/pricing |
| PostHog | Registration page and session analytics | Free up to 1M events — https://posthog.com/pricing |
| Clay | Speaker discovery and prospect enrichment | $149/mo (Explorer) — https://clay.com/pricing |

**Estimated play-specific cost: $0-164/mo** (Riverside free tier for short summits; Clay if used for speaker sourcing — can be skipped if speakers recruited through existing network)

## Drills Referenced

- `icp-definition` — defines the target audience and pain points that determine summit theme selection
- `summit-pipeline` — builds the full summit lifecycle: speaker recruitment, registration, promotion, production, follow-up
- `threshold-engine` — evaluates final metrics against pass/fail criteria and recommends next action
