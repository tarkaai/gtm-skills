---
name: joint-content-campaigns-durable
description: >
  Joint Content Campaigns -- Durable Intelligence. Always-on AI agents find the local
  maximum of joint content lead generation. The autonomous-optimization loop monitors
  per-asset and per-partner performance, generates improvement hypotheses (topic selection,
  format, distribution timing, partner mix), runs A/B experiments, evaluates results,
  and auto-implements winners. Weekly optimization briefs track convergence.
stage: "Marketing > ProblemAware"
motion: "PartnershipsWarmIntros"
channels: "Content, Email"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained content output of >=2 assets/month and >=70 qualified leads over 12 months via AI-driven topic selection, partner matching, and distribution optimization"
kpis: ["Monthly qualified leads from joint content", "Download-to-lead conversion rate trend", "AI experiment win rate", "Partner retention rate", "Cost per qualified lead trend", "Production cycle time trend", "Topic discovery hit rate"]
slug: "joint-content-campaigns"
install: "npx gtm-skills add PartnershipsWarmIntros/Marketing/ProblemAware/joint-content-campaigns"
drills:
  - autonomous-optimization
---
# Joint Content Campaigns -- Durable Intelligence

> **Stage:** Marketing -> ProblemAware | **Motion:** PartnershipsWarmIntros | **Channels:** Content, Email

## Outcomes
The joint content program sustains >=2 co-created assets per month and generates >=70 qualified leads over 12 months. An AI agent continuously optimizes topic selection, content format, partner matching, distribution timing, and email copy. The program maintains or improves performance with decreasing human oversight as the agent finds the local maximum.

## Leading Indicators
- Autonomous optimization loop fires daily without errors
- At least 1 experiment running at all times
- Experiment win rate exceeds 30% (agent generates useful hypotheses)
- Weekly optimization briefs are produced on schedule
- Convergence detection activates when successive experiments yield <2% improvement
- Partner churn rate stays below 20% annually (healthy portfolio)

## Instructions

### 1. Deploy the autonomous optimization loop
Run the `autonomous-optimization` drill configured for this play's metrics. The optimization loop operates on the joint content funnel:

**Phase 1 -- Monitor (daily via n8n cron):**
- Use `posthog-anomaly-detection` to check this play's primary KPIs: weekly downloads, download-to-lead conversion rate, leads per asset, leads per partner, partner-sourced lead percentage
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger Phase 2

**Phase 2 -- Diagnose (triggered by anomaly):**
- Pull the current program configuration from Attio: active partners, asset formats in production, topic pipeline, distribution schedule, email subject line variants
- Pull 8-week metric history from PostHog
- Run `hypothesis-generation` with the anomaly data and joint-content-specific context
- Receive 3 ranked hypotheses. Examples of joint-content-specific hypotheses:
  - "Download volume dropped because the last 2 assets used the same topic category. Test: produce next asset on an underserved topic identified by Clay ICP research."
  - "Partner-sourced leads declined because partner B stopped promoting to their full list. Test: send partner a performance incentive (early access to the next asset's data) to re-engage."
  - "Conversion rate plateaued because the landing page form asks for too many fields. Test: reduce form to name + email only for the next asset."
  - "Ebook format consistently underperforms checklist format. Test: convert the next planned ebook into a checklist + companion data set."
- Store hypotheses in Attio. If top hypothesis is high-risk (changes partner relationship terms, changes lead-sharing agreement), alert human and stop.

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
- Design the experiment using `posthog-experiments`: create a feature flag that splits traffic between control and variant
- Implementation examples:
  - Topic variation: publish two assets simultaneously on different topics, measure download velocity and conversion
  - Format variation: same topic in two formats (ebook vs. checklist), split promotion equally
  - Distribution timing: send co-promotion email at different times/days for variant vs. control
  - Landing page variation: test form length, headline copy, or social proof elements
  - Partner emphasis: allocate more production resources to high-performing partner segment
- Minimum duration: 14 days or 200+ downloads per variant, whichever is longer
- Log experiment start in Attio

**Phase 4 -- Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run `experiment-evaluation` with control vs. variant metrics
- Decision: Adopt (update the program defaults), Iterate (refine hypothesis), Revert (restore control), or Extend (keep running)
- Store full evaluation in Attio with: decision, confidence level, net impact on KPIs, reasoning

**Phase 5 -- Report (weekly via n8n cron):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from all adopted changes this week
- Generate weekly optimization brief:
  - What changed and why
  - Net impact on primary KPIs
  - Current distance from estimated local maximum
  - Recommended focus for next week
  - Partner portfolio health summary
- Post to Slack and store in Attio

