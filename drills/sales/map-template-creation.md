---
name: map-template-creation
description: Create Mutual Action Plan templates with milestone structures tailored to deal type, size, and complexity
category: Sales
tools:
  - Attio
  - Claude API
fundamentals:
  - attio-custom-attributes
  - attio-deals
  - attio-notes
---

# MAP Template Creation

This drill builds Mutual Action Plan (MAP) templates — structured milestone timelines co-owned by your team and the prospect that define every step from proposal to signature. Templates are parameterized by deal type so an agent can generate the right MAP for any opportunity.

## Input

- Deal type taxonomy: define the 2-4 deal archetypes in your pipeline (e.g., SMB Quick-Close, Mid-Market Standard, Enterprise Complex)
- Average sales cycle length per deal type (from Attio deal history)
- List of buyer-side activities required for purchase (legal review, procurement, security, executive approval)
- List of seller-side deliverables (proposal, security questionnaire, SOW, implementation plan)

## Steps

### 1. Define deal type taxonomy

Query Attio for all Closed Won deals from the last 12 months using `attio-deals`. Group by deal value and cycle length:

- **SMB Quick-Close:** Deal value < $15K, cycle < 30 days, 1-2 decision makers
- **Mid-Market Standard:** Deal value $15K-$75K, cycle 30-60 days, 3-5 stakeholders
- **Enterprise Complex:** Deal value > $75K, cycle 60-120 days, 5+ stakeholders, includes procurement/legal/security

Adjust thresholds based on your actual deal data. The taxonomy should cover >= 90% of your pipeline.

### 2. Create MAP custom attributes in Attio

Using `attio-custom-attributes`, create the following fields on the Deal object:

| Attribute | Slug | Type | Purpose |
|-----------|------|------|---------|
| MAP Status | `map_status` | select (Not Started, Active, Complete, Stalled) | Current state of the MAP |
| MAP Created Date | `map_created_date` | date | When the MAP was shared with the prospect |
| MAP Deal Type | `map_deal_type` | select (SMB, Mid-Market, Enterprise) | Which template was used |
| MAP Completion % | `map_completion_pct` | number | Percentage of milestones completed |
| MAP At-Risk | `map_at_risk` | checkbox | Whether any milestone is overdue |
| MAP Expected Close | `map_expected_close` | date | Close date derived from milestone timeline |
| MAP Stall Count | `map_stall_count` | number | Number of times a milestone has slipped |

### 3. Build milestone templates per deal type

For each deal type, define the milestone sequence. Each milestone has: name, owner (Seller or Buyer), typical duration, dependencies, and completion criteria.

**SMB Quick-Close Template (5 milestones, ~14 days):**

| # | Milestone | Owner | Duration | Dependencies | Done When |
|---|-----------|-------|----------|-------------|-----------|
| 1 | Proposal delivered | Seller | Day 0 | Demo completed | Prospect confirms receipt |
| 2 | Proposal review call | Both | Day 3-5 | Milestone 1 | Call completed, questions answered |
| 3 | Decision maker alignment | Buyer | Day 5-10 | Milestone 2 | DM confirms intent to proceed |
| 4 | Contract sent and reviewed | Both | Day 10-12 | Milestone 3 | Redlines returned or approved |
| 5 | Signature and kickoff scheduled | Buyer | Day 12-14 | Milestone 4 | Contract signed |

**Mid-Market Standard Template (8 milestones, ~45 days):**

| # | Milestone | Owner | Duration | Dependencies | Done When |
|---|-----------|-------|----------|-------------|-----------|
| 1 | Proposal delivered | Seller | Day 0 | Demo completed | Prospect confirms receipt |
| 2 | Technical review / Q&A | Both | Day 3-7 | Milestone 1 | Technical questions resolved |
| 3 | Stakeholder alignment meeting | Both | Day 7-14 | Milestone 2 | All stakeholders briefed |
| 4 | Business case / ROI review | Both | Day 14-21 | Milestone 3 | ROI validated by buyer |
| 5 | Legal review initiated | Buyer | Day 21-28 | Milestone 4 | Legal team has contract |
| 6 | Security / compliance review | Buyer | Day 21-28 | Milestone 4 | Security questionnaire returned |
| 7 | Final terms negotiation | Both | Day 28-35 | Milestones 5, 6 | All redlines resolved |
| 8 | Signature and kickoff scheduled | Buyer | Day 35-45 | Milestone 7 | Contract signed |

**Enterprise Complex Template (12 milestones, ~90 days):**

| # | Milestone | Owner | Duration | Dependencies | Done When |
|---|-----------|-------|----------|-------------|-----------|
| 1 | Proposal and scope document delivered | Seller | Day 0 | Discovery/demo complete | Prospect confirms receipt |
| 2 | Technical deep-dive / architecture review | Both | Day 3-10 | Milestone 1 | Technical requirements documented |
| 3 | POC / pilot scope agreement | Both | Day 10-14 | Milestone 2 | POC scope signed off |
| 4 | POC execution | Both | Day 14-35 | Milestone 3 | POC success criteria met |
| 5 | POC results review | Both | Day 35-40 | Milestone 4 | Results presented to buying committee |
| 6 | Business case / ROI presented to exec sponsor | Both | Day 40-50 | Milestone 5 | Exec sponsor approves business case |
| 7 | Procurement engaged | Buyer | Day 50-55 | Milestone 6 | Procurement contact identified |
| 8 | Legal review initiated | Buyer | Day 50-60 | Milestone 6 | Legal team has contract |
| 9 | Security / compliance review | Buyer | Day 50-65 | Milestone 6 | Security review completed |
| 10 | Final terms negotiation | Both | Day 65-75 | Milestones 7, 8, 9 | All terms finalized |
| 11 | Executive approval | Buyer | Day 75-85 | Milestone 10 | Budget approved, sign-off obtained |
| 12 | Signature and kickoff scheduled | Buyer | Day 85-90 | Milestone 11 | Contract signed |

### 4. Store templates as Attio notes

Using `attio-notes`, create a note on a dedicated "MAP Templates" company record in Attio (or use your own company record). Store each template as a structured markdown note so the agent can retrieve it programmatically when generating a MAP for a specific deal.

### 5. Validate templates against historical data

Query Attio for the last 10 Closed Won deals per deal type. For each:
- Map the actual deal timeline against the template milestones
- Check: Does the template cover the actual steps that happened?
- Check: Are the duration estimates within 25% of actual?
- Adjust milestone durations based on historical averages

## Output

- 3 MAP milestone templates stored in Attio (SMB, Mid-Market, Enterprise)
- 7 custom attributes on the Deal object for MAP tracking
- Deal type taxonomy documented
- Templates validated against >= 10 historical deals
