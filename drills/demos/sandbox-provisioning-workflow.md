---
name: sandbox-provisioning-workflow
description: Manually provision sandbox environments for qualified prospects with personalized sample data and kickoff materials
category: Demos
tools:
  - Attio
  - PostHog
  - Loops
  - Loom
fundamentals:
  - sandbox-environment-provision
  - sample-data-schema-design
  - seed-data-injection
  - attio-deals
  - attio-notes
  - attio-custom-attributes
  - loops-transactional
  - loom-recording
  - posthog-custom-events
---

# Sandbox Provisioning Workflow

This drill handles the end-to-end process of provisioning a sandbox environment for a qualified sales prospect: preparing the environment, populating it with relevant sample data, sending access with onboarding materials, and logging the provisioning in the CRM.

## Input

- A deal in Attio at the Connected stage with a completed discovery call
- Prospect's industry, role, and top use cases (from discovery notes in Attio)
- Product sandbox infrastructure ready (see `sandbox-environment-provision` fundamental)

## Steps

### 1. Qualify the sandbox request

Before provisioning, verify the deal justifies a sandbox. Pull the deal record from Attio using `attio-deals`:

- Deal stage must be Connected or later
- Discovery call must be completed (check Attio notes or Fireflies transcript)
- At least 2 specific use cases identified during discovery

If qualification criteria are not met, log a note in Attio explaining why sandbox was deferred and recommend the sales rep complete discovery first.

### 2. Design the sandbox configuration

Based on discovery notes, determine:

1. **Industry persona**: Which sample data persona best matches the prospect's business (e.g., `fintech_default`, `saas_growth`, `ecommerce_ops`). If no existing persona fits, use the `sample-data-schema-design` fundamental to create a new one.
2. **Feature set**: Which product features to highlight based on their stated use cases. Enable all features by default but prepare guidance that steers toward the relevant ones.
3. **Success checklist**: Define 3-5 specific workflows the prospect should complete to validate fit. Each milestone maps to a discovery pain point. Example:
   - "Import a sample dataset" (validates data handling)
   - "Build a custom report" (validates reporting)
   - "Set up an automated workflow" (validates automation)

Store the success checklist in Attio as a note on the deal.

### 3. Provision the environment

Run the `sandbox-environment-provision` fundamental:

1. Call the provisioning endpoint with the prospect's details, chosen persona, and feature configuration.
2. Verify the sandbox is accessible (GET the sandbox URL and confirm a 200 response).
3. Confirm sample data was injected (check the provisioning response for record counts).
4. Update the deal in Attio with sandbox metadata using `attio-custom-attributes`:
   - `sandbox_url`, `sandbox_id`, `sandbox_provisioned_at`, `sandbox_expires_at`, `sandbox_status`

Fire the `sandbox_provisioned` PostHog event using `posthog-custom-events`.

### 4. Prepare kickoff materials

Generate personalized onboarding content:

1. **Kickoff email**: Draft via Loops using `loops-transactional`. Include:
   - Sandbox URL and login instructions
   - The success checklist (3-5 items) tied to their specific use cases
   - Link to a walkthrough video (step 5)
   - Cal.com link to book a guided walkthrough call

2. **Walkthrough video**: Record a 3-5 minute Loom using `loom-recording` showing:
   - How to log in and orient themselves
   - A quick tour of the sample data relevant to their industry
   - How to complete the first success checklist item
   - Where to get help if they get stuck

Store the Loom link in Attio on the deal record.

### 5. Send sandbox access

Send the kickoff email via Loops with:
- Subject: "Your [Product] sandbox is ready — here's how to get started"
- Personalization: reference specific pain points from discovery
- Clear first action: complete success checklist item #1
- Expectation setting: "You have 14 days to explore. I'll check in after 48 hours."

Log the send in Attio and fire a `sandbox_kickoff_sent` PostHog event.

### 6. Schedule follow-up touchpoints

Create follow-up tasks in Attio:
- **48 hours post-send**: Check if prospect has logged in. If not, send a reminder.
- **Day 5**: Check milestone progress. If <2 milestones completed, offer a walkthrough call.
- **Day 10**: Check engagement score. If hot (61+), propose next steps. If cold (<30), send a "what's blocking you?" message.
- **Day 13**: Final reminder before expiry. Offer extension if engaged.

## Output

- Provisioned sandbox environment with industry-relevant sample data
- Personalized kickoff email sent with video walkthrough
- Deal record updated in Attio with sandbox metadata
- Follow-up touchpoints scheduled
- PostHog events: `sandbox_provisioned`, `sandbox_kickoff_sent`

## Triggers

Run when a deal reaches Connected stage and discovery is complete. Can also be triggered manually by the sales rep for any qualified opportunity.
