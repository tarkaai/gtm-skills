---
name: ai-content-generation-baseline
description: >
  AI Content Assistant — Baseline Run. Deploy always-on tracking, feature announcements, and
  activation flows to grow AI content adoption across all users and validate that sustained
  usage lifts engagement metrics.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=40% of active users generate AI content AND >=15pp engagement lift for AI users vs non-users"
kpis: ["AI content adoption rate (active users who generated at least once / total active users, trailing 14 days)", "Engagement lift (session frequency delta: AI users minus non-users)", "Acceptance rate (>=55% target)", "Repeat usage rate (users who generated 3+ times / users who generated at least once)"]
slug: "ai-content-generation"
install: "npx gtm-skills add product/retain/ai-content-generation"
drills:
  - posthog-gtm-events
  - feature-announcement
  - activation-optimization
---

# AI Content Assistant — Baseline Run

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Move from a small test cohort to all active users. Deploy always-on tracking, coordinated feature announcements across in-app and email channels, and activation flows that guide users to their first successful AI content generation. Validate that the engagement lift observed in Smoke holds at scale across the full user base and over a sustained period.

Pass threshold: >=40% of active users generate AI content at least once in a 14-day window, AND AI content users show >=15 percentage point higher weekly session frequency than non-users.

## Leading Indicators

- Feature announcement in-app message achieves >=20% click-through rate
- Feature announcement email achieves >=10% click-through rate
- First-generation funnel (announcement shown -> prompt submitted -> content generated -> content accepted) converts at >=15% end-to-end
- Repeat usage rate (3+ generations) reaches >=40% of adopters by day 14
- Acceptance rate holds at >=55% (no quality degradation from Smoke level)
- Regeneration rate stays below 35%

## Instructions

### 1. Deploy comprehensive event tracking

Run the `posthog-gtm-events` drill to extend the Smoke-level event taxonomy with always-on automation events:

Add these events:
```
ai_content_feature_announcement_shown     — user saw the in-app announcement
ai_content_feature_announcement_clicked   — user clicked through to the feature
ai_content_template_selected              — user selected a content template (if applicable)
ai_content_session_started                — user opened the AI content creation area
ai_content_session_completed              — user finished a generation session (accepted or exited)
```

Build PostHog funnels:
- **Discovery funnel**: `announcement_shown -> announcement_clicked -> session_started -> prompt_submitted -> generated -> accepted`
- **Quality funnel**: `generated -> accepted` vs `generated -> rejected` vs `generated -> regenerated`
- **Repeat funnel**: `first_generation -> second_generation (within 7 days) -> third_generation`

Set up cohort comparison: AI content users (at least 1 generation in trailing 14 days) vs non-users. Track weekly session frequency, feature breadth (distinct features used), and 30-day retention for each group.

### 2. Launch coordinated feature announcements

Run the `feature-announcement` drill to announce the AI content feature to all active users:

**In-app announcement (via Intercom):**
- Tier 1 announcement: banner at the top of the content creation area
- Copy: Lead with the benefit ("Create [content type] in seconds"), not the technology ("We added AI")
- CTA: "Try it now" linking directly to the AI content creation flow with a pre-selected content type
- Show once per user. Dismiss on click or explicit close. Do not re-show after dismissal.
- Segment: all active users who have not yet fired `ai_content_prompt_submitted`

**Email announcement (via Loops):**
- Send to all active users who have not used the AI content feature
- Subject line: test 2 variants using `loops-ab-testing` (benefit-focused vs curiosity-focused)
- Body: one paragraph on what it does, one example of output quality, one CTA linking to the feature
- Send on Tuesday or Wednesday between 10-11 AM in the user's timezone

### 3. Optimize the activation path

Run the `activation-optimization` drill to identify and fix the biggest drop-off in the discovery funnel:

1. After 3 days of announcements running, pull the discovery funnel from PostHog
2. Identify the step with the largest drop-off
3. For each common drop-off point, apply the fix:
   - **Announcement shown but not clicked**: The value proposition is unclear. Rewrite the copy to focus on a specific content type the user creates frequently. Use PostHog cohorts to personalize: if the user creates blog posts, show "Generate blog posts in seconds." If they create emails, show "Draft emails with AI assistance."
   - **Clicked but no prompt submitted**: The UI is confusing. Add a pre-filled example prompt so the user can generate immediately without thinking about what to write. Use `intercom-product-tours` to add a 2-step contextual guide.
   - **Prompt submitted but content rejected**: Output quality issue. Log the prompts that led to rejections (anonymized). Analyze patterns: are users asking for content types the AI handles poorly? Are prompts too vague? Feed findings back to the product team.
   - **Content accepted but no repeat usage**: The feature works but users forget it exists. Add a contextual reminder via `intercom-in-app-messages` when the user next creates content manually: "Want to try AI for this?"

4. Implement the fix for the top drop-off point. Let it run for 4 days. Re-measure the funnel.

### 4. Evaluate against threshold

At the end of 2 weeks, measure:

1. **Adoption rate**: Distinct active users who fired `ai_content_prompt_submitted` at least once in the trailing 14 days / total active users. Target: >=40%.
2. **Engagement lift**: Weekly session frequency for AI content users minus weekly session frequency for non-users. Target: >=15 percentage points.
3. **Acceptance rate**: Total `ai_content_accepted` + `ai_content_edited` / total `ai_content_generated`. Target: >=55%.
4. **Repeat usage**: Users with 3+ generations / users with 1+ generation. Track but no hard threshold at Baseline.

If PASS on adoption and engagement lift: proceed to Scalable. If FAIL on adoption but PASS on engagement lift: the feature works for those who find it but discovery needs more work. Double down on step 3. If FAIL on engagement lift: the feature is not driving retention. Investigate whether users generate content once and never return (novelty not utility).

## Time Estimate

- 3 hours: Extend event tracking and build funnels (step 1)
- 4 hours: Configure and launch feature announcements (step 2)
- 6 hours: Analyze funnels, diagnose drop-offs, implement fixes, re-measure (step 3)
- 3 hours: Final measurement and evaluation (step 4)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, cohorts, A/B testing | Free tier: 1M events/mo. https://posthog.com/pricing |
| Intercom | In-app announcements, product tours, contextual messages | Starter: ~$39/seat/mo. https://www.intercom.com/pricing |
| Loops | Email announcements, A/B subject line testing | Free tier: 1,000 contacts. https://loops.so/pricing |

## Drills Referenced

- `posthog-gtm-events` -- extends event taxonomy with announcement and session events, builds discovery/quality/repeat funnels
- `feature-announcement` -- coordinates in-app and email announcements to drive feature discovery
- `activation-optimization` -- diagnoses and fixes the largest drop-off in the activation funnel
