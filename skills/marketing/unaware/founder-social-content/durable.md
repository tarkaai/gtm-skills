---
name: founder-social-content-durable
description: >
  Founder Social & Content — Durable Intelligence. Always-on AI agents monitor content performance,
  detect anomalies, generate improvement hypotheses, run A/B experiments, and auto-implement winners.
  The autonomous optimization loop finds and maintains the local maximum for content-driven pipeline.
stage: "Marketing > Unaware"
motion: "FounderSocialContent"
channels: "Social"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving leads and meetings over 6 months; successive optimization experiments converge to <2% improvement, indicating local maximum reached."
kpis: ["Impressions per post (4-week rolling)", "Engagement rate (4-week rolling)", "Leads per week", "Meetings per week", "Pipeline value attributed to content", "Experiment win rate", "Optimization convergence rate"]
slug: "founder-social-content"
install: "npx gtm-skills add marketing/unaware/founder-social-content"
drills:
  - autonomous-optimization
---

# Founder Social & Content — Durable Intelligence

> **Stage:** Marketing → Unaware | **Motion:** FounderSocialContent | **Channels:** Social

## Outcomes

The content engine runs autonomously with AI agents continuously monitoring, diagnosing, experimenting, and optimizing. The `autonomous-optimization` drill creates the always-on loop that detects metric anomalies, generates improvement hypotheses, runs A/B experiments, evaluates results, and auto-implements winners. The `autonomous-optimization` drill provides the play-specific monitoring, attribution, and reporting that feeds the optimization loop. Together, they find and maintain the local maximum — the best possible content performance given the current audience, market, and competitive landscape.

Success = leads and meetings sustained at or above Scalable baseline for 6 months, with the optimization loop converging (successive experiments producing <2% improvement) indicating the local maximum is reached.

## Leading Indicators

- Autonomous optimization loop active: daily monitoring running, experiments in flight
- Weekly optimization briefs delivered (no gaps in reporting)
- Experiment cadence: 2-4 experiments per month
- Experiment win rate: ≥ 40% of experiments adopted (below 30% = hypotheses are poorly formed)
- Content-to-pipeline attribution complete: every lead traced back to source post
- No metric anomalies unresolved for >7 days
- Convergence tracking: when 3 consecutive experiments produce <2% improvement, local maximum is declared

## Instructions

### 1. Deploy the social content performance monitor

Run the `autonomous-optimization` drill to build the always-on monitoring system:

**Build the PostHog dashboard** with 5 panels:
1. Publishing Cadence — posts per week by platform and pillar
2. Engagement Health — engagement rate, impressions, follower growth (4-week rolling, by pillar and format)
3. Lead Generation Funnel — post_published -> engagement -> profile_visit -> dm -> lead_captured -> meeting_booked
4. Content-to-Pipeline Attribution — pipeline value attributed to content, top posts by leads generated
5. Efficiency — leads per hour of founder time, pipeline value per hour

**Configure anomaly detection** checking daily:
- Engagement rate drops >25% vs 4-week rolling average -> trigger "engagement-decline"
- Impressions per post drops >30% vs 4-week average -> trigger "reach-decline"
- Zero DMs in 7 days when baseline is 2+/week -> trigger "dm-drought"
- Zero leads in 7 days when baseline is 3+/week -> trigger "lead-drought"
- Lead-to-meeting conversion drops below 20% for 2 consecutive weeks -> trigger "conversion-decline"
- Follower growth stalls or goes negative -> trigger "growth-stall"

Each anomaly trigger automatically feeds into the `autonomous-optimization` drill's Phase 2 (Diagnose).

**Automate weekly and monthly reports:**
- Weekly report (Monday 9am): executive summary, key metrics vs 4-week average, top/bottom posts, recommended experiments
- Monthly deep-dive (first Monday): pillar ranking, format ranking, audience evolution, pipeline attribution, experiment results, efficiency trends

