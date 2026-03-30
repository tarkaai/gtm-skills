#!/usr/bin/env node
/**
 * export.js — Generates gtm-skills skill files from Tarka's plays.json
 *
 * Usage (from gtm-skills root):
 *   node scripts/export.js --plays <path-to-plays.json> --out .
 *
 * What it does:
 *   1. Reads plays.json
 *   2. Applies per-motion budget rules (play-specific tool costs only, not CRM/automation)
 *   3. Generates one skill .md file per play × level
 *   4. Outputs updated plays.json with corrected budget fields
 */

'use strict';

const fs = require('fs');
const path = require('path');

// ── CLI args ────────────────────────────────────────────────────────────────
const args = Object.fromEntries(
  process.argv.slice(2).reduce((acc, a, i, arr) => {
    if (a.startsWith('--')) acc.push([a.slice(2), arr[i + 1] || true]);
    return acc;
  }, [])
);

const PLAYS_PATH = args.plays || path.resolve(__dirname, '../plays.json');
const OUT_DIR = args.out || path.resolve(__dirname, '..');
const UPDATE_JSON = args['update-json'] !== 'false';

if (!fs.existsSync(PLAYS_PATH)) {
  console.error(`Cannot find plays.json at: ${PLAYS_PATH}`);
  console.error('Pass --plays <path> to specify the location.');
  process.exit(1);
}

const plays = JSON.parse(fs.readFileSync(PLAYS_PATH, 'utf8'));
console.log(`Loaded ${plays.length} plays from ${PLAYS_PATH}`);

// ── Directory mappings ───────────────────────────────────────────────────────
const stageToDir = { Marketing: 'marketing', Sales: 'sales', Product: 'product' };
const stageSubToDir = {
  Unaware: 'unaware',
  ProblemAware: 'problem-aware',
  SolutionAware: 'solution-aware',
  ProductAware: 'product-aware',
  Qualified: 'qualified',
  Connected: 'connected',
  Aligned: 'aligned',
  Proposed: 'proposed',
  Won: 'won',
  Onboard: 'onboard',
  Retain: 'retain',
  Upsell: 'upsell',
  Referrals: 'referrals',
  Winback: 'winback',
};

const stageSubLabel = {
  Unaware: 'Unaware',
  ProblemAware: 'Problem Aware',
  SolutionAware: 'Solution Aware',
  ProductAware: 'Product Aware',
  Qualified: 'Qualified',
  Connected: 'Connected',
  Aligned: 'Aligned',
  Proposed: 'Proposed',
  Won: 'Won',
  Onboard: 'Onboard',
  Retain: 'Retain',
  Upsell: 'Upsell',
  Referrals: 'Referrals',
  Winback: 'Winback',
};
const levelToFile = { Smoke: 'smoke', Baseline: 'baseline', Scalable: 'scalable', Durable: 'durable' };
const levelLabel = { Smoke: 'Smoke Test', Baseline: 'Baseline Run', Scalable: 'Scalable Automation', Durable: 'Durable Intelligence' };

// ── Motion/channel labels ────────────────────────────────────────────────────
const motionLabel = {
  OutboundFounderLed: 'Outbound Founder-Led',
  FounderSocialContent: 'Founder Social Content',
  CommunitiesForums: 'Communities & Forums',
  LightweightPaid: 'Lightweight Paid',
  MicroEvents: 'Micro Events',
  PartnershipsWarmIntros: 'Partnerships & Warm Intros',
  PREarnedMentions: 'PR & Earned Mentions',
  DirectoriesMarketplaces: 'Directories & Marketplaces',
  LeadCaptureSurface: 'Lead Capture Surface',
};

// ── Budget rules ─────────────────────────────────────────────────────────────
//
// Philosophy:
//   - Show ONLY play-specific tool costs (not CRM, n8n, PostHog standard stack)
//   - Smoke = free or near-free (validate before spending)
//   - Budget strings match format: itemized list joined with " + ", then total
//   - PostHog free tier covers most analytics needs at all levels
//
// Returns { budgetString, budgetItems } per level

