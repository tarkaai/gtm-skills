---
name: stakeholder-mapping-baseline
description: >
  Stakeholder Mapping Framework — Baseline Run. Deploy automated stakeholder enrichment on
  every new deal, multi-thread engagement across all classified roles, and track whether
  multi-threaded deals close faster than single-threaded ones.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Social, Email"
level: "Baseline Run"
time: "20 hours over 4 weeks"
outcome: ">=70% of active deals have >=4 stakeholders mapped with role classifications, and multi-threaded deals (3+ engaged stakeholders) close >=25% faster than single-threaded deals"
kpis: ["Stakeholders mapped per deal", "Multi-threading rate", "Deal velocity delta (multi vs single-threaded)", "Single-threaded deal risk count"]
slug: "stakeholder-mapping"
install: "npx gtm-skills add sales/connected/stakeholder-mapping"
drills:
  - stakeholder-enrichment-automation
  - multi-channel-cadence
  - posthog-gtm-events
---

# Stakeholder Mapping Framework — Baseline Run

> **Stage:** Sales > Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Social, Email

## Outcomes

Automate stakeholder discovery so every new deal gets a pre-built org chart and role classifications. Multi-thread engagement across each deal's buying committee. Prove that deals with 3+ engaged stakeholders close at least 25% faster than single-threaded deals over a 4-week period.

## Leading Indicators

- Automated enrichment fires within 30 minutes of new deal creation and populates 10+ contacts
- Role classification accuracy exceeds 80% when validated by the sales team after discovery calls
- Multi-channel cadence reaches 3+ stakeholders per deal within the first week of engagement
- Single-threaded deal alerts fire correctly and prompt the sales team to widen their engagement

## Instructions

### 1. Deploy automated stakeholder enrichment

Run the `stakeholder-enrichment-automation` drill to build an n8n workflow that:
1. Triggers when a new deal enters the Connected stage in Attio
2. Pulls the company from the deal record
3. Runs org chart research via Clay (15-20 Director+ contacts)
4. Classifies each person into a buying committee role using Claude
5. Creates Person records in Attio with role, confidence, and sentiment attributes
6. Links all stakeholders to the deal
7. Generates a stakeholder map summary note on the deal

Test the workflow on 3 existing deals first. Verify that the contacts it finds and the roles it assigns are reasonable. Adjust the Clay search filters (seniority, departments) and the Claude classification prompt if accuracy is below 80%.

### 2. Configure multi-channel engagement per role

Run the `multi-channel-cadence` drill to design role-specific outreach sequences:

- **Economic Buyer**: Email → LinkedIn connection → Personalized video (ROI-focused). Tone: business value, time-to-impact, competitive risk of inaction.
- **Champion**: Email → LinkedIn → Share internal selling kit (one-pager, comparison doc). Tone: arm them with ammunition.
- **Influencer**: Email → LinkedIn → Invite to technical deep-dive or demo. Tone: technical credibility, integration details.
- **Blocker**: Direct email addressing their likely concern (security, compliance, integration risk) → Offer a 1:1 to discuss. Tone: acknowledge and address, not sell.
- **End User**: Email → Offer sandbox or trial access. Tone: practical, show how it makes their job easier.

Configure separate Instantly campaigns per role type. Tag each email with the deal_id and stakeholder_role for tracking.

### 3. Set up event tracking

Run the `posthog-gtm-events` drill to configure stakeholder-specific events:
- `stakeholder_mapped` (deal_id, person_id, role, confidence)
- `stakeholder_contacted` (deal_id, person_id, role, channel)
- `stakeholder_engaged` (deal_id, person_id, role, channel, response_type)
- `stakeholder_meeting_booked` (deal_id, person_id, role)
- `deal_multi_threaded` (deal_id, engaged_stakeholder_count)

Build a PostHog funnel: stakeholder_mapped → stakeholder_contacted → stakeholder_engaged → deal_advanced. Segment by stakeholder role to see which roles respond best.

### 4. Execute for 4 weeks

Let the automation run on all new deals entering Connected stage. Monitor:
- **Week 1**: Verify enrichment is firing correctly. Check 5 deals for data quality. Fix any Clay filter or classification issues.
- **Week 2**: Review multi-channel cadence performance by role. Which roles respond? Which channels work best per role?
- **Week 3**: Check multi-threading rates. How many deals have 3+ engaged stakeholders? Which deals are still single-threaded?
- **Week 4**: Compare deal velocity — are multi-threaded deals progressing faster?

**Human action required:** After the automated enrichment maps stakeholders, review and validate the classifications before launching outreach. Override incorrect roles. Add stakeholders the automation missed (from discovery calls). The automation builds the map; the human refines it.

### 5. Evaluate against threshold

Measure:
- **>=70% of active deals** have >=4 stakeholders mapped with role classifications
- **Multi-threaded deals** (3+ engaged stakeholders) close **>=25% faster** than single-threaded deals

Pull data from Attio (stakeholder counts) and PostHog (deal velocity by multi-threading status). If PASS, proceed to Scalable. If FAIL, diagnose:
- Low mapping rate → Clay enrichment returning too few contacts (loosen filters or add Apollo as backup)
- Low engagement rate → Outreach messaging not resonating per role (test new messaging angles)
- No velocity difference → Multi-threading may not be the bottleneck (check deal stage, deal size, ICP fit)

## Time Estimate

- Automation setup (n8n workflow, Clay config, classification prompt): 6 hours
- Multi-channel cadence design and Instantly campaign setup: 4 hours
- PostHog event configuration: 2 hours
- Weekly monitoring and refinement (4 weeks x 1 hour): 4 hours
- Stakeholder map validation (ongoing, ~15 min per deal): 4 hours

**Total: ~20 hours over 4 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM with stakeholder attributes and deal tracking | Plus at $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Clay | Org chart research and people enrichment | Launch at $185/mo or Growth at $495/mo ([clay.com/pricing](https://clay.com/pricing)) |
| n8n | Workflow automation for enrichment + cadence orchestration | Starter at $24/mo or self-hosted free ([n8n.io/pricing](https://n8n.io/pricing)) |
| Instantly | Multi-channel email sequences per stakeholder role | Growth at $30/mo ([instantly.ai/pricing](https://instantly.ai/pricing)) |
| PostHog | Event tracking and funnel analysis | Free tier (1M events/mo) ([posthog.com/pricing](https://posthog.com/pricing)) |
| Anthropic | Claude API for stakeholder role classification | Pay per token (~$0.01-0.03 per classification) ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| LinkedIn Sales Navigator | Supplementary org chart research | Core at $99.99/mo ([business.linkedin.com/sales-solutions](https://business.linkedin.com/sales-solutions/compare-plans)) |

**Estimated monthly cost for this level: $270-370** (Attio Plus $29 + Clay Launch $185 + n8n Starter $24 + Instantly $30 + PostHog free + Claude API ~$5-10 + LinkedIn optional)

## Drills Referenced

- `stakeholder-enrichment-automation` — Automated workflow that enriches new deals with org charts and pre-classifies stakeholders into buying roles
- `multi-channel-cadence` — Orchestrate role-specific outreach sequences across email, LinkedIn, and direct engagement
- `posthog-gtm-events` — Configure event tracking for stakeholder mapping, engagement, and deal velocity measurement
