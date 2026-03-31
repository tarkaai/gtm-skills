---
name: ugc-health-monitor
description: Monitor UGC program health with diagnostic triggers, automated interventions, and escalation rules specific to content creation and amplification
category: Advocacy
tools:
  - PostHog
  - n8n
  - Intercom
  - Loops
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-cohorts
  - posthog-anomaly-detection
  - posthog-custom-events
  - n8n-scheduling
  - n8n-triggers
  - intercom-in-app-messages
  - loops-transactional
  - attio-lists
  - attio-notes
---

# UGC Health Monitor

This drill builds the play-specific monitoring layer for the UGC campaign. It complements the generic `autonomous-optimization` loop by tracking UGC-specific metrics, diagnosing content creation and amplification problems, and triggering UGC-specific interventions. The output is a daily health check that keeps the UGC flywheel spinning.

## Prerequisites

- UGC collection, moderation, and amplification pipelines running for at least 4 weeks (baseline data)
- PostHog tracking all UGC events
- n8n instance for scheduled monitoring
- Attio with UGC Library and Contributors lists populated

## Steps

### 1. Define the 8 UGC health metrics

Configure daily health checks for each metric using `posthog-dashboards`:

| Metric | Calculation | Healthy Range | Warning | Critical |
|--------|-------------|---------------|---------|----------|
| Submission rate | New UGC submissions per week | 5+ per week | 2-4 per week | <2 per week |
| Approval rate | Approved / total submitted (trailing 30 days) | 60%+ | 40-59% | <40% |
| Prompt conversion rate | `ugc_form_completed` / `ugc_prompt_shown` | 5%+ | 2-4.9% | <2% |
| Creator diversity | Unique creators / total submissions (trailing 30 days) | 50%+ unique | 30-49% unique | <30% (too few people creating) |
| Repeat creator rate | Creators with 2+ submissions / total creators | 25%+ | 15-24% | <15% |
| Amplification throughput | Pieces amplified per week / pieces approved per week | 80%+ | 50-79% | <50% (backlog building) |
| Referral traffic from UGC | Visits attributed to UGC links per week | Growing or stable | Declining 2 weeks | Declining 4+ weeks |
| Content quality trend | Average moderation composite score (trailing 30 days) | 3.5+ | 3.0-3.49 | <3.0 |

### 2. Build the daily health check workflow

Using `n8n-scheduling`, create a workflow that runs every morning:

1. Query PostHog for each of the 8 metrics (trailing 4-week rolling values)
2. Classify each metric: healthy, warning, critical
3. If all healthy: log to Attio, no action
4. If any warning: log to Attio with the specific metric and current value
5. If any critical: trigger diagnostic workflow (step 3) and escalate

Using `posthog-custom-events`, fire a daily `ugc_health_check` event:

```json
{
  "submission_rate": 7,
  "submission_rate_status": "healthy",
  "approval_rate": 0.65,
  "approval_rate_status": "healthy",
  "prompt_conversion": 0.03,
  "prompt_conversion_status": "warning",
  "creator_diversity": 0.55,
  "creator_diversity_status": "healthy",
  "repeat_rate": 0.12,
  "repeat_rate_status": "critical",
  "amplification_throughput": 0.85,
  "amplification_throughput_status": "healthy",
  "referral_traffic": 120,
  "referral_traffic_status": "healthy",
  "quality_trend": 3.8,
  "quality_trend_status": "healthy",
  "overall_health": "warning",
  "metrics_critical": 1,
  "metrics_warning": 1,
  "metrics_healthy": 6
}
```

### 3. Implement diagnostic triggers

For each metric that enters warning or critical, run a targeted diagnostic:

**Submission rate declining:**
- Check prompt impression volume: are fewer users seeing UGC prompts? If so, check cohort sizes and frequency capping rules.
- Check prompt conversion rate: are users seeing prompts but not acting? The ask may be stale or the timing wrong.
- Check external detection: are fewer users posting about the product organically? This may be a product engagement issue upstream.

