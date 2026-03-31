---
name: trigger-based-outreach-smoke
description: >
  Trigger-based Outreach — Smoke Test. Manually identify 30 solution-aware prospects
  exhibiting buying signals (funding, hiring, job changes, tech stack shifts), craft
  signal-specific outreach, and send from the founder's inbox. Validates whether
  timing outreach to real-world trigger events produces meetings at a higher rate
  than cold outreach.
stage: "Marketing > SolutionAware"
motion: "OutboundFounderLed"
channels: "Email, Social"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥ 3 meetings booked from 30 trigger-based contacts in 7 days"
kpis: ["Positive reply rate (target ≥ 10%)", "Meeting rate (target ≥ 10%)", "Time from signal detection to first reply (target < 48 hours)"]
slug: "trigger-based-outreach"
install: "npx gtm-skills add marketing/solution-aware/trigger-based-outreach"
drills:
  - icp-definition
  - signal-detection
---

# Trigger-based Outreach — Smoke Test

> **Stage:** Marketing > SolutionAware | **Motion:** OutboundFounderLed | **Channels:** Email, Social

## Outcomes

Prove that outreach timed to buying signals (funding rounds, executive hires, hiring sprees, tech stack changes, competitor churn) produces meetings at a materially higher rate than untriggered cold outreach. The founder manually scans for signals, crafts messages referencing the trigger, and sends from their primary inbox. No tooling budget. No automation. If 30 signal-triggered contacts produce 3+ meetings in a week, the timing hypothesis is validated.

Pass: 3 or more meetings booked from up to 30 trigger-based contacts within 7 days.
Fail: Fewer than 3 meetings after 30 sends and 7 days.

## Leading Indicators

- First reply arrives within 24 hours of send (signals that trigger-timed messages get faster attention than cold sends)
- Replies reference the trigger event you mentioned (confirms the signal added relevance, not just timing)
- At least 2 replies in the first 15 sends (signals both list quality and message-trigger alignment)

## Instructions

### 1. Define ICP and map signal types to your buyer

Run the `icp-definition` drill to document your Ideal Customer Profile. Then extend it with a signal map: for each ICP attribute, identify which buying signals indicate that a company matching that attribute is actively in-market now.

Build a simple signal priority matrix:

| Signal Type | Why It Matters for Your ICP | Where to Find It | Freshness Window |
|-------------|----------------------------|-------------------|------------------|
| Funding round (Series A-C) | New budget, new priorities, need to show ROI | Crunchbase, LinkedIn, TechCrunch | Last 30 days |
| VP/C-level hire in buyer persona role | New leader = new tools evaluation | LinkedIn job changes, press releases | Last 60 days |
| 3+ job postings in your product's domain | Building team, need infrastructure | LinkedIn Jobs, job boards | Last 14 days |
| Competitor mentioned negatively | Switching intent, open to alternatives | G2 reviews, Reddit, Twitter/X | Last 30 days |
| Complementary tool adoption | Integration opportunity, expanding stack | BuiltWith, job postings mentioning tool | Last 90 days |

**Human action required:** The founder validates which signals actually correlate with deals from their own experience. The agent drafts the matrix; the founder marks which signals they have seen lead to real conversations.

### 2. Manually scan for 30 triggered prospects

Run the `signal-detection` drill in manual mode. The agent searches for prospects exhibiting signals using free tools:
- **LinkedIn:** Search for people who changed jobs in the last 60 days matching your buyer persona title. Filter to companies in your ICP.
- **Crunchbase (free tier):** Search for companies that raised funding in the last 30 days matching your ICP industry and size.
- **LinkedIn Jobs:** Search for companies posting 3+ roles in your product's domain in the last 14 days.
- **G2/Reddit/Twitter/X:** Search for negative mentions of competitors your ICP would use.

For each prospect, record in a spreadsheet or Attio:
- Name, email (find via LinkedIn profile or company website), company, role
- Signal type (funding, hire, hiring spree, competitor churn, tech adoption)
- Signal detail (e.g., "Raised $15M Series B on March 12" or "Hired VP Engineering from [competitor] 3 weeks ago")
- Signal freshness (days since the event)

Target: 30 prospects across at least 3 different signal types. If you cannot find 30 with real signals, the signal sources may not be rich enough for your ICP — note which signal types are scarce.

### 3. Write signal-specific outreach messages

Do NOT use a single template. Each signal type gets a different message structure. The founder writes (or the agent drafts for founder review) one message template per signal type:

**Funding signal template (under 80 words):**
- Open: reference the specific round and amount
- Bridge: name one priority that companies at this stage typically face
- Connect: one sentence on how your product addresses that priority, with a specific metric from a similar customer
- Ask: "Worth a 15-min call this week?"