function getBudgetRules(motion, channels) {
  const hasEmail = channels.includes('Email');
  const hasSocial = channels.includes('Social');
  const hasDirect = channels.includes('Direct');
  const hasPaid = channels.includes('Paid');
  const hasEvents = channels.includes('Events');
  const hasProduct = channels.includes('Product');
  const hasContent = channels.includes('Content');
  const hasWebsite = channels.includes('Website');
  const hasCommunities = channels.includes('Communities');

  // Each entry: { item, cost } where cost is a string
  const rules = {
    Smoke: { items: [], total: 'Free' },
    Baseline: { items: [], total: 'Free' },
    Scalable: { items: [], total: 'Free' },
    Durable: { items: [], total: 'Free' },
  };

  switch (motion) {

    case 'OutboundFounderLed': {
      // Email outreach
      if (hasEmail) {
        rules.Baseline.items.push(
          { item: 'Instantly or Smartlead (email sequencing)', cost: '~$40–100/mo' },
          { item: 'Clay or Apollo (list building + enrichment)', cost: '~$50–150/mo' },
        );
        rules.Scalable.items.push(
          { item: 'Instantly or Smartlead (email sequencing, scaled)', cost: '~$100–200/mo' },
          { item: 'Clay (enrichment + AI personalization)', cost: '~$150–400/mo' },
          { item: 'LinkedIn Sales Navigator (prospecting, optional)', cost: '~$100/mo' },
        );
        rules.Durable.items.push(
          { item: 'Instantly or Smartlead (email sequencing)', cost: '~$100–200/mo' },
          { item: 'Clay (enrichment + continuous list refresh)', cost: '~$200–500/mo' },
          { item: 'LinkedIn Sales Navigator', cost: '~$100/mo' },
        );
      }
      // LinkedIn / social outreach
      if (hasSocial && !hasEmail) {
        rules.Baseline.items.push(
          { item: 'LinkedIn Sales Navigator', cost: '~$100/mo' },
        );
        rules.Scalable.items.push(
          { item: 'LinkedIn Sales Navigator', cost: '~$100/mo' },
          { item: 'Dripify or Expandi (LinkedIn automation)', cost: '~$60–100/mo' },
        );
        rules.Durable.items.push(
          { item: 'LinkedIn Sales Navigator', cost: '~$100/mo' },
          { item: 'Dripify or Expandi (LinkedIn automation)', cost: '~$60–100/mo' },
          { item: 'Clay (enrichment + AI-personalized messages)', cost: '~$100–300/mo' },
        );
      }
      // Mixed: email + social + direct (typical Sales stage outbound)
      if (hasEmail && hasSocial) {
        rules.Baseline.items.push(
          { item: 'LinkedIn Sales Navigator', cost: '~$100/mo' },
        );
        rules.Scalable.items.push(
          { item: 'LinkedIn Sales Navigator', cost: '~$100/mo' },
          { item: 'Dripify or Expandi (LinkedIn sequences)', cost: '~$60–100/mo' },
        );
        rules.Durable.items.push(
          { item: 'LinkedIn Sales Navigator', cost: '~$100/mo' },
          { item: 'Dripify or Expandi (LinkedIn automation)', cost: '~$60–100/mo' },
        );
      }
      // Calling / direct
      if (hasDirect && !hasEmail && !hasSocial) {
        rules.Baseline.items.push(
          { item: 'Apollo (includes dialer) or Aircall', cost: '~$50–100/mo' },
        );
        rules.Scalable.items.push(
          { item: 'Apollo or Aircall (calling at volume)', cost: '~$100–200/mo' },
        );
        rules.Durable.items.push(
          { item: 'Apollo or Aircall (AI-assisted calling)', cost: '~$100–300/mo' },
        );
      }
      // Product-led outreach (PLS / in-app triggers)
      if (hasProduct && !hasEmail) {
        rules.Baseline.items.push(
          { item: 'Intercom or Loops (in-app/email triggers)', cost: '~$75–150/mo' },
        );
        rules.Scalable.items.push(
          { item: 'Intercom or Loops (automated sequences)', cost: '~$100–300/mo' },
        );
        rules.Durable.items.push(
          { item: 'Intercom or Loops (agent-driven messaging)', cost: '~$150–400/mo' },
        );
      }
      break;
    }

    case 'FounderSocialContent': {
      // Minimal unique tooling — free to start
      rules.Baseline.items.push(
        { item: 'Taplio (LinkedIn analytics + scheduling)', cost: '~$50/mo' },
      );
      rules.Scalable.items.push(
        { item: 'Taplio (LinkedIn scheduling + AI assist)', cost: '~$50/mo' },
        { item: 'Buffer or Typefully (cross-platform scheduling)', cost: '~$10–20/mo' },
      );
      rules.Durable.items.push(
        { item: 'Taplio (analytics + AI content engine)', cost: '~$50/mo' },
        { item: 'Buffer or Typefully', cost: '~$10–20/mo' },
        { item: 'Descript or Loom (repurposing content to video)', cost: '~$15–30/mo' },
      );
      if (hasContent || hasEvents) {
        rules.Scalable.items.push(
          { item: 'Descript or Riverside (video/podcast production)', cost: '~$25–50/mo' },
        );
      }
      break;
    }

    case 'CommunitiesForums': {
      // Almost entirely free — time is the cost
      rules.Scalable.items.push(
        { item: 'Premium community memberships (Slack groups, paid newsletters)', cost: '~$50–200/mo' },
      );
      rules.Durable.items.push(
        { item: 'Community management tool (Common Room or Orbit)', cost: '~$50–200/mo' },
        { item: 'Premium community memberships', cost: '~$50–200/mo' },
      );
      break;
    }

    case 'LightweightPaid': {
      // Ad spend is the dominant cost
      rules.Smoke.items.push(
        { item: 'Ad spend (LinkedIn, Google, or Meta)', cost: '$300–1,000 test budget' },
      );
      rules.Smoke.total = '$300–1,000 ad spend';
      rules.Baseline.items.push(
        { item: 'Ad spend', cost: '$1,000–3,000/mo' },
        { item: 'Landing page tool (Webflow or Carrd, if needed)', cost: '~$15–40/mo' },
      );
      rules.Scalable.items.push(
        { item: 'Ad spend', cost: '$3,000–10,000/mo' },
        { item: 'Landing page tool', cost: '~$15–40/mo' },
      );
      if (hasSocial) {
        rules.Scalable.items.push(
          { item: 'LinkedIn Campaign Manager (included with ad spend — no extra fee)', cost: 'Free' },
        );
      }
      rules.Durable.items.push(
        { item: 'Ad spend (agent-optimized across channels)', cost: '$5,000–20,000/mo' },
      );
      break;
    }

    case 'MicroEvents': {
      rules.Smoke.items.push(
        { item: 'Webinar platform — Zoom free tier or Google Meet', cost: 'Free' },
        { item: 'Cal.com (scheduling, optional)', cost: 'Free' },
      );
      rules.Baseline.items.push(
        { item: 'Riverside (webinar + recording)', cost: '~$25/mo' },
        { item: 'Event promotion (LinkedIn posts, email invite)', cost: 'Free' },
      );
      rules.Scalable.items.push(
        { item: 'Riverside or Hopin (production-quality events)', cost: '~$25–150/mo' },
        { item: 'Event promotion spend (LinkedIn, email list)', cost: '~$100–500/mo' },
        { item: 'Loom (post-event follow-up clips)', cost: '~$15/mo' },
      );
      rules.Durable.items.push(
        { item: 'Riverside or Hopin', cost: '~$25–150/mo' },
        { item: 'Promotion spend', cost: '~$200–1,000/mo' },
        { item: 'Descript (AI-powered content repurposing)', cost: '~$30/mo' },
      );
      break;
    }

    case 'PartnershipsWarmIntros': {
      // Mostly relationship/time cost — very low unique tooling
      rules.Scalable.items.push(
        { item: 'Crossbeam (partner account mapping)', cost: 'Free tier available; ~$0–200/mo' },
      );
      rules.Durable.items.push(
        { item: 'Crossbeam or PartnerStack (partner program management)', cost: '~$200–500/mo' },
      );
      break;
    }

    case 'PREarnedMentions': {
      rules.Baseline.items.push(
        { item: 'Qwoted or HARO (journalist/podcast request monitoring)', cost: 'Free–$50/mo' },
      );
      rules.Scalable.items.push(
        { item: 'Featured.com (expert quote placements)', cost: '~$100/mo' },
        { item: 'Qwoted Pro', cost: '~$50/mo' },
      );
      rules.Durable.items.push(
        { item: 'Featured.com + Qwoted', cost: '~$150/mo' },
        { item: 'PR Newswire (occasional press release distribution)', cost: '~$300–1,000 per release' },
      );
      break;
    }

    case 'DirectoriesMarketplaces': {
      // Most listings have free tiers
      rules.Baseline.items.push(
        { item: 'G2, Capterra, Product Hunt — free listings', cost: 'Free' },
      );
      rules.Scalable.items.push(
        { item: 'G2 or Capterra review generation campaign', cost: '~$500–2,000/mo (sponsored)' },
        { item: 'Review incentive budget (gift cards, credits)', cost: '~$100–500' },
      );
      rules.Durable.items.push(
        { item: 'G2 or Capterra sponsored listings', cost: '~$1,000–3,000/mo' },
        { item: 'Reputation management tool (optional)', cost: '~$100–300/mo' },
      );
      break;
    }

    case 'LeadCaptureSurface': {
      if (hasProduct || hasEmail) {
        // Product/onboarding plays
        rules.Baseline.items.push(
          { item: 'Tally or Typeform (surveys + forms)', cost: 'Free–$25/mo' },
          { item: 'Loom (async video for onboarding/CSM)', cost: 'Free–$15/mo' },
        );
        rules.Scalable.items.push(
          { item: 'Intercom (in-app messaging + email sequences)', cost: '~$75–300/mo' },
          { item: 'Loom or Descript (video content at scale)', cost: '~$15–30/mo' },
          { item: 'Typeform (in-app surveys + NPS)', cost: '~$25/mo' },
        );
        rules.Durable.items.push(
          { item: 'Intercom (agent-triggered messaging, health-based)', cost: '~$150–500/mo' },
          { item: 'Typeform (automated NPS + CSAT loops)', cost: '~$25/mo' },
          { item: 'Descript (AI-powered video repurposing)', cost: '~$30/mo' },
        );
      } else if (hasWebsite || hasContent) {
        // Website/landing page capture
        rules.Baseline.items.push(
          { item: 'Tally (free form builder)', cost: 'Free' },
        );
        rules.Scalable.items.push(
          { item: 'Webflow (landing page optimization)', cost: '~$15–40/mo' },
          { item: 'Hotjar (session recording + heatmaps)', cost: '~$30/mo' },
        );
        rules.Durable.items.push(
          { item: 'Webflow', cost: '~$15–40/mo' },
          { item: 'Hotjar or FullStory', cost: '~$30–100/mo' },
        );
      } else {
        rules.Baseline.items.push(
          { item: 'Tally or Typeform (lead capture forms)', cost: 'Free–$25/mo' },
        );
        rules.Scalable.items.push(
          { item: 'Typeform (multi-step forms + logic)', cost: '~$25/mo' },
        );
        rules.Durable.items.push(
          { item: 'Typeform (AI-adapted qualification flows)', cost: '~$25/mo' },
        );
      }
      break;
    }

    default:
      break;
  }

  // Compute total strings — combine numeric ranges into a single range
  for (const lvl of ['Smoke', 'Baseline', 'Scalable', 'Durable']) {
    const r = rules[lvl];
    if (r.items.length === 0) {
      r.total = 'Free';
    } else if (!r.total || r.total === 'Free') {
      const costs = r.items.map(i => i.cost).filter(c => c !== 'Free');
      if (costs.length === 0) {
        r.total = 'Free';
      } else if (costs.length === 1) {
        r.total = costs[0];
      } else {
        // Try to combine ranges: extract all numbers, sum lows and highs
        let allNums = [];
        let hasMo = false;
        let hasSpend = costs.some(c => c.includes('spend') || c.includes('budget'));
        costs.forEach(c => {
          const nums = c.match(/\d[\d,]*/g);
          if (nums) allNums.push(...nums.map(n => parseInt(n.replace(',', ''), 10)));
          if (c.includes('/mo')) hasMo = true;
        });
        if (allNums.length >= 2 && !hasSpend) {
          allNums.sort((a, b) => a - b);
          const lo = allNums[0];
          const hi = allNums[allNums.length - 1];
          const suffix = hasMo ? '/mo' : '';
          r.total = `~$${lo}–${hi}${suffix}`;
        } else {
          r.total = costs.join(' + ');
        }
      }
    }
  }

  return rules;
}

