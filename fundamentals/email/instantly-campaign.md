---
name: instantly-campaign
description: Create and launch cold email campaigns in Instantly
tool: Instantly
difficulty: Intermediate
---

# Create a Campaign in Instantly

## Prerequisites
- Instantly account with connected, warmed sending accounts (see `fundamentals/email/instantly-account-setup`)
- Verified prospect list (see `fundamentals/enrichment/clay-email-verification`)

## Steps

1. **Create a new campaign.** In Instantly, go to Campaigns > New Campaign. Name it with context: "[Date] [Audience] [Angle]" (e.g., "Mar24 Series-A CTOs Pain-Point"). This naming convention helps you compare performance across campaigns.

2. **Upload your lead list.** Import your verified CSV with required columns: email, first_name, last_name, company_name. Add custom columns for personalization (e.g., recent_news, tech_stack, pain_point). Map columns during import.

3. **Write your email sequence.** Add 3-4 steps. Step 1 (day 0): Short, personalized opener referencing something specific about the prospect. Step 2 (day 3): Different angle, lead with value. Step 3 (day 7): Social proof or case study. Step 4 (day 14): Soft breakup. Keep each under 100 words. Use {{firstName}} and custom variables for personalization.

4. **Assign sending accounts.** Select 2-3 warmed sending accounts for the campaign. Instantly will rotate between them automatically, distributing volume evenly.

5. **Configure schedule.** Set sending window to weekdays, 8am-11am in the recipient's timezone. Set daily limits per account and overall campaign daily limit. Start with 20 sends per day total and ramp up after 3 days.

6. **Launch and monitor.** Activate the campaign. Check deliverability stats after the first 50 sends. Open rate below 40% suggests deliverability issues. Reply rate below 2% suggests messaging issues.
