---
name: case-study-recruitment-baseline
description: >
  Customer Story Pipeline — Baseline Run. Automate candidate identification and outreach
  into an always-on recruitment pipeline that produces at least 3 case studies per month
  without manual prospecting.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product, Email, Direct"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=3 case studies/month sustained over 2 months"
kpis: ["Recruitment acceptance rate", "Case study completion rate", "Pipeline velocity", "Time to publish"]
slug: "case-study-recruitment"
install: "npx gtm-skills add product/referrals/case-study-recruitment"
drills:
  - case-study-candidate-pipeline
  - case-study-creation
  - dashboard-builder
---

# Customer Story Pipeline — Baseline Run

> **Stage:** Product > Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Direct

## Outcomes

Transition from manual candidate selection to an always-on recruitment pipeline. The agent scores candidates weekly, runs outreach sequences automatically, and maintains a steady flow of interviews. Target: 3 published case studies per month for 2 consecutive months.

## Leading Indicators

- Candidate pool maintained at 20+ scored accounts with fit score >= 70
- Automated outreach sequence achieving 25%+ acceptance rate
- 4+ interviews scheduled per month (buffer for completion rate)
- Average time from interview to published case study under 21 days
- No manual candidate identification required after initial setup

## Instructions

### 1. Deploy the automated candidate pipeline

Run the `case-study-candidate-pipeline` drill to build the always-on scoring and outreach system:

1. Implement the 4-dimension scoring model (results strength, story potential, relationship health, timing signal) as a weekly n8n workflow
2. Create the "Case Study Candidates" list in Attio with score >= 70 filter
3. Build the 4-touch recruitment outreach sequence in Loops (3 emails + 1 in-app nudge)
4. Configure response handling: Cal.com booking webhook, decline tracking, cooldown enforcement
5. Set the active pipeline limit to 10 candidates at a time

Validate: run the scoring pipeline once and review the top 20 candidates. Cross-reference with your Smoke Test experience — do the top-scored candidates match the profile of customers who said yes? Adjust scoring weights if needed.

### 2. Standardize the case study production process

Run the `case-study-creation` drill with these Baseline-level enhancements:

- Create a reusable interview question template stored in Attio, with 3 variants by industry vertical
- Build a case study brief template: pre-populated with the customer's usage data, scoring dimensions, and suggested angle (pulled from Attio and PostHog at interview prep time)
- Standardize the review workflow: draft sent to customer within 5 business days of interview, customer has 7 business days to review, one revision round, then publish

**Human action required:** Conduct each interview personally. The interview itself remains human-led at Baseline; only the candidate identification and outreach are automated.

### 3. Build the recruitment dashboard

Run the `dashboard-builder` drill to create a PostHog dashboard tracking:

- **Candidate funnel**: scored -> in pipeline -> outreach sent -> responded -> interview scheduled -> interview done -> draft sent -> approved -> published
- **Acceptance rate**: interviews scheduled / outreach completed (target: 25%+)
- **Completion rate**: published / interviews done (target: 75%+)
- **Pipeline velocity**: case studies published per month (target: 3)
- **Time to publish**: median days from interview to publish (target: <21)
- **Candidate pool health**: count of accounts with score >= 70 not in cooldown

Set alerts:
- Pipeline velocity drops below 2/month for 2 consecutive weeks
- Candidate pool drops below 10
- Acceptance rate drops below 15%

### 4. Calibrate and iterate

After the first month:
1. Review the outreach sequence performance by touch: which email gets the most bookings? Which gets the most opens?
2. Review candidate scoring accuracy: of the candidates who accepted, what was their average score? Of those who declined, what was their average score? Tighten the threshold if low-score candidates are wasting pipeline capacity.
3. Review the content: are the resulting case studies being used by sales? Check if deal owners are attaching them to proposals. If not, the case study format may need adjustment.

After 2 months, evaluate: did you sustain 3+ case studies/month? If yes, proceed to Scalable. If no, diagnose: is the bottleneck candidate supply, acceptance rate, interview completion, or writing capacity?

## Time Estimate

- 6 hours: pipeline setup (scoring model, outreach sequence, response handling, dashboard)
- 2 hours/month: interview conducting (4 interviews x 30 min each)
- 4 hours/month: case study writing from transcripts
- 2 hours/month: pipeline review, calibration, and iteration

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Candidate scoring, funnel tracking, dashboards | Free tier (1M events/mo) |
| Attio | Candidate CRM, pipeline tracking | Free tier available |
| n8n | Scoring automation, response handling workflows | Self-hosted free; Cloud from $24/mo |
| Loops | Outreach email sequences | From $49/mo (1,000 contacts) |
| Intercom | In-app recruitment nudge | From $29/seat/mo (Essential) |
| Fireflies | Interview transcription | Free (800 min/mo); Pro $10/user/mo annual |
| Cal.com | Interview scheduling with webhook | Free (1 user); Teams $15/user/mo |
| Ghost | Case study publishing | Free (self-hosted); $9/mo (starter) |

**Play-specific cost:** Loops ~$49/mo + Intercom ~$29/mo = ~$78/mo

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._

## Drills Referenced

- `case-study-candidate-pipeline` — automated scoring, candidate selection, and outreach sequence
- `case-study-creation` — standardized interview, writing, and publishing workflow
- `dashboard-builder` — recruitment funnel dashboard with alerts
