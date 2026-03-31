---
name: intent-signal-tracking-smoke
description: >
  Intent Signal Tracking — Smoke Test. Manually identify and act on buying intent signals from
  website visitors, G2 research, job changes, and funding events. Validate that intent-based
  outreach produces measurably higher reply rates than cold outreach.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Product, Email, Website"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=5 high-intent accounts identified and >=30% reply rate from intent-based outreach vs <=15% from cold outreach in 1 week"
kpis: ["Intent signals captured per day", "Reply rate (intent vs cold)", "Time from signal to outreach"]
slug: "intent-signal-tracking"
install: "npx gtm-skills add sales/qualified/intent-signal-tracking"
drills:
  - signal-detection
  - intent-score-model
  - threshold-engine
---

# Intent Signal Tracking — Smoke Test

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Product, Email, Website

## Outcomes

Prove that outreach triggered by intent signals produces a measurably higher reply rate than equivalent cold outreach. Identify at least 5 high-intent accounts from signals you can actually capture today. This is a manual, one-week test — no automation, no budget.

## Leading Indicators

- Intent signals are appearing daily from at least one source (website analytics, G2, LinkedIn alerts)
- You can distinguish high-intent from low-intent accounts based on signal strength
- Reply rate on intent-based outreach is trending above 25% within the first 3 days
- Time from signal detection to first outreach is under 4 hours

## Instructions

### 1. Set up manual signal capture

You do not need paid tools for Smoke. Set up free signal sources:

- **Website:** Open PostHog and review identified visitors who viewed your pricing page, case studies, or demo page in the last 7 days. If PostHog identifies companies (via reverse-IP or logged-in users), note them.
- **G2:** If you have a G2 vendor profile, check my.g2.com for buyer intent signals (available free with basic profiles). Note companies browsing your category or comparing alternatives.
- **LinkedIn:** Set Google Alerts for your company name and competitor names. Monitor LinkedIn for prospects posting about problems your product solves.
- **Job boards:** Check if target accounts are hiring for roles that suggest they need your product (e.g., if you sell dev tools, look for "DevOps Engineer" postings at target companies).

Log every signal in a spreadsheet or Attio: company name, signal type, signal source, date detected, signal strength (high/medium/low).

### 2. Build a quick scoring model

Run the `signal-detection` drill to define which signals matter most for your ICP. Then run the `intent-score-model` drill in manual mode: assign rough point values to each signal type. You do not need Clay for Smoke — use a spreadsheet formula.

Suggested starting weights:
- Pricing page visit: 15 points
- G2 alternatives/compare signal: 20 points
- Multiple site visits: 5 points per visit (max 25)
- New exec hire at target: 5 points
- Active job postings in your domain: 5 points

Score each account. Any account scoring 40+ is "high intent."

### 3. Craft signal-specific outreach

For each high-intent account, write a personalized email that connects to the specific signal you detected. Do NOT reveal you know they visited your site. Instead, reference the underlying need the signal implies.

**Example for a pricing page visitor:**
"I noticed [Company] is scaling its [domain] team — we have been helping similar companies at your stage [solve specific problem]. Would a 15-minute call be useful?"

**Example for a G2 comparison signal:**
"Companies evaluating [category] tools often struggle with [specific pain point]. We built [product] specifically to solve that. Happy to share what makes us different in 15 minutes."

Write 2 variants per signal type. Send to the highest-ranking contact at each account.

**Human action required:** Send each email manually. Do not use an email sequencer — this is a Smoke test. Log every send in your spreadsheet/Attio with timestamp.

### 4. Run a cold control group

To prove intent signals matter, send the same number of outreach emails to accounts with NO detected intent signals but that otherwise match your ICP. Use your best generic cold email template. Log sends and replies identically.

### 5. Measure and evaluate

After 7 days, run the `threshold-engine` drill to evaluate:
- How many high-intent accounts did you identify? (target: >=5)
- What was the reply rate on intent-based outreach? (target: >=30%)
- What was the reply rate on cold outreach? (expected: <=15%)
- What was the average time from signal to outreach?

If intent outreach reply rate is at least 2x cold outreach, the signal is real. Proceed to Baseline.

## Time Estimate

- 1 hour: set up signal sources and spreadsheet
- 1 hour: review signals and score accounts
- 2 hours: write personalized outreach (intent + cold control)
- 1 hour: send outreach manually and log results
- 1 hour: measure, analyze, and document findings

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Website visitor analytics | Free tier (1M events/mo) |
| Attio | CRM for logging signals and outreach | Free tier (3 users) |
| G2 (my.g2.com) | Third-party intent signals | Free with vendor profile |
| Google Alerts | Brand/competitor mention monitoring | Free |
| Spreadsheet | Manual signal scoring | Free |

**Total play-specific cost: $0**

## Drills Referenced

- `signal-detection` — define which intent signals to monitor and how to categorize them
- `intent-score-model` — build the weighted scoring model (manual version for Smoke)
- `threshold-engine` — evaluate results against pass/fail threshold
