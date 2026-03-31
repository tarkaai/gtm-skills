---
name: partner-newsletter-swaps-scalable
description: >
  Partner Newsletter Swaps — Scalable Automation. Scale the swap program to 15-25 active partners
  with automated prospect-to-active pipelines, templatized email production, and performance-based
  cadence management that multiplies swap volume without proportional effort.
stage: "Marketing > ProblemAware"
motion: "PartnershipsWarmIntros"
channels: "Email"
level: "Scalable Automation"
time: "60 hours over 3 months"
outcome: ">=20 swaps/month across >=15 active partners, >=2,000 new subscribers, >=40 leads over 3 months"
kpis: ["Active partner count", "Swaps per month", "Subscribers per swap (trending)", "Cost per lead", "Partner pipeline fill rate", "Automation coverage ratio"]
slug: "partner-newsletter-swaps"
install: "npx gtm-skills add PartnershipsWarmIntros/Marketing/ProblemAware/partner-newsletter-swaps"
drills:
  - list-swap-scheduling
  - partner-pipeline-automation
---
# Partner Newsletter Swaps — Scalable Automation

> **Stage:** Marketing > ProblemAware | **Motion:** PartnershipsWarmIntros | **Channels:** Email

## Outcomes
- Maintain >=15 active swap partners with confirmed recurring cadences
- Execute >=20 swaps per month (combination of monthly, bimonthly, and quarterly partners)
- Acquire >=2,000 new subscribers from swap traffic over 3 months
- Generate >=40 leads over 3 months
- Reduce per-swap effort to <30 minutes (from ~2 hours at Baseline) through automation and templates

## Leading Indicators
- Partner pipeline has >=10 prospects in "Proposed" or "In Conversation" stage at all times
- Swap scheduling automation handles >=80% of coordination without human intervention
- Email template library covers >=5 proven variants reusable across partner types
- No swap is missed due to scheduling or coordination failure (0% drop rate)
- Per-swap subscriber acquisition remains stable (not declining due to audience fatigue)

## Instructions

### 1. Build the partner acquisition pipeline

Run the `partner-pipeline-automation` drill to automate the entire partner lifecycle from prospect to active:

1. **Automated partner outreach sequence:** When a new partner is added to the "Newsletter Partners" list in Attio with status "Prospect", n8n triggers a personalized outreach email via Instantly. If no reply in 5 days, one follow-up sends automatically. Positive replies update Attio status to "In Conversation" and create a deal in the Partnerships pipeline.

2. **Placement scheduling workflow:** Weekly cron checks Attio for partners with upcoming swap dates, verifies email copy is ready, and alerts when action is needed. This extends the Baseline `list-swap-scheduling` drill to handle 15-25 partners simultaneously.

3. **Performance tracking workflow:** PostHog webhooks fire on swap events. n8n routes these to Attio, incrementing per-partner lead counts and creating attributed lead records automatically.

4. **Partner nurture sequence:** Loops sequence keeps partners engaged between swaps — sharing performance data (Day 7), proposing next swap (Day 14), and sending monthly partnership summaries (Day 30).

5. **Partner health monitoring:** Monthly cron scores each partner on recency, frequency, and performance. Flags "At Risk" partners (zero leads in 2+ months) and "Expand" candidates (consistent high performers).

### 2. Scale the swap scheduling system

Extend the Baseline `list-swap-scheduling` drill to handle the larger portfolio:

1. **Performance-triggered cadence adjustment:** n8n workflows auto-propose cadence upgrades for partners whose last 2 swaps both exceeded 50 clicks and 2 meetings (quarterly -> bimonthly, bimonthly -> monthly). Auto-propose downgrades for partners with <10 clicks on last 2 swaps. Log all recommendations in Attio for human approval.

2. **List protection rules:** Enforce maximum 3 inbound swaps to your list per week. If more are scheduled, the system auto-staggers them and notifies partners of adjusted dates. Track your list's open rate and click rate weekly. If engagement drops >20% in weeks with 3+ inbound swaps, automatically reduce inbound frequency for the next month.