// ── Skill file generator ─────────────────────────────────────────────────────

function formatBudgetSection(items, total) {
  if (items.length === 0) {
    return `**Play-specific cost:** Free\n\n_Your CRM, PostHog, and automation platform are not included — standard stack paid once._`;
  }
  const lines = items.map(i => `- **${i.item}:** ${i.cost}`).join('\n');
  return `**Play-specific tools & costs**\n${lines}\n\n_Total play-specific: ${total}_\n\n_Your CRM, PostHog, and automation platform are not included — standard stack paid once._`;
}

function stepsFromInstructions(instructions) {
  // Already formatted as "1. ...\n\n2. ..." — return as-is
  return instructions;
}

function generateSkillFile(play, levelKey, budgetRules) {
  const level = play.levels[levelKey];
  const budget = budgetRules[levelKey];
  const fileName = levelToFile[levelKey];
  const motionStr = motionLabel[play.motion] || play.motion;
  const channelsStr = play.channels.join(', ');
  const stageDir = stageToDir[play.stage];
  const subStageDir = stageSubToDir[play.stageSub];
  const subStageDisplay = stageSubLabel[play.stageSub] || play.stageSub;

  const frontmatter = [
    '---',
    `name: ${play.slug}-${fileName}`,
    `description: >`,
    `  ${play.title} — ${levelLabel[levelKey]}. ${play.summary.split('.')[0]}.`,
    `stage: "${play.stage} > ${subStageDisplay}"`,
    `motion: "${motionStr}"`,
    `channels: "${channelsStr}"`,
    `level: "${levelLabel[levelKey]}"`,
    `time: "${level.time}"`,
    `outcome: "${level.outcome}"`,
    `kpis: [${level.kpis.map(k => `"${k}"`).join(', ')}]`,
    `slug: "${play.slug}"`,
    `install: "npx gtm-skills add ${stageDir}/${subStageDir}/${play.slug}"`,
    '---',
  ].join('\n');

  const toolList = level.recommendedTools && level.recommendedTools.length > 0
    ? level.recommendedTools.map(t => `- **${t.name}** (${t.category})`).join('\n')
    : '_No specialized tools required at this level._';

  const body = `
# ${play.title} — ${levelLabel[levelKey]}

> **Stage:** ${play.stage} → ${subStageDisplay} | **Motion:** ${motionStr} | **Channels:** ${channelsStr}

## Overview
${play.summary}

**Time commitment:** ${level.time}
**Pass threshold:** ${level.outcome}

---

## Budget

${formatBudgetSection(budget.items, budget.total)}

---

## Recommended tools
${toolList}

---

## Instructions

${stepsFromInstructions(level.instructions)}

---

## KPIs to track
${level.kpis.map(k => `- ${k}`).join('\n')}

---

## Pass threshold
**${level.outcome}**

${levelKey !== 'Durable' ? `If you hit this threshold → move to the **${getNextLevel(levelKey)}** skill.\nIf not → iterate on ICP, offer, or channel and re-run this level.` : 'This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run.'}

---

## How to run this skill

1. Ensure your stack is configured: \`cat ~/.gtm-config.json\` (or run \`npx gtm-skills init\`)
2. Your CRM (\`{{crm}}\`) and automation platform (\`{{automation}}\`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: \`npx gtm-skills add ${stageDir}/${subStageDir}/${play.slug}\`_
`.trimStart();

  return { content: frontmatter + '\n' + body, budgetString: budget.total };
}

