---
name: bundle-pricing-model
description: Generate bundle pricing structures that create joint value for both partners and their shared customers
tool: Anthropic
difficulty: Setup
---

# Bundle Pricing Model

Generate pricing structures for product bundles between two complementary SaaS tools. The model outputs discount tiers, revenue-split proposals, and a pricing page template that both partners can embed.

## Prerequisites

- Anthropic API key for Claude
- Your product's current pricing tiers and ARPU
- Partner product's current pricing tiers (or best estimate from their pricing page)
- Agreed-upon bundle scope (which plans are included, any feature exclusions)

## Steps

1. **Gather pricing inputs.** Collect before generating:
   - Your product pricing URL, plan names, and monthly/annual prices
   - Partner product pricing URL, plan names, and monthly/annual prices
   - Combined value proposition: what does the customer get from using both tools together?
   - Target discount range: typical SaaS bundles offer 15-30% off combined list price
   - Revenue split preference: 50/50, proportional to list price, or custom
   - Billing model: single invoice (one partner collects and remits) or dual invoice (each bills their portion)

2. **Generate the bundle pricing model using Claude.** Call the Anthropic API:

   ```
   POST https://api.anthropic.com/v1/messages
   Authorization: Bearer {ANTHROPIC_API_KEY}
   Content-Type: application/json

   {
     "model": "claude-sonnet-4-20250514",
     "max_tokens": 2048,
     "messages": [{
       "role": "user",
       "content": "Design a SaaS bundle pricing model for two complementary products.\n\nProduct A: {your_product_name}\n- Plans: {plan_names_and_prices}\n- ARPU: {arpu}\n\nProduct B: {partner_product_name}\n- Plans: {plan_names_and_prices}\n- Estimated ARPU: {partner_arpu}\n\nCombined value prop: {value_prop}\n\nRules:\n- Generate 3 bundle tiers (Starter, Growth, Scale) mapping to logical plan combinations\n- Discount range: 15-30% off combined list price, increasing with commitment\n- Monthly and annual pricing for each tier (annual gets extra 10-20% off)\n- Revenue split proposal with rationale\n- One-line positioning statement per tier\n- Show the customer's savings vs buying separately\n- Include a free trial or money-back guarantee recommendation\n\nOutput as structured JSON with fields: tiers[{name, your_plan, partner_plan, combined_list_price, bundle_price_monthly, bundle_price_annual, discount_pct, savings_monthly, positioning}], revenue_split: {model, your_pct, partner_pct, rationale}, trial_recommendation, billing_recommendation."
     }]
   }
   ```

3. **Validate the pricing model.** Before presenting to the partner:
   - Verify no tier prices your product below your cost floor
   - Verify the partner's share is attractive enough for them to promote (>40% of bundle revenue unless your product is the anchor)
   - Check that tier progression is logical (each tier adds clear value over the previous)
   - Ensure annual pricing creates genuine incentive (at least 15% cheaper than 12x monthly)
   - Confirm the discount is meaningful to customers (>15%) but sustainable for both companies

4. **Generate the pricing page copy.** Request a co-branded pricing comparison table showing: buying separately vs. buying the bundle, with savings highlighted per tier. This becomes the landing page content for the bundle deal.

## Error Handling

- If Claude generates unrealistic discounts (>40%), constrain the prompt with your minimum acceptable price per plan
- If the partner has usage-based pricing, model the bundle on typical usage at each tier rather than list price
- If revenue split negotiation stalls, propose a 90-day trial split with renegotiation based on actual attribution data

## Alternative Tools

- **OpenAI GPT-4o**: Alternative LLM for pricing model generation
- **PriceIntelligently (Paddle)**: SaaS pricing research and optimization
- **Stigg**: Pricing and packaging infrastructure for SaaS
- **Stripe Pricing Tables**: Embed bundle pricing directly in landing pages
- **Chargebee**: Subscription billing with bundle/add-on support
