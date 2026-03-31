---
name: video-tutorial-library-scalable
description: >
  Video Tutorial Library — Scalable. Personalize tutorial delivery by persona,
  A/B test video variants, and scale to 500+ users/month while maintaining >=35%
  play rate and activation lift across all segments.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Email, Content"
level: "Scalable"
time: "60 hours over 2 months"
outcome: ">=35% play rate at 500+ users/month AND activation lift >=6pp across all persona segments"
kpis: ["Video play rate by persona", "Video completion rate by persona", "Post-video activation rate by persona", "Activation lift vs non-exposed by persona", "Tutorial recommendation click-through rate", "Time to activation for tutorial watchers vs non-watchers"]
slug: "video-tutorial-library"
install: "npx gtm-skills add product/onboard/video-tutorial-library"
drills:
  - video-tutorial-personalization
  - ab-test-orchestrator
  - onboarding-persona-scaling
---

# Video Tutorial Library — Scalable

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Content

## Outcomes

Play rate holds at 35%+ across 500+ users per month. Every identified persona segment shows at least 6 percentage point activation lift from tutorials. Personalized tutorial recommendations outperform generic library presentation. The system runs without manual intervention except for recording new videos.

## Leading Indicators

- Persona detection accurately classifies 90%+ of new signups
- Personalized tutorial recommendations have higher click-through than generic suggestions
- Completion rates hold above 55% as user volume scales (no content fatigue signal)
- At least 2 A/B tests completed per month with statistically significant results
- Per-persona activation funnels show improving trends
- New tutorial requests from the recommendation engine are fulfilled within 1 week

## Instructions

### 1. Build persona-based tutorial routing

Run the `video-tutorial-personalization` drill to:

1. Map each tutorial to specific personas and onboarding stages (the routing matrix)
2. Set up PostHog feature flags for persona detection (Admin, End User, Data Analyst, or your product's specific personas)
3. Create PostHog cohorts for stage detection (first session, setup complete, first value, regular use)
4. Configure Intercom in-app messages for each persona-stage combination
5. Build Loops email sequences branched by persona with the right tutorial in each email
6. Deploy the n8n daily recommendation engine that identifies users who should see their next tutorial

**Human action required:** Define your product's personas if not already defined. Provide the mapping of which tutorials apply to which persona at which stage. The agent configures the routing but needs the persona definitions as input.

### 2. Expand the library for persona coverage

Audit tutorial coverage per persona. For each persona:
- Count how many tutorials exist for each onboarding stage
- Identify gaps where a persona has no tutorial for a high-friction step

Record new tutorials to fill gaps. Target: at least 3 tutorials per persona per stage. Use the `video-content-pipeline` drill for each new recording.

Total library should reach 25-35 tutorials covering all persona-stage combinations.

### 3. Run systematic A/B tests on video variables

Run the `ab-test-orchestrator` drill to test:

**Test 1: Video length** (Week 1-2)
- Control: current tutorial length (2-3 minutes)
- Variant: ultra-short tutorials (60-90 seconds covering only the critical action)
- Metric: completion rate AND post-video activation rate
- Hypothesis: shorter videos will have higher completion but the same activation rate because the core instruction is retained

**Test 2: Video surface** (Week 3-4)
- Control: Loom GIF thumbnail in email
- Variant: Inline video player in email (HTML5 video with fallback to GIF)
- Metric: play rate from email
- Hypothesis: inline players increase play rate by 5pp because they reduce friction

**Test 3: Tutorial trigger timing** (Week 5-6)
- Control: show tutorial immediately when user reaches the relevant step
- Variant: show tutorial only after user has been on the step for 30+ seconds (indicating confusion)
- Metric: play rate AND user satisfaction (from NPS)
- Hypothesis: delayed triggering targets confused users and improves relevance, increasing play rate

**Test 4: Post-video CTA** (Week 7-8)
- Control: generic "Try it now" button after video
- Variant: deep link that pre-fills the first field or opens the exact screen shown in the tutorial
- Metric: post-video activation rate
- Hypothesis: reducing clicks between tutorial and action increases activation by 10pp

Implement winners from each test before starting the next test. Document all results.

### 4. Scale persona routing to 500+ users/month

Run the `onboarding-persona-scaling` drill to ensure the persona detection and tutorial routing works at volume:

1. Monitor persona classification accuracy weekly (sample 20 users, manually verify their assigned persona matches their actual role)
2. Check that Intercom message frequency limits prevent tutorial fatigue (max 1 video recommendation per session)
3. Verify Loops email sequences are branching correctly by persona (check delivery reports for each branch)
4. Monitor n8n workflow execution volume -- ensure the daily recommendation engine handles the user count without timeouts

### 5. Monitor per-persona performance

Build a PostHog dashboard with per-persona breakdowns:

| Panel | Purpose |
|-------|---------|
| Play rate by persona (weekly) | Detect if any persona is underserved |
| Completion rate by persona (weekly) | Detect content quality issues per segment |
| Activation lift by persona (vs control or vs pre-tutorial baseline) | Prove value per segment |
| Recommendation click-through by source (Intercom vs Loops vs n8n) | Optimize delivery channel mix |
| Time to activation: tutorial watchers vs non-watchers by persona | Quantify speed improvement |

### 6. Evaluate against threshold

After 2 months with 500+ users:

**Primary threshold:** >=35% play rate across all persona segments (no segment below 25%)

**Secondary threshold:** >=6pp activation lift in every persona segment (not just overall)

If PASS: proceed to Durable. Document per-persona performance, A/B test results, and the final routing matrix.
If FAIL on specific personas: that persona's tutorials need rework. Check completion rate first -- if low, the content does not match the persona's needs or technical level. Rewrite and re-test for that segment only.
If FAIL at scale (rate held at low volume but dropped at high volume): check for system issues -- recommendation engine timeouts, Intercom message frequency caps, or email deliverability degradation.

## Time Estimate

- 12 hours: set up persona detection, routing matrix, Intercom messages, Loops branches
- 15 hours: record 10-20 new tutorials to fill persona gaps
- 16 hours: run 4 A/B tests (4 hours each: setup, monitoring, analysis)
- 8 hours: build per-persona dashboard and monitoring
- 5 hours: scale testing, troubleshooting, documentation
- 4 hours: final evaluation and Durable preparation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loom | Host 25-35 tutorial videos, API for analytics | Business: $12.50/user/mo. [loom.com/pricing](https://www.atlassian.com/software/loom/pricing) |
| Descript | Edit and caption all new tutorials | Creator: $24/mo. [descript.com/pricing](https://www.descript.com/pricing) |
| PostHog | Feature flags, experiments, per-persona funnels | Free tier (1M events). May approach paid tier at 500+ users with high event volume. [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Daily recommendation engine, Loom sync, test orchestration | Pro: ~$60/mo (10,000 executions). [n8n.io/pricing](https://n8n.io/pricing/) |
| Loops | Persona-branched onboarding email sequences | $49/mo+. [loops.so/pricing](https://loops.so/pricing) |
| Intercom | Per-persona in-app tutorial recommendations | Essential: $29/seat/mo (annual). [intercom.com/pricing](https://www.intercom.com/pricing) |

**Estimated cost at Scalable level:** $120-200/mo (Loom Business + Descript + n8n Pro; PostHog likely still free tier; Loops and Intercom assumed in stack)

## Drills Referenced

- `video-tutorial-personalization` -- build persona detection, routing matrix, and multi-channel tutorial delivery
- `ab-test-orchestrator` -- design, run, and analyze 4 systematic A/B tests on video variables
- `onboarding-persona-scaling` -- ensure persona routing works reliably at 500+ users/month
