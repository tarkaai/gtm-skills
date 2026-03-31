---
name: meddic-discovery-call
description: Run a structured MEDDIC discovery call — prep, execute with element-targeted questions, score, and log results to CRM
category: Sales
tools:
  - Fireflies
  - Attio
  - Anthropic
  - Cal.com
fundamentals:
  - fireflies-transcription
  - fireflies-action-items
  - call-transcript-meddic-extraction
  - attio-deals
  - attio-notes
  - calcom-booking-links
---

# MEDDIC Discovery Call

This drill covers the full lifecycle of a MEDDIC-focused discovery call: pre-call research, element-targeted question preparation, transcript analysis, MEDDIC scoring, and CRM logging. Designed for founder-led enterprise sales where the founder needs to efficiently qualify complex deals.

## Input

- Deal record in Attio with pre-enrichment MEDDIC scores (from `meddic-scorecard-setup` and `meddic-auto-scoring` drills)
- Cal.com booking link for scheduling
- Fireflies configured to auto-join meetings

## Steps

### 1. Pre-call research

Pull the deal record from Attio. Review the pre-enrichment MEDDIC scores to identify which elements are strong vs. weak. Focus your discovery questions on the weakest elements.

Query Attio for the deal:
```
attio.get_record({ object: "deals", record_id: "{deal_id}" })
```

Review all six element scores: `meddic_metrics_score`, `meddic_economic_buyer_score`, `meddic_decision_criteria_score`, `meddic_decision_process_score`, `meddic_identify_pain_score`, `meddic_champion_score`. Note which are below 50 — these are your priority areas for discovery.

Also review: `meddic_metrics_evidence`, `meddic_economic_buyer_evidence`, etc. to understand what signals enrichment already detected.

### 2. Generate a MEDDIC question guide

Based on the gaps, generate a call prep document. Use Claude to create tailored questions:

**Metrics questions (if metrics_score < 50):**
- "If this project succeeds, what specific numbers would change in your business?"
- "How do you currently measure success in this area? What KPIs does your team track?"
- "What would solving this problem be worth to you in dollars or hours per month?"
- "When you present results to your leadership, what metrics do they care about?"

**Economic Buyer questions (if economic_buyer_score < 50):**
- "Walk me through how a purchase at this price point gets approved at your company."
- "Who ultimately signs off on the budget for tools in this area?"
- "Have you discussed this initiative with your [VP/CFO/CTO]? What was their reaction?"
- "If we decided to move forward, whose calendar would we need to get on?"

**Decision Criteria questions (if decision_criteria_score < 50):**
- "What are the top 3 things that matter most when you evaluate a solution like this?"
- "Are there any technical requirements that are absolute must-haves?"
- "How important is [integration with X / compliance with Y / support for Z] in your evaluation?"
- "Have you created an evaluation scorecard or RFP? If so, can you share the criteria?"

**Decision Process questions (if decision_process_score < 50):**
- "What happens between us agreeing this is a fit and the contract getting signed?"
- "How many people need to review or approve this? Who are they and what do they care about?"
- "Is there a procurement or legal review involved? How long does that typically take?"
- "Have you bought a tool at this price point before? What did that process look like last time?"

**Identify Pain questions (if identify_pain_score < 50):**
- "What triggered your interest in solving this now rather than 6 months ago?"
- "How are you handling this today? What specifically is not working?"
- "If you do nothing for the next 12 months, what happens to your business?"
- "How much time or money are you losing each month because of this problem?"

**Champion questions (if champion_score < 50):**
- "Who on your team would benefit most from solving this?"
- "Is there someone internally who has been pushing for a solution in this area?"
- "If I gave you materials to share internally, who would you send them to and how would you frame it?"
- "What would you need from me to build the internal case for this?"

Store the question guide as an Attio note on the deal using `attio-notes`.

### 3. Ensure Fireflies is recording

Verify Fireflies is configured to auto-join the scheduled meeting. Check via Fireflies API:
```graphql
query { user { integrations { calendar_connected } } }
```

If the meeting is on Cal.com, verify the calendar sync is active.

### 4. Post-call: extract MEDDIC signals from transcript

After the call, wait for Fireflies to process the transcript (typically 5-15 minutes). Then run the `call-transcript-meddic-extraction` fundamental to extract structured MEDDIC scores from the conversation.

The extraction returns per-element:
- Scores (0-100) with supporting quotes
- Status classification
- Red flags
- For Economic Buyer: buyer name, title, access path
- For Decision Process: mapped steps and timeline estimate
- For Champion: champion name, influence level, motivation
- Composite score and qualification verdict
- Weakest elements and recommended next steps

### 5. Update CRM with discovery results

Using `attio-deals`, update the deal record with the new MEDDIC scores from the discovery call. Set `meddic_assessment_source` to "Discovery Call" and update `meddic_last_assessed` to today's date.

For each element, also update:
- The status field (e.g., `meddic_metrics_status` = "Quantified")
- The evidence field with key quotes and findings

Compare the post-call scores against the pre-enrichment scores. If any element changed by more than 20 points, log a note explaining why — this calibrates your enrichment model over time.

### 6. Log the call summary and next steps

Using `attio-notes`, create a structured note on the deal:

```
## MEDDIC Discovery Call — {date}

### Element Assessment
- **Metrics:** {score} — {status}. {key quote or finding}
- **Economic Buyer:** {score} — {status}. {buyer name/title if identified}. {access path}
- **Decision Criteria:** {score} — {status}. {top criteria identified}
- **Decision Process:** {score} — {status}. {steps mapped}. Est. timeline: {weeks}
- **Identify Pain:** {score} — {status}. {primary pain point}. Business impact: {quantified if available}
- **Champion:** {score} — {status}. {champion name if identified}. {their motivation}

### Composite: {score} — {verdict}
### Weakest Elements: {list}

### Key Quotes
{3-4 most important quotes from the call, tagged by which MEDDIC element they relate to}

### Next Steps
{action items extracted by Fireflies + MEDDIC-specific actions}

### Element Gaps to Address
{for each weak element: what specifically needs to happen to strengthen it}
```

### 7. Route based on verdict

- **Qualified (70+):** Move deal to "MEDDIC Qualified" stage. If champion identified, move to "Champion Engaged." Schedule the next meeting (demo for technical buyers, business case review for economic buyer) via Cal.com.
- **Needs Work (40-69):** Keep in "MEDDIC Needs Work" stage. Create follow-up tasks targeting the weakest elements:
  - Weak Economic Buyer: Request an introduction to the budget holder
  - Weak Champion: Send value materials the contact can share internally
  - Weak Metrics: Send a ROI calculator or case study with quantified outcomes
  - Weak Decision Process: Ask for the procurement team's requirements
  - Weak Decision Criteria: Send a comparison matrix addressing their evaluation areas
  - Weak Identify Pain: Send a relevant case study that amplifies the pain they mentioned
- **Disqualified (<40):** Move to "MEDDIC Disqualified." Send a polite nurture email. Add to a re-engagement sequence for 90 days later.

## Output

- Updated MEDDIC scores (all 6 elements) on the deal record in Attio
- Evidence fields populated with key quotes and findings
- Structured call notes with element-by-element assessment
- Deal routed to the correct pipeline stage
- Follow-up tasks created targeting specific MEDDIC element gaps

## Triggers

Run after every discovery call. Re-run after follow-up calls to re-assess MEDDIC scores as new information surfaces. Each re-assessment should reference the previous scores so you can track element progression over time.
