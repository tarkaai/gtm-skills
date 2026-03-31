---
name: executive-roundtables-smoke
description: >
  Executive Roundtables — Smoke Test. Host one invite-only roundtable with
  8-12 C-level and SVP leaders on a strategic topic to validate whether
  ultra-exclusive peer conversations generate high-value pipeline. Manual
  execution, no tooling budget.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=8 executive attendees and >=3 follow-up meetings booked within 2 weeks"
kpis: ["RSVP rate (target >=35%)", "Show rate (target >=75%)", "Meeting conversion rate (target >=30% of attendees)"]
slug: "executive-roundtables"
install: "npx gtm-skills add marketing/solution-aware/executive-roundtables"
drills:
  - icp-definition
  - roundtable-pipeline
  - threshold-engine
---

# Executive Roundtables — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** MicroEvents | **Channels:** Events

## Outcomes

- Confirm that C-level and SVP leaders will accept an invitation to a small, off-the-record peer discussion facilitated by your company
- Validate that a single roundtable with 8+ executives generates at least 3 follow-up meetings — a higher bar than micro-roundtables because the attendee seniority justifies higher conversion expectations
- Test whether the topic creates natural openings for your product domain without a product pitch
- Determine whether the exclusivity framing ("10 leaders, invitation-only, Chatham House Rule") resonates with your ICP

This play is distinct from `micro-roundtables` in three ways: (1) attendee seniority is C-suite/SVP only, (2) group size is slightly larger (8-12 vs 5-10) to account for higher no-show rates from senior execs, (3) the pipeline value per attendee is higher, so fewer attendees need to convert.

## Leading Indicators

