---
name: technical-discovery-call
description: Run a structured technical discovery call — prep with tech stack research, execute with category-targeted questions, extract requirements, score fit, and log to CRM
category: Sales
tools:
  - Fireflies
  - Attio
  - Anthropic
  - Cal.com
fundamentals:
  - fireflies-transcription
  - fireflies-action-items
  - call-transcript-tech-requirements-extraction
  - attio-deals
  - attio-notes
  - attio-custom-attributes
  - calcom-booking-links
---

# Technical Discovery Call

This drill covers the full lifecycle of a technical discovery call: pre-call tech stack research review, category-targeted question preparation, transcript analysis, technical fit scoring, and CRM logging. Designed for founder-led sales where the founder (or a solutions engineer) uncovers technical requirements that could block or accelerate a deal.

## Input

- Deal record in Attio with tech stack discovery already completed (from `tech-stack-discovery` drill)
- Cal.com booking link for scheduling
- Fireflies configured to auto-join meetings

## Steps

### 1. Pre-call review

Pull the deal record and technical intelligence profile from Attio:
```
attio.get_record({ object: "deals", record_id: "{deal_id}" })
attio.get_notes({ object: "deals", record_id: "{deal_id}" })
```

Find the note titled "Technical Discovery Call Prep" created by the `tech-stack-discovery` drill. Review:
- Known tech stack and predicted integrations
- Security posture and expected compliance requirements
- Technical maturity score
- Predicted blockers to verify
- Priority questions to ask

### 2. Generate a technical discovery question guide

Based on the tech intelligence profile gaps, generate tailored questions using Claude. Focus on the five requirement categories:

**Integration questions (always ask):**
- "What systems does your team use day-to-day that this tool would need to work with?"
- "Do you have an API-first approach, or do you prefer native integrations and UI-based connectors?"
- "Are there any systems where bi-directional sync is a hard requirement vs. one-way data push?"
- "Who manages integrations internally — engineering team, IT, or a specific platform team?"
- "Have you had integration projects fail before? What went wrong?"

**Security/compliance questions (probe based on predicted posture):**
- "What certifications do you require from vendors? SOC2, ISO27001, HIPAA, others?"
- "Do you have a formal vendor security review process? What does that look like and how long does it typically take?"
- "What are your data residency requirements? Does data need to stay in a specific region?"
- "Do you require SSO/SAML integration? What identity provider do you use?"
- "Is there an information security team that would need to review this before procurement?"

**Infrastructure questions (tailor to maturity level):**
- "What's your deployment preference — cloud SaaS, private cloud, or on-premise?"
- "If cloud, which provider — AWS, Azure, GCP? Any restrictions?"
- "What are your requirements for environment isolation — do you need a dedicated instance?"
- "Do you have VPN or IP whitelisting requirements for vendor tools?"
- "What does your disaster recovery and backup policy look like for critical systems?"

**Performance questions (scale-dependent):**
- "How many users would be on the platform? What's your expected growth over the next 12 months?"
- "What uptime SLA do you need? Is 99.9% sufficient or do you require 99.99%?"
- "Are there peak usage patterns we should know about — end of quarter, batch processing windows?"
- "What latency expectations does your team have for the core workflows?"
- "What data volume are we talking — number of records, transactions per day, storage needs?"

**Data migration questions (if replacing an existing tool):**
- "What system(s) would we be migrating data from? How much historical data needs to come over?"
- "What data formats are you working with? Any proprietary formats we should know about?"
- "Is there a migration timeline constraint — a contract end date or a hard cutover deadline?"
- "What's your tolerance for data downtime during migration?"
- "Are there data mapping complexities — custom fields, relationships, or hierarchies that need to be preserved?"

Store the customized question guide as an Attio note on the deal using `attio-notes`. Tag the note with `tech_discovery_prep`.

### 3. Ensure Fireflies is recording

Verify Fireflies is configured to auto-join the scheduled meeting:
```graphql
query { user { integrations { calendar_connected } } }
```

