---
name: account-research-playbook-durable
description: >
    Account Research & Intelligence — Durable Intelligence. Systematically research target accounts
  before outreach to personalize messaging and improve relevance, from manual LinkedIn research to
  AI-driven account intelligence that auto-generates comprehensive account profiles with buying
  signals and talk tracks.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Durable Intelligence"
time: "130 hours over 6 months"
outcome: "Sustained or improving research effectiveness (>=35% reply rate, >=2.5x faster progression) over 6 months via continuous agent-driven signal optimization, real-time intelligence, and personalization generation"
kpis: ["Reply rate trend", "Agent experiment win rate", "Signal prediction accuracy", "Research time efficiency"]
slug: "account-research-playbook"
install: "npx gtm-skills add sales/qualified/account-research-playbook"
drills:
  - dashboard-builder
  - signal-detection
---
# Account Research & Intelligence — Durable Intelligence

> **Stage:** Sales → Qualified | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Overview
Account Research & Intelligence — Durable Intelligence. Systematically research target accounts before outreach to personalize messaging and improve relevance, from manual LinkedIn research to AI-driven account intelligence that auto-generates comprehensive account profiles with buying signals and talk tracks.

**Time commitment:** 130 hours over 6 months
**Pass threshold:** Sustained or improving research effectiveness (>=35% reply rate, >=2.5x faster progression) over 6 months via continuous agent-driven signal optimization, real-time intelligence, and personalization generation

---

## Budget

**Play-specific tools & costs**
- **Ongoing tool costs:** ~$100-500/mo
- **Agent compute costs:** Variable based on monitoring frequency

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Build monitoring dashboards
Run the `dashboard-builder` drill to create a PostHog dashboard for account-research-playbook with panels: weekly send volume, reply rate trend, meeting conversion rate, pipeline value from this play, cost per meeting. Set up alerts for when any metric drops below the Scalable-level baseline by more than 20%.

### 2. Deploy signal-based targeting
Run the `signal-detection` drill to configure Clay to monitor for buying signals: job changes at target accounts, funding announcements, tech stack changes, competitor mentions. Feed these signals into your prospect list automatically via n8n. Prioritize outreach to signal-detected accounts.

### 3. Set up autonomous optimization
Configure n8n workflows to: (a) automatically pause underperforming sequences when reply rates drop below 1% for 3 consecutive days, (b) promote winning A/B test variants and start new experiments, (c) alert the founder when a high-value deal enters the pipeline.

### 4. Run continuous improvement cycles
Monthly: review dashboard trends, retire messaging that has decayed below threshold, test new ICP segments based on won-deal patterns. The agent should generate a monthly report summarizing: what changed, what was tested, what was retired, and recommended next experiments.

### 5. Evaluate sustainability
Measure against: Sustained or improving research effectiveness (>=35% reply rate, >=2.5x faster progression) over 6 months via continuous agent-driven signal optimization, real-time intelligence, and personalization generation. This level runs continuously. If metrics sustain or improve, the play is durable. If metrics decay, diagnose whether the issue is market saturation, message fatigue, or ICP drift.

---

## KPIs to track
- Reply rate trend
- Agent experiment win rate
- Signal prediction accuracy
- Research time efficiency

---

## Pass threshold
**Sustained or improving research effectiveness (>=35% reply rate, >=2.5x faster progression) over 6 months via continuous agent-driven signal optimization, real-time intelligence, and personalization generation**

This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/qualified/account-research-playbook`_
