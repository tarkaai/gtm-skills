---
name: google-display-network-campaigns-scalable
description: >
  Google Display Network — Scalable Automation. Find the 10x multiplier for display ads
  with AI-driven creative scaling, automated placement curation, systematic A/B testing,
  cross-platform expansion to Meta Audience Network, and lookalike audience building.
stage: "Marketing > SolutionAware"
motion: "LightweightPaid"
channels: "Paid"
level: "Scalable Automation"
time: "60 hours over 3 months"
outcome: ">=50 qualified leads/month from $8,000-12,000/month display spend with CPA <=$180 sustained for 3 months"
kpis: ["Monthly qualified leads (target >=50)", "CPA (target <=$180, trending stable or declining)", "Creative refresh rate (new variants per month)", "ICP match rate (target >=55%)", "Retargeting conversion rate vs cold (target >=3x)", "Cross-platform ROAS"]
slug: "google-display-network-campaigns"
install: "npx gtm-skills add marketing/solution-aware/google-display-network-campaigns"
drills:
  - ab-test-orchestrator
  - tool-sync-workflow
---

# Google Display Network — Scalable Automation

> **Stage:** Marketing → SolutionAware | **Motion:** LightweightPaid | **Channels:** Paid

## Outcomes

Find the 10x multiplier. At Baseline, you proved GDN produces qualified leads at a sustainable CPA. At Scalable, you remove the bottleneck that limits volume: creative fatigue. Display campaigns die when the audience sees the same banners for too long. This level automates creative production with AI-assisted generation, deploys systematic A/B testing to find winning patterns, automates placement curation (adding good sites, excluding bad ones), expands cross-platform to Meta Audience Network, and builds lookalike audiences from your converting leads. The agent handles creative rotation, placement hygiene, and budget reallocation. The human reviews weekly performance and approves new creative concepts.

**Pass threshold:** >=50 qualified leads/month from $8,000-12,000/month display spend with CPA <=$180 sustained for 3 months.

## Leading Indicators

- Creative pipeline never runs dry: at least 5 ad variants in the staging queue at all times
- No creative runs for more than 21 days without refresh
- Placement exclusion list growing weekly (agent is actively curating)
- Cross-platform reporting shows distinct audience segments on GDN vs Meta (not duplicating reach)
- A/B tests producing at least 1 winning variant per month
- ICP match rate stable or improving as volume scales (quality does not degrade with scale)
- Budget utilization >85% across all campaigns (audience is not exhausted)

## Instructions

### 1. Deploy AI-driven creative scaling

Run the the display creative scaling workflow (see instructions below) drill to build the automated creative production pipeline.

**Configure for this play:**

1. **Analyze Baseline winning patterns:**
   - Pull CTR, conversion rate, and CPA for every creative from Baseline (4+ weeks of data)
   - Segment by: hook type (stat/question/proof), pain point, image style (text overlay vs product screenshot vs illustration), CTA type
   - Document the top 3 winning combinations as the creative playbook

2. **Build the AI creative generation pipeline (n8n + Anthropic API):**
   - Configure the bi-weekly n8n workflow that sends winning patterns + new pain points to Claude
   - Claude generates 5 display ad variants per batch: headline, long headline, description, image concept, CTA
   - Variants enter a staging queue (Attio notes or structured storage)
   - Agent sends staging queue to Slack for human copy approval
   - On approval, agent uploads to Google Ads via API and to Meta Ads Manager

3. **Automate creative fatigue detection (daily n8n workflow):**
   - Query PostHog for CTR by creative_id over last 7 days vs first-week CTR
   - Flag creatives with CTR decline >25% OR age >21 days
   - Auto-pause fatigued creatives and promote next variant from staging queue
   - Log every rotation in Attio: which creative retired, why, what replaced it

4. **Scale to 5-7 pain points:**
   - Expand from Baseline's 3 pain points to 5-7 by mining:
     - Google Ads search query reports (from search ads play if running)
     - PostHog scroll depth data (which landing page sections get most engagement)
     - Customer interview transcripts or support tickets
   - For each new pain point: generate 5 creative variants, create a new ad group, allocate 10% of budget as a test

