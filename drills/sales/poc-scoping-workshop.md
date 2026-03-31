---
name: poc-scoping-workshop
description: Define POC scope, success criteria, milestones, stakeholder map, and decision framework from discovery data
category: Sales
tools:
  - Attio
  - Anthropic
  - Fireflies
  - Cal.com
fundamentals:
  - poc-success-criteria-template
  - attio-deals
  - attio-notes
  - attio-custom-attributes
  - fireflies-transcription
  - fireflies-action-items
  - calcom-booking-links
  - calcom-event-types
---

# POC Scoping Workshop

This drill takes a deal that has reached the Aligned stage and produces a complete POC plan: success criteria, milestones, stakeholder responsibilities, timeline, and scheduled kickoff. It runs once per deal and produces the foundation document that governs the entire POC.

## Input

- An Attio deal at the Aligned stage
- At least one completed discovery call with a Fireflies transcript
- Champion and economic buyer identified in CRM
- Product sandbox infrastructure available (for environment provisioning in later steps)

## Steps

### 1. Extract discovery context

Pull the deal from Attio using `attio-deals`. Then retrieve the discovery call transcript using `fireflies-transcription`:

1. Search Fireflies for the most recent transcript associated with the deal's contact email.
2. Run `fireflies-action-items` to extract structured action items, pain points, and decisions from the call.
3. From the transcript, extract:
   - Specific use cases the prospect wants to validate
   - Current workflow pain points with quantified impact (e.g., "takes 4 hours per week")
   - Technical requirements or integration needs mentioned
   - Decision timeline and process discussed
   - Stakeholders mentioned by name and role
   - Competitive alternatives being evaluated

Store the extracted context as an Attio note on the deal.

### 2. Generate POC success criteria

Run the `poc-success-criteria-template` fundamental with the extracted discovery context. This produces a structured JSON document containing:
- 3-5 must-have success criteria with measurable targets
- 1-2 nice-to-have criteria
- Milestone schedule distributed across the POC duration
- Stakeholder responsibilities for both sides
- Decision framework with named decision maker and date

Review the output. Verify each criterion directly maps to a pain point or use case from discovery. If a criterion is generic (not tied to the prospect's stated needs), regenerate with more specific context.

### 3. Build the stakeholder map

From the discovery transcript and Attio deal contacts, map the POC stakeholders:

1. **Champion**: The internal advocate running the evaluation day-to-day. Must have at least one identified.
2. **Technical evaluator**: The person who will test the product hands-on. May be the champion.
3. **Economic buyer**: The person who approves the purchase. Must be named in the decision framework.
4. **Blocker contacts**: Anyone whose sign-off is needed (IT security, procurement, legal).

Update the Attio deal with stakeholder roles using `attio-custom-attributes`:
- `poc_champion`, `poc_technical_evaluator`, `poc_economic_buyer`

If the economic buyer is not identified, flag this as a pre-POC blocker. The POC should not launch without a named decision maker.

### 4. Determine POC duration and type

Based on the complexity of the evaluation:

| Criteria Count | Integration Needs | Recommended Duration |
|---------------|-------------------|---------------------|
| 3-4, no integrations | None | 7 days |
| 4-5, basic integrations | 1-2 | 14 days |
| 5+, complex integrations | 3+ | 21 days |
| Enterprise with security review | Any | 21-30 days |

Set `poc_duration_days` and `poc_type` (standard / extended / enterprise) on the Attio deal.

### 5. Schedule the kickoff call

Using `calcom-booking-links`, generate a POC kickoff meeting link:

1. Create a Cal.com event type for "POC Kickoff" (45 minutes) using `calcom-event-types` if it does not already exist.
2. Generate a booking link with pre-filled context: prospect name, company, POC title.
3. Send the booking link to the champion via the deal owner's email.

The kickoff call agenda:
- Review and confirm success criteria (10 min)
- Walk through the POC environment (15 min)
- Confirm milestone schedule and check-in cadence (10 min)
- Identify potential blockers and assign owners (10 min)

### 6. Prepare the POC kickoff document

Compile everything into a single POC kickoff document and store it as an Attio note:

```
POC: {company_name} - {primary_use_case}
Duration: {duration} days ({start_date} to {end_date})
Champion: {champion_name} ({champion_email})
Decision Maker: {buyer_name} ({buyer_title})
Decision Date: {decision_date}

SUCCESS CRITERIA:
1. [must-have] {criterion_1} — Target: {target_1}
2. [must-have] {criterion_2} — Target: {target_2}
...

MILESTONES:
Day 1: {milestone_1} (Owner: {owner})
Day {n}: {milestone_2} (Owner: {owner})
...

CHECK-INS:
- Kickoff: {kickoff_date} (Cal.com link: {link})
- Mid-point: Day {mid} (Cal.com link: {link})
- Final review: Day {final} (Cal.com link: {link})

DECISION FRAMEWORK:
Pass if: {pass_criteria}
Fail if: {fail_criteria}
Decision by: {decision_date} — {decision_maker}
```

Fire a `poc_scoped` PostHog event with: `deal_id`, `criteria_count`, `duration_days`, `stakeholder_count`.

## Output

- POC success criteria document stored in Attio
- Stakeholder map with roles assigned
- POC duration and type determined
- Kickoff call scheduled via Cal.com
- PostHog event `poc_scoped` fired

## Triggers

Run once per deal when the deal owner decides a POC is the right next step. Typically after a discovery call at the Aligned stage. Manual trigger by the agent or deal owner.
