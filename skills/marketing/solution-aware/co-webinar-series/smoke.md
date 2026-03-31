---
name: co-webinar-series-smoke
description: >
  Co-Webinar Series — Smoke Test. Identify one complementary partner, co-host
  a single webinar to their combined audience, and validate that joint events
  generate registrations and qualified leads from solution-aware prospects
  before investing in a recurring series.
stage: "Marketing > Solution Aware"
motion: "Partnerships & Warm Intros"
channels: "Events, Email"
level: "Smoke Test"
time: "8 hours over 2 weeks"
outcome: "≥ 50 registrations and ≥ 3 qualified leads from one co-webinar"
kpis: ["Total registrations", "Show rate", "Engagement rate", "Qualified leads generated"]
slug: "co-webinar-series"
install: "npx gtm-skills add marketing/solution-aware/co-webinar-series"
drills:
  - webinar-pipeline
  - threshold-engine
---

# Co-Webinar Series — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Events, Email

## Outcomes

One complete co-webinar executed with one adjacent, non-competing partner. Both companies promote to their audiences. At least 50 registrations and at least 3 qualified leads (defined as: attendee who asked a question, replied to a follow-up email, or booked a meeting) within 14 days of the event. This proves that combining audiences with a complementary company generates higher reach and lead quality than a solo webinar, and that solution-aware prospects attend joint events positioned around integrated workflows.

## Leading Indicators

- Partner responds to co-webinar pitch within 5 days (signal: the co-webinar concept resonates with adjacent companies)
- Partner agrees to co-promote without requiring payment (signal: mutual audience value is obvious)
- Registrations split is at least 30/70 — the partner drives at least 30% of total registrations (signal: partner will actually promote, not just lend their name)
- Registration page conversion rate exceeds 20% of page visitors (signal: topic and positioning resonate)
- Show rate exceeds 30% (signal: registrants are genuinely interested, not just casually signing up)
- At least 3 attendees ask questions or respond to polls during the event (signal: the content engaged the audience)
- At least 1 follow-up email gets a reply within 48 hours (signal: post-event nurture is working)

## Instructions

### 1. Research and select one co-webinar partner

Run the the co webinar partner matching workflow (see instructions below) drill with a reduced scope: identify 5 candidate companies that meet these criteria:

- **Adjacent, not competing**: They serve the same buyer persona but solve a different problem. Example: if you sell analytics, partner with a feature flagging tool. If you sell a CRM, partner with an email deliverability tool.
- **Similar audience size**: Their email list or LinkedIn following should be within 0.5x-2x of yours. A massive size mismatch means one side carries all the promotional burden.
- **Active content program**: They publish regularly and have a track record of promoting content to their audience.
- **Solution-aware audience**: Their audience already understands the problem category you solve.
- **Has a speaker**: Someone at the partner company can present credibly on a relevant topic.

Score each candidate on audience overlap, promotional reach, content fit, webinar capability, and relationship proximity. Select the single highest-scoring partner. Prioritize partners where you have an existing relationship — cold co-webinar pitches add weeks of latency to a smoke test.

### 2. Pitch the co-webinar

**Human action required:** Reach out to your selected partner's marketing lead, DevRel lead, or founder. Send a short email or LinkedIn DM:

- Explain the proposal: a one-time, co-hosted webinar. Both companies promote to their audiences. Both companies present content. 45-60 minutes, live, with Q&A.
- Explain the mutual value: you both get exposure to a relevant, non-competing audience at zero cost. Unlike a solo webinar, each side gets credibility from the association with the other brand.
- Propose 2-3 specific topic ideas that sit at the intersection of both products' value. Example: "How [your product] + [their product] helps [ICP persona] solve [shared pain point]."
- Propose a date 3-4 weeks out to allow promotion time.
- Offer to handle event logistics (registration page, webinar platform, recording) to lower the partner's commitment barrier.

Log the outreach in Attio. Update the partner status from "Prospect" to "In Conversation."

### 3. Plan and build the webinar

Once the partner confirms, run the `webinar-pipeline` drill to set up the complete webinar infrastructure:

