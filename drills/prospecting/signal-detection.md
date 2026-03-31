---
name: signal-detection
description: Monitor and act on buying signals like job changes, funding rounds, and hiring sprees
category: SignalDetection
tools:
  - Clay
  - Apollo
  - LinkedIn
fundamentals:
  - clay-claygent
  - clay-enrichment-waterfall
  - attio-lists
---

# Signal Detection

This drill sets up ongoing monitoring for buying signals that indicate a prospect is more likely to convert right now. Signals include job changes, funding events, hiring activity, and technology adoption.

## Prerequisites

- Clay account with webhook or scheduled enrichment capability
- Target account list loaded in Clay or Attio
- Understanding of which signals matter most for your ICP

## Steps

### 1. Define your signal categories

Map signals to your ICP. The most common high-intent signals:

- **Job changes**: New VP/C-level hire in your buyer persona role (decision maker just arrived, budget unlocked)
- **Funding events**: Series A/B/C closed in last 90 days (new money, new priorities)
- **Hiring signals**: Posting 3+ roles in your product's domain (building a team, need tools)
- **Technology signals**: Adopted a complementary or competing tool (integration opportunity or displacement play)
- **Content signals**: Engaged with competitors or relevant industry content

### 2. Set up signal feeds in Clay

Using the `clay-claygent` fundamental, create Clay tables with automated enrichment that refresh on a schedule. For job changes: use LinkedIn or People Data Labs. For funding: use Crunchbase or PitchBook enrichment. For hiring: use job board scrapers. Set each to run daily or weekly depending on volume.

### 3. Configure alert thresholds

Not every signal deserves action. Set thresholds: a single job posting is noise; five engineering hires in a month is signal. A seed round is early; a Series B is prime. Score signals by recency (last 30 days strongest) and intensity (multiple signals from one account).

### 4. Route signals to action

When a signal fires, route it: high-score signals go directly into your outreach queue in Attio tagged with the signal type. Medium-score signals get added to a watch list. Use the `attio-lists` fundamental to create dynamic lists per signal type.

### 5. Craft signal-specific messaging

Each signal type gets its own outreach angle. Funding: congratulate and tie your product to their new goals. Job change: welcome to the role and offer relevant help. Hiring: point out how your tool supports the team they are building. Generic outreach wastes the signal.

### 6. Review and tune weekly

Every week, review which signals led to meetings and which were noise. Adjust thresholds, add new signal sources, and deprecate ones that don't convert. Track signal-to-meeting rate in PostHog.