function getNextLevel(levelKey) {
  const order = ['Smoke', 'Baseline', 'Scalable', 'Durable'];
  const idx = order.indexOf(levelKey);
  return idx < order.length - 1 ? levelLabel[order[idx + 1]] : null;
}

// ── Budget string for JSON update ────────────────────────────────────────────
// Returns a clean string suitable for the "budget" field in plays.json

function budgetToString(budgetRules, levelKey) {
  const b = budgetRules[levelKey];
  if (b.items.length === 0) return 'Free';
  // Summarize: list tools with costs
  return b.items.map(i => `${i.item}: ${i.cost}`).join('; ');
}

// ── Main export loop ─────────────────────────────────────────────────────────

let skillCount = 0;
let updatedBudgets = 0;
const updatedPlays = [];

for (const play of plays) {
  const stageDir = stageToDir[play.stage];
  const subStageDir = stageSubToDir[play.stageSub];

  if (!stageDir || !subStageDir) {
    console.warn(`Unknown stage/stageSub for play: ${play.slug} (${play.stage}/${play.stageSub})`);
    continue;
  }

  const budgetRules = getBudgetRules(play.motion, play.channels);
  const playDir = path.join(OUT_DIR, 'skills', stageDir, subStageDir, play.slug);
  fs.mkdirSync(playDir, { recursive: true });

  const updatedPlay = { ...play, levels: {} };

  for (const levelKey of ['Smoke', 'Baseline', 'Scalable', 'Durable']) {
    const { content, budgetString } = generateSkillFile(play, levelKey, budgetRules);
    const filePath = path.join(playDir, `${levelToFile[levelKey]}.md`);
    fs.writeFileSync(filePath, content);
    skillCount++;

    // Build updated level with corrected budget
    const newBudget = budgetToString(budgetRules, levelKey);
    const oldBudget = play.levels[levelKey].budget;
    if (oldBudget !== newBudget) updatedBudgets++;

    updatedPlay.levels[levelKey] = {
      ...play.levels[levelKey],
      budget: newBudget,
    };
  }

  updatedPlays.push(updatedPlay);
}