### 2. Automate placement curation

Build n8n workflows for ongoing placement hygiene:

1. **Weekly placement audit (n8n cron, every Monday):**
   - Pull placement report from Google Ads API for last 7 days
   - Exclude placements with 200+ impressions and zero conversions
   - Exclude placements with CTR <0.05% (likely bot traffic)
   - Flag placements where >50% of impressions are on mobile apps (accidental clicks)
   - Log all exclusions in Attio

2. **Managed placement expansion:**
   - Monthly: research 5-10 new industry publications and blogs relevant to your ICP
   - Use Clay or manual research: find sites where your ICP reads, verified by checking if the site has Google AdSense (required for GDN placement)
   - Add as managed placements in a test ad group with 5% of budget
   - After 2 weeks: promote sites with CTR >0.40% and conversions to the main managed placement campaign

3. **Negative placement list management:**
   - Maintain a master negative placement list (accumulates over time)
   - Share the list across all GDN campaigns
   - Export and store the list monthly in case of accidental deletion

### 3. Deploy systematic A/B testing

Run the `ab-test-orchestrator` drill to set up structured experimentation:

**Month 1 experiments:**
- Test hook types: stat hook vs question hook vs customer proof hook (hold image and CTA constant)
- Minimum: 500 impressions and 20 clicks per variant before declaring a winner

**Month 2 experiments:**
- Test image styles: bold text overlay vs product screenshot vs illustration
- Test CTA types: Learn More vs Download Guide vs See Pricing

**Month 3 experiments:**
- Test audience types: in-market vs custom intent vs lookalike (same creative, different targeting)
- Test landing page variants: long-form vs short-form, video vs no video

**Rules for all tests:**
- One variable at a time per campaign
- 95% statistical confidence required before adopting
- Log every test in Attio: hypothesis, variants, sample size, result, confidence, decision
- Maximum 2 concurrent tests across the display program (one on creative, one on targeting)

### 4. Expand cross-platform to Meta Audience Network

Using the `tool-sync-workflow` drill, extend display ads to Meta:

1. **Export your highest-converting audience data from Google:**
   - Extract converting lead emails from Attio (leads sourced from display-ads with deal created)
   - Hash emails (SHA-256) and upload to Meta as a Custom Audience
   - Build a 1% Lookalike Audience from this seed list

2. **Create Meta Audience Network campaigns:**
   - Campaign 1: Lookalike audience (1% from converting display leads)
   - Campaign 2: Retargeting (website visitors from all display campaigns who did not convert)
   - Placements: Audience Network only (do NOT use Automatic Placements)
   - Budget: 20-30% of total display budget allocated to Meta

3. **Sync creative across platforms:**
   - When a creative wins on GDN, adapt and deploy on Meta within 48 hours
   - Track `creative_concept_id` across both platforms in PostHog to compare the same concept's performance cross-platform
   - GDN: responsive display ads (Google mixes headlines/descriptions)
   - Meta: single image with bold text overlay (more visual, shorter copy)

4. **Build cross-platform exclusions via `cross-platform-retargeting-sync`:**
   - Sync conversion lists across platforms so converted leads are excluded everywhere
   - Sync existing customer lists so you never pay to show ads to customers

### 5. Build lookalike and similar audience expansion

1. From Attio, export your best converting leads from display ads (deal created, ICP score >=70)
2. Upload hashed emails to both Google Ads (Customer Match) and Meta (Custom Audience)
3. Google generates "Similar Audiences" automatically. If unavailable (Google has been phasing these out), build custom audiences using the keywords and URLs that your best leads interacted with before converting
4. Meta generates 1% Lookalike. Test 1% vs 3% vs 5% lookalike to find the sweet spot between reach and quality
5. Allocate 15% of budget to lookalike campaigns as an expansion play

### 6. Scale budget with guardrails

