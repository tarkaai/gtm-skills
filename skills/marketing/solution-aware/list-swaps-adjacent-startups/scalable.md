---
name: list-swaps-adjacent-startups-scalable
description: >
  List Swap With Partner — Scalable Automation. Automate a portfolio of 10+
  swap partners with scheduled swaps, email delivery, reciprocal sends, lead
  routing, and performance tracking — all running without manual coordination.
stage: "Marketing > Solution Aware"
motion: "Partnerships & Warm Intros"
channels: "Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥ 300 clicks and ≥ 8 meetings over 2 months"
kpis: ["Click-through rate", "Email open rate", "Click-to-meeting rate", "Swaps completed per month", "Partner retention rate"]
slug: "list-swaps-adjacent-startups"
install: "npx gtm-skills add marketing/solution-aware/list-swaps-adjacent-startups"
drills:
  - partner-pipeline-automation
  - tool-sync-workflow
---

# List Swap With Partner — Scalable Automation

> **Stage:** Marketing → Solution Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Email

## Outcomes

A portfolio of 10+ active swap partners with automated swap scheduling, email delivery, reciprocal send management, lead routing, and performance tracking. At least 300 clicks and 8 meetings over 2 months. The 10x multiplier at this level comes from: (a) managing more partners simultaneously without proportional effort, (b) reusing proven email templates across similar partner audiences, (c) automating the swap coordination that was manual at Baseline, and (d) using Crossbeam to identify partners with the highest account overlap.

## Leading Indicators

- Partner pipeline converts at >= 25% (prospects contacted to active swap partners)
- Swap cadence is >= 6 swaps completed per month across the portfolio
- Lead routing from PostHog to Attio happens automatically within 5 minutes of a swap click
- Per-partner click-to-meeting rate holds at or above Baseline average (>= 3%)
- Partner retention: >= 70% of partners agree to a second swap after the first
- Time spent on swap coordination drops below 3 hours/week (down from 6+ at Baseline)
- No more than 1 inbound swap to your list per week (protect list engagement)
- Reciprocity stays balanced: net swap value for any partner never exceeds 3x in either direction

## Instructions

### 1. Build the swap scheduling automation

Run the the list swap scheduling workflow (see instructions below) drill to create n8n workflows that automate the full swap lifecycle:

**Swap calendar workflow (weekly cron, Monday 9am):**
- Query Attio for active partners where "Next Swap Date" is within the next 14 days
- For each upcoming swap, check: is our email copy ready? Have we received the partner's email? Are both sides approved?
- Alert if any swap is missing email copy or partner approval
- Auto-send approved emails to partners with tracked CTA links
- Track swap status through: draft → approved → sent-to-partner → confirmed-sent

**Reciprocal send workflow:**
- When partner email is marked "reviewed" in Attio, automatically create a Loops broadcast targeting the agreed list segment
- Schedule for the agreed swap date
- After send, update Attio and fire `list_swap_reciprocal_sent` event in PostHog

**Confirmation workflow (daily cron at 6pm on swap days):**
- Verify both sides sent on scheduled swap days
- If one side didn't send: alert and follow up
- If both confirmed: mark swap as "Completed," set next swap date based on cadence tier

### 2. Scale the partner portfolio

Using the partner research from Baseline, expand to 10+ active partners. Run the `partner-pipeline-automation` drill to automate partner onboarding:

**Prioritize partners by:**
- Audience overlap with your ICP (highest first)
- Account overlap from Crossbeam (if configured) — partners whose subscribers are literally your target accounts
- Similar or larger list size (aim for 2,000+ subscribers minimum)
- Proven co-marketing friendliness (already swap with other companies)

**Cadence tiering:**
- **Monthly** (top 3-5 partners from Baseline with best click-to-meeting rates)
- **Bimonthly** (solid performers or new partners with promising first swaps)
- **Quarterly** (new partners in trial period)

Never swap the same partner more than once per month to avoid audience fatigue.

### 3. Templatize email production

Create a swap email template library based on Baseline winners:

- Organize templates by angle: curiosity, data-driven, story-driven
- Organize templates by partner audience type: technical founders, marketing leaders, product managers, executives
- Each template has fill-in variables: `{partner_audience_pain}`, `{your_specific_benefit}`, `{proof_stat}`, `{low_commitment_cta}`
- An agent can generate a new swap email from a template in under 2 minutes per partner

