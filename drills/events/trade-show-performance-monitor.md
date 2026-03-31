---
name: trade-show-performance-monitor
description: Track trade show ROI across shows, compare booth performance, nurture conversion, and generate post-show reports that feed optimization decisions
category: Events
tools:
  - PostHog
  - Attio
  - n8n
fundamentals:
  - posthog-dashboards
  - posthog-custom-events
  - posthog-funnels
  - attio-reporting
  - n8n-scheduling
  - n8n-workflow-basics
---

# Trade Show Performance Monitor

This drill builds the measurement and reporting layer for trade show presence. It tracks which shows produce pipeline, which booth approaches convert best, whether nurture sequences are working, and how the trade show motion is improving over time. The outputs feed directly into the `autonomous-optimization` drill at Durable level.

## Input

- PostHog events from `trade-show-booth-operations` and `trade-show-lead-nurture` drills
- Attio deal records tagged with trade show source
- At least 2 trade shows worth of data (minimum for comparison)
- Show costs tracked: booth fee, travel, shipping, staffing, swag

## Steps

### 1. Build the trade show dashboard

Using the `posthog-dashboards` fundamental, create a "Trade Show Presence" dashboard:

**Top row (headline metrics):**
- Total booth visits (last 90 days / rolling)
- Booth-to-demo conversion rate (what % of visitors got a demo)
- Demo-to-meeting conversion rate
- Pipeline generated from trade shows ($)
- Cost per qualified lead (total show cost / qualified leads)
- Trade show ROI (pipeline generated / total show cost)

**Middle row (per-show breakdown):**
- Table: show name, date, city, booth visits, demos given, meetings booked, Tier 1 leads, deals created, pipeline value, total cost, ROI
- Bar chart: meetings booked per show
- Funnel: booth_visit -> demo_given -> meeting_booked -> deal_created -> deal_won

**Bottom row (nurture and conversion signals):**
- Nurture conversion by tier: what % of each tier eventually books a meeting?
- Average days from booth visit to meeting booked (speed to pipeline)
- Follow-up response rate by tier and sequence step
- Interest level distribution across shows (are you attracting higher-quality traffic over time?)
- Pre-show outreach acceptance rate (did proactive targeting work?)

### 2. Build cross-show comparison analysis

Using `posthog-funnels`, create funnel analyses grouped by `show_name` to compare shows:

- Which shows have the highest booth-to-demo rate? (audience quality signal)
- Which shows have the highest demo-to-meeting rate? (product-market fit signal)
- Which shows produce the largest deal sizes? (audience budget signal)
- Which shows have the best nurture response rates? (lead quality signal)

This identifies:
- Shows with high traffic but low conversion (wrong audience — consider skipping next year)
- Shows with low traffic but high conversion (right audience — worth a bigger investment)
- Shows where Tier 1 leads concentrate (your best trade shows)

### 3. Track show costs and ROI

Create an Attio list "Trade Show Investments" with fields per show:

| Field | Description |
|-------|-------------|
| `show_name` | Conference/trade show name |
| `show_date` | Event dates |
| `booth_cost` | Booth rental fee |
| `travel_cost` | Flights, hotel, transport for all staff |
| `shipping_cost` | Booth materials, swag, equipment shipping |
| `staffing_cost` | Opportunity cost of staff time (days x daily rate) |
| `swag_cost` | Branded materials, giveaways |
| `total_cost` | Sum of all costs |
| `leads_captured` | Total booth interactions logged |
| `qualified_leads` | Tier 1 + Tier 2 count |
| `meetings_booked` | Meetings booked within 30 days |
| `pipeline_created` | Dollar value of deals created |
| `deals_won` | Deals closed-won attributed to this show |
| `revenue_attributed` | Revenue from won deals |
| `roi` | (pipeline_created - total_cost) / total_cost |

Update deal attribution monthly as nurture converts leads over time. A trade show's full ROI picture takes 90-180 days to materialize.

### 4. Configure automated reporting

Using `n8n-scheduling`, create two recurring reports:

**Post-show report (runs 30 days after each show):**
1. Pull all trade show metrics from PostHog for this show
2. Pull deal status from Attio using `attio-reporting`
3. Generate a structured post-show report:
   - Show summary: dates, cost, staff, booth location
   - Lead metrics: total captured, by tier, demo rate, meeting rate
   - Nurture metrics: follow-up sent, opened, replied, meetings from nurture
   - Pipeline: deals created, total pipeline value, deals advanced
   - ROI: cost per lead, cost per meeting, pipeline-to-cost ratio
   - Competitive intel: what competitors were present, their booth approach, messaging themes
   - Recommendations: should we attend next year? what to change?
4. Post to Slack and store in Attio

**Quarterly trade show review (runs quarterly):**
1. Aggregate all shows for the quarter
2. Compare: which shows produced the best ROI? Which produced the most pipeline?
3. Calculate: trade show motion cost per pipeline dollar vs other motions (outbound, paid, content)
4. Trend analysis: is trade show ROI improving, flat, or declining?
5. Generate quarterly recommendations: shows to continue, shows to drop, new shows to evaluate, budget reallocation suggestions

### 5. Build trade show selection intelligence

After 3+ shows, the data enables predictive show selection:

- Correlate show characteristics (size, industry focus, geography, cost tier) with outcomes
- Score upcoming shows based on historical patterns: "Shows with 500-2,000 attendees in {industry vertical} produce 3x more meetings per dollar than shows with 5,000+ attendees"
- Feed this intelligence back into the `event-scouting` drill for future show selection
- Track whether pre-show outreach acceptance rate correlates with show-day booth performance (it usually does — shows where targets engage pre-show tend to produce better booth traffic)

## Output

- PostHog dashboard with real-time trade show metrics
- Per-show ROI tracking in Attio
- Automated post-show reports (30-day lag for nurture attribution)
- Quarterly trade show motion reviews
- Show selection intelligence for future planning

## Triggers

- Dashboard: always-on, review after each show
- Post-show report: 30 days after each show via n8n cron
- Quarterly review: end of each quarter
- Show selection intelligence: updated after each post-show report
