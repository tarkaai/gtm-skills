---
name: stakeholder-role-classification
description: Classify contacts into buying committee roles (Champion, Economic Buyer, Influencer, Blocker, End User) using AI
tool: Anthropic
product: Claude API
difficulty: Advanced
---

# Stakeholder Role Classification

Use Claude or another LLM to classify contacts at a target account into buying committee roles based on their title, seniority, department, and any interaction history. Produces a structured role assignment for each stakeholder.

## Prerequisites

- List of contacts at a target account with: name, title, department, seniority level
- Optional: interaction history (emails, call notes, meeting transcripts)
- Anthropic API key or Claude MCP access

## Buying Committee Roles

| Role | Definition | Typical Signals |
|------|-----------|----------------|
| **Economic Buyer** | Controls budget, signs the contract | C-Suite, VP Finance, "Head of" with P&L ownership |
| **Champion** | Internal advocate who sells on your behalf | Engaged contact, asks for materials to share internally, refers you to others |
| **Influencer** | Shapes the decision but does not own it | Technical leads, architects, team leads who evaluate tools |
| **Blocker** | Actively or passively resists the purchase | Security, legal, procurement, or someone loyal to incumbent vendor |
| **End User** | Will use the product daily | ICs, managers in the target department |
| **Gatekeeper** | Controls access to the Economic Buyer | Executive assistants, Chiefs of Staff |

## Steps

### 1. Classify by title and department (rule-based first pass)

Apply deterministic rules before using AI:
```
IF title contains "CEO" OR "CRO" OR "CFO" OR "VP" with P&L keywords → Economic Buyer
IF title contains "Procurement" OR "Legal" OR "Compliance" OR "Security" → Potential Blocker
IF title contains "Engineer" OR "Developer" OR "Analyst" (IC level) → End User
IF title contains "Director" OR "Manager" in target department → Influencer
```

This first pass is fast and free. Flag contacts that do not match any rule for AI classification.

### 2. Classify ambiguous contacts with Claude

**API call:**
```
POST https://api.anthropic.com/v1/messages
Authorization: Bearer {ANTHROPIC_API_KEY}
Content-Type: application/json
x-api-version: 2023-06-01

{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 500,
  "messages": [
    {
      "role": "user",
      "content": "You are classifying stakeholders in a B2B software buying process.\n\nCompany: {company_name}\nProduct being sold: {your_product_description}\nContact: {name}, {title}, {department}\nInteraction history: {summary_of_interactions_or_none}\n\nClassify this person into exactly ONE primary role: Economic Buyer, Champion, Influencer, Blocker, End User, or Gatekeeper.\n\nReturn JSON:\n{\"role\": \"...\", \"confidence\": \"high|medium|low\", \"reasoning\": \"one sentence\"}"
    }
  ]
}
```

### 3. Incorporate interaction signals

If you have call transcripts or email threads, add behavioral signals to improve classification:
- **Champion signals**: Asks "What materials can I share with my team?", introduces you to other stakeholders, responds quickly, volunteers internal context
- **Blocker signals**: Asks about competitor features, mentions "we already have a solution", delays meetings, CC's procurement/legal early
- **Economic Buyer signals**: Asks about pricing, ROI, contract terms, implementation timeline
- **Influencer signals**: Asks detailed technical questions, requests a sandbox or trial, evaluates against specific criteria

Use `transcript-insight-extraction` fundamental to pull these signals from Fireflies transcripts.

### 4. Score confidence and flag unknowns

For each classification, assign confidence:
- **High**: Title + behavior clearly indicate role (e.g., CFO asking about pricing = Economic Buyer)
- **Medium**: Title suggests role but no behavioral confirmation (e.g., VP Engineering who has not engaged yet)
- **Low**: Ambiguous title, no interaction data (e.g., "Senior Director, Strategy")

Flag all low-confidence classifications for human review during discovery calls.

### 5. Store classifications in CRM

Write role classifications to Attio using `attio-custom-attributes`:
```json
{
  "data": {
    "values": {
      "stakeholder_role": [{"option": "Champion"}],
      "stakeholder_confidence": [{"option": "High"}],
      "stakeholder_sentiment": [{"option": "Supportive"}]
    }
  }
}
```

### 6. Re-classify as deals progress

Roles are not static. A Champion can become a Blocker if priorities shift. Re-run classification after every significant interaction (discovery call, demo, negotiation). Compare new classification to previous and flag changes for the sales team.

## Via Clay (Claygent)

For batch classification without API calls:
```
Claygent prompt: "Given that {Full Name} is {Title} at {Company Name} in the {Department} department, classify their likely role in a B2B software buying decision. Choose one: Economic Buyer, Champion, Influencer, Blocker, End User, Gatekeeper. Return the role and a one-sentence explanation."
```

Cost: 5-10 credits per classification. Use for initial bulk classification of new accounts.

## Tool Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Anthropic Claude | Messages API | Best reasoning for ambiguous cases |
| OpenAI GPT-4 | Chat Completions API | Good alternative, similar quality |
| Clay Claygent | Built-in AI column | Convenient for batch processing in Clay |
| Gong | Deal intelligence | Infers roles from call participation patterns |
| 6sense | Buying team detection | Enterprise-grade intent + role mapping |

## Error Handling

- **Over-classifying Champions**: Not every friendly contact is a Champion. A Champion must have organizational influence AND willingness to advocate. Friendly but junior contacts are End Users.
- **Missing Economic Buyer**: If no one in the map is classified as Economic Buyer, the deal is at risk. Prioritize discovery to find them.
- **Role conflicts**: Two people classified as Economic Buyer suggests either a matrix organization or misclassification. Flag for human verification.
- **API rate limits**: Anthropic rate limits vary by plan. Batch classifications in groups of 10-20 with 1-second delays.
