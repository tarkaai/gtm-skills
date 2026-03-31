---
name: stakeholder-consensus-tracker
description: Continuously track stakeholder alignment, detect consensus shifts, and recommend interventions when alignment degrades
category: Sales
tools:
  - Attio
  - PostHog
  - n8n
  - Anthropic
fundamentals:
  - consensus-score-computation
  - attio-deals
  - attio-contacts
  - attio-custom-attributes
  - attio-notes
  - posthog-custom-events
  - posthog-dashboards
  - n8n-workflow-basics
  - n8n-scheduling
  - n8n-triggers
---

# Stakeholder Consensus Tracker

This drill monitors stakeholder alignment across a deal over time. It computes consensus scores after every stakeholder interaction, detects when alignment is improving or degrading, identifies the specific stakeholders or conflicts causing problems, and recommends targeted interventions. The goal: never be surprised by a late-stage blocker.

## Input

- Active deals with stakeholder maps and sentiment data in Attio
- PostHog tracking configured for stakeholder events
- n8n instance for automated monitoring

## Steps

### 1. Compute Consensus Score

After every stakeholder interaction (discovery call, email exchange, demo), run the `consensus-score-computation` fundamental:
- Pull all stakeholder data for the deal from Attio
- Compute the weighted consensus score (0-100)
- Classify: Strong (80-100), Moderate (60-79), Weak (40-59), None (0-39)
- Store the score on the deal record
- Log to PostHog for time-series tracking

### 2. Build Consensus Trajectory Dashboard

Use `posthog-dashboards` to create a "Consensus Trajectory" dashboard:

**Panel 1: Consensus Score Over Time (per deal)**
- Line chart showing consensus score at each computation
- X-axis: date, Y-axis: 0-100, grouped by deal
- Overlay threshold lines at 40 (minimum for proposal) and 80 (strong consensus)

**Panel 2: Stakeholder Support Distribution**
- Stacked bar chart per deal showing count of Champions, Supporters, Neutrals, Skeptics, Blockers
- Deals with more Blockers than Supporters are flagged

**Panel 3: Coverage Completeness**
- Table showing each deal with: stakeholder count, engaged %, discovery complete %, Economic Buyer status
- Sort by lowest coverage first

**Panel 4: Consensus Change Alerts**
- List of deals where consensus score dropped >10 points in the last 7 days

### 3. Build Consensus Monitoring Workflow

Create an n8n workflow on a twice-weekly cron (Monday and Thursday):

1. For each active deal at Connected+ stage, compute the current consensus score
2. Compare to the prior computation:
   - **Improving** (score increased >5 points): log as healthy, no action
   - **Stable** (score changed <5 points): log as stable
   - **Degrading** (score dropped >5 points): trigger intervention analysis
   - **Critical** (score dropped >15 points OR dropped below 40): urgent alert

3. For degrading deals, diagnose the cause:
   - Which stakeholder's sentiment changed?
   - Was a new Blocker identified?
   - Did an engaged stakeholder go silent?
   - Was a new conflict area discovered?

### 4. Generate Intervention Recommendations

For each degrading deal, use Claude to generate a targeted intervention plan:

```
POST https://api.anthropic.com/v1/messages
Body: {
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1024,
  "messages": [{"role": "user", "content": "A B2B deal's consensus score dropped from {old_score} to {new_score}.\n\nCause: {diagnosis}\n\nStakeholder map:\n{stakeholder_summary_with_sentiments}\n\nConflict areas: {conflicts}\nUnresolved concerns: {unresolved}\n\nGenerate a 3-step intervention plan to recover consensus. For each step specify: what to do, who to target, what message to send, and expected outcome.\n\nReturn JSON: [{\"step\": 1, \"action\": \"...\", \"target_stakeholder\": \"...\", \"message_approach\": \"...\", \"expected_outcome\": \"...\"}]"}]
}
```

Store the intervention plan in Attio as a note on the deal, tagged `consensus-intervention`.

### 5. Track Intervention Effectiveness

After an intervention is executed:
1. Re-compute consensus score at the next monitoring cycle
2. If score recovered: log the intervention as successful, tag the approach for future reuse
3. If score did not recover: escalate to human review with full context
4. Track across all deals: which intervention types have the highest success rate?

### 6. Pre-Proposal Gate Check

Create an n8n workflow triggered when a deal's stage changes to "Proposed":
1. Compute the current consensus score
2. If score < 60: block the stage change (or alert that proposal is premature)
3. If any stakeholder with influence_score >= 7 is still classified as Blocker: alert
4. If the Economic Buyer has never had a direct discovery call: alert
5. Generate a "Proposal Readiness Report" showing all stakeholder positions and remaining risks

## Output

- Consensus scores computed and stored after every stakeholder interaction
- Time-series consensus trajectory in PostHog
- Automated monitoring with degradation alerts
- AI-generated intervention plans for at-risk deals
- Pre-proposal gate check preventing premature proposals
- Intervention effectiveness tracking across all deals

## Triggers

Run this drill:
- After every `stakeholder-discovery-call` drill completes
- Twice-weekly via n8n cron for all active deals
- When a deal stage changes (especially toward Proposed or Aligned)
