---
name: stakeholder-map-assembly
description: Map all buying committee stakeholders at a target account, classify roles, score influence, and store structured map in CRM
category: Sales
tools:
  - Clay
  - Attio
  - Anthropic
fundamentals:
  - org-chart-research
  - stakeholder-role-classification
  - clay-people-search
  - clay-enrichment-waterfall
  - clay-claygent
  - attio-contacts
  - attio-deals
  - attio-custom-attributes
  - attio-notes
  - posthog-custom-events
---

# Stakeholder Map Assembly

This drill produces a complete buying committee map for a deal: every stakeholder identified, role-classified, influence-scored, and stored in the CRM with engagement status tracking. It is the foundation for multi-stakeholder discovery — you cannot run targeted discovery calls without knowing who to talk to and why they matter.

## Input

- Deal record in Attio (stage >= Connected)
- Company domain or LinkedIn company URL
- Product value proposition (for role classification context)
- Optional: existing contacts already known at the account

## Steps

### 1. Pull Existing Contacts from CRM

Query Attio for all people already linked to this deal:

```
attio.list_records({
  object: "people",
  filter: { linked_deal_id: "{deal_id}" },
  select: ["name", "title", "email", "stakeholder_role", "last_interaction_date"]
})
```

This establishes the baseline: who do we already know? Flag contacts without a `stakeholder_role` as unclassified.

### 2. Research the Org Chart

Run the `org-chart-research` fundamental against the target company:
- Push the company to a Clay table
- Use `clay-people-search` to find 20-30 people at Director+ level
- Filter to departments relevant to the buying decision
- Enrich each person with title, department, seniority, LinkedIn URL, and email via `clay-enrichment-waterfall`
- Use Claygent to infer reporting lines

### 3. Classify Every Contact into Buying Committee Roles

Run the `stakeholder-role-classification` fundamental on each contact:
- Apply rule-based classification first (title patterns)
- Use Claude API for ambiguous contacts
- Assign one primary role per contact: Economic Buyer, Champion, Influencer, Blocker, End User, or Gatekeeper
- Score confidence: High, Medium, or Low

### 4. Score Influence Level

For each stakeholder, compute an influence score (1-10):

| Factor | Weight | How to Assess |
|--------|--------|---------------|
| Seniority | 30% | C-Suite=10, VP=8, Director=6, Manager=4, IC=2 |
| Budget authority | 25% | Owns budget=10, Influences budget=6, No budget role=2 |
| Department relevance | 20% | Primary user dept=10, Adjacent dept=6, Support dept=3 |
| Decision history | 15% | Led prior purchases=10, Participated=6, Unknown=4 |
| Organizational tenure | 10% | 3+ years=8, 1-3 years=6, <1 year=4 |

Compute: `influence_score = sum(factor_value * weight)`

### 5. Identify Gaps

After mapping, check for completeness:
- Is there an identified Economic Buyer? If not, this is a critical gap.
- Are there at least 3 distinct roles represented? Fewer means single-threaded risk.
- Are there any departments that use the product but have no contacts mapped?
- Is there a potential Blocker identified? (Security, Legal, Procurement)

Generate a gap report listing missing roles and departments with recommendations for who to find.

### 6. Push to Attio

For each stakeholder:
1. Create or update the Person record using `attio-contacts`
2. Set custom attributes using `attio-custom-attributes`:
   - `stakeholder_role`: the classified role
   - `stakeholder_confidence`: High/Medium/Low
   - `influence_score`: the computed score (1-10)
   - `engagement_status`: Unengaged (default for new contacts)
   - `discovery_status`: Not Started
3. Link the Person to the Deal record
4. Create an Attio note with the gap report using `attio-notes`

### 7. Log Events

Fire PostHog events for tracking:

```
posthog.capture("stakeholder_mapped", {
  "deal_id": "{deal_id}",
  "stakeholder_count": total_stakeholders,
  "roles_covered": ["Economic Buyer", "Influencer", ...],
  "gaps_found": ["No Blocker identified", ...],
  "influence_score_avg": avg_score
})
```

## Output

- Attio deal record with all stakeholders linked, role-classified, and influence-scored
- Gap report identifying missing roles and departments
- Each stakeholder has: role, confidence, influence score, engagement status, discovery status
- PostHog events logged for threshold evaluation

## Triggers

Run this drill:
- When a new deal enters the "Connected" stage
- When new contacts are added to an existing deal (re-run to update the map)
- Before any multi-stakeholder discovery call prep
- Monthly refresh for all active deals at Connected or later stages