3. **Staggered swap calendar:** Distribute monthly partners across 4 weeks, bimonthly across alternating months, quarterly on a rolling schedule. No two swaps with overlapping partner audiences in the same week (check for audience segment overlap in Attio).

### 3. Templatize email production

Build a reusable email variant library to cut per-swap writing time:

1. Analyze all swap email performance data from Baseline. Identify the top 3 email angles by click-to-lead conversion rate.

2. Create 5 master templates in the `list-swap-email-copy` drill:
   - **Curiosity template:** Open loop subject, pain-point lead, specific proof point, low-commitment CTA
   - **Data template:** Stat-led subject, benchmark comparison, your product as the solution, CTA to see results
   - **Story template:** Mini scenario subject, "before/after" narrative, social proof, CTA to experience the change
   - **Question template:** Provocative question subject, "most teams do X, what if Y?", contrarian angle, CTA
   - **Timely template:** Trend/news hook, connect to audience pain, position your product, CTA

3. For each new swap, the agent selects the template that best matches the partner's audience and tone, personalizes it with partner-specific context, and generates the tracked CTA link. Human approves the final version. Target: <20 minutes from template selection to approved email.

### 4. Build a partner referral flywheel

Activate existing partners as a source of new partners:

1. After a partner completes 3+ successful swaps, send them a referral ask: "Know any other newsletters that would benefit from a swap like ours? We'll prioritize anyone you recommend."
2. Track referral source on new partner records in Attio.
3. Referred partners skip cold outreach and enter the pipeline at "Warm Introduction" stage.
4. Target: >=30% of new partners sourced from existing partner referrals by month 3.

### 5. Evaluate against threshold

Measure over the 3-month period:
- **>=20 swaps/month:** Total completed swaps in the final month of the period
- **>=15 active partners:** Partners with at least 1 swap completed in the last 60 days
- **>=2,000 new subscribers:** Cumulative from `list_swap_subscriber_added` events
- **>=40 leads:** Cumulative from `list_swap_lead_created` events
- **Automation coverage:** >=80% of scheduling, tracking, and coordination handled by n8n without manual intervention

If PASS: The swap program scales without proportional effort. Each new partner adds incremental value with minimal marginal work. Proceed to Durable to let the agent autonomously optimize partner selection, email variants, and cadence.

If FAIL: Identify the bottleneck. If partner acquisition is slow, invest more in the referral flywheel and cold outreach automation. If per-swap results are declining, check for audience fatigue (reduce cadence with saturated partners) or email fatigue (refresh templates). If automation is unreliable, audit n8n workflows for failure points.

---

## Time Estimate
- Partner pipeline automation build: 12 hours
- Swap scheduling system scaling: 8 hours
- Email template library creation: 8 hours
- Partner referral program setup: 4 hours
- Ongoing management (3 months): 28 hours (~2.5 hours/week)

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| n8n | Pipeline automation, scheduling, health monitoring | Cloud: $24/mo. Self-hosted: free (https://n8n.io/pricing) |
| Attio | Partner CRM, deal tracking, relationship scoring | Plus: $34/user/mo (https://attio.com/pricing) |
| PostHog | Swap event tracking, performance analytics | Free tier: 1M events/mo (https://posthog.com/pricing) |
| Loops | Reciprocal sends and partner nurture sequences | Growth: $49/mo for 5K contacts (https://loops.so/pricing) |
| Instantly | Automated partner outreach at scale | Growth: $30/mo for 1K contacts (https://instantly.ai/pricing) |
| Clay | Partner prospect enrichment | Pro: $149/mo (https://www.clay.com/pricing) |

**Estimated play-specific cost:** ~$150-300/mo at scale

## Drills Referenced
- `list-swap-scheduling` — coordinate 15-25 partner swaps with performance-based cadence adjustment and list protection
- `partner-pipeline-automation` — automate the full partner lifecycle from prospect to active to health-monitored