**New-hire signal template (under 80 words):**
- Open: congratulate on the new role, reference the company by name
- Bridge: name the first challenge people in this role typically tackle
- Connect: one sentence on how a similar leader used your product to solve it
- Ask: offer a specific resource or short call

**Hiring-spree signal template (under 80 words):**
- Open: note the team growth and the specific roles posted
- Bridge: name the infrastructure gap that growing teams hit
- Connect: how your product helps teams at that inflection point
- Ask: "Happy to share how [similar company] handled this — quick call?"

**Competitor-churn signal template (under 80 words):**
- Open: acknowledge the pain point without naming the competitor explicitly ("saw you're evaluating alternatives for [category]")
- Bridge: name the specific gap that drives most switches
- Connect: how your product addresses that gap differently
- Ask: offer a comparison resource or quick demo

**Tech-adoption signal template (under 80 words):**
- Open: reference the tool they recently adopted that integrates with yours
- Bridge: name the workflow that combining the tools unlocks
- Connect: a specific result a similar company achieved with the integration
- Ask: "Want to see the integration in action? 15 min."

Personalize the first line of every message with the specific signal detail for that prospect. The templates are starting points — each email must reference the actual event.

**Human action required:** The founder reviews all outreach copy before sending. Signal-based outreach only works if it reads as genuinely informed, not templated.

### 4. Send manually over 5 days

**Human action required:** The founder sends emails from their primary inbox and/or sends LinkedIn connection requests with the message. Send 6 per day across 5 days. Prioritize by signal freshness — the most recent signals get contacted first, because trigger relevance decays rapidly.

For each send, log in Attio using the `attio-contacts` fundamental:
- Contact record with signal type, signal detail, signal date, send date
- Tag: "trigger-based-outreach-smoke"
- Status: "Prospected"

If using LinkedIn DMs alongside email, note which channel was used for each prospect. Some signals (new hire, job change) are better suited to LinkedIn because the prospect is active on the platform.

### 5. Handle replies within 1 hour

**Human action required:** When a positive reply arrives, the founder responds within 1 hour with 2-3 specific meeting times or a Cal.com booking link. Signal-triggered prospects are in active evaluation mode — response speed directly impacts conversion.

For each reply, update Attio:
- Positive reply: change status to "Replied - Interested", create deal at "Meeting Booked"
- Not now: change status to "Replied - Not Now", set 45-day follow-up (shorter than cold because the signal may still be active)
- Not interested: change status to "Replied - Not Interested"

Track which signal type each reply came from. This data drives the Baseline signal prioritization.

### 6. Evaluate results after 7 days

Count by signal type: sends, replies, meetings. Compute:
- Overall meeting rate = meetings / contacts sent
- Meeting rate per signal type
- Average time from send to reply (by signal type)
- Signal freshness correlation: did more recent signals convert better?

- **PASS (≥ 3 meetings from 30 contacts):** The trigger timing hypothesis is validated. Document: which signal types produced the best conversion rates, optimal signal freshness windows, and which message templates resonated. Proceed to Baseline.
- **MARGINAL (2 meetings):** Close. Analyze which signal types converted and which did not. Narrow to the top 2 signal types and re-run with 20 fresh prospects using only those signals.
- **FAIL (0-1 meetings):** Diagnose: Were the signals real buying indicators for your ICP, or just activity noise? Was the messaging generic despite the signal reference? Were signals too stale (>30 days)? Fix the weakest link and re-run once. If the second run also fails, trigger-based outreach may not match your market — prospects may not have public signals, or your product may not solve an urgent enough problem for signal timing to matter.

## Time Estimate

- ICP definition and signal mapping: 1.5 hours
- Manual signal scanning and prospect list building: 2 hours
- Writing signal-specific templates (5 types): 1 hour
- Sending, monitoring, and replying over 5 days: 1 hour total
- Evaluation and documentation: 0.5 hours
- Total: ~6 hours of active work spread over 1 week

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Log prospects, track signals and replies | Free for up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| Cal.com | Booking link in follow-up replies | Free plan ([cal.com/pricing](https://cal.com/pricing)) |
| LinkedIn (free) | Signal scanning (job changes, hiring) and DM outreach | $0 |
| Crunchbase (free tier) | Funding signal scanning | $0 |
| Founder's primary email | Sending | $0 (existing inbox) |

**Estimated monthly cost for Smoke:** $0

## Drills Referenced

- `icp-definition` — define the target audience and build the signal-to-ICP priority matrix
- `signal-detection` — manual scanning workflow for identifying prospects with active buying signals
