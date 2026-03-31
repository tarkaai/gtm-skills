---
name: microsoft-ads-conversion-tracking
description: Set up Universal Event Tracking (UET) and conversion goals for Microsoft Advertising campaigns
tool: Microsoft Advertising
difficulty: Config
---

# Set Up Microsoft Ads Conversion Tracking (UET)

## Prerequisites
- Microsoft Advertising account with API access
- Access to your website codebase or tag manager

## Steps

1. **Create a UET tag via API.** Use the Campaign Management API `AddUetTags` operation:
   ```xml
   <AddUetTagsRequest>
     <UetTags>
       <UetTag>
         <Name>Main Website UET Tag</Name>
         <Description>Tracks all website conversions</Description>
       </UetTag>
     </UetTags>
   </AddUetTagsRequest>
   ```
   The response returns a `TagId` and the JavaScript tracking snippet.

2. **Install the UET tag on all pages.** Add the returned JavaScript snippet to every page, or install via Google Tag Manager using the Microsoft Advertising tag template. The tag fires a page view event on every page load.

3. **Create conversion goals.** Use `AddConversionGoals` to define what counts as a conversion:
   ```xml
   <AddConversionGoalsRequest>
     <ConversionGoals>
       <ConversionGoal xsi:type="UrlGoal">
         <Name>Demo Request</Name>
         <ConversionWindowInMinutes>43200</ConversionWindowInMinutes> <!-- 30 days -->
         <CountType>Unique</CountType>
         <Revenue>
           <Type>FixedValue</Type>
           <Value>200</Value>
           <CurrencyCode>USD</CurrencyCode>
         </Revenue>
         <TagId>{uet_tag_id}</TagId>
         <UrlExpression>
           <Operator>Contains</Operator>
           <Value>/thank-you</Value>
         </UrlExpression>
       </ConversionGoal>
     </ConversionGoals>
   </AddConversionGoalsRequest>
   ```
   Goal types: UrlGoal (thank-you page), EventGoal (custom events), DurationGoal, PagesViewedPerVisitGoal.

4. **Set up event-based goals for form submissions.** Fire custom UET events from your form handler:
   ```javascript
   window.uetq = window.uetq || [];
   window.uetq.push('event', 'form_submit', {
     'event_category': 'lead',
     'event_label': 'demo_request',
     'event_value': 200
   });
   ```
   Then create an EventGoal in the API matching this event name.

5. **Verify conversion tracking.** Use the UET Tag Helper browser extension to confirm the tag fires correctly. Check the `ConversionGoalStatus` via API -- status should move from `NoRecentConversions` to `RecordingConversions` within 24 hours of the first conversion.

6. **Enable Enhanced Conversions (optional).** For server-side tracking, use the Microsoft Advertising Conversions API (CAPI) to send conversion events directly from your server, bypassing ad blockers:
   ```
   POST https://bat.bing.com/api/conversions
   {
     "conversions": [{
       "conversion_goal_id": "{goal_id}",
       "conversion_time": "2026-03-30T10:00:00Z",
       "conversion_value": 200,
       "hashed_email": "{sha256_hash}"
     }]
   }
   ```

## Error Handling
- `UetTagNotVerified`: Tag not detected on site. Verify installation and check for ad blockers during testing.
- `ConversionGoalNoRecentConversions`: No conversions recorded. Confirm the URL pattern or event name matches exactly.
