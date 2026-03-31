---
name: analyst-consultant-briefings-scalable
description: >
  Analyst & Consultant Briefings — Scalable Automation. Expand to 30+ analysts with automated
  nurture sequences, relationship tracking, and a referral attribution pipeline.
  Target >=6 intro meetings over 2 months with analyst-sourced pipeline tracked in Attio.
stage: "Sales > Qualified"
motion: "Partnerships & Warm Intros"
channels: "Other"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=6 analyst briefing meetings completed AND >=2 analyst-sourced referrals over 2 months"
kpis: ["Briefings completed", "Analyst-sourced referrals", "Referral-to-meeting conversion rate", "Analyst relationship health score", "Pipeline value from analyst referrals"]
slug: "analyst-consultant-briefings"
install: "npx gtm-skills add sales/qualified/analyst-consultant-briefings"
drills:
  - analyst-relationship-nurture
  - follow-up-automation
---

# Analyst & Consultant Briefings — Scalable Automation

> **Stage:** Sales → Qualified | **Motion:** Partnerships & Warm Intros | **Channels:** Other

## Outcomes

Find the 10x multiplier: expand from a handful of analyst relationships to a managed portfolio of 30+ analysts and consultants with automated nurture, relationship health tracking, and referral attribution. The shift from Baseline: you now have always-on automation maintaining analyst relationships without proportional time investment. Analysts who have been briefed receive quarterly updates automatically; referrals are tracked through the full sales pipeline.

**Pass threshold:** >=6 analyst briefing meetings completed AND >=2 analyst-sourced referrals over 2 months.

## Leading Indicators

- Analyst portfolio size (target: 30+ analysts across Tier 2-4 with Briefing Status = "Briefed" or "Engaged")
- Quarterly update open rate (target: >=40% — analysts are reading your updates)
- Re-briefing acceptance rate (target: >=50% for analysts who were engaged in initial briefing)
- Referral rate per briefed analyst (target: >=1 referral per 5 briefed analysts per quarter)
- Analyst relationship health: % in "Healthy" status (target: >=60%)

## Instructions

### 1. Expand the analyst target list

Re-run the `analyst-target-research` drill (from Smoke) with broader parameters:
- Include Tier 1-2 analysts now that you have a track record of successful briefings (social proof matters for large firms)
- Expand to adjacent categories — analysts who cover your buyer's broader technology stack, not just your specific category
- Add international analysts if you are expanding geographically
- Target: 30-50 analysts total in the Attio "Analyst Briefing Targets" list

For each new analyst, prepare briefing materials using the `briefing-deck-preparation` drill (from Smoke). Include results from your first briefings as proof points.

### 2. Build the automated nurture system

Run the `analyst-relationship-nurture` drill to create always-on relationship management:

**Quarterly update automation:** Build an n8n workflow triggered on the first Monday of each quarter. For each analyst with Briefing Status = "Briefed" or "Engaged," generate a personalized quarterly update email (2-3 bullets of significant news using their terminology), send via Loops, and log the event in PostHog.

**Milestone notification triggers:** Configure n8n workflows that fire when milestone events occur (funding announced, major customer win, product launch). For each event, generate tailored notifications for relevant analysts and queue for human review before sending.

**Re-briefing pipeline:** For analysts approaching the 12-month mark since last briefing, auto-generate a re-briefing request with updated materials and queue for human review.

**Human action required:** Review quarterly update content before each send. Ensure metrics are current and approved for external sharing. Review milestone notifications before sending.

### 3. Automate follow-up and referral tracking

Run the `follow-up-automation` drill to build n8n workflows for:

**Post-briefing follow-up:** After every `analyst_briefing_completed` event, trigger a workflow that:
- Sends a thank-you email within 2 hours (include the briefing document and any materials discussed)
- Creates a follow-up task in Attio for 2 weeks later
- If engagement score >= 4, add analyst to "High-Engagement" segment for priority nurture

**Referral attribution:** When a new deal is created in Attio and the source is "analyst_referral":
- Tag the deal with the referring analyst's name
- Fire an `analyst_referral_received` PostHog event
- Update the referring analyst's Attio record: increment referral count, update "Last Referral Date"
- Send a thank-you note to the analyst (queued for human review)

**Referral-to-pipeline tracking:** Connect analyst-sourced deals through the full sales pipeline. Track conversion rates compared to other lead sources. This data proves ROI of the analyst program.

### 4. Conduct 6+ briefings at scale

With automated nurture maintaining existing relationships, focus your manual time on:
- **New briefings:** Schedule and conduct briefings with new analysts from the expanded list (target: 3-4 new briefings per month)
- **Re-briefings:** Conduct annual update briefings with engaged analysts (target: 1-2 per month)
- **High-value follow-ups:** Deep-dive sessions with analysts who are actively writing about your category

**Human action required:** Continue conducting briefings personally. The automation handles nurture, scheduling, and follow-up — but the briefing itself requires a human who can speak to product vision and strategy.

### 5. Track relationship health

Build an Attio list view showing analyst relationship health:
- **Active:** In an ongoing briefing or follow-up conversation
- **Healthy:** Engaged in the last quarter (opened update, replied, or had interaction)
- **Cooling:** No engagement in 1-2 quarters
- **Cold:** No engagement in 3+ quarters

Configure a weekly alert: if any Priority 1 analyst moves from Healthy to Cooling, flag for immediate outreach.

### 6. Evaluate against threshold

Measure against: >=6 briefing meetings completed AND >=2 analyst-sourced referrals over 2 months.

If PASS: Document the full workflow: which automation is running, which analysts are most engaged, what referral patterns are emerging. Prepare the handoff to Durable by ensuring all PostHog events and Attio data are clean and consistent. Proceed to Durable.

If FAIL: Check the funnel. If briefings are happening but no referrals, the ask may be too subtle — be more direct in briefings about what kind of prospects you are looking for. If relationship health is dropping, nurture content may not be valuable enough — survey engaged analysts about what updates they actually want. If new analyst acquisition is stalled, expand your warm intro network or try different outreach channels.

## Time Estimate

- 10 hours: Expand analyst list, prepare new briefing materials
- 8 hours: Build nurture automation (n8n workflows, Loops sequences, PostHog events)
- 4 hours: Build follow-up and referral attribution automation
- 24 hours: Conduct 6-8 briefings (30 min each + prep and follow-up) over 2 months
- 8 hours: Monitor relationships, process referrals, manage re-briefings
- 6 hours: Evaluate metrics, iterate on messaging, document workflows

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM for analyst portfolio and referral tracking | Free tier or existing plan — [attio.com](https://attio.com) |
| PostHog | Event tracking, funnel analysis, dashboards | Free tier (1M events/mo) — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Workflow automation (nurture, follow-up, alerts) | Free self-hosted or $24/mo cloud — [n8n.io/pricing](https://n8n.io/pricing) |
| Loops | Quarterly update email sequences | Free tier (1,000 contacts) or $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| Cal.com | Briefing scheduling | Free tier — [cal.com/pricing](https://cal.com/pricing) |
| Clay | Analyst enrichment for expanded list | Growth $495/mo or existing plan — [clay.com](https://www.clay.com) |
| Claude API | Briefing documents, update content generation | ~$1-3/mo at this volume — [anthropic.com](https://console.anthropic.com) |

**Estimated play-specific cost:** $50-100/mo (Loops if beyond free tier + Clay enrichment credits for list expansion)

## Drills Referenced

- `analyst-relationship-nurture` — Automated quarterly updates, milestone notifications, and re-briefing triggers
- `follow-up-automation` — Post-briefing follow-up and referral attribution workflows