- 10+ RSVPs confirmed by Day -5 (senior execs commit early if the topic and peer group compel them)
- At least 2 attendees reference a strategic challenge related to your product domain during the discussion
- At least 2 attendees engage with each other directly (peer-to-peer exchange, not just answering the host's questions)
- At least 1 attendee replies to the follow-up email within 12 hours (C-suite reply speed signals high intent)

## Instructions

### 1. Define your executive roundtable ICP and topic

Run the `icp-definition` drill with executive-specific constraints:

- **Seniority floor**: C-suite (CEO, CTO, CRO, CMO, CFO) or SVP/VP at companies above 200 employees. Directors only if they are the top decision-maker in a sub-200 employee company.
- **Peer parity**: All attendees must be at similar company stages. Do not mix enterprise CROs with seed-stage founders — the conversation will not be useful for either group. Define a company size band (e.g., 200-2000 employees, or 2000-10000).
- **No direct competitors**: Verify that no two invitees compete directly. Check product category, target market, and geography.
- **Industry coherence**: Attendees should share enough context to have a productive discussion. A roundtable with a healthcare CISO and an e-commerce CMO will produce shallow generalities.

Choose a topic that is:
- **Strategic, not tactical**: "How are you structuring your AI investment for 2026?" not "What tools are you using for X?"
- **Decision-relevant**: The topic should connect to a budget decision, org change, or strategic bet that attendees are actively making
- **Polarizing**: There should be at least 2 legitimate approaches. If everyone agrees, the discussion dies.

Write 3 discussion questions ordered from easy to provocative. Store them in Attio using `attio-notes` on a new event record.

### 2. Build a guest list of 20-25 targets

Senior executives have higher decline rates (50-65%) so you need a larger invitation pool than micro-roundtables. For each target, collect:

- Name, email, company, title, company size, industry
- A specific reason why they would care about this topic (a recent earnings call comment, a LinkedIn post, a company announcement, or a known strategic initiative)
- A brief on why they would value the peer group (e.g., "She's scaling her GTM team and would benefit from hearing how peers handled the same transition")

Use the `attio-contacts` fundamental to log each person in Attio with tag "exec-roundtable-smoke-invited". Create an Attio list "Executive Roundtable - [Topic] - [Date]" via `attio-lists`.

Sources for guest identification:
- Your CRM: existing contacts who match the seniority and company profile
- LinkedIn Sales Navigator: search by title + company size + industry + geography
- Conference speaker lists: people who spoke at relevant industry events are likely comfortable in discussion formats
- Warm introductions: ask your board, investors, or advisors who they know that matches the profile

### 3. Send personal invitations in two waves

Run the `roundtable-pipeline` drill's invitation steps. At Smoke, all invitations are sent manually by the host.

**Wave 1 (Day -21): Top 12 targets**

Each email must include:
- **Exclusivity frame**: "I'm hosting a private discussion with 10 [title]-level leaders on [topic]. Invitation only, Chatham House Rule."
- **Peer proof**: "Other participants include leaders from [2-3 company types — do not name specific companies until they confirm]"
- **Topic hook**: Pose the most provocative discussion question. Example: "The central question: should you build or buy your [domain] capability in 2026?"
- **Logistics**: Date, time (60 minutes), video conferencing link (Zoom or Google Meet)
- **Low-friction RSVP**: "Reply 'in' to confirm your seat" — not a form, not a link. Reduce friction to zero for executives.

**Wave 2 (Day -14): Remaining 10-13 targets + Wave 1 non-responders**

Include: "8 leaders confirmed so far. We have 2-3 spots remaining."

**Day -7 follow-up (if under 10 confirmed)**:
Send a final push to non-responders: "Last call — we're at 9 confirmed and closing the group this week."

**Human action required:** The host must send invitations from their personal email. The agent drafts the copy; the host sends it. Executive spam filters and credibility requirements make this non-negotiable.

### 4. Prepare the host and execute the roundtable

Run the `roundtable-pipeline` drill steps 5-7.

**Day -3: Send the briefing packet to confirmed attendees**
- Attendee list: first name, title, and company for each confirmed guest
- The 3 discussion questions
- Meeting link and calendar hold

**Day -1: Agent generates the host's briefing**
- One paragraph per attendee: name, company, role, recent relevant activity (LinkedIn post, company news), and one question the host could ask them specifically
- Suggested discussion flow: opening frame (2 min), warm-up question (10 min), core question (20 min), provocative question (15 min), wrap-up (5 min)

**Event execution (Human action required):**
- Open with: "This is Chatham House Rule — you can reference ideas from today but not attribute them. No pitches, no slides, just a conversation among peers."
- Start with the easiest question to get voices in the room
- After 10 minutes, pivot to the core strategic question
- Call on quiet participants by name: "[Name], you're dealing with this at [company] — what's your perspective?"
- In the final 10 minutes, ask the provocative question that creates the sharpest disagreement
- End with: "What surprised you most in today's conversation?"

If Fireflies.ai is available (free tier: 800 min/month), connect it for transcription. Otherwise, the host takes brief notes on who said what.

### 5. Execute tiered follow-up within 4 hours

Within 4 hours of the event, send a personal follow-up to each attendee. The `roundtable-pipeline` drill covers data logging; here is the follow-up structure:

**High-engagement attendees (spoke 3+ times, expressed a pain point):**
- Reference a specific point they made: "Your point about [specific thing] really resonated with the group."
- Share 1 relevant resource (article, framework, data point) related to their stated challenge
- Direct meeting CTA: "I think there's something specific I can show you that's relevant to what you described. Would 20 minutes work next week? [3 specific time slots or Cal.com link]"

**Medium-engagement attendees (spoke 1-2 times):**
- Reference the discussion broadly: "Great to have your perspective in the room today."
- Share the discussion summary (3-5 key themes)
- Soft CTA: "If any of these themes hit close to home, I'd enjoy continuing the conversation 1:1."

**No-shows (confirmed but did not attend):**
- Subject: "Missed you at the [topic] roundtable"
- Share 3 key takeaways (create FOMO without giving everything away)
- CTA: "We're planning a follow-up session — want me to hold a spot for you?"

Log every attendee in Attio using `attio-contacts` and `attio-notes`: engagement tier, key statements, follow-up interest signals, and meeting booking status.

### 6. Evaluate results after 2 weeks

Run the `threshold-engine` drill to evaluate:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Executive attendees | >=8 | Count of attendees at VP+ level in Attio |
| Follow-up meetings booked | >=3 | Cal.com bookings or email-confirmed meetings within 14 days |
| RSVP rate | >=35% | Confirmed / Invited |
| Show rate | >=75% | Attended / Confirmed |

**PASS (>=8 attendees AND >=3 meetings):** The format works at executive level. Document: which topic angle drove engagement, which attendee profiles converted, what the host did well in facilitation. Proceed to Baseline.

**MARGINAL (8+ attendees but 1-2 meetings):** The event format works but follow-up conversion is low. Diagnose: Were follow-up emails sent within 4 hours? Did they reference specific discussion points? Was the CTA clear and low-friction? Adjust follow-up approach and re-run.

**FAIL (<8 attendees):** Diagnose the invitation funnel:
- Low RSVP rate (<25%): The topic or exclusivity framing is not compelling enough. Try a more provocative topic or a stronger peer group.
- High RSVP but low show rate (<60%): Commitment is weak. Add a pre-event call or personalized video from the host to increase commitment.
- Wrong seniority: If attendees are mostly Directors when you targeted C-suite, the invitation copy needs stronger exclusivity signals.

## Time Estimate

- ICP definition and topic selection: 1.5 hours
- Guest list building (manual research): 1.5 hours
- Invitation copywriting and sending (2 waves + follow-up): 1 hour
- Host briefing preparation: 30 minutes
- Facilitating the roundtable (live): 1 hour
- Follow-up emails and data logging: 30 minutes
- **Total: ~6 hours over 1-2 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Log invitees, track RSVPs, engagement tiers, and meetings | Free for up to 3 users — [attio.com/pricing](https://attio.com/pricing) |
| Cal.com | Booking link for follow-up meetings | Free plan — [cal.com/pricing](https://cal.com/pricing) |
| Zoom | Host the roundtable | Free tier: 100 participants, 40-min limit — [zoom.us/pricing](https://zoom.us/pricing) |
| Google Meet | Host the roundtable (alternative) | Free with Google Workspace — [workspace.google.com](https://workspace.google.com) |
| Fireflies.ai | Transcription (optional at Smoke) | Free plan: 800 min/month — [fireflies.ai/pricing](https://fireflies.ai/pricing) |

**Estimated monthly cost for Smoke: $0** (all free tiers)

## Drills Referenced

- `icp-definition` — define the executive target profile, seniority floor, peer parity criteria, and topic selection
- `roundtable-pipeline` — plan invitees, execute the roundtable, capture discussion insights and attendee data
- `threshold-engine` — evaluate results against the pass threshold and decide next action
