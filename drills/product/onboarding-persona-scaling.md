---
name: onboarding-persona-scaling
description: Scale persona-specific onboarding from 2-3 personas to 5+ with multi-channel delivery, automated persona classification, and per-segment optimization
category: Product
tools:
  - Intercom
  - PostHog
  - Loops
  - n8n
fundamentals:
  - intercom-product-tours
  - intercom-in-app-messages
  - posthog-feature-flags
  - posthog-cohorts
  - posthog-custom-events
  - loops-sequences
  - loops-audience
  - n8n-triggers
  - n8n-workflow-basics
---

# Onboarding Persona Scaling

This drill takes a working persona-based onboarding system (2-3 personas, proven at Baseline) and scales it to handle 5+ personas across multiple channels without proportional manual effort. The key shift: automated persona classification replaces manual tagging, and each persona's onboarding path spans in-app tours, email sequences, and contextual messages simultaneously.

## Prerequisites

- `onboarding-personalization` drill completed with 2-3 working persona tours
- Baseline activation data showing per-persona rates for at least 4 weeks
- At least 500 total users onboarded to have enough data per persona
- Intercom, PostHog, Loops, and n8n all operational

## Steps

### 1. Analyze activation data to discover new personas

Using the `posthog-cohorts` fundamental, cluster users who activated successfully but do not fit your existing 2-3 persona definitions. Look for patterns in:

- Job title / role (from signup or enrichment)
- First actions taken in the product (sequence of events in first 24 hours)
- Features used most in first week
- Company size and industry
- Signup source and referral path

Identify 2-3 additional persona segments where the current generic fallback tour underperforms. Each new persona must have at least 50 historical users and a measurably different activation path from existing personas.

### 2. Build automated persona classification

Using `n8n-triggers` and `n8n-workflow-basics`, create a classification workflow that fires on `signup_completed`:

1. Receive the PostHog webhook with signup data
2. Collect signals: role field from signup form, email domain (enriched via Clay if available), company size, signup source UTM parameters, referral path
3. Apply classification rules (if/else chain or weighted scoring):
   - Role contains "engineer" or "developer" AND signup source is "github" or "docs" → `technical_builder`
   - Role contains "manager" or "director" or "VP" AND company_size > 10 → `team_lead`
   - Company_size = 1 or role contains "freelance" or "solo" → `solo_creator`
   - Role contains "marketing" or "growth" → `marketer`
   - Role contains "sales" or "revenue" → `sales_user`
   - Default → `general` (gets the best-performing generic tour)
4. Write `persona_type` to both PostHog (via `posthog-custom-events`) and Intercom (via `intercom-user-properties` API call in n8n)
5. Write `persona_confidence` property: "explicit" (user selected role), "inferred" (classification rules), or "default" (no signal)

### 3. Create per-persona email sequences

Using the `loops-sequences` fundamental, build persona-specific email sequences alongside the in-app tours. Each persona gets a 5-email sequence (see `onboarding-sequence-design` for content framework) where:

- Subject lines reference the persona's specific use case
- CTAs link to the persona's activation action (not generic dashboard)
- Use case examples match the persona's industry or role
- Skip logic exits users from the sequence when they reach persona-specific activation

Using `loops-audience`, segment contacts by `persona_type` and enroll each new contact into their matching sequence automatically.

### 4. Add contextual in-app messages per persona

Using `intercom-in-app-messages`, create nudge messages for each persona's common stall points:

- If persona = `team_lead` and has not invited teammates after 48 hours: show tooltip "Invite your team to get started together"
- If persona = `technical_builder` and has not connected an integration after 72 hours: show banner "Connect your first integration in 2 minutes"
- If persona = `solo_creator` and has not created a project after 24 hours: show tooltip pointing to "New project" button

Each message fires once. Dismissed messages do not return. Messages do not overlap with active product tour steps.

### 5. Set up per-persona feature flags

Using `posthog-feature-flags`, create a multi-variant feature flag `onboarding-persona-v2` with one variant per persona. This flag controls:

- Which product tour starts
- Which dashboard layout the user sees on first login
- Which sample data or templates are pre-loaded
- Which help articles appear in the Intercom help center widget

Route flag assignment based on the `persona_type` property set in Step 2.

### 6. Build per-persona funnels and dashboards

Using `posthog-cohorts` and `posthog-custom-events`, build one activation funnel per persona:

```
signup_completed (persona=X)
  → tour_started (persona=X)
  → tour_completed (persona=X)
  → activation_reached (persona=X)
```

Also build a comparative dashboard showing all personas side by side: activation rate, time to activation, tour completion rate, email open rate, and email click rate. This dashboard is the primary input for identifying which persona paths need A/B testing.

### 7. Run per-persona A/B tests

For the worst-performing persona (lowest activation rate), use `posthog-feature-flags` to test variations:

- Test A: Different tour structure (3 steps vs 5 steps)
- Test B: Different first action (simpler initial milestone)
- Test C: Email-first vs tour-first (which channel drives activation better for this persona?)

Run one test at a time per persona. Require 100+ users per variant before evaluating. Use the `ab-test-orchestrator` drill for statistical rigor.

## Output

- 5+ persona-specific onboarding paths (tours + emails + in-app messages)
- Automated persona classification assigning 95%+ of new signups without manual tagging
- Per-persona activation funnels showing comparative performance
- At least one completed A/B test per persona improving the weakest activation paths