### 2. Deploy joint content performance monitoring
Run the `autonomous-optimization` drill to maintain a live scorecard of:
- Per-asset download velocity, conversion rate, and lead quality
- Per-partner contribution (how much of your lead volume comes from each partner's audience)
- Per-topic performance (which problem areas resonate most with the shared ICP)
- Per-format performance (which content types convert best)
- Distribution channel effectiveness (your email vs. partner email vs. organic vs. social)

The performance metrics feed directly into the autonomous optimization loop. When the agent detects a conversion drop or topic fatigue, it generates hypotheses specific to the content co-creation domain.

### 3. Implement advanced optimization strategies
Beyond the standard optimization loop, configure these joint-content-specific experiments:

**Topic discovery optimization:**
- Monthly: run Clay ICP research on 50 companies in the shared audience to detect emerging pain points
- Compare emerging topics against published asset topics to find gaps
- Score each candidate topic by: search volume (Ahrefs), ICP relevance (Clay), competitive gap (no existing co-created asset covers it)
- Auto-generate a topic brief for the highest-scoring candidate and propose it to the next available partner

**Partner matching optimization:**
- Maintain a partner-topic affinity matrix in Attio: which partners produce the best content on which topics
- When a new topic is selected, auto-recommend the partner most likely to produce a high-converting asset on that topic
- Track partner production velocity (days from agreement to delivery) and reliability (on-time delivery rate)
- Prioritize fast, reliable partners for time-sensitive topics

**Distribution timing optimization:**
- A/B test email send times for co-promotion blasts (day of week, time of day)
- Test whether simultaneous sends (both companies on the same day) outperform staggered sends (your list day 1, partner list day 3)
- Test whether social amplification within 24 hours of email sends boosts total downloads

**Landing page conversion optimization:**
- Test headline variations that emphasize different value propositions (data-driven vs. actionable vs. peer comparison)
- Test form length: email-only vs. name + email vs. name + email + company + role
- Test social proof: download count, partner logos, customer quotes
- Track which landing page variants produce the highest download-to-qualified-lead rate (not just download rate)

**Content format evolution:**
- Quarterly: review format performance data and retire underperforming formats
- Test emerging formats: interactive assessments, calculators, comparison tools
- Test content depth: short (5-page checklist) vs. long (20-page ebook) on the same topic
- Identify the format-topic combinations that produce the most qualified leads per hour of production effort

### 4. Detect convergence
The optimization loop runs indefinitely. However, it detects convergence -- when successive experiments produce diminishing returns (<2% improvement for 3 consecutive experiments). At convergence:

1. The play has reached its local maximum for current market conditions
2. Reduce monitoring frequency from daily to weekly
3. Report: "Joint content campaigns are optimized. Current performance: [metrics]. Further gains require strategic changes (new partner categories, new content distribution channels, product changes that enable new co-creation formats) rather than tactical optimization."
4. Continue monitoring for external disruptions: partner company changes (acquisition, pivot, layoffs), topic relevance shifts, competitive entries into the same co-marketing space

### 5. Maintain long-term sustainability

**Partner portfolio health:**
- Monitor partner churn: if a partner stops responding or declines future collaborations, investigate and document the reason
- Maintain a pipeline of 5+ partner prospects at all times to replace churned partners
- Invest in top-performing partners: exclusive topics, priority production slots, joint webinars, and co-sponsored distribution

**Content freshness:**
- Audit published assets quarterly: are they still generating downloads and leads?
- Refresh high-performing assets annually (update data, add new sections, rebrand if needed)
- Retire assets that generate <5 downloads/month -- remove from active promotion

**Market adaptation:**
- When new competitors enter the co-content space, differentiate through unique data or deeper expertise
- When the ICP's pain points shift (detected via quarterly Clay research), pivot the topic pipeline accordingly
- Track industry report calendars to avoid publishing on topics that just got covered by a major analyst firm

## KPIs to track
- Monthly qualified leads from joint content
- Download-to-lead conversion rate trend
- AI experiment win rate
- Partner retention rate
- Cost per qualified lead trend
- Production cycle time trend
- Topic discovery hit rate

## Pass threshold
**Sustained content output of >=2 assets/month and >=70 qualified leads over 12 months via AI-driven topic selection, partner matching, and distribution optimization**

This level runs continuously. Review monthly: what experiments ran, what improved, what to test next. The play is durable when it maintains performance with decreasing human oversight.

## Time Estimate
- 20 hours: autonomous optimization loop setup and configuration
- 10 hours: performance monitoring dashboard and alerts
- 100 hours: content co-production (24 assets x ~4 hours each, including optimization experiments)
- 30 hours: partner portfolio management and strategic review
- 20 hours: monthly optimization reviews and convergence analysis

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM for partner portfolio, lead attribution, experiment tracking | Plus plan ~$34/user/mo; https://attio.com/pricing |
| n8n | Automation for optimization loop, scheduling, attribution | Self-hosted free, Cloud from EUR20/mo; https://n8n.io/pricing |
| PostHog | Analytics, experiments, anomaly detection | Free up to 1M events/mo; https://posthog.com/pricing |
| Anthropic Claude | Hypothesis generation, content drafting, experiment evaluation | ~$50-100/mo at this volume; https://www.anthropic.com/pricing |
| Clay | ICP research for topic discovery | From $149/mo; https://clay.com/pricing |
| Crossbeam | Account overlap for partner matching | Free tier; paid from ~$0-200/mo; https://www.crossbeam.com/pricing |
| Ghost | Asset hosting | Free self-hosted; https://ghost.org/pricing |
| Loops | Email distribution | From $49/mo; https://loops.so/pricing |

## Drills Referenced
- `autonomous-optimization` -- the always-on monitor -> diagnose -> experiment -> evaluate -> implement loop that finds the local maximum
- `autonomous-optimization` -- per-asset, per-partner, and per-topic performance tracking and weekly briefs
