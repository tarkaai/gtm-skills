---
name: trade-show-presence-baseline
description: >
  Trade Show Presence — Baseline Run. Attend 2 trade shows over 8 weeks
  with automated lead capture, tiered post-show nurture sequences, and
  PostHog tracking across the full booth-to-pipeline funnel. Validate
  repeatable conversion and establish cost-per-lead benchmarks.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events"
level: "Baseline Run"
time: "40 hours over 8 weeks"
outcome: ">=150 booth conversations across 2 shows, >=30 qualified leads (Tier 1+2), >=8 meetings booked within 30 days"
kpis: ["Booth conversations per show", "Qualified lead rate", "Meetings booked", "Nurture reply rate", "Cost per qualified lead"]
slug: "trade-show-presence"
install: "npx gtm-skills add marketing/solution-aware/trade-show-presence"
drills:
  - trade-show-booth-operations
  - posthog-gtm-events
  - trade-show-lead-nurture
  - threshold-engine
---

# Trade Show Presence — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** MicroEvents | **Channels:** Events

## Outcomes

- Prove that trade show lead generation is repeatable across 2 shows (not a one-show fluke)
- Establish automated post-show nurture that converts booth leads to pipeline without manual follow-up
- Build the PostHog event tracking foundation for all future trade show measurement
- Establish cost-per-qualified-lead and cost-per-meeting benchmarks for the trade show motion

## Leading Indicators

- Second show produces equal or better qualified lead rate than first show (motion is repeatable)
- Tier 1 nurture follow-up reply rate >30% (personalized Loom approach works)
- Tier 2 nurture sequence reply rate >10% (automated nurture converts)
- At least 2 meetings booked from automated nurture sequences (not just manual follow-up)
- Cost per qualified lead trending in line with or better than other motions

## Instructions

### 1. Configure trade show event tracking

Run the `posthog-gtm-events` drill to implement the full trade show event taxonomy in PostHog:

- `trade_show_target_identified` — pre-show prospect added to target list (properties: show_name, icp_score)
- `trade_show_preshow_outreach_sent` — pre-show email/LinkedIn sent (properties: show_name, channel)
- `trade_show_preshow_reply_received` — target responded to pre-show outreach (properties: show_name, sentiment)
- `trade_show_booth_visit` — conversation logged at booth (properties: show_name, interest_level, staff_member)
- `trade_show_demo_given` — demo delivered (properties: show_name, demo_path, duration_minutes, interest_level)
- `trade_show_meeting_booked_onsite` — meeting booked via Cal.com at show (properties: show_name, days_until_meeting)
- `trade_show_lead_imported` — lead imported to Attio (properties: show_name, tier, source: badge_scan|manual_capture)
- `trade_show_followup_sent` — nurture email sent (properties: show_name, tier, sequence_step, followup_type)
- `trade_show_followup_opened` — nurture email opened (properties: show_name, tier, sequence_step)
- `trade_show_followup_replied` — prospect replied to nurture (properties: show_name, tier, sentiment)
- `trade_show_meeting_booked_from_nurture` — meeting from post-show nurture (properties: show_name, tier, days_since_show)
- `trade_show_deal_created` — deal created in Attio (properties: show_name, tier, deal_value_estimate)

Build a PostHog funnel: `trade_show_booth_visit` -> `trade_show_demo_given` -> `trade_show_followup_sent` -> `trade_show_followup_replied` -> `trade_show_meeting_booked_from_nurture` -> `trade_show_deal_created`

### 2. Upgrade booth operations for repeatability

Run the `trade-show-booth-operations` drill with these Baseline-level enhancements:

- **Standardized pre-show playbook**: Create a templated timeline that you clone for each show: T-4 weeks (select show, book booth), T-3 weeks (extract attendee list, enrich, score), T-2 weeks (launch pre-show outreach), T-1 week (finalize demo prep, brief staff), T-0 (execute). Store in Attio as a campaign checklist.
- **Enriched lead capture**: Upgrade from basic Tally form to an n8n-connected workflow: Tally submission -> n8n webhook -> Clay enrichment (fill in missing company data, LinkedIn URL, tech stack) -> Attio contact creation with full profile. This eliminates the manual same-day import from Smoke.
- **Competitive intel template**: Create a structured form for logging competitor observations at each show: competitor name, booth size, messaging themes, demo approach, traffic level, notable tactics. This accumulates show-over-show intelligence.
- **Staff performance tracking**: Log which booth staff member handled each conversation. Over 2 shows, this reveals who converts best and what approaches work.

### 3. Build post-show nurture automation

Run the `trade-show-lead-nurture` drill to create the full tiered follow-up system:

