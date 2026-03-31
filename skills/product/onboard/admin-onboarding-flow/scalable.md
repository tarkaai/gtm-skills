---
name: admin-onboarding-flow-scalable
description: >
  Admin vs User Onboarding — Scalable Automation. Scale the dual onboarding paths to 500+
  users with persona-specific variants for admins (SMB, mid-market, enterprise) and users
  (technical, non-technical). Automated persona classification, per-persona A/B testing, and
  multi-channel delivery across Intercom, Loops, and PostHog feature flags.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Scalable Automation"
time: "50 hours over 2 months"
outcome: "≥70% admin setup completion AND ≥60% user activation at 500+ total users, with per-persona rates within 10% of top performer"
kpis: ["Admin setup completion by persona", "User activation by persona", "Team invite rate", "Time to workspace ready by company size", "Per-persona checklist completion rate", "Experiment win rate"]
slug: "admin-onboarding-flow"
install: "npx gtm-skills add product/onboard/admin-onboarding-flow"
drills:
  - onboarding-persona-scaling
  - ab-test-orchestrator
---

# Admin vs User Onboarding — Scalable Automation

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Scale the dual onboarding paths from Baseline to handle 500+ users with persona-specific variants. Admins are segmented by company profile (SMB solo admin, mid-market team admin, enterprise multi-admin). Users are segmented by role type (technical builder, non-technical end user). Each persona gets a tailored checklist, email sequence, and product tour. Pass threshold: ≥70% admin setup completion AND ≥60% user activation across 500+ total users, with no persona more than 10 percentage points below the top-performing persona.

## Leading Indicators

- Automated persona classification covering ≥95% of signups (≤5% falling to "default")
- Per-persona activation funnels showing divergence (confirming personas are meaningfully different)
- At least 2 completed A/B tests per persona with clear winners
- Admin setup completion rate holding steady or improving as volume increases 10x
- User activation rate stable across signup source cohorts (not dependent on a single channel)
- Team expansion rate (invited users per admin) increasing with persona-specific invite prompts

## Instructions

### 1. Scale persona-based onboarding

Run the `onboarding-persona-scaling` drill to expand from the binary admin/user split to persona-specific paths.

**Admin personas (classify at workspace creation):**

| Persona | Signal | Setup focus |
|---------|--------|-------------|
| SMB Solo Admin | company_size ≤ 5, single admin | Minimal setup: skip permissions, simplified billing, emphasize quick team invite |
| Mid-Market Team Admin | company_size 6-100, admin role | Full setup: permissions templates, integration priority, team structure |
| Enterprise Admin | company_size > 100, SSO detected or enterprise plan | Compliance setup: SSO/SAML config, audit logging, custom permissions, IT review flow |

For each admin persona, create a separate Intercom Checklist with steps tailored to their needs. SMB gets 4 steps (skip permissions, simplify integrations). Mid-Market gets 6 steps (full flow). Enterprise gets 8 steps (add SSO, compliance, custom branding).

**User personas (classify at invite acceptance):**

| Persona | Signal | Onboarding focus |
|---------|--------|-----------------|
| Technical Builder | role contains "engineer"/"developer", or invited from technical workspace | API-first tour, code examples, integration setup, skip UI tutorials |
| Non-Technical End User | role contains "manager"/"analyst"/"coordinator", or default | UI-focused tour, workflow templates, guided first action |

For each user persona, create a separate Intercom Product Tour and Loops email sequence. Technical users get shorter, more direct content. Non-technical users get more hand-holding.

Build automated persona classification using n8n workflows that fire on `workspace_created` (admin personas) and `team_invite_accepted` (user personas). Classification uses signup data, enrichment from company domain, and explicit role selection if available.

Push persona assignments to PostHog (`admin_persona`, `user_persona` person properties), Intercom (`persona_type` user attribute), and Loops (`persona_type` contact property).

### 2. Run per-persona A/B tests

Run the `ab-test-orchestrator` drill to systematically test improvements to each persona's onboarding path.

**Test priority order:**

1. **Worst-performing admin persona**: test checklist structure (fewer steps vs current), test checklist copy (benefit-focused vs instruction-focused), test email cadence (daily vs every-other-day)
2. **Worst-performing user persona**: test tour length (3 steps vs 5 steps), test first suggested action (simpler quick-win vs full workflow), test email tone (technical vs conversational)
3. **Highest-volume persona**: any improvement here has the largest absolute impact. Test the most impactful variable.