### 2. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the social content play:

**Phase 1 — Monitor (daily via n8n cron):**
1. Pull the play's primary KPIs from PostHog: engagement rate, impressions per post, leads per week, meetings per week.
2. Compare last 2 weeks against 4-week rolling average.
3. Classify: normal (±10%), plateau (±2% for 3+ weeks), drop (>20% decline), spike (>50% increase).
4. If normal: log to Attio, no action.
5. If anomaly detected: trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
1. Gather context from PostHog: 8-week content performance history broken down by pillar, format, hook type, posting time, and CTA type.
2. Pull current content configuration from Attio: active pillars, posting cadence, AI generation parameters.
3. Run `hypothesis-generation` with the anomaly data and context.
4. Receive 3 ranked hypotheses. Example hypotheses for this play:
   - "Engagement declined because the 'scaling teams' pillar has saturated — audience has seen 12 posts on this topic in 8 weeks. Switch to the 'pricing mistakes' pillar for 2 weeks."
   - "Impressions dropped because posting time shifted. Move LinkedIn posts from 9am to 7:30am to catch the morning commute window."
   - "Lead conversion declined because CTAs switched from action ('DM me playbook') to question ('thoughts?'). Revert to action CTAs."
5. Store hypotheses in Attio. If top hypothesis is high-risk (affects >50% of content or requires budget changes >20%), send Slack alert for human review and STOP.
6. If low or medium risk: proceed to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
1. Take the top-ranked hypothesis.
2. Design the experiment using PostHog experiments: split content between control (current approach) and variant (hypothesis change).
3. Implement the variant. Examples of content experiments:
   - **Pillar rotation**: Publish 50% of posts from current top pillar and 50% from proposed new pillar. Compare leads per post.
   - **Hook style**: Generate half the batch with story hooks and half with data hooks. Compare engagement rate.
   - **Posting time**: Schedule half the posts at current time and half at proposed time. Compare impressions.
   - **CTA type**: Alternate between action CTAs and question CTAs. Compare DM rate.
   - **Content length**: Alternate between short (100-150 words) and long (250-350 words). Compare engagement and leads.
4. Set experiment duration: minimum 14 days or until 20+ posts per variant, whichever is longer. Content experiments need more observations than web experiments because each post is unique.
5. Log experiment start in Attio: hypothesis, start date, expected duration, success metric, control and variant definitions.

**Phase 4 — Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog.
2. Run `experiment-evaluation` comparing control vs variant on the primary metric.
3. Decision:
   - **Adopt**: Variant outperformed control with ≥95% confidence. Update the content generation pipeline to use the winning approach permanently. Log the change.
   - **Iterate**: Results suggest a direction but are not conclusive. Generate a refined hypothesis based on this result. Return to Phase 2.
   - **Revert**: Variant underperformed or no significant difference. Restore control configuration. Log the failure and the learning.
   - **Extend**: Insufficient data. Continue the experiment for another 14 days.
4. Store the full evaluation in Attio: decision, confidence level, impact on primary metric, reasoning.

**Phase 5 — Report (weekly via n8n cron):**
1. Aggregate all optimization activity for the week: anomalies detected, hypotheses generated, experiments running, decisions made.
2. Calculate: net metric change from all adopted changes this week.
3. Generate a weekly optimization brief:
   - What changed and why
   - Net impact on leads per week and meetings per week
   - Current distance from estimated local maximum
   - Recommended focus for next week
4. Post to Slack and store in Attio.

### 3. Implement play-specific optimization targets

Beyond the generic optimization loop, configure these social-content-specific optimization areas:

**Content pillar optimization:**
- Track leads per post by pillar. When a pillar's lead rate drops below 50% of the best-performing pillar for 4 consecutive weeks, propose retiring it.
- When a new industry trend or ICP pain point emerges (detected via engagement spikes on related content from other accounts), propose testing a new pillar.

