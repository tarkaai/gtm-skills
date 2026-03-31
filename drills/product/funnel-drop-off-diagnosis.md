---
name: funnel-drop-off-diagnosis
description: Diagnose the root cause of funnel drop-offs using session recordings, path analysis, and behavioral signals to produce prioritized fix recommendations
category: Product
tools:
  - PostHog
  - Anthropic
  - Attio
fundamentals:
  - posthog-session-recording
  - posthog-user-path-analysis
  - posthog-funnels
  - posthog-cohorts
  - hypothesis-generation
  - attio-notes
---

# Funnel Drop-Off Diagnosis

This drill takes a funnel with a known bottleneck step (identified by `signup-funnel-audit` or equivalent instrumentation) and systematically diagnoses WHY users drop off at that step. It combines quantitative path analysis with qualitative session recording review to produce ranked, testable hypotheses.

## Input

- A PostHog funnel insight ID showing the conversion flow
- The specific step with the highest absolute drop-off (the bottleneck)
- At least 100 users who reached the bottleneck step in the last 30 days
- PostHog session recordings enabled for the funnel pages

## Steps

### 1. Quantify the drop-off by segment

Using the `posthog-funnels` fundamental, break down the bottleneck step conversion rate by:

- `device_type` (mobile vs desktop) — mobile friction is the most common hidden killer
- `utm_source` / `$referring_domain` — traffic source differences reveal expectation mismatches
- `$browser` — browser-specific rendering bugs cause invisible drop-offs
- User properties: plan type, signup method (OAuth vs email), cohort week

Query via PostHog API:
```
POST /api/projects/<id>/insights/funnel/
{
  "filters": {
    "insight": "FUNNELS",
    "events": [
      {"id": "{bottleneck_step_event}"},
      {"id": "{next_step_event}"}
    ],
    "breakdown": "{property}",
    "breakdown_type": "event",
    "funnel_window_days": 7
  }
}
```

Rank segments by conversion rate. The segment with the lowest conversion rate is the highest-leverage fix target.

### 2. Analyze user paths at the bottleneck

Using the `posthog-user-path-analysis` fundamental, pull the paths users take when they reach the bottleneck step:

- **Completers path:** What do users who pass the bottleneck step do differently? Which pages do they visit? Which actions do they take?
- **Drop-off path:** Where do non-completers go instead? Do they bounce entirely, navigate to help docs, go back to a previous step, or visit pricing?

Create two PostHog cohorts using `posthog-cohorts`:
- "Funnel completers" — users who fired both the bottleneck event AND the next step event within the conversion window
- "Funnel droppers" — users who fired the bottleneck event but NOT the next step event within the conversion window

Compare their paths. The divergence point reveals the friction.

### 3. Review session recordings of drop-off users

Using the `posthog-session-recording` fundamental, pull recordings filtered to the "Funnel droppers" cohort:

```
GET /api/projects/<id>/session_recordings/?person_uuid_in_cohort={dropper_cohort_id}&date_from=-14d&limit=25
```

Review 20-25 recordings. For each recording, classify the drop-off cause:

| Category | Indicators |
|----------|-----------|
| **Form confusion** | User fills fields out of order, re-enters data, hovers over labels, scrolls up and down |
| **Validation blocking** | User hits error messages repeatedly on the same field, tries different inputs |
| **Technical failure** | Page errors, loading spinners that never resolve, broken buttons, layout shifts |
| **Mobile friction** | Keyboard covers fields, tap targets too small, horizontal scroll, form overflows viewport |
| **Trust hesitation** | User pauses at sensitive fields (password, payment, phone), reads privacy policy, opens new tabs to research |
| **Effort abandonment** | User starts the step, sees the amount of work required, and leaves immediately |
| **Value confusion** | User completes the step but then navigates aimlessly, suggesting they do not understand what the step accomplished |
| **Distraction exit** | User switches tabs, checks other apps, then never returns (no friction visible — context switch) |

Tally the categories. The most common category is the primary diagnosis.

### 4. Generate hypotheses

Pass the following to the `hypothesis-generation` fundamental:

```
Context: Funnel drop-off diagnosis for step "{bottleneck_step_name}"

Quantitative data:
- Overall conversion at this step: {X}%
- Worst segment: {segment} at {Y}% (vs {X}% average)
- Best segment: {segment} at {Z}%

Path analysis:
- Completers typically: {common completer behavior}
- Droppers typically: {common dropper behavior}

Session recording diagnosis (N={count} recordings reviewed):
- Primary friction category: {category} ({count}/{total})
- Secondary friction category: {category} ({count}/{total})
- Notable observations: {observations}

Generate 3-5 ranked hypotheses. For each:
1. What is the root cause?
2. What specific change would fix it?
3. What is the expected conversion lift?
4. How would you test this change?
5. Implementation effort (low/medium/high)

Rank by: expected_lift * confidence / effort
```

### 5. Store diagnosis output

Using the `attio-notes` fundamental, log the diagnosis as a structured note:

```json
{
  "funnel_name": "{funnel}",
  "bottleneck_step": "{step}",
  "baseline_conversion": "{X}%",
  "recordings_reviewed": {count},
  "primary_diagnosis": "{category}",
  "hypotheses": [
    {
      "rank": 1,
      "root_cause": "...",
      "proposed_fix": "...",
      "expected_lift": "...",
      "test_method": "...",
      "effort": "low|medium|high"
    }
  ],
  "diagnosis_date": "{ISO date}",
  "status": "pending_action"
}
```

## Output

- Segment-level conversion breakdown revealing the worst-performing segments
- User path comparison between completers and droppers
- Session recording friction classification (N=20-25 recordings)
- 3-5 ranked hypotheses with proposed fixes, expected lift, and test plans
- Attio note with full diagnosis for downstream action

## Triggers

Run once per identified bottleneck. Re-run when a previously fixed bottleneck re-emerges or a new bottleneck becomes the primary drop-off point.
