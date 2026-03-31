---
name: feature-spotlight-series-scalable
description: >
  Weekly Feature Spotlights — Scalable Automation. Scale the series by testing spotlight formats,
  personalizing per segment, and automating the full pipeline to reach all eligible users with
  minimal manual intervention.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥25% trial rate across 500+ users per spotlight with automated pipeline and <1 hour/week manual effort"
kpis: ["Trial rate at scale", "Adoption rate at scale", "Per-segment performance", "Pipeline automation rate", "Experiment win rate"]
slug: "feature-spotlight-series"
install: "npx gtm-skills add product/retain/feature-spotlight-series"
drills:
  - ab-test-orchestrator
  - spotlight-content-pipeline
  - spotlight-series-health-monitor
---

# Weekly Feature Spotlights — Scalable Automation

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Trial rate of 25% or more across 500+ targeted users per spotlight, with the full pipeline running on automation requiring less than 1 hour of human oversight per week. The 10x multiplier comes from three sources: testing to find the best spotlight format, personalizing spotlights per user segment, and automating the end-to-end pipeline so it runs itself.

## Leading Indicators

- Pipeline runs weekly with no manual intervention beyond approval (automation works)
- A/B tests producing statistically significant winners at least once per month (optimization is active)
- Different user segments receiving different spotlight variants (personalization is live)
- Trial rate holding above 25% as audience size scales past 500 per spotlight (no quality decay at scale)
- Feature coverage increasing: new features spotlighted within 4 weeks of launch

## Instructions

### 1. Test spotlight formats to find the best performing variant

Run the `ab-test-orchestrator` drill to systematically test the spotlight components that have the most impact on trial rate:

**Round 1 — Content format (weeks 1-3):**
Test two spotlight formats head-to-head using PostHog feature flags to split the target cohort:
- **Variant A (current):** Benefit-led headline + 150-word body + screenshot + CTA button
- **Variant B (interactive):** Same headline + 50-word body + embedded interactive demo or video walkthrough + CTA button

Measure: trial rate (primary), click-through rate (secondary). Run for 3 spotlights to accumulate sufficient sample size. Adopt the winner.

**Round 2 — Delivery timing (weeks 4-6):**
Test when spotlights are most effective:
- **Variant A:** Spotlight delivered during the user's active session (triggered by session start)
- **Variant B:** Spotlight delivered via email at a scheduled time (Tuesday 10am)

Measure: trial rate (primary), time-to-trial (secondary). Adopt the winner.

**Round 3 — Personalization depth (weeks 7-8):**
Test whether personalized spotlights outperform generic ones:
- **Variant A (generic):** Same spotlight content for all users in the target cohort
- **Variant B (personalized):** Spotlight headline references the user's most-used related feature: "You use [Feature X] every day — did you know [Spotlight Feature] makes it even better?"

Measure: trial rate (primary), adoption rate (secondary). Adopt the winner.

### 2. Scale the content pipeline with segment personalization

Run the `spotlight-content-pipeline` drill with these Scalable-level enhancements:

**Multi-segment targeting:** Instead of one cohort per spotlight, create 2-3 segments for each feature based on usage patterns:
- **Power users of related features**: They will see the most value. Message: "Level up your [related feature] workflow with [spotlight feature]."
- **Moderate users**: They use the product but have not explored deeply. Message: "Did you know you can [benefit]? Most [role] users find this saves them [time/effort]."
- **At-risk users (declining engagement)**: The spotlight doubles as a re-engagement touchpoint. Message: "There's a faster way to [task they used to do]. Check out [spotlight feature]."

Each segment gets a tailored headline and body copy while sharing the same visual and CTA.

**Automated content generation:** Extend the n8n workflow to auto-draft spotlight content based on templates:
1. Query PostHog for the feature's top use cases (most common workflows involving the feature)
2. Pull the feature's help documentation or changelog entry
3. Generate benefit-led headline and body copy from the use case data
4. **Human action required:** Approve or edit the auto-generated content. Target: review should take <15 minutes per spotlight.

### 3. Monitor series health and detect scaling problems

Run the `spotlight-series-health-monitor` drill to build the measurement infrastructure that keeps the series healthy at scale:

- Deploy the per-spotlight performance funnel and series-level dashboard
- Configure fatigue detection: declining open rates, rising dismiss rates, or shrinking target audiences are the signals that the series is wearing out
- Track audience saturation: if >30% of active users have received 6+ spotlights, implement tiered frequency (weekly for engagers, biweekly for non-engagers)
- Generate the weekly series report with per-segment breakdowns

Key scaling-specific metrics to watch:
- **Quality at scale**: Is trial rate holding above 25% as you target 500+ users per spotlight? If trial rate drops as audience grows, the outer segments are less receptive — tighten targeting or improve personalization.
- **Pipeline throughput**: Can the pipeline produce a new spotlight every week without bottlenecks? If human review becomes the bottleneck, invest more in auto-generated content quality.
- **Feature backlog velocity**: Are you spotlighting features faster than new features ship? If the backlog is exhausted, consider re-spotlighting features to new user cohorts who joined after the first spotlight.

### 4. Evaluate against threshold

After 8 weeks, measure:

- **Pass (trial ≥25% across 500+ users AND pipeline requires <1 hour/week):** The series scales. Proceed to Durable to deploy autonomous optimization.
- **Marginal pass (trial ≥25% but pipeline requires >1 hour/week):** Automation is insufficient. Focus on reducing the human review bottleneck — improve auto-generated content templates, pre-approve low-risk spotlights, or batch-approve multiple spotlights at once.
- **Fail (trial <25% at 500+ users):** Scale is degrading quality. Diagnose: is it the outer segments (tighten targeting), content fatigue (refresh format), or feature selection (spotlight higher-value features)? Fix and re-run for 4 more weeks.

## Time Estimate

- 10 hours: A/B test setup and management across 3 rounds of experimentation
- 15 hours: Multi-segment targeting, content templates, and pipeline automation enhancements
- 10 hours: Health monitor dashboard, fatigue detection, and weekly report setup
- 25 hours: Eight weekly cycles of pipeline operation, experiment management, and monitoring (~3 hours/week)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, funnels, cohorts, dashboards | Growth from $0.00045/event — https://posthog.com/pricing |
| Intercom | In-app spotlight delivery, per-segment targeting | ~$150-300/mo at scale — https://www.intercom.com/pricing |
| Loops | Email spotlight delivery, segment-based sends | Starter $49/mo — https://loops.so/pricing |
| n8n | Pipeline automation, experiment scheduling | Free self-hosted; Cloud from $24/mo — https://n8n.io/pricing |
| Attio | Spotlight Calendar, experiment audit trail, segment tracking | From $0/mo (free tier) — https://attio.com/pricing |

**Play-specific cost:** ~$200-400/mo (Intercom at scale + Loops Starter + PostHog Growth tier)

## Drills Referenced

- `ab-test-orchestrator` — systematic testing of spotlight formats, timing, and personalization depth
- `spotlight-content-pipeline` — scaled weekly production with multi-segment targeting and auto-generated content
- `spotlight-series-health-monitor` — series-level dashboard, fatigue detection, and audience saturation tracking
