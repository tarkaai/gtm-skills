---
name: authority-discovery-call
description: Run a structured discovery call focused on verifying decision-making authority — prep, execute, extract authority signals, and log to CRM
category: Discovery
tools:
  - Fireflies
  - Attio
  - Anthropic
  - Cal.com
fundamentals:
  - fireflies-transcription
  - fireflies-action-items
  - stakeholder-role-classification
  - attio-deals
  - attio-notes
  - attio-custom-attributes
  - calcom-booking-links
---

# Authority Discovery Call

This drill covers the full lifecycle of a discovery call designed to verify decision-making authority: pre-call stakeholder research, authority-focused question preparation, transcript analysis for authority signals, role classification update, and CRM logging. Designed for founder-led sales where the founder conducts the call.

## Input

- Deal record in Attio with stakeholder map already started (from `stakeholder-research` drill)
- Known contact on the call with existing role classification (may be Champion, Influencer, or Unknown)
- Cal.com booking link for scheduling
- Fireflies configured to auto-join meetings

## Steps

### 1. Pre-call authority research

Pull the deal record from Attio. Review the existing stakeholder map to understand:
- Who is classified as Economic Buyer (if anyone)?
- Who is the current contact and what is their classified role?
- What gaps exist in the buying committee map?

Query Attio for the deal:
```
attio.get_record({ object: "deals", record_id: "{deal_id}" })
```

Review: `stakeholder_role`, `stakeholder_confidence`, `engagement_level` for each linked person. Identify whether an Economic Buyer has been confirmed or is still unknown.

### 2. Generate authority-focused questions

Using Claude, generate a tailored question list based on the contact's role and the authority gaps identified:

```
POST https://api.anthropic.com/v1/messages
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 800,
  "messages": [{
    "role": "user",
    "content": "You are preparing authority-verification questions for a sales discovery call.\n\nContext:\n- Company: {company_name}, {employee_count} employees\n- Contact: {name}, {title}\n- Current role classification: {stakeholder_role} (confidence: {confidence})\n- Known Economic Buyer: {eb_name_or_none}\n- Deal value: {deal_value}\n- Product: {your_product_description}\n\nGenerate 5-7 questions that naturally uncover:\n1. Who controls the budget for this type of purchase\n2. What the approval process looks like (committee, single signer, procurement)\n3. Whether the contact can make a unilateral decision or needs sign-off\n4. Who else needs to be involved before a contract is signed\n5. What happened the last time they bought similar software\n\nThe questions must sound conversational, not interrogative. They should be open-ended and allow the contact to reveal authority dynamics naturally.\n\nReturn as a numbered list with a one-line note after each question explaining what authority signal it probes."
  }]
}
```

Store the question list as a pre-call note in Attio using `attio-notes`.

### 3. Execute the call

**Human action required:** Conduct the discovery call. Fireflies auto-joins and transcribes.

During the call, work through the authority questions naturally. Listen for these specific signals:

**Economic Buyer signals:**
- "I can approve this" / "I own this budget"
- References to specific budget amounts or fiscal cycles
- Asks about pricing without deferring to someone else
- Describes the purchasing process from a position of ownership

**Non-authority signals (contact is NOT the Economic Buyer):**
- "I'll need to run this by [name]" / "My boss would need to sign off"
- "Our procurement team handles the contracting"
- "I can recommend but the decision is above my level"
- Defers pricing questions or says "I don't know the budget"
- References a committee or board approval process

**Champion signals (high-value even without authority):**
- Asks for materials to share internally
- Offers to make introductions to decision-makers
- Describes internal politics and how to navigate them
- Shows enthusiasm about the product and asks "how do I sell this to my team?"

### 4. Extract authority signals from transcript

After the call, use Fireflies to access the transcript. Run Claude to extract authority-specific signals:

```
POST https://api.anthropic.com/v1/messages
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1000,
  "messages": [{
    "role": "user",
    "content": "Analyze this sales call transcript for authority verification signals.\n\nTranscript:\n{transcript_text}\n\nFor each participant (excluding the seller), extract:\n1. **Authority classification**: Economic Buyer, Champion, Influencer, Blocker, End User, or Gatekeeper\n2. **Confidence**: High, Medium, or Low\n3. **Evidence**: Direct quotes that support the classification\n4. **Budget authority**: Does this person control or influence the budget? Quote the evidence.\n5. **Approval process**: What did they reveal about how purchase decisions are made? Quote the evidence.\n6. **Other stakeholders named**: List any other people mentioned who are part of the buying process, with their implied role.\n7. **Authority verification status**: VERIFIED (they confirmed they can sign), LIKELY (strong signals but not explicit), UNLIKELY (signals suggest they cannot sign), UNKNOWN (insufficient data)\n\nReturn as structured JSON."
  }]
}
```

### 5. Update stakeholder classifications in CRM

Based on the transcript analysis:

1. Update the contact's `stakeholder_role` and `stakeholder_confidence` in Attio using `attio-custom-attributes`
2. For any NEW stakeholders mentioned in the call, create Person records in Attio with preliminary role classifications
3. Update the `authority_verification_status` field on the deal:
   - `verified` — Economic Buyer confirmed and engaged
   - `identified` — Economic Buyer identified but not yet engaged
   - `unverified` — No clear Economic Buyer found yet
4. Log the authority evidence as a structured note on the deal using `attio-notes`:

```
## Authority Verification — {Company Name}
Call date: {date}
Contact: {name}, {title}

### Authority Status: {verified/identified/unverified}

### Evidence
{Direct quotes supporting the classification}

### Buying Process
{What was revealed about how decisions are made}

### Stakeholders Named
- {Name}, {Title} — Implied role: {role}

### Next Steps
- {If verified: schedule pricing/proposal conversation}
- {If identified but not engaged: get introduction to Economic Buyer}
- {If unverified: plan next call targeting authority discovery}
```

### 6. Determine next action

Based on authority verification status:

- **Verified**: The person on the call can sign. Move to proposal/pricing. Log `authority_verified_date` on the deal.
- **Identified**: The Economic Buyer was named but is not the current contact. Use the Champion to get an introduction. Create a task in Attio: "Schedule intro call with {EB name}."
- **Unverified**: No clear authority signal. Either (a) the org structure is unclear — run `org-chart-research` for more data, or (b) the contact is not being forthcoming — try a different entry point.

## Output

- Updated stakeholder map with authority-verified classifications
- Authority verification status on the deal record
- Structured authority evidence note on the deal
- New stakeholder records for anyone mentioned in the call
- Clear next action based on verification outcome

## Triggers

- Run on every first substantive call with a new qualified prospect
- Re-run when stakeholder dynamics change (reorg, Champion departure, deal stall)
- Re-run when a new contact is introduced into an existing deal
