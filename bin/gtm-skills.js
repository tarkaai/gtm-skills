#!/usr/bin/env node
'use strict';

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');
const readline = require('readline');

const args = process.argv.slice(2);
const cmd = args[0];

const SKILLS_DIR = path.join(__dirname, '..', 'skills');
const CLAUDE_SKILLS_DIR = path.join(os.homedir(), '.claude', 'skills');
const GLOBAL_CONFIG = path.join(os.homedir(), '.gtm-config.json');

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function ask(rl, question) {
  return new Promise(resolve => rl.question(question, resolve));
}

async function init() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  console.log('\nWelcome to gtm-skills! Let\'s configure your stack.\n');

  const crm = await ask(rl, 'CRM? (attio / salesforce / hubspot / pipedrive / clarify) [attio]: ');
  const automation = await ask(rl, 'Automation platform? (n8n / claude-code / make) [n8n]: ');
  const email_tool = await ask(rl, 'Email sequencing? (instantly / smartlead / lemlist / loops) [instantly]: ');
  const enrichment = await ask(rl, 'Lead enrichment? (clay / apollo) [clay]: ');
  const linkedin_tool = await ask(rl, 'LinkedIn automation? (dripify / expandi / waalaxy) [dripify]: ');
  const scheduling = await ask(rl, 'Scheduling? (cal.com / calendly) [cal.com]: ');

  rl.close();

  const config = {
    crm: crm || 'attio',
    automation: automation || 'n8n',
    email_tool: email_tool || 'instantly',
    enrichment: enrichment || 'clay',
    linkedin_tool: linkedin_tool || 'dripify',
    scheduling: scheduling || 'cal.com',
    analytics: 'posthog',
  };

  fs.writeFileSync(GLOBAL_CONFIG, JSON.stringify(config, null, 2));
  console.log(`\nConfig saved to ${GLOBAL_CONFIG}`);
  console.log('\nRun `npx gtm-skills install` to install skills into Claude Code.\n');
}

function installSkills({ stage, play, level } = {}) {
  ensureDir(CLAUDE_SKILLS_DIR);

  let installed = 0;
  const stageFilter = stage ? stage.toLowerCase() : null;
  const playFilter = play ? play.toLowerCase() : null;
  const levelFilter = level ? level.toLowerCase() : null;

  const stages = fs.readdirSync(SKILLS_DIR).filter(s => {
    if (stageFilter && s !== stageFilter) return false;
    return fs.statSync(path.join(SKILLS_DIR, s)).isDirectory();
  });

  for (const stageName of stages) {
    const stagePath = path.join(SKILLS_DIR, stageName);
    const subStages = fs.readdirSync(stagePath).filter(s =>
      fs.statSync(path.join(stagePath, s)).isDirectory()
    );
    for (const subStageName of subStages) {
      const subStagePath = path.join(stagePath, subStageName);
      const plays = fs.readdirSync(subStagePath).filter(p => {
        if (playFilter && p !== playFilter) return false;
        return fs.statSync(path.join(subStagePath, p)).isDirectory();
      });
      for (const playName of plays) {
        const playPath = path.join(subStagePath, playName);
        const files = fs.readdirSync(playPath).filter(f => {
          if (levelFilter && f !== `${levelFilter}.md`) return false;
          return f.endsWith('.md');
        });
        const destDir = path.join(CLAUDE_SKILLS_DIR, 'gtm', stageName, subStageName, playName);
        ensureDir(destDir);
        for (const file of files) {
          fs.copyFileSync(path.join(playPath, file), path.join(destDir, file));
          installed++;
        }
      }
    }
  }

  console.log(`\nInstalled ${installed} skill files to ${CLAUDE_SKILLS_DIR}/gtm/\n`);

  if (!fs.existsSync(GLOBAL_CONFIG)) {
    console.log('No config found. Run `npx gtm-skills init` to configure your stack.\n');
  }
}

async function main() {
  switch (cmd) {
    case 'init':
      await init();
      break;
    case 'install': {
      const stageIdx = args.indexOf('--stage');
      const playIdx = args.indexOf('--play');
      const levelIdx = args.indexOf('--level');
      installSkills({
        stage: stageIdx > -1 ? args[stageIdx + 1] : null,
        play: playIdx > -1 ? args[playIdx + 1] : null,
        level: levelIdx > -1 ? args[levelIdx + 1] : null,
      });
      break;
    }
    case 'add': {
      // npx gtm-skills add marketing/solution-aware/outbound-founder-email
      const slug = args[1];
      if (!slug) { console.error('Usage: gtm-skills add <stage/sub-stage/play-slug>'); process.exit(1); }
      const parts = slug.split('/');
      if (parts.length === 3) {
        installSkills({ stage: parts[0], play: parts[2] });
      } else {
        console.error('Usage: gtm-skills add <stage/sub-stage/play-slug>');
        process.exit(1);
      }
      break;
    }
    default:
      console.log(`
gtm-skills — GTM play skills for AI agents

Commands:
  init                          Configure your CRM and automation stack
  install                       Install all skills to ~/.claude/skills/
  install --stage <stage>       Install one stage (marketing/sales/product)
  install --play <slug>         Install one play (all 4 levels)
  install --level <level>       Combined with --play: install one level only
  add <stage/sub-stage/play>    Shorthand to add one play

Examples:
  npx gtm-skills init
  npx gtm-skills install
  npx gtm-skills install --stage marketing
  npx gtm-skills add marketing/solution-aware/outbound-founder-email
`);
  }
}

main().catch(err => { console.error(err); process.exit(1); });
