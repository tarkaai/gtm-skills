---
name: qualified-prospect-calls-smoke
description: >
  Founder calls to prospects — Smoke Test. Founder personally calls 20-30 qualified
  prospects in one week to validate that direct phone outreach produces meetings. Agent
  builds the call list, enriches contacts with phone numbers, prepares per-prospect
  call briefs, and logs every outcome. Human executes the calls.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Email, Social, Direct"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: "≥ 2 meetings booked in 1 week from ≤ 30 dials"
kpis: ["Connect rate", "Dials attempted", "Meeting conversion rate", "Average call duration"]
slug: "qualified-prospect-calls"
install: "npx gtm-skills add sales/qualified/qualified-prospect-calls"
drills:
  - icp-definition
  - build-prospect-list
  - enrich-and-score
  - cold-call-framework
  - meeting-booking-flow
  - threshold-engine
---

# Founder Calls to Prospects — Smoke Test

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Email, Social, Direct

## Outcomes

Book 2 or more meetings from no more than 30 dial attempts in 1 week. This validates that your ICP responds to direct phone outreach from the founder and that the problem resonance is strong enough to earn a conversation.

## Leading Indicators

- Connect rate above 20% (6+ live conversations from 30 dials)
- Average call duration above 90 seconds (prospects are engaging, not hanging up)
- At least 1 prospect asks a question about your product unprompted (genuine curiosity signal)
- Positive sentiment in at least 50% of connected calls (not hostile or dismissive)

## Instructions

### 1. Define your ICP for phone outreach

Run the `icp-definition` drill. Focus the ICP on prospects reachable by phone: prioritize roles where direct dials are available (VP and above at companies with 20-200 employees tend to answer more often than enterprise execs behind gatekeepers). Document the company size, industry, job titles, pain points, and triggering events that make a prospect worth calling.

### 2. Build and enrich a call list of 20-30 prospects

Run the `build-prospect-list` drill to source 40-50 contacts matching your ICP from Clay and Apollo. Then run the `enrich-and-score` drill to score and filter to the top 20-30. Critical enrichment for phone outreach: use the Clay enrichment waterfall to find direct phone numbers (mobile preferred over office). Prospects without a phone number get dropped from this list — do not waste a Smoke test dial on a generic company switchboard.

Push the scored list to Attio. Tag each contact with `qualified-prospect-calls-smoke` and the signal that triggered inclusion (funding, hire, job change, technology adoption).

### 3. Prepare per-prospect call briefs

For each of the 20-30 prospects, the agent prepares a one-paragraph call brief containing:

- Their name, title, company, and company size
- The specific signal that makes them relevant right now (e.g., "Closed Series B 3 weeks ago" or "Just hired 4 engineers in 2 months")
- One sentence connecting that signal to the problem your product solves
- The open-ended question to ask if they engage (from the `cold-call-framework` drill)

Store each brief as a note on the prospect's Attio record so the founder can pull it up during the call.

### 4. Set up meeting booking infrastructure

Run the `meeting-booking-flow` drill to create a Cal.com event type for "Discovery Call — 15 min" with the founder's availability. Generate a booking link. The founder will verbally offer this link during calls or send it via follow-up text/email immediately after a positive call.

### 5. Execute the calls

**Human action required:** The founder makes the calls. Block 1-hour sessions (aim for 10-15 dials per session). Call during optimal windows: Tuesday-Thursday, 8-10am or 4-5pm in the prospect's timezone. Follow the call structure from the `cold-call-framework` drill:

- Open with name + pattern interrupt referencing their signal
- Ask permission ("Did I catch you at an okay time?")
- State the problem in their language
- Ask the open-ended question from the brief
- If interest: suggest the 15-min follow-up and share the Cal.com link
- If no interest: thank them and note the objection

### 6. Log every call outcome immediately

After each call, log the outcome in Attio using structured fields:

- **Disposition**: Connected / Voicemail / No Answer / Gatekeeper
- **If connected**: Meeting Set / Follow-Up Requested / Not Interested / Call Back Later
- **Duration**: Approximate seconds
- **Objection** (if any): Price / Timing / Already Have Solution / Not My Problem / Other
- **Notes**: One sentence on what happened and any insight gained
- **Signal used**: Which trigger was referenced in the opener

### 7. Evaluate against threshold

After all 30 dials (or at end of 1 week, whichever comes first), run the `threshold-engine` drill. Pull logged data from Attio. Compute:

- Total dials attempted
- Connect rate (connected / attempted)
- Meeting conversion rate (meetings booked / connected)
- Total meetings booked

**Pass: 2 or more meetings booked.** Proceed to Baseline.

**Fail: fewer than 2 meetings.** Diagnose:
- If connect rate < 15%: phone numbers are bad or call timing is wrong. Re-enrich with different providers, test different time windows.
- If connect rate >= 15% but meeting rate < 15% of connected: the pitch or pain point is not resonating. Rewrite the call script and problem statement.
- If both metrics are decent but volume was too low (< 20 dials): the issue is execution consistency, not the play itself. Recommit and re-run.

## Time Estimate

- ICP definition + list building + enrichment: 1 hour (agent)
- Call brief preparation: 30 minutes (agent)
- Meeting booking setup: 15 minutes (agent)
- Calling sessions: 1 hour total across the week (human)
- Logging + threshold evaluation: 15 minutes (agent)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM, call logging, prospect records | Free tier: 3 users, unlimited records |
| Clay | Enrichment, phone number discovery | Free tier: 100 credits/mo; Explorer: $149/mo |
| Cal.com | Meeting scheduling | Free tier: 1 event type |
| Apollo | Initial prospect sourcing | Free tier: 60 credits/mo |

**Estimated play-specific cost at this level:** Free (all tools within free tiers for 30 prospects)

## Drills Referenced

- `icp-definition` — define who to call and why
- `build-prospect-list` — source 40-50 ICP-matching contacts
- `enrich-and-score` — score, filter to top 20-30, enrich with phone numbers
- `cold-call-framework` — structure for the call script and objection handling
- `meeting-booking-flow` — Cal.com setup for booking discovery calls
- `threshold-engine` — evaluate pass/fail against 2-meeting target