Increase total display budget 20-30% monthly as long as:
- CPA stays within $180 target (or within 110% of previous month)
- ICP match rate stays above 50%
- Budget utilization stays above 85% (audience is not exhausted)

Build n8n guardrail workflows:
- Daily: if any campaign's daily spend exceeds budget by >15%, pause and alert
- Weekly: if CPA exceeds $220 for 7 consecutive days, reduce that campaign's budget by 25% and shift to the lowest-CPA campaign
- Monthly: generate a budget allocation recommendation based on 30-day CPA by campaign type

**Human action required:** Approve monthly budget increases. Review weekly performance brief. Approve new creative concepts from the AI pipeline.

### 7. Evaluate against threshold

At the end of month 3, measure:
- Monthly qualified leads (from Attio: leads with ICP match confirmed, sourced from display-ads)
- CPA by month and by campaign type
- Trend: is CPA stable or declining month-over-month?
- ICP match rate by month
- Cross-platform comparison: GDN CPA vs Meta CPA
- Creative pipeline health: variants in staging queue, average creative lifespan

**Pass:** >=50 qualified leads/month for all 3 months with CPA <=$180. Proceed to Durable.

**Fail -- volume below 50/month:** The display channel may have a ceiling for your market. Before failing: test broader in-market categories, expand geographic targeting, or add Microsoft Advertising display network. If volume still caps, display works but is a supporting channel, not a primary lead source.

**Fail -- CPA above $180:** Creative fatigue or audience exhaustion is degrading efficiency. Accelerate creative refresh cadence (weekly instead of bi-weekly). Test entirely new pain points. Consider narrowing to managed placements only (higher quality, lower waste).

**Fail -- quality degrading (ICP match <45%):** Volume scaling attracted lower-quality traffic. Tighten lookalike percentages (1% instead of 3%). Remove broad in-market categories. Rely more on custom intent with specific solution-comparison keywords.

## Time Estimate

- 12 hours: Build AI creative pipeline, fatigue detection, and staging queue system
- 8 hours: Configure A/B testing framework and first month's experiments
- 10 hours: Set up Meta Audience Network campaigns, cross-platform syncing, and exclusion management
- 6 hours: Build lookalike audiences, budget guardrail workflows, and reporting
- 8 hours: Automated placement curation (weekly workflows, managed placement research)
- 16 hours: Monthly monitoring, creative approval, budget decisions, experiment evaluation (3 months)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Google Ads | Display campaigns (managed placements, custom intent, retargeting, lookalike) | $6,000-8,000/mo ad spend -- [ads.google.com](https://ads.google.com) |
| Meta Ads | Audience Network display (lookalike, retargeting) | $2,000-4,000/mo ad spend -- [ads.meta.com](https://ads.meta.com) |
| PostHog | Analytics, experiments, funnels, cross-platform attribution | Growth ~$50-200/mo -- [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Workflow automation (creative pipeline, placement curation, budget guardrails) | Pro EUR 60/mo -- [n8n.io/pricing](https://n8n.io/pricing) |
| Anthropic API (Claude) | AI creative generation | ~$20-50/mo -- [anthropic.com](https://console.anthropic.com) |
| Clay | Lead enrichment | Explorer $149/mo -- [clay.com/pricing](https://clay.com/pricing) |
| Attio | CRM, experiment log, creative rotation audit trail | Plus $29/user/mo -- [attio.com/pricing](https://attio.com/pricing) |
| Loops | Email nurture sequences | Starter $49/mo -- [loops.so/pricing](https://loops.so/pricing) |

**Estimated play-specific cost:** $8,000-12,000/mo ad spend + ~$350-550/mo tooling + ~$20-50/mo AI compute

## Drills Referenced

- the display creative scaling workflow (see instructions below) -- AI-assisted creative generation pipeline, systematic A/B testing, fatigue detection, cross-platform creative synchronization
- `ab-test-orchestrator` -- Design, run, and evaluate A/B tests on display creative, targeting, and landing pages with statistical rigor
- `tool-sync-workflow` -- Cross-platform audience syncing, conversion exclusion lists, and CRM-to-ad-platform data flows
