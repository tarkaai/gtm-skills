---
name: youtube-preroll-ads-scalable
description: >
  YouTube Pre-roll Ads — Scalable Automation. Scale to $3,000-10,000/mo with automated
  creative testing, AI-driven placement discovery, cross-platform retargeting, and
  n8n-managed campaign operations. Hit ≥ 50 qualified leads from 500,000+ views
  over 4 months without proportional increase in manual effort.
stage: "Marketing > Problem Aware"
motion: "Lightweight Paid"
channels: "Paid, Content"
level: "Scalable Automation"
time: "75 hours over 4 months"
outcome: "≥ 500,000 views and ≥ 50 qualified leads from $10,000/month over 4 months"
kpis: ["Cost per qualified lead (CPqL)", "View rate (VTR)", "View-to-lead conversion rate", "Creative refresh rate (new variants per 2-week cycle)", "Audience discovery rate (new channels added per month)", "Blended ROAS from YouTube-sourced pipeline"]
slug: "youtube-preroll-ads"
install: "npx gtm-skills add marketing/problem-aware/youtube-preroll-ads"
drills:
  - ab-test-orchestrator
  - youtube-preroll-audience-builder
  - dashboard-builder
  - tool-sync-workflow
  - budget-allocation
  - threshold-engine
---

# YouTube Pre-roll Ads — Scalable Automation

> **Stage:** Marketing → Problem Aware | **Motion:** Lightweight Paid | **Channels:** Paid, Content

## Outcomes

Generate at least 500,000 views and 50 qualified leads over 4 months with $3,000-10,000/mo spend. The 10x multiplier at this level comes from three things: (1) systematic creative testing that finds winning video hooks faster, (2) automated placement discovery that continuously finds new channels your ICP watches, and (3) cross-platform retargeting that nurtures video viewers across YouTube, Display, and email without manual intervention.

At Scalable, the agent manages campaigns weekly. A human reviews the weekly report, produces new videos from agent-generated briefs, and approves major changes (new pain points, budget increases above 30%). The human does NOT need to log into Google Ads daily.

## Leading Indicators

- New video ad variants launched every 2 weeks (creative pipeline is not stalling)
- Winner variant VTR is at least 1.3x the average (testing is finding real winners)
- CPqL stays within 20% of Baseline CPqL despite higher spend (scale is not degrading quality)
- Retargeting conversion rate stays 2x+ higher than cold traffic (retargeting pool is healthy)
- New placements discovered and added monthly (audience is not saturating)
- CRM pipeline from YouTube preroll grows month-over-month (leads are converting downstream)

## Instructions

### 1. Scale to 3 pain points and all audience types

If you ran 2 pain points in Baseline, add a third. For each pain point, run all 3 audience types:

Run the `youtube-preroll-audience-builder` drill at scalable volume:
- **Placements:** 100-200 channels + 50 specific video placements. Use YouTube Data API to auto-discover new channels weekly: search for videos published in the last 30 days that match your pain point keywords, extract their channel IDs, filter by subscriber count.
- **Custom intent:** 3 segments (one per pain point, 10-15 keywords each)
- **Topics + Affinity:** Broader targeting as a discovery layer. Layer topic targeting with in-market audiences for "Business Software" or "IT Services."

Each audience type runs in its own campaign. Each pain point runs in its own ad group within each campaign. This gives you a clean matrix for performance analysis.

### 2. Set up systematic A/B testing

Run the `ab-test-orchestrator` drill configured for YouTube pre-roll:

**What to test (in priority order):**
1. Hook type: Does stat, question, or proof hook produce the lowest CPqL?
2. Pain point: Which of 3 pain points generates the most qualified leads?
3. Video length: 15s vs. 30s vs. 60s for skippable in-stream
4. CTA type: "Download guide" vs. "Watch full breakdown" vs. "Get the checklist"
5. Audience type: Placements vs. custom intent vs. topics — which produces the highest-quality leads?

**Testing framework:**
- Run each test for 7 days minimum or until each variant has 5,000+ impressions
- Primary metric: Cost per qualified lead (CPqL, not just CPL — must be ICP-match)
- Secondary metric: Lead-to-meeting conversion rate (check 14 days after lead capture)
- Use PostHog experiments to track which variant each lead came from and measure downstream conversion

