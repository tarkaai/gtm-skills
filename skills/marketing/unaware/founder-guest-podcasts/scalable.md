---
name: founder-guest-podcasts-scalable
description: >
  Founder Guest Podcast — Scalable Automation. Automate podcast discovery, pitch at 50+ shows,
  repurpose every episode into multi-channel content, and drive 10+ inbound leads over 2 months.
stage: "Marketing > Unaware"
motion: "PR & Earned Mentions"
channels: "Content"
level: "Scalable Automation"
time: "40 hours over 2 months"
outcome: "≥ 8 podcast bookings AND ≥ 10 inbound leads from aired episodes over 2 months"
kpis: ["Pitches sent", "Booking rate", "Episodes aired", "Referral traffic", "Leads from podcast traffic", "Content pieces per episode"]
slug: "founder-guest-podcasts"
install: "npx gtm-skills add marketing/unaware/founder-guest-podcasts"
drills:
  - podcast-prospect-research
  - podcast-pitch-outreach
  - podcast-guest-preparation
  - content-repurposing
  - podcast-performance-monitor
  - ab-test-orchestrator
---

# Founder Guest Podcast — Scalable Automation

> **Stage:** Marketing → Unaware | **Motion:** PR & Earned Mentions | **Channels:** Content

## Outcomes

Book 8+ podcast appearances in 2 months and generate 10+ inbound leads from aired episodes. The 10x multiplier comes from two levers: (a) automated prospecting and pitching at higher volume, and (b) repurposing every episode into 5-10 derivative content pieces that extend reach beyond podcast listeners.

## Leading Indicators

- Podcast prospect pipeline refills automatically with 10+ new qualified shows per month
- Booking rate holds steady at ≥ 10% as volume scales from 25 to 50+ pitches
- Each aired episode generates ≥ 3 derivative content pieces
- Content repurposing drives 2-3x more traffic than the episode alone
- Podcast referral traffic grows week-over-week

## Instructions

### 1. Automate podcast prospecting

Run the `podcast-prospect-research` drill at Scalable scale:
- Use Rephonic audience overlap to find similar-audience podcasts radiating out from your best-performing Baseline appearances
- Set up a monthly Clay workflow: search ListenNotes for new podcasts matching your keywords, filter for active + guest format, enrich host contacts, score, and push to Attio
- Target: 50+ qualified podcasts in the pipeline at any time
- Segment into tiers: Tier 1 (listen_score 40+, high topic fit) get maximum personalization; Tier 2 (listen_score 25-40) get standard personalization; Tier 3 (listen_score 20-25) get template pitches

### 2. Scale pitch outreach

Run the `podcast-pitch-outreach` drill at Scalable volume:
- Run Instantly campaigns with inbox rotation across 2-3 sending accounts
- A/B test pitch variables using the `ab-test-orchestrator` drill:
  - Subject line variants (episode reference vs direct pitch vs question format)
  - Pitch angle (data-driven vs story-driven vs contrarian take)
  - Social proof positioning (placed first vs placed last in email)
  - Follow-up cadence (day 3/7 vs day 5/12)
- Track which variables drive the highest positive reply rate
- Send 15-20 pitches per week, staggered across Tier 1 → Tier 2 → Tier 3

### 3. Streamline guest preparation

Run the `podcast-guest-preparation` drill with a templatized process:
- Maintain a master talking points library organized by topic angle. Update monthly.
- For each new booking, customize the template with podcast-specific research (host's recent content, audience profile)
- Pre-create tracking links in bulk: set up vanity URLs for all booked podcasts in one batch via Dub.co API
- Build an n8n workflow: when Attio status changes to "booked" → auto-create tracking link → auto-generate prep doc → send host pre-interview packet

### 4. Repurpose every episode

Run the `content-repurposing` drill for each aired episode:
- **Audio clips**: Extract 3-5 short clips (60-90 seconds each) of the founder's best moments. Use Descript to cut and add captions.
- **LinkedIn posts**: Turn each key insight into a standalone LinkedIn post (5-8 posts per episode)
- **Blog post**: Write a summary post on your blog with embedded audio clips and a link to the full episode
- **Newsletter**: Feature the episode in your email newsletter with a unique angle
- **Twitter/X thread**: Condense the core argument into a 5-7 tweet thread

Target: 5-10 derivative pieces per episode. Spread distribution over 2-3 weeks.

### 5. Build the performance dashboard

Run the `podcast-performance-monitor` drill:
- PostHog dashboard: traffic per podcast, lead funnel per podcast, episode traffic decay curves
- Attio tracking: per-episode clicks (7d, 30d, lifetime), leads attributed, host-reported downloads
- Weekly automated report via n8n: new episodes aired, total podcast traffic, leads this week, booking pipeline status
- After 5+ episodes: run pattern analysis (which podcast characteristics → best ROI)

### 6. Optimize based on data

Run the `ab-test-orchestrator` drill on podcast selection and preparation:
- Analyze: do niche podcasts (listen_score 25-35) outperform larger shows on lead conversion rate?
- Test: different CTA offers per episode (free trial vs resource download vs consultation)
- Test: different verbal CTA scripts ("head to..." vs "I built a special page for...")
- Feed winning patterns back into prospect research targeting and pitch angle selection

### 7. Evaluate against threshold

Measure against: ≥ 8 bookings AND ≥ 10 leads over 2 months. If bookings are high but leads are low, the problem is post-air conversion (CTA, landing page, offer). If bookings are low, the problem is prospecting or pitching. Diagnose and fix before Durable.

## Time Estimate

- 6 hours: Automated prospecting setup (Clay workflows, Rephonic analysis)
- 8 hours: Pitch campaign management (Instantly setup, A/B tests, reply handling)
- 8 hours: Guest preparation (8 bookings × 1 hour each)
- 10 hours: Content repurposing (8 episodes × ~75 min each)
- 4 hours: Dashboard setup and weekly reporting
- 4 hours: Optimization analysis and iteration

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| ListenNotes | Podcast search API | $9/mo Pro ([pricing](https://www.listennotes.com/api/pricing/)) |
| Rephonic | Audience overlap and similar-show discovery | $99/mo Light ([pricing](https://rephonic.com/pricing)) |
| Clay | Host enrichment and automated prospecting | Credits-based, ~$50-150/mo at this volume ([pricing](https://clay.com/pricing)) |
| Instantly | Automated pitch sequences with A/B testing | Growth: $37/mo ([pricing](https://instantly.ai/pricing)) |
| Dub.co | Tracking link management | Free or Pro $25/mo ([pricing](https://dub.co/pricing)) |
| Descript | Audio clip editing and captioning | $24/mo Creator ([pricing](https://descript.com/pricing)) |
| PostHog | Attribution tracking and dashboards | Free tier ([pricing](https://posthog.com/pricing)) |
| n8n | Workflow automation (prep, reporting) | Part of default stack |
| Attio | Pipeline and performance tracking | Part of default stack |

**Estimated play-specific cost:** $150-350/mo

## Drills Referenced

- `podcast-prospect-research` — automated monthly podcast discovery pipeline
- `podcast-pitch-outreach` — scaled pitch campaigns with A/B testing via Instantly
- `podcast-guest-preparation` — templatized prep with automated tracking link creation
- `content-repurposing` — turn each episode into 5-10 derivative content pieces
- `podcast-performance-monitor` — PostHog dashboard, automated weekly reports, ROI tracking
- `ab-test-orchestrator` — test pitch variables, CTA offers, and targeting criteria
