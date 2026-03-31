---
name: interactive-content-tools-durable
description: >
  Interactive Content Tools — Durable Intelligence. Always-on AI agents monitor tool funnel health,
  detect metric anomalies, generate improvement hypotheses, run A/B experiments, and auto-implement
  winners. Autonomous optimization finds the local maximum for each tool. New tool concepts are
  surfaced from customer conversation analysis.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Website, Content"
level: "Durable Intelligence"
time: "85 hours over 6 months"
outcome: "Sustained or improving tool completion rate and SQL conversion rate over 6 months via autonomous optimization"
kpis: ["Tool completion rate trend", "SQL conversion rate", "Revenue per tool lead", "Tool engagement depth", "Personalization effectiveness"]
slug: "interactive-content-tools"
install: "npx gtm-skills add marketing/solution-aware/interactive-content-tools"
drills:
  - autonomous-optimization
  - interactive-tool-performance-monitor
  - interactive-tool-nurture-pipeline
---

# Interactive Content Tools — Durable Intelligence

> **Stage:** Marketing → Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Website, Content

## Outcomes

The tool portfolio runs autonomously. AI agents monitor every tool's funnel metrics daily, detect when completion rates drop or conversion patterns shift, generate hypotheses for improvement, run experiments, and auto-implement winners. The system converges on the local maximum for each tool — the best achievable performance given the current market and audience. New tool concepts are automatically surfaced from customer conversation analysis.

**Pass threshold:** Sustained or improving tool completion rate and SQL conversion rate over 6 months via autonomous optimization

## Leading Indicators

- Autonomous optimization loop running: ≥2 experiments completed per month across the tool portfolio
- Weekly optimization briefs generated without human intervention
- At least 1 experiment per quarter produces a statistically significant winner (>5% improvement)
- Tool-to-revenue attribution tracked end-to-end: tool completion → email capture → nurture → meeting → deal → closed-won
- Convergence detection: the system identifies when a tool has reached its local maximum and reduces optimization frequency

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to create the always-on monitor → diagnose → experiment → evaluate → implement loop for the interactive content tools play.

Configure the optimization loop with these play-specific parameters:

**Monitored metrics (via PostHog):**
- Tool completion rate per tool (daily check)
- Email capture rate per tool (daily check)
- Field-level drop-off rates (daily check)
- Tool-to-meeting conversion rate (weekly check)
- SQL conversion rate from tool leads (weekly check)
- Revenue per tool lead (monthly check)

**Optimization variables (what the agent can experiment on):**
- Question order within each tool
- Question wording and helper text
- Email gate placement (which field it appears after)
- Result display format (dollar amount vs percentage vs ranking vs visual score)
- CTA copy and placement on results page
- Nurture sequence timing and content (subject lines, send delay, number of emails)
- AI personalization prompt (adjust how results narrative is generated)
- Landing page headline and supporting copy

**Guardrails (what the agent cannot change without human approval):**
- Tool calculation formulas or scoring methodology (changing the math requires human review)
- Email gate removal (gate must always be present)
- Adding new input fields (can remove or reorder, but adding requires human approval)
- Pricing or product claims in result recommendations
- Budget allocation changes >20% on paid promotion channels

**Experiment constraints:**
- Maximum 1 active experiment per tool at a time
- Minimum 200 completions per variant before evaluating
- Auto-revert if primary metric drops >30% during an experiment
- Maximum 4 experiments per tool per month
- 7-day cooldown after a failed experiment on the same variable

### 2. Deploy play-specific monitoring

Run the `interactive-tool-performance-monitor` drill to build:

- **Tool funnel dashboard** (7 panels): views → starts → completions → captures → results viewed → CTA clicks → meetings booked, broken out by tool and week
- **Field-level drop-off heatmap**: identifies exactly which question kills completion on each tool. This is the highest-signal diagnostic panel — every field with >25% drop-off is an optimization target.
- **Per-tool health scoring**: daily 0-100 score combining completion rate, capture rate, and conversion rate vs baseline. Alert when any tool drops below 50 for 3+ days.
- **Anomaly detection**: automated alerts for completion rate drops, capture rate declines, field drop-off spikes, CTA click drops, and traffic source shifts.
- **Weekly AI-generated briefs**: Monday morning summary of what changed, what needs attention, the top optimization hypothesis to test, and which tool is performing best/worst.

### 3. Build the autonomous tool concept generator

Configure an n8n workflow (monthly cron) that surfaces new tool ideas:

1. **Analyze customer conversations**: Pull recent sales call transcripts (via Fireflies API or Gong), support tickets (via Intercom export), and community discussions. Use Anthropic API to extract:
   - Questions prospects ask repeatedly that involve calculations or comparisons
   - Pain points that could be quantified with user-provided inputs
   - Competitor mentions where a comparison tool would help

