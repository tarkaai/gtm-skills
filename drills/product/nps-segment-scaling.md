---
name: nps-segment-scaling
description: Scale NPS surveys across multiple user segments with differentiated timing, channels, and follow-up strategies
category: Product
tools:
  - PostHog
  - n8n
  - Intercom
  - Loops
  - Attio
fundamentals:
  - posthog-cohorts
  - posthog-feature-flags
  - posthog-custom-events
  - posthog-experiments
  - n8n-scheduling
  - n8n-workflow-basics
  - intercom-in-app-messages
  - loops-sequences
  - attio-lists
---

# NPS Segment Scaling

This drill scales the NPS program from a single-cohort survey into a multi-segment operation where different user groups receive surveys at different times, through different channels, with different follow-up strategies. The goal is maximum coverage and response rate without survey fatigue.

## Prerequisites

- NPS baseline running for at least 4 weeks with response routing active
- PostHog with user segments defined
- n8n instance for survey scheduling
- Intercom and Loops configured
- At least 200 active users across segments

## Steps

### 1. Define survey segments

Using `posthog-cohorts`, create distinct cohorts for differentiated NPS treatment:

| Segment | Criteria | Survey Timing | Channel |
|---------|----------|---------------|---------|
| New users | 30-60 days since signup, activated | 45 days post-signup | In-app (Intercom) |
| Established users | 60-180 days, active last 14 days | Quarterly | Email (Loops) |
| Power users | Top 20% usage, 90+ days | Quarterly, offset 6 weeks from established | In-app (Intercom) |
| Churning users | Usage declined 50%+ in last 30 days | Triggered on decline detection | Email (Loops) |
| Post-support users | Closed support ticket in last 7 days | 3 days after ticket close | Email (Loops) |
| Expansion users | Upgraded plan in last 30 days | 21 days post-upgrade | In-app (Intercom) |

Rules:
- Never survey a user more than once per 90 days
- Never survey during onboarding (first 14 days)
- Never survey within 7 days of a support interaction starting
- If a user qualifies for multiple segments, use priority: churning > post-support > new > expansion > established > power

### 2. Build the survey scheduling engine

Using `n8n-scheduling`, create a master workflow that runs daily:

1. For each segment, query PostHog for users who qualify AND have not been surveyed in 90+ days
2. Check the daily survey cap: never send more than 5% of your active user base per day (prevents response data from being skewed by a single day's cohort)
3. Queue surveys in priority order. If the cap is reached, defer lower-priority segments to the next day
4. For in-app surveys: use `intercom-in-app-messages` to schedule the survey message for the next user session
5. For email surveys: use `loops-sequences` to send the survey email at the user's optimal send time (based on historical email open data from Loops)
6. Log every survey sent as a PostHog event using `posthog-custom-events`: `nps_survey_sent` with properties: segment, channel, user_id

### 3. A/B test survey parameters per segment

Using `posthog-experiments`, run experiments on survey variables by segment:

**Timing experiments:**
- New users: test 30 vs 45 vs 60 days post-signup
- Established users: test quarterly vs biannual cadence
- Post-support: test 3 vs 7 days after ticket close

**Channel experiments:**
- Test in-app survey vs email survey for established users (use `posthog-feature-flags` to split)
- Test interstitial modal vs slide-in panel vs embedded widget for in-app surveys
- Test plain-text email vs branded HTML email for email surveys

**Copy experiments:**
- Test "How likely are you to recommend us?" vs "How satisfied are you with [Product]?"
- Test mandatory vs optional open-text field
- Test with vs without explanation of how feedback is used

Each experiment runs until statistical significance (minimum 200 responses per variant). Log experiment results in Attio using `attio-lists`.

### 4. Build segment-specific follow-up strategies

Each segment gets customized follow-up through the `nps-response-routing` drill, but at scale add these segment-specific enhancements:

**New user detractors:** Route to onboarding team, not general support. Their issues are likely activation problems. Trigger an onboarding recovery sequence.

**Power user promoters:** Fast-track to advocacy pipeline. Their testimonials carry the most weight. Offer exclusive beta access as a thank-you.

**Churning user feedback:** Regardless of score, every response from this segment gets a personal follow-up within 24 hours. Their feedback is the most actionable for retention.

**Post-support respondents:** Cross-reference NPS score with CSAT from the ticket. If NPS is low but CSAT was high, the product (not support) is the problem. If both are low, escalate the support quality issue.

### 5. Build the coverage dashboard

Using `posthog-custom-events`, create a dashboard tracking:

- **Survey coverage**: % of each segment surveyed in the current quarter
- **Response rate by segment**: track which segments respond at highest rates
- **Response rate by channel**: compare in-app vs email across segments
- **NPS by segment**: separate NPS scores for each segment, trended monthly
- **Survey fatigue indicator**: declining response rates for users surveyed multiple times
- **Experiment status**: active experiments, sample sizes, time remaining

Target: 60%+ of each segment surveyed per quarter with 40%+ response rate.

### 6. Implement anti-fatigue guardrails

Using `n8n-workflow-basics`, enforce these rules in the scheduling engine:

- If a user's response rate drops (responded to first survey but not second), extend their cool-off period to 120 days
- If segment-level response rate drops below 30%, pause that segment's surveys and investigate (wrong timing, wrong channel, or survey fatigue)
- If a user submits a detractor score twice in a row, do NOT survey them again until their issue is resolved. Instead, flag in Attio for manual outreach.
- Track overall survey volume: if more than 15% of active users have been surveyed in a 30-day window, throttle all segments

## Output

- Multi-segment survey scheduling engine with daily priority queue
- Per-segment survey timing, channel, and copy optimization
- A/B testing framework for survey parameters
- Segment-specific follow-up strategy enhancements
- Coverage dashboard with fatigue monitoring
- Anti-fatigue guardrails preventing over-surveying

## Triggers

Master scheduling workflow runs daily via n8n cron. A/B test evaluation runs weekly. Coverage dashboard updates daily. Anti-fatigue checks run with every survey batch.
