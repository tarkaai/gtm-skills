---
name: pr-earned-scalable
description: >
  PR & Earned Placements — Scalable Automation. Automate media monitoring, opportunity detection,
  and journalist relationship management. Scale to 75+ targets with tiered personalization.
  A/B test pitch angles, outlets, and timing to find the 10x multiplier.
stage: "Marketing > Unaware"
motion: "PREarnedMentions"
channels: "Email, Content"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥ 8 placements and ≥ 400 referral clicks over 2 months"
kpis: ["Placement rate", "Referral clicks per placement", "Pitch-to-reply rate", "Leads from earned media", "Cost per placement", "Placement-to-lead conversion rate"]
slug: "pr-earned"
install: "npx gtm-skills add marketing/unaware/pr-earned"
drills:
  - ab-test-orchestrator
---

# PR & Earned Placements — Scalable Automation

> **Stage:** Marketing → Unaware | **Motion:** PREarnedMentions | **Channels:** Email, Content

## Outcomes

Find the 10x multiplier for earned media. Automate media monitoring and opportunity detection so the agent surfaces PR opportunities in real-time. Scale to 75+ media targets with tiered personalization. A/B test pitch angles, outreach timing, and outlet types to identify which combinations produce the highest placement rate and referral traffic per hour invested. Success = at least 8 placements and at least 400 referral clicks from earned media over 2 months.

## Leading Indicators

- Media target list scaled to 75+ contacts with monthly refresh cycle
- Opportunity detection pipeline active (source requests, brand mentions, trending topics flowing)
- Pitches sent per week (target: 10-15/week)
- Source requests answered per week (target: 5-8/week)
- A/B test running: at least one active experiment on pitch angle, timing, or format
- Placement-to-amplification time: <24 hours from publication to social sharing
- Cost per placement trending downward as efficiency improves
- Journalist relationship scores improving (Attio health scores trending from 0-1 toward 2-3)

## Instructions

### 1. Deploy media monitoring and opportunity detection

Run the the media relationship automation workflow (see instructions below) drill to build always-on automation:

**Source request pipeline:**
1. Build an n8n workflow that monitors Qwoted and Featured.com email alerts.
2. Each alert is parsed for: topic, journalist name, outlet, deadline, and requirements.
3. Claude API evaluates relevance (1-5 score) against your expertise areas.
4. For relevance >= 3: Claude drafts a response using the founder's voice, expertise, and available data.
5. Draft and original request are posted to Slack #pr-opportunities for human review.
6. **Human action required:** Approve or edit the response before submitting. For high-relevance requests (score 4-5), aim to respond within 2 hours of the alert.

**Brand and competitor monitoring:**
1. Set up Mention API alerts for your brand name, product name, and 2-3 competitor names.
2. n8n webhook receives alerts and classifies: positive mention, neutral, negative, competitor coverage.
3. Positive brand mentions: auto-log in Attio, post to Slack, queue a thank-you social post.
4. Competitor mentions: flag the journalist as a pitch target. If a journalist covered a competitor but not you, draft a pitch offering your alternative perspective.
5. Negative mentions: immediate Slack alert for human review and response.

**Trending topic detection:**
1. Daily n8n cron: query Mention API for your industry keywords, sorted by mention velocity.
2. Claude evaluates if any trending topic intersects with your pitch angles.
3. If match found: draft a reactive pitch and post to Slack with urgency flag.
4. **Human action required:** Approve and send reactive pitches within 24 hours (trend windows close fast).

### 2. Scale the media target list

Expand from 25 to 75+ targets:

1. Re-run `media-target-research` at Scalable volume. Add new outlets discovered through monitoring (journalists who covered competitors, trending outlets in your space).
2. Implement a monthly refresh cycle: n8n cron runs Clay enrichment on the full list monthly. Flag journalists who changed outlets. Remove contacts that bounced. Add new contacts from source request platforms where your responses were selected.
3. Segment the expanded list:
   - **Tier 1 (15 targets):** Highest-reach outlets with proven ICP audience overlap. Full hand-personalization.
   - **Tier 2 (30 targets):** Mid-reach outlets with good topic fit. Template + 3 merge fields.
   - **Tier 3 (30+ targets):** Niche outlets, new journalists. Template + 2 merge fields.

### 3. A/B test pitch approaches

Run the `ab-test-orchestrator` drill to systematically test variables:

**Test 1 — Pitch angle (weeks 1-3):**
- Hypothesis: "Data-driven pitch angles (leading with a specific stat) will produce 2x higher reply rate than story-driven angles (leading with a narrative)."
- Split: alternate angles across Tier 2 targets. Track reply rate and placement rate per angle.
- Minimum sample: 15+ pitches per variant.

**Test 2 — Outreach timing (weeks 3-5):**
- Hypothesis: "Pitches sent 7am-8am journalist timezone will produce 30%+ higher open rate than pitches sent 9am-11am."
- Split: randomize send times within Instantly.
- Track: open rate, reply rate.

