---
name: collaborative-features-durable
description: >
  Multiplayer Product Features — Durable Intelligence. Always-on AI agents continuously optimize
  collaboration adoption, viral loops, and team retention. The autonomous-optimization drill runs
  the core loop: detect metric anomalies in collaboration health -> generate improvement hypotheses
  -> run A/B experiments -> evaluate results -> auto-implement winners. Weekly optimization briefs.
  Converges when successive experiments produce <2% improvement.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving collaboration ratio ≥50% and viral coefficient k ≥ 0.3 over 6 months via autonomous agent-driven optimization"
kpis: ["Collaboration ratio (7d)", "Viral coefficient (k-factor)", "Retention lift (30d)", "Experiment velocity", "Agent optimization lift"]
slug: "collaborative-features"
install: "npx gtm-skills add product/retain/collaborative-features"
drills:
  - autonomous-optimization
---

# Multiplayer Product Features — Durable Intelligence

> **Stage:** Product → Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The collaboration system runs autonomously. AI agents continuously monitor collaboration health, detect when adoption or viral metrics degrade, experiment with improved invite flows and sharing surfaces, and auto-implement winners. The `autonomous-optimization` drill runs the core loop: detect metric anomalies in collaboration performance -> generate improvement hypotheses -> run A/B experiments -> evaluate results -> auto-implement winners. Weekly optimization briefs report what changed and why. The system converges when successive experiments produce <2% improvement, indicating collaboration has reached its local maximum for your product and user base.

## Leading Indicators

- Autonomous optimization loop running daily, generating at least 1 experiment per month
- Collaboration ratio stable above 50% for 4+ consecutive weeks
- Viral coefficient (k-factor) stable above 0.3 or trending upward
- Weekly optimization briefs being generated and posted to Slack
- At least 1 experiment adopted in the first month (invite flow change, sharing surface tweak, or amplification message update)
- Convergence detection active — system identifies when optimization has plateaued per dimension
- Collaboration health digest showing no sustained anomalies for 3+ consecutive weeks

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the collaborative-features play. This creates the always-on agent loop with 5 phases:

**Phase 1 — Monitor (daily via n8n cron):**
The agent checks collaboration play KPIs daily using `posthog-anomaly-detection`:
- Collaboration ratio (7d rolling)
- Invite acceptance rate (14d rolling)
- Viral coefficient (weekly k-factor)
- Retention lift (30d, team vs. solo)
- Solo-to-Multiplayer funnel conversion at each step
- Content sharing velocity (shares per active user per week)
- Invite propagation rate (% of invitees who re-invite)
- Average team size across active workspaces
- Collaboration-driven signup attribution rate

Classify each metric: normal (within +/-10% of 4-week average), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase). If anomaly detected, trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
The agent gathers context from Attio (current invite flow configuration, sharing surfaces, amplification messages, engagement score weights) and 8-week metric history from PostHog. Runs `hypothesis-generation` to produce 3 ranked hypotheses. Examples of collaboration-specific hypotheses:

- "Collaboration ratio dropped because invite acceptance rate declined 25%. Hypothesis: the invite email subject line has gone stale — test 3 new variants emphasizing the inviter's specific content rather than generic product messaging."
- "Viral coefficient declined from 0.35 to 0.22 because share-to-signup conversion dropped. Hypothesis: the share landing page CTA is below the fold on mobile. Test a sticky mobile CTA bar."
- "Retention lift eroded from 25pp to 18pp because solo users improved (good) but team users declined. Hypothesis: team workspaces with 3+ members are experiencing collaboration noise (too many notifications). Test a 'quiet hours' default setting for larger teams."
- "Invite propagation rate dropped — activated invitees are not re-inviting. Hypothesis: the onboarding flow for invited users does not surface the invite mechanism. Test adding an 'Invite your own teammates' step at the end of invitee onboarding."
- "Co-editing session count dropped 30% while team size stayed flat. Hypothesis: users are collaborating asynchronously (comments, shares) instead of synchronously. This is fine for retention — adjust the collaboration ratio definition to weight async collaboration higher."

Store hypotheses in Attio. If risk = "high" (e.g., changing the share landing page for all public links), send Slack alert for human review. If risk = "low" or "medium", proceed automatically.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
Design and run the experiment using PostHog feature flags:

- **Invite flow experiments:** Split new solo users into control and variant cohorts. Variant receives the modified invite prompt (timing, copy, mechanism, or follow-up sequence). Measure `team_invite_sent` and `team_invite_accepted` rates. Minimum 200 users per variant.
- **Sharing surface experiments:** Split users approaching a share moment into control and variant. Variant sees modified share CTA, landing page, or social proof. Measure `content_shared` rate and downstream `shared_content_viewed` → signup conversion.
- **Amplification message experiments:** Split power collaborators into control and variant. Variant receives modified engagement messages (different frequency, copy, or metrics highlighted). Measure continued sharing/inviting velocity.
- **Retention intervention experiments:** Split at-risk team workspaces into control and variant. Variant receives modified re-engagement (different message, different channel, or different timing). Measure 14-day re-activation rate.

