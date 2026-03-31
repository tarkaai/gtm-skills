---
name: pr-earned-smoke
description: >
  PR & Earned Placements — Smoke Test. Identify 10 micro-newsletter editors and podcast hosts
  covering your space, pitch 5-10 with personalized angles, and test whether earned coverage
  drives referral clicks and inbound interest.
stage: "Marketing > Unaware"
motion: "PREarnedMentions"
channels: "Email, Content"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥ 1 placement and ≥ 30 referral clicks in 2 weeks"
kpis: ["Placement rate (placements / pitches sent)", "Referral clicks per placement", "Pitch-to-reply rate"]
slug: "pr-earned"
install: "npx gtm-skills add marketing/unaware/pr-earned"
drills:
  - media-target-research
  - media-pitch-outreach
  - threshold-engine
---

# PR & Earned Placements — Smoke Test

> **Stage:** Marketing → Unaware | **Motion:** PREarnedMentions | **Channels:** Email, Content

## Outcomes

Prove that earned media produces referral traffic and inbound interest. The founder identifies 10 media targets (micro-newsletter editors, podcast hosts, niche journalists), pitches 5-10 with personalized angles, and tracks whether the resulting coverage drives clicks to your site. Success = at least 1 placement published and at least 30 referral clicks from earned media within 2 weeks.

## Leading Indicators

- Media targets identified and enriched (target: 10 contacts with verified emails)
- Pitches sent (target: 5-10 over the week)
- Pitch open rate (target: 60%+ since these are hand-personalized)
- Positive replies received (target: 2-3 from 5-10 pitches)
- Journalist/editor requesting more info or scheduling a call
- Source requests answered on Qwoted or Featured.com (target: 2-3 submissions)

## Instructions

### 1. Research and build your media target list

Run the `media-target-research` drill at Smoke scale (10 targets):

1. Define 3 pitch angles -- specific story ideas where the founder has genuine expertise and data. Each angle should tie to a current trend or problem the target audience cares about. Examples: "Why most startups waste 60% of their marketing budget on the wrong funnel stage," or "Data from 200 companies shows X pattern."

2. Search for media targets across three categories:
   - **Micro-newsletters** (3-4 targets): Search Substack and Beehiiv for newsletters covering your vertical with 1K-25K subscribers. Prioritize editors who accept guest contributions or regularly feature external expertise.
   - **Niche podcasts** (3-4 targets): Use ListenNotes to find podcasts with listen_score 20-50 that accept guest interviews in your topic area.
   - **Industry journalists** (2-3 targets): Search BuzzSumo or Google for journalists who wrote about your topic or competitors in the last 30 days.

3. For each target, manually research: their name, outlet, recent article/episode topic, contact email, and one specific observation about their recent work that you can reference in your pitch.

4. Store the list in Attio or a spreadsheet with columns: name, outlet, outlet type, email, recent work reference, best pitch angle, status.

### 2. Craft and send personalized pitches

Run the `media-pitch-outreach` drill at Smoke scale (5-10 hand-written pitches):

1. For each target, write a personalized pitch email from the founder's personal email account. Use the `media-pitch-email` framework for journalists and newsletter editors, and the `podcast-pitch-email` framework for podcast hosts.

2. Every pitch must include:
   - A specific reference to the target's recent work (proves you actually read/listen)
   - The pitch angle most relevant to their coverage area
   - One concrete data point, stat, or insight that makes the story credible
   - An offer of specific assets (data, quotes, a pre-written draft for newsletters)

3. Send 1-2 pitches per day, Tuesday through Thursday, between 7am-9am in the target's timezone.

4. After 5 days, send one follow-up to non-responders. Tie the follow-up to a current news event or offer a different angle.

**Human action required:** The founder must review and send each pitch personally. At Smoke level, every pitch is hand-crafted from the founder's established email domain for maximum trust.

### 3. Respond to journalist source requests

In parallel with proactive pitching, set up reactive PR:

1. Create free accounts on Qwoted and Featured.com.
2. Set topic preferences matching your expertise areas.
3. When a relevant source request arrives, draft a 2-3 sentence expert response with a specific stat or insight. Submit before the deadline.
4. Track each submission: platform, topic, journalist, deadline, whether your response was selected.

Target: answer 2-3 source requests during the Smoke test week.

### 4. Track placements and referral traffic

When a placement publishes:

1. Add UTM parameters to any links the journalist will use: `?utm_source={outlet_slug}&utm_medium=earned&utm_campaign=pr-earned-smoke`
2. Log the placement in Attio: outlet name, URL, publish date, estimated reach.
3. Monitor referral traffic in PostHog (or Google Analytics) for clicks from the placement URL.
4. Track any inbound leads (DMs, contact form submissions, demo requests) that reference the coverage.

For podcast bookings, track: recording date, expected publish date, episode URL once live.

### 5. Evaluate against threshold

Run the `threshold-engine` drill at end of week 2:

**Pass threshold:** ≥ 1 placement published AND ≥ 30 referral clicks from earned media within 2 weeks.

Count a placement as: a published article mentioning your company, a newsletter edition featuring your content or quote, or a podcast episode where the founder appeared as a guest.

Count referral clicks as: visitors arriving at your site from the placement URL (tracked via UTMs or PostHog referrer data).

If PASS: document which pitch angles worked, which outlet types responded, and proceed to Baseline.

If FAIL: diagnose --
- Zero replies? Pitch angles are not newsworthy. Strengthen with harder data or a more contrarian take.
- Replies but no placements? The story pitch is interesting but you are not providing enough usable material. Offer pre-written content, data packages, or customer quotes.
- Placement but low clicks? The placement reached the wrong audience. Target outlets whose readers match your ICP more closely.
- Good clicks but no leads? Landing page is not converting PR traffic. Add social proof (the mention itself) and a clear CTA on your landing page.

Re-run with adjustments.

## Time Estimate

- Media target research and list building: 1.5 hours
- Pitch writing and personalization (5-10 pitches): 1.5 hours
- Source request monitoring and responses: 30 minutes
- Follow-up emails and reply handling: 30 minutes
- Tracking and evaluation: 30 minutes
- **Total: ~5 hours over 1 week** (evaluation continues through week 2)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| ListenNotes | Podcast discovery and research | Free tier: 5 req/min (https://www.listennotes.com/api/pricing/) |
| Qwoted | Journalist source requests | Free basic access (https://qwoted.com) |
| Featured.com | Expert quote placements | Free basic submissions (https://featured.com) |
| Hunter.io | Journalist email finding | 25 searches/mo free (https://hunter.io/pricing) |
| Gmail / Workspace | Sending personalized pitches | Free / existing |
| PostHog | Referral traffic tracking | Free up to 1M events/mo (https://posthog.com/pricing) |

## Drills Referenced

- `media-target-research` — find, qualify, and rank 10 media targets (newsletters, podcasts, journalists) with enriched contact info
- `media-pitch-outreach` — craft personalized pitches using media-pitch-email and podcast-pitch-email frameworks, send manually, handle replies
- `threshold-engine` — evaluate pass/fail against the 1-placement / 30-click threshold