For each test:
- Form a hypothesis: "If we reduce the SMB admin checklist from 4 steps to 3 (removing integration step), then setup completion will increase by 8pp, because SMB admins want speed over configurability."
- Use PostHog experiments to split traffic 50/50 within the persona segment
- Require 100+ users per variant before evaluating (this determines test duration)
- Evaluate with 95% confidence level
- If the variant wins: implement permanently for that persona
- If inconclusive: keep the simpler variant

Target: at least 2 completed experiments per persona over the 2-month Scalable period. Document every experiment: hypothesis, variants, result, and what was learned.

### 3. Build per-persona dashboards and alerts

Create a PostHog dashboard "Admin Onboarding by Persona" with:
- Admin setup completion rate by persona (weekly trend, 8-week window)
- Checklist step completion heatmap by persona (which steps complete, which stall)
- Median time-to-workspace-ready by persona
- Team invite rate by admin persona
- Email engagement by persona (open rate, click rate, unsubscribe rate)

Create a PostHog dashboard "User Onboarding by Persona" with:
- User activation rate by persona (weekly trend)
- Tour completion rate by persona
- First-core-action rate by persona
- Email engagement by persona

Set alerts:
- Any persona's setup completion or activation rate drops below threshold for 2 consecutive weeks
- Any persona's email unsubscribe rate exceeds 2%
- Persona classification "default" rate exceeds 10% (classification logic needs updating)

### 4. Automate persona-specific stall interventions

Expand the stall-point nudges from Baseline to be persona-aware:
- SMB admin stalled at billing for 48h: "No credit card needed — start your 14-day trial and invite your team now."
- Mid-Market admin stalled at integrations for 72h: "Teams like yours typically connect [top integration] first. Here's a 2-minute setup guide."
- Enterprise admin stalled at SSO for 1 week: "Need help with SSO setup? Our team can configure it for you in a 15-minute call." (Route to sales-assist.)
- Technical user stalled at first action: "Here's a code snippet to get started: [API quickstart]."
- Non-technical user stalled at first action: "Watch this 60-second walkthrough: [video link]."

Wire these via n8n workflows that check persona + stall duration + step and trigger the appropriate Intercom message.

### 5. Evaluate at scale

After 2 months, measure against the pass criteria across all 500+ users:

- **Admin setup completion by persona**: each persona ≥70%, with no persona more than 10pp below the best
- **User activation by persona**: each persona ≥60%, with no persona more than 10pp below the best
- **Persona classification accuracy**: ≥95% classified, ≤5% default
- **Experiment velocity**: at least 4 experiments completed, at least 2 with statistically significant results

If PASS: document all persona paths, winning experiment results, and the current configuration. Proceed to Durable.

If FAIL: identify the underperforming persona. If it is a classification problem (users ending up in wrong persona), fix classification logic. If it is a content problem (correct persona, wrong onboarding content), run more targeted experiments. If one persona is structurally different from others (e.g., enterprise needs human touch), consider a hybrid human+automated approach for that persona.

## Time Estimate

- 12 hours: persona definition, classification automation, and per-persona checklist/tour/email creation
- 10 hours: per-persona A/B test design, setup, and analysis (5 hours per test cycle x2)
- 8 hours: dashboard and alert setup
- 8 hours: persona-specific stall interventions
- 12 hours: monitoring, iteration, and experiment management over 2 months (~1.5 hr/week)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Analytics, feature flags, experiments, cohorts | Growth: ~$0-450/mo based on events (https://posthog.com/pricing) |
| Intercom | Checklists, product tours, in-app messages | Pro: $99/seat/mo for advanced targeting (https://www.intercom.com/pricing) |
| Loops | Lifecycle email sequences per persona | Growth: $49-149/mo for 5K-25K contacts (https://loops.so/pricing) |
| n8n | Automation (persona routing, stall detection, event bridging) | Pro: $50/mo for higher execution volume (https://n8n.io/pricing) |

**Estimated monthly cost at Scalable:** ~$200-700/mo (Intercom $99-200 + Loops $49-149 + PostHog $0-300 + n8n $24-50)

## Drills Referenced

- `onboarding-persona-scaling` — expands the binary admin/user split into persona-specific onboarding paths with automated classification
- `ab-test-orchestrator` — runs rigorous per-persona A/B tests on checklist structure, email copy, and tour design
