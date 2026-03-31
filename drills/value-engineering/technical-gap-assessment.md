---
name: technical-gap-assessment
description: Assess prospect's technical requirements against product capabilities, classify gaps by severity, and generate response strategies per gap type
category: Value Engineering
tools:
  - Attio
  - Anthropic
  - Clay
  - Fireflies
  - PostHog
fundamentals:
  - call-transcript-tech-requirements-extraction
  - call-transcript-objection-extraction
  - tech-stack-detection
  - clay-claygent
  - clay-enrichment-waterfall
  - attio-deals
  - attio-notes
  - attio-custom-attributes
  - posthog-custom-events
---

# Technical Gap Assessment

This drill takes a prospect's stated technical requirements (from discovery calls, emails, or RFPs) and systematically evaluates each against your product's current capabilities. It classifies every gap by type and severity, then generates the appropriate response strategy: roadmap commitment, workaround demonstration, custom development scope, or honest no-fit acknowledgment.

## Input

- Deal record in Attio with at least one technical discovery call transcribed
- Technical requirements data (from `call-transcript-tech-requirements-extraction`)
- Product capability matrix (stored in Attio or a shared document the agent can read)

## Steps

### 1. Extract technical requirements from all deal interactions

Query Attio for the deal record and all associated notes, call transcripts, and email threads. For each call transcript, run `call-transcript-tech-requirements-extraction` if not already done. Aggregate all technical requirements into a single list.

Deduplicate: if the same requirement appears in multiple calls, keep the most specific version and note how many times it was raised (frequency indicates importance).

### 2. Build the product capability matrix lookup

Query your product capability reference. This should be a structured document or Attio object listing:

```json
{
  "capabilities": [
    {
      "category": "integrations",
      "name": "Salesforce native integration",
      "status": "available",
      "details": "Bi-directional sync, real-time, supports custom objects"
    },
    {
      "category": "integrations",
      "name": "SAP integration",
      "status": "roadmap_q3_2026",
      "details": "Planned API integration, basic data sync"
    },
    {
      "category": "security",
      "name": "SOC2 Type II",
      "status": "available",
      "details": "Certified since 2025, annual renewal"
    },
    {
      "category": "security",
      "name": "HIPAA",
      "status": "not_planned",
      "details": ""
    }
  ]
}
```

If no structured capability matrix exists, prompt the founder to build one. **Human action required:** Create or validate the product capability matrix.

### 3. Match requirements to capabilities

For each technical requirement from the prospect, find the matching capability. Send to Claude:

```json
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 4000,
  "messages": [{
    "role": "user",
    "content": "Match each prospect requirement to our product capabilities and classify the gap.\n\nProspect requirements:\n{requirements_json}\n\nOur capabilities:\n{capabilities_json}\n\nFor each requirement, return JSON:\n{\n  \"requirement\": \"what they asked for\",\n  \"category\": \"integration|security|performance|infrastructure|data_migration|feature\",\n  \"prospect_priority\": \"must_have|nice_to_have\",\n  \"times_raised\": 0,\n  \"matching_capability\": \"our capability or null\",\n  \"gap_type\": \"no_gap|roadmap|workaround_available|custom_dev_required|partner_solution|no_fit\",\n  \"gap_severity\": \"none|low|medium|high|dealbreaker\",\n  \"response_strategy\": \"demonstrate|commit_timeline|show_workaround|scope_custom_work|propose_partner|acknowledge_gap\",\n  \"response_detail\": \"specific response to give the prospect\",\n  \"proof_needed\": \"architecture_diagram|benchmark_data|customer_reference|live_demo|documentation|none\",\n  \"risk_level\": \"low|medium|high\",\n  \"risk_reason\": \"why this requirement poses risk if any\"\n}"
  }]
}
```

### 4. Classify overall technical fit

Compute a composite technical fit assessment:

- Count gaps by severity: dealbreaker, high, medium, low, none
- If any `must_have` requirement has `gap_type: no_fit` -> overall verdict: `no_fit`
- If any `must_have` requirement has `gap_type: custom_dev_required` and dev timeline exceeds prospect's timeline -> overall verdict: `weak_fit`
- If all `must_have` requirements are met (no_gap, roadmap within timeline, or workaround_available) -> overall verdict: `strong_fit` or `moderate_fit`

### 5. Generate the gap response plan

For each gap that is not `no_gap`, generate the specific response:

**Roadmap gaps:** Pull the planned delivery date. Frame as: "This is on our roadmap for {quarter}. Here is the product brief. We can include a contractual commitment to deliver by {date}."

**Workaround gaps:** Document the alternative approach step by step. Prepare a live demonstration or architecture diagram showing how the workaround achieves the same outcome.

**Custom development gaps:** Scope the work: estimated effort, timeline, cost (if any), and whether it can be included in the deal or requires a separate SOW.

**Partner solution gaps:** Identify the partner or third-party tool that fills the gap. Prepare an integration architecture showing how it works together.

**No-fit gaps:** Acknowledge honestly. Frame as: "This is not something we do today or plan to build. Here is what we recommend instead." Losing a deal honestly protects reputation and generates referrals.

### 6. Store results and create response brief

Push structured gap assessment to Attio:
- Set `tech_gap_count: {n}` and `tech_gap_severity_max: {severity}` on the deal
- Create a note with the full gap assessment and response plan
- Set `tech_fit_verdict: {verdict}`
- Tag each gap with its response strategy

Generate a one-page response brief:

```
## Technical Gap Response Plan — {Company Name}

### Overall Fit: {verdict} ({gap_count} gaps identified)

### Dealbreaker Gaps (must resolve to proceed):
- {gap}: {response_strategy} — {response_detail}

### High Gaps (address proactively):
- {gap}: {response_strategy} — {response_detail}

### Medium Gaps (address if raised):
- {gap}: {response_strategy} — {response_detail}

### Proof Points Needed:
- {proof_type} for {requirement}

### Recommended Next Step:
{next_step based on gap analysis}
```

### 7. Log the assessment event

Fire a PostHog event:
```json
{
  "event": "tech_gap_assessment_completed",
  "properties": {
    "deal_id": "...",
    "company": "...",
    "total_requirements": 12,
    "gap_count": 4,
    "dealbreaker_count": 0,
    "high_gap_count": 1,
    "fit_verdict": "moderate_fit",
    "response_strategies_used": ["roadmap", "workaround_available", "custom_dev_required"]
  }
}
```

## Output

- Structured gap assessment stored in Attio
- Response plan with specific strategies per gap
- Technical fit verdict and risk score on the deal record
- One-page response brief for the technical call
- PostHog event for tracking

## Triggers

Run after every technical discovery call. Re-run when the prospect raises new requirements or when product capabilities change (new feature shipped, roadmap updated).
