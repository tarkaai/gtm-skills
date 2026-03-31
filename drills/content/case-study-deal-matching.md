---
name: case-study-deal-matching
description: Automated engine that matches published case studies to active deals by industry, use case, and company profile, then routes relevant assets to deal owners
category: Content
tools:
  - Attio
  - n8n
  - PostHog
  - Loops
fundamentals:
  - attio-deals
  - attio-contacts
  - attio-lists
  - attio-notes
  - attio-custom-attributes
  - n8n-scheduling
  - n8n-triggers
  - n8n-workflow-basics
  - posthog-custom-events
  - loops-transactional
---

# Case Study Deal Matching

This drill builds an always-on engine that automatically matches published case studies to active deals and routes the most relevant social proof to each deal owner at the right moment. The goal is to ensure every prospect sees a case study from a company that looks like them before they make a buying decision.

## Prerequisites

- At least 5 published case studies with metadata in Attio (industry, use case, company size, primary metric)
- Attio deal pipeline with active deals that have company and industry data
- n8n instance for scheduling and event-driven workflows
- PostHog tracking case study views and deal stage changes
- Loops configured for transactional emails

## Steps

### 1. Build the case study metadata index

Using `attio-lists`, create a "Published Case Studies" list in Attio. For each case study, store these attributes using `attio-custom-attributes`:

- `case_study_id`: unique identifier
- `company_name`: the customer featured
- `industry`: their industry (e.g., "SaaS", "Healthcare", "Fintech")
- `company_size`: employee range (e.g., "10-50", "51-200", "201-1000", "1000+")
- `use_case`: the primary use case the case study demonstrates
- `primary_metric`: the headline result (e.g., "2x retention rate", "40% faster onboarding")
- `metric_category`: what type of result (e.g., "retention", "revenue", "efficiency", "growth")
- `publish_date`: when it was published
- `assets`: which derivative assets exist (full_story, one_pager, email_snippet, pull_quotes)
- `deal_influence_count`: how many deals this case study has been routed to (updated by the engine)
- `deal_win_count`: how many influenced deals closed won (updated retroactively)

### 2. Define the matching algorithm

For each active deal, compute a `case_study_match_score` against each published case study. Score 0-100 using these dimensions:

**Industry match (weight: 40%)**
- Exact industry match: 100
- Adjacent industry (e.g., prospect is "Fintech", case study is "SaaS"): 50
- No industry match: 0

**Company size match (weight: 25%)**
- Same size bracket: 100
- Adjacent bracket (one step up or down): 60
- Two or more brackets away: 0

**Use case match (weight: 25%)**
- Exact use case match: 100
- Related use case (same product area, different workflow): 50
- No use case match: 0

**Metric relevance (weight: 10%)**
- The case study's metric category matches the prospect's stated pain point or evaluation criteria: 100
- No clear match: 0

Composite: `(industry * 0.4) + (size * 0.25) + (use_case * 0.25) + (metric * 0.1)`

Threshold: only route case studies with composite score >= 50.

### 3. Build the new-deal matching workflow

Using `n8n-triggers`, create a workflow triggered by the `deal_created` event in PostHog or a new deal webhook from Attio:

1. Read the new deal's company data from Attio using `attio-deals`: industry, company size, use case interest, stated pain points
2. Run the matching algorithm against all published case studies
3. Select the top 2-3 matches (highest composite scores above threshold)
4. For each matched case study:
   - Using `attio-notes`, attach a note to the deal: "Matched case study: [Company] ([Industry], [Size]) achieved [Primary Metric]. Assets: [list]. Match score: [score]."
   - Increment the case study's `deal_influence_count`
5. Notify the deal owner via Loops using `loops-transactional`:
   - Subject: "Social proof for [Deal Company]: [Case Study Company] achieved [metric]"
   - Body: 2-3 sentence summary of the case study, link to the full story, one-page PDF attached, and the email snippet they can forward to the prospect
6. Fire `case_study_routed_to_deal` in PostHog using `posthog-custom-events`:

```javascript
posthog.capture('case_study_routed_to_deal', {
  deal_id: 'deal_abc123',
  case_study_id: 'cs_xyz789',
  match_score: 82,
  match_dimensions: { industry: 100, size: 60, use_case: 100, metric: 0 },
  deal_stage: 'discovery',
  assets_routed: ['email_snippet', 'one_pager', 'full_story']
});
```

### 4. Build the deal-stage-triggered routing

Using `n8n-triggers`, create a workflow that fires when a deal moves to a new stage in Attio:

**Discovery -> Evaluation stage:** Route the top case study match with the email snippet and one-pager. This is the "credibility" moment -- the prospect is deciding whether to evaluate seriously.

**Evaluation -> Decision stage:** Route a second case study (different from the one sent at Discovery) with the full story and pull quotes. This is the "validation" moment -- the prospect wants proof from someone like them.

**Decision -> Negotiation stage (if applicable):** Route the case study with the strongest ROI/metric result, regardless of industry match. This is the "justify the budget" moment.

For each routing event, fire `case_study_stage_routed` in PostHog with the deal stage and case study details.

### 5. Build the weekly gap analysis

Using `n8n-scheduling`, create a weekly workflow that runs every Monday:

1. Pull all active deals from Attio
2. For each deal, check: does it have at least one matched case study with score >= 50?
3. Deals with no match are "coverage gaps"
4. Group gaps by industry and use case
5. Generate a gap report: "X active deals have no relevant case study. Top gaps: [Industry A] (Y deals), [Use Case B] (Z deals)."
6. Store the gap report in Attio as a note on the case study program record
7. Fire `case_study_coverage_gap_report` in PostHog with the gap counts

This gap report feeds back into the `case-study-candidate-pipeline` drill -- prioritize recruiting case study candidates from gap industries and use cases.

### 6. Track routing effectiveness

Using `posthog-custom-events`, instrument the full routing-to-influence funnel:

- `case_study_routed_to_deal` — case study matched and sent to deal owner
- `case_study_forwarded_to_prospect` — deal owner forwarded the case study to the prospect (tracked via email open/click from the forwarded link)
- `case_study_prospect_viewed` — prospect viewed the case study page (tracked via UTM parameters: `utm_source=deal_routing&utm_campaign={deal_id}`)
- `case_study_influenced_deal_won` — deal closed won after case study was routed (attributed within the deal lifecycle)

Build a PostHog funnel: routed -> forwarded -> viewed -> deal_won. This measures the actual influence of case study routing on deal outcomes and allows scoring of which case studies are most effective at driving wins.

## Output

- Case study metadata index in Attio with matching attributes
- New-deal matching workflow that auto-routes top 2-3 case studies to each deal owner
- Stage-triggered routing that delivers the right case study at the right sales moment
- Weekly coverage gap analysis that feeds back to the candidate pipeline
- Full routing-to-influence funnel tracking in PostHog

## Triggers

New-deal matching fires on `deal_created`. Stage routing fires on deal stage changes. Gap analysis runs weekly via n8n cron. All workflows are always-on after initial setup.
