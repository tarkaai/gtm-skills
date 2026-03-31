---
name: trade-show-presence-scalable
description: >
  Trade Show Presence — Scalable Automation. Scale to a quarterly trade show
  calendar with agent-managed pre-show targeting, automated enrichment
  pipelines, A/B tested booth messaging, content repurposing from each show,
  and cross-show performance optimization. Multiply pipeline generated per
  show without proportional effort increase.
stage: "Marketing > SolutionAware"
motion: "MicroEvents"
channels: "Events"
level: "Scalable Automation"
time: "80 hours over 4 months"
outcome: ">=400 booth conversations across 4+ shows, >=80 qualified leads, >=25 meetings booked, cost per meeting trending down quarter-over-quarter"
kpis: ["Booth conversations per show", "Qualified lead rate", "Meetings booked per show", "Cost per meeting", "Nurture conversion rate", "Content derivative registrations"]
slug: "trade-show-presence"
install: "npx gtm-skills add marketing/solution-aware/trade-show-presence"
drills:
  - trade-show-booth-operations
  - trade-show-lead-nurture
  - ab-test-orchestrator
  - follow-up-automation
  - content-repurposing
  - trade-show-performance-monitor
---

# Trade Show Presence — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** MicroEvents | **Channels:** Events

## Outcomes

- Scale from ad-hoc shows to a consistent quarterly trade show calendar with automated pre-show and post-show operations
- Generate 80+ qualified leads across 4+ shows with agent-managed targeting, enrichment, and nurture
- Systematically test booth messaging, demo approaches, and nurture copy to find the highest-converting combination
- Build a content flywheel where each show produces derivative content that drives future registrations and pipeline
- Reduce cost per meeting over time through operational efficiency and better show selection

## Leading Indicators

- Pre-show target engagement rate improving show-over-show (outreach effectiveness)
- Net-new leads per show increasing even as you attend the same circuit (broader targeting)
- Meetings from automated nurture exceed meetings from manual follow-up (automation is working)
- Content derivatives from past shows drive >=10% of next show's pre-show engagement
- Cost per qualified lead trending down vs Baseline benchmarks

## Instructions

### 1. Build the annual trade show calendar

Using data from Baseline, build a scored calendar of shows for the next 6-12 months:

- Run `event-scouting` quarterly to refresh the show pipeline. Score shows using Baseline data: shows that produced >=15 qualified leads per event are "must attend." Shows that produced <5 qualified leads are "re-evaluate or drop."
- Build a master calendar in Attio with: show name, dates, city, estimated cost, ICP density score, historical performance (if attended before), and status (confirmed/tentative/evaluating).
- Budget allocation: allocate 60% of trade show budget to proven shows (top performers from Baseline), 30% to new shows with high ICP density scores, and 10% to experimental shows in new verticals or regions.
- Target cadence: 1 show per month or 4+ shows per quarter, depending on your market density.

### 2. Automate pre-show operations

Upgrade the `trade-show-booth-operations` drill to run with minimal manual intervention:

- **Automated attendee pipeline**: Build an n8n workflow triggered when a new show is added to the Attio calendar. The workflow: extracts the attendee list (via event API or web scrape), runs Clay enrichment, scores against ICP criteria, segments into priority tiers, and pushes to an Attio list. This should take the agent 2 hours per show vs 4+ hours manually.
- **Pre-show outreach sequences**: Move from manual personal emails to a structured Loops sequence for pre-show outreach. Segment by priority:
  - Priority 1 (top 10 targets): Personal email from a founder or exec. Offer a private demo at the booth.
  - Priority 2 (next 40 targets): Automated but personalized email sequence: "We're at booth #{number} — here's what we're showing that's relevant to {their pain point}."
  - Priority 3 (remaining ICP matches): Single awareness email: "Come visit us at booth #{number} at {show}."
- **Staff briefing automation**: Auto-generate booth staff briefs per show by pulling target lists, competitor exhibitor data, and show-specific talking points from Attio.

### 3. A/B test booth and nurture variables

Run the `ab-test-orchestrator` drill to systematically test one variable at a time across successive shows:

**Variables to test (in priority order):**

1. **Booth hook**: Test 2-3 different opening statements across shows. Track which hook produces the highest demo-to-conversation rate. Example: "We help {ICP title}s cut {pain point} by 50%" vs "Most {ICP title}s waste 10 hours/week on {pain point}."
2. **Demo path effectiveness**: Track which demo path (elevator, guided, deep) produces the most meetings. Optimize the guided demo — it is your workhorse. Test different pain point focus areas within the guided path.
3. **Pre-show outreach subject lines**: A/B test within the same show's outreach. Split the target list and test two subject lines. Measure open rate and reply rate.
4. **Nurture sequence copy**: Test different Tier 2 sequence approaches: resource-led ("here's a case study") vs question-led ("are you still evaluating solutions for {pain point}?") vs social-proof-led ("companies like {similar company} use us to...").
5. **Follow-up timing**: Test Tier 1 follow-up at 6 hours vs 12 hours vs 24 hours. Measure reply rate.

For each test, log the hypothesis, the variants, and the result in Attio. After 4 shows, compile a "winning formula" document: best booth hook, optimal demo path, strongest nurture copy angle, ideal follow-up timing.

### 4. Scale post-show follow-up

Upgrade the `trade-show-lead-nurture` drill and add `follow-up-automation` for multi-channel coverage:

