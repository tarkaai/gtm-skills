---
name: multi-stakeholder-discovery-scalable
description: >
  Multi-Stakeholder Discovery Process — Scalable Automation. Automated stakeholder engagement
  orchestration across all deals: role-specific outreach sequencing, coverage dashboards,
  intelligent gap alerting, and consensus-gated deal progression. The 10x multiplier is
  engagement orchestration — reaching every stakeholder without proportional founder time.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Scalable Automation"
time: "55 hours over 2 months"
outcome: ">=75% of complex deals have >=4 stakeholder roles engaged, consensus score >=60, and automated engagement orchestration running over 2 months"
kpis: ["Stakeholder engagement rate (outreach → reply)", "Average roles engaged per deal", "Consensus score at time of proposal", "Deal velocity (multi-threaded vs single-threaded)", "Discovery coverage completeness"]
slug: "multi-stakeholder-discovery"
install: "npx gtm-skills add sales/connected/multi-stakeholder-discovery"
drills:
  - dashboard-builder
---

# Multi-Stakeholder Discovery Process — Scalable Automation

> **Stage:** Sales → Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Find the 10x multiplier. At Baseline, the founder ran every discovery call. At Scalable, automated outreach sequences reach every stakeholder, the agent coordinates engagement timing to prevent collisions, coverage dashboards track multi-threading depth, and consensus-gated progression prevents premature proposals. The founder focuses only on high-value discovery calls — everything else is orchestrated.

**Pass threshold:** >=75% of complex deals have >=4 stakeholder roles engaged, consensus score >=60, and automated engagement orchestration active over 2 months.

## Leading Indicators

- Automated outreach sequences deployed for each stakeholder wave (priority-ordered by role)
- Outreach reply rate >=15% across all stakeholder roles
- Coverage dashboard shows improving multi-threading depth week over week
- Gap alerts trigger <24 hours after a stakeholder engagement gap is detected
- Pre-proposal gate blocks deals without adequate consensus (saves from late-stage surprises)
- Deal velocity for multi-threaded deals is >=25% faster than single-threaded deals
- Founder's time per deal decreases while coverage per deal increases

## Instructions

### 1. Deploy Stakeholder Engagement Orchestration

Run the the stakeholder engagement orchestration workflow (see instructions below) drill:

**Build the engagement priority queue:**
1. Create an n8n workflow that triggers whenever `stakeholder-map-assembly` completes (i.e., a new deal is mapped)
2. Query Attio for all unengaged stakeholders on the deal, sorted by influence score
3. Group into 3 engagement waves:
   - Wave 1: Champion and Economic Buyer (unlock access to others)
   - Wave 2: Influencers and Technical Evaluators (engage once top-level priorities are understood)
   - Wave 3: End Users and Gatekeepers (engage with targeted questions informed by earlier discovery)

**Generate role-specific outreach:**
1. For each stakeholder in the queue, call Claude to generate a personalized meeting request
2. The message references their specific role and what you are trying to understand (not a pitch)
3. Example for an Economic Buyer: "We've been speaking with your engineering team about {topic}. Before we recommend anything, I want to understand how this aligns with your strategic priorities for {quarter}. Would 15 minutes be useful?"
4. Example for a Technical Evaluator: "Your team mentioned {specific integration concern}. I'd like to walk through our architecture with someone who can evaluate the technical fit. Would a brief call make sense?"

**Build outreach sequences in Instantly:**
1. Create a 3-touch sequence per wave: initial request, follow-up with added context, final attempt with Cal.com booking link
2. Tag each campaign with deal_id, stakeholder_role, wave_number
3. Stagger waves: Wave 1 starts immediately, Wave 2 starts 5 days after Wave 1 reply or 10 days if no reply, Wave 3 starts after Wave 2

**Build engagement tracking:**
1. n8n workflow triggered by Instantly reply webhooks: update Attio (`engagement_status = Engaged`), log PostHog event, trigger calendar follow-up if positive
2. n8n workflow triggered by Cal.com booking webhooks: update Attio (`discovery_status = Scheduled`), refresh discovery question bank
3. n8n workflow for unresponsive stakeholders: after sequence completes with no reply, suggest alternative approach (champion introduction, LinkedIn, different angle)

### 2. Build the Coverage Dashboard

Run the `dashboard-builder` drill:

**PostHog dashboard (6 panels):**
1. Discovery Coverage Funnel: mapped → outreach sent → replied → scheduled → call completed
2. Consensus Score Distribution: score distribution across all active deals, by stage
3. Stakeholder Coverage Over Time: average engaged % per deal, trended weekly
4. Discovery Impact on Win Rate: close rate for high-consensus (>=60) vs low-consensus (<60) deals
5. Stakeholder Role Engagement Rates: reply rate by role — shows which roles are hardest to reach
6. Time to Full Coverage: median days from deal creation to >=75% stakeholder engagement

