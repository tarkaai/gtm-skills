---
name: change-management-objection-smoke
description: >
  Change Management Objection Handling — Smoke Test. Manually diagnose change resistance
  root causes on 5+ deals, generate status quo cost analyses, and deliver tailored change
  support talking points. Validate that structured change objection handling advances
  deals that would otherwise stall at status quo.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: ">=5 change objections diagnosed and handled in 1 week with >=60% accepting change support plan and advancing to next stage"
kpis: ["Change objection resolution rate", "Root cause diagnosis accuracy", "Status quo cost acceptance rate", "Deal progression rate"]
slug: "change-management-objection"
install: "npx gtm-skills add sales/connected/change-management-objection"
drills:
  - threshold-engine
---

# Change Management Objection Handling — Smoke Test

> **Stage:** Sales > Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Outcomes

Handle change management objections on >= 5 deals in 1 week using structured diagnosis and tailored interventions. Achieve >= 60% of prospects accepting a change support plan and advancing to the next pipeline stage. This proves that diagnosing resistance root causes and addressing them with targeted evidence works better than generic reassurance.

## Leading Indicators

- Call prep documents generated for each prospect with predicted resistance factors
- Resistance root cause identified within the first 15 minutes of each conversation
- Prospects engage with the status quo cost framing (ask questions, push back on numbers, request details)
- At least 3 out of 5 prospects accept a pilot, phased rollout, or training preview
- Deals that were stalled on "we're happy with what we have" re-enter active pipeline

## Instructions

### 1. Identify 5+ deals with change management objections

Review your active pipeline in Attio for deals exhibiting change resistance signals:
- Prospect said "we're happy with our current solution"
- Prospect mentioned switching costs, training burden, or past migration failures
- Deal stalled after the prospect learned they would need to change tools
- Prospect asked "why should we switch from X?"

If you have fewer than 5 deals with explicit change resistance, include deals where resistance is likely based on:
- Long tenure on current solution (> 3 years)
- Large team using the current tool
- Enterprise accounts with complex integrations

### 2. Prepare for each conversation

Run the the change objection call prep workflow (see instructions below) drill for each deal. The drill:
- Pulls deal context and current solution info from Attio
- Enriches the incumbent via Clay (pricing, switching barriers, common complaints)
- Predicts likely resistance root causes based on company profile
- Generates a status quo cost estimate (staying vs. switching)
- Produces a call prep document with discovery questions and talking points

Review the call prep before each conversation. Internalize the top 2-3 predicted resistance factors and the status quo cost highlights. The prep tells you what to ask, not what to say.

### 3. Conduct the change management conversations

**Human action required:** Have 5+ conversations where you diagnose and address change resistance. Follow these rules:

- **Diagnose before prescribing.** Ask questions to understand the root cause before offering solutions. "What's your biggest concern about making a change?" is better than "Don't worry, we make it easy."
- **Name the root cause.** Once identified, mirror it back: "It sounds like your main concern is that the data migration could go wrong, given your 5 years of records in the current system. Is that right?"
- **Quantify the status quo.** Share the cost-of-staying analysis: "Based on what you told me about [pain], staying on [current solution] is costing you roughly $X per month. Over 3 years, that's $Y."
- **Match the intervention to the cause.** Do not offer a generic "we'll help you transition." Offer the specific support that addresses their concern:
  - disruption_fear -> phased rollout with parallel running period
  - past_failure -> case study of similar company that succeeded + reference call
  - training_burden -> training program overview with total hours per user
  - data_migration -> migration scope document with rollback plan
  - team_pushback -> champion enablement materials for internal communication
  - sunk_cost_bias -> forward-looking cost comparison eliminating sunk cost framing
- **Propose a concrete next step.** "Would it help if I put together a migration plan showing exactly what the first 4 weeks look like?" or "Can I connect you with [customer] who was in a similar situation?"
- **Log everything.** After each conversation, note: root cause diagnosed, intervention offered, prospect response, next step agreed.

### 4. Log results after each conversation

Within 1 hour of each conversation, log the following in Attio as a note on the deal:

```markdown
## Change Objection Handling — {date}
### Prospect: {company} / {contact name, title}

### Current Solution
- Using: {solution} for {years} years
- Annual spend: ${estimate}

### Resistance Diagnosed
| Root Cause | Severity (1-10) | Key Quote | Addressed? |
|-----------|-----------------|-----------|------------|
| {root_cause} | {severity} | "{prospect quote}" | Yes/Partial/No |

### Intervention Delivered
- Approach: {what you offered: pilot, case study, cost comparison, etc.}
- Prospect response: {engaged, skeptical, dismissed, requested more info}
- Change support plan accepted: Yes/No

### Status Quo Cost Framing
- Presented cost of staying: ${annual} / ${3_year}
- Prospect reaction: {accepted numbers, pushed back, asked for details}

### Outcome
- Next step: {agreed action}
- Deal advanced to next stage: Yes/No
- Estimated close impact: {moved closer, neutral, lost ground}
```

### 5. Evaluate against threshold

Run the `threshold-engine` drill to evaluate your results. The threshold engine checks:
- Did you handle change objections on >= 5 deals?
- Did >= 60% accept a change support plan (pilot, phased rollout, training preview, or reference call)?
- Did >= 60% of handled deals advance to the next pipeline stage?

If **PASS**: You have validated that structured change objection handling works. The root cause diagnosis approach consistently uncovers addressable concerns, and tailored interventions move deals forward. Proceed to Baseline to automate extraction and response.

If **FAIL**: Diagnose why. Common causes:
- **Low diagnosis accuracy:** Your questions are too generic. Refine the root cause discovery questions in the call prep.
- **Low plan acceptance:** The interventions don't match the concerns. Check whether you're diagnosing correctly but prescribing wrong, or whether the concerns are genuinely unaddressable.
- **Low deal advancement:** Plans are accepted but deals don't move. The change support may need to be more concrete (actual migration timeline, specific case study, live reference call).

Re-run the Smoke test with adjustments.

## Time Estimate

- Call prep (5 deals x 30 min): 2.5 hours
- Conversations (5 x 30 min average): 2.5 hours
- Post-conversation logging (5 x 20 min): 1.5 hours
- Threshold evaluation: 1.5 hours
- **Total: ~8 hours over 1 week**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal records, change resistance data, conversation notes | Free tier (up to 3 users); Plus $29/user/mo |
| Cal.com | Schedule follow-up calls | Free tier (1 user); Teams $15/user/mo |
| Clay | Enrich incumbent solution and company context | Free tier (100 credits); Launch $185/mo |
| Fireflies | Record and transcribe calls for post-call review | Free (800 min/mo); Pro $10/user/mo (annual) |
| PostHog | Track change objection events | Free tier (1M events/mo) |
| Claude API | Generate status quo cost analysis and call prep | Sonnet: $3/$15 per M input/output tokens |

**Estimated play-specific cost at Smoke:** Free (all tools have free tiers sufficient for 5 conversations)

## Drills Referenced

- the change objection call prep workflow (see instructions below) — Research the incumbent, predict resistance root causes, generate status quo cost estimate and discovery questions
- `threshold-engine` — Evaluate results against pass/fail criteria