Minimum experiment duration: 14 days or 200 users per variant, whichever is longer. Log experiment start in Attio.

**Phase 4 — Evaluate (triggered by experiment completion):**
Pull results from PostHog. Run `experiment-evaluation`:
- **Adopt:** Variant outperforms control by 5%+ with 95% confidence. Update live configuration. Log the change.
- **Iterate:** Results inconclusive or mixed (primary metric improved but secondary metric degraded). Generate a refined hypothesis. Return to Phase 2.
- **Revert:** Control outperforms variant. Disable variant. Log the failure and reasoning. Return to Phase 1.
- **Extend:** Insufficient data. Run for another period.

Store full evaluation in Attio with decision, confidence, reasoning, and net metric impact.

**Phase 5 — Report (weekly via n8n cron):**
Generate weekly optimization brief:
```
## Collaboration Optimization Brief — Week of {date}

### Anomalies Detected
- {metric}: {classification} ({value} vs {4-week avg})

### Experiments Active
- {experiment_name}: {status}. {days remaining or results}

### Decisions Made
- {experiment_name}: {decision}. Net impact: {metric change}

### Collaboration Health
| Metric | This Week | 4-Week Avg | Target | Status |
|--------|-----------|------------|--------|--------|
| Collaboration Ratio | {pct}% | {pct}% | ≥50% | {on/below target} |
| Viral Coefficient (k) | {value} | {value} | ≥0.3 | {on/below target} |
| Invite Acceptance Rate | {pct}% | {pct}% | ≥40% | {on/below target} |
| Retention Lift (30d) | {pp}pp | {pp}pp | ≥20pp | {on/below target} |
| Invite Propagation Rate | {pct}% | {pct}% | ≥15% | {on/below target} |
| Collab-Driven Signups | {pct}% | {pct}% | ≥10% | {on/below target} |
| Avg Team Size | {value} | {value} | trending up | {up/down/flat} |

### Viral Loop Performance
| Loop | Cycle Time | Step Conversion | Volume/Week | Trend |
|------|-----------|-----------------|-------------|-------|
| Invite | {days} | {pct}% per step | {count} | {up/down/flat} |
| Share | {days} | {pct}% per step | {count} | {up/down/flat} |
| Co-edit | {days} | {pct}% per step | {count} | {up/down/flat} |

### Convergence Status
- Consecutive experiments with <2% improvement: {count}/3
- Estimated distance from local maximum: {assessment}
- Dimensions converged: {list or "none yet"}

### Recommended Focus Next Week
- {recommendation based on data}
```

Post to Slack and store in Attio.

Estimated time for setup: 20 hours. Then always-on.

### 2. Run continuous collaboration health monitoring

Run the `autonomous-optimization` drill at Durable level. Enhance it beyond Scalable:

- **Cross-workspace pattern detection:** When 5+ workspaces show the same collaboration decline pattern (e.g., co-editing drops after team size exceeds 5), flag it as a systemic product issue rather than individual workspace problems. Feed this into the autonomous optimization loop as a high-priority anomaly.
- **Seasonal pattern learning:** Over 6 months, the monitor should detect weekly and monthly patterns (e.g., collaboration dips on Fridays, spikes Monday-Wednesday). Exclude known patterns from anomaly detection to reduce false positives.
- **Cohort lifecycle tracking:** Track collaboration adoption curves by signup cohort month. Compare: are newer cohorts adopting collaboration faster than older cohorts? If yes, product improvements are working. If no, the collaboration experience may be degrading or market expectations are changing.
- **Per-workspace health scoring:** Continue daily scoring from the drill. At Durable, add trend prediction: using 4 weeks of history, predict which "Healthy" workspaces will become "Stalling" in the next 2 weeks and intervene early.

Estimated time: 10 hours enhancement, then always-on.

### 3. Sustain and extend network-effect amplification

Continue running the the collaboration network effects workflow (see instructions below) drill from Scalable. At Durable level, enhance:

- **Dynamic amplification:** Instead of static messages to power collaborators, personalize based on their specific impact data. "Your shared dashboard was forked by 8 teams this month — you're one of our top contributors" performs better than generic engagement numbers.
- **Cross-pollination:** When the agent detects that two workspaces are working on similar content types but are not connected, suggest collaboration between them (for products where inter-workspace collaboration is appropriate). This creates new network effect paths that did not exist organically.
- **Referral attribution depth:** Track network depth beyond first-degree invites. Compute: "User A invited User B, who invited User C, who invited User D." Report the deepest invite chains and the content that triggered them. Invite chains of depth 3+ indicate strong product-market fit for collaboration.
- **Viral coefficient decomposition:** Break k-factor into invite-k and share-k weekly. Track which experiments affected which component. When one component plateaus, shift optimization focus to the other.

Estimated time: 10 hours enhancement, then always-on.

