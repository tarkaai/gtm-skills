---
name: case-study-candidate-pipeline
description: Automated pipeline that identifies high-fit case study candidates from product usage data, scores them, and runs personalized outreach sequences
category: Advocacy
tools:
  - PostHog
  - Attio
  - n8n
  - Loops
  - Intercom
  - Cal.com
fundamentals:
  - posthog-cohorts
  - posthog-custom-events
  - posthog-retention-analysis
  - attio-lists
  - attio-contacts
  - attio-custom-attributes
  - attio-notes
  - n8n-scheduling
  - n8n-triggers
  - n8n-workflow-basics
  - loops-sequences
  - loops-transactional
  - intercom-in-app-messages
  - calcom-booking-links
---

# Case Study Candidate Pipeline

This drill builds an always-on pipeline that surfaces customers most likely to say yes to a case study, scores them on storytelling potential, and runs a multi-touch recruitment sequence. The output is a steady stream of qualified, willing case study participants without manual prospecting.

## Prerequisites

- PostHog tracking core product events for at least 60 days (need retention data)
- Attio configured with contact and company records
- n8n instance for automation workflows
- Loops configured for email sequences
- Intercom configured for in-app messages
- Cal.com with a "Case Study Interview" event type created

## Steps

### 1. Define case study candidate scoring

Build a composite score from four dimensions. Each dimension is scored 0-100, then weighted into a final `case_study_fit_score`:

**Results strength (weight: 35%)**
Using `posthog-retention-analysis`, identify accounts with the strongest measurable outcomes:
- Retention rate vs. cohort average (how much better than typical?)
- Feature adoption breadth (using 70%+ of available features signals deep value)
- Usage volume growth over the last 90 days
- Time-to-value: how fast they activated relative to median

Score formula: `(retention_vs_avg * 0.3) + (feature_breadth_ratio * 0.3) + min(usage_growth_90d / 0.5, 1) * 0.2 + (1 - (ttv_days / median_ttv_days)) * 0.2`

**Story potential (weight: 25%)**
Using `attio-contacts` and `attio-custom-attributes`, evaluate:
- Company size (mid-market and enterprise tell better stories for sales enablement; SMB tells better stories for product-led)
- Industry relevance (does their industry match your top ICPs?)
- Recognizable brand (would prospects know their name?)
- Role seniority of primary contact (VP+ quotes carry more weight)

Score formula: `industry_match * 0.3 + brand_recognition * 0.3 + role_seniority_score * 0.2 + size_fit_score * 0.2`

**Relationship health (weight: 25%)**
Using `posthog-custom-events` and Attio data:
- NPS score (if available; 9-10 = strong candidate)
- Support ticket sentiment (low volume + positive resolution = healthy)
- Engagement with product emails (high open/click rates)
- Days since last negative interaction (recent complaints disqualify)

Score formula: `nps_normalized * 0.4 + support_health * 0.2 + email_engagement * 0.2 + (days_since_negative > 90 ? 1 : 0) * 0.2`

**Timing signal (weight: 15%)**
Using `posthog-custom-events`:
- Recently hit a milestone (crossed a usage threshold, completed onboarding of a new team, renewed or expanded)
- Not currently in a sales cycle for upsell (avoid asking for favors during negotiation)
- Account age between 90 days and 2 years (too new = thin story; too old = stale story)

Score formula: `recent_milestone * 0.4 + (not_in_sales_cycle ? 1 : 0) * 0.3 + age_window_fit * 0.3`

**Composite**: `results * 0.35 + story * 0.25 + relationship * 0.25 + timing * 0.15`

### 2. Implement the scoring pipeline

Using `n8n-scheduling`, create a weekly workflow:

1. Pull all active accounts from PostHog with 60+ days of data
2. Compute each scoring dimension using PostHog queries and Attio lookups
3. Calculate composite `case_study_fit_score`
4. Using `attio-custom-attributes`, write the score and dimension breakdown to each contact
5. Using `posthog-custom-events`, fire `case_study_fit_scored` with score and dimensions:

```javascript
posthog.capture('case_study_fit_scored', {
  composite_score: 82,
  results_strength: 90,
  story_potential: 78,
  relationship_health: 85,
  timing_signal: 65,
  top_result_metric: 'retention_rate_2x_cohort_avg',
  disqualified: false,
  disqualify_reason: null
});
```

### 3. Build the candidate list

Using `attio-lists`, create a "Case Study Candidates" list with filters:
- `case_study_fit_score >= 70`
- Not already a published case study
- Not declined in the last 6 months
- Not currently in the recruitment sequence

Rank by composite score descending. Limit the active recruitment pipeline to 10 candidates at a time to maintain quality of outreach.

### 4. Build the recruitment outreach sequence

Using `loops-sequences`, create a 4-touch recruitment sequence triggered when a candidate enters the pipeline:

**Email 1 (Day 0): The ask**
Subject: personalized with their top result metric (e.g., "Your 2x retention rate is worth sharing")
Body: acknowledge their specific success, explain what a case study involves (30-min interview, they review the draft, published on your site with their approval), state the benefits to them (exposure, backlink, positioned as industry leader). Include a Cal.com booking link using `calcom-booking-links` for a "Case Study Interview" event type.

**Email 2 (Day 4): Social proof**
Subject: "How [Similar Company] told their story"
Body: link to an existing case study from a similar company or industry. Show them what the output looks like. Reiterate the low time commitment. Include the booking link again.

**Email 3 (Day 9): In-app nudge**
Using `intercom-in-app-messages`, show a targeted in-app message to candidates who opened Email 1 or 2 but did not book: "We'd love to feature your team's success. It's a 30-minute conversation." CTA links to the booking page.

**Email 4 (Day 14): Final follow-up**
Subject: "Last check — still interested?"
Body: brief, low-pressure. Offer alternatives: written Q&A instead of live interview, async video response, or just a quote they approve. Include all options with links.

**After Day 21 with no response**: mark as "Declined (no response)" in Attio. Do not re-contact for 6 months.

### 5. Handle responses

Using `n8n-triggers`, listen for:

- **Booking confirmed** (Cal.com webhook): update Attio status to "Interview Scheduled", add interview date, assign to the person who will conduct the interview. Fire `case_study_interview_scheduled` in PostHog.
- **Declined** (Loops reply detection or manual): update Attio status to "Declined", set `case_study_declined_date`, add the reason if provided. Fire `case_study_declined` in PostHog. Set a 6-month cooldown.
- **Alternative accepted** (written Q&A or async video): update Attio status to "Alternative Format", trigger the appropriate follow-up workflow.

### 6. Track pipeline metrics

Using `posthog-custom-events`, instrument the full funnel:
- `case_study_candidate_scored` (weekly, all accounts)
- `case_study_candidate_entered_pipeline` (when added to active list)
- `case_study_outreach_sent` (each touch, with touch_number property)
- `case_study_outreach_opened` (email opens)
- `case_study_outreach_clicked` (CTA clicks)
- `case_study_interview_scheduled` (booking confirmed)
- `case_study_declined` (explicit or timeout)
- `case_study_completed` (final asset published)

## Output

- Weekly scoring pipeline computing case study fit for all active accounts
- Ranked candidate list in Attio with composite scores
- 4-touch automated recruitment sequence (3 email + 1 in-app)
- Response handling automation for bookings, declines, and alternatives
- Full funnel instrumentation in PostHog

## Triggers

Scoring runs weekly via n8n cron. Outreach triggers when a candidate enters the pipeline. Response handling is event-driven. All workflows are always-on after initial setup.
