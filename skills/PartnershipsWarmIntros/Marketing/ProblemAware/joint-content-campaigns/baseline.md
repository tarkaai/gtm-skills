---
name: joint-content-campaigns-baseline
description: >
  Joint Content Campaigns -- Baseline Run. First always-on content co-creation pipeline.
  Systematize partner outreach, co-produce 3+ assets with multiple partners, track
  per-asset and per-partner performance, and validate that results hold over 8 weeks.
stage: "Marketing > ProblemAware"
motion: "PartnershipsWarmIntros"
channels: "Content, Email"
level: "Baseline Run"
time: "18 hours over 8 weeks"
outcome: ">=3 co-created assets published and >=30 qualified leads in 8 weeks"
kpis: ["Assets published per month", "Qualified leads per asset", "Download-to-lead conversion rate", "Partner-sourced lead percentage", "Time from partner agreement to publication"]
slug: "joint-content-campaigns"
install: "npx gtm-skills add PartnershipsWarmIntros/Marketing/ProblemAware/joint-content-campaigns"
drills:
  - warm-intro-request
  - posthog-gtm-events
  - threshold-engine
---
# Joint Content Campaigns -- Baseline Run

> **Stage:** Marketing -> ProblemAware | **Motion:** PartnershipsWarmIntros | **Channels:** Content, Email

## Outcomes
Three or more co-created content assets published with different partners. At least 30 qualified leads attributed to joint content in 8 weeks. This proves the model is repeatable across multiple partners and topics, not a one-time success.

## Leading Indicators
- 5+ partner outreach conversations active simultaneously
- At least 2 partners agree to collaborate within the first 2 weeks
- Each asset generates downloads from both audiences within 48 hours
- Lead quality from joint content matches or exceeds lead quality from solo content
- Second and third assets produce leads at a rate consistent with the first

## Instructions

### 1. Build a systematic partner outreach pipeline
Run the `warm-intro-request` drill to establish a repeatable process for reaching content partners. For each of the top 10 partners identified at Smoke level (or refreshed via `partner-prospect-research`):
- Identify mutual connections who can make warm introductions
- Craft personalized intro requests that reference the successful Smoke test asset as proof of concept
- Track request-to-intro conversion in Attio

Target: 10 outreach attempts, expecting 3-5 positive responses.

### 2. Configure event tracking for joint content
Run the `posthog-gtm-events` drill to implement standardized tracking for this play. Create these events:
- `content_download` -- fires when a user submits the lead-capture form (properties: `asset_slug`, `partner_slug`, `content_topic`, `utm_source`, `utm_medium`)
- `lead_qualified` -- fires when a downloaded lead meets qualification criteria (properties: `asset_slug`, `partner_slug`, `qualification_method`)
- `meeting_booked` -- fires when a joint-content lead books a call (properties: `source: joint-content`, `asset_slug`, `partner_slug`)

Ensure UTM parameters propagate from email clicks through form submissions to downstream conversion events.

### 3. Co-produce 3+ assets over 8 weeks
Run the the joint content production workflow (see instructions below) drill once per partner collaboration. Stagger production so you are working on multiple assets simultaneously at different stages:
- Week 1-2: Partner A -- topic research and outline
- Week 2-4: Partner A -- drafting and assembly; Partner B -- topic research and outline
- Week 4-6: Partner A -- publication and promotion; Partner B -- drafting; Partner C -- topic research
- Week 6-8: All assets live, monitoring performance

Vary the content format across assets to test what converts best:
- Asset 1: Same format as your Smoke test (known to work)
- Asset 2: Different format (if Smoke was an ebook, try a benchmark report or checklist)
- Asset 3: Experiment with the format that performed best in Assets 1-2

### 4. Track per-asset and per-partner performance
After each asset publishes, monitor in PostHog:
- Downloads by source channel (your email, partner email, organic, social)
- Download-to-qualified-lead conversion rate
- Time from download to meeting booked
- Which partner's audience converts at a higher rate

Update Attio deal records weekly with performance data.

### 5. Evaluate against threshold
Run the `threshold-engine` drill to measure against: >=3 co-created assets published and >=30 qualified leads in 8 weeks.

If PASS: proceed to Scalable. You have proven the model works across multiple partners, topics, and formats.
If FAIL: analyze:
- If 3+ assets published but <30 leads -> topic selection or distribution is weak. Double down on the best-performing topic/format combo.
- If <3 assets published -> partner pipeline is the bottleneck. Increase outreach volume or lower the collaboration bar (shorter assets, less partner effort required).

## Time Estimate
- 3 hours: partner outreach and relationship management across 8 weeks
- 2 hours: PostHog event tracking setup
- 9 hours: content co-production (3 assets x 3 hours each)
- 2 hours: monitoring and analysis
- 2 hours: threshold evaluation and documentation

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM for partner and lead tracking | Free tier available; https://attio.com/pricing |
| Clay | Partner research and enrichment | From $149/mo; https://clay.com/pricing |
| Crossbeam | Account overlap mapping | Free tier available; https://www.crossbeam.com/pricing |
| PostHog | Event tracking and analytics | Free up to 1M events/mo; https://posthog.com/pricing |
| Anthropic Claude | Content drafting | Pay-per-use; https://www.anthropic.com/pricing |
| Ghost | Asset hosting and landing pages | Free self-hosted; https://ghost.org/pricing |
| Loops | Co-promotion email distribution | Free up to 1,000 contacts; https://loops.so/pricing |

## Drills Referenced
- `warm-intro-request` -- systematic warm intro process to reach content partners
- the joint content production workflow (see instructions below) -- end-to-end co-creation per partner asset
- `posthog-gtm-events` -- standardized event tracking for joint content funnel
- `threshold-engine` -- evaluate pass/fail against the 30-lead threshold