**Audience evolution monitoring:**
- Monthly: pull follower demographics from Taplio/Shield. Compare to ICP definition.
- If follower base is drifting away from ICP (e.g., too many students, too many non-buyers), adjust content pillars to re-attract the target audience.
- If follower base is closely matching ICP, increase CTA aggressiveness (more "DM me" and "book a call" prompts).

**Platform mix optimization:**
- Compare leads per hour invested by platform (LinkedIn vs Twitter/X).
- If one platform produces 3x more leads per unit effort, propose shifting 70% of effort to that platform.
- If both platforms produce similar results, maintain equal split for audience diversification.

### 4. Maintain convergence tracking

Track the optimization loop's progress toward the local maximum:

- After each adopted experiment, record the percentage improvement on the primary metric.
- When 3 consecutive experiments produce <2% improvement, declare convergence.
- At convergence:
  1. The play has reached its local maximum for the current audience, content approach, and market conditions.
  2. Reduce monitoring frequency from daily to weekly.
  3. Reduce experiment cadence from 2-4/month to 1/month (maintenance experiments).
  4. Report: "Social content play is optimized. Current performance: [X leads/week, Y meetings/week, Z engagement rate]. Further gains require strategic changes (new platform, new audience segment, product-led content) rather than tactical optimization."

### 5. Handle long-term content decay

Social content has a unique challenge: audience fatigue. Even optimized content eventually loses effectiveness as the audience has "heard it all."

Configure the agent to detect content decay signals:
- Engagement rate declining despite no other changes (3+ weeks of steady decline)
- Follower growth stalling while publishing cadence is stable
- DM volume declining while engagement stays stable (audience is engaging but not converting)

When decay is detected, the agent should propose strategic interventions:
- Introduce a new content format (video, carousels, live sessions) that the founder has not tried
- Test a new platform (YouTube Shorts, LinkedIn newsletters, Substack)
- Propose a "content reset" — 1 week of no posting followed by a high-impact return post
- Flag for founder review: "The current content approach may have reached its ceiling. Consider these strategic pivots: [options]."

**Human action required:** Strategic pivots require founder approval. The agent proposes, the founder decides.

## Time Estimate

- Performance monitor setup: 8 hours (one-time)
- Autonomous optimization loop configuration: 6 hours (one-time)
- Weekly monitoring and report review (24 weeks x 30 min): 12 hours
- Experiment design and implementation (12-16 experiments x 2 hours): 24-32 hours
- Monthly deep-dive reviews (6 x 2 hours): 12 hours
- Strategic intervention reviews (as needed): 4 hours
- Convergence documentation: 2 hours
- **Total: ~70 hours active work over 6 months** (budget allows 200 hours including agent compute and iteration)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| LinkedIn (free account) | Publishing, engagement, DMs | Free |
| Taplio | LinkedIn analytics + scheduling + AI assist | ~$49/mo (https://taplio.com/pricing) |
| Typefully or Buffer | Cross-platform scheduling | ~$12-25/mo (https://typefully.com/pricing / https://buffer.com/pricing) |
| PostHog | Event tracking, experiments, anomaly detection | Free up to 1M events/mo (https://posthog.com/pricing) |
| Clay | Lead enrichment | From $149/mo (https://www.clay.com/pricing) |
| Anthropic Claude API | Content generation, hypothesis generation, experiment evaluation | ~$5-15/mo (https://www.anthropic.com/pricing) |
| n8n (self-hosted) | Automation: monitoring, publishing, reporting | Free self-hosted (https://n8n.io/pricing) |
| Attio | CRM + optimization audit trail | Free up to 3 users (https://attio.com/pricing) |

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics -> detect anomalies -> generate hypotheses -> run A/B experiments -> evaluate results -> auto-implement winners -> weekly optimization briefs
- `autonomous-optimization` — play-specific dashboard, anomaly detection, content-to-pipeline attribution, and weekly/monthly reporting