- **Tier 1 (hot, interest 4-5)**: Personalized Loom video follow-up within 12 hours. The booth staff member records a 60-90 second video referencing the specific conversation. Agent drafts talking points and email template. Sent from the staff member's personal email.
- **Tier 2 (warm, interest 3-4)**: 3-touch automated Loops sequence over 8 days. Each email references the show and includes a relevant resource. n8n trigger: if Tier 2 replies, auto-create Attio deal and escalate to personal follow-up.
- **Tier 3 (curious, interest 2-3)**: 2-touch lightweight Loops sequence. Brief, resource-focused, low-pressure.
- **Tier 4 (badge scan only)**: Single "Thanks for visiting" email. Added to general marketing nurture.
- **Escalation triggers**: Tier 2/3 opens email 3+ times -> promote to higher tier. Any tier visits pricing page -> alert sales rep immediately.

This replaces the manual follow-up from Smoke with a system that scales to any show size.

### 4. Execute 2 trade shows over 8 weeks

**Show 1**: Apply the upgraded operations from steps 2-3. Focus on validating the automation: does the enriched lead capture work end-to-end? Does the tiered nurture produce replies and meetings? Collect every data point.

**Show 2**: Apply learnings from Show 1. Adjust: booth messaging if demo conversion was low, nurture copy if reply rates were low, pre-show outreach if target engagement was low. Keep the process identical except for specific improvements — you are testing repeatability, not changing everything.

**Human action required:** You still staff the booth and deliver demos. The agent handles pre-show research, lead capture automation, nurture sequences, and analytics.

### 5. Analyze cross-show performance

After Show 2's nurture window closes (30 days post-show), compare:

| Metric | Show 1 | Show 2 | Target |
|--------|--------|--------|--------|
| Booth conversations | ? | ? | >=150 total |
| Qualified leads (Tier 1+2) | ? | ? | >=30 total |
| Demo-to-conversation rate | ? | ? | >=20% |
| Tier 1 follow-up reply rate | ? | ? | >=30% |
| Tier 2 nurture reply rate | ? | ? | >=10% |
| Meetings booked | ? | ? | >=8 total |
| Cost per qualified lead | ? | ? | Benchmark established |

Identify: Which show had better ICP density? Which nurture tier converted best? Which demo path produced the most meetings? Did pre-show outreach correlate with show-day performance?

### 6. Evaluate against the threshold

Run the `threshold-engine` drill:

**PASS** (all three met): >=150 total booth conversations, >=30 qualified leads (Tier 1+2), >=8 meetings booked. Proceed to Scalable. You have repeatable trade show operations and working nurture automation.

**FAIL**: Diagnose by metric:
- Low conversations: Show selection problem (wrong audience) or booth execution problem (poor location, weak signage, insufficient staff). Review show scoring criteria in `event-scouting`.
- Low qualified rate: Conversations are happening but interest is low. Booth hook or demo path is not resonating. A/B test messaging at the next show.
- Low meetings from nurture: Leads are captured but nurture is not converting. Review Tier 1 Loom quality, Tier 2 email copy, and CTA clarity. Test different follow-up timing.

## Time Estimate

- PostHog event tracking setup: 3 hours
- Booth operations upgrade (n8n enrichment workflow, templates, checklists): 4 hours
- Post-show nurture automation (Loops sequences, n8n triggers, escalation rules): 6 hours
- Per-show agent effort (pre-show research, enrichment, lead import, nurture launch): 8 hours x 2 = 16 hours
- Per-show human effort (booth staffing): excluded (human hours, not agent hours)
- Cross-show analysis and iteration: 4 hours
- Threshold evaluation: 2 hours
- Competitive intel logging: 2 hours x 2 = 4 hours
- **Total: ~40 hours over 8 weeks** (agent hours; excludes booth staffing time)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Pre-show enrichment + lead enrichment | $185/mo Launch (2,500 credits) — [clay.com/pricing](https://www.clay.com/pricing) |
| Loops | Tiered nurture sequences | Free tier (1,000 contacts) or $49/mo (5,000 contacts) — [loops.so/pricing](https://loops.so/pricing) |
| Loom | Personalized Tier 1 video follow-ups | $12.50/mo Business — [loom.com/pricing](https://www.loom.com/pricing) |
| PostHog | Event tracking + funnels | Free tier: 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | Lead tracking, deals, campaign management | Free tier (3 users) or $29/user/mo Plus — [attio.com](https://attio.com) |
| n8n | Lead capture automation + nurture triggers | Self-hosted free or Cloud Starter EUR24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Cal.com | Meeting booking QR code | Free tier — [cal.com/pricing](https://cal.com/pricing) |
| Tally | Booth lead capture form | Free tier — [tally.so/pricing](https://tally.so/pricing) |

**Estimated play-specific cost at Baseline: $200-275/mo** (Clay + Loops + Loom; other tools on free tier)

Note: Booth rental, travel, and materials are show-specific costs. Budget $3,000-8,000 per show at this level (booth + travel for 2-3 people + basic booth materials).

## Drills Referenced

- `trade-show-booth-operations` — pre-show research, lead capture automation, demo prep, show-day execution, and same-day enrichment
- `posthog-gtm-events` — implement standard trade show event taxonomy for full-funnel measurement
- `trade-show-lead-nurture` — tiered post-show follow-up: Loom for Tier 1, automated sequences for Tier 2-3, escalation triggers
- `threshold-engine` — evaluate pass/fail against conversation, qualified lead, and meeting targets
