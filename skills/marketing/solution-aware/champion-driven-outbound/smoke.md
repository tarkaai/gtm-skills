---
name: champion-driven-outbound-smoke
description: >
  Champion-driven Outbound — Smoke Test. Identify potential champions at 10 target accounts using
  enrichment signals, manually recruit the top candidates, and validate that champion-facilitated
  introductions produce higher-quality meetings than cold outbound alone.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email, Social, Direct"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥2 champion-facilitated meetings from 10 target accounts in 2 weeks"
kpis: ["Champion identification rate", "Recruitment reply rate", "Champion-facilitated meeting rate"]
slug: "champion-driven-outbound"
install: "npx gtm-skills add marketing/solution-aware/champion-driven-outbound"
drills:
  - icp-definition
  - champion-profiling
  - threshold-engine
---
# Champion-driven Outbound — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email, Social, Direct

## Overview
Validate that champion-based account entry produces meetings. The agent identifies champion candidates at 10 accounts using Clay enrichment. The founder manually recruits the best candidates and tests whether champion-facilitated introductions outperform cold approaches.

**Time commitment:** 6 hours over 1 week
**Pass threshold:** ≥2 champion-facilitated meetings from 10 target accounts in 2 weeks

---

## Budget

**Play-specific cost:** Free (uses Clay free tier or existing credits)

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

---

## Instructions

### 1. Define ICP and champion persona
Run the `icp-definition` drill. In addition to the standard ICP firmographics, define your champion persona:
- **Champion title patterns:** titles one level below the economic buyer in the department that uses your product (e.g., "Head of Engineering" if the buyer is VP Engineering, "Senior PM" if buyer is Head of Product)
- **Champion department:** the team that feels the pain your product solves
- **Champion seniority band:** Manager to Director level — senior enough to have credibility, junior enough to feel the pain daily
- **Champion tenure range:** 6 months to 3 years at current company — long enough to have influence, recent enough to still want to prove themselves

Document the champion persona in Attio as a note on your ICP record.

### 2. Select 10 target accounts
From your existing Attio pipeline or a Clay table, select 10 accounts that match your ICP. Prioritize accounts where you have zero existing contacts — this tests whether champion identification alone can open a door. Tag these accounts in Attio with `play: champion-driven-outbound` and `play_level: smoke`.

### 3. Profile champion candidates
Run the `champion-profiling` drill against the 10 accounts. For each account, the drill will:
- Search Clay for 3-5 contacts matching your champion persona
- Enrich with behavioral signals (public posts about pain points, competitor engagement, job changes)
- Score and rank candidates
- Push the top candidates to Attio with `champion_status: Candidate`

Review the output. You should have 2-5 scored candidates per account (20-50 total). Filter to Hot (75+) and Warm (50-74) candidates.

### 4. Manually recruit top champions
For each account, select the single highest-scoring champion candidate. Write a personalized outreach message that references their specific behavioral signal.

**Human action required:** Send the outreach manually. For Hot candidates, send a LinkedIn connection request with a signal-referencing note AND an email. For Warm candidates, email only. Log every touchpoint in Attio:
- Set `champion_outreach_date` to today
- Set `champion_outreach_channel` to the channel used
- Add a note with the exact message sent

The message should follow this structure:
1. Reference their specific signal (e.g., "Saw your post about X" or "Congrats on the new role")
2. Share one genuinely useful insight related to that signal
3. Ask a low-commitment question — NOT a meeting request

### 5. Track responses and facilitate meetings
Monitor responses over 10 days. For each response:
- Log the response in Attio (update `champion_status` based on reply sentiment)
- Positive reply: respond with a value asset (ROI calculator, case study, benchmark data). Ask if they would be open to a brief call, or if they could introduce you to the person who owns the budget
- Referral: add the referred person to Attio, link to the champion, and reach out referencing the introduction
- Negative/no response: set `champion_status: Disengaged`

For champions who agree to facilitate an introduction, log the meeting in Attio with `meeting_source: champion-facilitated`.

### 6. Evaluate against threshold
Run the `threshold-engine` drill to measure:
- **Primary metric:** ≥2 champion-facilitated meetings from 10 target accounts in 2 weeks
- **Secondary metrics:** champion identification rate (candidates found per account), recruitment reply rate, and time from first touch to meeting

If PASS: document which champion signals correlated with successful recruitment. Proceed to Baseline.
If FAIL: diagnose whether the issue was (a) poor champion identification (wrong profiles), (b) weak recruitment messaging (low reply rate), or (c) champions replied but did not facilitate intros (enablement gap). Adjust and re-run.

---

## KPIs to track
- Champion identification rate (scored candidates per account)
- Recruitment reply rate (replies / outreach sent)
- Champion-facilitated meeting rate (meetings / accounts targeted)

---

## Pass threshold
**≥2 champion-facilitated meetings from 10 target accounts in 2 weeks**

If you hit this threshold, move to the **Baseline Run** level.
If not, iterate on your champion persona, signal criteria, or recruitment messaging and re-run.

---

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Champion enrichment and signal search | Free tier: 100 credits/mo. Pro: $149/mo (https://clay.com/pricing) |
| Attio | CRM for champion tracking and deal linkage | Free tier for <3 users. Plus: $34/user/mo (https://attio.com/pricing) |
| LinkedIn | Manual connection requests and DMs | Free (Sales Navigator optional at this level) |

---

## Drills Referenced
- `icp-definition` — defines ICP firmographics and champion persona criteria
- `champion-profiling` — identifies, enriches, scores, and ranks champion candidates at target accounts
- `threshold-engine` — evaluates play results against pass/fail threshold

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{crm}}`) and automation platform (`{{automation}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `npx gtm-skills add marketing/solution-aware/champion-driven-outbound`_
