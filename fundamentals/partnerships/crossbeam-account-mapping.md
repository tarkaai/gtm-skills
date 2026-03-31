---
name: crossbeam-account-mapping
description: Use Crossbeam to find overlapping accounts between your CRM and a partner's CRM
tool: Crossbeam
difficulty: Config
---

# Crossbeam Account Mapping

## Prerequisites
- Crossbeam account (Free tier available at https://www.crossbeam.com/pricing)
- CRM connected to Crossbeam (Attio, HubSpot, Salesforce, Pipedrive, or Clarify)
- At least one partner connected on Crossbeam

## Steps

1. **Connect your CRM to Crossbeam.** In the Crossbeam dashboard, go to Integrations and connect your CRM. Crossbeam supports HubSpot, Salesforce, Pipedrive, and custom CRM integrations via CSV upload or API. For Attio, use the CSV export from Attio (export Companies collection) and upload to Crossbeam, or use Crossbeam's REST API to push account data programmatically.

   ```
   POST https://api.crossbeam.com/v1/populations
   Authorization: Bearer {CROSSBEAM_API_KEY}
   Content-Type: application/json

   {
     "name": "All Customers",
     "source": "csv",
     "filters": []
   }
   ```

2. **Create populations.** Populations are segments of your accounts. Create at minimum: "Customers" (closed-won deals), "Open Pipeline" (active deals), and "Target Accounts" (prospects you want to reach). Each population maps to a CRM filter or uploaded list.

   ```
   POST https://api.crossbeam.com/v1/populations
   {
     "name": "Target Accounts",
     "description": "ICP-qualified prospects for partner co-marketing",
     "source": "manual"
   }
   ```

3. **Invite a partner or accept an invitation.** Search the Crossbeam Network (30,000+ companies) for your partner. Send a partnership request. Once accepted, you can define sharing rules — what data you share and what you receive.

4. **Configure sharing rules.** Set overlap sharing to show account names and domains where both you and your partner have matching accounts. Never share deal values or contact details without explicit agreement. Start with company name + domain only.

5. **Run the overlap report.** Query the Crossbeam API for overlapping accounts between your populations and your partner's:

   ```
   GET https://api.crossbeam.com/v1/reports/overlaps?partner_id={PARTNER_ID}&population_id={YOUR_POPULATION_ID}
   Authorization: Bearer {CROSSBEAM_API_KEY}
   ```

   Response includes: overlapping account names, domains, and which of your populations they appear in.

6. **Export overlaps for action.** Download the overlap report as CSV or push it to your CRM via the API. Tag overlapping accounts in Attio with the partner name and overlap type (e.g., "Partner: Acme — Overlap: Their Customer + Our Prospect"). This data feeds the `partner-prospect-research` drill to prioritize which partners have the most valuable audience overlap.

## Error Handling
- If CRM sync fails, check API credentials and field mappings in Crossbeam settings
- If no overlaps found, verify your populations are populated (minimum 50 accounts recommended)
- Rate limit: Crossbeam API allows 100 requests/minute; batch large queries

## Alternative Tools
- **Reveal (formerly Crossbeam competitor)**: Similar account mapping, merged with Crossbeam in 2024
- **PartnerTap**: Enterprise-focused account mapping
- **Partnered.com**: Lightweight partner overlap tool
- **Manual CSV exchange**: For partners not on any platform, exchange anonymized domain lists and match locally
