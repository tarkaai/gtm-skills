---
name: seed-data-injection
description: Programmatically inject sample data records into a new user account via product API or database
tool: Product
product: Product API
difficulty: Advanced
---

# Seed Data Injection

Programmatically insert sample data records into a user's account so they see a populated product experience on first login.

## When to Use

After designing the sample data schema (via `sample-data-schema-design`), use this fundamental to actually insert the records. This runs during account provisioning (signup flow) or on-demand when a user requests sample data.

## Instructions

### 1. Choose the injection method

| Method | Best When | Implementation |
|--------|-----------|---------------|
| **Product API** | Your product has a RESTful or GraphQL API with create endpoints for all entities | Call the API sequentially, respecting rate limits and auth context |
| **Database seed script** | You have direct database access and need speed | Run SQL INSERT or ORM create operations in a transaction |
| **Background job** | Injection takes >2 seconds and should not block signup | Queue a job (Sidekiq, Bull, Celery) that runs after account creation completes |
| **Feature flag gated** | You want to A/B test sample data vs. empty accounts | Use PostHog feature flags to decide whether to inject at signup |

### 2. Implement the injection endpoint

Create an internal API endpoint or function that accepts:

```
POST /internal/accounts/{account_id}/seed-sample-data
Headers: Authorization: Bearer {internal_service_token}
Body: {
  "schema_version": "1.0",
  "persona": "default",
  "force": false
}
```

The endpoint should:
1. Check if the account already has sample data (`_sample: true` records exist). If `force` is false and sample data exists, return 200 with no-op.
2. Read the seed file for the specified persona from the product's config or asset storage.
3. Create records in dependency order: parent entities first, then child entities, then relationships.
4. Tag every created record with `_sample: true` and `_seed_version: "1.0"` metadata.
5. Return a summary: `{ "created": { "projects": 3, "tasks": 15, "comments": 6 }, "duration_ms": 450 }`.

### 3. Wire into the signup flow

Trigger injection at the right moment in account provisioning:

**Option A — Synchronous (if <2 seconds):**
```
signup_completed → create_account → seed_sample_data → redirect_to_dashboard
```

**Option B — Asynchronous (if >2 seconds):**
```
signup_completed → create_account → redirect_to_dashboard → queue_seed_job
```
Show a loading skeleton or progress indicator while seeding completes. Use a WebSocket or polling endpoint to notify the frontend when data is ready.

**Option C — On-demand:**
Add a "Load sample data" button on the empty-state screen. Wire it to the injection endpoint. This lets users opt in rather than forcing sample data on everyone.

### 4. Implement the cleanup endpoint

Users must be able to remove sample data when they are ready to use real data:

```
DELETE /internal/accounts/{account_id}/sample-data
Headers: Authorization: Bearer {internal_service_token}
```

The endpoint should:
1. Query all records where `_sample: true` for the given account.
2. Delete in reverse dependency order: relationships first, then children, then parents.
3. Return a summary: `{ "deleted": { "projects": 3, "tasks": 15, "comments": 6 } }`.

Expose this as a "Clear sample data" button in the product UI, with a confirmation dialog: "This will remove all sample projects, tasks, and comments. Your real data will not be affected."

### 5. Track injection and cleanup events

Fire PostHog events for every lifecycle moment:

```javascript
posthog.capture('sample_data_injected', {
  account_id: accountId,
  schema_version: '1.0',
  persona: 'default',
  records_created: 24,
  duration_ms: 450
});

posthog.capture('sample_data_cleared', {
  account_id: accountId,
  records_deleted: 24,
  days_since_injection: 5,
  had_real_data: true
});
```

These events feed into the `sample-data-engagement-monitor` drill.

## Error Handling

- **Partial injection failure**: If record creation fails mid-way, roll back the transaction. Never leave an account with partial sample data.
- **Schema mismatch**: If the seed file references a field or entity that no longer exists, log the error, skip the record, and alert the engineering team.
- **Rate limiting**: If using the product API, batch creates and respect rate limits. Add exponential backoff for 429 responses.
- **Duplicate prevention**: Always check for existing sample data before injection. Idempotent by default.

## Output

A seeded user account with realistic sample data, ready for the user to explore. Plus PostHog events tracking the injection.
