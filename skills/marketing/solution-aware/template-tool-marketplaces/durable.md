---
name: template-tool-marketplaces-durable
description: >
  Template or Tool Marketplace — Durable Intelligence. Always-on AI agents autonomously optimize
  template listings, portfolio composition, cross-promotion, and landing pages via the
  detect-diagnose-experiment-evaluate loop. Finds the local maximum for template-driven lead generation.
stage: "Marketing > SolutionAware"
motion: "DirectoriesMarketplaces"
channels: "Other"
level: "Durable Intelligence"
time: "20 hours setup + 2 hours/week ongoing"
outcome: "Downloads and leads sustained at or above Scalable baseline for 6 consecutive months; successive optimization experiments produce <2% improvement (convergence)"
kpis: ["Total downloads (trend)", "Leads captured (trend)", "Download-to-lead conversion rate (trend)", "Cross-promotion CTR (trend)", "Experiment win rate", "Convergence score"]
slug: "template-tool-marketplaces"
install: "npx gtm-skills add marketing/solution-aware/template-tool-marketplaces"
drills:
  - autonomous-optimization
  - dashboard-builder
---

# Template or Tool Marketplace — Durable Intelligence

> **Stage:** Marketing > SolutionAware | **Motion:** DirectoriesMarketplaces | **Channels:** Other

## Outcomes

Always-on AI agents finding the local maximum. The `autonomous-optimization` drill runs the core loop: detect metric anomalies in template marketplace performance, generate improvement hypotheses, run A/B experiments on listings and conversion paths, evaluate results, and auto-implement winners. Weekly optimization briefs. The play converges when successive experiments produce <2% improvement.

**Pass threshold:** Downloads and leads sustained at or above Scalable baseline for 6 consecutive months; successive optimization experiments produce <2% improvement (convergence).

## Leading Indicators

- Autonomous optimization loop running daily (monitoring) and weekly (experiment cycle)
- At least 1 experiment active per month across the template portfolio
- Weekly optimization briefs delivered automatically
- No manual intervention required for routine listing updates, cross-promotion changes, or nurture sequence adjustments
- Download and lead trends stable or improving over 4-week rolling window
- Convergence detected: 3 consecutive experiments produce <2% improvement on any single variable

## Instructions

### 1. Initialize the autonomous optimization loop

Run the `autonomous-optimization` drill configured for this play's KPIs:

**Primary KPIs to monitor:**
- Total downloads per week (across all templates and marketplaces)
- Total leads captured per week (from template-sourced traffic)
- Download-to-lead conversion rate (portfolio-wide)
- Cross-promotion click-through rate (measures network effect health)

**Anomaly detection thresholds:**
- Normal: within +/-10% of 4-week rolling average
- Plateau: +/-2% for 3+ consecutive weeks
- Drop: >20% decline week-over-week
- Spike: >50% increase week-over-week

**Phase 1 -- Monitor (daily via n8n cron):**
1. Pull PostHog data for marketplace_visit, marketplace_cta_click, marketplace_lead_captured
2. Pull marketplace-level download data using `marketplace-analytics-scraping` fundamental
3. Compare against 4-week rolling average
4. If anomaly detected -> trigger Phase 2 (Diagnose)
5. If normal -> log metrics, no action

**Phase 2 -- Diagnose (triggered by anomaly):**
1. Gather context: current listing copy for each template on each marketplace, current landing page variant, current nurture sequence performance, cross-promotion link CTRs
2. Pull 8-week metric history from PostHog
3. Run `hypothesis-generation` with anomaly data + context
4. Receive 3 ranked hypotheses. Examples specific to this play:
   - "Downloads dropped on Notion for our OKR template because a competitor published a similar template with better screenshots and a video walkthrough. Hypothesis: update our cover image to include a walkthrough video thumbnail and refresh the description to emphasize what makes ours unique."
   - "Leads dropped despite stable downloads because the landing page CTA changed in a recent deploy. Hypothesis: revert landing page headline to previous version and test."
   - "Cross-promotion CTR dropped from 4% to 1.5% because the same 3 templates have been cross-promoted for 8 weeks and users have seen them. Hypothesis: rotate cross-promotion links to feature newer templates."
   - "Gumroad downloads spiked 200% because a tech influencer shared our template. Hypothesis: capitalize by publishing 2 related templates this week and linking them from the viral template."
