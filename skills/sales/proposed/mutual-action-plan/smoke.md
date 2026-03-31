---
name: mutual-action-plan-smoke
description: >
  Mutual Action Plan (MAP) — Smoke Test. Manually co-create milestone timelines with 3 prospects
  in proposal stage to validate that shared accountability accelerates deal progression and
  reduces stalls compared to deals without MAPs.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Smoke Test"
time: "7 hours over 2 weeks"
outcome: ">=3 MAPs created and MAP deals close >=25% faster than non-MAP deals within 2 weeks"
kpis: ["MAP adoption rate", "Deal velocity (MAP vs non-MAP)", "Milestone completion rate", "Stall rate"]
slug: "mutual-action-plan"
install: "npx gtm-skills add sales/proposed/mutual-action-plan"
drills:
  - map-template-creation
  - threshold-engine
---

# Mutual Action Plan (MAP) — Smoke Test

> **Stage:** Sales > Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Create Mutual Action Plans for 3 active deals in proposal stage. Co-build each MAP with the prospect's champion during a live call. Measure whether MAP deals progress faster and stall less than deals without MAPs.

Pass: >= 3 MAPs created AND MAP deals close >= 25% faster than concurrent non-MAP deals within 2 weeks.
Fail: Fewer than 3 MAPs created, or MAP deals show no velocity improvement over non-MAP deals.

## Leading Indicators

- Prospects agree to MAP planning calls within 2 business days of request (champion is engaged)
- Prospects contribute at least 3 buyer-side milestones during the MAP call (they are co-owning the timeline)
- Milestone owners are named individuals, not departments (accountability is specific)
- At least 1 MAP deal completes its first milestone within 5 days of MAP creation (momentum is established)
- Prospects reference the MAP unprompted in follow-up communications ("per our action plan...")

## Instructions

### 1. Set up MAP tracking in Attio

Run the `map-template-creation` drill to create MAP custom attributes on the Deal object and build milestone templates for your deal types.

The drill creates these fields:
- `map_status` (Not Started / Active / Complete / Stalled)
- `map_created_date`
- `map_deal_type` (SMB / Mid-Market / Enterprise)
- `map_completion_pct`
- `map_at_risk`
- `map_expected_close`
- `map_stall_count`

Also creates 3 milestone templates (SMB, Mid-Market, Enterprise) stored as Attio notes. Review the templates and adjust milestone names and durations to match your actual sales process.

### 2. Select 3 deals and 3 non-MAP controls

From your active pipeline in Attio, select 6 deals currently in or entering proposal stage:
- 3 deals for MAP treatment (choose deals where you have an engaged champion)
- 3 deals as controls (similar deal size and stage, no MAP)

Log the selection in Attio. Tag MAP deals with `map_status` = "Not Started". Record the current stage entry date for all 6 deals so you can measure velocity differences.

### 3. Schedule MAP planning calls

For each of the 3 MAP deals, send a message to the champion:

```
Subject: Shared timeline for {Company} x {Your Company}

Hi {Champion},

To make sure we stay aligned on next steps, I'd like to build a shared action plan together — a simple timeline of what we each need to do between now and go-live.

It usually takes 20-30 minutes and helps both sides avoid surprises. Do you have time this week?

{Booking link via Cal.com}
```

**Human action required:** Send the scheduling messages. Book the calls.

### 4. Conduct MAP planning calls

**Human action required:** Run the 3 MAP planning calls. Record each call via Fireflies.

For each call, follow this structure:

**Open (2 min):** "I want to map out the steps between now and getting you live. Let's build this together so we both know what's coming."

**Map seller milestones (5 min):** Walk through what your team will deliver and when: proposal finalization, security questionnaire, SOW, implementation plan, onboarding.

**Map buyer milestones (10 min):** Ask the prospect to define their steps:
- "What needs to happen on your side before you can approve this?"
- "Who needs to review the contract? How long does that typically take?"
- "Is there a procurement or security review? When should we start that?"
- "Who is the final decision maker, and when can we get them aligned?"

For each buyer milestone, get:
- A named owner (person, not department)
- A realistic date
- Dependencies on other milestones

