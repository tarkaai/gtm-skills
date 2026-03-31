---
name: demo-storytelling-framework-baseline
description: >
  Demo Storytelling Framework — Baseline Run. First always-on automation for story-driven demos.
  When a demo is scheduled, the agent auto-selects the best customer story from the library, generates
  a personalized narrative demo prep document, and tracks engagement signals post-demo. Story matching
  and narrative generation run without manual intervention.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Product"
level: "Baseline Run"
time: "18 hours over 2 weeks"
outcome: ">=80% of demos use story-driven prep, demo-to-proposal conversion improves >=15% vs pre-storytelling baseline over 2 weeks"
kpis: ["Storytelling adoption rate", "Demo-to-proposal conversion lift", "Story match score average", "Prospect story connection rate", "Engagement score average"]
slug: "demo-storytelling-framework"
install: "npx gtm-skills add sales/connected/demo-storytelling-framework"
drills:
  - posthog-gtm-events
---

# Demo Storytelling Framework — Baseline Run

> **Stage:** Sales → Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Product

## Outcomes

First always-on automation. When a demo is scheduled, the agent automatically selects the highest-resonance customer story from the library, generates a complete story-driven demo preparation document with narration scripts and feature-to-story mapping, and tracks engagement outcomes post-demo. The founder delivers the demo using the prep doc and logs the outcome. Story matching and narrative generation happen without manual intervention.

**Pass threshold:** >=80% of demos use story-driven prep, and demo-to-proposal conversion improves >=15% vs pre-storytelling baseline over 2 weeks.

## Leading Indicators

- Story-matched demo prep auto-generates within 2 hours of demo scheduling
- Average story match score >=60 (stories are well-matched to prospects)
- Prospects relate to the customer story in >=60% of demos (story connection moment logged)
- Questions about the customer story average >=2 per demo
- Demo-to-next-step commitment rate improves vs Smoke level

## Instructions

### 1. Configure Event Tracking

Run the `posthog-gtm-events` drill to set up PostHog events for the storytelling program:

| Event | Trigger |
|-------|---------|
| `story_match_scored` | Story selected for a demo |
| `story_narrative_generated` | Narrative demo prep created |
| `story_demo_prep_generated` | Full prep doc assembled and stored in Attio |
| `story_demo_completed` | Demo delivered, outcome logged |

Connect PostHog events to Attio via n8n webhook so deal records update with story usage data automatically.

Also capture the pre-storytelling baseline: query Attio for demo-to-proposal conversion rate from the 4 weeks before the Smoke test. Store this as the comparison benchmark.

### 2. Expand the Story Library

Before launching automation, ensure the library is ready for broader use:

- Review the story library from Smoke. Add any new stories from customers who recently achieved results.
- Target: >=5 approved stories covering your top 3 ICP segments by deal volume.
- For each story, verify: quantified primary result, at least 1 direct quote, and accurate metadata tags.
- Run `story-matching-scoring` against the last 10 deals to check coverage. If any deal's top match score is below 50, that segment has a story gap — prioritize filling it.

### 3. Deploy Automated Story-Matched Demo Prep

Run the the story matched demo prep workflow (see instructions below) drill and configure it to auto-trigger:

- Create an Attio automation: when a deal stage changes to "Demo Scheduled" (or when a Cal.com booking fires), send a webhook to n8n.
- n8n workflow: receive webhook -> pull deal context from Attio -> pull discovery transcript from Fireflies -> extract pains -> pull story library from Attio -> run story matching -> run narrative generation -> assemble prep doc -> store in Attio -> notify the founder via Slack with a link to the prep doc.

The agent handles everything. The founder opens the prep doc before the demo and delivers using the story structure.

**Human action required:** Deliver the demo using the story-driven prep doc. After the demo, log the outcome in Attio:
- `outcome`: next_step_committed / follow_up_needed / no_interest
- `prospect_related_to_story`: true/false
- `questions_about_story`: count
- `emotional_connection_observed`: true/false
- `story_feedback`: any notes on what worked or didn't in the narrative

### 4. Monitor for 2 Weeks

Let the automated prep run for all scheduled demos. Check daily:

- Are prep docs generating for every scheduled demo? (Target: 100% automation rate)
- What are the story match scores? (Target: average >=60)
- Is the founder using the prep docs? (Check if `story_demo_completed` events fire after `story_demo_prep_generated`)
- Are engagement signals improving vs Smoke level?

Adjust mid-flight if needed:
- If match scores are consistently low (<50): the story library has gaps. Create new stories targeting the underserved segments.
- If the founder isn't using prep docs: the docs may be too long or the story doesn't feel natural. Simplify the narrative structure — shorter phases, fewer scripted lines.
- If engagement is strong but proposals aren't following: the closing bridge may need strengthening. Test a more direct close: "Based on what {Customer} achieved, what would it take to move forward?"

### 5. Evaluate Against Threshold

After 2 weeks, measure:
- Storytelling adoption rate: % of demos that used a story-driven prep doc (target: >=80%)
- Demo-to-proposal conversion lift: compare the proposal rate for story-driven demos vs the pre-storytelling baseline (target: >=15% improvement)
- Story connection rate: % of demos where the prospect related to the story (track for optimization at Scalable)
- Average engagement score: if Gong recordings are available, score a sample (track for optimization at Scalable)

**If PASS:** Proceed to Scalable to add engagement analysis, A/B testing of stories, and scale volume.
**If FAIL:** Diagnose:
- If adoption is low: the prep process may be too cumbersome or the founder doesn't trust the AI story selection. Simplify and add a manual override option.
- If adoption is high but conversion didn't improve: the stories may not be resonating. Review which stories were used and correlate with outcomes. The matching algorithm may need tuning.
- If conversion improved for some segments but not others: the story library has uneven quality. Strengthen stories for the underperforming segments.

## Time Estimate

- 3 hours: PostHog event configuration and baseline measurement
- 3 hours: Story library expansion and validation
- 5 hours: Automated demo prep workflow build (n8n + story matching + narrative generation)
- 5 hours: Daily monitoring and mid-flight adjustments (25 min/day x 14 days)
- 2 hours: Threshold evaluation, analysis, and diagnosis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal tracking, story records, demo prep storage | $29/user/mo (Plus) — [attio.com/pricing](https://attio.com/pricing) |
| Fireflies | Transcription — discovery call transcripts for pain extraction | Free (800 min/mo) or $18/user/mo (Pro) — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| PostHog | Analytics — event tracking, funnel analysis | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Automation — demo prep workflow orchestration | Self-hosted free or $24/mo (Starter) — [n8n.io/pricing](https://n8n.io/pricing) |
| Anthropic API | AI — story matching, narrative generation | ~$0.10-0.15 per demo prep, ~$3-5/mo at this volume — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** ~$50-75/mo incremental. Primary cost: n8n ($24), Anthropic API (~$5), Fireflies Pro ($18) if not already provisioned.

## Drills Referenced

- the story matched demo prep workflow (see instructions below) — auto-select the best customer story for each prospect and generate a complete story-driven demo preparation document
- `posthog-gtm-events` — configure PostHog event tracking for the storytelling program