**Automation:**
Build an n8n workflow that runs daily:
1. Pull per-variant performance from Google Ads Reporting API
2. For each active variant, check: impressions >= 5,000 AND VTR < 10%
3. If both conditions met, pause the variant via the API
4. Send a summary to Slack: "Paused variant X (VTR 7.2% after 6,800 impressions). Top performer is variant Y (VTR 22%, CPqL $38)."

### 3. Build automated placement discovery

Create an n8n workflow that runs weekly:

1. Use YouTube Data API to search for videos published in the last 7 days matching each pain point's keywords
2. For each video with 10,000+ views, extract the channel ID
3. Check if the channel is already in your placement list
4. For new channels: pull subscriber count, upload frequency, recent video titles
5. Filter: 10,000-2,000,000 subscribers, 2+ uploads/month, content relevant to your ICP
6. Add qualifying channels to a "new placement candidates" list in Attio
7. Once per week, the agent adds verified candidates to the Google Ads placement targeting

**Human action required:** Review the new placement candidates weekly. The agent should flag any channels that look borderline (e.g., entertainment channels that happen to mention tech). Human approves or rejects.

### 4. Build cross-platform retargeting

Run the `tool-sync-workflow` drill to connect YouTube data to other channels:

**YouTube viewer to Display retargeting:**
- Create remarketing audiences in Google Ads based on video interaction: viewers who watched 25%+, 50%+, 75%+, and 100%
- Run display retargeting (banner ads on Google Display Network) to 75%+ viewers with a different CTA format
- Also run YouTube bumper ads (6s) to 50%+ viewers who did not click

**YouTube lead to Email nurture sync:**
- When a lead converts from YouTube, the the youtube preroll lead routing workflow (see instructions below) drill already triggers Loops nurture
- Sync converted leads back to Google Ads as a Customer Match exclusion list (do not retarget people who already converted)