**Approval rate declining:**
- Check the distribution of rejection reasons from the moderation API: are submissions getting worse (quality issue), or is the moderation model too strict?
- Check if a specific content type is driving rejections: if all rejected pieces are "reviews," the review prompt may be attracting low-effort submissions.
- Check new vs. returning creators: if new creators have low approval rates, the submission form needs clearer guidance.

**Prompt conversion rate declining:**
- Check prompt dismissal rates by trigger type: which prompts are being ignored?
- Check if frequency capping is too aggressive (users want to contribute but are suppressed)
- Compare conversion by user tier: if power users still convert but standard users don't, the prompts may need better targeting.

**Creator diversity declining (same few people creating):**
- Check if the creator tier system is creating a "contributor class" that crowds out new voices
- Check if UGC prompts are reaching new users or only re-prompting existing creators
- Check which trigger moments produce the most first-time creators and amplify those triggers.

**Repeat creator rate declining:**
- Check the gap between first and second submission: if average gap exceeds 30 days, the follow-up engagement is too slow
- Check if the creator tier rewards are motivating: query PostHog for `ugc_creator_promoted` events and correlate with subsequent submissions
- Check if featured creators are being notified when their content is amplified (notification failure kills repeat motivation)

**Amplification throughput declining (backlog building):**
- Check if the weekly selection workflow is running
- Check if content quality is too low for amplification (approved but not amplifiable)
- Check if the team is bottlenecking on manual approvals for review-queue items

**Referral traffic declining:**
- Check which amplification channels are driving traffic: has a channel stopped performing?
- Check if UGC links are still live (link rot)
- Check social engagement rates on UGC posts: if impressions are stable but clicks declining, the content or CTAs need refreshing

**Content quality declining:**
- Check by content type: are certain types dragging the average down?
- Check by submission source: are external detections lower quality than in-product submissions?
- Check if the UGC prompts are producing formulaic responses (a sign the prompt templates need variation)

### 4. Configure automated interventions

Using `n8n-triggers`, deploy automated responses:

- **Prompt fatigue detected** (prompt conversion drops below 2% for 2 weeks): automatically rotate to the next prompt variant in Intercom. If all variants have been tried, pause prompts for 2 weeks and surface a different engagement mechanism.
- **Repeat rate stall** (below 15% for 3 weeks): trigger a "comeback creator" email via Loops to all First-time Creators who submitted 30-60 days ago but haven't returned. Include a specific themed challenge or contest invitation.
- **Amplification backlog** (>10 approved pieces unshared for 7+ days): trigger an alert to the content team with the backlog count and the top 3 pieces ranked by amplification score.
- **Quality decline** (average below 3.0 for 2 weeks): update the submission form to include a quality tip: "The best submissions include specific results or numbers. Example: 'I saved 3 hours per week by...'"

### 5. Build the weekly health report

Using `n8n-scheduling`, generate a weekly report every Monday:

1. Aggregate daily health checks for the week
2. Trend analysis: which metrics improved, declined, or held steady
3. Intervention outcomes: which automated interventions fired and what happened
4. Top content: the 3 highest-scoring UGC pieces of the week
5. Creator spotlight: highlight 1 new and 1 returning creator
6. Pipeline status: submissions pending review, approved awaiting amplification, recently amplified
7. Recommendations: what the optimization loop should focus on next
8. Store in Attio as a note on the UGC program record
9. Post summary to Slack

### 6. Set escalation rules

Define when the agent should stop and request human intervention:

- Any metric critical for 5+ consecutive days
- Submission rate drops to zero for 7 days (the pipeline is broken)
- Approval rate below 30% for 2 weeks (either content quality cratered or moderation is miscalibrated)
- 3+ automated interventions fired in one week with no improvement
- A creator flags that they were featured without permission (immediate escalation, pause amplification)

Escalation format: Slack alert with metric name, current value, healthy range, days in warning/critical, diagnostics run, interventions attempted, and recommended next step.

## Output

- Daily health check workflow with 8 UGC-specific metrics
- Diagnostic triggers for each declining metric
- 4 automated interventions for common UGC failure modes
- Weekly health report with trends, creator spotlights, and recommendations
- Escalation rules for human handoff

## Triggers

Daily health check runs every morning via n8n cron. Interventions fire on their specific triggers. Weekly report runs Monday morning. All workflows are always-on.
