---
name: review-request-health-monitor
description: Play-specific monitoring for in-app review request campaigns — tracks ask-to-review funnels, optimal timing windows, sentiment drift, and platform-specific conversion with automated interventions
category: Advocacy
tools:
  - PostHog
  - Intercom
  - n8n
  - Attio
  - G2
  - Capterra
fundamentals:
  - posthog-custom-events
  - posthog-dashboards
  - posthog-cohorts
  - posthog-anomaly-detection
  - intercom-in-app-messages
  - directory-review-monitoring
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-contacts
  - attio-reporting
---

# Review Request Health Monitor

This drill builds the play-specific monitoring layer for in-app review request campaigns. It complements the generic `autonomous-optimization` loop by tracking the unique metrics and intervention patterns specific to asking happy users for G2/Capterra reviews at optimal product moments. The drill detects when review ask timing degrades, when platform-specific conversion diverges, when ask fatigue sets in, and when sentiment in submitted reviews shifts -- triggering automated corrections before the review pipeline stalls.

## Input

- In-app review request system running at Scalable level for at least 4 weeks (baseline data required)
- PostHog tracking configured with review-specific events (output from `posthog-gtm-events`)
- Intercom in-app messaging active for review prompts
- G2 and Capterra API credentials for review monitoring
- n8n instance for scheduling health checks
- Attio CRM with review candidate tracking

## Steps

### 1. Define review request health metrics

Using `posthog-custom-events`, ensure the following events are instrumented:

- `review_ask_shown`: In-app review prompt displayed. Properties: `trigger_type` (milestone/nps-promoter/support-resolved/usage-streak), `platform_target` (g2/capterra), `user_engagement_score`, `user_tenure_days`, `prompt_variant`.
- `review_ask_clicked`: User clicked the review link in the prompt. Properties: same as above plus `time_to_click_seconds`.
- `review_ask_dismissed`: User dismissed the prompt. Properties: same as above plus `dismiss_action` (close/snooze/never-ask).
- `review_ask_snoozed`: User chose "remind me later." Properties: same as above.
- `review_submitted`: New review detected on G2/Capterra via webhook. Properties: `platform`, `rating`, `word_count`, `reviewer_tenure_days`, `trigger_type_attributed`, `time_from_ask_to_review_hours`.
- `review_response_posted`: Vendor response posted to the review. Properties: `platform`, `review_rating`, `response_time_hours`.

### 2. Build the review request health dashboard

Using `posthog-dashboards`, create a "Review Request Health" dashboard:

**Panel 1 -- Ask-to-Review Funnel:**
- Funnel: `review_ask_shown` -> `review_ask_clicked` -> `review_submitted`
- Break down by `trigger_type`
- Display conversion rates at each step and median time between steps

**Panel 2 -- Timing Effectiveness:**
- Table: `trigger_type` vs. click-through rate, review completion rate, average review rating
- Sorted by review completion rate descending
- Goal: identify which product moments produce the highest quality reviews

**Panel 3 -- Platform Split:**
- Bar chart: reviews submitted per week, stacked by `platform_target` (G2 vs Capterra)
- Average rating trend per platform per week
- Total review count per platform (cumulative)

**Panel 4 -- Engagement Score Distribution of Reviewers:**
- Histogram: `user_engagement_score` of users who submitted reviews vs. all users who saw asks
- Goal: validate that high-engagement users convert to reviewers at higher rates

**Panel 5 -- Ask Fatigue Signals:**
- Trend: dismiss rate per week (`review_ask_dismissed` / `review_ask_shown`)
- Trend: "never ask again" rate per week (subset of dismissals)
- Trend: snooze rate per week
- Alert threshold: dismiss rate exceeds 60% or "never ask" rate exceeds 10%

**Panel 6 -- Review Quality:**
- Average rating of new reviews per week (7-day rolling)
- Average word count of new reviews per week
- Distribution: ratings 1-2 vs 3 vs 4-5

### 3. Configure daily health checks via n8n

Using `n8n-scheduling` and `n8n-workflow-basics`, create a workflow triggered daily at 08:00 UTC:

**Check 1 -- Ask funnel health:**
- Query PostHog for last 7 days: `review_ask_shown` count, `review_ask_clicked` count, `review_submitted` count
- Compute: show-to-click rate, click-to-submit rate, overall show-to-submit rate
- Compare each against 4-week rolling average
- Flag: any rate declined >15% from rolling average

**Check 2 -- Timing window health:**
- Query PostHog for last 7 days: click-through rate by `trigger_type`
- Compare each trigger type against its own 4-week baseline
- Flag: any trigger type's CTR dropped >20% (signals the timing moment is losing effectiveness)

**Check 3 -- Platform balance:**
- Query review counts submitted per platform in last 14 days
- Compare: is one platform receiving disproportionately fewer reviews?
- Flag: if G2-to-Capterra ratio shifted >30% from baseline (may need to rotate which platform is promoted)

