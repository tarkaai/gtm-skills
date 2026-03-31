---
name: success-criteria-workshop
description: Structured workflow to co-create measurable success criteria with prospects using call transcripts, AI extraction, and mutual success plan generation
category: Sales
tools:
  - Anthropic
  - Attio
  - Fireflies
  - PostHog
  - Cal.com
fundamentals:
  - success-criteria-extraction
  - fireflies-transcription
  - fireflies-action-items
  - attio-deals
  - attio-custom-attributes
  - attio-notes
  - posthog-custom-events
  - calcom-booking-links
---

# Success Criteria Workshop

This drill executes the success criteria definition conversation with a prospect. It prepares the agent for the call by analyzing prior discovery transcripts, runs AI extraction during/after the call, and produces a mutual success plan document that both parties can agree on.

## Input

- Active deal in Attio at Connected stage with at least 1 prior discovery call recorded
- Fireflies transcript of the discovery call(s)
- Product capabilities document (what can be measured and delivered)
- Historical success criteria achievement data from Attio (optional but improves quality at Baseline+)

## Steps

### 1. Pre-Call Preparation

Query Attio for the deal record. Pull: company name, industry, headcount, current tools, deal value, champion name and title, all notes from prior interactions.

Retrieve the discovery call transcript from Fireflies using `fireflies-transcription`. If multiple calls exist, retrieve all and concatenate chronologically.

Run `success-criteria-extraction` with the transcript and deal context. This generates a draft set of 3-5 success criteria with achievability scores.

Review the AI-generated criteria:
- Remove any criterion with `achievability_score < 30` (too risky to propose)
- Flag criteria with `achievability_score` between 30-60 as "stretch goals" that need careful framing
- Criteria with `achievability_score > 60` are safe to propose directly

Store the draft criteria in Attio as a note tagged `success-criteria-draft`.

### 2. Schedule and Prepare the Workshop Call

Use `calcom-booking-links` to generate a 30-minute "Success Criteria Workshop" booking link. The call purpose: collaboratively define what success looks like for this prospect.

Prepare the call agenda:
1. Review their stated goals (2 minutes)
2. Propose specific metrics and targets for each goal (10 minutes)
3. Align on timelines and measurement methods (10 minutes)
4. Identify who on their team will measure each criterion (5 minutes)
5. Agree on review cadence (3 minutes)

Send the booking link to the champion via Attio email activity log.

**Human action required:** The founder conducts the 30-minute workshop call. The agent prepares talking points and a printable draft of proposed criteria, but the human runs the conversation.

### 3. Post-Call Extraction and Refinement

After the call, retrieve the Fireflies transcript using `fireflies-transcription`.

Run `success-criteria-extraction` again with the workshop call transcript. Compare the refined criteria against the pre-call draft:
- Add any new criteria the prospect raised
- Update targets and timelines based on what was discussed
- Recalculate achievability scores with the updated context

Use `fireflies-action-items` to extract any action items from the call (e.g., "prospect will provide baseline data for metric X").

### 4. Generate the Mutual Success Plan

Using the finalized criteria, generate a structured mutual success plan. Create an Attio note tagged `mutual-success-plan` with:

```
## Mutual Success Plan: {Company Name}
Date: {date}
Participants: {founder_name}, {champion_name}

### Success Criteria

| # | Goal | Metric | Target | Timeline | Baseline | Measured By |
|---|------|--------|--------|----------|----------|-------------|
| 1 | {prospect_goal} | {metric} | {target} | {timeline} | {baseline} | {measured_by} |
...

### Review Schedule
- {timeline_1}: First checkpoint for criteria 1, 2
- {timeline_2}: Full review of all criteria
- {final_date}: Final success evaluation

### Next Steps
{action_items from Fireflies extraction}

### Achievability Assessment (internal only — do not share)
| Criterion | Score | Risk Level | Notes |
|-----------|-------|------------|-------|
...
```

### 5. Track in CRM and Analytics

Update the Attio deal record using `attio-custom-attributes`:
- `success_criteria_status` = "defined" | "draft" | "pending_agreement"
- `success_criteria_count` = number of criteria
- `avg_achievability_score` = average across all criteria
- `mutual_plan_date` = date the plan was agreed
- `next_review_date` = first review checkpoint

Fire PostHog events using `posthog-custom-events`:
- `success_criteria_defined`: properties = `deal_id`, `criteria_count`, `avg_achievability_score`, `categories`
- `mutual_success_plan_created`: properties = `deal_id`, `stakeholder_count`, `review_cadence`

## Output

- Mutual success plan document stored in Attio
- Deal record updated with success criteria metadata
- PostHog events fired for funnel tracking
- Internal achievability assessment for the sales team

## Triggers

- Run once per deal when it reaches the Connected stage and has at least 1 discovery call recorded
- Re-run if criteria need updating (e.g., after a technical deep dive reveals new constraints)
