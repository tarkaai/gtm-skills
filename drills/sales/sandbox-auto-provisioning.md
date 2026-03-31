---
name: sandbox-auto-provisioning
description: Automatically provision personalized sandbox environments when deals reach Connected stage, with intelligent configuration based on CRM and enrichment data
category: Sales
tools:
  - n8n
  - Attio
  - Clay
  - PostHog
  - Loops
  - Anthropic
fundamentals:
  - sandbox-environment-provision
  - sample-data-schema-design
  - seed-data-injection
  - n8n-triggers
  - n8n-workflow-basics
  - n8n-crm-integration
  - n8n-error-handling
  - attio-deals
  - attio-automation
  - attio-custom-attributes
  - clay-company-search
  - clay-enrichment-waterfall
  - posthog-custom-events
  - posthog-feature-flags
  - loops-transactional
  - anthropic-api-patterns
---

# Sandbox Auto-Provisioning

This drill replaces manual sandbox provisioning with a fully automated pipeline. When a deal reaches the Connected stage in Attio, n8n triggers a workflow that enriches the prospect's context, selects the optimal sandbox configuration, provisions the environment, generates personalized onboarding content, and sends access — with zero manual intervention for standard deals.

## Input

- Attio deal pipeline configured with stage webhooks
- Clay workspace with company enrichment tables
- Sandbox infrastructure with API provisioning (from `sandbox-environment-provision`)
- n8n instance with Attio, Clay, PostHog, and Loops integrations
- Anthropic API key for content generation

## Steps

### 1. Configure the Attio trigger

Using `attio-automation` and `n8n-triggers`, set up a webhook that fires when a deal's stage changes to "Connected":

1. In Attio, create an automation rule: "When deal stage changes to Connected, send webhook to n8n."
2. In n8n, create a Webhook trigger node that receives the deal payload.
3. Extract from the payload: `deal_id`, `company_name`, `contact_email`, `contact_name`, `deal_value`, and any custom attributes from discovery.

### 2. Enrich the prospect context

Build an n8n workflow branch that enriches the deal data before provisioning:

1. Use `clay-company-search` to look up the prospect's company. Extract: industry, company size, tech stack, funding stage.
2. Use `clay-enrichment-waterfall` to verify and enrich the contact: confirmed email, LinkedIn profile, job title, seniority.
3. Pull discovery notes from Attio using `attio-deals` — extract use cases, pain points, and competitor mentions.
4. Feed all context to Claude via `anthropic-api-patterns` with a structured prompt:

```
Given this prospect context, determine:
1. Best sample data persona (from available personas: {persona_list})
2. Top 3 features to highlight based on their use cases
3. Custom success checklist (3-5 milestones) tied to their specific pain points
4. Industry-specific walkthrough talking points

Prospect context:
- Company: {company_name}, {industry}, {size} employees
- Contact: {name}, {title}
- Discovery pain points: {pain_points}
- Use cases discussed: {use_cases}
- Competitor mentioned: {competitor}

Return JSON with persona, features, milestones, and talking_points.
```

### 3. Auto-provision the sandbox

Using `sandbox-environment-provision` via the n8n HTTP Request node:

1. Call the provisioning endpoint with the enriched configuration (persona, features, milestones).
2. Verify provisioning succeeded (check response status and sandbox URL accessibility).
3. If provisioning fails, use `n8n-error-handling` to retry once, then alert the deal owner via Slack with the error details.

Update the deal in Attio with sandbox metadata using `attio-custom-attributes`.

### 4. Generate personalized onboarding content

In the n8n workflow, call Claude to generate the kickoff email body:

```
Write a sandbox kickoff email for {contact_name} at {company_name}.
They care about: {use_cases}.
Their pain points: {pain_points}.
The sandbox URL is: {sandbox_url}.
The success checklist is: {milestones}.

Requirements:
- Reference their specific situation (not generic)
- Lead with the most relevant use case
- Include the success checklist as numbered items
- Keep it under 200 words
- End with a Cal.com link to book a walkthrough
```

### 5. Send personalized access

Use `loops-transactional` via n8n to send the kickoff email with:
- AI-generated personalized body
- Sandbox URL and login instructions
- Success checklist
- Walkthrough video link (use the default product walkthrough; AI-personalized videos come at Durable)
- Cal.com booking link

Fire `sandbox_provisioned` and `sandbox_kickoff_sent` PostHog events.

### 6. A/B test sandbox configurations

Using `posthog-feature-flags`, create experiments on sandbox onboarding:

- **Test A**: Sample data persona selection (industry-matched vs. generic)
- **Test B**: Kickoff email format (personalized AI copy vs. template)
- **Test C**: Success checklist length (3 items vs. 5 items)

Track each variant's impact on first-login rate, milestone completion, and sandbox-to-proposal conversion.

### 7. Build the auto-provisioning dashboard

Create a PostHog dashboard tracking:
- Auto-provisioning success rate (target: >95%)
- Average provisioning time (target: <30 seconds)
- First-login rate within 24 hours by configuration variant
- Failure reasons and frequency
- Weekly provisioning volume

### 8. Handle edge cases

Build n8n error-handling branches for:

- **Missing discovery data**: If no discovery notes exist, provision with a generic persona and alert the deal owner to complete discovery and re-configure.
- **Duplicate request**: If a sandbox already exists for this deal, skip provisioning and send a "Your sandbox is still active" reminder instead.
- **Enterprise override**: If deal value exceeds $50K or company size >500, route to manual provisioning workflow for a custom-configured enterprise sandbox.

## Output

- Fully automated sandbox provisioning triggered by CRM stage changes
- AI-personalized sandbox configuration (persona, features, milestones)
- AI-generated kickoff emails
- A/B testing on sandbox onboarding variants
- Auto-provisioning monitoring dashboard
- Edge case handling for failures, duplicates, and enterprise deals

## Triggers

Fires automatically when any deal reaches the Connected stage in Attio. The n8n workflow runs end-to-end in <60 seconds for standard deals.