Store the template library in Attio or a shared document linked from each partner record. Track which templates produce the best click-to-meeting rates.

### 4. Connect all tools

Run the `tool-sync-workflow` drill to ensure data flows bidirectionally:

- PostHog list swap events → Attio partner records (clicks, meetings, conversion rates per swap)
- Attio partner status changes → n8n workflows (trigger next automation step)
- Loops broadcast metrics → Attio (track how your list responded to each inbound swap)
- Instantly outreach events → Attio partner pipeline (track partner prospect outreach status, if using Instantly for partner discovery)

Verify the sync by checking: when a swap click arrives in PostHog, does the Attio partner record update within 5 minutes?

### 5. Run the scaled program

Execute 6+ swaps per month across the portfolio:

- Stagger swaps across the month (max 2 per week, max 1 inbound swap to your list per week)
- Rotate email variants so the same partner's audience sees different angles on repeat swaps
- Track which partners have the best click-to-meeting conversion (not just click volume)
- Identify "anchor partners" — the 3-5 partners that consistently generate the most meetings
- Monitor reciprocity: ensure balanced value exchange. If a partner consistently receives 3x more value from your list than you get from theirs, renegotiate or reduce cadence.

### 6. Manage list health

Your own list is an asset. Protect it:

- Cap inbound swaps at 4 per month (1 per week max)
- Monitor unsubscribe rate after each inbound swap. If any partner's email causes >0.5% unsubscribes, pause swaps with that partner and review email quality.
- Track list engagement (open rate, click rate) on your own newsletters. If engagement drops >10% in months with active swaps, reduce inbound swap frequency.
- Never swap with a partner whose audience or content is off-brand for your subscribers.

### 7. Evaluate against threshold

After 2 months, measure aggregate results:

**Pass threshold: >= 300 clicks AND >= 8 meetings over 2 months**

- **Pass**: Document the partner portfolio, automation workflows, per-partner economics, and top email templates. Identify anchor partners. Proceed to Durable.
- **Marginal**: 200-299 clicks or 5-7 meetings. Scale is working but conversion needs optimization. Test different landing pages, email variants, or partner types before Durable.
- **Fail**: <200 clicks. Diagnose: Is the partner pipeline too small? Are swaps actually running on schedule? Is email quality declining as you scale? Are the wrong partners in the portfolio? Fix the bottleneck and run one more month.

## Time Estimate

- Automation setup (n8n workflows, tool sync): 15 hours
- Partner pipeline expansion (research + outreach): 12 hours
- Email template library creation: 5 hours
- Ongoing management (8 weeks x 2.5 hours/week): 20 hours
- Analysis and optimization: 8 hours

Total: ~60 hours over 2 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| n8n | Workflow automation (swap scheduling, lead routing, confirmations) | Cloud Starter: ~EUR 24/mo; Pro: ~EUR 60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Partner CRM, swap tracking, pipeline management | Plus: $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Event tracking, attribution, analytics | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Loops | Send partner swap emails to your list (broadcasts) | Paid from $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Crossbeam | Partner account overlap mapping | Free tier: 3 seats; Connector from ~$400/mo ([crossbeam.com/pricing](https://www.crossbeam.com/pricing)) |
| Instantly | Partner outreach sequences (optional) | Growth: $47/mo ([instantly.ai/pricing](https://instantly.ai/pricing)) |
| Clay | Partner enrichment (if expanding research) | Launch: $185/mo ([clay.com/pricing](https://www.clay.com/pricing)) |

**Estimated cost for this level: ~$80-200/mo** (n8n + Attio Plus required; Crossbeam free tier, Loops paid tier. Clay and Instantly optional depending on existing tools.)

## Drills Referenced

- the list swap scheduling workflow (see instructions below) — automate swap cadence, reciprocal sends, and partner coordination across 10+ partners
- `partner-pipeline-automation` — automate partner outreach, onboarding, and lifecycle management
- `tool-sync-workflow` — connect PostHog, Attio, Loops, and n8n for bidirectional data flow
