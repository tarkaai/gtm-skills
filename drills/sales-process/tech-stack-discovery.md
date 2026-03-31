---
name: tech-stack-discovery
description: Discover a prospect's technical stack, integration landscape, and technical constraints from public signals before a technical discovery call
category: Discovery
tools:
  - Clay
  - Attio
  - Anthropic
fundamentals:
  - clay-claygent
  - clay-enrichment-waterfall
  - clay-company-search
  - account-intelligence-assembly
  - attio-deals
  - attio-notes
  - attio-custom-attributes
---

# Tech Stack Discovery

This drill discovers a prospect's technical environment before a technical discovery call. It surfaces existing tools, likely integration requirements, probable security posture, and technical maturity level — so the founder walks into the call already knowing what questions to ask and what blockers to probe.

## Input

- Deal record in Attio with company name and domain
- Clay account with credits for Claygent queries

## Steps

### 1. Pull existing deal context from Attio

Query Attio for the deal and company record:
```
attio.get_record({ object: "deals", record_id: "{deal_id}" })
attio.get_record({ object: "companies", record_id: "{company_id}" })
```

Extract: company name, domain, industry, employee count, funding stage, any prior technical notes.

### 2. Run tech stack detection via Clay Claygent

Create a Clay table row for the prospect company. Add Claygent columns with these prompts:

**Column 1 — Tech Stack Detection:**
```
Visit {domain} and analyze the page source, job postings on their careers page, and any publicly available technical blog posts. List every technology, tool, and platform this company appears to use. Organize by category: CRM, Marketing, Analytics, Infrastructure, Security, Communication, Development. For each tool, note the evidence source (page source, job posting, blog, etc.).
```

**Column 2 — Integration Landscape:**
```
Based on {Company Name}'s tech stack and industry ({industry}), what systems would they most likely need to integrate a new tool with? List the top 5 integration requirements in order of likelihood. For each, explain why (e.g., "Salesforce — they have 200+ employees in sales-heavy industry, likely the CRM of record").
```

**Column 3 — Security Posture Assessment:**
```
Research {Company Name}'s security and compliance posture. Check: Do they have a security page on their website? Are they SOC2 certified? Do they mention GDPR, HIPAA, or other compliance on their site? Do their job postings mention security team, CISO, or compliance roles? What industry regulations likely apply to them? Return: estimated security maturity (low/medium/high), likely compliance requirements, and evidence.
```

**Column 4 — Technical Maturity Score:**
```
Based on {Company Name}'s size ({employee_count} employees), industry ({industry}), funding stage ({funding}), and tech stack, rate their technical maturity on a scale of 1-5: 1=No technical team, buying off-the-shelf only. 2=Small IT team, basic integrations. 3=Engineering team, API-first approach, moderate integration complexity. 4=Platform engineering team, strict security review, complex integration requirements. 5=Enterprise-grade, formal procurement, security questionnaires mandatory. Return the score and 2-3 bullet points explaining why.
```

### 3. Enrich with job posting analysis

Add a Claygent column to scan the company's open job postings:
```
Search for open job postings at {Company Name}. Look for roles mentioning: DevOps, Platform Engineering, Security, IT, Solutions Architect, Integration Engineer. For each relevant posting, extract: job title, key technologies mentioned, and any platforms/tools listed as requirements. This reveals their internal technical capabilities and what systems they rely on.
```

### 4. Assemble technical intelligence profile

Using Claude, merge all Claygent outputs into a structured technical intelligence profile:

```
POST https://api.anthropic.com/v1/messages

Prompt: "Given this prospect research, create a Technical Intelligence Profile. Return JSON:
{
  "company": "{company_name}",
  "tech_stack": {
    "confirmed": ["tools with strong evidence"],
    "likely": ["tools with moderate evidence"],
    "possible": ["tools with weak evidence"]
  },
  "integration_requirements": [
    {"system": "name", "likelihood": "high|medium|low", "complexity": "simple|moderate|complex", "evidence": "why we think this"}
  ],
  "security_posture": {
    "maturity": "low|medium|high",
    "certifications_likely": ["SOC2", "GDPR", etc.],
    "will_require_security_review": true|false,
    "evidence": "summary of findings"
  },
  "technical_maturity": {
    "score": 1-5,
    "has_engineering_team": true|false,
    "has_security_team": true|false,
    "procurement_complexity": "low|medium|high"
  },
  "discovery_call_focus_areas": ["top 3-5 areas to probe on the call"],
  "predicted_blockers": ["potential deal-killing technical issues to verify"],
  "prepared_questions": [
    {"area": "integration|security|infrastructure|performance|migration", "question": "specific question to ask", "why": "what signal this will surface"}
  ]
}"
```

### 5. Store in CRM and prepare call brief

Push the technical intelligence profile to Attio:
- Store the full JSON as an Attio note on the deal
- Set `tech_stack_researched: true` and `tech_maturity_score: {1-5}`
- Populate `tech_predicted_integrations` with the top 3 integration systems
- Set `tech_security_review_expected: true/false`

Generate a one-page call prep brief and store as an Attio note:
```
## Technical Discovery Call Prep — {Company Name}

### Known Tech Stack: {list}
### Predicted Integration Needs: {list}
### Security Posture: {maturity level} — likely requires: {certifications}
### Technical Maturity: {score}/5

### Priority Questions for This Call:
1. {question} — probing {area}
2. {question} — probing {area}
3. {question} — probing {area}

### Potential Blockers to Verify:
- {blocker 1}
- {blocker 2}
```

### 6. Log discovery event

Fire a PostHog event:
```json
{
  "event": "tech_stack_discovery_completed",
  "properties": {
    "deal_id": "...",
    "company": "...",
    "tech_maturity_score": 3,
    "predicted_integration_count": 5,
    "security_review_expected": true,
    "tools_detected": 12
  }
}
```

## Output

- Technical intelligence profile stored in Attio as a deal note
- Technical maturity score and predicted integrations on the deal record
- Call prep brief with priority questions and predicted blockers
- PostHog event for tracking

## Triggers

Run once per new qualified opportunity, before the first technical discovery call. Re-run if the prospect's company undergoes major changes (acquisition, new funding round, reorg).
