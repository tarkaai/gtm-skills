---
name: podcast-sponsor-rate-negotiation
description: Negotiate paid podcast sponsorship rates, packages, and terms with hosts or ad sales contacts
tool: Anthropic
product: Claude API
difficulty: Config
---

# Podcast Sponsor Rate Negotiation

Structure and negotiate paid podcast ad sponsorship rates, commitment packages, and terms with podcast hosts or their ad sales representatives.

## Prerequisites

- Podcast identified and qualified via `podcast-sponsor-marketplace-search` or `podcast-directory-search`
- Budget range approved for this placement
- Contact email for the podcast host, producer, or ad sales contact
- Anthropic API key for drafting negotiation emails

## Steps

### 1. Request the media kit

Send an initial inquiry to the podcast's ad contact. Use the Anthropic API to draft:

```
POST https://api.anthropic.com/v1/messages
Authorization: Bearer {ANTHROPIC_API_KEY}
Content-Type: application/json

{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 512,
  "messages": [{
    "role": "user",
    "content": "Write a short email (under 100 words) to the host/producer of {podcast_name} requesting their advertising media kit or sponsor rate card. Mention that we are {company_description} and our target audience overlaps with their listeners. Note that we are interested in a host-read ad placement. Keep the tone professional and concise. Sign off as {sender_name}, {sender_title} at {company_name}."
  }]
}
```

Send via your business email. Log the outreach in Attio on the podcast record.

### 2. Evaluate the media kit

When the media kit arrives, extract and record:

- **Downloads per episode**: Average and recent trend (growing or declining)
- **Audience demographics**: Job titles, industries, company sizes, geographic distribution
- **Ad formats available**: Pre-roll (15-30 sec), mid-roll host-read (60 sec), post-roll (15-30 sec), custom integration
- **CPM rate**: Per ad format. B2B niche benchmark: $25-40 CPM for host-read mid-roll
- **Flat rate option**: Some podcasts quote per-episode flat rates instead of CPM
- **Minimum commitment**: Per-episode, multi-episode package (3, 6, 12 episodes), or monthly
- **Lead time**: How far in advance must the ad script/talking points be submitted
- **Calendar availability**: Which episode dates are open for sponsorship
- **Past sponsors**: Who else has advertised (validates the program; reveals competitors)
- **Reporting**: Will the host share download numbers for your sponsored episode?

### 3. Calculate effective cost

Normalize pricing for comparison:

```
effective_cpm = (cost_per_placement / downloads_per_episode) * 1000
cost_per_estimated_listener = cost_per_placement / (downloads_per_episode * 0.7)
```

The 0.7 factor estimates unique listeners (some downloads are automated or incomplete).

For B2B podcasts, target:
- Effective CPM $20-50 is competitive
- Effective CPM $50-80 is acceptable for high-ICP-density niche shows
- Effective CPM $80+ needs negotiation or a pass

### 4. Negotiate the rate

Common negotiation levers for podcast sponsorships:

- **Test episode discount**: "We would like to try a single episode at a reduced rate. If performance meets our benchmarks, we will commit to a multi-episode package."
- **Multi-episode package**: "Can you offer a 15-20% discount if we commit to 4 episodes?"
- **Off-peak/bonus episodes**: "Do you have upcoming episodes with lower demand where we could get a discounted placement?"
- **Value exchange**: "We have an audience of {your_audience_size}. We can mention your podcast in our newsletter as a reciprocal promotion."
- **Performance clause**: "Can we structure a portion of the rate as performance-based — a base fee plus a bonus per lead generated via our tracking URL?"
- **Longer reads**: "Instead of 60 seconds, could we get a 90-second read at the same rate? The extra detail helps our conversion."

Draft the negotiation email using the Anthropic API with the specific lever. Log in Attio.

### 5. Confirm the booking

Once terms are agreed, capture the finalized deal. Create a deal record in Attio:

- Deal name: "Podcast Sponsor — {podcast_name} — {episode_date}"
- Amount: agreed price per placement
- Stage: "Booked"
- Close date: the episode air date
- Custom fields:
  - Podcast name and host
  - Ad format (pre-roll / mid-roll / post-roll / custom)
  - Read duration (15s / 30s / 60s / 90s)
  - Script/talking points deadline
  - Estimated downloads per episode
  - Number of episodes committed
  - Total package cost
  - Reporting commitment (will host share download numbers)
  - Payment terms

Set a reminder for the script submission deadline.

### 6. Log in budget tracker

Record the committed spend. Tag as `podcast-sponsorship` with the podcast name and episode date. This feeds the `budget-allocation` drill for cross-channel budget optimization.

## Error Handling

- **Host does not respond within 7 business days**: Send one follow-up. Podcast hosts are often solo operators with slower response times than newsletter publishers. If no response after 14 days, move to the next podcast.
- **Rate exceeds budget**: Counter with a specific number, not "can you do better?" Example: "Our budget for a test placement is $200. Is there a format or off-peak episode that could work at that level?"
- **Host only offers multi-episode minimum**: Ask for a single test episode with a commitment to book the package if results meet your threshold.
- **No media kit exists**: Some smaller podcasts do not have a formal media kit. Ask for: downloads per episode, audience description, and their rate for a 60-second host-read mid-roll.

## Alternative Tools

- **AdvertiseCast (Libsyn Ads)**: Handles booking and payment through the platform, reducing direct negotiation
- **Podcorn**: Self-serve marketplace with direct negotiation but platform-managed payment
- **Gumball**: Transparent pricing, less negotiation needed
- **Attio**: CRM for tracking negotiation status and deal terms
- **HubSpot / Salesforce / Pipedrive / Clarify**: Alternative CRMs for deal tracking