- **Registration page**: Build a landing page with: co-branded headline, what attendees will learn (3 bullet points), both speakers' bios, date/time with timezone, and a simple registration form (name, email, company, role). Track registrations in PostHog using the `posthog-custom-events` fundamental.
- **Email confirmations and reminders**: Configure Loops to send: immediate confirmation, 1-week reminder, 1-day reminder, and 1-hour reminder with join link. Each reminder should re-sell the value, not just remind.
- **Registration tracking**: Create an Attio list for registrants. Tag each registrant with the event slug and their source (from your promotion or the partner's, tracked via UTM parameters).
- **Event content**: Collaborate with the partner on the agenda. A proven format for co-webinars: 5-minute intro by you, 15-minute presentation by your speaker, 15-minute presentation by partner speaker, 15-minute live Q&A moderated by either side. Total: 50 minutes.

Build UTM-tagged promotion links for each side:
- Your promotion: `{registration_page}?utm_source=own&utm_medium=co-webinar&utm_campaign=co-webinar-series&utm_content={partner_slug}`
- Partner promotion: `{registration_page}?utm_source={partner_slug}&utm_medium=co-webinar&utm_campaign=co-webinar-series&utm_content={partner_slug}`

### 4. Promote the event

Both sides promote using their own channels:

**Your promotion (agent-assisted):**
- Send a registration email to your relevant subscriber segment via Loops
- Post 2 LinkedIn announcements (announcement + countdown) using your social pipeline
- Send personal invites via Attio to 10-20 prospects in active pipeline — a co-webinar is a low-friction way to advance stagnant deals
- If you use Intercom, post an in-app message to relevant users

**Partner promotion (coordinate, do not control):**
- Share the partner's UTM-tagged link and suggest promotion assets (email copy, LinkedIn post drafts, social images)
- Let the partner promote through their own channels in their own voice
- Track their registrations via the UTM source parameter

**Human action required:** Send the promotion emails and LinkedIn posts. Coordinate with the partner on promotion timing. Run the event live.

### 5. Execute the co-webinar

**Human action required:** Deliver the webinar. Key execution notes:

- Start on time. Open with a hook, not housekeeping.
- Introduce both brands in 2 minutes. Do not spend 10 minutes on company overviews.
- Encourage chat participation early with a poll or question.
- Leave 25-30% of time for Q&A — this is where the best engagement happens and where you identify high-intent attendees.
- End with clear CTAs from both sides: book a demo, try the product, download a resource.
- Record the session on Riverside, Zoom, or equivalent.

### 6. Follow up with attendees

Within 24 hours of the event, segment registrants into tiers:

- **Tier 1 — Active attendee**: Attended AND asked a question or responded to a poll. Highest intent.
- **Tier 2 — Passive attendee**: Attended but did not engage beyond watching.
- **Tier 3 — No-show**: Registered but did not attend.

Send differentiated follow-up emails via Loops:
- Tier 1: Recording link + personalized note referencing their question. CTA: book a 15-minute call.
- Tier 2: Recording link + key takeaways summary. CTA: reply with which takeaway resonated.
- Tier 3: Recording link with "Sorry we missed you" framing. CTA: watch the recording.

Tag all registrants in Attio with the event slug, their tier, and their source (partner or own). Create deals in Attio for any Tier 1 contacts who match your ICP.

### 7. Evaluate against threshold

Run the `threshold-engine` drill 14 days after the event. Measure:

- Total registrations (all sources)
- Qualified leads generated (Tier 1 attendees + anyone who replied to follow-up + anyone who booked a meeting)
- Partner contribution (what % of registrations came from the partner's promotion)
- Show rate and engagement rate

**Pass threshold: >= 50 registrations AND >= 3 qualified leads**

- **Pass**: Document what worked (partner type, topic, format, promotion split, audience response). Note the partner contribution balance. Proceed to Baseline.
- **Marginal**: 30-49 registrations or 1-2 qualified leads. The channel shows promise but needs iteration. Diagnose: was the problem topic selection (low registrations), timing (low show rate), content quality (low engagement), or follow-up (low conversion)? Try one more co-webinar with a different partner or topic.
- **Fail**: <30 registrations. Diagnose: Did the partner actually promote? Was the topic too niche or too broad? Was the registration page converting? Was the audience truly solution-aware? Fix the biggest bottleneck and re-test.

## Time Estimate

- Partner research and selection: 2 hours
- Partner outreach and negotiation: 1 hour (human action)
- Registration page, tracking, and email setup: 1.5 hours
- Content collaboration with partner: 1 hour (human action)
- Promotion (emails, LinkedIn, personal invites): 1 hour
- Event execution: 1 hour (human action)
- Follow-up segmentation and email sends: 30 minutes
- Monitoring and evaluation: 30 minutes

Total: ~8 hours of active work over 2 weeks (including partner coordination wait time)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Partner research and enrichment | Launch: $185/mo ([clay.com/pricing](https://www.clay.com/pricing)) |
| Attio | Partner CRM, registrant tracking, deal creation | Free for up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Registration, attendance, and conversion tracking | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Loops | Confirmation emails, reminders, follow-up sequences | Free up to 1K contacts ([loops.so/pricing](https://loops.so/pricing)) |
| Riverside | Webinar hosting and recording | Free plan for 2 participants; Business: $24/mo ([riverside.fm/pricing](https://riverside.fm/pricing)) |
| Cal.com | Scheduling follow-up calls with qualified leads | Free tier available ([cal.com/pricing](https://cal.com/pricing)) |
| Anthropic Claude | Partner scoring, topic ideation, email copywriting | Sonnet: ~$0.10-0.50 per use ([docs.anthropic.com/en/docs/about-claude/models](https://docs.anthropic.com/en/docs/about-claude/models)) |

**Estimated cost for this level: Free** (all tools within free tiers for a single co-webinar)

## Drills Referenced

- the co webinar partner matching workflow (see instructions below) — find and score adjacent companies whose audiences overlap your ICP for co-webinar partnerships
- `webinar-pipeline` — plan, promote, execute, and follow up on the webinar lifecycle
- `threshold-engine` — evaluate registrations and qualified leads against the pass threshold
