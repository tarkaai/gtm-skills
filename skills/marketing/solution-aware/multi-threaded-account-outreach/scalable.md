---
name: multi-threaded-account-outreach-scalable
description: >
  Multi-threaded Outreach — Scalable Automation. Scale to 200 accounts/month with automated
  stakeholder discovery, dynamic thread orchestration, and continuous A/B testing across
  role-specific sequences and channel timing.
stage: "Marketing > Solution Aware"
motion: "Outbound Founder-Led"
channels: "Email, Social, Direct"
level: "Scalable Automation"
time: "75 hours over 3 months"
outcome: "≥2.5% account-to-meeting rate at 200 accounts/month over 3 months"
kpis: ["Account-to-meeting rate at scale", "Multi-thread engagement rate", "Cost per meeting", "Automation throughput", "A/B test velocity"]
slug: "multi-threaded-account-outreach"
install: "npx gtm-skills add marketing/solution-aware/multi-threaded-account-outreach"
drills:
  - stakeholder-org-mapping
  - follow-up-automation
  - ab-test-orchestrator
---

# Multi-threaded Outreach — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** Outbound Founder-Led | **Channels:** Email, Social, Direct

## Outcomes

Scale multi-threaded outreach from 50 to 200 accounts per month without proportional increase in effort. The 10x multiplier comes from three automation layers: (1) automated stakeholder discovery that populates thread maps without manual research, (2) dynamic thread orchestration that handles cross-stakeholder coordination at scale, (3) continuous A/B testing that improves role-specific messaging based on data rather than intuition.

**Pass threshold:** ≥2.5% account-to-meeting rate sustained across 200 accounts/month for 3 consecutive months. Cost per meeting must not exceed 2x the Baseline cost per meeting.

## Leading Indicators

- Stakeholder discovery automation populates ≥3 contacts per account for ≥80% of new accounts within 24 hours
- Automation handles ≥90% of send/pause/escalation decisions without manual intervention
- A/B test cycle time under 14 days (hypothesis to result for 200+ sample tests)
- Email deliverability stays above 97% at the higher volume
- Cross-thread signal rate (accounts with multi-stakeholder engagement) stays within 20% of Baseline level

## Instructions

### 1. Deploy automated stakeholder discovery

Run the `stakeholder-org-mapping` drill to build the always-on stakeholder pipeline. Configure:

**Trigger**: When a new account enters the Attio pipeline tagged `multi-thread-target`, the n8n workflow fires.

**Discovery workflow**:
1. Extract company domain from the Attio deal record
2. Call Clay People Search: filter by seniority (Director+), departments matching your buyer personas
3. Run enrichment waterfall for verified email + LinkedIn URL on each contact
4. Classify each contact using Claude: send title + department + company context, receive stakeholder_role + confidence
5. Write contacts to Attio linked to the deal with role classification and channel assignment
6. Generate the thread map note on the deal (Champion Day 0, Influencer Day 4, Economic Buyer Day 7)

**Quality gate**: If fewer than 3 contacts are found with verified email, flag the account for manual research and do not auto-enroll in sequences.

**Volume target**: Process 50 new accounts per week (200/month). Budget Clay enrichment credits accordingly: ~15 credits per account for people search + waterfall = 3,000 credits/month.

### 2. Build dynamic thread orchestration in n8n

Upgrade the Baseline coordination rules into a full orchestration engine:

**Master workflow**: One n8n workflow per active account that manages all threads. The workflow:
1. Reads the thread map from Attio (which stakeholders, which channels, which timing)
2. Enrolls each contact in the appropriate Instantly campaign (Champion sequence, Economic Buyer sequence, Influencer sequence) on the correct day offset
3. Checks Attio before every scheduled send for:
   - Has any contact at this account responded? (pause rule)
   - Has the deal stage changed? (escalation rule)
   - Has any contact opted out? (suppression rule)
4. Executes escalation logic: if Champion responds positively, immediately queue the Economic Buyer with an updated message variant that references the Champion's interest
5. Logs every decision (send, pause, escalate, suppress) as a PostHog event for attribution

**Scaling approach**: Use n8n's workflow scheduling to process accounts in batches of 25. Run 4 batches per week to handle 200 accounts/month with processing headroom.

**Error handling**: If Clay enrichment fails for an account, retry once after 1 hour. If Instantly returns a bounce on first send to any contact, flag the account's email data quality and re-verify via Clay before continuing.

### 3. Scale Instantly sending infrastructure

At 200 accounts/month with 3 contacts each = 600 contacts = ~2,400 emails/month (4 steps per sequence average).

Configure Instantly for this volume:
- Add 3-5 sending accounts across 2-3 domains
- Each account sends max 40 emails/day
- Rotate sending accounts per campaign to distribute volume
- Maintain warmup on all accounts continuously
- Monitor domain reputation weekly via Instantly's health dashboard

Create separate Instantly campaigns per role AND per message variant (for A/B testing). Naming convention: `MTO-{role}-{variant}-{month}` (e.g., `MTO-champion-v2-apr26`).

### 4. Launch A/B testing across all sequence variables

Run the `ab-test-orchestrator` drill to systematically test the variables that matter most for multi-threaded outreach:

**Priority 1 — Message variants per role (Month 1):**
Test 2 variants of Email 1 for each role. Minimum 100 sends per variant before declaring a winner.
- Champion: test problem-aware opener vs. peer comparison opener
- Economic Buyer: test ROI-first vs. risk-first positioning
- Influencer: test technical depth (architecture) vs. technical breadth (integration landscape)

