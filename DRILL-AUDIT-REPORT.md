# Drill Audit Report

Generated: 2026-03-30

## Summary

| Category | Count | % of Total |
|----------|-------|------------|
| Total drills | 678 | 100% |
| Multi-use (2+ plays) | 404 | 60% |
| Single-use (1 play) | 264 | 39% |
| Orphaned (0 play refs) | 10 | 1% |

## 1. Orphaned Drills (10)

All 10 "orphaned" drills have 0 direct play frontmatter references but ARE actively
referenced by other drills (listed in their `fundamentals:` sections). They function
as building-block sub-drills. **Deleting them would break drill dependency chains.**

| Drill | Location | Referenced by N other drills |
|-------|----------|------------------------------|
| call-transcript-bant-extraction | discovery/ | 3 |
| call-transcript-competitor-extraction | discovery/ | 1 |
| call-transcript-meddic-extraction | discovery/ | 1 |
| call-transcript-need-extraction | discovery/ | 1 |
| call-transcript-objection-extraction | discovery/ | 6 |
| call-transcript-pain-extraction | discovery/ | 5 |
| call-transcript-risk-extraction | discovery/ | 4 |
| call-transcript-tech-requirements-extraction | discovery/ | 4 |
| call-transcript-timing-extraction | discovery/ | 3 |
| competitor-changelog-monitoring | research/ | 4 |

**Recommendation:** Do NOT delete. These are sub-drills used transitively. Consider
reclassifying them as fundamentals if that better matches the architecture (they behave
like fundamentals -- atomic, tool-specific operations -- but live in drills/).

## 2. Multi-Use Drills (404) -- Keep As-Is

Top 20 most reused drills:

| Drill | Play count |
|-------|-----------|
| threshold-engine | 320 |
| autonomous-optimization | 233 |
| posthog-gtm-events | 229 |
| ab-test-orchestrator | 199 |
| dashboard-builder | 71 |
| icp-definition | 59 |
| follow-up-automation | 44 |
| tool-sync-workflow | 36 |
| upgrade-prompt | 30 |
| activation-optimization | 28 |
| signal-detection | 28 |
| build-prospect-list | 27 |
| nps-feedback-loop | 26 |
| churn-prevention | 25 |
| content-repurposing | 23 |
| feature-adoption-monitor | 20 |
| cold-email-sequence | 20 |
| lead-capture-surface-setup | 19 |
| onboarding-flow | 17 |
| budget-allocation | 16 |

## 3. Single-Use Drill Analysis (264)

### 3a. `*-health-monitor` pattern: 37 drills

Every "durable" play level gets its own health monitor drill. These are nearly
identical in structure -- they watch KPIs specific to the play and alert on degradation.

**Merge recommendation:** Replace all 37 with ONE generic `play-health-monitor` drill
that accepts parameters (KPI list, thresholds, alert rules). The play's frontmatter
or instructions provide the play-specific config. Savings: **36 drills eliminated.**

