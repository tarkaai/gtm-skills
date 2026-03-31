---
name: sample-data-seeding
description: Design, generate, and deploy realistic sample data into new user accounts to accelerate time-to-value
category: Product
tools:
  - PostHog
  - Anthropic
  - n8n
fundamentals:
  - sample-data-schema-design
  - seed-data-injection
  - posthog-custom-events
  - posthog-feature-flags
  - n8n-workflow-basics
---

# Sample Data Seeding

This drill produces a complete sample data package for your product: the schema design, realistic content, injection mechanism, cleanup flow, and tracking. The output is a working system that pre-populates new accounts with data that demonstrates the product's core value.

## Input

- Your product's data model (entities, relationships, required fields)
- Your activation metric (the user action that predicts retention)
- The product's core value proposition (what makes it worth using)
- PostHog installed with user identification

## Steps

### 1. Audit the empty-state experience

Before building sample data, measure the current empty-state experience:

1. Create a fresh test account in your product
2. Using `posthog-custom-events`, capture the current time-to-first-action for new users: how long from signup to first meaningful interaction
3. Screenshot every empty state the user encounters (empty dashboard, empty project list, empty inbox)
4. Document where users get stuck: which empty states cause the most drop-off in your PostHog onboarding funnel

The empty states with the highest drop-off are where sample data has the most impact.

### 2. Design the sample data schema

Run the `sample-data-schema-design` fundamental to produce a seed file. Design the schema to address the top 3 empty-state drop-off points identified in step 1.

Key design decisions:
- **Persona-based**: Create 2-3 sample data personas matching your top ICP segments. A project management tool might have "Marketing Team" and "Engineering Sprint" personas. Each persona gets different sample data.
- **Progressive disclosure**: Do not dump everything at once. Seed the minimum data needed for the first session. Additional sample data can load when users explore deeper features.
- **Value demonstration**: At least one sample record must showcase the product's unique differentiator in a completed state, so users can see the outcome before they do any work.

### 3. Generate realistic content

Use the Anthropic API (via `anthropic-api-patterns`) to generate sample data content. For each entity in the schema:

1. Write a generation prompt specifying the product domain, entity type, field constraints, and realism requirements
2. Generate content for all personas
3. Validate that dates, statuses, and relationships are internally consistent
4. Review for cultural sensitivity and industry accuracy — sample data that references real companies or uses culturally specific names may alienate users outside that context

Store generated content in a seed file per persona: `seeds/default.json`, `seeds/marketing_team.json`, `seeds/engineering_sprint.json`.

### 4. Implement injection and cleanup

Run the `seed-data-injection` fundamental to build:
- The injection endpoint that creates sample records during account provisioning
- The cleanup endpoint that removes sample records when users are ready
- PostHog event tracking for both injection and cleanup

Decision: should sample data be opt-in or opt-out?
- **Opt-out (recommended for Smoke test)**: Inject sample data by default. Show a "Clear sample data" button prominently. Track how many users clear vs. keep.
- **Opt-in**: Show an empty state with a "Load sample data" option. Track how many users choose to load it.

Use PostHog feature flags (via `posthog-feature-flags`) to A/B test opt-in vs. opt-out if you have sufficient traffic.

### 5. Build the first-run experience around sample data

The sample data should not just appear — the product should guide users through it:

1. On first login after injection, show a brief orientation: "We've set up a sample [project/workspace/pipeline] so you can explore. Here's what to try first."
2. Highlight 1-2 specific sample records that demonstrate the product's core value
3. Include a clear call-to-action: "When you're ready, create your own [project] or clear the sample data"
4. Use `posthog-custom-events` to track each orientation step: `sample_data_orientation_started`, `sample_data_orientation_completed`, `sample_data_first_interaction`

### 6. Set up refresh automation

Using `n8n-workflow-basics`, create a workflow that:
1. Runs monthly to regenerate sample data content (so it stays current with dates and trends)
2. Validates the seed file against the current product schema (catches breaking changes)
3. Alerts the team if validation fails (schema drift)

## Output

- 2-3 persona-based seed files with realistic sample data
- Injection endpoint wired into the signup flow
- Cleanup endpoint with a UI button
- First-run orientation guiding users through sample data
- PostHog tracking on every sample data lifecycle event
- Monthly refresh automation via n8n

## Triggers

Run once during initial play setup. Re-run when:
- Product schema changes significantly (new entities, removed fields)
- New ICP segments are identified (add new personas)
- Sample data content becomes stale (quarterly refresh)