**CRM to Google Ads feedback loop:**
- Export closed-won customers from Attio weekly via n8n: upload as Customer Match exclusion AND as a source for Similar Audiences
- Export qualified leads from Attio: use for Similar Audience targeting (Google's equivalent of lookalikes)

### 5. Scale budget with automated guardrails

Run the `budget-allocation` drill with scalable-specific rules:

**Budget scaling protocol:**
- If blended CPqL is below target for 2 consecutive weeks, increase total budget by 20%
- If blended CPqL exceeds target by 20% for 1 week, freeze budget and diagnose
- If any single campaign's CPqL exceeds 2x target for 5 days, reduce that campaign's budget by 30%
- Maximum single budget increase: 30% per month

**Automate via n8n:**
Build a workflow that runs every Monday:
1. Pull last 7 days of spend, views, and lead data from Google Ads + PostHog
2. Calculate blended CPqL and per-campaign CPqL
3. Compare against target CPqL
4. If scaling conditions are met, adjust daily budgets via Google Ads API
5. Log the adjustment in PostHog: `yt_preroll_budget_adjusted`, with properties `direction`, `amount`, `reason`

**Human action required:** Set a maximum monthly budget cap that the automation cannot exceed. Review and approve any budget increase above $5,000/mo.

### 6. Produce creative at scale

Run the the youtube preroll creative pipeline workflow (see instructions below) drill on a 2-week cadence:
- Every 2 weeks: agent generates 5-8 new creative briefs using Anthropic API
- Use winning patterns from A/B tests: if stat hooks on pain point 2 are winning, generate more stat hooks with different data points for that pain point
- Test at least one entirely new angle each cycle (new pain point, new format, new length)
- Archive every variant's performance data: variant_id, pain_point, hook_type, video_length, VTR, CTR, CPqL, lead_quality_score

**Human action required:** Produce the videos from the briefs. At scalable volume, consider batching: record 5-8 videos in a single 2-hour session every 2 weeks.

Over 4 months, you should produce and test 30-50 unique video ad variants. Your top 5-8 performers will drive the majority of leads.

### 7. Set up performance monitoring

Run the `dashboard-builder` drill:
- Daily automated health checks with alerts on VTR drops, CPqL spikes, budget pacing issues
- Creative fatigue detection: auto-pause variants with 30%+ VTR decay after 14 days
- Audience saturation detection: flag campaigns where frequency exceeds 4 and CPqL is rising
- Weekly performance report to Slack with headline metrics, top/bottom variants, and one specific recommendation

### 8. Evaluate against threshold

Run the `threshold-engine` drill at months 1, 2, 3, and 4.

**Month 1 checkpoint:** ≥ 100,000 views and ≥ 10 qualified leads. If behind pace, diagnose and adjust.

**Month 2 checkpoint:** Cumulative ≥ 200,000 views and ≥ 20 qualified leads.

**Month 4 final:** Cumulative ≥ 500,000 views and ≥ 50 qualified leads over the full period.

Also evaluate operational metrics:
- Is creative production keeping pace? (new variants every 2 weeks)
- Is placement discovery finding new channels? (10+ new channels per month)
- Is lead routing still working? (check for n8n workflow failures)
- Are leads converting downstream? (check meeting rate and pipeline value from Attio)

Decision:
- **PASS:** 50+ qualified leads, CPqL within target, automation running smoothly, creative pipeline producing regularly. Proceed to Durable.
- **MARGINAL:** 30-49 leads or 50+ leads but CPqL 20%+ above target. Extend Scalable by 1 month. Focus on the weakest area (creative, audiences, or landing page).
- **FAIL:** <30 leads despite $3,000+/mo spend. Re-evaluate whether YouTube pre-roll is the right channel for your ICP. Consider: is the video quality holding back CTR? Is the landing page converting? Are you reaching the right channels? If fundamentals are sound but volume is the problem, consider combining YouTube pre-roll with a complementary play (LinkedIn thought leader ads, podcast sponsorships).

## Time Estimate

- 10 hours: Cross-platform retargeting + CRM sync setup (one-time)
- 6 hours: A/B test framework and n8n automation for campaign management (one-time)
- 6 hours: Performance monitoring setup (one-time)
- 4 hours: Automated placement discovery workflow (one-time)
- 4 hours bi-weekly: Creative brief generation + video production coordination
- 2 hours weekly: Performance review
- 4 hours: Month 1-3 checkpoint analyses
- 4 hours: Month 4 final evaluation and documentation

Total: ~75 hours over 4 months (front-loaded in first 2 weeks, then ~4 hrs/week ongoing)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Google Ads (YouTube) | Video ad platform | $3,000-10,000/mo ad spend. CPV $0.02-0.10. [Pricing](https://ads.google.com/home/pricing/) |
| YouTube Data API | Automated placement discovery | Free (10,000 units/day quota). [Pricing](https://developers.google.com/youtube/v3/getting-started#quota) |
| Clay | Lead enrichment and ICP scoring | $149-$349/mo depending on volume. [Pricing](https://clay.com/pricing) |
| Loops | Nurture sequences | Free up to 1,000 contacts, then $49/mo. [Pricing](https://loops.so/pricing) |
| PostHog | Experiments, funnels, event tracking | Free up to 1M events/mo. [Pricing](https://posthog.com/pricing) |
| n8n | Campaign automation, lead routing, placement discovery, monitoring | Free self-hosted or $20-50/mo cloud. [Pricing](https://n8n.io/pricing) |
| Webflow | Landing pages | $14-23/mo. [Pricing](https://webflow.com/pricing) |
| Descript | Video production | $24/mo. [Pricing](https://www.descript.com/pricing) |
| Anthropic API | Creative brief generation | ~$0.50-2.00 per batch of 8 briefs (Claude Sonnet). [Pricing](https://www.anthropic.com/pricing) |

**Estimated scalable monthly cost:** $3,000-10,000 ad spend + ~$500-700 tooling = $3,500-10,700/mo

## Drills Referenced

- `ab-test-orchestrator` — systematic creative and audience testing with statistical rigor
- the youtube preroll creative pipeline workflow (see instructions below) — bi-weekly creative brief generation and testing (30-50 variants over 4 months)
- `youtube-preroll-audience-builder` — 100-200 placements with automated weekly discovery
- `dashboard-builder` — daily health checks, fatigue detection, weekly reports
- `tool-sync-workflow` — sync CRM, PostHog, and Google Ads bidirectionally via n8n
- `budget-allocation` — automated budget scaling with per-campaign CPqL guardrails
- `threshold-engine` — evaluate at monthly checkpoints and month 4 final