5. If top hypothesis is high-risk (changes affecting >50% of portfolio or landing page core structure) -> alert human and STOP
6. If low/medium risk -> proceed to Phase 3

**Phase 3 -- Experiment:**
1. Take the top hypothesis
2. Design the experiment:
   - For listing changes: update the listing and compare 2-week performance before/after (most marketplaces do not support native split testing)
   - For landing page changes: use PostHog feature flags to split marketplace-sourced traffic 50/50 between control and variant
   - For cross-promotion changes: rotate links in a subset of templates and compare CTR
   - For nurture sequence changes: create a variant email sequence in Loops and split new subscribers
   - For portfolio composition changes: publish a new template and measure incremental impact
3. Set minimum duration: 14 days or 500+ marketplace-sourced sessions, whichever is longer
4. Log experiment in Attio: hypothesis, start date, duration, success criteria

**Phase 4 -- Evaluate:**
1. Pull experiment results from PostHog and marketplace analytics
2. Run `experiment-evaluation`:
   - **Adopt:** Implement the winning variant permanently. Log the change.
   - **Iterate:** Generate a new hypothesis building on the result. Return to Phase 2.
   - **Revert:** Restore the control. Log the failure. Return to Phase 1.
   - **Extend:** Keep running if sample size is insufficient.
3. Store full evaluation in Attio

**Phase 5 -- Report (weekly via n8n cron):**
1. Aggregate: anomalies detected, hypotheses generated, experiments run, decisions made
2. Calculate net metric change from all adopted changes
3. Generate weekly optimization brief:
   - What changed and why
   - Net impact on downloads, leads, and conversion rate
   - Portfolio health: which templates are growing, stable, or declining
   - Cross-promotion network performance
   - Current distance from estimated local maximum
   - Convergence status (are gains diminishing?)
4. Post to Slack and store in Attio

### 2. Configure play-specific monitoring

Run the `autonomous-optimization` drill with Durable-level enhancements:

**Competitive intelligence automation:**
- Weekly Clay scrape of top 5 competing templates per marketplace per category
- Alert when a competitor template's downloads jump significantly in a week
- Alert when a new template appears in your category with high initial traction (>100 downloads in first week)
- Feed competitive changes into the hypothesis generator as context

**Template portfolio health monitoring:**
- Track per-template download velocity trends (not just totals)
- Detect template fatigue: if a template's weekly downloads drop 30%+ from its peak for 4+ consecutive weeks, flag for refresh or retirement
- Monitor marketplace algorithm changes: detect sudden ranking shifts that affect multiple templates simultaneously (indicates a platform change, not a content issue)
- Track seasonal patterns: some template topics have quarterly or annual demand cycles (e.g., planning templates spike in January, Q4 review templates in October)

**Lead quality monitoring:**
- Track template-sourced leads through the sales pipeline in Attio
- Compare lead quality (deal close rate, average deal size) between template-sourced leads and other channels
- Identify which specific templates produce the highest-quality leads (closest to ICP, fastest to close)
- Feed lead quality data back into template topic prioritization

### 3. Build the executive dashboard

Run the `dashboard-builder` drill to create the Durable-level template marketplace dashboard:

**Panel 1 -- Portfolio Health:**
- Traffic light status per template: green (downloads growing), yellow (stable), red (declining)
- Total downloads, site visits, and leads (30-day rolling)
- Comparison to Scalable baseline (are we maintaining or exceeding?)

**Panel 2 -- Optimization Activity:**
- Active experiments (count, descriptions)
- Experiments completed this month (win/loss/no-call)
- Cumulative improvement from adopted experiments (% change from Scalable baseline)
- Convergence indicator: moving average of experiment impact (trending toward <2%)

