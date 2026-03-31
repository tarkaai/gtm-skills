---
name: consensus-score-computation
description: Compute a weighted consensus score across all stakeholders in a deal based on sentiment, influence, and alignment
tool: Anthropic
product: Claude API
difficulty: Advanced
---

# Consensus Score Computation

Calculate a single numeric consensus score (0-100) for a deal based on every mapped stakeholder's sentiment, influence level, and alignment with each other. The score predicts how likely the buying committee is to reach a collective "yes" decision.

## Prerequisites

- Stakeholder map with role classifications (from `stakeholder-role-classification`)
- Per-stakeholder sentiment and support levels (from `stakeholder-sentiment-extraction`)
- Influence weights by role (configured below)
- Attio deal record with stakeholder data

## Formula

### Influence Weights by Role

| Role | Weight | Rationale |
|------|--------|-----------|
| Economic Buyer | 0.35 | Controls budget, ultimate veto power |
| Champion | 0.25 | Internal advocate, drives momentum |
| Influencer | 0.15 | Shapes technical/operational evaluation |
| End User | 0.10 | Adoption determines long-term success |
| Blocker | 0.10 | Can stall or kill the deal |
| Gatekeeper | 0.05 | Controls access but rarely the decision |

### Support Level Scores

| Support Level | Score |
|---------------|-------|
| Champion (active advocate) | 100 |
| Supporter (positive, passive) | 75 |
| Neutral | 50 |
| Skeptic (has concerns) | 25 |
| Blocker (actively resists) | 0 |

### Consensus Score Calculation

```
For each stakeholder i:
  weighted_score_i = influence_weight[role_i] * support_score[support_level_i]

raw_consensus = sum(weighted_score_i for all stakeholders)

# Penalty for unengaged stakeholders (no discovery call completed)
unengaged_penalty = (count_unengaged / count_total) * 20

# Penalty for active conflict between stakeholders
conflict_penalty = count_conflict_areas * 5  (max 15)

consensus_score = max(0, raw_consensus - unengaged_penalty - conflict_penalty)
```

## Steps

### 1. Pull stakeholder data from Attio

Query all contacts linked to the deal with stakeholder attributes:

```
attio.list_records({
  object: "people",
  filter: { deal_id: "{deal_id}" },
  select: ["name", "title", "stakeholder_role", "stakeholder_sentiment", "stakeholder_support_level", "engagement_level", "last_interaction_date"]
})
```

### 2. Compute the score

Apply the formula above. Use the weights table. If a stakeholder has no `support_level` set, treat them as unengaged and apply the penalty.

Implementation in any scripting language:

```python
weights = {"Economic Buyer": 0.35, "Champion": 0.25, "Influencer": 0.15, "End User": 0.10, "Blocker": 0.10, "Gatekeeper": 0.05}
scores = {"Champion": 100, "Supporter": 75, "Neutral": 50, "Skeptic": 25, "Blocker": 0}

weighted_sum = 0
unengaged = 0
total = len(stakeholders)

for s in stakeholders:
    if s.support_level is None:
        unengaged += 1
        continue
    w = weights.get(s.role, 0.05)
    sc = scores.get(s.support_level, 50)
    weighted_sum += w * sc

unengaged_penalty = (unengaged / total) * 20 if total > 0 else 0
conflict_penalty = min(len(conflict_areas) * 5, 15)
consensus_score = max(0, weighted_sum - unengaged_penalty - conflict_penalty)
```

### 3. Classify the consensus level

| Score Range | Classification | Recommended Action |
|-------------|---------------|-------------------|
| 80-100 | Strong Consensus | Proceed to proposal with confidence |
| 60-79 | Moderate Consensus | Address skeptic concerns before proposing |
| 40-59 | Weak Consensus | Significant discovery gaps; prioritize engagement with unengaged/negative stakeholders |
| 0-39 | No Consensus | Deal at risk; diagnose whether the problem is coverage (haven't talked to key people) or alignment (stakeholders disagree) |

### 4. Store in CRM

Write the consensus score to the deal record in Attio:

```
PATCH https://api.attio.com/v2/objects/deals/records/{deal_id}
{
  "data": {
    "values": {
      "consensus_score": [{"value": {score}}],
      "consensus_level": [{"option": "{classification}"}],
      "consensus_computed_at": [{"value": "{iso_timestamp}"}]
    }
  }
}
```

### 5. Track consensus trajectory

Log each computation as a PostHog event:

```
posthog.capture("consensus_score_computed", {
  "deal_id": "{deal_id}",
  "score": consensus_score,
  "level": classification,
  "stakeholder_count": total,
  "unengaged_count": unengaged,
  "conflict_count": len(conflict_areas)
})
```

Over time, plot the consensus score trajectory per deal. Deals where consensus improves week-over-week have higher close rates than deals where it stalls.

## Via Claude (for edge cases)

When the formula produces ambiguous results (e.g., score is 60 but the Economic Buyer is a Blocker), use Claude for nuanced assessment:

```
POST https://api.anthropic.com/v1/messages
Body: {
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 1024,
  "messages": [{"role": "user", "content": "Given these stakeholder sentiments for a B2B deal:\n{stakeholder_summary}\n\nThe formula-based consensus score is {score}. However, {anomaly_description}.\n\nShould the consensus level be adjusted? Return JSON: {\"adjusted_score\": N, \"adjusted_level\": \"...\", \"reasoning\": \"...\"}"}]
}
```

## Tool Alternatives

| Tool | Method | Notes |
|------|--------|-------|
| Anthropic Claude | API for edge-case adjustment | Best reasoning when formula is ambiguous |
| Gong | Deal intelligence score | Native multi-stakeholder engagement scoring |
| Clari | Revenue intelligence | Predictive consensus from engagement patterns |
| Custom Python | Scripted formula | Fastest, no API cost for standard computation |

## Error Handling

- **Missing Economic Buyer**: If no Economic Buyer is mapped, consensus score is unreliable. Flag the deal as "Economic Buyer Unknown" and cap the maximum consensus score at 60 regardless of other stakeholders.
- **Single-threaded deals**: If only 1 stakeholder is mapped, consensus score is meaningless. Return score = 0 with note "Single-threaded deal — multi-stakeholder discovery required."
- **Stale data**: If any stakeholder's last interaction was >30 days ago, flag their sentiment as potentially stale. Weight stale stakeholders at 50% of their normal influence.