**Priority 2 — Thread timing (Month 2):**
Test the cross-stakeholder timing sequence:
- Variant A (current): Champion Day 0, Influencer Day 4, Economic Buyer Day 7
- Variant B (compressed): All stakeholders within Day 0-3
- Variant C (reversed): Economic Buyer Day 0, Champion Day 3, Influencer Day 5
Measure: account-to-meeting rate AND cross-thread signal rate for each variant.

**Priority 3 — Channel mix (Month 3):**
Test LinkedIn-first vs. email-first for Champion and Influencer roles:
- Variant A: LinkedIn connection on Day 0, email on Day 2
- Variant B: Email on Day 0, LinkedIn connection on Day 3
Measure: response rate by channel and overall account conversion.

Use PostHog feature flags to assign accounts to test groups. Each account (not contact) is the randomization unit — all contacts at one account get the same timing variant.

### 5. Build automated follow-up workflows

Run the `follow-up-automation` drill to handle engagement signals at scale:

**High-intent follow-up triggers:**
- Contact opened email 3+ times → send a shorter, direct meeting ask 48 hours later
- Contact clicked a link → send deeper content on the clicked topic + meeting ask
- LinkedIn connection accepted → trigger DM sequence with 24-hour delay
- Contact visited your pricing page (PostHog event) → fast-track all threads at that account to meeting-ask step

**Cross-thread escalation triggers:**
- 2+ contacts at same account engaged in same week → send a "your team is exploring this" message to the Economic Buyer
- Champion books a meeting → pause all other threads at that account, update CRM deal stage

**Safety guardrails:**
- Max 8 total touches per contact across all channels
- Max 15 touches per account across all contacts
- If 3+ contacts at an account reply negatively, suppress the entire account permanently
- Never send automated follow-up within 4 hours of a manual touchpoint logged in Attio

### 6. Monitor at scale with weekly reviews

Build a PostHog dashboard for the Scalable level:

**Volume panel**: Accounts processed this month, contacts enrolled, emails sent, LinkedIn connections sent
**Conversion funnel**: Accounts targeted → accounts with engagement → accounts with multi-stakeholder engagement → meetings → deals
**Per-role performance**: Reply rate, meeting rate, and sentiment by stakeholder role (Champion, Economic Buyer, Influencer)
**A/B test status**: Active experiments, sample sizes, projected completion dates
**Health metrics**: Deliverability rate, LinkedIn restriction warnings, bounce rate, negative reply rate

Review weekly. If account-to-meeting rate drops below 2% for 2 consecutive weeks, investigate whether the issue is volume-related (sending too fast, domain reputation) or targeting-related (ICP drift at higher volume).

### 7. Evaluate against pass threshold

After 3 months of running at 200 accounts/month:

1. Calculate average monthly account-to-meeting rate across all 3 months
2. Calculate cost per meeting: (Instantly + Clay + LinkedIn Sales Navigator costs) / total meetings
3. Compare cost per meeting to Baseline level

**PASS (≥2.5% sustained + cost per meeting ≤2x Baseline):** Multi-threaded outreach works at scale with automation. Document the winning A/B variants, optimal timing sequence, and best-performing channel mix. Proceed to Durable.

**FAIL — rate dropped from Baseline:** Scale introduced quality problems. Check: Is the automated stakeholder classification accurate? Are the auto-generated thread maps as good as the manual ones? Is email deliverability suffering from volume?

**FAIL — rate held but cost exploded:** Efficiency problem. Look for wasted enrichment credits (accounts that should have been filtered out earlier), sending to unverified emails (bounces), or LinkedIn accounts hitting rate limits.

## Time Estimate

- Stakeholder discovery automation setup: 8 hours
- Thread orchestration n8n workflow build: 12 hours
- Instantly scaling (domains, warmup, campaigns): 6 hours
- A/B test design and implementation (3 experiments): 9 hours
- Follow-up automation workflows: 6 hours
- PostHog dashboard and monitoring: 4 hours
- Weekly monitoring and optimization (3 months): 30 hours
- Total: 75 hours over 3 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Cold email sequences at scale (3 role campaigns, A/B variants) | Hypergrowth: $77/mo for 25,000 emails (https://instantly.ai/pricing) |
| Clay | Stakeholder discovery + enrichment (3,000 credits/mo) | Explorer: $149/mo or Pro: $349/mo if credits exceed (https://www.clay.com/pricing) |
| LinkedIn Sales Navigator | Stakeholder research + InMail for high-value contacts | Core: $99/mo (https://business.linkedin.com/sales-solutions/compare-plans) |
| Dripify or Expandi | LinkedIn automation for connection + DM sequences | Dripify: $59/mo (https://dripify.io/pricing) |
| PostHog | Event tracking, funnels, feature flags, experiments | Free tier: 1M events/mo (https://posthog.com/pricing) |
| n8n | Workflow orchestration (thread coordination, follow-up automation) | Starter: $20/mo (https://n8n.io/pricing) |
| Attio | CRM for deals, stakeholder tracking, campaign attribution | Plus: $29/user/mo (https://attio.com/pricing) |

**Estimated monthly cost:** $385-$585/mo (Instantly $77 + Clay $149-$349 + LinkedIn $99 + Dripify $59 + n8n included in stack)

## Drills Referenced

- `stakeholder-org-mapping` — automated stakeholder discovery and classification for all incoming accounts
- `follow-up-automation` — engagement-triggered follow-up and cross-thread escalation workflows
- `ab-test-orchestrator` — systematic testing of message variants, timing sequences, and channel mix