- **Tier 1 at scale**: For shows with 10+ Tier 1 leads, the Loom approach becomes a bottleneck. Introduce a hybrid: the top 5 Tier 1s get personal Loom videos; the remaining get a high-quality templated email with show-specific personalization (their pain point, booth notes) auto-pulled from Attio by the agent.
- **Multi-channel nurture**: Add LinkedIn touches to the Tier 2 sequence using `follow-up-automation`. After email 1 (day 1), send a LinkedIn connection request (day 2). After email 2 (day 4), engage with their recent LinkedIn post if they have one. This doubles the touchpoints without doubling the email volume.
- **Cross-show nurture**: For prospects you met at multiple shows (repeat contacts), create a dedicated high-intent sequence: "We've now met at both {show 1} and {show 2} — that usually means {pain point} is a real priority. Let's find 15 minutes to go deeper."
- **Automated deal creation**: Upgrade Attio workflows: any Tier 1 lead that replies positively to follow-up automatically gets a deal created with estimated value based on their company size (enriched by Clay).

### 5. Build the content repurposing engine

Run the `content-repurposing` drill to extract content from each show:

- **Demo recordings**: Record your best 3-minute guided demo at each show (set up a camera or use a screen recording). Extract the core demo flow as a shareable video.
- **Show insights**: After each show, write a "What we learned at {show name}" post. Include: top 3 pain points attendees mentioned, competitive landscape observations, and your product's reception.
- **Customer quotes**: With permission, capture 2-3 short video testimonials from interested booth visitors. "What challenge brought you to {show name}?" format.
- **Social content**: Each show produces at least 5 LinkedIn posts: day-of booth photo, key insight, customer quote clip, competitive observation, and "what we heard" recap.
- **Newsletter content**: Summarize show insights for your Loops newsletter to drive awareness for the next show.

Schedule derivatives to publish over the 4-6 weeks between shows. Link each piece of content to the next show's pre-registration or company page.

### 6. Monitor and optimize the trade show motion

Run the `trade-show-performance-monitor` drill to build always-on reporting:

- Per-show ROI dashboard in PostHog: booth visits, demos, meetings, pipeline, cost, ROI for each show
- Cross-show comparison: identify winning show characteristics, booth approaches, and nurture sequences
- Cost tracking in Attio: total investment per show vs pipeline generated
- Quarterly review: aggregate performance, compare trade shows vs other motions, adjust calendar

### 7. Evaluate against the threshold

After 4 months (4+ shows), evaluate:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Total booth conversations | >=400 | Sum across all shows |
| Qualified leads (Tier 1+2) | >=80 | Attio records by tier |
| Meetings booked | >=25 | Cal.com + manually tracked within 30 days per show |
| Cost per meeting | Trending down | Total show costs / meetings, show-over-show |
| Nurture conversion rate | >=8% | Meetings from nurture / total nurtured leads |

**PASS**: Core metrics met and cost per meeting trending down. Proceed to Durable. You have a scalable trade show machine with working automation and clear ROI.

**FAIL**: Diagnose by metric:
- Low conversations at scale: Show calendar includes too many low-ICP-density events. Cull the calendar — focus on the top 3 shows by historical performance. Invest more in fewer, better shows.
- Low qualified rate: Booth messaging not resonating at scale. Revisit A/B test results — are you using the winning hook? Is your ICP definition too broad?
- High cost per meeting: Operational costs not declining as expected. Audit: are you spending too much on booth materials? Is travel for too many staff members? Can you reduce Clay credit usage with smarter targeting?

## Time Estimate

- Annual calendar planning and show selection: 6 hours
- Pre-show automation setup (n8n workflows, Loops sequences, Clay templates): 10 hours
- A/B test planning and implementation: 4 hours
- Content repurposing system setup: 4 hours
- Per-show agent effort (targeting, enrichment, nurture, analytics): 8 hours x 5 shows = 40 hours
- Per-show human effort (booth staffing): excluded (human hours)
- Cross-show analysis and optimization: 8 hours
- Performance monitoring setup and quarterly review: 8 hours
- **Total: ~80 hours over 4 months** (agent hours)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Clay | Pre-show enrichment + lead enrichment at scale | $185/mo Launch or $495/mo Growth — [clay.com/pricing](https://www.clay.com/pricing) |
| Loops | Pre-show outreach + tiered nurture sequences | $49/mo (5,000 contacts) — [loops.so/pricing](https://loops.so/pricing) |
| Loom | Personalized Tier 1 video follow-ups | $12.50/mo Business — [loom.com/pricing](https://www.loom.com/pricing) |
| PostHog | Full-funnel tracking + experiments | Free tier: 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Attio | CRM, deal tracking, show calendar, campaign management | $29/user/mo Plus — [attio.com](https://attio.com) |
| n8n | Pre-show automation, lead enrichment pipelines, nurture triggers | Self-hosted free or Cloud Pro EUR60/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Descript | Demo recording clips + content derivatives | $24/mo Creator — [descript.com/pricing](https://www.descript.com/pricing) |
| Cal.com | Meeting booking CTA | Free tier — [cal.com/pricing](https://cal.com/pricing) |

**Estimated play-specific cost at Scalable: $360-680/mo** (Clay + Loops + Loom + Descript + n8n Pro; PostHog/Cal.com on free tier)

Note: Show-specific costs at this level typically $4,000-10,000 per show (better booth locations, more polished materials, 2-3 staff). Budget $16,000-40,000/quarter for 4 shows.

## Drills Referenced

- `trade-show-booth-operations` — automated pre-show targeting, enrichment pipelines, and scalable lead capture
- `trade-show-lead-nurture` — tiered multi-channel nurture with escalation triggers and cross-show re-engagement
- `ab-test-orchestrator` — systematically test booth hooks, demo paths, outreach copy, nurture angles, and follow-up timing
- `follow-up-automation` — multi-channel follow-up combining email and LinkedIn touches
- `content-repurposing` — transform each show into derivative content that drives future pipeline
- `trade-show-performance-monitor` — per-show ROI dashboards, cross-show comparison, and quarterly motion review
