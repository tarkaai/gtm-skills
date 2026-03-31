---
name: bant-discovery-call
description: Run a structured BANT discovery call — prep, execute, score, and log results to CRM
category: Discovery
tools:
  - Fireflies
  - Attio
  - Anthropic
  - Cal.com
fundamentals:
  - fireflies-transcription
  - fireflies-action-items
  - call-transcript-bant-extraction
  - attio-deals
  - attio-notes
  - calcom-booking-links
---

# BANT Discovery Call

This drill covers the full lifecycle of a BANT-focused discovery call: pre-call research, question preparation, transcript analysis, BANT scoring, and CRM logging. Designed for founder-led sales where the founder is the one on the call.

## Input

- Deal record in Attio with pre-enrichment BANT scores (from `bant-scorecard-setup` and `enrich-and-score` drills)
- Cal.com booking link for scheduling
- Fireflies configured to auto-join meetings

## Steps

### 1. Pre-call research

Pull the deal record from Attio. Review the pre-enrichment BANT scores to identify which dimensions are strong vs. weak. Focus your discovery questions on the weakest dimensions.

Query Attio for the deal:
```
attio.get_record({ object: "deals", record_id: "{deal_id}" })
```

Review: `bant_budget_score`, `bant_authority_score`, `bant_need_score`, `bant_timeline_score`. Note which are below 50 — these are your priority areas for discovery.

### 2. Generate a BANT question guide

Based on the gaps, generate a call prep document. Use Claude to create tailored questions:

**Budget questions (if budget_score < 50):**
- "What are you currently spending on [problem area]?"
- "Is there a budget allocated for solving this, or would we need to build the case?"
- "Who controls the budget for tools in this area?"
- "What's your typical procurement process for a tool at this price point?"

**Authority questions (if authority_score < 50):**
- "Walk me through how your team evaluates and buys new tools."
- "Who else would need to weigh in on this decision?"
- "Have you bought a tool like this before? What did that process look like?"
- "If we decided to move forward, what would the sign-off chain look like?"

**Need questions (if need_score < 50):**
- "What's driving your interest in solving this now?"
- "How are you handling this today? What's working and what's not?"
- "If you don't solve this in the next 6 months, what happens?"
- "How does this problem rank against your other priorities this quarter?"

**Timeline questions (if timeline_score < 50):**
- "Is there a deadline or event driving your timeline?"
- "When would you ideally have a solution in place?"
- "Are you evaluating other options in parallel?"
- "What needs to happen between now and a decision?"

Store the question guide as an Attio note on the deal using `attio-notes`.

### 3. Ensure Fireflies is recording

Verify Fireflies is configured to auto-join the scheduled meeting. Check via Fireflies API:
```graphql
query { user { integrations { calendar_connected } } }
```

If the meeting is on Cal.com, verify the calendar sync is active.

### 4. Post-call: extract BANT signals from transcript

After the call, wait for Fireflies to process the transcript (typically 5-15 minutes). Then run the `call-transcript-bant-extraction` fundamental to extract structured BANT scores from the conversation.

The extraction returns:
- Per-dimension scores (0-100) with supporting quotes
- Red flags per dimension
- Authority mapping (who else is involved)
- Estimated close timeline
- Composite score and qualification verdict

### 5. Update CRM with discovery results

Using `attio-deals`, update the deal record with the new BANT scores from the discovery call. Set `bant_assessment_source` to "Discovery Call" and update `bant_last_assessed` to today's date.

Compare the post-call scores against the pre-enrichment scores. If any dimension changed by more than 20 points, log a note explaining why — this calibrates your enrichment model over time.

### 6. Log the call summary and next steps

Using `attio-notes`, create a structured note on the deal:

```
## Discovery Call — {date}
### BANT Assessment
- Budget: {score} — {status}. {key quote or finding}
- Authority: {score} — {status}. {key quote or finding}
- Need: {score} — {status}. {key quote or finding}
- Timeline: {score} — {status}. {key quote or finding}

### Composite: {score} — {verdict}

### Key Quotes
{2-3 most important quotes from the call}

### Next Steps
{action items extracted by Fireflies}

### Gaps to Address
{which BANT dimensions still need work and how to address them}
```

### 7. Route based on verdict

- **Qualified (70+):** Move deal to "BANT Qualified" stage. Schedule the next meeting (demo, proposal review, etc.) via Cal.com.
- **Needs Work (40-69):** Keep in "BANT Needs Work" stage. Create follow-up tasks to address specific gaps (e.g., "Send case study to help prospect build internal budget case").
- **Disqualified (<40):** Move to "BANT Disqualified." Send a polite nurture email. Add to a re-engagement sequence for 90 days later.

## Output

- Updated BANT scores on the deal record in Attio
- Structured call notes with key quotes and next steps
- Deal routed to the correct pipeline stage
- Follow-up tasks created for any BANT gaps

## Triggers

Run after every discovery call. Can also be re-run after follow-up calls to re-assess BANT scores as new information surfaces.
