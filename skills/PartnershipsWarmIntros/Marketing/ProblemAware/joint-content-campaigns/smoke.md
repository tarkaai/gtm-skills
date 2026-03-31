---
name: joint-content-campaigns-smoke
description: >
  Joint Content Campaigns -- Smoke Test. Identify one partner, co-create one gated
  content asset (ebook, guide, or report), distribute to both audiences, and measure
  whether joint content generates qualified leads from problem-aware prospects.
stage: "Marketing > ProblemAware"
motion: "PartnershipsWarmIntros"
channels: "Content, Email"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=1 co-created asset published and >=10 qualified leads in 4 weeks"
kpis: ["Downloads per asset", "Download-to-lead conversion rate", "Partner response rate", "Time to publish"]
slug: "joint-content-campaigns"
install: "npx gtm-skills add PartnershipsWarmIntros/Marketing/ProblemAware/joint-content-campaigns"
drills:
  - icp-definition
  - partner-prospect-research
  - joint-content-production
  - threshold-engine
---
# Joint Content Campaigns -- Smoke Test

> **Stage:** Marketing -> ProblemAware | **Motion:** PartnershipsWarmIntros | **Channels:** Content, Email

## Outcomes
One co-created content asset published and generating downloads. At least 10 qualified leads attributed to the asset within 4 weeks. This proves that partner co-creation amplifies reach beyond your own audience.

## Leading Indicators
- Partner responds to outreach within 5 business days
- Content outline agreed within 1 week of first contact
- Both companies contribute sections on schedule
- Downloads begin within 48 hours of publication
- At least 30% of downloads come from the partner's audience (not yours)

## Instructions

### 1. Define your partner ICP
Run the `icp-definition` drill to define what makes an ideal content partner: complementary product (not competitor), overlapping buyer persona, similar company stage, active content marketing program. Document the partner ICP in Attio.

### 2. Research and select one partner
Run the `partner-prospect-research` drill to identify 10-20 candidate partners. Score each on audience overlap, content quality, and responsiveness. Select the single best-fit partner for this smoke test.

**Human action required:** Reach out to the selected partner personally. Propose a specific co-creation project: "We co-author a [format] on [topic], gate it behind a shared form, each promote to our lists. Both keep the leads." Use warm intros where possible. Log all outreach in Attio.

### 3. Co-create the content asset
Run the `joint-content-production` drill to:
- Select the topic using Clay research on the shared ICP
- Generate a structured outline with section assignments
- Draft your sections using Claude
- Collect partner sections
- Assemble, polish, and publish behind a lead-capture form
- Send co-promotion emails to both audiences

Track every step in Attio on the partner deal record: outline agreed, sections drafted, sections received, asset published, emails sent.

### 4. Monitor early performance
Check the asset landing page analytics in PostHog daily for the first week:
- Total downloads
- Downloads by source (your email, partner email, organic)
- Form completion rate
- Any leads that immediately book a meeting

Log observations in Attio.

### 5. Evaluate against threshold
Run the `threshold-engine` drill to measure against: >=1 co-created asset published and >=10 qualified leads in 4 weeks.

If PASS: proceed to Baseline. The signal confirms that partner-amplified content generates leads you cannot reach alone.
If FAIL: analyze the failure mode:
- Low downloads from partner audience -> partner did not promote effectively, try a different partner
- Low download-to-lead conversion -> the topic or format did not resonate, try a different angle
- Partner did not deliver on time -> improve partner qualification criteria

## Time Estimate
- 1 hour: partner ICP definition and prospect research
- 1 hour: partner outreach and negotiation
- 2 hours: content co-creation (outline, your sections, assembly)
- 1 hour: publication and co-promotion setup
- 1 hour: monitoring and threshold evaluation

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM for partner tracking and lead attribution | Free tier available; https://attio.com/pricing |
| Clay | Partner research and ICP enrichment | From $149/mo; https://clay.com/pricing |
| Crossbeam | Account overlap mapping with partner | Free tier available; https://www.crossbeam.com/pricing |
| Anthropic Claude | Content drafting and outline generation | Pay-per-use; https://www.anthropic.com/pricing |
| Ghost | Asset landing page and publication | Free self-hosted; https://ghost.org/pricing |
| Loops | Co-promotion email broadcast | Free up to 1,000 contacts; https://loops.so/pricing |

## Drills Referenced
- `icp-definition` -- define what makes an ideal content partner
- `partner-prospect-research` -- find, audit, and score partner candidates
- `joint-content-production` -- end-to-end co-creation from topic selection through publication
- `threshold-engine` -- evaluate pass/fail against the 10-lead threshold