**Test 3 — Outlet type ROI (weeks 5-8):**
- Hypothesis: "Newsletter placements produce 3x more referral clicks per placement than podcast appearances."
- Compare: referral clicks and leads per placement by outlet type.
- This is an observational test using Baseline + Scalable data.

**Test 4 — Follow-up approach (weeks 3-6):**
- Hypothesis: "Follow-ups tied to current news events produce 50%+ higher reply rate than generic 'checking in' follow-ups."
- Split: alternate follow-up styles. Track incremental replies from follow-ups.

Log all test results in PostHog. After each test concludes, implement the winner permanently and move to the next variable.

### 4. Automate post-placement amplification

Build n8n workflows that fire when a placement is logged in Attio (status = "published"):

1. Auto-generate social media posts: LinkedIn post celebrating the coverage + Twitter/X post tagging the journalist/outlet.
2. Route social posts to Slack for approval. On approval, schedule via Buffer or Typefully.
3. Auto-add the placement to the website press page via CMS API.
4. Auto-draft a newsletter section featuring the placement for the next email send.
5. Auto-send a thank-you DM/email to the journalist (drafted by Claude, reviewed by human).
6. Log referral traffic tracking with UTMs.

Target: <24 hours from placement publication to full amplification cycle completion.

### 5. Build and maintain journalist relationships

Track every interaction in Attio with relationship health scores (0-5):

- After each positive interaction, increment the score.
- For Tier 1 targets with score >= 2: shift from pitching to nurturing. Share relevant data, offer exclusive access to announcements, provide quotes when they need sources. The goal is to become a go-to source they contact proactively.
- For Tier 2 targets with successful placements: move to Tier 1 and deepen the relationship.
- Monthly: review relationship scores. Identify 5 journalists to nurture from score 1 to 2+.

### 6. Evaluate against threshold

At the end of 2 months, measure against the pass threshold:

**Pass threshold:** ≥ 8 placements published AND ≥ 400 referral clicks from earned media over 2 months.

Pull from PostHog and Attio:
- Total placements (by outlet type and tier)
- Referral clicks per placement
- Leads from earned media
- Cost per placement (total tool costs + estimated time cost / placements)
- A/B test results: which pitch angles, timing, and outlet types won
- Relationship scores: average score improvement over 2 months

If PASS: document the winning pitch approaches, outlet type ROI, and automation workflows. Prepare the playbook for Durable handoff. Proceed to Durable.

If FAIL: diagnose using A/B test data --
- Low placement rate despite high volume? Personalization quality has degraded at scale. Tighten Tier 1 personalization and reduce Tier 3 volume.
- Placements but low referral clicks? Outlets are not reaching your ICP. Cut low-performing outlets and double down on high-traffic-per-placement targets.
- Source requests not converting? Response quality is generic. Train the Claude draft prompt with examples of winning responses.
- Monitoring not surfacing opportunities? Expand keyword coverage and add more competitor names.

## Time Estimate

- Media monitoring and automation setup: 10 hours (one-time)
- Media target expansion and enrichment: 5 hours
- Pitch campaign execution (8 weeks x 3 hours/week): 24 hours
- A/B test setup and analysis (4 tests): 8 hours
- Amplification workflow setup: 4 hours
- Relationship management (8 weeks x 30 min/week): 4 hours
- Monthly review and optimization: 5 hours
- **Total: ~60 hours over 2 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Tracked pitch sending with sequences | From $37/mo (https://instantly.ai/pricing) |
| Clay | Contact enrichment at scale | From $149/mo (https://www.clay.com/pricing) |
| Mention | Brand and competitor media monitoring | From $41/mo Solo (https://mention.com/en/pricing/) |
| Qwoted | Journalist source requests | Pro ~$50/mo (https://qwoted.com) |
| Featured.com | Expert quote placements | Pro ~$99/mo (https://featured.com/pricing) |
| n8n (self-hosted) | Automation: monitoring, amplification, reporting | Free self-hosted (https://n8n.io/pricing) |
| PostHog | PR event tracking and experiments | Free up to 1M events/mo (https://posthog.com/pricing) |
| Attio | Media contact CRM and relationship tracking | Free up to 3 users (https://attio.com/pricing) |
| Anthropic Claude API | Pitch drafting, opportunity evaluation | ~$5-15/mo (https://www.anthropic.com/pricing) |
| Buffer or Typefully | Social post scheduling for amplification | ~$12-25/mo (https://buffer.com/pricing) |

## Drills Referenced

- the media relationship automation workflow (see instructions below) — always-on automation: source request monitoring, brand/competitor mention detection, trending topic alerts, journalist relationship tracking, post-placement amplification
- `ab-test-orchestrator` — systematically test pitch angles, outreach timing, outlet types, and follow-up approaches to find the winning combinations