If the meeting is on Cal.com, verify the calendar sync is active.

### 4. Post-call: extract technical requirements from transcript

After the call, wait for Fireflies to process the transcript (typically 5-15 minutes). Then run the `call-transcript-tech-requirements-extraction` fundamental to extract structured technical requirements from the conversation.

The extraction returns:
- Per-category scores (0-100) for: integrations, security/compliance, infrastructure, performance, data migration
- Specific requirements with priority levels and supporting quotes
- Blocker flags for each category
- Tech stack context: existing tools, tech maturity, internal resources, decision influencers
- Composite fit score and technical verdict
- Gaps requiring follow-up

### 5. Update CRM with discovery results

Using `attio-deals`, update the deal record with the post-call technical scores:
- `tech_integrations_score`, `tech_security_score`, `tech_infrastructure_score`, `tech_performance_score`, `tech_migration_score`
- `tech_composite_fit_score` and `tech_verdict`
- `tech_blocker_count` and `tech_blockers_summary`
- `tech_assessment_source: "discovery_call"`
- `tech_last_assessed: "{today}"`

Compare the post-call scores against the pre-call predictions from `tech-stack-discovery`. Log discrepancies >20 points — this calibrates the pre-call research model.

### 6. Log the call summary and technical requirements

Using `attio-notes`, create a structured note on the deal:

```
## Technical Discovery Call — {date}
### Attendees: {names and roles}

### Integration Requirements
| System | Type | Priority | Complexity | Quote |
|--------|------|----------|------------|-------|
| {system} | {api/sso/data_sync} | {must_have/nice_to_have} | {simple/moderate/complex} | "{quote}" |

### Security & Compliance
- Certifications required: {list}
- Security review process: {description}
- Data residency: {requirement}
- SSO: {provider} — {required/preferred}
- Blockers: {list}

### Infrastructure
- Deployment: {cloud_saas/private_cloud/on_premise/hybrid}
- Cloud provider: {aws/azure/gcp}
- Special requirements: {list}

### Performance
- User volume: {count}, growth expected: {rate}
- SLA requirement: {uptime%}
- Data volume: {estimate}

### Data Migration
- Migrating from: {systems}
- Historical data: {scope}
- Timeline constraint: {date or "none"}

### Composite Technical Fit: {score}/100 — {verdict}
### Blockers: {count}
{list of blockers with mitigation options}

### Gaps Requiring Follow-Up
{areas where requirements are still unclear}

### Next Steps
{action items from the call}
{recommended follow-up actions from extraction}
```

### 7. Route based on technical verdict

- **Strong Fit (75+):** Move deal to "Technically Qualified" stage. No blockers prevent closing. Proceed with commercial discussions.
- **Moderate Fit (50-74):** Flag specific gaps. If blockers are addressable (roadmap item, partner integration, configuration change), create follow-up tasks:
  - Schedule solutions engineer call for complex integration discussions
  - Send relevant technical documentation (API docs, security whitepaper, compliance certs)
  - Engage product team if a blocker requires roadmap commitment
- **Weak Fit (25-49):** Multiple blockers or significant gaps. Escalate to product/engineering for feasibility assessment before investing more sales time. Set a 1-week deadline for internal feasibility response.
- **No Fit (<25):** Critical blockers with no path to resolution. Move deal to "Technically Disqualified." Log the specific reasons — this feeds product roadmap decisions and helps identify patterns in lost deals.

**Human action required:** For any deal with unresolved blockers, the founder must decide whether to invest engineering resources to address them or disqualify the deal.

## Output

- Updated technical fit scores on the deal record in Attio
- Structured call notes with per-category requirement details
- Blocker list with severity and mitigation options
- Deal routed to the correct pipeline stage
- Follow-up tasks created for any unresolved technical gaps

## Triggers

Run after every technical discovery call. Re-run after follow-up technical calls (solutions engineer sessions, security review calls) to re-assess technical fit as new information surfaces.
