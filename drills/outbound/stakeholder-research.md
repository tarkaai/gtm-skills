---
name: stakeholder-research
description: Manually research and classify all stakeholders in a target account's buying committee
category: Prospecting
tools:
  - Clay
  - Attio
  - LinkedIn
fundamentals:
  - org-chart-research
  - stakeholder-role-classification
  - attio-custom-attributes
  - attio-notes
  - clay-people-search
---

# Stakeholder Research

This drill walks through the manual process of identifying, researching, and classifying every stakeholder involved in a deal at a target account. It produces a complete stakeholder map stored in your CRM with role classifications, sentiment ratings, and engagement priorities.

## Input

- A target account with at least one known contact (an active deal or qualified prospect)
- Access to Clay for enrichment and LinkedIn for manual research
- Attio CRM with the deal record created

## Steps

### 1. Start with what you know

Open the deal in Attio. List every contact you have already spoken to or exchanged emails with. For each, note their title, department, and your gut read on their role (Champion, Blocker, etc.). This is your seed list.

### 2. Research the org chart

Run the `org-chart-research` fundamental against the target company in Clay. Pull the top 15-25 people at Director level and above. Focus on departments that will be involved in your deal: the buying department, finance, IT/security, procurement, and executive leadership.

### 3. Classify each stakeholder

Run the `stakeholder-role-classification` fundamental on every contact. For known contacts with interaction history, use behavioral signals to improve classification confidence. For newly discovered contacts with no interaction, classify by title and department only (these will be low-to-medium confidence).

### 4. Set up CRM tracking

Using the `attio-custom-attributes` fundamental, create these custom fields on Person records if they do not already exist:
- `stakeholder_role` (select: Economic Buyer, Champion, Influencer, Blocker, End User, Gatekeeper)
- `stakeholder_confidence` (select: High, Medium, Low)
- `stakeholder_sentiment` (select: Supportive, Neutral, Opposed, Unknown)
- `engagement_level` (select: Active, Warm, Cold, No Contact)

Write the classification for each person to their Attio record.

### 5. Identify gaps and risks

Review the completed map and flag:
- **No Economic Buyer identified**: This is the highest-risk gap. You cannot close without budget authority. Prioritize discovery.
- **No Champion**: Without an internal advocate, you are selling from the outside. Find someone who will carry your message internally.
- **Unaddressed Blockers**: Known Blockers with no engagement plan will silently kill the deal. Plan direct outreach to address their concerns.
- **Single-threaded**: If only 1-2 stakeholders are engaged, the deal is fragile. Any one person leaving or changing priorities stalls everything.

### 6. Document the stakeholder map

Using the `attio-notes` fundamental, create a note on the deal record with the full stakeholder map:
```
## Stakeholder Map — {Company Name}
Updated: {date}

### Economic Buyer
- {Name}, {Title} — Confidence: {H/M/L} — Sentiment: {S/N/O} — Engagement: {level}

### Champion
- {Name}, {Title} — Confidence: {H/M/L} — Sentiment: {S/N/O} — Engagement: {level}

### Influencers
- {Name}, {Title} — Confidence: {H/M/L} — Sentiment: {S/N/O} — Engagement: {level}

### Blockers
- {Name}, {Title} — Confidence: {H/M/L} — Sentiment: {S/N/O} — Engagement: {level}

### End Users
- {Name}, {Title} — Confidence: {H/M/L} — Sentiment: {S/N/O} — Engagement: {level}

### Gaps
- {Missing roles or low-confidence classifications that need discovery}
```

### 7. Prioritize engagement actions

For each stakeholder, define the next action:
- **Economic Buyer**: Schedule a pricing/ROI conversation
- **Champion**: Arm with internal selling materials (one-pagers, ROI calculators, comparison docs)
- **Influencer**: Invite to a technical deep-dive or demo
- **Blocker**: Address concerns directly — schedule a 1:1 or send targeted content
- **End User**: Offer a sandbox or trial experience
- **No Contact**: Find a warm introduction path through the Champion or mutual connections

## Output

- Complete stakeholder map stored as an Attio deal note
- Each person record tagged with role, confidence, sentiment, and engagement level
- Prioritized list of engagement actions per stakeholder
- Gap analysis identifying missing roles and single-threaded risks

## Triggers

- Run this drill when a new deal enters the Connected stage
- Re-run when a deal stalls for 2+ weeks (stakeholder dynamics may have shifted)
- Re-run after every significant meeting where new stakeholders are introduced
