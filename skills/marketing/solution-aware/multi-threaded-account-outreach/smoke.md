---
name: multi-threaded-account-outreach-smoke
description: >
  Multi-threaded Outreach — Smoke Test. Manually coordinate simultaneous outreach to 2-3
  stakeholders within 10 target accounts to validate that role-specific messaging produces
  meetings faster than single-threaded cold outreach.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email, Social, Direct"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥2 meetings from 10 target accounts (2-3 contacts each) in 2 weeks"
kpis: ["Response rate per stakeholder role", "Accounts with multi-stakeholder engagement", "Time to first response"]
slug: "multi-threaded-account-outreach"
install: "npx gtm-skills add marketing/solution-aware/multi-threaded-account-outreach"
drills:
  - icp-definition
  - stakeholder-research
---

# Multi-threaded Outreach — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email, Social, Direct

## Outcomes

Validate that contacting multiple stakeholders within the same account — with role-specific messaging on coordinated timing — produces more meetings than sending cold email to a single contact. The signal to look for is not just reply rate but whether touches to one stakeholder cause another stakeholder to engage (internal referrals, "my colleague mentioned you" responses).

**Pass threshold:** ≥2 meetings booked from 10 target accounts where each account received outreach to 2-3 contacts. At least 1 meeting should involve an internal referral or mention of another thread.

## Leading Indicators

- Connection acceptance rate on LinkedIn ≥30% (validates that the role-specific opener resonates)
- At least 3 accounts where 2+ stakeholders respond (even if only 1 books a meeting)
- At least 1 response that references another stakeholder ("I saw you spoke with my colleague...")
- Response time under 5 business days for Champion-role contacts (they should respond fastest)

## Instructions

### 1. Define your ICP and select 10 target accounts

Run the `icp-definition` drill to document your Ideal Customer Profile. Focus on solution-aware buyers: companies that have evaluated or are currently evaluating tools in your category. Signals: they follow competitors on LinkedIn, they attended a competitor webinar, they have the problem you solve mentioned in job postings.

Select 10 accounts matching this ICP. Prioritize companies with 50-500 employees — large enough to have multiple stakeholders in the buying committee, small enough that you can identify the right people without a massive org chart.

Log the 10 accounts in Attio. For each, create a deal record at the "Prospecting" stage.

### 2. Research and map stakeholders at each account

For each of the 10 accounts, run the `stakeholder-research` drill. Identify 2-3 contacts per account in different roles:

- **Minimum viable thread:** 1 Champion (hands-on user who would benefit from your product) + 1 Economic Buyer (person who controls budget)
- **Better thread:** Add 1 Influencer (technical evaluator or senior IC) for a 3-person thread

Use Clay to find contacts by company + title. Classify each using the role taxonomy from `stakeholder-research`. Store all contacts in Attio linked to the deal record with `stakeholder_role`, `stakeholder_confidence`, and `engagement_level` attributes.

**Human action required:** Manually verify that the contacts are still at the company by checking their LinkedIn profiles. Remove any who have left.

### 3. Design per-account thread maps

For each account, run the the account thread mapping workflow (see instructions below) drill. This produces:
- A message angle for each stakeholder based on their role
- A primary channel assignment (email or LinkedIn) based on their activity
- A timing sequence: Champion on Day 0, End Users/Influencers on Day 2-4, Economic Buyer on Day 7

Write the thread map as a note on each deal in Attio. You should have 10 thread maps, each with 2-3 stakeholders, totaling 20-30 individual messages to draft.

### 4. Draft role-specific messages

For each contact, draft the first-touch message using the angle from the thread map:

- **Champion message**: Reference a specific problem they likely face in their role. Mention a concrete result a similar company achieved. Ask a question about their current workflow — not a pitch.
- **Economic Buyer message**: Lead with a business outcome (cost reduction, revenue impact, risk mitigation). Keep it under 60 words. Mention that their team (role of Champion) is often the one who benefits most.
- **Influencer message**: Share a technical insight relevant to their stack. Link to documentation, an architecture diagram, or a benchmark. Position yourself as a peer, not a seller.

Store each draft as a note on the contact record in Attio.

### 5. Execute the threads manually

**Human action required:** Send each message according to the timing plan. For email, send from your personal inbox (no sequencing tool at Smoke level). For LinkedIn, send connection requests with the drafted note.

Log every send in Attio: update the contact's `engagement_level` to "Active" and add a note with the date, channel, and message sent.

**Critical coordination rule:** Before each send, check Attio for any responses from other stakeholders at the same account. If someone responded positively, adjust the remaining messages to reference their interest.

### 6. Track responses and cross-thread effects

For each response, log in Attio:
- Which stakeholder role responded
- Response sentiment (positive, neutral, negative)
- Whether they mentioned another stakeholder or thread
- Days from send to response

Watch for cross-thread effects: did contacting the Champion make the Economic Buyer more receptive? Did the End User mention your name to the Influencer?

### 7. Evaluate against pass threshold

After 2 weeks, count:
- Total meetings booked from the 10 accounts
- Accounts where 2+ stakeholders engaged
- Internal referrals or cross-thread mentions

**PASS (≥2 meetings + ≥1 cross-thread signal):** The multi-threaded approach produces meetings and creates internal momentum. Proceed to Baseline.

**FAIL (0-1 meetings OR zero cross-thread signals):** Diagnose: Was the ICP wrong (no responses at all)? Was the role-specific messaging off (responses but no meetings)? Was the timing too compressed or too spread out? Adjust and re-run.

## Time Estimate

- ICP definition and account selection: 1 hour
- Stakeholder research across 10 accounts: 2 hours
- Thread map design and message drafting: 2 hours
- Send execution and tracking over 2 weeks: 1 hour
- Total: 6 hours of active work over 1-2 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Find contacts at target companies, enrich with email + LinkedIn | Free tier: 100 credits/mo (https://www.clay.com/pricing) |
| Attio | Track deals, contacts, stakeholder roles, engagement | Free tier: up to 3 users (https://attio.com/pricing) |
| LinkedIn | Connection requests and messages | Free (manual, no Sales Navigator required at Smoke) |
| Personal email | First-touch email outreach | Free |

**Estimated monthly cost:** $0 (all within free tiers)

## Drills Referenced

- `icp-definition` — define the Ideal Customer Profile and account selection criteria
- `stakeholder-research` — research and classify stakeholders at each target account
- the account thread mapping workflow (see instructions below) — design per-account multi-threaded outreach plans with role-specific messaging and timing
