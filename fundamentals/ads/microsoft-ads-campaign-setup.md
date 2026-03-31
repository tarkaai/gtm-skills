---
name: microsoft-ads-campaign-setup
description: Create and manage Microsoft Advertising (Bing) search campaigns via the Microsoft Advertising API
tool: Microsoft
product: Microsoft Ads
difficulty: Config
---

# Set Up a Microsoft Advertising Search Campaign

## Prerequisites
- Microsoft Advertising account with API access (developer token required)
- OAuth 2.0 credentials configured for the Microsoft Advertising API
- Conversion tracking configured (UET tag installed)

## Steps

1. **Authenticate via OAuth 2.0.** Obtain an access token using the Microsoft identity platform:
   ```
   POST https://login.microsoftonline.com/common/oauth2/v2.0/token
   Content-Type: application/x-www-form-urlencoded

   client_id={app_id}&scope=https://ads.microsoft.com/msads.manage&grant_type=client_credentials&client_secret={secret}
   ```

2. **Create a campaign via the Campaign Management API.** Use the `AddCampaigns` operation:
   ```xml
   <AddCampaignsRequest>
     <AccountId>{account_id}</AccountId>
     <Campaigns>
       <Campaign>
         <Name>Q1 Search - High Intent Keywords</Name>
         <BudgetType>DailyBudgetStandard</BudgetType>
         <DailyBudget>25.00</DailyBudget>
         <TimeZone>EasternTimeUSCanada</TimeZone>
         <CampaignType>Search</CampaignType>
         <BiddingScheme xsi:type="MaxConversionsBiddingScheme"/>
       </Campaign>
     </Campaigns>
   </AddCampaignsRequest>
   ```
   Campaign types: Search (text ads), Shopping, Audience (display), Performance Max.

3. **Set geographic and demographic targeting.** Use `AddCampaignCriterions`:
   ```xml
   <CampaignCriterion xsi:type="BiddableCampaignCriterion">
     <CampaignId>{campaign_id}</CampaignId>
     <Criterion xsi:type="LocationCriterion">
       <LocationId>190</LocationId>  <!-- United States -->
     </Criterion>
   </CampaignCriterion>
   ```

4. **Create ad groups.** Use `AddAdGroups` to organize by keyword theme:
   ```xml
   <AddAdGroupsRequest>
     <CampaignId>{campaign_id}</CampaignId>
     <AdGroups>
       <AdGroup>
         <Name>CRM Software - Exact Match</Name>
         <CpcBid><Amount>2.50</Amount></CpcBid>
       </AdGroup>
     </AdGroups>
   </AddAdGroupsRequest>
   ```

5. **Add keywords.** Use `AddKeywords` with match types:
   ```xml
   <AddKeywordsRequest>
     <AdGroupId>{ad_group_id}</AdGroupId>
     <Keywords>
       <Keyword>
         <Text>best crm for startups</Text>
         <MatchType>Exact</MatchType>
         <Bid><Amount>3.00</Amount></Bid>
       </Keyword>
     </Keywords>
   </AddKeywordsRequest>
   ```
   Match types: Exact, Phrase, Broad. Start with Exact for high-intent terms.

6. **Create Responsive Search Ads.** Use `AddAds`:
   ```xml
   <Ad xsi:type="ResponsiveSearchAd">
     <Headlines>
       <AssetLink><Asset xsi:type="TextAsset"><Text>Best CRM for Startups</Text></Asset></AssetLink>
       <AssetLink><Asset xsi:type="TextAsset"><Text>Close Deals 2x Faster</Text></Asset></AssetLink>
     </Headlines>
     <Descriptions>
       <AssetLink><Asset xsi:type="TextAsset"><Text>Built for founders. Free trial, no credit card.</Text></Asset></AssetLink>
     </Descriptions>
     <FinalUrls><string>https://example.com/demo?utm_source=bing</string></FinalUrls>
   </Ad>
   ```

7. **Add ad extensions.** Use `AddAdExtensions` for sitelinks, callouts, and structured snippets to improve CTR and quality score.

8. **Import from Google Ads (optional).** Microsoft Advertising supports direct Google Ads import via the `GoogleImportJob` API operation. This copies campaigns, ad groups, keywords, and ads from Google to Microsoft with one API call. Use this to quickly mirror a working Google campaign.

9. **Monitor and optimize.** Query performance via the Reporting API (`SubmitGenerateReport`). Track impressions, clicks, conversions, CPC, and quality score. Microsoft Ads CPCs are typically 30-40% lower than Google for the same keywords.

## Error Handling
- `CampaignServiceInvalidBudget`: Budget below minimum ($5/day). Increase daily budget.
- `CampaignServiceDuplicateCampaignName`: Campaign name already exists. Append a date suffix.
- `KeywordServiceInvalidKeywordText`: Keyword contains disallowed characters or exceeds 80 chars. Clean the keyword text.
- Rate limit: 12 calls per second per account. Implement exponential backoff.

## Authentication Notes
Microsoft Advertising API uses OAuth 2.0 via the Microsoft identity platform. Store refresh tokens securely. Tokens expire after 1 hour; use the refresh token flow to obtain new access tokens automatically.
