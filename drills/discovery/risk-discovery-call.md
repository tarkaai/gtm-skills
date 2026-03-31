---
name: risk-discovery-call
description: Post-call processing for risk discovery -- transcribe, extract risks by category, score severity and likelihood, log to CRM, route mitigations
category: Discovery
tools:
  - Fireflies
  - Attio
  - Anthropic
  - PostHog
fundamentals:
  - fireflies-transcription
  - fireflies-action-items
  - call-transcript-risk-extraction
  - attio-deals
  - attio-notes
  - posthog-custom-events
---

# Risk Discovery Call

This drill handles everything that happens after a discovery/evaluation call where risk probing occurred: transcript retrieval, automated risk extraction across all five categories, severity/likelihood scoring, CRM logging, comparison to pre-call predictions, and routing to mitigation workflows. It converts a conversation into structured, actionable risk intelligence.

## Input

- Completed call with Fireflies recording
- Deal record in Attio (ideally with `risk-prep` note from `risk-discovery-call-prep`)
- Call risk prep document with predicted risks (optional but recommended)

## Steps

### 1. Retrieve and verify transcript

Wait for Fireflies to process the transcript (typically 5-15 minutes post-call). Poll the Fireflies API:

```graphql
query {
  transcripts(filter: { date_from: "{today}" }) {
    id
    title
    duration
    sentences { speaker_name text start_time end_time }
    summary
    action_items
  }
}
```

Match the transcript to the deal by meeting title or attendee email. If no transcript found within 30 minutes, alert the caller and fall back to manual risk entry.

Validate transcript has sufficient content: minimum 150 words of prospect speech. If below this threshold, the call had limited discovery value -- log it but skip automated extraction.

### 2. Extract risks from transcript

Run the `call-transcript-risk-extraction` fundamental with the full transcript text. This returns:
- Array of risks with categories, severity/likelihood scores, and supporting quotes
- Implicit risks hinted at but not stated
- Risk discovery gaps (categories not explored)
- Seller risk-handling quality assessment

### 3. Score each risk

For each extracted risk, compute the composite risk score:
- `risk_score = severity * likelihood` (scale 1-100)
- Classify: **Low** (1-24), **Medium** (25-49), **High** (50-79), **Critical** (80-100)
- Flag risks where `blocks_decision` is true -- these must be addressed before proposal

### 4. Calculate aggregate risk metrics

Compute:
- **Total risk score:** Sum of all individual `risk_score` values
- **Risk density:** `risk_count / call_duration_minutes`
- **Mitigation coverage:** Risks with `response_effectiveness` in ["resolved", "partially_resolved"] / `risk_count`
- **Decision-blocking risk count:** Count where `blocks_decision` is true
- **Category distribution:** { "financial": 2, "technical": 1, "organizational": 3, "timeline": 0, "vendor": 1 }
- **Unaddressed critical risks:** Count where risk_score >= 50 AND `response_effectiveness` is "unaddressed"

### 5. Compare to pre-call predictions

Pull the `risk-prep` note from Attio. Compare:
- Which predicted risks were confirmed? (Predicted and found)
- Which predicted risks were not mentioned? (Predicted but absent -- may need probing)
- Which risks were unexpected? (Found but not predicted -- enrichment missed signals)

This comparison calibrates the pre-call research over time. Log the prediction hit rate.

### 6. Update CRM with risk data

Using `attio-deals`, update the deal record:
```json
{
  "risk_count": 5,
  "unaddressed_risk_count": 2,
  "total_risk_score": 186,
  "dominant_risk_category": "organizational",
  "deal_risk_level": "high",
  "mitigation_coverage": 0.6,
  "decision_blocking_risks": 2,
  "risk_discovery_date": "2026-03-30",
  "risk_prediction_hit_rate": 0.7
}
```

Using `attio-notes`, create a structured note:

```markdown
## Risk Discovery Results -- {date}
### Prospect: {company_name} / {contact_name}

### Risk Summary
| # | Risk | Category | Severity | Likelihood | Score | Blocks Decision | Status |
|---|------|----------|----------|------------|-------|-----------------|--------|
| 1 | {summary} | {category} | {sev}/10 | {like}/10 | {score} | {yes/no} | {resolved/unaddressed} |
| 2 | ... | ... | ... | ... | ... | ... | ... |

**Total Risk Score:** {total}
**Mitigation Coverage:** {coverage}%
**Decision-Blocking Risks:** {count}

### Key Concern Quotes
- "{most critical concern quote}" -- on {category} risk
- "{second quote}" -- on {category} risk

### Implicit Risks (Hinted But Not Stated)
- {implicit risk} -- probe with: "{suggested question}"

### Categories Not Explored
- {gap category} -- probe in next conversation

### Seller Risk Handling
- Quality: {strong/adequate/weak}
- Addressed {n} of {total} risks during the call

### Mitigation Actions Needed
- [ ] {Risk 1}: Send {mitigation_type} within 24 hours
- [ ] {Risk 2}: Schedule {reference_call/demo} this week
- [ ] {Risk 3}: Prepare {documentation} for next meeting

### Next Steps
- {action items from Fireflies}
- Follow up on unaddressed risks within 48 hours
```

### 7. Fire tracking events

Using `posthog-custom-events`, log:

```json
{
  "event": "risk_discovery_call_completed",
  "properties": {
    "deal_id": "...",
    "risk_count": 5,
    "unaddressed_risk_count": 2,
    "total_risk_score": 186,
    "dominant_risk_category": "organizational",
    "deal_risk_level": "high",
    "mitigation_coverage": 0.6,
    "decision_blocking_risks": 2,
    "risk_prediction_hit_rate": 0.7,
    "call_duration_minutes": 38,
    "seller_risk_handling": "adequate"
  }
}
```

### 8. Route based on results

- **Low risk (total score < 50, no decision-blockers):** Log and proceed. The deal has minimal risk exposure. Focus on advancing.
- **Medium risk (score 50-149 or 1 decision-blocker):** Trigger `risk-mitigation-delivery` drill within 24 hours for all unaddressed risks. Schedule mitigation review before next call.
- **High risk (score 150+ or 2+ decision-blockers):** Urgent. Trigger `risk-mitigation-delivery` immediately. Alert founder/sales lead. Schedule dedicated risk-mitigation call within 1 week.
- **Critical (any single risk with score >= 80):** Escalation required. Route to executive sponsor or technical lead who can directly address the concern. The deal will stall unless this specific risk is mitigated.

## Output

- Structured risk data stored in Attio with severity/likelihood scores
- Call notes with supporting quotes and mitigation action items
- PostHog events for risk funnel tracking
- Routing recommendation and mitigation actions triggered
- Prediction accuracy logged for continuous improvement

## Triggers

Run automatically after every discovery/evaluation call via n8n workflow triggered by Fireflies transcript completion webhook.
