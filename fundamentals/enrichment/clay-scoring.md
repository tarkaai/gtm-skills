---
name: clay-scoring
description: Build lead scoring formulas in Clay to prioritize outreach
tool: Clay
product: Clay
difficulty: Intermediate
---

# Score Leads in Clay

## Prerequisites
- Clay table with enriched company and contact data
- Defined ICP with weighted criteria

## Steps

1. **Define your scoring dimensions.** Create separate score columns for: Company Fit (firmographics), Contact Fit (title/seniority), and Signal Strength (timing indicators). Each dimension gets a 0-100 score.

2. **Build the Company Fit formula.** Add a formula column that scores based on: Employee Count in ICP range (+30), Industry match (+25), Funding stage match (+20), Technology stack overlap (+15), Geography match (+10). Use Clay's formula syntax with IF/THEN logic.

3. **Build the Contact Fit formula.** Score based on: Title matches buyer persona (+40), Seniority is Director+ (+25), Department match (+20), Tenure at company > 6 months (+15). Subtract points for titles containing "intern" or "assistant" (-50).

4. **Build the Signal Score.** Score timing signals: Recent funding round (+30), Job posting for your category (+25), Technology change detected (+20), Company growth rate >20% (+15), Recent leadership hire (+10).

5. **Create composite score.** Add a Total Score column: (Company Fit * 0.4) + (Contact Fit * 0.3) + (Signal Score * 0.3). This weights company fit highest since it is the hardest to change.

6. **Set priority tiers.** Create a Tier column: Score 80+ = Tier 1 (immediate outreach), 60-79 = Tier 2 (next batch), below 60 = Tier 3 (nurture only). Sort your outreach queue by tier.
