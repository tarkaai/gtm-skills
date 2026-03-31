---
name: account-thread-mapping
description: Design and execute a coordinated multi-stakeholder outreach plan within a single account, assigning per-persona channels, messages, and timing
category: Outreach
tools:
  - Attio
  - Clay
  - Instantly
  - LinkedIn
  - n8n
fundamentals:
  - stakeholder-role-classification
  - attio-custom-attributes
  - attio-notes
  - attio-deals
  - clay-people-search
  - clay-enrichment-waterfall
  - instantly-campaign
  - linkedin-organic-engagement
  - n8n-workflow-basics
---

# Account Thread Mapping

This drill takes a single target account with its stakeholder map and produces a coordinated, per-persona outreach plan. Each stakeholder gets a different message angle, channel, and timing -- designed so the touches reinforce each other without conflicting. This is what makes outreach "multi-threaded" rather than just "multi-contact."

## Prerequisites

- Stakeholder map complete for the account (run `stakeholder-research` or `stakeholder-org-mapping` drill first)
- At least 3 classified stakeholders per account with email and/or LinkedIn URL
- Attio deal record with stakeholders linked
- ICP and messaging framework defined

## Input

- Account name and Attio deal ID
- Stakeholder map: list of contacts with role (Economic Buyer, Champion, Influencer, Blocker, End User), title, email, LinkedIn URL, engagement level

## Steps

### 1. Assign message angles by stakeholder role

Each role cares about different things. Map your product's value to each stakeholder's priorities:

- **Economic Buyer** (CFO, VP, CEO): ROI, total cost of ownership, risk mitigation, time-to-value. Lead with business outcomes and numbers.
- **Champion** (hands-on user, team lead): how this makes them look good internally, ease of adoption, proof it works. Lead with case studies from similar roles.
- **Influencer** (architect, senior IC): technical depth, integration with existing stack, security, scalability. Lead with technical content.
- **Blocker** (procurement, legal, IT security): compliance, vendor stability, data handling, pricing transparency. Lead with trust signals.
- **End User** (individual contributor): daily workflow improvement, learning curve, time saved. Lead with product experience.

For each stakeholder on the account, write one first-touch message using their role's angle. Store the draft in Attio notes on the contact record using the `attio-notes` fundamental.

### 2. Assign channels per stakeholder

Not every channel works for every persona. Default channel assignment:

- **C-suite / VP**: LinkedIn first (they read LinkedIn), then email. Never cold call first.
- **Director / Senior Manager**: Email first (they process email efficiently), LinkedIn second.
- **IC / Technical**: Email or community channels. LinkedIn for senior ICs only.

Override based on enrichment data from Clay: if a contact has posted on LinkedIn in the last 30 days, prioritize LinkedIn. If they have no LinkedIn activity, default to email. Use `clay-people-search` to check LinkedIn activity recency.

Store channel assignments as a custom attribute on each Attio contact record using `attio-custom-attributes`: `outreach_channel_primary` (Email, LinkedIn, Phone) and `outreach_channel_secondary`.

### 3. Design the cross-stakeholder timing sequence

The key to multi-threading is **coordinated timing**. Within one account, touches should land in a specific order to create internal conversation:

- **Day 0**: Contact the Champion first. They are most likely to respond and can provide intel.
- **Day 2**: Contact the End Users. If they engage, the Champion has allies when advocating internally.
- **Day 4**: Contact the Influencer with technical content. If the Champion or End Users mention you, the Influencer is primed.
- **Day 7**: Contact the Economic Buyer. By now, other stakeholders may have mentioned your name, making the cold outreach warmer.
- **Day 10**: If a Blocker is identified, proactively address their concerns with a targeted message. Waiting lets the Champion build internal momentum first.

Adjust timing based on account urgency. High-priority accounts (active evaluation, funding signal): compress to 7 days. Standard accounts: use the 10-day cadence above.

Store the timing plan as a structured note on the deal in Attio:
```
## Thread Map — {Account Name}
Day 0: {Champion Name} via {Channel} — {Message angle summary}
Day 2: {End User Name} via {Channel} — {Message angle summary}
Day 4: {Influencer Name} via {Channel} — {Message angle summary}
Day 7: {Economic Buyer Name} via {Channel} — {Message angle summary}
Day 10: {Blocker Name} via {Channel} — {Message angle summary}
```

### 4. Execute the threads

Launch each thread according to the timing plan:

- For email threads: use the `instantly-campaign` fundamental. Create separate sequences per stakeholder role with the role-specific messaging. Tag each sequence with the account name and stakeholder role for attribution.
- For LinkedIn threads: use the `linkedin-organic-engagement` fundamental. Send connection requests on the assigned day. Queue the follow-up message for 2 days after acceptance.

**Critical coordination rule:** If any stakeholder responds positively, pause all other threads for that account for 24 hours. Check Attio deal status before each send. Use `n8n-workflow-basics` to build a pre-send check that queries Attio for recent activity on the account.

### 5. Track thread-level engagement

Log every touch and response per stakeholder in Attio using `attio-deals`. Track:
- Which stakeholder responded first
- Which message angle generated the response
- Whether internal referrals happened (e.g., "My colleague [Champion] mentioned you...")
- Time from first touch to first response per role
- Time from first response to meeting booked

### 6. Adapt threads based on responses

As responses come in, adjust the remaining threads:

- **Champion responds positively**: Accelerate Economic Buyer outreach. Ask Champion for a warm intro. Adjust Economic Buyer message to reference the Champion's interest.
- **End User responds positively**: Add their experience as a proof point in the Influencer message.
- **Blocker surfaces concerns**: Pause the Economic Buyer thread until you have answers. Prepare objection-handling content.
- **No responses after Day 10**: Trigger the breakup sequence from `cold-email-sequence` for all contacts simultaneously. If one responds to the breakup, re-engage the full thread map.

## Output

- Per-account thread map with stakeholder-specific messages, channels, and timing stored in Attio
- Coordinated cross-stakeholder outreach executing across email and LinkedIn
- Real-time thread status tracking in CRM showing which contacts are engaged
- Engagement data feeding back to refine future thread maps

## Triggers

- Run once per account when the stakeholder map is complete
- Re-run when new stakeholders are discovered (from `stakeholder-org-mapping` drill)
- Re-run when a thread stalls (no response from any stakeholder after 14 days)
