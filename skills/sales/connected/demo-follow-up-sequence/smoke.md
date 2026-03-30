---
name: demo-follow-up-sequence-smoke
description: >
  Demo Follow-Up Sequence — Smoke Test. Structured multi-touch follow-up after demos delivering recap, resources, answers to questions, and clear next steps to maintain momentum and accelerate deals.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Email, Direct"
level: "Smoke Test"
time: "6 hours over 2 weeks"
outcome: "Demo follow-up completed on ≥8 opportunities in 2 weeks"
kpis: ["Follow-up completion rate", "Response rate", "Next step scheduling rate", "Content engagement"]
slug: "demo-follow-up-sequence"
install: "npx gtm-skills add sales/connected/demo-follow-up-sequence"
---
# Demo Follow-Up Sequence — Smoke Test

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Email, Direct

## Overview
Structured multi-touch follow-up after demos delivering recap, resources, answers to questions, and clear next steps to maintain momentum and accelerate deals.

**Time commitment:** 6 hours over 2 weeks
**Pass threshold:** Demo follow-up completed on ≥8 opportunities in 2 weeks

---

## Budget

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Recommended tools
- **Attio** (CRM)
- **PostHog** (CDP)

---

## Instructions

1. After first 8-10 demos, immediately send demo recap email (within 2 hours) summarizing: key points discussed, how product addresses their needs, answers to questions raised, suggested next steps.

2. Include relevant resources in recap: link to recording, relevant case study, feature documentation, ROI calculator, pricing overview.

3. Schedule Day 1 follow-up: send personalized email checking in, asking if additional questions arose, offering to connect with specific team members (technical, customer success).

4. Execute Day 3 follow-up: share additional valuable content based on demo discussion (integration guide, security docs, customer story); propose specific next step (technical demo, POC, proposal discussion).

5. Implement Day 7 follow-up: if no response, send value-add touch (relevant blog post, industry report, competitor comparison); ask if timeline has changed.

6. Track PostHog events: demo_recap_sent, resource_clicked, follow_up_sent, response_received, next_step_scheduled.

7. Log all follow-up activities in Attio; note which follow-ups generate responses and which content drives engagement.

8. Set pass threshold: Complete demo follow-up sequences on ≥8 opportunities in 2 weeks with ≥50% scheduling next step.

9. Measure effectiveness: track response rates by follow-up touch, time to next step, demo-to-proposal conversion rate.

10. Document which follow-up approaches and content drive highest engagement; proceed to Baseline if threshold met.

---

## KPIs to track
- Follow-up completion rate
- Response rate
- Next step scheduling rate
- Content engagement

---

## Pass threshold
**Demo follow-up completed on ≥8 opportunities in 2 weeks**

If you hit this threshold → move to the **Baseline Run** skill.
If not → iterate on ICP, offer, or channel and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/demo-follow-up-sequence`_
