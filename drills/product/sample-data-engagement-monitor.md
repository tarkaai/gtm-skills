---
name: sample-data-engagement-monitor
description: Track how users interact with sample data and templates, measure impact on activation, and identify optimization opportunities
category: Product
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-custom-events
  - posthog-funnels
  - posthog-cohorts
  - posthog-dashboards
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-notes
---

# Sample Data Engagement Monitor

This drill builds a monitoring system that tracks every user interaction with sample data and templates, measures the causal impact on activation and retention, and surfaces actionable optimization opportunities. It is the feedback loop that tells you whether your sample data strategy is working.

## Input

- Sample data seeding deployed (via `sample-data-seeding` drill)
- Template gallery deployed (via `template-gallery-setup` drill, if applicable)
- PostHog tracking events from both drills flowing correctly
- At least 2 weeks of data from users who received sample data

## Steps

### 1. Define the sample data event taxonomy

Using `posthog-custom-events`, ensure these events are tracked consistently:

**Sample Data Lifecycle Events:**
| Event | Trigger | Key Properties |
|-------|---------|---------------|
| `sample_data_injected` | Account seeded with sample data | `persona`, `records_created`, `schema_version` |
| `sample_data_orientation_started` | User sees the sample data walkthrough | `persona`, `step` |
| `sample_data_orientation_completed` | User finishes the walkthrough | `persona`, `steps_completed`, `duration_ms` |
| `sample_data_record_viewed` | User opens a sample record | `entity_type`, `record_id`, `persona` |
| `sample_data_record_edited` | User modifies a sample record | `entity_type`, `record_id`, `field_changed` |
| `sample_data_record_cloned` | User duplicates a sample record | `entity_type`, `record_id` |
| `sample_data_cleared` | User removes all sample data | `days_since_injection`, `records_deleted`, `had_real_data` |

**Template Events:**
| Event | Trigger | Key Properties |
|-------|---------|---------------|
| `template_gallery_viewed` | User visits template gallery | `surface`, `category_filter` |
| `template_previewed` | User previews a template | `template_id`, `surface`, `time_spent_ms` |
| `template_installed` | User installs a template | `template_id`, `surface`, `category` |
| `template_object_edited` | User edits a template-created object | `template_id`, `entity_type`, `edit_type` |
| `template_object_deleted` | User deletes a template-created object | `template_id`, `days_since_install` |

### 2. Build the engagement dashboard

Using `posthog-dashboards`, create a "Sample Data & Templates" dashboard with these panels:

**Row 1 — Volume and reach:**
- Total accounts seeded this week (trend)
- Template installs this week by template (bar chart)
- Sample data coverage: % of new signups who received sample data

**Row 2 — Engagement quality:**
- Sample data interaction rate: % of seeded accounts that viewed at least 1 sample record within 48 hours
- Template install-to-edit rate: % of template installs where the user edited within 7 days
- Mean time to first sample data interaction (trend)

**Row 3 — Impact on activation:**
- Activation rate: seeded users vs. non-seeded users (comparison)
- Activation rate: template users vs. non-template users (comparison)
- Time to activation: seeded vs. non-seeded (distribution)

**Row 4 — Lifecycle signals:**
- Sample data clearance rate by day since injection (histogram)
- Clearance reason distribution (if collected)
- Users who cleared sample data AND created real data within 7 days (the success metric)

### 3. Build the comparison cohorts

Using `posthog-cohorts`, create cohorts for analysis:

- **Seeded users**: `sample_data_injected` event exists
- **Non-seeded users**: No `sample_data_injected` event (control group, if feature-flagged)
- **Engaged with sample data**: Seeded AND at least 1 `sample_data_record_viewed` event
- **Ignored sample data**: Seeded AND zero `sample_data_record_viewed` events within 7 days
- **Template adopters**: At least 1 `template_installed` event
- **Cleared and converted**: `sample_data_cleared` followed by real data creation within 7 days
- **Cleared and churned**: `sample_data_cleared` followed by no activity for 14+ days

Compare these cohorts on: activation rate, 7-day retention, 30-day retention, and time-to-first-real-object.

### 4. Build the activation funnel

Using `posthog-funnels`, create the sample-data-to-activation funnel:

```
sample_data_injected
  → sample_data_orientation_completed
  → sample_data_record_viewed (any)
  → sample_data_record_edited OR real_object_created
  → activation_reached
```

Break down by persona, signup source, and plan. Identify the biggest drop-off step. If most users complete orientation but never view a record, the sample data is not discoverable enough. If they view but never edit, the data is not inspiring action.

### 5. Set up automated alerts

Using `n8n-scheduling` and `n8n-workflow-basics`, create monitoring workflows:

**Daily check:**
- Query PostHog for today's sample data interaction rate
- If interaction rate drops below 50% of the 7-day average, send an alert
- If template install-to-edit rate drops below 25%, flag specific templates

**Weekly report:**
- Aggregate all sample data metrics for the week
- Compare seeded vs. non-seeded activation rates
- Calculate the "sample data lift": the percentage point improvement in activation attributable to sample data
- List the top 3 templates by install count and the bottom 3 by engagement
- Post the report to Slack and store in Attio using `attio-notes`

### 6. Identify optimization opportunities

From the monitoring data, surface specific improvements:

- **Low interaction rate on specific sample records**: These records are not interesting or not discoverable. Redesign them or add in-app pointers.
- **High clearance, low real-data creation**: Users clear sample data but do not create their own — the transition from sample to real is too abrupt. Add a "Create your own based on this sample" flow.
- **Template install without edit**: The template does not match user needs or the post-install experience is confusing. Review the template content and add a guided customization wizard.
- **Persona mismatch**: If a specific persona's sample data underperforms, the content may not resonate with that ICP segment. Regenerate content with better domain specificity.

## Output

- PostHog dashboard with 4 rows of sample data metrics
- 7 comparison cohorts for impact analysis
- Sample-data-to-activation funnel
- Daily alert and weekly report via n8n
- Prioritized list of optimization opportunities

## Triggers

Run the initial setup once after deploying sample data. The monitoring workflows run continuously:
- Daily: interaction rate check and alerts
- Weekly: full report with optimization recommendations
- Monthly: deep-dive cohort analysis comparing sample data lift over time
