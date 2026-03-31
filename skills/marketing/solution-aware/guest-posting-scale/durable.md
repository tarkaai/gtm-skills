---
name: guest-posting-scale-durable
description: >
  Guest Posting at Scale — Durable Intelligence. Autonomous AI agents optimize the entire guest
  posting pipeline: detect metric anomalies, test pitch variations, experiment with blog tiers
  and topics, auto-implement winners, and converge on local maximum performance.
stage: "Marketing > Solution Aware"
motion: "PR & Earned Mentions"
channels: "Content, Email"
level: "Durable Intelligence"
time: "90 hours over 6 months"
outcome: "Sustained or improving acceptance rate and ≥2,000 referral visits/month over 6 months via autonomous optimization finding the local maximum"
kpis: ["Pitch acceptance rate trend (sustained ≥15%)", "Articles published per month (sustained ≥10)", "Referral traffic trend (sustained ≥2,000/mo)", "Backlink portfolio growth (new referring domains/month)", "Conversion rate from referrals", "Optimization experiment win rate"]
slug: "guest-posting-scale"
install: "npx gtm-skills add marketing/solution-aware/guest-posting-scale"
drills:
  - autonomous-optimization
  - guest-post-performance-monitor
  - guest-post-outreach-automation
---

# Guest Posting at Scale — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** PR & Earned Mentions | **Channels:** Content, Email

## Outcomes

The guest posting pipeline runs autonomously. AI agents continuously monitor performance, detect when metrics plateau or decline, generate hypotheses for improvement, run controlled experiments, and auto-implement winning variants. The system converges on the local maximum — the best achievable acceptance rate, referral traffic, and conversion rate given current market conditions — and maintains it as the competitive landscape shifts.

## Leading Indicators

- Autonomous optimization loop executes without manual intervention for 4+ consecutive weeks
- At least 2 optimization experiments per month with ≥1 producing measurable improvement
- Acceptance rate holds within 2% of peak despite increasing outreach volume
- Referral traffic per published article trends upward (content quality improving, not just volume)
- Weekly optimization briefs are generated automatically with actionable insights

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the guest posting play. This creates the core Monitor → Diagnose → Experiment → Evaluate → Implement cycle:

**Phase 1 — Monitor (daily via n8n cron):**
Use `posthog-anomaly-detection` to check the guest posting KPIs daily:
- Pitch acceptance rate (2-week rolling vs. 4-week average)
- Referral traffic per published article (2-week rolling)
- Backlink acquisition rate (new referring domains/week)
- Conversion rate from guest post referrals

Classify each KPI: **normal** (within ±10%), **plateau** (±2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase). If anomaly detected, trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
Gather context: pull current pipeline configuration from Attio (blog tiers being targeted, pitch templates in use, article topics, backlink strategy). Pull 8-week metric history from PostHog. Run `hypothesis-generation` with anomaly data + context. Receive 3 ranked hypotheses.

Example hypotheses the system might generate:
- "Acceptance rate dropped because we exhausted high-quality Tier 1 blogs → test expanding to adjacent niches"
- "Referral traffic per article is declining → test longer-form articles (2,000+ words) vs. current 1,200-word average"
- "Conversion rate dropped → test different backlink target pages (tool page vs. guide page)"
- "Pitch reply rate declining → test new pitch angle structure (data-led vs. story-led)"

Store hypotheses in Attio. If top hypothesis is "high risk" (e.g., changing audience targeting), send to Slack for human review and STOP. Otherwise proceed.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
Use `posthog-experiments` to design a controlled test:
- Split outreach into control (current approach) and variant (hypothesis change)
- Example: pitch 50 blogs with current template (control) and 50 with data-led opening (variant)
- Minimum duration: 14 days or until 50+ responses per group, whichever is longer
- Log experiment start in Attio

**Phase 4 — Evaluate (triggered by experiment completion):**
Run `experiment-evaluation` with control vs. variant results:
- **Adopt:** Update the pipeline to use the winning variant. Log the change.
- **Iterate:** Generate a new hypothesis building on the result. Return to Phase 2.
- **Revert:** Restore control. Log the failure. Return to Phase 1.

**Phase 5 — Report (weekly via n8n cron):**
Generate a weekly optimization brief:
- Anomalies detected this week
- Experiments running and their interim results
- Experiments completed and decisions made
- Net impact on KPIs from adopted changes
- Estimated distance from local maximum
- Recommended focus for next week

Post to Slack and store in Attio.

### 2. Maintain and evolve the outreach automation

The `guest-post-outreach-automation` workflows from Scalable continue running. At Durable, the autonomous optimization loop tunes their parameters:

**Blog discovery tuning:**
- The optimization loop tests different niche keyword sets and DA thresholds
- If a new niche vertical yields higher acceptance rates, the agent expands discovery into that vertical
- If a blog tier consistently underperforms (Tier 3 acceptance <8%), the agent raises the minimum DA threshold

**Pitch template evolution:**
- The agent maintains a library of 8-12 pitch templates
- New templates are generated based on winning experiment patterns
- Templates that drop below 10% reply rate are retired
- Template performance is tracked per blog tier and topic category

**Relationship deepening:**
- For editors who accepted 2+ guest posts, the agent schedules quarterly pitch cycles with new topics
- The agent generates "relationship health" scores based on: acceptance rate, editorial feedback tone, time between pitches, and cross-promotion activity
- High-relationship editors get priority access to exclusive content angles

### 3. Deploy continuous performance monitoring

The `guest-post-performance-monitor` drill runs always-on at Durable level with enhanced alerting:

- **Backlink health check (daily):** Detect lost backlinks within 24 hours. If a Tier 1 backlink is lost, the agent generates a replacement pitch for the same blog.
- **Content decay detection (weekly):** Identify guest posts where referral traffic has declined >50% from peak. Propose content refresh pitches to the editor.
- **Competitor monitoring (weekly):** Track competitor guest posting activity. When a competitor lands a placement on a new high-DA blog, the agent generates a counter-pitch within 48 hours.
- **Domain authority tracking (weekly):** Correlate DR changes with guest post backlink acquisition. Calculate the incremental DR impact per published guest post.

### 4. Configure Durable guardrails

All Scalable guardrails remain in effect. Additional Durable guardrails:

- **Experiment rate limit:** Maximum 1 active optimization experiment at a time. Never stack experiments.
- **Auto-revert threshold:** If any primary KPI drops >30% during an experiment, auto-revert immediately.
- **Human approval required for:** Audience/niche changes affecting >50% of the pipeline, budget increases >20%, any change flagged as "high risk" by hypothesis generation.
- **Experiment cooldown:** After a failed experiment, wait 7 days before testing a new hypothesis on the same variable.
- **Monthly experiment cap:** Maximum 4 experiments per month. If all 4 fail, pause optimization and flag for human strategic review.
- **Convergence detection:** When 3 consecutive experiments produce <2% improvement, the play has reached its local maximum. Reduce monitoring to weekly. Report: "Guest posting pipeline is optimized at current performance. Further gains require strategic changes (new channels, new audience segments, or product changes)."

### 5. Evaluate sustainability

This level runs continuously. Monthly review:
- Are KPIs sustaining or improving over 6 months?
- Is the optimization loop finding and implementing improvements?
- Is the backlink portfolio growing in both quantity and average DR?
- Are editor relationships deepening (repeat placements)?

If all metrics sustain or improve for 6 months, the play is durable. If metrics decay despite optimization, diagnose: market saturation, topic fatigue, or competitive pressure? Surface the diagnosis in the monthly report for human strategic decision.

## Time Estimate

- Autonomous optimization setup: 8 hours
- Monthly maintenance and oversight: 5 hours/month (30 hours over 6 months)
- Experiment design and evaluation review: 3 hours/month (18 hours over 6 months)
- Strategic review and human decisions: 2 hours/month (12 hours over 6 months)
- Workflow maintenance and bug fixes: 2 hours/month (12 hours over 6 months)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| n8n | Optimization loop, pipeline automation, alerting | Self-hosted free, Cloud $20/mo (https://n8n.io/pricing) |
| Ahrefs | Backlink monitoring, competitor tracking, DR tracking | Advanced $399/mo recommended at Durable scale (https://ahrefs.com/pricing) |
| PostHog | Anomaly detection, A/B experiments, dashboards | Free up to 1M events (https://posthog.com/pricing) |
| Clay | Enrichment for new discovery targets | Explorer $349/mo (https://clay.com/pricing) |
| Instantly | Pitch sending with experiment variants | Hypergrowth $77.6/mo (https://instantly.ai/pricing) |
| Attio | Pipeline CRM, experiment logging, relationship tracking | Plus $34/seat/mo (https://attio.com/pricing) |
| Anthropic API | Hypothesis generation, pitch generation, article drafting, evaluation | ~$10-20/mo at Durable scale (https://anthropic.com/pricing) |

## Drills Referenced

- `autonomous-optimization` — the always-on Monitor → Diagnose → Experiment → Evaluate → Implement loop that finds and maintains the local maximum
- `guest-post-performance-monitor` — continuous backlink health, referral traffic, and conversion monitoring with enhanced Durable alerting
- `guest-post-outreach-automation` — the automated discovery, pitching, and reply routing pipeline whose parameters the optimization loop tunes
