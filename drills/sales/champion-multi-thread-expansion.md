---
name: champion-multi-thread-expansion
description: Leverage active champions to map additional stakeholders and create multi-threaded deal engagement
category: Sales
tools:
  - Clay
  - Attio
  - Instantly
  - Anthropic
fundamentals:
  - clay-people-search
  - clay-enrichment-waterfall
  - attio-contacts
  - attio-deals
  - attio-champion-tracking
  - attio-notes
  - instantly-campaign
  - ai-content-ghostwriting
---

# Champion Multi-Thread Expansion

This drill uses active champions as leverage to identify and engage additional stakeholders within the account. Single-threaded deals (relying on one contact) are the #1 deal-killer. This drill systematically expands deal coverage by mapping the buying committee through and around the champion.

## Input

- Active champions in Attio (`champion_status` = "Active", `champion_score` >= 60)
- Deal records with linked company and champion
- Clay account for stakeholder enrichment

## Steps

### 1. Map the Buying Committee

For each deal with an active champion, identify the buying committee roles that need to be engaged:

| Role | Typical Title | Purpose |
|------|---------------|---------|
| Economic Buyer | VP/C-level in champion's chain | Final budget authority |
| Technical Evaluator | Senior Engineer/Architect | Validates technical fit |
| End Users | Team members in champion's department | Will use the product daily |
| Legal/Procurement | Legal Counsel, Procurement Manager | Contract review |
| Executive Sponsor | CxO or SVP | Strategic alignment |

Using `clay-people-search`, find contacts at the champion's company matching each role. Enrich with `clay-enrichment-waterfall` for emails and LinkedIn profiles.

### 2. Ask the Champion for the Map

Generate a stakeholder mapping request using `ai-content-ghostwriting`:

```
"Draft a short email from me to {champion_name} asking them to help map the decision process at {company}. The tone should be collaborative, not interrogative. Frame it as: 'I want to make sure we're including the right people early so this doesn't stall later.' Ask them to confirm:
1. Who has final budget authority for this type of purchase?
2. Who else on your team would need to evaluate this?
3. Is there anyone in IT/security who needs to sign off?
4. Who should we NOT contact directly (politically sensitive)?

Keep it under 100 words."
```

Send this email and log the response in Attio using `attio-notes`. The champion's response is gold — it tells you the org chart AND the political landscape.

### 3. Cross-Reference Champion Input with Clay Data

Compare the champion's mapping response against the Clay research:
- Names the champion mentioned → update Attio contacts with confirmed roles
- Names Clay found but champion didn't mention → ask champion about these in a follow-up ("I noticed {name} is also on the {department} team — are they involved in decisions like this?")
- Roles the champion mentioned but Clay can't find contacts for → ask champion for introductions

### 4. Build Role-Specific Outreach

For each identified stakeholder, create tailored messaging using `ai-content-ghostwriting`:

**Economic Buyer:**
- Lead with ROI and business impact
- Reference the champion by name (with their permission): "Your team lead {champion_name} has been evaluating our platform and suggested I share the business case with you"
- Include the one-page business case from the enablement kit

**Technical Evaluator:**
- Lead with architecture, integration, and security
- Offer a technical deep-dive or sandbox access
- Reference specific technical requirements if the champion shared them

**End Users:**
- Lead with day-to-day workflow improvements
- Offer a hands-on demo focused on their specific use case
- Keep it short — end users are busy and don't care about strategy

**Executive Sponsor:**
- Lead with strategic alignment and competitive advantage
- Keep email to 3 sentences maximum
- Suggest a 15-minute briefing, not a demo

### 5. Execute Champion-Assisted Introductions

The best path to stakeholders is through the champion. For each stakeholder:

**Preferred path (champion introduces):**
Generate a draft introduction email for the champion to send using `ai-content-ghostwriting`:
```
"Draft an internal email that {champion_name} can forward to {stakeholder_name} introducing us. Write it in {champion_name}'s voice. Keep it to 3 sentences: what the product does, why they've been evaluating it, and a request for {stakeholder_name} to take a meeting with us. Do not use marketing language."
```

Send the draft to the champion and ask them to forward it.

**Fallback path (direct outreach with champion reference):**
If the champion can't or won't introduce, send a direct email using `instantly-campaign` that references the champion:
"Hi {stakeholder_name}, I've been working with {champion_name} on your team regarding {project/initiative}. They suggested it would be valuable to include you in the conversation because {role-specific reason}."

### 6. Track Multi-Threading Progress

Update Attio for each deal:
- Link all new stakeholder contacts to the Deal
- Set their role (Technical Evaluator, Economic Buyer, etc.) as a custom attribute
- Track: total contacts engaged, meetings held per role, and deal stage progression

Log a `champion_introduced_colleague` event in PostHog each time the champion facilitates an introduction.

### 7. Measure Multi-Thread Impact

Query Attio to compare:
- Average contacts per deal (champion-assisted vs non-champion)
- Deal velocity for multi-threaded vs single-threaded deals
- Win rate by number of stakeholder roles covered

## Output

- Buying committee mapped for each active deal
- Role-specific messaging drafted for each stakeholder
- Champion-assisted introduction drafts delivered
- All new contacts linked to Deals in Attio with role labels
- Multi-threading metrics tracked in PostHog

## Triggers

- Run when a champion reaches "Active" status with a score >= 60
- Re-run when a new role is identified that isn't yet covered
- Run proactively before any deal moves from Qualified → Proposed (ensure multi-threading before proposal)
