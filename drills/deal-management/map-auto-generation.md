---
name: map-auto-generation
description: Auto-generate a Mutual Action Plan when a deal reaches proposal stage by populating the correct template with deal-specific data
category: Deal Management
tools:
  - Attio
  - n8n
  - Claude API
  - Loops
fundamentals:
  - attio-deals
  - attio-custom-attributes
  - attio-notes
  - n8n-workflow-basics
  - n8n-triggers
  - n8n-crm-integration
  - n8n-email-integration
---

# MAP Auto-Generation

This drill creates an n8n workflow that automatically generates a Mutual Action Plan when a deal moves to the Proposed stage. The agent selects the right template based on deal characteristics, personalizes milestones with deal-specific dates and stakeholders, and delivers the draft MAP for review.

## Input

- MAP templates created via `map-template-creation` drill (stored in Attio)
- Deal data from Attio: value, company, contacts, stage, close date
- n8n instance with Attio and email integrations configured

## Steps

### 1. Create the trigger workflow in n8n

Using `n8n-triggers`, build a workflow triggered when a deal's stage changes to "Proposed" in Attio:

**Trigger:** Attio webhook — Deal status updated to "Proposed"

**Step 1 — Classify deal type:**
Using `attio-deals`, pull the deal record: value, company size, number of associated contacts (stakeholder count), and industry.

Apply classification rules:
- Value < $15K AND stakeholder count <= 2 → SMB Quick-Close
- Value $15K-$75K OR stakeholder count 3-5 → Mid-Market Standard
- Value > $75K OR stakeholder count > 5 → Enterprise Complex

**Step 2 — Retrieve the matching template:**
Using `attio-notes`, query the MAP Templates record for the note matching the classified deal type.

**Step 3 — Personalize the template:**
Using Claude API, generate the personalized MAP:

Prompt:
```
Given this deal context:
- Company: {company_name}
- Primary contact: {contact_name}, {contact_title}
- Deal value: {deal_value}
- Expected close date: {close_date}
- Stakeholders: {list of associated contacts with titles}

And this MAP template:
{template_milestones}

Generate a personalized Mutual Action Plan with:
1. Concrete dates for each milestone working backward from the expected close date
2. Specific owner assignments using actual contact names where the owner is "Buyer"
3. Any milestone adjustments based on the company type or deal specifics
4. A summary paragraph explaining the MAP to the prospect

Output as structured markdown.
```

**Step 4 — Store the MAP in Attio:**
Using `attio-notes`, create a new note on the deal with the personalized MAP. Using `attio-custom-attributes`, update:
- `map_status` → "Active"
- `map_created_date` → today
- `map_deal_type` → classified type
- `map_completion_pct` → 0
- `map_at_risk` → false
- `map_expected_close` → calculated close date from milestones

**Step 5 — Send MAP draft to rep:**
Using `n8n-email-integration`, send the personalized MAP to the deal owner (rep/founder) for review before sharing with the prospect. Include a link to the Attio deal record.

### 2. Build the prospect delivery workflow

After the rep reviews and approves the MAP (manually marks it as approved in Attio or replies to the email), trigger a second workflow:

**Trigger:** Attio attribute `map_status` updated to "Active" (or manual approval signal)

**Step 1 — Format for prospect delivery:**
Using Claude API, convert the MAP into a clean, professional email:

```
Subject: {Company} x {Your Company} — Shared Action Plan

Hi {Champion First Name},

Following our conversation, I've put together a shared timeline for getting {Company} live with {Product}. This covers what we'll handle on our end and what you'll need on yours.

[MAP milestones formatted as a clean table]

The goal is to keep us both on track so nothing falls through the cracks. Would you review this and let me know if the dates and owners look right?

[Signature]
```

**Step 2 — Send via Loops or direct email:**
Using `n8n-email-integration`, send the MAP email to the champion contact. Log the send in Attio as a note.

### 3. Handle edge cases

Build error handling in the n8n workflow:

- **No expected close date:** Prompt the rep to set one before generating the MAP
- **No contacts associated:** Alert the rep to add stakeholders to the deal
- **Deal value missing:** Default to Mid-Market template and flag for rep review
- **Multiple deals for same company:** Generate separate MAPs, link them in Attio notes

## Output

- n8n workflow that auto-generates MAP when deals reach Proposed stage
- Personalized MAP with concrete dates and named stakeholders
- MAP stored in Attio with tracking attributes populated
- Prospect delivery email sent after rep approval
- Error handling for incomplete deal data
