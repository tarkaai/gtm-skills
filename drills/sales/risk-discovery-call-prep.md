---
name: risk-discovery-call-prep
description: Research the prospect and generate a tailored risk-probing question guide organized by five risk categories before a discovery call
category: Sales
tools:
  - Attio
  - Clay
  - Fireflies
  - Anthropic
  - Cal.com
fundamentals:
  - attio-deals
  - attio-notes
  - clay-company-search
  - clay-claygent
  - fireflies-transcription
  - calcom-booking-links
  - anthropic-api-patterns
---

# Risk Discovery Call Prep

This drill prepares a founder or AE to systematically probe for risks and concerns during a discovery call. It researches the prospect's company, identifies likely risk areas based on industry, size, and deal context, and generates a tailored risk-probing question guide organized by the five risk categories: Financial, Technical, Organizational, Timeline, and Vendor. The output is a risk prep document stored as an Attio note on the deal.

## Input

- Deal record in Attio with at least: company name, contact name, contact title, industry
- Cal.com booking link (meeting already scheduled)
- Fireflies configured to auto-join meetings
- Prior pain discovery data (if available from `pain-discovery-call` drill)

## Steps

### 1. Pull deal context from CRM

Query Attio for the deal record:
```
attio.get_record({ object: "deals", record_id: "{deal_id}" })
```

Extract: company name, contact name, contact title, industry, company size, deal value, existing pain data, prior call notes, competitor mentions, stakeholders identified so far.

### 2. Enrich for risk signals

Use the `clay-company-search` fundamental to pull firmographic data. Use `clay-claygent` to find risk-relevant signals:
```
Research {Company Name} ({domain}). Find:
1. Current tech stack (integration complexity signals)
2. Recent leadership changes or layoffs (organizational change resistance signals)
3. Regulatory environment for their industry (compliance risk signals)
4. Previous vendor switches or failed implementations mentioned in reviews/press
5. IT team size relative to company size (technical capacity signals)
6. Budget cycle timing (fiscal year end, planning season)
7. Competitor products they may be evaluating or currently using
Return each item with date, source, and a one-sentence summary.
```

Cost: 5-10 credits per company.

### 3. Predict likely risks by category

Send the enrichment data + deal context to Claude via `anthropic-api-patterns`:

```json
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 2000,
  "messages": [{
    "role": "user",
    "content": "Based on this prospect profile, predict the most likely risks and concerns they will have about buying our product. Organize by category.\n\nProspect: {company_name}, {industry}, {headcount} employees, {funding_stage}\nContact: {contact_name}, {contact_title}\nDeal value: {deal_value}\nCurrent tech stack: {tech_stack}\nPrior pain points identified: {pain_data}\nSignals: {enrichment_signals}\nOur product: {product_description}\n\nFor each of the 5 risk categories, provide:\n\n1. **Financial risks**: Budget, ROI uncertainty, hidden costs, sunk cost of current solution\n   - Predicted risk (one sentence)\n   - Why this prospect likely has it (based on their profile)\n   - Discovery question to surface it (open-ended, empathetic, not leading)\n   - Follow-up to quantify impact: 'What happens if this risk materializes?'\n\n2. **Technical risks**: Integration, security, data migration, performance, downtime\n   - Same structure\n\n3. **Organizational risks**: Change management, adoption, training, team disruption, internal politics\n   - Same structure\n\n4. **Timeline risks**: Implementation delays, competing priorities, resource availability, urgency\n   - Same structure\n\n5. **Vendor risks**: Company stability, support quality, product roadmap, lock-in, references\n   - Same structure\n\nAlso provide:\n- The 2 categories most likely to be decision-blockers for THIS prospect (with reasoning)\n- 3 universal risk questions that work regardless of category:\n  * 'What concerns do you have about making this change?'\n  * 'What would need to be true for you to feel confident this will succeed?'\n  * 'What has gone wrong with past vendor decisions?'"
  }]
}
```

### 4. Build the risk prep document

Structure the output:

```markdown
## Risk Discovery Prep -- {company_name}
### Date: {call_date}
### Contact: {contact_name}, {contact_title}

### Company Risk Profile
- {headcount} employees, {industry}, {funding_stage}
- Key risk signals: {2-3 bullet points from enrichment}
- Prior pain identified: {summary from earlier discovery}

### Predicted Decision-Blocking Categories
1. **{Category}** -- {reasoning}
2. **{Category}** -- {reasoning}

### Risk Probing Questions by Category

#### Financial Risks
- Predicted: {risk}
- Discovery Q: "{question}"
- Follow-up: "{impact question}"
- Mitigation ready: {yes/no -- does content library have an asset?}

#### Technical Risks
- Predicted: {risk}
- Discovery Q: "{question}"
- Follow-up: "{impact question}"
- Mitigation ready: {yes/no}

#### Organizational Risks
- Predicted: {risk}
- Discovery Q: "{question}"
- Follow-up: "{impact question}"
- Mitigation ready: {yes/no}

#### Timeline Risks
- Predicted: {risk}
- Discovery Q: "{question}"
- Follow-up: "{impact question}"
- Mitigation ready: {yes/no}

#### Vendor Risks
- Predicted: {risk}
- Discovery Q: "{question}"
- Follow-up: "{impact question}"
- Mitigation ready: {yes/no}

### Call Structure for Risk Discovery (15-20 min block)
- After initial pain discovery, transition: "I want to make sure we address any concerns early..."
- Start with the 2 predicted decision-blocking categories
- Use universal openers if prospect is not forthcoming
- For each risk surfaced: acknowledge, probe for severity, note whether it blocks the decision
- Close risk block: "Is there anything else that would prevent this from being successful?"

### Rules for the Caller
- Never dismiss a concern -- acknowledge it first, then probe deeper
- Capture the exact words they use to describe the risk
- Ask: "On a scale of 1-10, how worried are you about this?" for each risk
- Note WHO raised the concern -- different stakeholders fear different things
- If they say "nothing" to a risk question, probe indirectly: "When your team has evaluated tools before, what typically derails the process?"
```

### 5. Store prep in CRM

Using `attio-notes`, create a note on the deal record with the full risk prep document. Tag the note as `risk-prep` for retrieval by the `risk-discovery-call` drill post-call.

### 6. Verify recording is active

Check that Fireflies is configured to auto-join the scheduled meeting. Query the Fireflies API:
```graphql
query { user { integrations { calendar_connected } } }
```

If not connected, send alert to the caller.

## Output

- Enriched deal record with risk-relevant company signals
- Risk prep document stored as Attio note with per-category predicted risks and probing questions
- Fireflies recording verified for the meeting
- Caller has a structured risk-probing guide organized by the 5 risk categories

## Triggers

Run this drill 24 hours before every scheduled discovery/evaluation call. Trigger automatically via n8n when a Cal.com booking event fires. If prior pain discovery data exists on the deal, incorporate it into the risk predictions.
