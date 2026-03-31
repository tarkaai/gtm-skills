---
name: champion-driven-outbound-baseline
description: >
  Champion-driven Outbound — Baseline Run. Scale champion identification to 40 accounts with
  automated recruitment sequences and enablement delivery. First always-on champion pipeline
  with multi-channel outreach and engagement tracking.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email, Social, Direct"
level: "Baseline Run"
time: "18 hours over 3 weeks"
outcome: "≥4% account-to-meeting rate via champion strategy in 40 accounts over 3 weeks"
kpis: ["Account-to-meeting conversion rate", "Champion recruitment rate", "Enablement kit forward rate", "Cost per champion-facilitated meeting"]
slug: "champion-driven-outbound"
install: "npx gtm-skills add marketing/solution-aware/champion-driven-outbound"
drills:
  - posthog-gtm-events
---
# Champion-driven Outbound — Baseline Run

> **Stage:** Marketing → Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email, Social, Direct

## Overview
First always-on champion pipeline. Automate the profiling-to-recruitment flow across 40 accounts using multi-channel sequences. Deliver personalized enablement kits to recruited champions. Validate that champion conversion rates hold at 4x the volume of the Smoke test.

**Time commitment:** 18 hours over 3 weeks
**Pass threshold:** ≥4% account-to-meeting rate via champion strategy in 40 accounts over 3 weeks

---

## Budget

**Play-specific tools & costs**
- **Instantly:** cold email sequences for champion recruitment — $30/mo (Growth plan, https://instantly.ai/pricing)
- **Clay:** enrichment and champion signal search at 40-account scale — $149/mo (Pro, https://clay.com/pricing)
- **LinkedIn Sales Navigator:** advanced people search for champion identification — $99/mo (Core plan)

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Configure champion event tracking
Run the `posthog-gtm-events` drill to set up the champion-specific event taxonomy in PostHog. Create these events:

| Event | Trigger | Properties |
|-------|---------|------------|
| `champion_profiled` | Champion candidate added to Attio | `account_id`, `champion_score`, `signal_type` |
| `champion_contacted` | First outreach sent to candidate | `account_id`, `champion_id`, `channel`, `track` |
| `champion_replied` | Candidate responds to outreach | `account_id`, `champion_id`, `sentiment`, `channel` |
| `champion_recruited` | Status changed to Recruited | `account_id`, `champion_id`, `days_to_recruit` |
| `champion_enabled` | Enablement kit delivered | `account_id`, `champion_id`, `kit_type` |
| `champion_forwarded` | Champion forwarded materials internally | `account_id`, `champion_id`, `asset_forwarded` |
| `champion_meeting_facilitated` | Meeting booked via champion intro | `account_id`, `champion_id`, `meeting_type` |

Connect Attio webhooks to PostHog via n8n so champion status changes automatically fire events.

### 2. Expand account targeting to 40
Using the ICP and champion persona validated in Smoke, build a list of 40 target accounts in Clay. Run the `champion-profiling` drill (from the Smoke level's drills) against all 40 accounts. This produces 100-200 scored champion candidates in Attio.

Segment candidates into Track A (score 75+, signal-led) and Track B (score 50-74, value-led).

### 3. Launch automated recruitment sequences
Run the the champion recruitment sequence workflow (see instructions below) drill. This creates:

**For Track A candidates (signal-led):**
- 4-touch email sequence via Instantly: signal reference → value asset → personalized Loom video → breakup with referral ask
- Parallel LinkedIn touches: connection request (Day 1) → DM with value asset (Day 5) → content engagement (Day 10)

**For Track B candidates (value-led):**
- 3-touch email sequence via Instantly: problem education → peer proof case study → direct ask
- LinkedIn connect only, no DM unless they accept and engage

The drill configures Instantly campaigns, creates Loom video scripts, and sets up n8n tracking workflows.

**Human action required:** Record personalized Loom videos for Track A candidates scoring 85+. The agent prepares the script and talking points. Aim for 60-90 seconds per video.

### 4. Enable recruited champions
As champions move to `champion_status: Recruited`, run the the champion enablement delivery workflow (see instructions below) drill. For each recruited champion, the drill:
- Generates a personalized enablement kit using Claude (internal email draft, one-page business case, objection responses, talking points)
- Sets up a 3-email drip via Loops delivering the kit over 5 days
- Tracks engagement: email opens, Loom views, material forwards

Monitor the enablement engagement data. Champions who forward materials to colleagues (visible via Loom multi-viewer tracking) are the strongest advocates — flag them as priority in Attio.

### 5. Monitor and adjust mid-flight
Check daily during the 3-week run:
- **Reply rate by track:** if Track A reply rate falls below 10% after 20 sends, refresh the signal-reference copy or switch to different signals
- **Recruitment-to-enablement conversion:** if champions are replying positively but not engaging with enablement kits, the kit content may not match their actual pain — adjust the Claude prompt
- **Enablement-to-meeting conversion:** if champions engage with kits but do not facilitate introductions, add a direct ask in the Day 5 check-in email

Log all adjustments as Attio notes on the campaign record.

### 6. Evaluate against threshold
Measure: ≥4% account-to-meeting rate via champion strategy in 40 accounts over 3 weeks. That means ≥2 champion-facilitated meetings from the 40-account cohort.

Pull data from PostHog:
- Full funnel: accounts targeted → champions profiled → contacted → replied → recruited → enabled → meetings facilitated
- Conversion rate at each stage
- Average days from first contact to meeting
- Cost per champion-facilitated meeting (tool costs / meetings)

If PASS: document the winning recruitment track (A vs B), enablement kit engagement patterns, and top-performing champion signals. Proceed to Scalable.
If FAIL: identify the funnel bottleneck. Is it profiling (not finding good candidates), recruitment (low reply rates), enablement (champions not advocating), or conversion (advocacy not producing meetings)? Fix the weakest stage and re-run.

---

## KPIs to track
- Account-to-meeting conversion rate
- Champion recruitment rate (recruited / contacted)
- Enablement kit forward rate (forwards / kits delivered)
- Cost per champion-facilitated meeting

---

## Pass threshold
**≥4% account-to-meeting rate via champion strategy in 40 accounts over 3 weeks**

If you hit this threshold, move to the **Scalable Automation** level.
If not, iterate on your approach and re-run this level.

---

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Champion recruitment email sequences | Growth: $30/mo (https://instantly.ai/pricing) |
| Clay | Champion enrichment and signal search | Pro: $149/mo (https://clay.com/pricing) |
| LinkedIn Sales Nav | Advanced champion candidate search | Core: $99/mo (https://linkedin.com/sales-solutions) |
| Loops | Enablement kit drip sequences | Starter: $49/mo (https://loops.so/pricing) |
| Loom | Personalized recruitment videos | Business: $12.50/user/mo (https://loom.com/pricing) |

**Estimated monthly cost:** ~$340/mo

---

## Drills Referenced
- the champion recruitment sequence workflow (see instructions below) — multi-channel outreach sequence to convert champion candidates into active advocates
- the champion enablement delivery workflow (see instructions below) — delivers personalized internal selling materials to recruited champions
- `posthog-gtm-events` — configures champion-specific event tracking in PostHog

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/champion-driven-outbound`_