### 4. Guardrails (CRITICAL)

The autonomous optimization loop must respect these constraints:

- **Rate limit:** Maximum 1 active experiment per collaboration dimension (invites, sharing, co-editing, retention) at a time. Never test invite timing and invite mechanism simultaneously.
- **Revert threshold:** If collaboration ratio drops >15% at any point during an experiment, auto-revert immediately and alert the team.
- **Human approval required for:**
  - Changes to the share landing page that affect all public links
  - Invite email changes that affect the sender name or reply-to address
  - Any experiment touching the co-editing experience (high risk of UX regression)
  - Changes to notification frequency for team workspaces (risk of churn from notification fatigue)
  - Any change the hypothesis generator flags as "high risk"
- **Cooldown:** After a failed experiment, wait 7 days before testing a new hypothesis on the same dimension.
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for human strategic review.
- **Never optimize what is not measured:** If a collaboration metric does not have PostHog tracking, fix tracking first (use the collaboration instrumentation workflow (see instructions below) drill) before running experiments on it.
- **Protect the viral loop:** Never run an experiment that could break an existing positive viral loop. Always include the viral coefficient as a guardrail metric in every experiment.

### 5. Convergence detection

The optimization loop runs indefinitely at Durable level. Detect convergence per dimension:

- **Invite optimization:** Track improvement % of each successive invite experiment. When 3 consecutive invite experiments produce <2% improvement on invite acceptance rate, declare invite optimization converged.
- **Sharing optimization:** Same threshold for share-to-signup conversion experiments.
- **Amplification optimization:** Same threshold for amplification message engagement experiments.
- **Retention optimization:** Same threshold for team retention intervention experiments.

At convergence for all dimensions:
1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment frequency to 1 per quarter (maintenance mode)
3. Report: "Collaboration features are optimized. Current performance: collaboration ratio {pct}%, viral coefficient k={value}, retention lift {pp}pp. Further gains require product changes (new collaboration features, deeper integrations, or new sharing surfaces) rather than tactical optimization of existing features."
4. Continue watching for external changes that break convergence: competitor launches, user behavior shifts, product changes that affect collaboration flows

### 6. Evaluate sustainability

Measure continuously against threshold: Sustained or improving collaboration ratio ≥50% and viral coefficient k ≥ 0.3 over 6 months.

Monthly review checklist:
- Collaboration ratio: still ≥50%? Trend direction?
- Viral coefficient: still ≥0.3? Which component (invite or share) is stronger?
- Retention lift: team vs. solo gap maintained at ≥20pp?
- Experiment velocity: at least 2 experiments completed this month?
- Adopted experiments: at least 1 winner implemented this month (or convergence detected)?
- Network depth: are invite chains getting deeper or shallower?
- Collaboration-driven signups: still ≥10% of new signups?
- Workspace health: are "Thriving" workspaces growing as a % of total?

This level runs continuously. If metrics sustain or improve, the play is durable. If metrics decay, diagnose whether the cause is market saturation (most potential collaborators already on the platform), product fatigue (collaboration features need refresh), competitive pressure (a competitor launched better collaboration), or seasonal patterns.

## Time Estimate

- Autonomous optimization setup: 20 hours
- Collaboration health monitoring enhancement: 10 hours
- Network-effect amplification enhancement: 10 hours
- Ongoing monitoring, experiment review, and strategic oversight: ~110 hours over 6 months (~4-5 hours/week)

**Total: ~150 hours over 6 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Dashboards, funnels, feature flags, experiments, anomaly detection, cohorts | Standard stack (excluded) |
| n8n | Orchestration — optimization loop, health monitor, amplification engine, scoring pipeline | Standard stack (excluded) |
| Attio | Experiment logs, workspace health scores, collaboration champion lists, network attribution | Standard stack (excluded) |
| Intercom | In-app messages for experiment variants, amplification, and retention interventions | Proactive Support: $349/mo. [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Lifecycle emails for invite sequences, power collaborator engagement, re-engagement campaigns | $49/mo (up to 5,000 contacts). [loops.so/pricing](https://loops.so/pricing) |
| Anthropic API | Claude for optimization loop (hypothesis generation, experiment evaluation, weekly briefs) | ~$30-100/mo at Durable volume (Sonnet 4.6: $3/$15 per MTok). [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Play-specific cost: ~$80-500/mo** (Loops $49/mo + Anthropic API ~$30-100/mo; Intercom Proactive Support $349/mo if not already active)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor collaboration metrics daily, diagnose anomalies, generate hypotheses, run experiments on invite flows and sharing surfaces, evaluate results, auto-implement winners, generate weekly optimization briefs
- `autonomous-optimization` — enhanced at Durable with cross-workspace pattern detection, seasonal pattern learning, cohort lifecycle tracking, and predictive workspace health scoring
- the collaboration network effects workflow (see instructions below) — enhanced at Durable with dynamic amplification, cross-pollination suggestions, deep referral attribution, and viral coefficient decomposition
