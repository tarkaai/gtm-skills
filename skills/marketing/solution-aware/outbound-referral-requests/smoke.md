---
name: outbound-referral-requests-smoke
description: >
  Outbound Referral Requests — Smoke Test. Manually map your network to 15 target
  accounts, craft personalized referral asks, and send them to test whether your
  existing relationships can generate warm introductions to solution-aware prospects.
stage: "Marketing > SolutionAware"
motion: "OutboundFounderLed"
channels: "Email, Direct"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=3 warm intros from 15 referral requests in 2 weeks"
kpis: ["Request-to-intro rate", "Days from ask to intro", "Intro-to-meeting conversion"]
slug: "outbound-referral-requests"
install: "npx gtm-skills add marketing/solution-aware/outbound-referral-requests"
drills:
  - referral-network-mapping
  - referral-ask-copywriting
  - threshold-engine
---

# Outbound Referral Requests — Smoke Test

> **Stage:** Marketing > SolutionAware | **Motion:** OutboundFounderLed | **Channels:** Email, Direct

## Outcomes

Prove that your existing network (customers, advisors, investors, peers) can generate warm introductions to specific target accounts. After 2 weeks, at least 3 of 15 referral requests should result in an actual introduction being made. This validates that you have sufficient relationship capital and that your ask approach works before investing in automation.

## Leading Indicators

- Referral map completed within first 2 days: 15 target accounts matched to at least 1 connector each with composite score >=20
- First referral ask sent within 3 days of starting the play
- At least 5 connectors respond to the ask (positive or negative) within the first week — indicates your network is engaged
- At least 1 connector forwards the blurb within 48 hours of receiving the ask — indicates the ask is frictionless
- The introduced prospect replies to the intro email within 3 days — indicates the blurb is compelling

## Instructions

### 1. Select 15 target accounts

Identify 15 companies where a warm introduction would meaningfully increase your chance of starting a conversation. These should be solution-aware prospects: companies that know they have the problem you solve and are actively evaluating options, but you have no existing relationship with the buyer.

Pull from your existing pipeline in Attio or manually select accounts. For each target, identify the specific person you want to reach (VP Engineering, Head of Product, CTO — whatever matches your buyer persona). Log all 15 in Attio as a list called "Referral Targets — Smoke."

Estimated time: 30 minutes.

### 2. Map your network to targets

Run the `referral-network-mapping` drill manually. For each of the 15 targets:

1. Export your Attio contacts (customers, advisors, investors, peers, former colleagues)
2. For each target, manually check LinkedIn for mutual connections between your network and the target contact
3. Score each connector-target pair: Intro Likelihood (1-10) based on relationship evidence, and Connector Willingness (1-5) based on your relationship strength
4. Compute composite score (Intro Likelihood x Connector Willingness, max 50)
5. For each target, select the highest-scoring connector as the primary intro path

At Smoke level, this is manual — you are checking LinkedIn and your memory. No Clay enrichment needed. The goal is to prove the concept, not automate it.

If any targets have no viable intro path (all composite scores below 10), replace them with targets where you do have a connector. You need 15 viable pairs to test the play.

Estimated time: 2 hours.

### 3. Craft personalized referral asks

Run the `referral-ask-copywriting` drill for all 15 pairs. For each connector-target pair, generate:

1. **The ask message** (sent to the connector): Maximum 100 words. Reference your specific relationship with the connector. State what value you offer the target (not a pitch). Include an explicit opt-out. Choose email or LinkedIn DM based on where you normally communicate with this connector.

2. **The forwardable blurb** (for the connector to send to the target): Maximum 60 words. Sounds like the connector wrote it, not you. Tailored to the target's company and role. Ends with a soft CTA.

At Smoke level, use Claude to draft these, then manually review each one. Verify that relationship references are accurate (the agent may hallucinate how you know the connector). Verify the blurb is genuinely easy to forward.

Estimated time: 1.5 hours (including review).

### 4. Send all 15 referral asks

Send the asks over 3-5 days (3-5 per day). Do not batch-send all 15 at once — space them so you can respond promptly when intros come in.

For each ask:
- Send via the connector's preferred channel (email or LinkedIn DM)
- Log in Attio: date sent, channel, ask variant, connector name, target company
- Set a reminder for 7 days: follow up if no response

**Human action required:** You must send these personally. At Smoke level, the asks come from the founder, not an automation tool. The connector needs to see your name, not a system email.

Estimated time: 1 hour (spread over 3-5 days).

### 5. Follow up on non-responses

After 7 days, for any connector who has not responded:

Send one gentle follow-up: "Just floating this back up — totally understand if the timing is not right. Let me know either way." Do NOT send more than one follow-up. If they do not respond after the follow-up, mark the pair as "No Response" and move on.

Update Attio with the follow-up date and outcome.

Estimated time: 20 minutes.

### 6. Handle introductions

When an intro is made:
- Respond within 2 hours. Speed signals respect for both the connector and the target.
- Thank the connector immediately (same channel).
- Reply to the target with context from the blurb. Open with the shared connection, not a pitch.
- Log in Attio: intro received date, response time, target's reply status
- Track whether the intro leads to a meeting booked

Estimated time: 30 minutes per intro received.

### 7. Evaluate against threshold

Run the `threshold-engine` drill after 2 weeks. Measure against: >=3 warm intros from 15 referral requests.

Also assess:
- **Request-to-intro rate**: What percentage of asks resulted in intros? Target: >=20%.
- **Average days from ask to intro**: How fast do connectors act? Target: <7 days.
- **Intro-to-meeting rate**: What percentage of intros led to a meeting booked? (Not part of pass threshold at Smoke, but important signal.)
- **Connector willingness calibration**: Were your willingness scores accurate? Did high-willingness connectors actually act?
- **Blurb effectiveness**: Did connectors forward the blurb as-is, modify it, or write their own?

If PASS (>=3 intros), proceed to Baseline. Document which ask styles, connector types, and blurb formats worked best.

If FAIL, diagnose: Were your composite scores inaccurate? Were the asks too long or too vague? Did connectors not see the messages? Did they decline? Adjust and re-run.

Estimated time: 30 minutes.

## Time Estimate

- Target account selection: 30 minutes
- Network mapping (manual): 2 hours
- Ask copywriting and review: 1.5 hours
- Sending asks (spread over 3-5 days): 1 hour
- Follow-ups: 20 minutes
- Handling intros (estimated 3-5): 30 minutes
- Threshold evaluation: 30 minutes

**Total: ~6 hours over 1-2 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — connector records, target accounts, intro tracking, referral map list | Standard stack (excluded from play budget) |
| PostHog | Event tracking (optional at Smoke — manual logging is sufficient) | Standard stack (excluded from play budget) |
| LinkedIn | Mutual connection lookup, DM channel for asks | Free (organic features) |

**Play-specific cost: Free**

## Drills Referenced

- `referral-network-mapping` — maps your existing network to target accounts, scores each connector-target pair by intro likelihood and willingness
- `referral-ask-copywriting` — generates personalized ask messages and forwardable blurbs for each connector-target pair
- `threshold-engine` — evaluates results against the pass/fail threshold and recommends next action
