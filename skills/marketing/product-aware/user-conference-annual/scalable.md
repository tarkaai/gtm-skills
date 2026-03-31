---
name: user-conference-annual-scalable
description: >
  Annual User Conference -- Scalable Automation. Transform the annual conference
  into a repeatable program with satellite events, automated content repurposing
  pipeline, A/B tested promotion strategies, and an expanding attendee base
  that compounds year over year. Multiply reach and pipeline without
  proportional effort increase.
stage: "Marketing > ProductAware"
motion: "MicroEvents"
channels: "Events"
level: "Scalable Automation"
time: "80 hours over 4 months"
outcome: ">=400 registrations, >=55% show rate, >=40 expansion meetings booked, content repurposing generates >=500 additional content engagements"
kpis: ["Total registrations", "Show rate", "Expansion meetings booked", "Content derivative engagements", "Cost per expansion meeting", "Net new attendees (non-customer)", "Repeat attendee rate"]
slug: "user-conference-annual"
install: "npx gtm-skills add marketing/product-aware/user-conference-annual"
drills:
  - ab-test-orchestrator
  - content-repurposing
  - follow-up-automation
---

# Annual User Conference -- Scalable Automation

> **Stage:** Marketing -> Product Aware | **Motion:** MicroEvents | **Channels:** Events

## Outcomes

- Scale the conference from 150 to 400+ registrations by expanding beyond your customer base to product-aware prospects and partner audiences
- Build an automated content repurposing pipeline that turns each conference session into 10+ derivative content pieces driving year-round engagement
- Systematically A/B test promotion strategies, registration incentives, session formats, and follow-up approaches to find the highest-converting combinations
- Reduce cost per expansion meeting through automation efficiency
- Establish satellite events (regional meetups, virtual replays) that extend the conference's reach beyond a single day

## Leading Indicators

- Net new registrations (non-customers) represent >=40% of total registrations -- the conference is attracting new audience, not just servicing existing customers
- Content derivatives (clips, blog posts, LinkedIn posts, newsletter sections) generate >=500 total engagements in the 60 days post-conference
- At least 3 A/B test results are conclusive and actionable for next year's conference planning
- Satellite events (virtual replay sessions, regional meetups) drive >=50 additional registrations beyond the main event
- Cost per expansion meeting trending down vs. Baseline

## Instructions

### 1. Expand the registration funnel

Run the the conference planning pipeline workflow (see instructions below) drill with Scalable-level enhancements to the promotion engine:

**Multi-channel promotion at scale:**
- **Owned channels**: Using Loops, send segmented email invitations to your full customer list AND product-aware prospect list. Segment by: account tier, product usage patterns, industry vertical, and buyer role. Each segment gets a tailored email emphasizing the sessions most relevant to them.
- **Clay prospecting**: Use `clay-people-search` and `clay-enrichment-waterfall` to find 1,000+ net-new prospects who match your conference ICP: people with the right titles at companies in your target industries who show signals of being product-aware (visited competitor sites, posted about the problem space, changed jobs into relevant roles). Import into Loops for invitation.
- **Partner co-promotion**: Identify 3-5 integration partners, complementary tools, or industry associations. Offer them: a speaker slot, co-branded content, or a sponsor mention in exchange for promoting the conference to their audience. Each partner should drive 30-100 registrations. Track partner-sourced registrations with unique UTM parameters.
- **LinkedIn paid promotion (optional)**: Promote the registration page via LinkedIn Sponsored Content. Target by title + industry matching your conference ICP. Budget: $500-1,000 for a 4-week campaign. Track cost per registration by channel in PostHog.
- **Customer referral incentive**: Give registered customers a unique referral link. For every colleague they bring who registers, both get early access to recordings or a bonus resource. Track referral registrations in PostHog.

**Registration optimization:**
- Build a 2-step registration process: quick RSVP (name + email only) followed by a detailed profile form. This reduces friction at the top of the funnel while still capturing rich data.
- Implement waitlist mechanics if approaching capacity: "Only X spots remaining" messaging increases urgency.
- Add social proof to the registration page: attendee count, notable speakers, past attendee testimonials (from Baseline feedback).

### 2. A/B test conference variables

Run the `ab-test-orchestrator` drill to systematically test one variable at a time across conference promotion and execution:

**Pre-conference tests (during promotion window):**

1. **Email subject lines**: A/B test invite email subject lines within each send via Loops. Test: benefit-focused ("Learn how [Company] grew 3x with [Product]") vs. curiosity-focused ("The conference our customers have been asking for") vs. social proof ("Join 200+ [industry] leaders at our annual summit"). Track open rate and registration rate.