**Confirm timeline (5 min):** Read back the full MAP. Confirm dates. Identify the critical path — the sequence of milestones that determines the close date.

**Agree on cadence (2 min):** "I'll send you a weekly update on where we stand. If anything slips, we flag it immediately so we can adjust."

### 5. Log each MAP in Attio

Within 1 hour of each call, create an Attio note on the deal with the full MAP:

```markdown
## Mutual Action Plan — {Company}
### Created: {date} | Type: {SMB/Mid-Market/Enterprise}
### Expected Close: {date}

| # | Milestone | Owner | Due Date | Dependencies | Status |
|---|-----------|-------|----------|-------------|--------|
| 1 | {milestone} | {name, title} | {date} | {deps or "None"} | Not Started |
| 2 | ... | ... | ... | ... | Not Started |

### Critical Path
{Which milestones are on the critical path}

### Risks Identified
{Any concerns raised during the call}

### Next Milestone
{First upcoming milestone, owner, and due date}
```

Update Attio attributes:
- `map_status` → "Active"
- `map_created_date` → today
- `map_deal_type` → classified type
- `map_completion_pct` → 0
- `map_expected_close` → derived from MAP timeline

### 6. Send weekly MAP updates

At the end of each week, manually send a progress email to each MAP prospect:

```
Subject: {Company} Action Plan Update — Week of {date}

Hi {Champion},

Quick update on our shared timeline:

Completed:
{checkmark list of completed milestones}

Coming up:
{list of next milestones with dates and owners}

Progress: {n} of {total} milestones complete

{IF any overdue:}
Needs attention: {milestone} was due {date}. Can you give me an update on timing?

Let me know if anything has changed on your end.
```

Track PostHog events manually:
- `map_created` for each MAP
- `map_milestone_completed` when milestones are done
- `map_update_sent` for each weekly email

### 7. Evaluate against threshold

After 2 weeks, run the `threshold-engine` drill. Compare:

**MAP deals (3):**
- Average days in Proposed stage
- Number of milestones completed
- Stall events (7+ days with no milestone progress)

**Control deals (3):**
- Average days in Proposed stage
- Stall events

**Pass criteria:**
- >= 3 MAPs created with prospect participation
- MAP deals close >= 25% faster (or progress >= 25% further through pipeline)
- MAP deals have lower stall rate than controls

If **PASS:** MAP-driven deal management works. Proceed to Baseline to automate MAP generation and tracking.

If **FAIL:** Diagnose:
- **Low adoption (prospects won't do MAP calls):** Reposition the MAP as a "shared checklist" rather than a formal plan. Make it simpler.
- **No velocity improvement:** Milestones may be too vague or dates too generous. Tighten the timeline.
- **High stall rate despite MAP:** The milestones may not reflect the real buying process. Interview lost deals to understand actual buyer steps.

## Time Estimate

- MAP template setup in Attio: 1.5 hours
- Scheduling MAP calls (3 deals): 0.5 hours
- MAP planning calls (3 x 30 min): 1.5 hours
- Logging MAPs in Attio (3 x 20 min): 1 hour
- Weekly updates (2 weeks x 3 deals x 15 min): 1.5 hours
- Threshold evaluation: 1 hour
- **Total: ~7 hours over 2 weeks**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal records, MAP storage, milestone tracking | Free (up to 3 users); Plus $29/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Cal.com | Schedule MAP planning calls | Free (1 user); Teams $15/user/mo ([cal.com/pricing](https://cal.com/pricing)) |
| Fireflies | Record MAP planning calls | Free (800 min/mo); Pro $10/user/mo annual ([fireflies.ai/pricing](https://fireflies.ai/pricing)) |
| PostHog | Track MAP events | Free (1M events/mo) ([posthog.com/pricing](https://posthog.com/pricing)) |

**Estimated play-specific cost at Smoke:** Free (all tools have free tiers sufficient for 3 deals)

## Drills Referenced

- `map-template-creation` — Create MAP milestone templates by deal type and set up Attio tracking attributes
- `threshold-engine` — Evaluate MAP vs non-MAP deal velocity against the 25% improvement threshold
