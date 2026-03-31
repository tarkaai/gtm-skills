---
name: discovery-based-demo-baseline
description: >
  Discovery-Based Demo — Baseline Run. Scale to 10-15 demos over 2 weeks with
  automated demo prep, structured follow-up sequences, and continuous tracking.
  First always-on automation: agent generates demo prep docs from discovery
  transcripts and monitors conversion rates.
stage: "Sales > Aligned"
motion: "Outbound Founder-Led"
channels: "Direct, Product"
level: "Baseline Run"
time: "22 hours over 2 weeks"
outcome: ">=70% demo-to-nextstep conversion and >=40% demo-to-proposal conversion over 2 weeks"
kpis: ["Demo-to-nextstep conversion", "Demo-to-proposal conversion", "Demo engagement score", "Recap video view rate"]
slug: "discovery-based-demo"
install: "npx gtm-skills add sales/aligned/discovery-based-demo"
drills:
  - demo-prep-automation
  - posthog-gtm-events
  - follow-up-automation
---

# Discovery-Based Demo — Baseline Run

> **Stage:** Sales > Aligned | **Motion:** Outbound Founder-Led | **Channels:** Direct, Product

## Outcomes

70% or more of demos result in a next-step commitment. 40% or more of demos progress to a proposal request within 2 weeks. Automated demo prep reduces founder preparation time by at least 50% compared to Smoke level manual prep.

## Leading Indicators

- Demo prep docs are generated within 30 minutes of discovery call completion
- Recap videos achieve >50% view rate from prospects
- Prospects who watch >80% of recap video convert to next step at >85% rate
- Follow-up emails sent within 2 hours of demo completion
- Pain-to-feature mapping accuracy improves (fewer "I already knew about that" moments in demos)

## Instructions

### 1. Configure automated demo prep

Run the `demo-prep-automation` drill to set up the automation pipeline. After each discovery call:

1. Fireflies transcribes the call and makes the transcript available via API
2. The agent runs BANT extraction on the transcript (using `call-transcript-bant-extraction` fundamental)
3. The agent maps extracted pains to product features using Claude
4. The agent generates a structured demo prep document with: opening hook, pain recap, ordered feature demo sections, ROI estimates, and closing strategy
5. The agent stores the prep doc as an Attio note on the deal

**Human action required:** Review each auto-generated demo prep doc before the demo. Verify pain-to-feature mappings are accurate. Adjust the demo flow if needed. The agent does the research; the founder makes the judgment calls.

### 2. Set up PostHog tracking for the full funnel

Run the `posthog-gtm-events` drill to configure event tracking for the complete discovery-to-demo pipeline:

- `discovery_call_completed` -- fired when Fireflies transcript is processed
- `demo_prep_generated` -- fired when the agent creates a prep doc
- `demo_scheduled` -- fired when Cal.com booking is confirmed
- `demo_completed` -- fired after each demo with outcome, pains addressed, questions asked, duration
- `recap_video_sent` -- fired when Loom recap is shared
- `recap_video_viewed` -- fired when prospect watches the recap (via Loom webhook)
- `next_step_committed` -- fired when prospect agrees to next meeting
- `proposal_requested` -- fired when prospect requests pricing

Connect PostHog to Attio via n8n webhook so deal stage changes are tracked automatically.

### 3. Build demo persona templates

Create demo templates in Attio for your top 3 prospect personas. Each template includes:

- Persona definition (role, industry, typical pains)
- Default demo flow for that persona (which features to lead with)
- Standard ROI benchmarks (e.g., "Operations leaders typically save 15 hours/week")
- Common objections and handling strategies

The agent personalizes each template using discovery data. Templates reduce prep time for common personas while still tailoring to individual pains.

### 4. Execute demos and send automated follow-ups

**Human action required:** Run each demo live using the auto-generated prep doc.

Run the `follow-up-automation` drill to configure post-demo workflows:

1. **Within 2 hours of demo:** Agent generates and sends a recap email referencing the 3 pains discussed, features shown, and ROI estimates. Includes a Loom recap video link (recorded by the founder after the demo using the auto-generated script) and a Cal.com link for the next meeting.
2. **If recap video viewed >80%:** Agent creates a high-priority follow-up task in Attio. If no next step committed within 48 hours, agent drafts a nudge email.
3. **If no video view within 3 days:** Agent sends a text-only recap email as backup with the same content minus the video.
4. **If prospect mentioned other stakeholders in discovery:** Agent generates a one-page internal summary the prospect can forward. Sent as a follow-up 2 days after the demo.

### 5. Monitor and evaluate over 2 weeks

Build a PostHog funnel: `discovery_call_completed` -> `demo_scheduled` -> `demo_completed` -> `next_step_committed` -> `proposal_requested`

After 2 weeks with 10-15 demos completed:
- Primary: >=70% of demos resulted in next-step commitment
- Primary: >=40% of demos progressed to proposal request
- Secondary: Recap video view rate >=50%
- Secondary: Average demo prep time <20 minutes (down from 30 min at Smoke)

If PASS, proceed to Scalable. If FAIL, diagnose:
- Low next-step rate but high engagement: closing technique needs work, not discovery
- Low engagement: pain-to-feature mapping is off; review prep docs vs actual demo flow
- Low video view rate: recap content or timing needs adjustment

## Time Estimate

- 4 hours: initial setup (demo-prep-automation, PostHog events, follow-up workflows)
- 2 hours: build 3 persona templates
- 10 hours: execute 10-15 demos (40-45 min each)
- 3 hours: review auto-generated prep docs (15 min each)
- 2 hours: record recap videos (10 min each)
- 1 hour: weekly funnel review and threshold evaluation
- **Total: ~22 hours over 2 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM -- deal records, demo prep notes, pipeline | Free (3 users); Plus $29/user/mo |
| PostHog | Analytics -- demo funnel, event tracking | Free tier (1M events/mo) |
| Fireflies | Transcription -- discovery and demo call recording | Pro $10/user/mo (annual); Business $19/user/mo for API access |
| Cal.com | Scheduling -- demo booking links | Free (1 user); Teams $15/user/mo |
| Loom | Video -- recap videos after demos | Free (25 videos); Business $12.50/user/mo for analytics |
| n8n | Automation -- demo prep pipeline, follow-up workflows | Free (self-hosted); Starter $24/mo cloud |
| Anthropic API | AI -- BANT extraction, pain-feature mapping, prep doc generation | ~$0.50-2.00 per demo prep (Claude Sonnet) |

**Estimated play-specific cost at Baseline:** ~$75-150/mo (Fireflies Pro + Loom Business + n8n Starter + Anthropic API usage)

## Drills Referenced

- `demo-prep-automation` -- auto-generate personalized demo prep docs from discovery transcripts
- `posthog-gtm-events` -- configure event tracking for the demo funnel
- `follow-up-automation` -- automated post-demo follow-up sequences across email and video
