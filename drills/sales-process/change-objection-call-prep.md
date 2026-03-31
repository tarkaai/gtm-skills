---
name: change-objection-call-prep
description: Research the prospect's current solution, diagnose likely change resistance factors, generate status quo cost estimates and change support talking points before a call
category: Discovery
tools:
  - Attio
  - Clay
  - Anthropic
  - Fireflies
  - Cal.com
fundamentals:
  - attio-deals
  - attio-notes
  - clay-company-search
  - clay-enrichment-waterfall
  - change-resistance-diagnosis
  - status-quo-cost-analysis
  - call-brief-generation
  - fireflies-transcription
---

# Change Objection Call Prep

This drill prepares the seller for a conversation where the prospect has expressed resistance to changing from their current solution. It researches the incumbent, estimates switching costs vs. staying costs, predicts likely resistance root causes, and generates a prep document with talking points and evidence.

## Input

- Deal record in Attio with known current solution and any prior notes about change resistance
- Scheduled call in Cal.com (discovery, evaluation, or follow-up)
- Prior call transcripts if available (from Fireflies)

## Steps

### 1. Pull deal context from Attio

Using `attio-deals`, retrieve the deal record including:
- Company name, size, industry
- Current solution name and estimated spend
- Years on current solution
- Any prior change resistance notes
- Stakeholder list with roles
- Pain data from prior discovery calls
- Deal value and stage

If `current_solution` is not populated on the deal, proceed to step 2 for enrichment. If it is populated, skip to step 3.

### 2. Research the current solution

Using `clay-company-search` and `clay-enrichment-waterfall`:
1. Search Clay for the prospect company to pull tech stack data
2. Identify the specific product/tool in the relevant category
3. Research the incumbent: pricing model, contract terms, migration difficulty, common complaints
4. Pull any public reviews from G2/Capterra mentioning switching difficulty

Store the findings on the Attio deal record using `attio-notes`:
```markdown
## Incumbent Research — {date}
- Current solution: {name}
- Estimated annual spend: ${estimate}
- Contract type: {annual/monthly/enterprise}
- Known switching barriers: {data migration complexity, training investment, integrations, customizations}
- Common complaints (from reviews): {top 3 from G2/Capterra}
```

### 3. Predict resistance root causes

If prior call transcripts exist, use `change-resistance-diagnosis` to extract resistance signals from the transcript.

If no transcripts exist yet (first call), generate predicted resistance factors based on enrichment data:
- Company on current solution > 3 years -> predict `sunk_cost_bias` and `training_burden`
- Enterprise company (>500 employees) -> predict `team_pushback` and `political_dynamics`
- Regulated industry -> predict `compliance_risk`
- Prior call notes mention failed migration -> predict `past_failure`
- Deep integrations with current solution -> predict `vendor_lock_in`

### 4. Generate status quo cost estimate

Run `status-quo-cost-analysis` with available data. At Smoke level, this will use estimates and benchmarks rather than deep discovery data. The output includes:
- Total cost of staying (direct + hidden + opportunity)
- Total cost of switching (one-time + annual + productivity dip)
- Break-even month
- Cost of delay per month

### 5. Build the call prep document

Using `call-brief-generation`, generate a prep document tailored to change management:

```markdown
## Change Management Call Prep — {company_name} — {date}

### Current Situation
- Using: {current_solution} for {years} years
- Estimated annual spend: ${current_spend}
- Key stakeholders: {list with roles and change stance if known}

### Predicted Resistance Factors
1. {root_cause_1}: {why predicted, severity estimate}
2. {root_cause_2}: {why predicted, severity estimate}

### Status Quo Cost Highlights
- Staying costs: ${annual_staying}/year (${3_year_staying} over 3 years)
- Switching costs: ${year_1_switching} in year 1
- Break-even: Month {break_even_month}
- **Cost of delay: ${cost_of_delay}/month**

### Discovery Questions to Diagnose Resistance
1. "What's been your experience with switching tools in the past?" (probes past_failure)
2. "If you decided to move forward, what would the rollout look like internally?" (probes disruption_fear)
3. "Who else would need to be involved in this decision?" (probes political_dynamics)
4. "What's your team's relationship with {current_solution}?" (probes team_pushback)
5. "How much have you customized the current setup?" (probes vendor_lock_in)

### Change Support Talking Points
- "We've helped {X} companies migrate from {similar_solution} — average transition was {Y} weeks"
- "We offer a phased rollout where you can run both systems in parallel until you're confident"
- "Our implementation team handles the data migration — we guarantee data integrity"

### Assets to Reference
- Migration case study: {relevant industry/size match}
- Implementation timeline template
- Training program overview
- ROI comparison showing cost of delay

### Call Objective
Diagnose the specific root causes of change resistance. Do NOT try to overcome them on this call.
Listen, probe, understand. The prep document helps you ask the right questions, not deliver answers.
```

### 6. Store and verify

1. Store the prep document as an Attio note on the deal
2. Verify Fireflies is configured to record the upcoming call using `fireflies-transcription`
3. Log PostHog event: `change_objection_call_prepped` with properties: deal_id, predicted_root_causes, status_quo_cost_estimate

## Output

- Call prep document stored in Attio with predicted resistance, cost analysis, and discovery questions
- Fireflies recording verified for post-call extraction
- PostHog event logged

## Triggers

Run manually before any call where change resistance is expected. At Baseline and above, trigger automatically 24 hours before scheduled Cal.com events on deals flagged with change resistance.