2. **Registration page variants**: Test two versions of the registration page using PostHog feature flags. Variant A: agenda-first layout (sessions and speakers above the fold). Variant B: value-prop-first layout (what you will learn + testimonials above the fold, agenda below). Track page-to-registration conversion rate.

3. **Promotion timing**: Test sending invite emails on different days. Split your list and send Variant A on Tuesday 10am and Variant B on Thursday 10am. Track open rate and registration rate by send time.

4. **Registration incentive**: Test offering early registrants an exclusive resource (recording of a bonus session, template, or tool) vs. no incentive. Measure: registration velocity in the first 2 weeks.

**Post-conference tests (during follow-up window):**

5. **Follow-up timing**: Test sending the initial follow-up email 4 hours vs. 24 hours after the conference. Measure: open rate, click rate, and reply rate.

6. **CTA variant**: Test a direct expansion meeting CTA ("Book a call to discuss your upgrade path") vs. a softer CTA ("Reply with your biggest takeaway and we'll send personalized next steps"). Measure: meetings booked within 14 days.

For each test, define the hypothesis, success metric, minimum sample size, and experiment duration before running. Document results in Attio. After the conference, compile a "winning formula" report that guides next year's conference planning.

### 3. Build the content repurposing flywheel

Run the `content-repurposing` drill after the conference to multiply content output from each session:

**Recording -> clips**: Using Descript ($24/mo Creator), extract 3-5 highlight clips per session (60-90 seconds each). Focus on: the strongest insight, the best audience question + answer, a quotable customer moment, and a product demo highlight. Aim for 20-30 clips total across all sessions.

**Recording -> blog posts**: Transcribe each session and transform into a standalone blog post (1,200-2,000 words). Focus on the frameworks, insights, and actionable takeaways. Each post links to the full session recording and next year's conference registration (when available).

**Clips -> LinkedIn posts**: Each clip becomes a LinkedIn post with a text hook, the video clip, and a CTA. Schedule 2-3 posts per week for 8-10 weeks post-conference. This creates a sustained LinkedIn presence from a single day of content.

**Clips -> email sequence**: Bundle the best clips into a 5-email "Conference Highlights" sequence in Loops. Send to: (a) everyone who registered but did not attend, (b) product-aware prospects who did not register, and (c) your broader email list. Each email focuses on one theme, embeds a clip, and includes a CTA to join next year's conference.

**Sessions -> newsletter content**: Each session's key takeaway becomes a section in your newsletter for the next 2-3 months. Reference the session, embed the relevant clip, and link to the full recording.

**Schedule**: Publish derivative content over the 60 days post-conference. Map out a content calendar: Week 1-2 blog posts, Week 2-8 LinkedIn posts, Week 3-6 email highlights sequence, Week 4-10 newsletter sections. Track all content engagements in PostHog: views, clicks, shares, replies, and conference registrations driven by derivative content.

### 4. Automate post-conference follow-up at scale

Run the `follow-up-automation` drill to build n8n workflows that handle post-conference pipeline generation:

**Engagement-based routing**: Build an n8n workflow that runs 24 hours after the conference:
1. Pull attendee engagement data from PostHog: sessions attended, questions asked, CTAs clicked, polls answered
2. Score each attendee: sessions_attended * 10 + questions_asked * 25 + cta_clicked * 30 + poll_answered * 5
3. Route to the appropriate Loops nurture sequence based on score tier
4. For scores >75: auto-create an Attio deal with source `conference-20XX`, populate with engagement context, and notify the account owner or founder via Slack

**Smart follow-up triggers**: Using `n8n-triggers`, build workflows that respond to post-conference signals:
- When a Tier 1 attendee opens the follow-up email 3+ times within 48 hours: escalate to personal outreach from the account owner
- When a no-show watches >50% of a session recording: send a targeted follow-up email referencing that session
- When a prospect (non-customer) books an expansion meeting: auto-enrich them in Clay and create a full prospect profile in Attio
- When 5+ attendees from the same company register: flag as a target account for multi-threaded follow-up

**Satellite event automation**: 4-6 weeks after the main conference, host 2-3 "Conference Replay" virtual sessions:
- Select the 3 highest-rated sessions from attendee feedback
- Package them as a focused virtual replay event with live Q&A added
- Promote to: (a) no-shows from the main event, (b) prospects who did not register, (c) new leads acquired since the conference
- This extends the conference's pipeline generation window and captures people who could not attend the main event

**Human action required:** You still deliver keynotes and moderate live sessions. Speaker recruitment conversations are human-led. All other conference operations -- promotion, registration, follow-up, content repurposing, satellite events -- are agent-managed.

