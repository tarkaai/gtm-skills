---
name: sandbox-environment-provision
description: Programmatically provision an isolated sandbox environment for a prospect via product API or infrastructure automation
tool: Product API
difficulty: Advanced
---

# Sandbox Environment Provision

Create an isolated sandbox environment for a sales prospect so they can evaluate the product with realistic data and their own use cases, without affecting production systems.

## When to Use

During the sales process when a deal reaches the Connected stage and a prospect needs hands-on product evaluation. This fundamental handles the technical provisioning; the drill layer handles the sales workflow around it.

## Instructions

### 1. Choose the provisioning method

| Method | Best When | Implementation |
|--------|-----------|---------------|
| **Multi-tenant sandbox** | Your product supports workspace isolation natively | Create a new workspace/org via product API with sandbox flag |
| **Dedicated instance** | Prospect needs full isolation (enterprise, regulated industries) | Spin up a new instance via infrastructure API (AWS, GCP, Vercel) |
| **Feature-flagged sandbox mode** | Product is single-tenant but you can gate features | Use PostHog feature flags to enable sandbox-specific UI and data isolation |
| **Container-based** | You need reproducible, disposable environments | Deploy a pre-built Docker image or Kubernetes namespace per prospect |

### 2. Implement the provisioning endpoint

Create an internal API endpoint that accepts a provisioning request:

```
POST /internal/sandboxes
Headers: Authorization: Bearer {internal_service_token}
Body: {
  "prospect_company": "Acme Corp",
  "prospect_email": "jane@acme.com",
  "deal_id": "attio_deal_abc123",
  "industry": "fintech",
  "persona": "ops_leader",
  "expiry_days": 14,
  "features_enabled": ["core", "integrations", "reporting"],
  "sample_data_persona": "fintech_default"
}
```

The endpoint should:
1. Create the isolated environment (workspace, instance, or namespace).
2. Call the `seed-data-injection` fundamental to populate industry-relevant sample data.
3. Create an admin user account for the prospect with the provided email.
4. Generate a magic link or temporary credentials for first login.
5. Set an expiry date (default 14 days) after which the sandbox auto-deactivates.
6. Return the provisioning result:

```json
{
  "sandbox_id": "sandbox_abc123",
  "url": "https://sandbox-abc123.yourproduct.com",
  "login_method": "magic_link",
  "magic_link": "https://sandbox-abc123.yourproduct.com/auth?token=...",
  "expires_at": "2026-04-13T00:00:00Z",
  "sample_data": { "projects": 3, "records": 45 },
  "status": "ready"
}
```

### 3. Configure environment defaults

Each sandbox should include:
- **Sample data**: Pre-loaded via the `seed-data-injection` fundamental, matched to the prospect's industry and persona.
- **Feature access**: All features enabled by default unless the prospect is evaluating a specific tier.
- **Integrations**: Mock or sandbox versions of third-party integrations the prospect cares about.
- **Usage limits**: Set generous but bounded limits (e.g., 1,000 API calls, 10 GB storage) to prevent abuse.

### 4. Implement lifecycle management

Build endpoints for sandbox lifecycle operations:

```
GET /internal/sandboxes/{sandbox_id}/status
  → { "status": "active|expired|deactivated", "usage": {...}, "days_remaining": 7 }

POST /internal/sandboxes/{sandbox_id}/extend
Body: { "additional_days": 7 }
  → Extends expiry. Maximum 30 days total.

DELETE /internal/sandboxes/{sandbox_id}
  → Deactivates sandbox, archives data, frees resources.
```

### 5. Wire into CRM

After provisioning, update the deal in Attio (or your CRM) with sandbox metadata:

```json
{
  "sandbox_url": "https://sandbox-abc123.yourproduct.com",
  "sandbox_id": "sandbox_abc123",
  "sandbox_provisioned_at": "2026-03-30T10:00:00Z",
  "sandbox_expires_at": "2026-04-13T00:00:00Z",
  "sandbox_status": "active"
}
```

Use the `attio-custom-attributes` fundamental to create these fields if they do not exist.

### 6. Track provisioning events

Fire PostHog events:

```javascript
posthog.capture('sandbox_provisioned', {
  sandbox_id: 'sandbox_abc123',
  deal_id: 'attio_deal_abc123',
  industry: 'fintech',
  persona: 'ops_leader',
  sample_data_records: 45,
  provisioning_duration_ms: 3200
});
```

## Error Handling

- **Provisioning timeout**: If environment creation exceeds 60 seconds, queue it as a background job and notify the sales rep when ready.
- **Capacity limits**: If maximum concurrent sandboxes is reached, queue the request and alert ops.
- **Provisioning failure**: Retry once. If the retry fails, create a support ticket and notify the sales rep with an ETA.
- **Expired sandbox access**: Return a friendly "Your sandbox has expired" page with a CTA to request an extension or schedule a call.

## Output

A fully provisioned, isolated sandbox environment with sample data, accessible via URL and magic link, tracked in the CRM with expiry management.
