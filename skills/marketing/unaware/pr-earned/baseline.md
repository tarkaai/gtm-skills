---
name: pr-earned-baseline
description: >
  PR & Earned Placements — Baseline Run. Scale to 25 media targets with tool-assisted outreach,
  implement PR event tracking, and run a 4-week continuous pitch campaign to prove earned media
  produces repeatable referral traffic and leads.
stage: "Marketing > Unaware"
motion: "PREarnedMentions"
channels: "Email, Content"
level: "Baseline Run"
time: "15 hours over 4 weeks"
outcome: "≥ 3 placements and ≥ 100 referral clicks over 4 weeks"
kpis: ["Placement rate (placements / pitches sent)", "Referral clicks per placement", "Pitch-to-reply rate", "Leads from earned media"]
slug: "pr-earned"
install: "npx gtm-skills add marketing/unaware/pr-earned"
drills:
  - media-target-research
  - media-pitch-outreach
  - posthog-gtm-events
  - content-repurposing
---

# PR & Earned Placements — Baseline Run

> **Stage:** Marketing → Unaware | **Motion:** PREarnedMentions | **Channels:** Email, Content

## Outcomes

Prove that earned media is repeatable and produces measurable referral traffic over a sustained period. Expand the media target list to 25 contacts, use Instantly for tracked outreach, implement full PR event tracking in PostHog, and repurpose every placement into additional content assets. Success = at least 3 placements and at least 100 referral clicks from earned media over 4 weeks.

## Leading Indicators

- Media target list expanded and enriched (target: 25 contacts with verified emails)
- Pitches sent per week (target: 5-8/week for 4 weeks)
- Pitch-to-reply rate (target: 15-25%)
- Reply-to-placement rate (target: 30-50% of positive replies)
- Source requests answered per week (target: 3-5/week on Qwoted and Featured.com)
- Content assets created from each placement (target: 3-5 per placement)
- PostHog PR events flowing correctly (all 5+ event types)

## Instructions

### 1. Expand the media target list

Run the `media-target-research` drill at Baseline scale (25 targets):

1. Start with the Smoke test contacts that responded or showed interest. These are warm targets.
2. Expand to 25 total targets across three categories:
   - **Micro-newsletters** (8-10 targets): Substack, Beehiiv, and niche industry newsletters
   - **Niche podcasts** (8-10 targets): ListenNotes listen_score 20-50 with confirmed guest format
   - **Industry journalists** (5-8 targets): Beat reporters covering your space at trade publications and tech blogs
3. Enrich all contacts in Clay: verified email, Twitter, LinkedIn, recent article URL, outlet audience size.
4. Score and rank using the composite model: relevance (40%), audience (25%), accessibility (20%), competitor coverage (15%).
5. Push the ranked list to Attio with tier assignments.

### 2. Implement PR event tracking

Run the `posthog-gtm-events` drill to configure PR-specific events:

1. Define and implement these events in PostHog:
   - `pr_pitch_sent` — properties: outlet_name, outlet_type, journalist_name, pitch_angle, tier
   - `pr_pitch_replied` — properties: outlet_name, journalist_name, reply_sentiment
   - `pr_placement_published` — properties: outlet_name, outlet_type, url, estimated_reach
   - `pr_referral_click` — properties: source_outlet, placement_url, landing_page (tracked via UTMs)
   - `pr_lead_from_media` — properties: source_outlet, placement_url, lead_name, lead_company

2. Create a PostHog funnel: pitch_sent -> pitch_replied -> placement_published -> referral_click -> lead_captured

3. Set up UTM parameter structure for all PR links:
   ```
   ?utm_source={outlet_slug}&utm_medium=earned&utm_campaign=pr-earned-baseline&utm_content={pitch_angle_slug}
   ```

4. Verify events are flowing correctly by sending a test pitch and confirming all events log.

### 3. Execute a 4-week pitch campaign

Run the `media-pitch-outreach` drill at Baseline scale (20-30 pitches over 4 weeks):

**Week 1: Tier 1 targets (highest priority)**
1. Set up Instantly with the `instantly-campaign` fundamental. Create three campaigns by outlet type.
2. Map merge fields from Clay: contact_first_name, outlet_name, recent_article_topic, specific_observation, pitch_angle.
3. Send pitches to Tier 1 targets (top 5-6 contacts). These get maximum personalization -- review each email before sending.
4. Continue answering Qwoted and Featured.com source requests (target: 3-5/week).

