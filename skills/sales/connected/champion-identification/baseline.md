---
name: champion-identification-baseline
description: >
  Champion Identification & Development — Baseline Run. First always-on automation for champion
  identification, recruitment, and enablement. Automated profiling runs when deals enter Connected
  stage, recruitment sequences fire for scored candidates, and enablement kits are delivered to
  recruited champions.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Baseline Run"
time: "20 hours over 2 weeks"
outcome: ">=60% of active deals have at least 1 recruited champion, and champion deals show >=35% higher win rate over 2 weeks"
kpis: ["Champion rate per deal", "Champion recruitment conversion rate", "Enablement forward rate", "Win rate (champion vs non-champion)", "Champion engagement score"]
slug: "champion-identification"
install: "npx gtm-skills add sales/connected/champion-identification"
drills:
  - champion-recruitment-sequence
  - champion-enablement-delivery
  - posthog-gtm-events
---

# Champion Identification & Development — Baseline Run

> **Stage:** Sales → Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

First always-on automation. When a deal enters the Connected stage, champion profiling runs automatically, recruitment sequences fire for qualified candidates, and recruited champions receive personalized enablement kits. The agent manages the pipeline — the founder reviews and records Loom videos.

**Pass threshold:** >=60% of active deals have at least 1 recruited champion, and champion deals show >=35% higher win rate over 2 weeks.

## Leading Indicators

- Champion profiling auto-triggers within 24 hours of deal entering Connected
- Recruitment sequences achieve >=15% positive reply rate
- >=50% of recruited champions open the enablement kit emails
- >=20% of champions forward enablement materials to colleagues (Loom multi-viewer signal)
- Champion deals show faster email response times from the account

## Instructions

### 1. Set Up Champion CRM Tracking

Run the champion tracking setup from the `champion-profiling` drill prerequisites:
- Create all champion custom attributes on People and Deals objects in Attio (champion_status, champion_score, champion_signals, etc.)
- Create the three dynamic lists: Champion Candidates, Active Champions, At-Risk Champions
- Set up the two Attio automations: auto-update deal champion health, auto-count champions per deal

This is one-time setup. Once configured, all subsequent drills read from and write to these fields.

### 2. Configure Event Tracking

Run the `posthog-gtm-events` drill to set up PostHog events for the champion program:

| Event | Trigger |
|-------|---------|
| `champion_candidate_identified` | New candidate pushed to Attio from profiling |
| `champion_email_sent` | Recruitment email sent via Instantly |
| `champion_email_replied` | Reply received (positive, neutral, or negative) |
| `champion_recruited` | Status changed to "Recruited" |
| `champion_enablement_delivered` | Enablement kit sent via Loops |
| `champion_material_forwarded` | Loom video viewed by additional viewers |
| `champion_activated` | Status changed to "Active" |

Connect PostHog events to Attio via n8n webhook so deal records update automatically.

### 3. Launch Recruitment Sequences

Run the `champion-recruitment-sequence` drill:
- Build Track A (high-signal, 4-email sequence) and Track B (warm-signal, 3-email sequence) in Instantly
- Configure LinkedIn touch layer for Track A candidates
- Set up the n8n workflow that listens for positive replies and auto-updates Attio

Load all champion candidates from the Smoke test into the appropriate track. Also configure the profiling drill to auto-trigger when new deals hit Connected:
- Create an Attio automation: when deal stage = "Connected", fire a webhook to n8n
- n8n workflow: receive webhook → run champion profiling for the deal's company → push candidates to Instantly sequences

**Human action required:** Record Loom videos for Track A Email 3. The agent prepares scripts and sets up the Loom recording page with the champion's company logo. The founder records a personalized 60-90 second video per Hot candidate.

### 4. Deploy Enablement Delivery

Run the `champion-enablement-delivery` drill:
- Configure the Loops 3-email enablement sequence
- Set up the AI enablement kit generator (Claude generates personalized business case, internal email draft, objection responses, talking points)
- Connect Loom analytics tracking so champion video views are logged

When a candidate's status changes to "Recruited" in Attio, the n8n workflow auto-triggers:
1. Generate the personalized enablement kit via Claude
2. Store the kit in Attio notes
3. Enroll the champion in the Loops enablement sequence
4. Notify the founder to record the Loom walkthrough video

### 5. Monitor and Iterate for 2 Weeks

Check daily:
- New candidates identified (should be 3-5 per new Connected deal)
- Recruitment reply rates (target >=15% positive)
- Enablement open rates (target >=50%)
- Any Loom videos forwarded (strong advocacy signal)

Adjust mid-flight if needed:
- If reply rate <10% after 50 sends: revise email copy, test different signal references
- If enablement open rate <30%: test different subject lines or switch to LinkedIn delivery
- If no champions are forwarding materials: simplify the kit (shorter docs, shorter video)

### 6. Evaluate Against Threshold

After 2 weeks, measure:
- Champion rate: % of active deals with at least 1 recruited champion (target >=60%)
- Win rate comparison: close rate of champion deals vs non-champion deals (target >=35% lift)
- If both pass: proceed to Scalable
- If champion rate passes but win rate doesn't: champions are being recruited but not converting to advocates — focus on enablement quality
- If champion rate fails: profiling or recruitment is the bottleneck — review candidate selection criteria and outreach messaging

## Time Estimate

- 4 hours: CRM tracking setup (one-time)
- 3 hours: PostHog event configuration
- 4 hours: Recruitment sequence build in Instantly + n8n automation
- 3 hours: Enablement sequence build in Loops + Claude integration
- 4 hours: Loom video recording (~15 min per champion, estimated 10-15 champions over 2 weeks)
- 2 hours: Daily monitoring and mid-flight adjustments (15 min/day x 14 days)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — champion tracking, automations | Free (3 users) or $29/user/mo — [attio.com/pricing](https://attio.com/pricing) |
| Clay | Enrichment — champion signal search | $185/mo (Launch) — [clay.com/pricing](https://www.clay.com/pricing) |
| Instantly | Cold email — recruitment sequences | $47/mo (Growth, 5K emails) — [instantly.ai/pricing](https://instantly.ai/pricing) |
| Loom | Video — personalized walkthrough videos | Free (25 videos) or $12.50/mo (Business) — [loom.com/pricing](https://www.loom.com/pricing) |
| Loops | Email — enablement drip sequences | Free tier available — [loops.so/pricing](https://loops.so/pricing) |
| PostHog | Analytics — event tracking | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Automation — workflow orchestration | Self-hosted free or $24/mo (Starter) — [n8n.io/pricing](https://n8n.io/pricing) |

**Estimated play-specific cost this level:** ~$50-250/mo depending on which tools are already in the stack. Incremental cost is primarily Instantly ($47/mo) and Loom ($12.50/mo) if not already provisioned.

## Drills Referenced

- `champion-recruitment-sequence` — multi-channel outreach to convert champion candidates into recruited advocates
- `champion-enablement-delivery` — deliver personalized selling materials to recruited champions
- `posthog-gtm-events` — configure PostHog event tracking for the champion program
