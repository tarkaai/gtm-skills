---
name: ai-prospect-research
description: Use AI agents (Clay Claygent + Anthropic Claude) to conduct deep per-prospect research and generate personalized outreach hooks at scale
category: Prospecting
tools:
  - Clay
  - Anthropic
  - Attio
fundamentals:
  - clay-claygent
  - clay-enrichment-waterfall
  - clay-scoring
  - attio-contacts
  - attio-notes
  - posthog-custom-events
---

# AI Prospect Research

This drill replaces manual prospect research with AI-driven deep research. For each prospect, an AI agent (Clay Claygent or Anthropic Claude via API) researches the person and company, identifies specific pain points, finds recent trigger events, and generates a personalized outreach hook. The output is a Clay table where every row has a research brief and a ready-to-use personalization snippet that feeds directly into `cold-email-sequence` or `linkedin-outreach` drills.

## Input

- A scored prospect list in Clay (from `build-prospect-list` or `enrich-and-score` drill)
- ICP definition with documented pain points and trigger events (from `icp-definition` drill)
- Anthropic API key (for Claude-powered research when Claygent alone is insufficient)

## Why AI Research Matters for SDR Prospecting

Traditional SDR prospecting uses merge fields (first name, company name, job title). AI SDR prospecting generates a research brief per prospect that enables the outreach to reference: a specific blog post the prospect wrote, a recent company announcement, a technology they adopted, a hiring pattern that signals a problem your product solves, or a competitive tool they are currently using. This level of personalization at scale is what separates AI SDR from bulk outreach.

## Steps

### 1. Define research questions per ICP segment

Before running AI research, define what the agent should look for. Create a research prompt template in Clay using the `clay-claygent` fundamental. The prompt should instruct the agent to find:

- **Company context**: What does this company do? What stage are they at (funding, headcount growth, recent milestones)?
- **Prospect's role**: What is this person responsible for? What are they likely measured on?
- **Recent activity**: Has this person posted on LinkedIn in the last 90 days? Published a blog post? Spoken at a conference? Changed jobs recently?
- **Pain signals**: Is the company hiring for roles that suggest a problem your product solves? Did they recently adopt or drop a competitor tool? Are there public complaints from their users or employees about the problem area?
- **Competitive context**: What tools in your category is this company likely using? Are there signs of dissatisfaction (G2 reviews, Reddit threads, job postings mentioning migration)?

Store the research prompt as a Clay template column so it is consistent across all prospects.

### 2. Configure Clay Claygent columns

Using the `clay-claygent` fundamental, add these AI research columns to your Clay table:

- **`research_brief`** (Claygent column): Full research output. Prompt: "Research {company_name} and {first_name} {last_name} ({title} at {company_name}). Find: 1) One specific recent event or achievement at {company_name} from the last 90 days. 2) One pain point related to {icp_pain_area} that someone in {title}'s role typically faces. 3) One piece of content {first_name} has published or shared recently. 4) Whether {company_name} uses any tools in the {product_category} space. Return facts only, no speculation. Cite sources."

- **`personalization_hook`** (Claygent column): A one-sentence outreach opener derived from the research brief. Prompt: "Using this research: {research_brief}. Write a single opening sentence for a cold email from a founder. The sentence must reference ONE specific fact about {first_name} or {company_name} — not their job title or company description. It must sound like a human wrote it after genuine research. Under 25 words. No flattery. No 'I noticed that...' or 'I saw that...' patterns."

- **`pain_hypothesis`** (Claygent column): The likely pain point this prospect has. Prompt: "Based on this research: {research_brief}. What is the single most likely reason {first_name} at {company_name} would need a solution for {product_problem_statement}? Write one sentence. Be specific to their situation, not generic."

- **`outreach_angle`** (Claygent column): Which angle to use in outreach. Prompt: "Based on this research: {research_brief}. Classify the best outreach angle: 'trigger_event' (something just changed), 'competitive_displacement' (they use a competitor with known gaps), 'pain_match' (their role/company profile matches our ideal pain), or 'content_connection' (they published something related). Return only the classification label."

### 3. Run research in batches

Process 25-50 prospects at a time. Claygent credits are consumed per research query, so:

1. Start with your highest-scored prospects (Tier 1 from `enrich-and-score`)
2. Run the first batch of 25 and manually review the research_brief and personalization_hook columns
3. Check for: hallucinated facts (Claygent will occasionally invent events — verify the first 5 manually), generic hooks that could apply to anyone (rewrite the prompt if this happens), and missing data (if Claygent cannot find recent activity, the prospect may be too low-profile for AI research)
4. If quality is acceptable (80%+ of hooks are specific and accurate), run the remaining batches
5. Log quality metrics in PostHog using `posthog-custom-events`: `ai_research_completed` with properties `batch_size`, `quality_pass_rate`, `credits_used`

### 4. Enrich research with competitive intelligence

For prospects where `outreach_angle` is `competitive_displacement`, use the `clay-enrichment-waterfall` fundamental to pull additional data:

1. Run technographic enrichment (BuiltWith, Wappalyzer) to confirm the competitor tool is in use
2. Use Claygent to search for G2 reviews or Reddit discussions mentioning both the prospect's company and the competitor
3. If confirmed: update the personalization_hook to reference the specific competitive gap
4. If not confirmed: downgrade the outreach_angle to `pain_match` to avoid an embarrassing wrong guess

### 5. Score research quality and prioritize

Add a `research_quality_score` formula column using `clay-scoring`:

- Has a specific, verifiable personalization hook: +30 points
- Has a recent trigger event (last 90 days): +25 points
- Has confirmed competitive context: +20 points
- Has content connection (published/shared something): +15 points
- Has pain hypothesis tied to a real signal (not generic): +10 points

Re-sort by combined score (lead score + research quality score). The top-scored prospects get the first outreach batch.

### 6. Push research to CRM and outreach tools

Using the `attio-contacts` fundamental, sync the AI research data to Attio:

- Map `research_brief` to an Attio note on the contact (use `attio-notes`)
- Map `personalization_hook` to a custom attribute on the contact
- Map `outreach_angle` to a custom attribute for filtering
- Map `pain_hypothesis` to a note so the founder has context before calls

The `personalization_hook` and `pain_hypothesis` fields feed directly into the `cold-email-sequence` drill as merge variables and into `linkedin-outreach` as conversation context.

## Output

- Clay table where every prospect has: a research brief, a personalized outreach hook, a pain hypothesis, and a classified outreach angle
- Research data synced to Attio contacts as notes and custom attributes
- Quality metrics logged in PostHog for tracking research accuracy over time

## Reusability

This drill feeds into any outreach play that benefits from deep personalization: `cold-email-sequence`, `linkedin-outreach`, `founder-cold-email-copy`, `video-prospecting-outreach`. The research format is tool-agnostic — if you switch from Instantly to Smartlead, the personalization data still applies.
