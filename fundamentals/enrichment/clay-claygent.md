---
name: clay-claygent
description: Use Claygent AI agent to research prospects with natural language prompts
tool: Clay
difficulty: Intermediate
---

# Use Claygent for AI-Powered Research

## Prerequisites
- Clay account with credits (Claygent uses 5-10 credits per query)
- Table with company or contact seed data

## Steps

1. **Understand Claygent.** Claygent is Clay's built-in AI agent that can browse the web, read pages, and answer natural language questions about companies or people. It is more flexible than structured enrichment but costs more credits and is slower.

2. **Add a Claygent column.** In your table, add a new enrichment column and select "Claygent" as the provider. Write a natural language prompt that references other columns using curly braces: "What does {Company Name} sell and who are their main competitors?"

3. **Write effective prompts.** Be specific about the output format you want. Bad: "Tell me about this company." Good: "In one sentence, describe what {Company Name} does. Then list their top 3 competitors by name only." Claygent works best with structured output instructions.

4. **Use for hard-to-find data.** Claygent excels at: recent news about a company, identifying the specific product a company sells, finding case studies or testimonials, and determining technology stack from job postings. Use structured enrichment for standard firmographics.

5. **Control costs.** Claygent costs 5-10 credits per row depending on query complexity. Only run it on your Tier 1 prospects (see `fundamentals/enrichment/clay-scoring`) to keep costs manageable. Never run Claygent on your full table as a first step.

6. **Validate outputs.** Claygent can hallucinate. Spot-check the first 10 results manually before trusting the data for outreach personalization. If accuracy is below 90%, rewrite your prompt to be more specific.