**Week 2: Tier 2 targets + follow-ups**
1. Send Tier 1 follow-ups (one follow-up per contact, tied to current news).
2. Pitch Tier 2 targets (next 8-10 contacts) via Instantly with template + merge fields.
3. Handle all replies: interested -> send press kit, covering -> provide assets, declined -> log and note.

**Week 3: Tier 3 targets + placement maximization**
1. Pitch remaining Tier 3 targets.
2. For any placements that published, immediately execute step 4 (repurpose content).
3. Review pitch performance: which angles have the highest reply rate? Double down on winners.

**Week 4: Final push + evaluation**
1. Send final follow-ups to non-responders with a new angle or news hook.
2. Ensure all placements are tracked with UTMs and logged in PostHog.
3. Collect final referral traffic data.

### 4. Repurpose every placement

Run the `content-repurposing` drill for each published placement:

1. Turn the placement into social proof: screenshot the mention, create a LinkedIn post ("Excited to be featured in {outlet}..."), share on Twitter/X.
2. Extract quotable insights from your contribution and turn them into 2-3 standalone social posts.
3. Add the placement to your website press page or "As seen in" section.
4. Include the placement in your next email newsletter with a brief commentary.
5. If the placement contains data or insights, write a blog post expanding on the topic with a link back to the original coverage.

Target: 3-5 derivative content assets per placement.

### 5. Evaluate against threshold

At the end of week 4, measure against the pass threshold:

**Pass threshold:** ≥ 3 placements published AND ≥ 100 referral clicks from earned media over 4 weeks.

Pull metrics from PostHog:
- Total pitches sent
- Pitch-to-reply rate
- Placements published (with URLs)
- Referral clicks per placement
- Leads captured from earned media referral traffic

If PASS: document the media targets, pitch angles, and outreach cadence that worked. Note which outlet types (newsletters vs podcasts vs journalists) produced the most referral traffic per placement. Proceed to Scalable.

If FAIL: diagnose --
- Plenty of replies but few placements? Your pitch is interesting but you are not closing. Improve your press kit, offer more concrete assets, and respond faster when journalists express interest.
- Placements but low clicks? The outlets do not reach your ICP. Tighten targeting to outlets your customers actually read.
- Good outreach metrics but not enough volume? Expand the target list and increase send cadence.
- Source requests not converting? Improve response quality -- be more specific, include hard data, offer a contrarian take.

Re-run at Baseline with adjustments.

## Time Estimate

- Media target research and enrichment (25 contacts): 3 hours
- PostHog PR event setup and verification: 2 hours
- Pitch campaign execution (4 weeks x 2 hours/week): 8 hours
- Content repurposing per placement (est. 3 placements x 30 min): 1.5 hours
- Evaluation and documentation: 30 minutes
- **Total: ~15 hours over 4 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Tracked pitch sending with sequences | From $37/mo Starter (https://instantly.ai/pricing) |
| Clay | Contact enrichment and merge field population | From $149/mo (https://www.clay.com/pricing) |
| ListenNotes | Podcast discovery | Free tier or $9/mo (https://www.listennotes.com/api/pricing/) |
| Qwoted | Journalist source requests | Free or Pro at ~$50/mo (https://qwoted.com) |
| Featured.com | Expert quote placements | Free or Pro at ~$99/mo (https://featured.com/pricing) |
| PostHog | PR event tracking and funnels | Free up to 1M events/mo (https://posthog.com/pricing) |
| Attio | Media contact CRM and pipeline | Free up to 3 users (https://attio.com/pricing) |

## Drills Referenced

- `media-target-research` — expand to 25 media targets across newsletters, podcasts, and journalists with full enrichment
- `media-pitch-outreach` — execute a 4-week pitch campaign with Instantly tracking, structured follow-ups, and reply handling
- `posthog-gtm-events` — implement PR-specific event taxonomy for tracking the full pitch-to-pipeline funnel
- `content-repurposing` — turn every placement into 3-5 derivative content assets across social, email, and web
