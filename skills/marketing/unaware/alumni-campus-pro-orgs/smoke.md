---
name: alumni-campus-pro-orgs-smoke
description: >
  Alumni & Campus Outreach — Smoke Test. Discover alumni, campus, and professional org communities
  where your ICP is active, post value-first content in 3-5 communities, and validate whether
  community engagement produces at least 1 meeting in 1 week.
stage: "Marketing > Unaware"
motion: "Communities & Forums"
channels: "Communities, Other"
level: "Smoke Test"
time: "3 hours over 1 week"
outcome: "≥ 1 meeting booked from community engagement in 1 week"
kpis: ["Post engagement (reactions + replies)", "Inbound DMs or inquiries", "Referral sessions from community links"]
slug: "alumni-campus-pro-orgs"
install: "npx gtm-skills add marketing/unaware/alumni-campus-pro-orgs"
drills:
  - community-reconnaissance
  - community-content-posting
  - threshold-engine
---

# Alumni & Campus Outreach — Smoke Test

> **Stage:** Marketing → Unaware | **Motion:** Communities & Forums | **Channels:** Communities, Other

## Outcomes

Validate that alumni networks, campus organizations, and professional associations contain your ICP and that posting value-first content there generates at least 1 meeting. This is a one-time local agent run — no automation, no always-on. Just proof of signal.

## Leading Indicators

- At least 3 communities identified with >100 members matching your ICP
- At least 1 post receives 5+ reactions or 3+ replies within 48 hours
- At least 1 inbound DM or inquiry referencing your community post
- At least 1 referral session tracked in PostHog from a community link

## Instructions

### 1. Map your community landscape

Run the `community-reconnaissance` drill. Instead of focusing only on Reddit, target three community categories:

**Alumni networks:** Use the `community-directory-search` fundamental to find LinkedIn alumni groups, university alumni Slack workspaces, and alumni chapter mailing lists for universities where your founders or team attended. Search for groups matching: `"{university} alumni {industry}"`, `"{university} founders"`, `"{university} {city} alumni"`.

**Campus organizations:** Search for active student/faculty organizations at target universities: entrepreneurship clubs, industry-specific student groups, faculty research groups. These are reached via their public Slack/Discord channels, event mailing lists, or LinkedIn groups.

**Professional organizations:** Search for industry associations, local chapters of national orgs (YPO, EO, industry-specific councils), and professional Slack/Discord communities. Target groups where your ICP holds membership: `"{ICP role} association"`, `"{industry} professionals {city}"`, `"{industry} council members"`.

**Output:** A ranked list of 10-15 communities across all three categories, stored in Attio with engagement profiles (platform, member count, activity level, join requirements, your unique angle).

### 2. Join and observe target communities

**Human action required:** Join 3-5 top-ranked communities. For communities requiring approval (most alumni and professional groups), submit applications referencing your genuine affiliation. Observe for 2-3 days before posting: note the tone, common topics, posting frequency, and what content gets engagement.

### 3. Create value-first community content

Run the `community-content-posting` drill adapted for non-Reddit platforms. For each of 3-5 target communities, create 1-2 pieces of content matched to the community's format:

- **LinkedIn Groups:** Write a discussion-starting post (150-300 words) sharing an insight, asking a question, or presenting data relevant to the group's focus. No links in the initial post.
- **Slack/Discord:** Share a helpful resource, answer an existing question thoroughly, or start a discussion in the appropriate channel. Keep messages under 200 words.
- **Email lists/forums:** Write a concise, informative post that provides genuine value — a framework, benchmark, lesson learned, or curated resource list.

Content rules:
- Lead with value that demonstrates expertise, not a pitch
- Reference your affiliation to the community (alumni status, shared profession) to establish belonging
- Include a soft CTA only if natural: "Happy to chat more about this" or "DM me if you want the full breakdown"
- Track all shared links with UTM parameters: `utm_source={platform}&utm_medium=community&utm_campaign=alumni-campus-pro-orgs&utm_content={community_name}_{post_topic}`

### 4. Engage with responses

Monitor your posts for 48 hours after publishing. Reply to every comment or reaction substantively. Each reply thread is an opportunity to demonstrate deeper expertise and move toward a conversation. If someone expresses interest, offer a specific next step: "I can walk you through how we approached this — want to grab 15 minutes this week?"

**Human action required:** Respond to DMs, comments, and inquiries within 4 hours during business hours. Log every interaction: community name, interaction type, topic, outcome (conversation, DM, meeting request, nothing).

### 5. Evaluate against threshold

Run the `threshold-engine` drill to measure results against: **≥ 1 meeting booked from community engagement in 1 week**.

Gather data from:
- PostHog: referral sessions where `utm_campaign=alumni-campus-pro-orgs`
- Activity log: DMs received, meeting requests, conversations initiated
- Attio: any new contacts or deals attributed to community engagement

**PASS (≥ 1 meeting):** Proceed to Baseline. Document which communities and content types produced the meeting.
**FAIL (0 meetings):** Diagnose — were the communities too small, the content mismatched, or the engagement insufficient? Try 3-5 different communities or adjust content approach. Re-run Smoke.

## Time Estimate

- Community discovery and profiling: 1 hour
- Content creation (3-5 posts): 1 hour
- Engagement and follow-up over 1 week: 1 hour
- **Total: 3 hours over 1 week**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Community discovery and enrichment | $185/mo Launch plan (https://clay.com/pricing) — use free trial for Smoke |
| PostHog | Track referral sessions from community links | Free tier: 1M events/mo (https://posthog.com/pricing) |
| Attio | Store community targets and log interactions | Free tier available (https://attio.com/pricing) |

**Estimated play-specific cost at Smoke level:** $0 (use free tiers and trials)

## Drills Referenced

- `community-reconnaissance` — discover and rank alumni, campus, and professional org communities where ICP is active
- `community-content-posting` — create and publish value-first content adapted to each community's format and culture
- `threshold-engine` — evaluate meeting count against the ≥ 1 meeting pass threshold
