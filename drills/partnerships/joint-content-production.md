---
name: joint-content-production
description: End-to-end workflow for co-creating a gated content asset with a partner, from topic selection through publication and lead capture
category: Partnerships
tools:
  - Anthropic
  - Clay
  - Attio
  - Crossbeam
  - Ghost
  - Loops
fundamentals:
  - ai-content-ghostwriting
  - anthropic-api-patterns
  - clay-claygent
  - clay-enrichment-waterfall
  - crossbeam-account-mapping
  - partner-co-marketing-brief
  - attio-deals
  - attio-notes
  - ghost-blog-publishing
  - loops-broadcasts
---

# Joint Content Production

This drill produces a single co-created content asset (ebook, guide, benchmark report, or checklist) with one partner company. The asset combines both companies' expertise and is published behind a shared lead-capture form so both sides generate leads from it.

## Input

- Partner company selected and agreement confirmed (from `partner-prospect-research` or manual identification)
- Your ICP definition (from `icp-definition` drill)
- Partner contact record in Attio with status "Active"
- Agreed content format and approximate scope

## Steps

### 1. Select the co-creation topic

Use the `clay-claygent` fundamental to research the intersection of your audience and your partner's audience. For 30 companies in your shared ICP, ask Claygent: "What is {Company}'s biggest challenge at the intersection of {your domain} and {partner domain}?" Aggregate into a frequency table. Select the topic appearing in 40%+ of results.

If you have Crossbeam configured, run the `crossbeam-account-mapping` fundamental first to identify the overlap population. Use overlapping accounts as the research sample -- these are the exact companies both audiences serve.

Record the selected topic, supporting data, and rationale in Attio as a note on the partner deal record using `attio-notes`.

### 2. Build the content outline

Call the Anthropic API using the `anthropic-api-patterns` fundamental to generate a structured outline:

```
POST https://api.anthropic.com/v1/messages
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 2000,
  "messages": [{
    "role": "user",
    "content": "Create a detailed outline for a co-branded {FORMAT} on the topic '{TOPIC}'. The asset is co-authored by {YOUR_COMPANY} (expertise: {YOUR_DOMAIN}) and {PARTNER_COMPANY} (expertise: {PARTNER_DOMAIN}). Target audience: {ICP_DESCRIPTION}. Structure: executive summary, 4-6 sections alternating between your and your partner's expertise areas, actionable takeaways, and a joint CTA. Each section should specify: which company contributes primary content, data points needed, and estimated word count. Total asset: {WORD_COUNT} words."
  }]
}
```

Store the outline in Attio on the partner deal record. Share with the partner for approval before proceeding.

**Human action required:** Send the outline to the partner contact for review and feedback. Wait for partner sign-off before drafting.

### 3. Draft your sections

For each section assigned to your company, use the `ai-content-ghostwriting` fundamental to generate first drafts:

```
POST https://api.anthropic.com/v1/messages
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 4000,
  "messages": [{
    "role": "user",
    "content": "Write section '{SECTION_TITLE}' for a co-branded {FORMAT} on '{TOPIC}'. This section is contributed by {YOUR_COMPANY}. Context: {OUTLINE_FOR_THIS_SECTION}. Requirements: include specific data, frameworks, or step-by-step instructions. Avoid generic advice. Reference your product only in the context of solving a specific problem. Write for {ICP_DESCRIPTION}. Word count: {SECTION_WORD_COUNT}."
  }]
}
```

**Human action required:** Review each section for accuracy and voice. Add proprietary data, customer examples, or founder perspective where drafts are generic.

### 4. Collect partner sections

Track partner section delivery in Attio using `attio-deals` -- update the deal record with:
- `sections_sent_to_partner`: count
- `sections_received_from_partner`: count
- `partner_sections_due_date`: date

If sections are late (>3 days past due date), send a reminder via the partner contact email.

**Human action required:** Review partner-contributed sections for quality. If sections are weak, use `ai-content-ghostwriting` to suggest specific improvements and send feedback to the partner.

### 5. Assemble and polish the asset

Combine all sections. Use the `ai-content-ghostwriting` fundamental to:
- Write transitions between sections so the asset reads as one cohesive document, not a patchwork
- Generate the executive summary from the assembled content
- Write the joint CTA paragraph at the end

```
POST https://api.anthropic.com/v1/messages
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 2000,
  "messages": [{
    "role": "user",
    "content": "Edit this co-branded {FORMAT} for consistency. Smooth transitions between sections from different authors. Ensure a single consistent voice throughout. Fix any redundancy. Write a 200-word executive summary and a joint CTA that mentions both {YOUR_COMPANY} ({YOUR_CTA_URL}) and {PARTNER_COMPANY} ({PARTNER_CTA_URL}). Full content: {ASSEMBLED_CONTENT}"
  }]
}
```

### 6. Publish with lead capture

Publish the asset using the `ghost-blog-publishing` fundamental:
- Create a landing page describing the asset with a form gate
- Host the asset PDF/page behind the form
- Set UTM parameters: `utm_source={partner_slug}&utm_medium=co-content&utm_campaign=joint-{asset_slug}`

Send a co-promotion email using the `loops-broadcasts` fundamental:
- Email to your list promoting the asset with the partner's endorsement
- Coordinate with the partner to send to their list simultaneously
- Use distinct UTM sources to attribute leads to each distribution channel

### 7. Attribute leads to the partnership

As form submissions arrive, create lead records in Attio using `attio-deals`:
- Tag each lead with `source: joint-content`, `partner: {partner_slug}`, `asset: {asset_slug}`
- Share lead data with the partner per your data-sharing agreement
- Track: total downloads, your-list downloads, partner-list downloads, organic downloads

## Output

- One published co-branded content asset behind lead capture
- Landing page with UTM tracking for both companies
- Co-promotion emails sent to both audiences
- Lead attribution in Attio by source channel and partner
- Deal record updated with asset performance data

## Triggers

Run this drill once per partner collaboration. At Smoke level, run once manually. At Baseline, run 3-5 times over 8 weeks. At Scalable, run continuously with an n8n-scheduled pipeline.