**Check 4 -- Ask fatigue:**
- Query PostHog: dismiss rate and "never ask" rate for last 7 days
- Compare against 4-week rolling average
- Flag: dismiss rate >60%, "never ask" rate >10%, or either metric increased >25% from baseline

**Check 5 -- Review sentiment:**
- Fetch new reviews from G2 and Capterra APIs via `directory-review-monitoring`
- Compute: average rating of reviews submitted in last 14 days
- Flag: average rating dropped below 4.0 or below 4-week rolling average by 0.5+ stars

### 4. Implement automated interventions

Using `n8n-workflow-basics` and `intercom-in-app-messages`, configure these automated responses:

**Intervention: Stale timing trigger**
When a trigger type's CTR drops >20% for 2 consecutive weeks:
- Reduce that trigger's frequency by 50% (from every occurrence to every-other occurrence)
- Increase weight on the best-performing trigger type
- Log the rotation in Attio

**Intervention: Ask fatigue**
When dismiss rate exceeds 60% for 1 week:
- Extend the cooldown period between review asks from 30 days to 60 days per user
- Rotate the prompt copy to the next variant
- If "never ask" rate exceeds 10%, reduce the eligible user pool to engagement score >70 (from >60)

**Intervention: Platform imbalance**
When one platform receives <30% of total reviews for 2 weeks:
- Rotate the primary platform shown in the prompt
- For users who already reviewed on one platform, ask for the other
- Log the rotation

**Intervention: Negative review spike**
When a 1-2 star review is submitted:
- Immediately alert the CS team via Slack
- Pause review asks for that specific user
- Queue a vendor response draft using `directory-review-monitoring` response templates
- If 3+ negative reviews in 7 days, pause all review asks for 48 hours and escalate

**Intervention: Review drought**
When zero reviews submitted in 14 consecutive days:
- Check if asks are still being shown (prompt display may be broken)
- If asks are showing but not converting, rotate to a different trigger type
- If asks are not showing, check PostHog feature flag status and Intercom message status
- Escalate if automated checks cannot diagnose the issue

### 5. Build the weekly review request health report

Using `n8n-scheduling`, generate a weekly report (Monday 9am):

```
# Review Request Health Report -- Week of {date}

## Funnel Performance
- Asks shown: {count} ({change}% vs 4-week avg)
- Click-through rate: {ctr}% ({change}% vs baseline)
- Review completion rate: {comp}% ({change}% vs baseline)
- Reviews submitted: {count} ({change}% vs 4-week avg)

## Timing Effectiveness (ranked by completion rate)
1. {trigger_type}: {ctr}% CTR, {comp}% completion, {avg_rating} avg rating
2. {trigger_type}: ...
3. {trigger_type}: ...

## Platform Health
- G2: {count} new reviews, avg rating {rating}
- Capterra: {count} new reviews, avg rating {rating}
- Platform balance: {ratio} (target: 40-60%)

## Fatigue Signals
- Dismiss rate: {rate}% (threshold: 60%)
- "Never ask" rate: {rate}% (threshold: 10%)
- Snooze rate: {rate}%

## Interventions This Week
- {list of automated interventions triggered and their status}

## Optimization Signals for autonomous-optimization
- {data-driven signals for the optimization loop to act on}
```

Post to Slack and store in Attio.

### 6. Maintain review candidate pipeline in Attio

Using `attio-contacts` and `attio-reporting`, track review readiness per user:

- `engagement_score`: current score from `engagement-score-computation`
- `review_ask_eligible`: boolean (engagement score >60, tenure >30 days, no review yet, not in cooldown)
- `last_review_ask_date`: when last prompted
- `review_ask_count`: total times prompted
- `review_ask_outcome`: clicked / dismissed / snoozed / never-ask / submitted
- `reviewed_platform`: g2 / capterra / both / none
- `review_rating`: rating if submitted
- `review_cooldown_until`: date when eligible for next ask

Weekly pipeline health check:
- Count eligible users not yet asked
- Count users in cooldown
- Count users who said "never ask"
- Calculate weeks of pipeline remaining at current ask rate
- If pipeline depth <4 weeks, flag: need to wait for new users to reach eligibility or lower engagement threshold

## Output

- Real-time PostHog dashboard tracking the complete review request funnel
- Daily automated health checks catching degradation within 24 hours
- Automated interventions for fatigue, timing decay, platform imbalance, and negative reviews
- Weekly health reports with actionable optimization signals
- Review candidate pipeline health tracking in Attio

## Triggers

- Dashboard: always-on, refreshes with live PostHog data
- Daily health checks: 08:00 UTC via n8n cron
- Weekly report: Monday 09:00 UTC via n8n cron
- Negative review alert: immediate via G2/Capterra webhook -> n8n
- Pipeline health: weekly, appended to the health report
