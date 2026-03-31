---
name: integration-compatibility-assessment
description: Evaluate the technical feasibility and effort required to build a product integration with a partner
tool: Clay
difficulty: Config
---

# Integration Compatibility Assessment

## Prerequisites
- Partner product identified (name, domain, public docs URL)
- Clay account or web search API access for automated research
- Understanding of your own product's API surface (endpoints, webhooks, auth methods)

## Steps

1. **Locate the partner's developer documentation.** Search for `{partner_domain}/docs`, `{partner_domain}/developers`, or `{partner_domain}/api`. Use Clay's Claygent to automate discovery:

   ```
   Clay Claygent prompt:
   "Find the developer documentation or API reference for {partner_domain}.
   Return: docs_url, api_type (REST/GraphQL/webhook/SDK), authentication_method
   (API key/OAuth2/JWT), public_api (yes/no), developer_program_url."
   ```

2. **Assess API availability and maturity.** Check the partner's API for:
   - **Public REST/GraphQL API**: Endpoints documented, versioned, rate limits published
   - **Webhook support**: Can the partner push events to your system (new record created, status changed)?
   - **SDK availability**: Do they publish client libraries (Node, Python, Go)?
   - **Sandbox/test environment**: Can you develop against a free test account?
   - **Rate limits**: What are the request limits per minute/day?

   Score API maturity 1-5:
   - 5: Full REST API + webhooks + SDKs + sandbox + versioned docs
   - 4: REST API + webhooks + docs (no SDK or sandbox)
   - 3: REST API with docs but no webhooks
   - 2: API exists but poorly documented or in beta
   - 1: No public API; integration requires scraping or manual work

3. **Map integration surfaces.** Identify the specific data flows your integration would implement:
   - **Your product -> Partner**: What data would you push? (contacts, events, metrics)
   - **Partner -> Your product**: What data would you pull or receive? (user records, activity, status)
   - **Bidirectional sync**: Does the use case require two-way data flow?
   - **Trigger-based**: Are there events in either product that should trigger actions in the other?

   Document each flow as: `{source_object} -> {action} -> {destination_object}` (e.g., "Attio deal stage change -> webhook -> partner project created").

4. **Estimate development effort.** Classify the integration:
   - **Light (1-2 days)**: Webhook listener + single API call. Example: send a Slack notification when a deal closes.
   - **Medium (1-2 weeks)**: Bidirectional sync with auth flow. Example: sync contacts between CRM and email platform.
   - **Heavy (2-4 weeks)**: Deep product integration with UI components. Example: embed partner features inside your product.
   - **Native marketplace (4-8 weeks)**: Build and publish to the partner's app marketplace (e.g., HubSpot App Marketplace, Salesforce AppExchange).

5. **Check for existing connectors.** Before building from scratch, check:
   - **n8n**: Does n8n have a built-in node for this partner? Search `https://n8n.io/integrations/`
   - **Zapier/Make**: Existing connectors you could leverage for an MVP
   - **Tray.io / Workato**: Enterprise integration platforms with pre-built connectors
   - **Partner's marketplace**: Do they already have a connector for your product category?

   If an existing connector covers >80% of the use case, use it for the Smoke/Baseline levels and build native only at Scalable.

6. **Record the assessment.** Store in your CRM (Attio) on the partner company record:
   - `api_maturity_score`: Number (1-5)
   - `integration_type`: Light / Medium / Heavy / Native Marketplace
   - `estimated_dev_days`: Number
   - `docs_url`: URL to partner API docs
   - `existing_connector`: Yes/No (and platform name if yes)
   - `integration_surfaces`: Text describing the data flows
   - `blockers`: Any technical blockers identified

## Error Handling
- If no public API found, check if the partner has a Zapier/Make integration (indirect API access)
- If API is in beta, contact the partner's developer relations team for access
- If authentication requires OAuth2, factor in extra setup time for the auth flow

## Alternative Tools
- **Postman**: Test partner API endpoints interactively before committing to build
- **RapidAPI**: Check if the partner's API is listed for quick testing
- **BuiltWith / Wappalyzer**: Detect the partner's tech stack to infer API capabilities
- **Apollo / Clearbit**: Enrich the partner company to find the right developer relations contact
- **GitHub**: Search for community-built SDKs or integration examples