Drills:
- activation-health-monitor (product/onboard/activation-milestone-tracking/durable.md)
- ai-coach-health-monitor (product/onboard/ai-onboarding-coach/durable.md)
- ai-content-usage-health-monitor (product/retain/ai-content-generation/durable.md)
- announcement-health-monitor (product/retain/feature-announcement-campaign/durable.md)
- at-risk-intervention-health-monitor (product/winback/at-risk-intervention/durable.md)
- certification-health-monitor (product/onboard/certification-program/durable.md)
- champion-program-health-monitor (product/referrals/community-champions/durable.md)
- commitment-health-monitor (product/upsell/multiyear-commitment/durable.md)
- comparison-page-health-monitor (marketing/solution-aware/comparison-alternative-pages/durable.md)
- cs-playbook-health-monitor (product/retain/customer-success-playbooks/durable.md)
- cta-experiment-health-monitor (product/retain/cta-testing/durable.md)
- deprecation-health-monitor (product/retain/feature-deprecation-management/durable.md)
- docs-content-health-monitor (marketing/solution-aware/documentation-as-marketing/durable.md)
- downgrade-intervention-health-monitor (product/retain/downgrade-prevention/durable.md)
- empty-state-health-monitor (product/onboard/empty-state-onboarding/durable.md)
- expansion-upsell-health-monitor (product/upsell/usage-limit-sales-upsell/durable.md)
- experiment-portfolio-health-monitor (product/retain/ab-testing-framework/durable.md)
- free-to-paid-funnel-health-monitor (product/upsell/free-to-paid-conversion-funnel/durable.md)
- in-app-message-health-monitor (product/retain/in-app-messaging-campaigns/durable.md)
- inactive-reengagement-health-monitor (product/winback/email-reengagement-inactive/durable.md)
- invite-health-monitor (product/upsell/invite-mechanism/durable.md)
- ndr-health-monitor (product/retain/net-retention-optimization/durable.md)
- nps-health-monitor (product/referrals/nps-program/durable.md)
- personalization-health-monitor (product/retain/ai-personalization/durable.md)
- plg-conversion-health-monitor (product/upsell/plg-sales-hybrid/durable.md)
- poc-health-monitoring (sales/aligned/poc-management-framework/scalable.md)
- proactive-outreach-health-monitor (product/retain/proactive-support-outreach/durable.md)
- public-share-health-monitor (product/referrals/public-sharing/durable.md)
- recommendation-health-monitor (product/retain/ai-recommendations/durable.md)
- review-request-health-monitor (product/referrals/in-app-review-request/durable.md)
- signup-funnel-health-monitor (product/onboard/self-serve-signup-optimization/durable.md)
- social-share-health-monitor (product/referrals/social-sharing-features/durable.md)
- testimonial-health-monitor (product/referrals/testimonial-collection/durable.md)
- ttv-health-monitor (product/onboard/time-to-value-optimization/durable.md)
- video-tutorial-health-monitor (product/onboard/video-tutorial-library/durable.md)
- winback-campaign-health-monitor (product/winback/winback-campaign/durable.md)
- workflow-optimization-health-monitor (product/retain/workflow-optimization-suggestions/durable.md)

### 3b. `*-monitor` pattern (non-health): 43 drills

Similar to health monitors but more domain-specific (performance monitors, intelligence
monitors, adoption monitors). Most follow the same structure: watch metrics, detect
anomalies, surface insights.

**Merge recommendation:** Group into 2-3 generic drills:
- `performance-monitor` (for marketing/campaign-level monitoring)
- `intelligence-monitor` (for sales/competitive intelligence)
- `adoption-monitor` (for product adoption tracking)
Savings: **~35 drills eliminated.**

Drills:
- ama-performance-monitoring, booking-conversion-monitor, breakup-reengagement-monitor
- budget-intelligence-monitor, business-case-effectiveness-monitor
- change-objection-intelligence-monitor, chrome-store-performance-monitor
- co-webinar-performance-monitor, collaboration-adoption-monitor
- competitive-intelligence-monitor, conference-booth-performance-monitor
- conference-performance-monitor, deal-negotiation-intelligence-monitor
- devrel-performance-monitor, display-ads-performance-monitor
- field-event-performance-monitor, gift-performance-monitor
- hallway-demo-performance-monitor, infographic-performance-monitor
- interactive-tool-performance-monitor, joint-content-performance-monitor
- marketplace-performance-monitor, newsletter-performance-monitor
- objection-intelligence-monitor, partner-marketplace-monitor
- piggyback-meetup-performance-monitor, referral-funnel-monitor
- report-performance-monitor, research-effectiveness-monitor
- retargeting-performance-monitor, roi-skepticism-intelligence-monitor
- sandbox-usage-monitoring, sdk-adoption-monitor, segment-drift-monitor
- sms-performance-monitor, so-authority-monitoring, summit-performance-monitor
- technical-intelligence-monitor, technical-objection-intelligence-monitor
- timing-intelligence-monitor, value-asset-performance-monitor
- viral-coefficient-monitor, workshop-performance-monitor