### 5. Evaluate against the threshold

After the 60-day post-conference window (main event + satellite events + content repurposing window), evaluate:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Total registrations (main + satellite) | >=400 | Attio conference registrant lists combined |
| Show rate (main event) | >=55% | Main event attendees / main event registrations |
| Expansion meetings booked | >=40 | Cal.com bookings + email-to-meeting conversions within 60 days |
| Content derivative engagements | >=500 | PostHog: sum of views, clicks, and shares on all conference-derived content |
| Cost per expansion meeting | Trending down vs. Baseline | Total conference spend / meetings booked |
| Net new attendees (non-customer) | >=40% of total | Attio: registrants not tagged as existing customers |
| Repeat attendee rate | >=20% (if 2nd year) | Attio: attended this year AND last year |

**PASS**: Core metrics met (registrations, meetings, content engagements). Proceed to Durable. You have a scalable conference program with automated operations and a content flywheel.

**FAIL**: Diagnose by metric:
- Low registrations: Partner co-promotion did not drive enough volume, or Clay prospecting list was too narrow. Expand partner network. Broaden Clay search criteria. Consider a pricing change (paid -> free or vice versa).
- Low meetings: Conference content not driving enough expansion intent. Add more product-focused sessions (roadmap, new features, power user workshops). Strengthen the expansion CTA throughout the conference. Personalize Tier 1 follow-up with account-specific expansion opportunities.
- Low content engagements: Clips not compelling enough, or distribution not reaching the right audience. Review which clip types get the most engagement. Test different LinkedIn post formats (video vs. carousel vs. text). Expand email distribution beyond conference registrants.

## Time Estimate

- Expanded promotion engine build (Clay integration, partner coordination, email sequences): 12 hours
- A/B test planning and implementation: 6 hours
- Speaker recruitment and coordination (5-8 speakers): 6 hours
- Conference delivery (expanded agenda): 6 hours
- Content repurposing pipeline setup (Descript, templates, distribution calendar): 8 hours
- Post-conference automation build (n8n workflows, Loops sequences): 8 hours
- Satellite replay events (2-3 events): 6 hours
- Cross-event analysis and optimization: 8 hours
- Content derivative creation and scheduling: 12 hours
- A/B test analysis and "winning formula" report: 4 hours
- Partner coordination: 4 hours
- **Total: ~80 hours over 4 months** (10 weeks pre-event + event + 6 weeks post-event)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Riverside | Conference recording + production | $29/mo Pro (4K, 15hr transcription) -- [riverside.com/pricing](https://riverside.com/pricing) |
| Loops | Email invites, reminders, nurture, highlights sequence | $49/mo (up to 5,000 contacts) -- [loops.so/pricing](https://loops.so/pricing) |
| PostHog | Event tracking, funnels, experiments, feature flags | Free tier: 1M events/mo -- [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM, registrant tracking, deal creation, reporting | $29/user/mo Plus -- [attio.com](https://attio.com) |
| n8n | Registration webhooks, follow-up automation, satellite event ops | Self-hosted free or Cloud Pro EUR60/mo -- [n8n.io/pricing](https://n8n.io/pricing) |
| Clay | Prospect sourcing for invites (1,000+ prospects) | $185/mo Launch (2,500 credits) -- [clay.com/pricing](https://www.clay.com/pricing) |
| Descript | Recording clips + transcription for repurposing | $24/mo Creator -- [descript.com/pricing](https://www.descript.com/pricing) |
| Loom | Personalized follow-up clips for Tier 1 attendees | $12.50/mo Business -- [loom.com/pricing](https://www.loom.com/pricing) |
| Cal.com | Expansion call booking CTA | Free tier -- [cal.com/pricing](https://cal.com/pricing) |
| Luma | Event registration page | Free -- [lu.ma](https://lu.ma) |
| LinkedIn Ads | Paid promotion (optional) | ~$500-1,000 campaign -- [linkedin.com/ad](https://www.linkedin.com/ad) |

**Estimated play-specific cost at Scalable: $330-600/mo** (all tools above + optional LinkedIn Ads spend)

## Drills Referenced

- the conference planning pipeline workflow (see instructions below) -- expanded conference operations: multi-channel promotion engine, partner coordination, satellite events, scaled registration
- `ab-test-orchestrator` -- systematically test email subject lines, registration page layouts, promotion timing, registration incentives, and follow-up approaches
- `content-repurposing` -- transform conference recordings into 20-30 clips, blog posts, LinkedIn posts, email sequences, and newsletter content
- `follow-up-automation` -- automated engagement-based attendee routing, smart follow-up triggers, and satellite event promotion
