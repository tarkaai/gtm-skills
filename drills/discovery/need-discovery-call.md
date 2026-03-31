---
name: need-discovery-call
description: Run a structured need assessment discovery call — prep, execute, extract needs from transcript, score, and log to CRM
category: Discovery
tools:
  - Fireflies
  - Attio
  - Anthropic
  - Cal.com
fundamentals:
  - fireflies-transcription
  - fireflies-action-items
  - call-transcript-need-extraction
  - attio-deals
  - attio-notes
  - calcom-booking-links
  - posthog-custom-events
---

# Need Discovery Call

This drill covers the full lifecycle of a need-focused discovery call: pre-call research, question preparation, transcript analysis, need scoring, and CRM logging. Designed for founder-led sales where the goal is to systematically uncover whether a prospect has genuine business needs your product solves.

## Input

- Deal record in Attio with pre-enrichment need hypothesis (from `need-scorecard-setup`)
- Need categories defined (from `need-scorecard-setup` drill)
- Cal.com booking link for scheduling
- Fireflies configured to auto-join meetings

## Steps

### 1. Pre-call research

Pull the deal record from Attio. Review any pre-enrichment need signals to identify which need categories have evidence and which are unknown. Focus discovery on unknown categories — these represent the biggest information gap.

Query Attio for the deal:
```
attio.get_record({ object: "deals", record_id: "{deal_id}" })
```

Review existing scores across all need categories. Note which are 0 (Not Assessed) — these are priority discovery targets.

### 2. Generate a need-focused question guide

Based on the gaps, generate a call prep document. Use Claude to create tailored questions for each unexplored need category:

**For each need category, prepare 3-5 probing questions. Example for "reducing manual data entry":**
- "Walk me through what happens when a new lead comes in — how many systems do you touch?"
- "What percentage of your team's time goes to data entry versus actual selling/building?"
- "Have you tried to automate any of this? What happened?"
- "If you could eliminate all manual data entry tomorrow, what would your team do with that time?"
- "What's the cost when data entry gets done wrong or gets delayed?"

**For "improving data accuracy":**
- "When was the last time bad data caused a real problem — a missed deal, a wrong report, a bad decision?"
- "How do you know your CRM data is accurate right now? What's your confidence level?"
- "What happens when two people update the same record differently?"

**Question design principles:**
- Start with open-ended situational questions ("walk me through...")
- Follow with impact questions ("what happens when...")
- Probe for severity ("how often does this happen?", "what does it cost you?")
- Ask about prior attempts ("have you tried to solve this?", "what happened?")
- Close with urgency ("if you don't fix this in 6 months, what happens?")

Store the question guide as an Attio note on the deal using `attio-notes`.

### 3. Ensure Fireflies is recording

Verify Fireflies is configured to auto-join the scheduled meeting. Check via Fireflies API:
```graphql
query { user { integrations { calendar_connected } } }
```

If the meeting is on Cal.com, verify the calendar sync is active.

### 4. Post-call: extract need signals from transcript

After the call, wait for Fireflies to process the transcript (typically 5-15 minutes). Then run the `call-transcript-need-extraction` fundamental with the full transcript text and the need categories JSON.

The extraction returns:
- Array of identified needs with categories, severity scores, and supporting quotes
- Total need score (sum of severity across all categories)
- Critical need count
- Whether the prospect meets the minimum viable need threshold
- Gaps not explored (need categories not discussed)
- Recommended follow-up questions

### 5. Score each need category

Map the extracted needs to your predefined categories. For each category:
- **Critical (3):** Prospect described severe pain, quantified the impact, has tried to solve it, and expressed urgency
- **Moderate (2):** Prospect acknowledged the problem, described some impact, but urgency or severity is moderate
- **Low (1):** Prospect mentioned the area but did not describe meaningful pain or urgency
- **Not Assessed (0):** Category was not discussed — flag for follow-up

Calculate:
- `total_need_score` = sum of all category scores
- `critical_need_count` = count of categories scored 3
- `need_tier` = High Need (>=15), Medium Need (12-14), Low Need (<12)

### 6. Update CRM with need assessment results

Using `attio-deals`, update the deal record with all need scores, the tier classification, and the verdict. Set `need_assessment_source` to "Discovery Call" and update `need_last_assessed` to today.

Compare pre-call hypothesis scores against post-call scores. If any category changed by more than 1 point, log a note explaining why — this calibrates your enrichment-based need hypothesis over time.

### 7. Log the call summary and next steps

Using `attio-notes`, create a structured note on the deal:

```markdown
## Need Discovery Call — {date}
### Prospect: {company_name} / {contact_name}

### Need Assessment Summary
| Category | Severity | Label | Key Signal |
|----------|----------|-------|------------|
| {category_1} | {1-3} | {Critical/Moderate/Low} | {supporting quote} |
| {category_2} | {1-3} | {Critical/Moderate/Low} | {supporting quote} |
| ... | ... | ... | ... |

### Total Score: {score}/21 — {tier}
### Critical Needs: {count}
### Verdict: {Qualified/Nurture/Disqualified}

### Key Quotes
- "{most impactful quote}" — on {need area}
- "{second quote}" — on {need area}

### Attempted Solutions
- {what they've tried for each need}

### Urgency Signals
- {signal 1}
- {signal 2}

### Gaps (Explore in Follow-Up)
- {need categories not discussed}
- {categories scored Low that may hide deeper needs}

### Next Steps
- {action items from Fireflies}
```

### 8. Fire tracking events

Using `posthog-custom-events`, log:
```json
{
  "event": "need_assessment_completed",
  "properties": {
    "deal_id": "...",
    "total_need_score": 16,
    "critical_need_count": 3,
    "need_tier": "high_need",
    "needs_above_threshold": true,
    "categories_assessed": 5,
    "categories_not_assessed": 2,
    "hypothesis_accuracy": 0.7,
    "call_duration_minutes": 35
  }
}
```

### 9. Route based on results

- **High Need (score >=15, >=2 Critical):** Move to "Need Qualified." Schedule demo or proposal call via Cal.com. The prospect has genuine, urgent needs your product addresses.
- **Medium Need (score 12-14):** Keep in "Need Assessed." Schedule a follow-up call focused on the unexplored need categories and probing deeper on Moderate-scored categories. They may qualify with more discovery.
- **Low Need (score <12):** Move to "Need Disqualified." The prospect does not have sufficient business needs for your product right now. Add to a content nurture sequence (case studies, pain-focused content) and reassess in 90 days.

## Output

- Updated need scores on the deal record in Attio (per-category and aggregate)
- Structured call notes with supporting quotes, urgency signals, and next steps
- PostHog events for funnel tracking
- Routing recommendation and next action

## Triggers

Run after every need discovery call. Re-run after follow-up calls to reassess need scores as new information surfaces.
