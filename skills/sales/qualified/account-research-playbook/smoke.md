---
name: account-research-playbook-smoke
description: >
  Account Research & Intelligence — Smoke Test. Research 10 target accounts manually
  using Clay enrichment and web signals, generate personalization hooks, execute
  outreach, and measure whether deep research produces higher reply rates than
  generic outreach.
stage: "Sales > Qualified"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: ">=8 accounts researched and >=30% reply rate from personalized outreach within 1 week"
kpis: ["Reply rate (researched vs non-researched)", "Research time per account", "Personalization hook effectiveness"]
slug: "account-research-playbook"
install: "npx gtm-skills add sales/qualified/account-research-playbook"
drills:
  - account-outreach-research
  - icp-definition
  - build-prospect-list
  - threshold-engine
---

# Account Research & Intelligence — Smoke Test

> **Stage:** Sales > Qualified | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Research at least 8 target accounts with structured briefs containing 2-3 personalization hooks each. Send personalized outreach referencing specific research findings. Achieve a reply rate of >=30% from researched outreach within 1 week, demonstrating that deep account research measurably improves engagement over generic outreach.

## Leading Indicators

- Research briefs produced with at least 2 specific personalization hooks per account
- Outreach messages reference concrete signals (funding, hires, tech stack) rather than generic value propositions
- Recipients reference the personalization in their replies ("thanks for noticing our Series B")
- Researched accounts reply faster (within 24-48 hours vs 5+ days for generic)

## Instructions

### 1. Define your ICP

Run the `icp-definition` drill. Document your firmographic criteria (company size, industry, funding stage), buyer personas (titles, departments), and top 3 pain points your product solves. This ICP drives which accounts you select for research and what signals you look for.

### 2. Build a target list of 10 accounts

Run the `build-prospect-list` drill. Source 10 target accounts matching your ICP from Clay and Apollo. Select accounts where you have no prior relationship (cold outreach). Export to Attio with primary contact for each account.

Also select 10 comparison accounts matching the same ICP criteria. These will receive generic (non-researched) outreach as the control group.

### 3. Research each target account

Run the `account-outreach-research` drill for each of the 10 target accounts. For each account, the drill:

1. Pulls firmographics from Clay (company size, funding, industry)
2. Searches for news signals from the last 90 days (funding, hires, launches)
3. Detects technology stack and classifies as complementary/competing/neutral
4. Identifies 3-5 key contacts matching your buyer personas
5. Generates 2-3 ranked personalization hooks with suggested email first lines
6. Stores the complete brief in Attio as a note on the company record

Track time spent per account. Target: 15-20 minutes per account for thorough research.

### 4. Craft personalized outreach

For each researched account, write outreach using the personalization hooks from the brief:

- **Email first line**: Use the top-ranked hook's suggested first line. Example: "Saw {Company} just closed your Series B with {Investor} — as you scale the engineering team, {pain point} becomes critical."
- **Bridge to value**: Connect the signal to your product's value. One sentence.
- **Ask**: One clear call to action (15-minute call, async Loom review, etc.)

For the 10 control accounts, write outreach using your standard template with no account-specific personalization.

**Human action required:** Review each personalized message for accuracy. Verify the research signals are correct. Edit any AI-generated first lines that sound robotic. Send all 20 messages (10 researched, 10 control) within the same 2-day window.

### 5. Log outreach in Attio and PostHog

For each message sent, create a PostHog event:
- `outreach_sent` with properties: `company_domain`, `channel`, `hook_type` (funding/hire/tech/news/none), `research_depth` (manual/none), `personalized` (true/false)

When replies arrive, log:
- `outreach_replied` with properties: `company_domain`, `channel`, `hook_type`, `sentiment` (positive/neutral/negative), `research_depth`

When meetings are booked, log:
- `meeting_booked` with properties: `company_domain`, `hook_type`, `research_depth`, `days_from_first_touch`

### 6. Evaluate against threshold

Run the `threshold-engine` drill after 1 week. Compare:

| Metric | Researched (10) | Control (10) |
|--------|----------------|--------------|
| Reply rate | Target: >=30% | Baseline comparison |
| Positive reply rate | Track | Track |
| Meeting rate | Track | Track |

**PASS criteria:** >=8 accounts researched AND >=30% reply rate from personalized outreach.

If PASS: Research demonstrably improves outreach. Proceed to Baseline to scale research with automation.

If FAIL: Diagnose — was the issue research quality (hooks were generic), research accuracy (signals were wrong), messaging (good hooks but bad copy), or targeting (wrong ICP)?

## Time Estimate

- ICP definition: 1 hour
- List building: 1 hour
- Account research (10 accounts x 20 min): 3.5 hours
- Outreach crafting (20 messages): 1.5 hours
- Tracking and evaluation: 1 hour
- **Total: ~8 hours over 1 week**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Company enrichment, Claygent research, tech stack detection | Free tier: 100 credits/month. Launch: $185/month ([clay.com/pricing](https://www.clay.com/pricing)) |
| Attio | CRM — store briefs, log outreach, track deals | Free tier available. Plus: $34/user/month ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Event tracking — reply rates, research effectiveness | Free tier: 1M events/month ([posthog.com/pricing](https://posthog.com/pricing)) |
| LinkedIn | Manual contact research | Free LinkedIn or Sales Navigator Core: $99.99/month ([linkedin.com/sales/pricing](https://business.linkedin.com/sales-solutions/compare-plans)) |

**Estimated play-specific cost: Free** (Clay free tier sufficient for 10 accounts)

## Drills Referenced

- `account-outreach-research` — manual account research producing structured brief with personalization hooks
- `icp-definition` — define firmographic criteria, buyer personas, and pain points
- `build-prospect-list` — source and qualify 10 target accounts from Clay/Apollo
- `threshold-engine` — evaluate reply rate against >=30% pass threshold