**Panel 3 -- Template Performance Matrix:**
- Scatter plot: downloads (x-axis) vs lead conversion rate (y-axis) per template
- Quadrant labels: "Star" (high downloads, high conversion), "Volume Play" (high downloads, low conversion), "Niche Winner" (low downloads, high conversion), "Candidate for Retirement" (low both)

**Panel 4 -- Cross-Promotion Network:**
- Network graph showing cross-promotion link flows between templates
- CTR per link
- Identify the highest-traffic cross-promotion paths

**Panel 5 -- Competitive Position:**
- Your templates' rank vs top 3 competitors per marketplace per category
- Download gap (how far ahead or behind the leading competing template)

### 4. Guardrails

Follow all guardrails from the `autonomous-optimization` drill, plus these play-specific limits:

- **Template change rate limit:** Maximum 1 major listing change per template per 2-week period. Frequent changes disrupt marketplace ranking signals.
- **Cross-promotion rotation:** Rotate cross-promotion links no more than once per month. More frequent changes confuse the compounding effect.
- **Portfolio size cap:** Do not exceed 15 active templates without human approval. Each template requires maintenance -- diminishing returns set in around 10-15 templates.
- **Nurture sequence changes:** Never change more than 1 email in the nurture sequence at a time. Sequential changes make it impossible to attribute impact.
- **Landing page changes:** Never change the landing page CTA type (form vs calendar vs chat) without human approval. Only test copy/design variations within the same surface type.
- **Template retirement:** Never unpublish a template that generated >10 leads in the last quarter without human approval. Even declining templates may still contribute.

### 5. Convergence and steady state

When the optimization loop detects convergence (<2% improvement from 3 consecutive experiments):

1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment cadence from monthly to quarterly
3. Report: "Template marketplace channel optimized. Current performance: {downloads}/week, {leads}/week, {conversion_rate}% conversion across {template_count} templates on {marketplace_count} marketplaces. Further gains require strategic changes (new template categories, new marketplace platforms, product changes that unlock new template types)."
4. Continue passive monitoring for external disruptions (marketplace algorithm changes, new competitors, trending template topics)
5. Re-enter active optimization if any primary KPI drops >15% from the converged baseline

## Time Estimate

- 8 hours: Configure autonomous optimization loop (n8n workflows, PostHog experiments, Attio logging)
- 4 hours: Competitive intelligence and portfolio health monitoring setup
- 4 hours: Executive dashboard build
- 2 hours: Guardrail configuration and testing
- 2 hours: Lead quality tracking setup
- Ongoing: 2 hours/week reviewing optimization briefs and approving high-risk experiments

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Tracking, experiments, dashboards, anomaly detection | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Automation orchestration (monitoring, experiments, reports) | Cloud Pro EUR 60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Anthropic API | Hypothesis generation + experiment evaluation | ~$20-50/mo at optimization cadence ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| Clay | Competitive monitoring, template research | Explorer $149/mo ([clay.com/pricing](https://clay.com/pricing)) |
| Attio | CRM + experiment logging + lead pipeline | Plus $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Loops | Nurture sequence management and A/B testing | Starter $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Notion Marketplace | Template distribution | Free listings ([notion.com/marketplace](https://www.notion.com/help/selling-on-marketplace)) |
| Gumroad | Template distribution + email capture | Free for $0 products ([gumroad.com/pricing](https://gumroad.com/pricing)) |
| Figma Community | Template distribution | Free ([figma.com/community](https://www.figma.com/community)) |

**Estimated monthly cost at this level:** $400-600 (n8n + Clay + Attio + Loops + Anthropic API; marketplace listings and PostHog remain free at typical volumes)

## Drills Referenced

- `autonomous-optimization` -- the core detect-diagnose-experiment-evaluate loop that finds the local maximum for template marketplace performance
- `autonomous-optimization` -- enhanced with competitive intelligence, template portfolio health tracking, lead quality monitoring, and seasonal pattern detection
- `dashboard-builder` -- executive dashboard with portfolio health, optimization activity, template performance matrix, and convergence tracking
