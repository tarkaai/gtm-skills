---
name: champion-driven-outbound-scalable
description: >
  Champion-driven Outbound — Scalable Automation. Scale to 150 accounts/month with automated
  champion health monitoring, multi-threaded account coverage, A/B-tested recruitment sequences,
  and self-healing follow-up workflows that re-engage disengaged champions.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email, Social, Direct"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: "≥3% account conversion at 150 accounts/month over 4 months"
kpis: ["Monthly account volume", "Account-to-meeting conversion rate", "Champion pipeline velocity", "Automation coverage rate", "Cost per champion-facilitated meeting"]
slug: "champion-driven-outbound"
install: "npx gtm-skills add marketing/solution-aware/champion-driven-outbound"
drills:
  - dashboard-builder
  - follow-up-automation
  - ab-test-orchestrator
---
# Champion-driven Outbound — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email, Social, Direct

## Overview
Find the 10x multiplier. Automate the full champion lifecycle — profiling, recruitment, enablement, and health monitoring — to sustain 150 accounts/month without proportional effort. The agent handles the volume; the founder handles only high-signal champion conversations.

**Time commitment:** 75 hours over 3 months
**Pass threshold:** ≥3% account conversion at 150 accounts/month over 4 months

---

## Budget

**Play-specific tools & costs**
- **Instantly:** scaled email sequences — $77/mo (Hypergrowth plan, https://instantly.ai/pricing)
- **Clay:** continuous enrichment and signal monitoring — $349/mo (Team, https://clay.com/pricing)
- **LinkedIn Sales Navigator:** advanced search and lead tracking — $99/mo (Core)
- **Loops:** enablement drip sequences — $49/mo (Starter, https://loops.so/pricing)
- **Loom:** personalized video at scale — $12.50/user/mo (Business, https://loom.com/pricing)

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

**Estimated monthly cost:** ~$590/mo

---

## Instructions

### 1. Deploy champion health monitoring
Run the `dashboard-builder` drill. This creates an always-on system that:
- Runs daily health checks for all active and recruited champions
- Scores each champion on a composite engagement metric (email opens, replies, material forwards, meeting activity)
- Detects disengagement early: if a champion's score drops >15 points or they go dark for 14+ days, the system alerts via Slack and creates re-engagement tasks in Attio
- When a champion goes dark for 21+ days, automatically triggers `champion-profiling` to find a replacement at the same account
- Produces a weekly Champion Health Digest posted to Slack

Configure the health check n8n workflow with the champion events defined during Baseline. The drill sets up the PostHog dashboard panels: champion health distribution, score trends, deals-without-champions, recruitment funnel, and at-risk alert volume.

### 2. Build self-healing follow-up automation
Run the `follow-up-automation` drill, configured specifically for the champion pathway:

**Workflow 1 — Recruitment follow-up:**
n8n detects when a champion candidate opens a recruitment email but does not reply within 48 hours. Trigger: send a follow-up via a different channel (if email → LinkedIn DM, if LinkedIn → email). Log the cross-channel touch in Attio.

**Workflow 2 — Enablement re-engagement:**
n8n detects when a recruited champion does not open the enablement kit within 5 days of delivery. Trigger: resend via a different subject line. If still no open after 3 days, switch to a LinkedIn DM with a direct link to the Loom video.

**Workflow 3 — Champion revival:**
n8n detects when a champion's status changes from Active to At Risk (from the health monitoring drill). Trigger: send a personalized check-in email asking "How did the conversation go internally? Any concerns I can help address?" Log the re-engagement attempt.

**Workflow 4 — Positive reply routing:**
n8n detects positive sentiment in email replies (via Instantly webhook + Claude sentiment classification). Trigger: update Attio champion status, notify the founder via Slack with the reply text and recommended next action, and create a task in Attio.

### 3. Launch A/B testing on the champion funnel
Run the `ab-test-orchestrator` drill. Set up experiments on the champion-specific variables that matter most:

**Experiment 1 — Recruitment message framing:**
- Control: signal-reference opening ("Saw your post about X")
- Variant: problem-quantification opening ("Companies like {company} typically lose $X/year to {problem}")
- Metric: reply rate. Minimum 100 sends per variant.

**Experiment 2 — Enablement kit format:**
- Control: text-based enablement kit (email + PDF)
- Variant: Loom video walkthrough of the business case (no PDF)
- Metric: champion forward rate. Minimum 30 kits per variant.

**Experiment 3 — Recruitment cadence timing:**
- Control: 4-touch sequence over 14 days
- Variant: 3-touch sequence over 7 days (faster cadence, one fewer touch)
- Metric: days from first contact to recruited status.

Use PostHog feature flags to randomly assign each new champion candidate to experiment variants. Run each experiment until statistical significance (p < 0.05) or 4 weeks, whichever is longer.

### 4. Scale to 150 accounts/month
Increase the monthly account intake to 150. The automation handles:
- **Profiling:** Clay runs weekly scheduled enrichment against a growing account list, pushing new champion candidates to Attio automatically
- **Recruitment:** Instantly sequences launch automatically when new candidates appear in Attio (via n8n webhook on `champion_status: Candidate`)
- **Enablement:** Loops sequences trigger automatically when status changes to Recruited
- **Health monitoring:** Daily checks run for all champions regardless of volume

The founder's weekly time commitment should be:
- 1 hour: review Champion Health Digest and act on at-risk alerts
- 1 hour: record Loom videos for top 5 highest-scoring new candidates
- 30 min: review A/B test results and approve next experiments

### 5. Set up guardrails
Configure n8n guardrails:
- If account-to-meeting rate drops below 2% for 2 consecutive weeks (vs 3% target), pause new account intake and diagnose
- If champion recruitment reply rate drops below 5% for 50+ sends, pause the underperforming Instantly campaign and alert founder
- If any single account has >5 champion candidates contacted without a single reply, blacklist the account for 90 days
- Weekly: compare champion-facilitated meeting quality (deal size, close rate) against non-champion outbound. If champion deals are not outperforming, escalate for strategic review.

### 6. Evaluate against threshold
Measure monthly over 4 months: ≥3% account conversion at 150 accounts/month. That means ≥4-5 champion-facilitated meetings per month from the 150-account cohort.

Pull from PostHog:
- Monthly funnel: accounts → profiled → contacted → recruited → enabled → meetings
- Conversion rate trend by month (should be stable or improving)
- A/B test winners and their impact on funnel metrics
- Cost per meeting trend (should be declining as automation coverage increases)
- Champion yield: average meetings facilitated per active champion

If PASS: document the optimized champion playbook (winning variants, best signals, optimal cadence). Proceed to Durable.
If FAIL: identify whether the issue is volume (not enough accounts), quality (wrong ICP), process (automation failures), or market (champion strategy saturating). Fix and re-run.

---

## KPIs to track
- Monthly account volume (target: 150)
- Account-to-meeting conversion rate (target: ≥3%)
- Champion pipeline velocity (days from profiling to meeting)
- Automation coverage rate (% of touchpoints handled without manual intervention)
- Cost per champion-facilitated meeting

---

## Pass threshold
**≥3% account conversion at 150 accounts/month over 4 months**

If you hit this threshold, move to the **Durable Intelligence** level.
If not, iterate on your approach and re-run this level.

---

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Scaled recruitment email sequences | Hypergrowth: $77/mo (https://instantly.ai/pricing) |
| Clay | Continuous enrichment and signal monitoring | Team: $349/mo (https://clay.com/pricing) |
| LinkedIn Sales Nav | Champion candidate search at volume | Core: $99/mo (https://linkedin.com/sales-solutions) |
| Loops | Automated enablement kit delivery | Starter: $49/mo (https://loops.so/pricing) |
| Loom | Personalized recruitment videos | Business: $12.50/user/mo (https://loom.com/pricing) |

**Estimated monthly cost:** ~$590/mo

---

## Drills Referenced
- `dashboard-builder` — daily health checks, disengagement alerts, and replacement champion triggers
- `follow-up-automation` — self-healing workflows that re-engage stalled champions across channels
- `ab-test-orchestrator` — A/B tests on recruitment framing, enablement format, and cadence timing

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/champion-driven-outbound`_
