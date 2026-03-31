---
name: interactive-content-tools-smoke
description: >
  Interactive Content Tools — Smoke Test. Build one interactive calculator, assessment, or grader
  targeting a validated ICP pain point. Deploy on a landing page with email-gated results and
  basic PostHog tracking. Prove that prospects will complete the tool and trade their email for results.
stage: "Marketing > Solution Aware"
motion: "Lead Capture Surface"
channels: "Website, Content"
level: "Smoke Test"
time: "6 hours over 3 weeks"
outcome: "≥50 tool completions and ≥15 email captures in 3 weeks"
kpis: ["Tool completion rate", "Email capture rate", "Conversion to demo/signup", "Tool shares"]
slug: "interactive-content-tools"
install: "npx gtm-skills add marketing/solution-aware/interactive-content-tools"
drills:
  - icp-definition
  - threshold-engine
---

# Interactive Content Tools — Smoke Test

> **Stage:** Marketing → Solution Aware | **Motion:** Lead Capture Surface | **Channels:** Website, Content

## Outcomes

Prove that your ICP will complete an interactive tool and exchange their email for the results. One tool, one landing page, one lead capture gate. No automation, no nurture sequences. Just: does this concept attract completions and captures?

**Pass threshold:** ≥50 tool completions and ≥15 email captures in 3 weeks

## Leading Indicators

- Tool start rate (views → starts) above 40% — visitors understand what the tool does and want to try it
- Field-level completion without major drop-offs — questions are answerable without research
- Time-to-completion under 90 seconds — the tool respects the user's time
- At least 1 organic share (someone sends the tool link to a colleague)

## Instructions

### 1. Define your ICP and tool concept

Run the `icp-definition` drill to identify your target persona, their pain points, and what calculations or assessments they need help with. The output tells you what tool to build.

Pick ONE tool concept. Choose the concept where:
- The pain is quantifiable (dollars lost, hours wasted, score below benchmark)
- Your ICP already has the input data in their head (no spreadsheet lookups required)
- The result connects naturally to your product's value prop

### 2. Build the interactive tool

Run the the interactive tool build workflow (see instructions below) drill to research the pain landscape, design the input fields and calculation logic, build the tool in Tally (free) or a simple web page, gate results behind email capture, and deploy on a landing page.

At Smoke level, use Tally for the tool (zero cost, fast to build). Keep it to 5-7 input fields maximum. The tool should be completable in under 90 seconds.

**Human action required:** Review the tool's calculations and result copy before launching. Verify the math is correct with 3-4 test inputs. Ensure the results screen delivers a genuine insight — not just a restatement of what the user entered.

### 3. Promote the tool manually

No paid promotion at Smoke level. Distribute through:
- Post on LinkedIn with a hook: "I built a free {tool type} for {ICP role}s. Takes 60 seconds. Here's what 3 beta testers found:" followed by anonymized example results
- Post in 2-3 communities where your ICP hangs out (Slack groups, subreddits, Discord servers). Frame as "I made this free tool — would love feedback"
- Email your existing contacts and newsletter list (if any)
- Add the tool link to your email signature and LinkedIn profile

**Human action required:** Write and post the promotion content. Respond to comments and DMs personally.

### 4. Monitor behavior

Check PostHog daily during the 3-week window. Look at:
- `tool_viewed` → `tool_started` conversion (are visitors engaging?)
- `tool_started` → `tool_email_captured` conversion (is the gate working?)
- `tool_field_completed` events by `field_position` (where do people abandon?)
- `tool_results_viewed` → `tool_cta_clicked` (are results compelling enough to act on?)

If completion rate is below 40% after week 1, simplify: remove 1-2 fields, shorten question text, or add default values to numeric inputs.

### 5. Evaluate against threshold

Run the `threshold-engine` drill to measure against: ≥50 tool completions and ≥15 email captures in 3 weeks.

- **PASS:** The tool concept works. Document which tool type, which pain point, and which promotion channels drove completions. Proceed to Baseline.
- **MARGINAL (30-49 completions or 10-14 captures):** The concept has potential. Simplify the tool (fewer fields), improve the landing page copy, or try different promotion channels. Re-run for 2 more weeks.
- **FAIL (<30 completions or <10 captures):** The tool concept or pain point may not resonate. Interview 3-5 ICP contacts about what calculation or assessment they wish existed. Build that instead.

---

## Time Estimate

- ICP research and tool concept selection: 1 hour
- Tool build (fields, calculations, results, email gate): 2 hours
- Landing page setup and PostHog tracking: 1 hour
- Promotion (LinkedIn, communities, email): 1 hour
- Monitoring and iteration over 3 weeks: 1 hour

Total: ~6 hours of active work over 3 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Tally | Build the interactive tool (forms, calculations, conditional logic) | Free (unlimited forms, submissions, webhooks) |
| PostHog | Track tool funnel events (views, starts, completions, captures) | Free up to 1M events/mo |
| Attio | Store tool leads as CRM contacts | Free up to 3 seats |

**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

## Drills Referenced

- `icp-definition` — define the target persona and identify the pain point the tool addresses
- the interactive tool build workflow (see instructions below) — build the interactive tool, deploy it, wire tracking and CRM routing
- `threshold-engine` — evaluate tool completions and email captures against the pass threshold
