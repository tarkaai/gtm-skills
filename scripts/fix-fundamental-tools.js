#!/usr/bin/env node
/**
 * Fix fundamental tool names: replace compound "Tool1 / Tool2 / ..." with a single primary tool.
 */
const fs = require('fs');
const path = require('path');

const FUNDAMENTALS_DIR = path.join(__dirname, '..', 'fundamentals');

// Explicit overrides for specific tool strings
const TOOL_MAP = {
  // Twitter/X is a single platform name, not a compound - keep as-is
  'Twitter/X Ads': 'X Ads',
  'Twitter/X': 'X',

  // Reddit
  'Reddit Ads / PostHog': 'Reddit Ads',

  // Calling
  'Orum / PhoneBurner / JustCall / Aircall / Kixie': 'Orum',

  // Enrichment / Research
  'Clay / Web Search / LinkedIn API': 'Clay',
  'Clay / Apollo / LinkedIn': 'Clay',
  'PostHog / Attio / Spreadsheet': 'PostHog',
  'PostHog / Attio / n8n': 'PostHog',

  // Community
  'Syften / n8n / Reddit API': 'Syften',
  'n8n / Common Room / Slack API / Discord API': 'Common Room',
  'Reddit API / Web Search': 'Reddit API',

  // AI
  'AI (Claude / GPT)': 'Anthropic',

  // Design
  'Plotly / Chart.js / D3': 'Plotly',
  'Sharp (Node.js) / Pillow (Python)': 'Sharp',

  // Directories / Reviews
  'G2 / Capterra / Product Hunt / Clay / n8n': 'G2',
  'G2 / Capterra / Product Hunt / GetApp / TrustRadius / SourceForge': 'G2',
  'G2 / Capterra / Product Hunt / TrustRadius / n8n': 'G2',

  // Docs
  'Mintlify / GitBook / ReadMe / Docusaurus / Fumadocs': 'Mintlify',
  'Algolia / Mintlify / PostHog': 'Algolia',

  // GitHub
  'GitHub CLI / git': 'GitHub CLI',
  'GitHub CLI / GitHub API': 'GitHub CLI',

  // CRM / Notes
  'Google Docs / Notion / Attio': 'Notion',

  // Influencer
  'SparkToro / Modash / Passionfroot / Clay': 'SparkToro',
  'Instantly / Loops / Passionfroot / LinkedIn': 'Instantly',

  // Intent
  'Bombora / G2 / 6sense / TrustRadius / Demandbase': 'Bombora',
  'RB2B / Leadpipe / Koala / Clearbit Reveal / Leadfeeder': 'RB2B',

  // Media / PR
  'Muck Rack / Prowly / JustReachOut / Anewstip / Hunter Journalists': 'Muck Rack',
  'Mention / Google Alerts / Qwoted / Featured.com / HARO': 'Mention',
  'PR Newswire / Business Wire / GlobeNewsWire / EIN Presswire / Newswire.com': 'PR Newswire',

  // Email
  'Instantly / Gmail / Smartlead': 'Instantly',
  'Instantly / Gmail': 'Instantly',

  // Paid / Newsletter
  'Paved / Swapstack / Sparkloop / Letterhead / direct outreach': 'Paved',
  'Email / CRM': 'Attio',
  'Email / CRM / Anthropic': 'Anthropic',

  // Partner Marketplaces
  'Salesforce AppExchange / HubSpot App Marketplace / Shopify App Store / Slack App Directory / Zapier': 'Salesforce AppExchange',
  'Salesforce AppExchange / HubSpot App Marketplace / Shopify App Store / Slack App Directory / Zapier / Make': 'Salesforce AppExchange',
  'Salesforce AppExchange / HubSpot App Marketplace / Shopify App Store / Slack App Directory / G2': 'Salesforce AppExchange',

  // Partnerships / Affiliates
  'Rewardful / FirstPromoter / PartnerStack / Tapfiliate': 'Rewardful',
  'Rewardful / FirstPromoter / PartnerStack / PayPal / Wise': 'Rewardful',
  'Rewardful / FirstPromoter / PartnerStack / Tapfiliate / Reflio': 'Rewardful',

  // Podcast
  'ListenNotes / Podchaser / Rephonic': 'ListenNotes',
  'Spotify for Podcasters / Buzzsprout / Transistor / RSS Analytics': 'Buzzsprout',
  'Descript / Riverside / Opus Clip / Headliner': 'Descript',
  'Buzzsprout / Transistor / RSS.com / Spotify for Podcasters': 'Buzzsprout',
  'Apple Podcasts Connect / Spotify for Podcasters / Google Podcasts Manager': 'Apple Podcasts Connect',
  'AdvertiseCast / Podcorn / Acast / Podscribe / Gumball / RedCircle': 'AdvertiseCast',

  // Sharing / referral
  'PostHog / Dub.co / Rebrandly / Stripe': 'PostHog',
  'PostHog / Rebrandly / Dub.co': 'PostHog',
  'Vercel OG / @vercel/og': 'Vercel OG',
  'Custom API / Short.io / Dub.co': 'Dub.co',

  // Product
  'Product Database / ORM': 'Product API',
  'Product API / Infrastructure': 'Product API',
  'Product API / Database': 'Product API',
  'Product API / CMS': 'Product API',
  'Product API / PostHog': 'Product API',

  // QA Platforms
  'Stack Exchange API / Quora (scraping) / Dev.to API': 'Stack Exchange API',
  'Stack Exchange API / Dev.to API': 'Stack Exchange API',
  'Stack Exchange API / n8n / SerpAPI': 'Stack Exchange API',

  // SDK / Package managers
  'cargo CLI / crates.io API': 'cargo CLI',
  'git / Go toolchain': 'Go CLI',
  'Maven / Gradle / Sonatype API': 'Maven',
  'npm CLI / npm API': 'npm CLI',
  'dotnet CLI / NuGet API': 'dotnet CLI',
  'twine / PyPI API': 'twine',
  'gem CLI / RubyGems API': 'gem CLI',

  // SEO
  'CLI/API': 'Node.js',

  // SMS
  'Twilio / n8n / Attio': 'Twilio',
  'Twilio / Salesmsg / OpenPhone (Quo)': 'Twilio',
  'Twilio / Salesmsg / OpenPhone (Quo) / SlickText / Heymarket': 'Twilio',

  // Social / LinkedIn
  'Dripify / Expandi / PhantomBuster / Linked Helper / Waalaxy': 'Expandi',
  'lemlist / Expandi / Unipile / La Growth Machine / HeyReach': 'lemlist',

  // Voice
  'ElevenLabs / Play.ht / Resemble.AI / WellSaid / Deepgram': 'ElevenLabs',
  'VoiceDrop.ai / Slybroadcast / Drop Cowboy / PhoneBurner / Kixie': 'VoiceDrop.ai',
};

function processFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');

  // Match frontmatter
  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!fmMatch) return null;

  const frontmatter = fmMatch[1];
  const toolMatch = frontmatter.match(/^tool:\s*(.+)$/m);
  if (!toolMatch) return null;

  const oldTool = toolMatch[1].trim();

  // Check if it contains a slash (compound)
  if (!oldTool.includes('/')) return null;

  // Look up in map
  const newTool = TOOL_MAP[oldTool];
  if (!newTool) {
    console.log(`  WARNING: No mapping for "${oldTool}" in ${path.relative(FUNDAMENTALS_DIR, filePath)}`);
    return null;
  }

  if (oldTool === newTool) return null;

  const newContent = content.replace(`tool: ${oldTool}`, `tool: ${newTool}`);
  fs.writeFileSync(filePath, newContent);
  return { file: path.relative(FUNDAMENTALS_DIR, filePath), from: oldTool, to: newTool };
}

// Walk all .md files
function walkDir(dir) {
  const results = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...walkDir(fullPath));
    } else if (entry.name.endsWith('.md')) {
      results.push(fullPath);
    }
  }
  return results;
}

const files = walkDir(FUNDAMENTALS_DIR);
console.log(`Found ${files.length} fundamental files`);

let changed = 0;
let skipped = 0;
const changes = [];

for (const file of files) {
  const result = processFile(file);
  if (result) {
    changes.push(result);
    changed++;
  }
}

console.log(`\nChanged ${changed} files:`);
for (const c of changes) {
  console.log(`  ${c.file}: "${c.from}" -> "${c.to}"`);
}
console.log(`\nDone.`);