2. **Score tool concepts**: For each candidate concept, score on:
   - Search volume for related keywords (check Google Keyword Planner via API)
   - Differentiation (does this tool already exist from competitors?)
   - Connection to product value prop (does completing this tool naturally lead to your product?)
   - Build effort (can it use existing tool templates?)

3. **Generate a concept brief**: For the top-scoring concept, use Anthropic API to generate:
   - Proposed input fields and calculation logic
   - Estimated completion time
   - Target keyword cluster
   - Expected conversion funnel based on similar tools in the portfolio

4. **Route for decision**: Post the concept brief to Slack for human review. If approved, the agent builds the tool using the `interactive-tool-build` drill template.

**Human action required:** Review tool concept briefs monthly. Approve or reject new tool ideas. Verify that proposed calculations are accurate and the tool concept aligns with current product strategy.

### 4. Optimize nurture sequences autonomously

Extend the `interactive-tool-nurture-pipeline` to be optimized by the autonomous loop:

- The agent monitors nurture email performance (open rates, click rates, reply rates, meeting conversion) per sequence and per email step
- When a nurture email underperforms its 4-week average, the agent generates a new subject line and body variant using Anthropic API
- The agent runs the variant as an A/B test via Loops + PostHog
- Winners auto-implement; losers revert
- The agent detects when a sequence has converged (successive tests produce <2% improvement) and shifts optimization effort to other sequences

### 5. Build the convergence detection system

The autonomous optimization loop must detect when a tool has reached its local maximum:

- Track the net improvement from each experiment per tool over a rolling 3-month window
- When 3 consecutive experiments on the same tool produce <2% improvement each, declare convergence
- At convergence:
  - Reduce the monitoring frequency from daily to weekly for that tool
  - Generate a convergence report: "Tool {X} is optimized. Current metrics: {completion_rate}%, {capture_rate}%, {SQL_rate}%. Further gains require strategic changes (new ICP targeting, new tool concept, or product changes) rather than tactical optimization."
  - Shift optimization resources to underperforming tools or new tool concepts

### 6. Evaluate sustainability

Measure against: Sustained or improving tool completion rate and SQL conversion rate over 6 months.

This level runs continuously. Monthly review:
- How many experiments ran this month? How many produced winners?
- Net metric change across the tool portfolio (completion rate, capture rate, SQL rate, revenue)
- Which tools converged? Which still have optimization headroom?
- Were any new tool concepts generated and approved?
- Is the cost-per-SQL from tool leads trending down (efficiency gains from optimization)?

If metrics sustain or improve for 6+ months, the play is durable. If metrics decay despite active optimization, the agent diagnoses whether the cause is market saturation (tool concepts exhausted), audience shift (ICP changed), or competitive pressure (competitors launched similar tools) and recommends strategic interventions.

---

## Time Estimate

- Autonomous optimization loop configuration: 12 hours
- Play-specific monitoring setup (dashboard, anomaly detection, briefs): 10 hours
- Tool concept generator workflow: 8 hours
- Nurture sequence autonomous optimization: 6 hours
- Convergence detection system: 4 hours
- Monthly reviews and strategic decisions (6 months): 15 hours
- Agent compute monitoring and prompt refinement: 30 hours over 6 months

Total: ~85 hours of active work over 6 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Funnel tracking, experiments, feature flags, anomaly detection | Free up to 1M events/mo; $0.00045/event after |
| n8n | Optimization loop orchestration, concept generator, monitoring workflows | $20/mo cloud or free self-hosted |
| Anthropic | Hypothesis generation, experiment evaluation, concept briefs, personalization | ~$50-150/mo (higher at Durable due to daily monitoring + AI generation) |
| Attio | CRM with full tool attribution, deal tracking, reporting | $29/seat/mo Pro |
| Loops | Nurture sequences with A/B test variants | $49-159/mo depending on contact volume |
| Tally or OutGrow | Ongoing tool hosting | Tally: $29/mo; OutGrow: $115/mo |

**Play-specific cost:** ~$100-500/mo (tools + AI compute + hosting)

Agent compute costs are variable based on monitoring frequency and experiment volume. Budget ~$50-150/mo for Anthropic API at daily monitoring cadence across 8-12 tools.

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics → detect anomalies → generate hypotheses → run experiments → evaluate results → auto-implement winners. Weekly optimization briefs. Converges when successive experiments produce <2% improvement.
- `interactive-tool-performance-monitor` — play-specific monitoring: tool funnel dashboard, field-level drop-off heatmap, per-tool health scoring, anomaly detection, and weekly AI-generated briefs
- `interactive-tool-nurture-pipeline` — nurture sequences that the autonomous loop continuously optimizes for open rate, click rate, and meeting conversion
