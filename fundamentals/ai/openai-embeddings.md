---
name: openai-embeddings
description: Use OpenAI embeddings for lead similarity, content matching, and semantic search in GTM
tool: OpenAI
difficulty: Advanced
---

# OpenAI Embeddings for GTM

### Use cases
1. **ICP lookalike scoring:** Embed descriptions of your best 20 customers. For each new lead, embed their Clay-enriched profile and compute cosine similarity. Score > 0.8 = strong match.
2. **Content-prospect matching:** Embed your blog posts and case studies. When a new lead enters, find the most relevant content to send them.
3. **Competitive positioning:** Embed competitor messaging alongside yours. Identify gaps in your positioning.

### Implementation
1. Use `text-embedding-3-small` (1536 dimensions, $0.02/1M tokens)
2. Store embeddings in a simple JSON file or Supabase pgvector column
3. Compute cosine similarity in n8n using a Code node
4. Cache embeddings — recompute only when source data changes

### Tips
- Batch embed (up to 2048 inputs per request) to minimize API calls
- Normalize text before embedding: lowercase, remove special chars, trim to 500 words
- Refresh ICP embeddings monthly as your customer base evolves
