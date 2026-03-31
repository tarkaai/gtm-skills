---
name: change-management-objection-scalable
description: >
    Change Management Objection Handling — Scalable Automation. Overcome resistance to changing from
  current solution by quantifying switching costs vs ongoing pain costs, and providing comprehensive
  change support to reduce adoption risk.
stage: "Sales > Connected"
motion: "Outbound Founder-Led"
channels: "Direct"
level: "Scalable Automation"
time: "59 hours over 2 months"
outcome: "Change objections handled systematically at scale over 2 months with improved resolution and adoption rates"
kpis: ["Objection resolution rate", "Status quo overcome rate", "Deal progression rate", "Post-sale adoption rate", "Implementation success"]
slug: "change-management-objection"
install: "npx gtm-skills add sales/connected/change-management-objection"
drills:
  - follow-up-automation
  - tool-sync-workflow
  - ab-test-orchestrator
---
# Change Management Objection Handling — Scalable Automation

> **Stage:** Sales → Connected | **Motion:** Outbound Founder-Led | **Channels:** Direct

## Overview
Change Management Objection Handling — Scalable Automation. Overcome resistance to changing from current solution by quantifying switching costs vs ongoing pain costs, and providing comprehensive change support to reduce adoption risk.

**Time commitment:** 59 hours over 2 months
**Pass threshold:** Change objections handled systematically at scale over 2 months with improved resolution and adoption rates

---

## Budget

**Play-specific tools & costs**
- **Tool and automation costs:** ~$100-500/mo at scale

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Build automated follow-up workflows
Run the `follow-up-automation` drill to create n8n workflows that: (a) detect when a prospect opens an email but doesn't reply, and trigger a follow-up sequence, (b) detect when a LinkedIn connection is accepted, and trigger a personalized message, (c) route positive replies to Attio and notify the founder via Slack.

### 2. Connect your tool stack
Run the `tool-sync-workflow` drill to build n8n sync workflows connecting Instantly replies to Attio deals, LinkedIn activity to Attio contact records, and PostHog events to Attio properties. Ensure no data is siloed.

### 3. Launch A/B testing
Run the `ab-test-orchestrator` drill. Set up experiments on: email subject lines, email body copy, LinkedIn message templates, send timing (day of week, time of day). Use PostHog feature flags to randomly assign variants. Run each test for a minimum of 100 sends per variant before declaring a winner.

### 4. Scale volume
Increase prospect volume to 200-500 per month. Use the automated workflows to handle follow-ups without manual intervention. Monitor the n8n execution logs for errors.

### 5. Evaluate against threshold
Measure against: Change objections handled systematically at scale over 2 months with improved resolution and adoption rates. Review A/B test results to identify winning variants. If PASS, proceed to Durable. If FAIL, focus on the lowest-performing stage in the funnel and run targeted experiments.

---

## KPIs to track
- Objection resolution rate
- Status quo overcome rate
- Deal progression rate
- Post-sale adoption rate
- Implementation success

---

## Pass threshold
**Change objections handled systematically at scale over 2 months with improved resolution and adoption rates**

If you hit this threshold, move to the **Durable Intelligence** level.
If not, iterate on your approach and re-run this level.

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add sales/connected/change-management-objection`_