### 3c. `*-reporting` pattern: 17 drills

Play-specific reporting drills. All follow the same pattern: aggregate metrics,
format a report, deliver via dashboard or Slack.

**Merge recommendation:** Replace with ONE generic `play-performance-reporting` drill.
Savings: **16 drills eliminated.**

Drills:
- authority-verification-reporting, bundle-performance-reporting
- champion-outbound-reporting, champion-program-reporting
- crm-data-quality-reporting, discord-community-program-reporting
- display-performance-reporting, engagement-performance-reporting
- event-performance-reporting, experiment-impact-reporting
- field-performance-reporting, hackathon-optimization-reporting
- pain-intelligence-reporting, partner-performance-reporting
- poc-intelligence-reporting, sandbox-intelligence-reporting
- tla-performance-reporting

### 3d. `*-scoring` pattern: 8 drills

Play-specific scoring models. Each defines criteria and weights for a different domain
but the mechanism (weighted scorecard, threshold-based routing) is identical.

**Merge recommendation:** Replace with ONE generic `criteria-scoring` drill parameterized
by scoring criteria and weights. Savings: **7 drills eliminated.**

Drills:
- bant-auto-scoring, champion-identification-scoring, change-readiness-scoring
- expansion-scoring-pipeline, meddic-auto-scoring, need-auto-scoring
- timing-auto-scoring, trial-activation-scoring

### 3e. `*-pipeline` pattern: 15 drills

Content/process pipeline drills. Each defines a production pipeline for a specific
domain (content type, lifecycle stage, etc.).

**Merge recommendation:** Review case-by-case. Some are truly unique (crm-pipeline-setup)
while others are variants of "content scaling pipeline" or "nurture pipeline."
Estimate **~10 drills** could be merged into 2-3 generic pipeline drills.

### 3f. `*-automation` pattern: 19 drills

Process automation drills. Varied enough that wholesale merging is harder, but
clusters exist:
- Event series automation (field-event, hackathon, summit, workshop) -> 1 generic `event-series-automation`
- Fulfillment/delivery automation (certification, best-practices, referral) -> partially mergeable
Estimate **~8 drills** could be merged.

### 3g. Truly unique single-use: 118 drills

These don't follow a mergeable pattern. For each, the question is:
should it be a drill (reusable capability) or absorbed into the play?

Quick heuristic: if the drill is used by only one play AND the play level is
`smoke` (the simplest level), the drill likely describes the core manual
procedure and is a good candidate for absorption into the play instructions.

## 4. Reduction Estimate

| Action | Drills eliminated | New drills created |
|--------|-------------------|--------------------|
| Merge health-monitors into 1 | -36 | +1 |
| Merge monitors into 3 | -40 | +3 |
| Merge reporting into 1 | -16 | +1 |
| Merge scoring into 1 | -7 | +1 |
| Merge pipelines | -10 | +3 |
| Merge automations | -8 | +2 |
| Absorb unique smoke-level drills | ~-30 | 0 |
| **Total** | **~-147** | **+11** |

**Estimated drill count after cleanup: 678 - 147 + 11 = ~542**

To reach the 200-300 target, the 118 "truly unique" drills need a second pass
to determine which can be absorbed into play instructions. That requires
reading each drill and its single consuming play to decide.

## 5. Next Steps

1. Create generic parameterized drills: `play-health-monitor`, `play-performance-reporting`,
   `criteria-scoring`, `performance-monitor`, `intelligence-monitor`, `adoption-monitor`
2. Update all consuming plays to reference the generic drills with play-specific config
3. Delete the 97+ merged drills
4. Second pass: review 118 unique drills for absorption into play instructions
5. Reclassify the 10 "orphaned" sub-drills (move to fundamentals or add to play frontmatter)