console.log(`Generated ${skillCount} skill files in ${path.join(OUT_DIR, 'skills')}/`);
console.log(`Budget fields updated: ${updatedBudgets} / ${plays.length * 4}`);

// ── Write updated plays.json ─────────────────────────────────────────────────

if (UPDATE_JSON) {
  // Write back to the source plays.json paths
  const websiteTarkaDataDir = path.dirname(PLAYS_PATH);

  // Update plays.json (combined)
  fs.writeFileSync(PLAYS_PATH, JSON.stringify(updatedPlays, null, 2));
  console.log(`Updated ${PLAYS_PATH}`);

  // Update split files
  const marketing = updatedPlays.filter(p => p.stage === 'Marketing');
  const sales = updatedPlays.filter(p => p.stage === 'Sales');
  const product = updatedPlays.filter(p => p.stage === 'Product');

  const mPath = path.join(websiteTarkaDataDir, 'plays-marketing.json');
  const sPath = path.join(websiteTarkaDataDir, 'plays-sales.json');
  const prPath = path.join(websiteTarkaDataDir, 'plays-product.json');

  if (fs.existsSync(mPath)) { fs.writeFileSync(mPath, JSON.stringify(marketing, null, 2)); console.log(`Updated ${mPath}`); }
  if (fs.existsSync(sPath)) { fs.writeFileSync(sPath, JSON.stringify(sales, null, 2)); console.log(`Updated ${sPath}`); }
  if (fs.existsSync(prPath)) { fs.writeFileSync(prPath, JSON.stringify(product, null, 2)); console.log(`Updated ${prPath}`); }
}

console.log('\nDone.');
