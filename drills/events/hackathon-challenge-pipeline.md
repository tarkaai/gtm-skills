---
name: hackathon-challenge-pipeline
description: Plan, promote, host, and judge a developer hackathon challenge that showcases product capabilities and generates qualified technical leads
category: Events
tools:
  - Devpost
  - Luma
  - Loops
  - Attio
  - PostHog
  - Clay
  - Cal.com
fundamentals:
  - calcom-event-types
  - loops-broadcasts
  - loops-audience
  - posthog-custom-events
  - attio-lists
  - attio-contacts
  - clay-people-search
  - clay-enrichment-waterfall
  - event-discovery-api
---

# Hackathon Challenge Pipeline

This drill covers the complete lifecycle of a single hackathon: challenge design, participant recruitment, event execution, judging, and prize fulfillment. The hackathon can be hosted (you run the entire event) or sponsored (you provide a challenge track within an existing hackathon).

## Input

- Product or API that participants will build with
- ICP definition: what kind of developers you want to attract (language, framework, domain)
- Budget: prizes, platform fees, promotion spend
- Format decision: virtual, in-person, or hybrid
- Duration: typically 24-48 hours for in-person, 1-2 weeks for virtual

## Steps

### 1. Design the challenge

Define a hackathon challenge that forces participants to use your product in a meaningful way. The challenge must be:

- **Specific enough** that submissions actually demonstrate your product's value (not just generic projects that mention your API once)
- **Open enough** that creative solutions are possible (avoid over-constraining to a single use case)
- **Achievable** within the hackathon timeframe by a team of 2-4 developers

Structure the challenge document:

```
## Challenge: {Title}

### Problem Statement
{1-2 paragraphs describing a real problem your product solves}

### Requirements
- Must use {your product/API} for {specific function}
- Must demonstrate {key capability}
- Submissions must include: working demo, source code, README, 2-minute video walkthrough

### Judging Criteria
- Technical implementation (30%): How well does the project use the API/product?
- Innovation (25%): Is the approach creative or novel?
- Impact (25%): Does the project solve a real problem?
- Presentation (20%): Is the demo clear and compelling?

### Prizes
- 1st place: ${amount} + {product credits/perks}
- 2nd place: ${amount} + {product credits/perks}
- 3rd place: ${amount} + {product credits/perks}
- All participants: {free tier upgrade, swag, credits}

### Resources
- API documentation: {link}
- Quickstart guide: {link}
- Sample project: {link}
- Support channel: {Discord/Slack link}
```

Prepare starter templates and boilerplate repos on GitHub so participants spend time building, not configuring.

### 2. Set up the hackathon platform

**If hosting your own hackathon:**

Create the event on your chosen platform:

- **Devpost** (virtual/hybrid): Create a hackathon at devpost.com/hackathons/new. Configure: challenge description, rules, prizes, judging criteria, timeline, and submission requirements. Devpost handles registration, team formation, and submission collection.
- **Luma** (in-person/virtual): Create the event at lu.ma. Configure: event details, registration form with custom fields (GitHub username, experience level, tech stack), and capacity limits.
- **Devfolio** (dev-focused): Contact partner@devfolio.co for setup. Best for developer-centric hackathons in tech communities.

**If sponsoring an existing hackathon:**

Contact the hackathon organizer to secure a sponsor track. Provide: challenge description, prizes, judging criteria, API access for participants, and mentor availability. Use `event-discovery-api` to find upcoming hackathons in your target developer communities.

Track registration events in PostHog using `posthog-custom-events`:
- `hackathon_page_viewed` with `hackathon_slug`, `source`
- `hackathon_registered` with `hackathon_slug`, `team_size`, `experience_level`

### 3. Recruit participants

Build a targeted outreach campaign to reach the right developers:

**Community channels:**
- Post in relevant Discord servers, Slack communities, and subreddits
- Share on Hacker News (Show HN) and dev.to
- Post in GitHub Discussions for related open-source projects

**Email outreach:**
Using `clay-people-search`, find developers who:
- Contributed to open-source projects in the relevant tech stack
- Have public GitHub profiles with activity in the target domain
- Match your ICP criteria (role, company size, experience level)

Enrich with `clay-enrichment-waterfall` and add to a Loops audience segment using `loops-audience`. Send a targeted invite sequence using `loops-broadcasts`:
- Email 1 (4 weeks before): Announcement with challenge details and prize info
- Email 2 (2 weeks before): Spotlight on starter templates and resources
- Email 3 (1 week before): Final registration push with early registrant count as social proof

**Tracking:**
Using `calcom-event-types`, set up office hours / mentor booking slots so participants can get help during the hackathon.

Add all registrants to Attio using `attio-contacts` with tags: `source: hackathon-{slug}`, `registration_date`, `experience_level`, `tech_stack`.

### 4. Execute the hackathon

**Pre-event (24 hours before):**
- Send a logistics email via `loops-broadcasts`: schedule, rules, support channels, starter resources
- Ensure API keys / product access is provisioned for all registered participants
- Brief mentors and judges on their schedules

**During the event:**
- Host a kickoff session: introduce the challenge, walk through resources, answer questions
- Provide mentor office hours (use Cal.com booking slots) for technical support
- Post updates in the hackathon Discord/Slack channel at regular intervals
- For in-person: provide workspace, WiFi, food, and a visible countdown timer

**Submission deadline:**
- Send a 2-hour warning and a 30-minute warning via the event platform
- Close submissions at the deadline — no exceptions

**Judging:**
- Assign 3-5 judges. Each judge scores every submission on the criteria defined in Step 1.
- Collect scores in a shared spreadsheet or the platform's built-in judging tool (Devpost has this).
- Average scores. Resolve ties by re-reviewing the top 2-3 projects together.

**Awards ceremony:**
- Announce winners live (virtual or in-person). Walk through the winning projects.
- Record the ceremony for social content.

### 5. Capture and process leads

After the hackathon closes, extract the participant data:

Using `attio-lists`, create a "Hackathon {Slug} Participants" list with fields:
- Name, email, GitHub URL, team name
- Submission status: submitted / registered-only / withdrawn
- Submission quality score (from judging)
- Product usage depth: how extensively they used your API (check API logs)
- Follow-up tier: Winner / Top 10 / Submitted / Registered-Only

Track in PostHog using `posthog-custom-events`:
- `hackathon_submission_received` with `hackathon_slug`, `team_name`, `quality_score`
- `hackathon_api_usage` with `hackathon_slug`, `calls_made`, `features_used`

### 6. Measure results

Calculate key metrics:
- Registration count and registration-to-submission rate (target: >40%)
- Number of submissions and average quality score
- API/product adoption depth: how many participants used >3 features
- Qualified leads generated: participants who match ICP and showed strong engagement
- Cost per qualified lead: total spend / qualified leads

## Output

- Completed hackathon with scored submissions
- Participant list segmented by engagement and lead quality in Attio
- PostHog events for full-funnel tracking
- Content assets: winning project demos, ceremony recording, participant testimonials

## Triggers

- Run per hackathon event (typically quarterly)
