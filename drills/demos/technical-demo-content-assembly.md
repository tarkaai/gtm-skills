---
name: technical-demo-content-assembly
description: Assemble prospect-customized technical demo materials including API walkthroughs, architecture diagrams, integration code samples, and security documentation
category: Demos
tools:
  - Anthropic
  - Attio
  - Clay
  - PostHog
fundamentals:
  - technical-demo-script-generation
  - tech-stack-detection
  - account-intelligence-assembly
  - attio-deals
  - attio-notes
  - attio-contacts
  - posthog-custom-events
---

# Technical Demo Content Assembly

This drill takes a scheduled technical deep-dive demo and produces a complete set of customized technical materials: a demo script with live API calls, integration code tailored to the prospect's tech stack, architecture talking points mapped to their requirements, and a security review checklist. It differs from `demo-prep-automation` (which focuses on pain-to-feature mapping for business demos) by going deep into the technical layer -- actual API endpoints, real code, and architecture details that engineers and architects evaluate.

## Input

- Deal record in Attio at Connected stage with a technical deep-dive demo scheduled
- Attendee list with at least one technical stakeholder (engineer, architect, CTO, VP Engineering)
- Discovery notes or transcript with technical requirements identified
- Product API documentation, architecture overview, integration catalog, and security documentation (stored in config or provided as file paths)

## Steps

### 1. Detect the prospect's tech stack

Run `tech-stack-detection` on the prospect's domain via Clay. Retrieve their current technologies categorized by:
- Infrastructure (cloud provider, CDN, hosting)
- Backend frameworks and languages
- Databases and data stores
- Authentication providers
- Analytics and monitoring
- CI/CD and deployment
- Integration middleware (Zapier, n8n, Workato, etc.)

Store the tech stack on the Attio deal record for reuse.

### 2. Pull account intelligence and discovery context

Run `account-intelligence-assembly` to gather firmographics, recent news, and competitive context. Pull discovery notes from Attio using `attio-notes` -- extract every technical requirement, constraint, and concern the prospect mentioned.

Classify each attendee using `attio-contacts`:
- **Architect**: Cares about system design, scalability, reliability. Prioritize architecture module.
- **Backend Engineer**: Cares about APIs, SDKs, developer experience. Prioritize API walkthrough.
- **DevOps/SRE**: Cares about deployment, monitoring, uptime. Prioritize infrastructure and observability.
- **Security Engineer/CISO**: Cares about auth, encryption, compliance. Prioritize security module.
- **CTO/VP Engineering**: Cares about total cost of ownership, team velocity, technical debt. Prioritize integration and architecture.

### 3. Generate the technical demo script

Run `technical-demo-script-generation` with the prospect's tech stack, technical requirements, pain points, and attendee profiles. The output is a structured demo script with:
- Ordered modules (architecture, API, integration, security) weighted by attendee profiles
- Live API calls to execute during the demo, with request/response payloads
- Integration code snippets targeting tools from the prospect's actual stack
- Security topics calibrated to their compliance requirements
- Anticipated technical questions with prepared answers

### 4. Prepare the sandbox environment for live demo

If the prospect has a sandbox (check Attio for `sandbox_url` custom attribute), configure it for the demo:
- Pre-populate with data relevant to the demo modules
- Set up the specific integrations that will be demonstrated
- Verify all API calls in the demo script execute successfully against the sandbox
- Create bookmarked URLs or saved API requests (in Postman/Insomnia collection or curl scripts) for each live demo step

If no sandbox exists, prepare a shared demo environment with the prospect's industry-relevant configuration.

### 5. Build the technical follow-up package

Assemble a prospect-specific technical package:

1. **API Documentation**: Links to relevant API docs, filtered to endpoints shown in the demo
2. **Integration Guide**: Step-by-step guide for connecting to the specific tools in their stack (e.g., "Connecting to your PostgreSQL via our REST API" not generic "Database integrations")
3. **Architecture Diagram**: High-level architecture diagram annotated with where their systems connect
4. **Security Documentation**: Compliance certifications, encryption specs, auth flow documentation, SOC2/GDPR/HIPAA details as relevant to their requirements
5. **SDK and Code Samples**: Code in the language(s) detected in their stack, showing the integration patterns demoed

Store the package as an Attio note on the deal, ready to share post-demo.

### 6. Store the demo prep and track quality

Save the full demo script and technical package to Attio using `attio-notes`:

```
attio.create_note({
  parent: { object: "deals", record_id: "{deal_id}" },
  title: "Technical Demo Prep — {company_name} — {demo_date}",
  content: "{demo_script_markdown}",
  tags: ["technical-demo-prep"]
})
```

Fire PostHog events using `posthog-custom-events`:

```json
{
  "event": "technical_demo_prepped",
  "properties": {
    "deal_id": "...",
    "company_name": "...",
    "modules_prepared": ["architecture", "api", "integration", "security"],
    "tech_stack_detected": true,
    "integration_targets": ["PostgreSQL", "AWS", "Datadog"],
    "attendee_roles": ["CTO", "Senior Engineer"],
    "sandbox_configured": true,
    "follow_up_package_ready": true
  }
}
```

After the demo, log the outcome:

```json
{
  "event": "technical_demo_completed",
  "properties": {
    "deal_id": "...",
    "modules_shown": ["architecture", "api", "integration"],
    "live_api_calls_executed": 5,
    "technical_questions_asked": 8,
    "technical_blockers_identified": ["SSO integration with Okta"],
    "outcome": "poc_requested|proposal_requested|follow_up_needed|no_interest",
    "duration_minutes": 35,
    "attendee_count": 4
  }
}
```

## Output

- Structured technical demo script with ordered modules, live API calls, and integration code
- Sandbox environment configured for the demo (if available)
- Prospect-specific technical follow-up package (API docs, integration guide, architecture diagram, security docs, code samples)
- All materials stored in Attio on the deal record
- PostHog events for demo prep tracking and outcome measurement

## Triggers

- Run when a technical deep-dive demo is scheduled (Cal.com webhook for bookings tagged "technical-demo")
- Re-run if the prospect shares additional technical requirements before the demo
- Re-run if new attendees are added (especially if a new role type changes the module weighting)
