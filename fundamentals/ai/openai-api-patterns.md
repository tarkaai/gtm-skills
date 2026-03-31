---
name: openai-api-patterns
description: Use the OpenAI API for embeddings, content generation, and classification in GTM workflows
tool: OpenAI
difficulty: Config
---

# OpenAI API Patterns for GTM

### When to use OpenAI
OpenAI excels at: text embeddings for similarity search (finding similar leads/content), structured classification (routing leads, categorizing objections), and fast content generation.

### Key patterns
1. **Lead similarity scoring:** Embed your best customers' descriptions, then embed new leads. Cosine similarity identifies lookalikes.
2. **Email classification:** Classify inbound replies as positive/negative/neutral/out-of-office using GPT-4o-mini (fast, cheap).
3. **Content ideation:** Generate content topic ideas based on your best-performing posts and ICP pain points.
4. **Data normalization:** Clean and standardize CRM data (company names, titles, industries) using structured outputs.

### Setup
- API key from platform.openai.com
- Use gpt-4o-mini for classification and simple generation
- Use text-embedding-3-small for embeddings
- Always use structured outputs (JSON mode) for data processing tasks
