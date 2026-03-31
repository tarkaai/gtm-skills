---
name: sandbox-environment-demo-smoke
description: >
  Sandbox Environment Demo — Smoke Test. Manually provision sandbox environments for 5+
  qualified prospects with personalized sample data and structured kickoff materials to
  validate whether hands-on product access accelerates deal progression.
stage: "Sales > Connected"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Smoke Test"
time: "7 hours over 1 week"
outcome: "Sandboxes provided to ≥5 opportunities in 1 week with ≥60% showing active usage (3+ sessions, 30+ minutes total)"
kpis: ["Sandbox provisioning rate", "Time to first login", "Active usage rate (3+ sessions)", "Feature exploration depth", "Demo-to-proposal conversion"]
slug: "sandbox-environment-demo"
install: "npx gtm-skills add sales/connected/sandbox-environment-demo"
drills:
  - sandbox-provisioning-workflow
  - threshold-engine
---

# Sandbox Environment Demo — Smoke Test

> **Stage:** Sales → Connected | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Provision sandbox environments for at least 5 qualified opportunities in one week. At least 60% of provisioned sandboxes must show active usage: 3 or more sessions and 30 or more minutes of total time. This validates that prospects will actually use a sandbox when given access and that the provisioning workflow is executable.

## Leading Indicators

- Time from provisioning to first login (target: <24 hours for 80%+ of prospects)
- Number of distinct features explored per sandbox in the first session
- Success checklist items attempted within 48 hours of access
- Prospect replies to kickoff email (questions, requests for walkthrough)

## Instructions

### 1. Identify 5-8 qualified sandbox candidates

Pull deals at Connected stage from Attio. For each, verify sandbox qualification: discovery call completed, at least 2 use cases identified, deal value justifies the investment of provisioning time. Select 5-8 deals to provision this week.

### 2. Run the sandbox-provisioning-workflow drill

For each selected deal, run the `sandbox-provisioning-workflow` drill. This handles:
- Determining the best sample data persona based on discovery notes
- Provisioning the sandbox environment with relevant sample data
- Generating a personalized success checklist (3-5 milestones tied to discovery pain points)
- Recording a Loom walkthrough video
- Sending the kickoff email with sandbox access, checklist, and video
- Scheduling follow-up touchpoints in Attio (48 hours, Day 5, Day 10, Day 13)

**Human action required:** Review each kickoff email before sending. Verify the success checklist items map to actual pain points discussed in discovery. Record or review the Loom walkthrough to ensure it covers the right features. Conduct the scheduled walkthrough calls when prospects book them.

### 3. Track sandbox usage manually

For each provisioned sandbox, check PostHog daily for:
- Whether the prospect has logged in
- Which features they explored
- How many success checklist milestones they completed
- Any errors they encountered

Log usage observations as notes in Attio on each deal. When a prospect shows high engagement (3+ features used, checklist item completed), reach out to acknowledge progress and suggest next steps. When a prospect shows low engagement (no login after 48 hours, single short session), send a check-in offering help.

### 4. Execute follow-up touchpoints

Follow the touchpoint schedule from the provisioning workflow:
- **48 hours**: If no login, send reminder. If logged in, send encouragement.
- **Day 5**: Check milestone progress. Offer walkthrough call if <2 milestones completed.
- **Day 10**: Assess engagement. If hot, propose next steps toward proposal. If cold, send "what's blocking you?" message.
- **Day 13**: Final reminder before expiry. Offer extension for engaged prospects.

**Human action required:** Execute each touchpoint. Personalize the message based on observed usage patterns.

### 5. Evaluate against threshold

Run the `threshold-engine` drill to measure results against the pass criteria:

- **Primary**: Sandboxes provisioned for ≥5 opportunities in 1 week
- **Secondary**: ≥60% of provisioned sandboxes show active usage (3+ sessions, 30+ minutes total)
- **Signal**: Track correlation between sandbox usage and demo-to-proposal conversion

Pull data from PostHog (usage metrics) and Attio (deal progression) to compute the verdict. Log the threshold check result in PostHog.

### 6. Document learnings

Record what worked and what failed:
- Which sample data personas drove the most engagement?
- Which success checklist items were completed most/least?
- Did walkthrough videos or walkthrough calls drive more usage?
- Which follow-up touchpoints generated the strongest response?

Store learnings in Attio as a note on a "Sandbox Program" campaign record. These learnings inform Baseline configuration.

## Time Estimate

- 1 hour: Identify and qualify sandbox candidates
- 3 hours: Provision 5-8 sandboxes (provision, customize checklist, record Loom, send kickoff)
- 2 hours: Monitor usage and execute follow-up touchpoints over the week
- 1 hour: Evaluate threshold and document learnings

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loom | Walkthrough video recording | Free (Starter: 25 videos, 5 min limit) or $12.50/creator/mo (Business) — [loom.com/pricing](https://www.loom.com/pricing) |
| Loops | Kickoff and follow-up emails | Free up to 1,000 contacts / 4,000 sends — [loops.so/pricing](https://loops.so/pricing) |

**Estimated play-specific cost:** Free (Loom Starter + Loops Free tier sufficient for 5-8 sandboxes)

_CRM (Attio), analytics (PostHog), and automation (n8n) are standard stack — not included in play budget._

## Drills Referenced

- `sandbox-provisioning-workflow` — provisions the sandbox, generates personalized onboarding materials, and sends access to the prospect
- `threshold-engine` — evaluates sandbox usage data against pass/fail criteria and recommends next action