**Attio saved views:**
1. "Deals at Risk — Low Consensus": consensus <40, sorted by value
2. "Discovery Gaps — Missing Key Roles": no Economic Buyer or Champion mapped
3. "Stakeholder Outreach Pipeline": unengaged high-influence stakeholders awaiting outreach
4. "Consensus Champions": deals with score >=80 ready for proposal

**Weekly metrics snapshot (n8n cron):**
- New stakeholders mapped, discovery calls completed, average consensus score trend
- Outreach reply rate, coverage completeness trend
- Top risks (consensus drops) and top wins (high-consensus deals)
- Posted to Slack and stored in Attio

### 3. Strengthen Consensus Gating

Extend the the stakeholder consensus tracker workflow (see instructions below) drill with Scalable-level guardrails:

**Proposal gate:**
- Deals cannot advance to Proposed if consensus_score < 60
- If Economic Buyer has not had a direct conversation, flag as "proposal risk"
- If any stakeholder with influence_score >= 7 is classified as Blocker, require a documented mitigation plan before proposal

**Stale engagement detection:**
- If a deal has been at Connected for >30 days and average stakeholder engagement is <50%, alert as stagnant
- Recommend: "This deal needs re-engagement. Generate fresh outreach for Wave 1 stakeholders with updated context."

**Consensus trajectory alerts:**
- Twice-weekly monitoring with AI-generated intervention plans for degrading deals
- Track which intervention types succeed across all deals

### 4. Set Guardrails

- Outreach volume: maximum 3 stakeholders contacted per day per deal to avoid overwhelming the prospect's organization
- Sequence quality: if negative reply rate exceeds 10% on any sequence, pause and review messaging
- Coverage completeness: deals must maintain >=75% of Baseline's discovery depth — if coverage drops, alert
- Engagement orchestration must not contact anyone who has explicitly asked not to be contacted

### 5. Run for 2 Months and Evaluate

After 2 months, evaluate against the threshold:
- Count complex deals with >=4 roles engaged AND consensus >=60 AND orchestration active
- Compare deal velocity and close rates to Baseline benchmarks
- Review the coverage dashboard for trends

If PASS: Multi-stakeholder discovery is scaling. Proceed to Durable for autonomous optimization.
If FAIL: Diagnose the bottleneck — outreach (stakeholders not replying?), discovery quality (calls happening but consensus not improving?), or orchestration (automation errors?).

## Time Estimate

- 10 hours: Build and test engagement orchestration workflows (n8n + Instantly + Cal.com)
- 6 hours: Build intelligence reporting dashboards and Attio saved views
- 4 hours: Configure consensus gating and guardrails
- 3 hours: Test end-to-end with live deals
- 25 hours: Run discovery calls over 2 months (founder's time, decreasing as orchestration handles more)
- 7 hours: Weekly monitoring, iteration, and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — stakeholder data, deal tracking, consensus scores, saved views | $29/user/mo (Plus) — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — stakeholder mapping, org chart research | $185/mo (Launch) or $495/mo (Growth) — [clay.com/pricing](https://www.clay.com/pricing) |
| Instantly | Cold email — stakeholder outreach sequences | $47/mo (Growth) or $97/mo (Hypergrowth) — [instantly.ai/pricing](https://instantly.ai/pricing) |
| Cal.com | Scheduling — discovery call booking links | Free (1 user) or $15/user/mo (Teams) — [cal.com/pricing](https://cal.com/pricing) |
| Fireflies | Transcription — discovery call recording | $10/user/mo (Pro, annual) — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| PostHog | Analytics — dashboards, funnels, consensus tracking | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Automation — orchestration, monitoring, reporting | $60/mo (Pro) — [n8n.io/pricing](https://n8n.io/pricing) |
| Anthropic API | AI — outreach generation, sentiment extraction, question generation | Usage-based, ~$3/MTok input (Sonnet 4.6) — [claude.com/pricing](https://claude.com/pricing) |

**Estimated play-specific cost this level:** ~$250-450/mo. Primary cost drivers: Clay ($185-495), Instantly ($47-97), n8n Pro ($60), Anthropic API (~$30-50/mo for extraction + outreach generation).

## Drills Referenced

- the stakeholder engagement orchestration workflow (see instructions below) — automated role-specific outreach sequencing, engagement tracking, coverage monitoring, and gap alerting across all deals
- `dashboard-builder` — PostHog dashboards, Attio saved views, weekly metrics snapshots, and monthly ROI calculations for multi-stakeholder discovery effectiveness
- the stakeholder consensus tracker workflow (see instructions below) — consensus score computation, trajectory monitoring, degradation alerts, intervention plans, and pre-proposal gate enforcement
