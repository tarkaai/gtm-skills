---
name: case-study-recruitment-smoke
description: >
  Customer Story Pipeline — Smoke Test. Manually identify 5-10 high-fit customers,
  recruit them for case study interviews, and publish at least 3 completed case studies
  to prove that your customer base will participate and produce compelling stories.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product, Email, Direct"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=3 completed case studies"
kpis: ["Recruitment acceptance rate", "Case study completion rate", "Content quality score"]
slug: "case-study-recruitment"
install: "npx gtm-skills add product/referrals/case-study-recruitment"
drills:
  - power-user-scoring
  - case-study-creation
  - threshold-engine
---

# Customer Story Pipeline — Smoke Test

> **Stage:** Product > Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Direct

## Outcomes

Prove that your customer base contains willing, articulate case study participants who can produce stories with measurable results. The pass threshold is 3 completed, published case studies from a pool of 5-10 candidates approached.

## Leading Indicators

- At least 5 customers identified with strong usage metrics and positive sentiment
- Outreach response rate above 30% (candidates reply to the ask)
- At least 4 interviews scheduled (buffer for no-shows or thin stories)
- Interview recordings produce at least 2 quotable metrics per conversation

## Instructions

### 1. Identify candidate customers

Run the `power-user-scoring` drill to score your active user base. Pull the top 10 accounts by composite score. For each, verify manually in Attio:
- They have been active for at least 60 days
- They have no open support escalations
- Their primary contact is reachable (has responded to email in the last 30 days)
- They are in an industry or use case that your prospects would recognize

Narrow to 5-10 candidates. Store them in an Attio list named "Case Study Candidates — Smoke."

### 2. Send personal outreach

Do not use a template blast. For each candidate, write a personal email referencing their specific usage and results. Include:
- The specific metric or behavior that caught your attention (e.g., "Your team has processed 400+ workflows in the last month")
- What the case study involves: a 30-minute video interview, they review the draft before publish
- What they get: published story with backlink, exposure to your audience, positioned as an industry leader
- A direct scheduling link (Cal.com) for the interview

**Human action required:** Send each outreach email personally from the founder or customer success lead. A personal sender increases acceptance rate 2-3x over a generic company address.

### 3. Conduct case study interviews

Run the `case-study-creation` drill for each accepted candidate:
- Prepare 8-10 open-ended questions covering challenge, solution, and results
- Record the interview using Fireflies for transcription
- Ask follow-up questions when specific numbers are mentioned
- Request permission to use their company name, logo, and quotes

### 4. Write and publish case studies

Follow the `case-study-creation` drill's writing process:
- Structure: Challenge (150-200 words), Solution (200-250 words), Results (150-200 words)
- Include a summary box with company name, industry, size, key metric, and pull quote
- Send the draft to the customer for review and approval
- Publish via Ghost or your CMS

**Human action required:** The customer must approve the final draft before publishing. Allow 5-7 business days for their review.

### 5. Evaluate against threshold

Run the `threshold-engine` drill to measure against: >=3 completed case studies.

If PASS: Document what worked — which candidate types accepted, what objections came up, how long the full cycle took from outreach to publish. Proceed to Baseline.

If FAIL: Diagnose the failure point. If candidates declined, the ask or incentive needs work. If interviews produced thin stories, the question framework needs improvement. If customers stalled on approval, the review process needs streamlining. Iterate and re-run.

## Time Estimate

- 1 hour: scoring and candidate identification
- 1 hour: writing personalized outreach for 5-10 candidates
- 1.5 hours: conducting 3-4 interviews (30 min each)
- 1 hour: writing 3 case studies from transcripts
- 0.5 hours: evaluation and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Usage data for candidate scoring | Free tier (1M events/mo) |
| Attio | Candidate tracking and pipeline | Free tier available |
| Fireflies | Interview transcription | Free (800 min/mo); Pro $10/user/mo annual |
| Cal.com | Interview scheduling | Free (1 user) |
| Ghost | Case study publishing | Free (self-hosted); $9/mo (starter) |

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

## Drills Referenced

- `power-user-scoring` — identify top customers by composite usage score
- `case-study-creation` — interview, write, and publish each case study
- `threshold-engine` — evaluate pass/fail against the 3 case study target
