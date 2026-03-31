---
name: technical-collateral-matching
description: Automatically match prospect technical requirements to relevant technical documentation, security certifications, integration guides, and case studies
category: Sales
tools:
  - Attio
  - Anthropic
  - n8n
fundamentals:
  - attio-deals
  - attio-notes
  - n8n-workflow-basics
  - n8n-triggers
---

# Technical Collateral Matching

This drill takes a prospect's stated technical requirements (from `technical-discovery-call`) and automatically surfaces the most relevant technical collateral: API documentation, security whitepapers, compliance certificates, integration guides, architecture diagrams, and case studies from similar technical environments. It eliminates the manual work of hunting through internal repos for the right doc to send.

## Input

- Deal record in Attio with technical requirements extracted (from `call-transcript-tech-requirements-extraction`)
- A technical collateral catalog (see Step 1 for how to build it)

## Steps

### 1. Build and maintain a technical collateral catalog

Create an Attio list called "Technical Collateral Catalog" with these attributes:
- `collateral_title` (text): Name of the document
- `collateral_type` (select): API Docs, Integration Guide, Security Whitepaper, Compliance Certificate, Architecture Diagram, Case Study, Performance Benchmark, Migration Guide, FAQ
- `relevant_categories` (multi-select): Integrations, Security, Infrastructure, Performance, Data Migration
- `relevant_systems` (multi-select): Salesforce, HubSpot, Slack, Okta, Azure AD, AWS, GCP, etc.
- `relevant_certifications` (multi-select): SOC2, GDPR, HIPAA, ISO27001, FedRAMP, PCI-DSS
- `relevant_industries` (multi-select): Healthcare, Finance, SaaS, E-commerce, Government, etc.
- `file_url` (URL): Link to the document
- `last_updated` (date): When the document was last reviewed for accuracy

Populate this catalog with every piece of technical collateral your company has. This is a one-time setup task, maintained as new collateral is created.

**Human action required:** Initially populate the collateral catalog. The agent cannot create security whitepapers or compliance certificates — it can only match existing ones.

### 2. Match requirements to collateral

When a deal has technical requirements extracted, run the matching logic:

Send the deal's technical requirements + collateral catalog to Claude:

```
POST https://api.anthropic.com/v1/messages

Prompt: "Given this prospect's technical requirements and our collateral catalog, select the most relevant documents to send. Return JSON.

Prospect Requirements:
{tech_requirements_json from deal record}

Collateral Catalog:
{catalog entries as JSON array}

Return:
{
  "matches": [
    {
      "collateral_title": "...",
      "collateral_type": "...",
      "file_url": "...",
      "relevance_reason": "one sentence explaining why this is relevant to this specific prospect",
      "addresses_requirement": "the specific requirement this addresses",
      "priority": "send_immediately|include_in_followup|have_ready_for_questions"
    }
  ],
  "gaps": [
    {
      "requirement": "...",
      "gap_description": "We don't have collateral addressing this requirement",
      "recommended_action": "create_new_doc|request_from_engineering|custom_response_needed"
    }
  ],
  "followup_email_sections": [
    {
      "heading": "section heading for the follow-up email",
      "body": "1-2 sentences introducing the attached collateral and how it addresses their specific requirement",
      "attachments": ["collateral_title_1", "collateral_title_2"]
    }
  ]
}"
```

### 3. Generate a technical follow-up package

Using the matches, assemble a follow-up package:

**Immediate send (within 24 hours of discovery call):**
- Documents matching `priority: send_immediately`
- A cover email referencing the specific requirements discussed

Generate the email using Claude:
```
Subject: {Company Name} — Technical Documentation Following Our Call

{Prospect name},

Following our technical discussion today, I wanted to send over the specific documentation you asked about:

{For each send_immediately match:}
- **{collateral_title}** — {relevance_reason}
  {file_url}

{If security certifications were requested:}
Our {certification} documentation is attached. If your security team needs additional detail, I'm happy to schedule a call with our security lead.

{If integration guides were relevant:}
The integration documentation covers {specific systems mentioned}. Our API supports {relevant capabilities}. Let me know if your engineering team has questions.

{If gaps exist:}
You also asked about {gap requirement}. I'm pulling together the relevant details and will follow up by {date}.

{closing with next step from discovery call}
```

Store the email draft and collateral list as an Attio note on the deal.

### 4. Flag collateral gaps for content team

For any `gaps` returned by the matching:
- Create an Attio note tagged `collateral_gap`
- If the gap is `create_new_doc`, log a PostHog event:
```json
{
  "event": "tech_collateral_gap_detected",
  "properties": {
    "deal_id": "...",
    "requirement": "...",
    "gap_type": "create_new_doc",
    "deal_value": "..."
  }
}
```
- Track gap frequency over time — if multiple prospects need the same collateral, prioritize creating it

### 5. Track collateral effectiveness

Log which collateral was sent and whether the deal progressed:
```json
{
  "event": "tech_collateral_sent",
  "properties": {
    "deal_id": "...",
    "collateral_titles": ["doc1", "doc2"],
    "collateral_count": 2,
    "categories_addressed": ["security", "integrations"],
    "gaps_count": 1
  }
}
```

After the deal progresses (or stalls), correlate collateral sent with deal outcome. Over time this reveals which collateral actually helps close deals.

## Output

- Matched collateral list with relevance explanations
- Draft follow-up email with attached documentation
- Gap report for content team
- PostHog events for tracking collateral effectiveness

## Triggers

- Run after every `technical-discovery-call` completion
- Re-run if new collateral is added to the catalog (batch re-match across open deals)
- Re-run if a deal's technical requirements change after a follow-up call
