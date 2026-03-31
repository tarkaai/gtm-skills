---
name: quora-ads-question-targeting
description: Configure Quora Ads question, topic, and keyword targeting to reach problem-aware audiences on specific question pages
tool: Quora
product: Quora Ads
difficulty: Config
---

# Quora Ads — Question & Topic Targeting

Configure Quora's contextual targeting options to place ads on specific question pages where your ICP is actively researching problems your product solves. Quora offers four contextual targeting types and three audience targeting types.

## Contextual Targeting Types

### 1. Topic Targeting (recommended starting point)

Show ads alongside question pages tagged with specific Quora topics. This is the broadest contextual option and delivers the most scale.

**How to configure in Ads Manager:**

1. In the Ad Set, select **Topic Targeting**
2. Search for topics related to your product category and ICP pain points
3. Select 10-20 topics per ad set
4. Quora will show your ad on any question page tagged with those topics

**Topic selection strategy for problem-aware B2B:**

- **Tier 1 (direct problem)**: Topics describing the exact problem your product solves. Example for a DevOps tool: "Continuous Integration," "Deployment Automation," "Site Reliability Engineering"
- **Tier 2 (adjacent problem)**: Topics where the ICP hangs out but the problem is implicit. Example: "Software Engineering Management," "Cloud Computing," "Docker"
- **Tier 3 (industry)**: Broad industry topics for volume. Example: "Software as a Service," "Startup Companies," "Enterprise Software"

Start with Tier 1 topics only. Add Tier 2 and 3 as you need more reach.

**Estimated reach:** 50,000-500,000 monthly impressions per 10-20 topics (varies by topic popularity).

### 2. Question Targeting (most granular)

Target specific Quora question pages by URL. Your ad appears only when users view those exact questions.

**How to configure:**

1. In the Ad Set, select **Question Targeting**
2. Search for questions using keywords, or paste question URLs directly
3. Select individual questions (Quora shows estimated monthly views per question)
4. Target questions with 1,000+ monthly views for meaningful delivery

**Question selection strategy:**

1. Search Quora for questions your ICP asks. Examples:
   - "What is the best tool for [your category]?"
   - "How do you solve [problem your product addresses]?"
   - "What are alternatives to [competitor]?"
   - "[Pain point] — how do other companies handle this?"
2. Filter by monthly views (visible in Ads Manager). Target questions with 500+ monthly views.
3. Select 50-100 questions per ad set for meaningful reach
4. Group questions by theme into separate ad sets (allows per-theme creative and bidding)

**Estimated reach:** 5,000-50,000 monthly impressions per 50-100 questions. Question targeting is the most precise but lowest volume option.

**Important:** Quora recommends pairing question targeting with at least one other targeting type for adequate delivery. Use it as a complement to topic targeting, not a replacement.

### 3. Keyword Targeting

Target questions in bulk based on keywords present in question text. Broader than question targeting, narrower than topic targeting.

**How to configure:**

1. In the Ad Set, select **Keyword Targeting**
2. Enter keywords related to your product and ICP problems
3. Use a mix of broad and specific keywords:
   - Broad: "deployment automation" (matches many questions)
   - Specific: "kubernetes deployment pipeline" (matches fewer, higher-intent questions)
4. Add 20-50 keywords per ad set
5. Use negative keywords to exclude irrelevant questions (e.g., exclude "free" if targeting enterprise buyers)

**Estimated reach:** 20,000-200,000 monthly impressions per 20-50 keywords.

### 4. Broad Targeting

No contextual constraints. Quora places ads across the platform using its own optimization. Use only at Scalable/Durable levels when contextual targeting is maxed out and you want to let Quora's algorithm find high-intent users.

## Audience Targeting Types

Layer audience targeting on top of contextual targeting for precision.

### 1. Website Traffic Audience (Retargeting)

Retarget visitors to your website who viewed your Quora landing page or other pages.

1. Install the Quora Pixel on your website (see `quora-ads-conversion-tracking`)
2. In Ads Manager, go to **Audiences** > **Create Audience** > **Website Traffic**
3. Define the audience: all website visitors, or specific URL patterns (e.g., `/pricing`, `/demo`)
4. Set the lookback window: 7 days (hot), 30 days (warm), 90 days (cool)
5. Minimum audience size: 300 users for Quora to serve ads

### 2. List Match Audience

Upload a list of email addresses to target (or exclude) specific people.

1. In Ads Manager, go to **Audiences** > **Create Audience** > **List Match**
2. Upload a CSV of email addresses (must be emails used for Quora accounts)
3. Quora matches against its user base (expect 20-40% match rate)
4. Use cases: target newsletter subscribers, exclude existing customers, target event attendees

### 3. Lookalike Audience

Create an audience similar to an existing audience (website visitors or list match).

1. Source audience must have 300+ matched users
2. In Ads Manager, go to **Audiences** > **Create Audience** > **Lookalike**
3. Select the source audience and desired reach (1%-10% of Quora users in target geo)
4. Smaller percentage = more similar to source, less reach

## Targeting Combinations

Combine contextual + audience targeting for precision:

| Level | Contextual | Audience | Use Case |
|-------|-----------|----------|----------|
| Smoke | Topic (Tier 1) | None | Prove the channel works |
| Baseline | Topic + Question | Website retargeting | Repeatable with retargeting |
| Scalable | Topic + Question + Keyword | Retargeting + Lookalike | Scale with audience expansion |
| Durable | All + Broad | All + List Match | Full optimization across all levers |

## Targeting Research Workflow

For an agent preparing targeting recommendations:

1. **Identify ICP pain points**: List 5-10 problems your product solves
2. **Search Quora for each pain point**: Use Quora search to find popular questions
3. **Map to Quora topics**: Note which topics these questions are tagged with
4. **Score questions**: By monthly views (visible in Ads Manager), relevance to ICP, and commercial intent
5. **Build targeting spec**: Output a structured list of topics, questions, and keywords grouped by ad set
6. **Present for human execution**: The agent cannot configure targeting directly — output the spec for manual entry in Ads Manager
