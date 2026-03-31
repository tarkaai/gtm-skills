---
name: partnerships-warm-intros-smoke
description: >
  Partnerships & Warm Intros — Smoke Test. Manually identify 10 connectors in your network,
  send personalized intro requests, and test whether warm routes produce any intros and meetings
  before investing in systems or automation.
stage: "Sales > Qualified"
motion: "PartnershipsWarmIntros"
channels: "Other"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: "≥ 3 intros received and ≥ 2 meetings booked within 2 weeks"
kpis: ["Intro requests sent", "Intros received", "Meetings booked from intros", "Request-to-intro rate"]
slug: "partnerships-warm-intros"
install: "npx gtm-skills add sales/qualified/partnerships-warm-intros"
drills:
  - icp-definition
  - build-prospect-list
  - warm-intro-request
  - threshold-engine
---

# Partnerships & Warm Intros — Smoke Test

> **Stage:** Sales > Qualified | **Motion:** PartnershipsWarmIntros | **Channels:** Other

## Outcomes

Prove that warm introductions from your existing network can generate qualified meetings. At Smoke, you are testing the channel with zero budget and manual effort. Success means your network is willing to make intros and those intros convert to real conversations.

Pass threshold: **>= 3 intros received AND >= 2 meetings booked within 2 weeks.**

## Leading Indicators

- Connector response rate to intro requests (target: >50% respond within 5 days)
- Intro request acceptance rate (target: >30% of requests result in an actual intro)
- Time from intro request sent to intro made (target: <5 days average)
- Prospect response rate after receiving intro (target: >70% reply)

## Instructions

### 1. Define your partner ICP and target prospects

Run the `icp-definition` drill to define two profiles:

**A. Ideal Connector Profile:** Who in your network is most likely to make intros? Filter for:
- People who know your target buyers personally (not just LinkedIn connections)
- People with credibility in your target market (advisors, investors, industry leaders, happy customers)
- People who have made intros for you before (proven willingness)
- People who are responsive to your messages (active communicators)

**B. Ideal Intro Target Profile:** Who do you want to be introduced to? Filter for:
- Decision makers at companies matching your ICP
- People currently experiencing the problem your product solves
- People whose companies have budget and timeline to buy

Write both profiles as structured criteria the agent can evaluate against. Store in Attio as saved filters.

### 2. Build a prospect list of connectors and targets

Run the `build-prospect-list` drill twice:

**First run — Connectors:** Search your Attio contacts, LinkedIn connections, and email history. Identify 10-15 people who match your Ideal Connector Profile. For each connector, note:
- Relationship strength (strong/medium/weak)
- Estimated reach into your target market (how many targets do they know?)
- Last interaction date (when did you last communicate?)
- Best communication channel (email, LinkedIn DM, text, call)

**Second run — Targets:** Identify 15-20 target prospects you want intros to. For each target:
- Company name, role, LinkedIn URL
- Which connectors might know this person (check LinkedIn mutual connections)
- Why an intro would be valuable (specific reason, not generic)

Create two Attio lists: "Warm Intro Connectors — Smoke" and "Warm Intro Targets — Smoke." Map which connectors can reach which targets.

### 3. Craft and send intro requests

Run the `warm-intro-request` drill for your top 10 connector-target pairs. For each request:

1. Write a short, specific message to the connector explaining:
   - Who you want to meet and why (one sentence)
   - What value you can offer the target (one sentence)
   - A pre-written forwardable blurb the connector can copy-paste to the target
2. Send via the connector's preferred channel (email or LinkedIn DM)
3. Log the request in Attio: connector name, target name, date sent, channel used

**Human action required:** Send intro requests personally. Do not automate at Smoke level. The personal touch is what makes warm intros work. Make each request feel like a real ask from one human to another.

### 4. Handle introductions and book meetings

When an intro is made:
1. Respond within 2 hours. Thank the connector (reply-all or separately).
2. Open with the context the connector provided. Reference the specific connection.
3. Propose a specific meeting time using your Cal.com link or suggest 2-3 time slots.
4. Log in Attio: intro received date, meeting booked (yes/no), meeting date.

When a meeting happens:
1. Log the outcome in Attio: meeting held, next steps, deal created (yes/no)
2. Send a thank-you note to the connector reporting how the meeting went

### 5. Evaluate against threshold

Run the `threshold-engine` drill after 2 weeks. Measure:

- **Intro requests sent:** Count of requests logged in Attio (target: >= 10)
- **Intros received:** Count of actual introductions made (target: >= 3)
- **Meetings booked:** Count of meetings scheduled from intros (target: >= 2)
- **Request-to-intro rate:** intros / requests (track but no minimum at Smoke)

**PASS (>= 3 intros AND >= 2 meetings):** Warm intros work for your network. Document which connectors responded, what messaging worked, and which targets converted. Proceed to Baseline.

**FAIL:** Diagnose why:
- If connectors did not respond: Your relationship is weaker than expected, or your ask was unclear. Try different connectors or refine your request template.
- If connectors responded but did not intro: Your target selection does not match their network. Ask connectors who they *can* intro you to instead.
- If intros were made but meetings did not book: Your positioning after the intro needs work. Review how you followed up on each intro.

## Time Estimate

- 1 hour: Define connector and target profiles, build lists
- 1 hour: Craft personalized intro requests and send
- 1 hour: Handle intros, book meetings, log outcomes, evaluate

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — track connectors, targets, intros, meetings | Free for up to 3 users; $29/user/mo Plus plan ([attio.com/pricing](https://attio.com/pricing)) |
| LinkedIn | Identify mutual connections, send DM requests | Free (basic); Sales Navigator ~$100/mo for advanced search |
| Cal.com | Meeting booking links for intro follow-ups | Free for 1 user ([cal.com/pricing](https://cal.com/pricing)) |

**Estimated Smoke cost: $0** (all tools have free tiers sufficient for this level)

## Drills Referenced

- `icp-definition` — define ideal connector profile and ideal intro target profile
- `build-prospect-list` — build and enrich connector and target lists in Attio
- `warm-intro-request` — craft intro requests, map mutual connections, send and track
- `threshold-engine` — evaluate intro and meeting counts against pass threshold
