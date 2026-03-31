#!/usr/bin/env python3
"""
Rewrite all 960 play files with:
1. Correct per-level drill assignments (no compounding)
2. Agent-executable instructions referencing specific drills
3. Clear human vs agent responsibility
"""
import os
import re
import sys
import yaml

REPO = "/Users/dan/Projects/tarka/gtm-skills"
SKILLS_DIR = os.path.join(REPO, "skills")

# =============================================================================
# MOTION -> LEVEL -> DRILLS mapping
# Each level gets ONLY the drills relevant to THAT level's work
# =============================================================================

MOTION_DRILLS = {
    "Outbound Founder-Led": {
        "smoke": ["icp-definition", "build-prospect-list", "threshold-engine"],
        "baseline": ["cold-email-sequence", "linkedin-outreach", "posthog-gtm-events"],
        "scalable": ["follow-up-automation", "tool-sync-workflow", "ab-test-orchestrator"],
        "durable": ["dashboard-builder", "signal-detection"],
    },
    "Founder Social Content": {
        "smoke": ["icp-definition", "social-content-pipeline", "threshold-engine"],
        "baseline": ["content-repurposing", "posthog-gtm-events"],
        "scalable": ["follow-up-automation", "ab-test-orchestrator"],
        "durable": ["dashboard-builder"],
    },
    "Communities & Forums": {
        "smoke": ["icp-definition", "social-content-pipeline", "threshold-engine"],
        "baseline": ["posthog-gtm-events", "content-repurposing"],
        "scalable": ["tool-sync-workflow", "ab-test-orchestrator"],
        "durable": ["dashboard-builder"],
    },
    "Lightweight Paid": {
        "smoke": ["ad-campaign-setup", "landing-page-pipeline", "threshold-engine"],
        "baseline": ["budget-allocation", "posthog-gtm-events", "retargeting-setup"],
        "scalable": ["ab-test-orchestrator", "tool-sync-workflow"],
        "durable": ["dashboard-builder"],
    },
    "Micro Events": {
        "smoke": ["icp-definition", "webinar-pipeline", "threshold-engine"],
        "baseline": ["meetup-pipeline", "posthog-gtm-events"],
        "scalable": ["follow-up-automation", "ab-test-orchestrator"],
        "durable": ["dashboard-builder"],
    },
    "Partnerships & Warm Intros": {
        "smoke": ["icp-definition", "build-prospect-list", "threshold-engine"],
        "baseline": ["warm-intro-request", "posthog-gtm-events"],
        "scalable": ["follow-up-automation", "tool-sync-workflow"],
        "durable": ["dashboard-builder"],
    },
    "PR & Earned Mentions": {
        "smoke": ["icp-definition", "blog-seo-pipeline", "threshold-engine"],
        "baseline": ["case-study-creation", "newsletter-pipeline", "posthog-gtm-events"],
        "scalable": ["content-repurposing", "ab-test-orchestrator"],
        "durable": ["dashboard-builder"],
    },
    "Directories & Marketplaces": {
        "smoke": ["icp-definition", "blog-seo-pipeline", "threshold-engine"],
        "baseline": ["posthog-gtm-events", "landing-page-pipeline"],
        "scalable": ["ab-test-orchestrator", "tool-sync-workflow"],
        "durable": ["dashboard-builder"],
    },
    "Lead Capture Surface": {
        "smoke": ["icp-definition", "onboarding-flow", "threshold-engine"],
        "baseline": ["posthog-gtm-events", "feature-announcement", "activation-optimization"],
        "scalable": ["ab-test-orchestrator", "churn-prevention", "upgrade-prompt"],
        "durable": ["dashboard-builder", "nps-feedback-loop"],
    },
}

# =============================================================================
# LEVEL NAMES and next-level references
# =============================================================================
LEVEL_META = {
    "smoke": {
        "label": "Smoke Test",
        "next": "Baseline Run",
        "next_file": "baseline",
        "philosophy": "prepare_and_measure",
    },
    "baseline": {
        "label": "Baseline Run",
        "next": "Scalable Automation",
        "next_file": "scalable",
        "philosophy": "setup_and_run",
    },
    "scalable": {
        "label": "Scalable Automation",
        "next": "Durable Intelligence",
        "next_file": "durable",
        "philosophy": "automate_and_optimize",
    },
    "durable": {
        "label": "Durable Intelligence",
        "next": None,
        "next_file": None,
        "philosophy": "monitor_and_evolve",
    },
}


def parse_frontmatter(content):
    """Extract frontmatter and body from a markdown file."""
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    fm_text = parts[1]
    body = parts[2]

    # Parse frontmatter manually (simple YAML-like)
    fm = {}
    current_key = None
    current_list = None
    multiline_val = False
    multiline_buf = ""

    for line in fm_text.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue

        # List items
        if current_list is not None and stripped.startswith("- "):
            current_list.append(stripped[2:].strip())
            continue
        elif current_list is not None and not stripped.startswith("- "):
            fm[current_key] = current_list
            current_list = None
            current_key = None

        # Multiline value continuation
        if multiline_val:
            if ":" in stripped and not stripped.startswith(" "):
                fm[current_key] = multiline_buf.strip()
                multiline_val = False
                multiline_buf = ""
            else:
                multiline_buf += " " + stripped
                continue

        # Key: value pairs
        if ":" in stripped:
            key, _, val = stripped.partition(":")
            key = key.strip()
            val = val.strip()

            if val == ">":
                multiline_val = True
                multiline_buf = ""
                current_key = key
                continue
            elif val == "" or val == "[]":
                if val == "[]":
                    fm[key] = []
                else:
                    current_key = key
                    current_list = []
                continue
            else:
                # Strip quotes
                val = val.strip('"').strip("'")
                # Check for inline list like ["a", "b"]
                if val.startswith("[") and val.endswith("]"):
                    items = val[1:-1].split(",")
                    fm[key] = [i.strip().strip('"').strip("'") for i in items]
                else:
                    fm[key] = val
                current_key = key

    # Flush any pending
    if multiline_val:
        fm[current_key] = multiline_buf.strip()
    if current_list is not None:
        fm[current_key] = current_list

    return fm, body


def build_frontmatter(fm, drills):
    """Reconstruct the frontmatter string with updated drills."""
    lines = ["---"]

    # name
    lines.append(f'name: {fm.get("name", "")}')

    # description (multiline)
    desc = fm.get("description", "")
    lines.append("description: >")
    # Wrap at ~100 chars
    words = desc.split()
    current_line = "  "
    for w in words:
        if len(current_line) + len(w) + 1 > 100:
            lines.append(current_line)
            current_line = "  " + w
        else:
            current_line += " " + w if current_line.strip() else "  " + w
    if current_line.strip():
        lines.append(current_line)

    # stage, motion, channels, level
    for key in ["stage", "motion", "channels", "level"]:
        if key in fm:
            lines.append(f'{key}: "{fm[key]}"')

    # time, outcome
    for key in ["time", "outcome"]:
        if key in fm:
            lines.append(f'{key}: "{fm[key]}"')

    # kpis
    if "kpis" in fm:
        kpis = fm["kpis"]
        if isinstance(kpis, list):
            kpi_str = ", ".join(f'"{k}"' for k in kpis)
            lines.append(f"kpis: [{kpi_str}]")
        else:
            lines.append(f"kpis: {kpis}")

    # slug, install
    for key in ["slug", "install"]:
        if key in fm:
            lines.append(f'{key}: "{fm[key]}"')

    # drills
    lines.append("drills:")
    for d in drills:
        lines.append(f"  - {d}")

    lines.append("---")
    return "\n".join(lines)


# =============================================================================
# INSTRUCTION GENERATORS PER MOTION x LEVEL
# =============================================================================


def gen_instructions_outbound_smoke(fm):
    slug = fm.get("slug", "this-play")
    name = fm.get("name", "").replace("-smoke", "").replace("-", " ").title()
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Define your ICP and build a target list
Run the `icp-definition` drill to document your Ideal Customer Profile for {slug}. Define company size, industry, job titles, and pain points. Then run the `build-prospect-list` drill to source 20-50 contacts matching this ICP from Clay. Export the list to Attio CRM.

### 2. Prepare outreach materials
Using the ICP output, draft your {slug} materials manually. Write 2-3 variants of your core message targeting the specific pain points identified. Keep it scrappy -- this is a Smoke test to validate the channel, not to optimize.

**Human action required:** Execute the outreach manually. Send messages, make calls, or run the micro-campaign by hand. Log every touchpoint in Attio with status and response.

### 3. Track results
For each interaction, log the outcome in Attio (replied, meeting booked, ignored, bounced). Note which message variant and which ICP segment performed best.

### 4. Evaluate against threshold
Run the `threshold-engine` drill to evaluate results against your pass threshold: {outcome}. The threshold engine will pull your logged data from Attio and PostHog, compare against the target, and return PASS or FAIL.

If PASS, proceed to the Baseline level. If FAIL, adjust your ICP, messaging, or targeting and re-run this Smoke test."""


def gen_instructions_outbound_baseline(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Set up cold outreach tooling
Run the `cold-email-sequence` drill to configure Instantly with warmed-up sending accounts. Import your prospect list from Attio (built during Smoke). Create 3-5 email variants using the ICP pain points validated in Smoke. Set up A/B subject line testing.

### 2. Launch LinkedIn outreach in parallel
Run the `linkedin-outreach` drill to set up a connection request + follow-up message sequence targeting the same prospect list. Coordinate timing so LinkedIn and email touches don't overlap for the same prospect.

### 3. Configure tracking
Run the `posthog-gtm-events` drill to set up event tracking for this play. Configure events: `{slug}_email_sent`, `{slug}_email_replied`, `{slug}_meeting_booked`, `{slug}_linkedin_connected`. Connect PostHog to Attio via webhook so deal stage changes are tracked automatically.

### 4. Execute and monitor for 2 weeks
Let the sequences run. Monitor daily: check reply rates, positive vs negative sentiment, bounce rates. Adjust messaging mid-flight if reply rates are below 2% after the first 50 sends.

### 5. Evaluate against threshold
Review PostHog funnel data and Attio deal pipeline. Measure against: {outcome}. If PASS, proceed to Scalable. If FAIL, diagnose whether the issue is targeting (wrong ICP), messaging (low reply rate), or conversion (replies but no meetings)."""


def gen_instructions_outbound_scalable(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Build automated follow-up workflows
Run the `follow-up-automation` drill to create n8n workflows that: (a) detect when a prospect opens an email but doesn't reply, and trigger a follow-up sequence, (b) detect when a LinkedIn connection is accepted, and trigger a personalized message, (c) route positive replies to Attio and notify the founder via Slack.

### 2. Connect your tool stack
Run the `tool-sync-workflow` drill to build n8n sync workflows connecting Instantly replies to Attio deals, LinkedIn activity to Attio contact records, and PostHog events to Attio properties. Ensure no data is siloed.

### 3. Launch A/B testing
Run the `ab-test-orchestrator` drill. Set up experiments on: email subject lines, email body copy, LinkedIn message templates, send timing (day of week, time of day). Use PostHog feature flags to randomly assign variants. Run each test for a minimum of 100 sends per variant before declaring a winner.

### 4. Scale volume
Increase prospect volume to 200-500 per month. Use the automated workflows to handle follow-ups without manual intervention. Monitor the n8n execution logs for errors.

### 5. Evaluate against threshold
Measure against: {outcome}. Review A/B test results to identify winning variants. If PASS, proceed to Durable. If FAIL, focus on the lowest-performing stage in the funnel and run targeted experiments."""


def gen_instructions_outbound_durable(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Build monitoring dashboards
Run the `dashboard-builder` drill to create a PostHog dashboard for {slug} with panels: weekly send volume, reply rate trend, meeting conversion rate, pipeline value from this play, cost per meeting. Set up alerts for when any metric drops below the Scalable-level baseline by more than 20%.

### 2. Deploy signal-based targeting
Run the `signal-detection` drill to configure Clay to monitor for buying signals: job changes at target accounts, funding announcements, tech stack changes, competitor mentions. Feed these signals into your prospect list automatically via n8n. Prioritize outreach to signal-detected accounts.

### 3. Set up autonomous optimization
Configure n8n workflows to: (a) automatically pause underperforming sequences when reply rates drop below 1% for 3 consecutive days, (b) promote winning A/B test variants and start new experiments, (c) alert the founder when a high-value deal enters the pipeline.

### 4. Run continuous improvement cycles
Monthly: review dashboard trends, retire messaging that has decayed below threshold, test new ICP segments based on won-deal patterns. The agent should generate a monthly report summarizing: what changed, what was tested, what was retired, and recommended next experiments.

### 5. Evaluate sustainability
Measure against: {outcome}. This level runs continuously. If metrics sustain or improve, the play is durable. If metrics decay, diagnose whether the issue is market saturation, message fatigue, or ICP drift."""


def gen_instructions_social_smoke(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Define your content ICP
Run the `icp-definition` drill to define who you are creating content for. Document: target audience job titles, pain points they search for, platforms they use, content formats they engage with.

### 2. Create a content batch
Run the `social-content-pipeline` drill to create 5-10 pieces of social content. Use the LinkedIn hook frameworks and content templates. Write posts targeting the pain points from your ICP definition. Prepare content for manual posting.

**Human action required:** Post the content manually on LinkedIn/Twitter over 1-2 weeks. Engage with comments and replies personally.

### 3. Track engagement
Log each post's performance: impressions, likes, comments, profile views, DMs received, link clicks. Note which topics and formats got the most engagement.

### 4. Evaluate against threshold
Run the `threshold-engine` drill to measure results against: {outcome}. If PASS, proceed to Baseline. If FAIL, adjust your content topics, hooks, or posting frequency and re-run."""


def gen_instructions_social_baseline(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Set up content repurposing
Run the `content-repurposing` drill to build a system that takes each piece of content and adapts it across formats: LinkedIn post to Twitter thread, blog post to newsletter, video clip to social post. This multiplies your content output without multiplying effort.

### 2. Configure analytics tracking
Run the `posthog-gtm-events` drill to track content performance events: `{slug}_post_published`, `{slug}_engagement_received`, `{slug}_profile_visit`, `{slug}_dm_received`, `{slug}_lead_captured`. Connect social platform analytics to PostHog via n8n webhooks.

### 3. Execute a 2-week content calendar
Publish 3-5 pieces per week across platforms using the repurposed content system. Track all engagement in PostHog. Identify which content pillars (topics) drive the most qualified engagement.

### 4. Evaluate against threshold
Review PostHog data against: {outcome}. If PASS, proceed to Scalable. If FAIL, pivot content topics or try different formats (video, carousels, threads vs single posts)."""


def gen_instructions_social_scalable(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Automate content distribution
Run the `follow-up-automation` drill to build n8n workflows that: schedule posts across platforms, auto-DM new followers who match ICP criteria, and notify you when high-engagement posts deserve a follow-up or repurpose.

### 2. Launch content A/B testing
Run the `ab-test-orchestrator` drill to systematically test: hook styles (question vs statistic vs story), content length (short vs long-form), posting times, CTAs (comment vs DM vs link). Run each test over 10+ posts before declaring winners.

### 3. Scale to daily publishing
Increase to daily posting with automated scheduling. Use the repurposing pipeline to generate 5+ pieces from each original piece of content. Monitor engagement rates to ensure quality doesn't drop with volume.

### 4. Evaluate against threshold
Measure against: {outcome}. If PASS, proceed to Durable. If FAIL, focus on the content pillars and formats that showed the best results and cut the rest."""


def gen_instructions_social_durable(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Build performance dashboards
Run the `dashboard-builder` drill to create a PostHog dashboard tracking: weekly impressions trend, engagement rate by content pillar, follower growth rate, DMs and leads from content, content-attributed pipeline value. Set alerts for engagement rate drops.

### 2. Autonomous content optimization
Configure the agent to: monitor which content pillars are trending up or down, suggest retirement of underperforming topics, propose new topics based on ICP pain point research, and auto-generate content briefs for the next week based on what performed best.

### 3. Run monthly content reviews
The agent generates a monthly report: top-performing posts, engagement trends, audience growth, content-to-pipeline attribution. Review and approve the next month's content strategy.

### 4. Evaluate sustainability
Measure against: {outcome}. This level runs continuously. If engagement sustains or grows, the play is durable. If engagement decays, test new content formats or platforms."""


def gen_instructions_communities_smoke(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Identify target communities
Run the `icp-definition` drill to map where your ICP spends time: Slack communities, Discord servers, Reddit subreddits, forums, Facebook groups. List 5-10 communities ranked by relevance and activity level.

### 2. Create valuable content for communities
Run the `social-content-pipeline` drill to create 5-10 pieces of community-appropriate content: helpful answers, resource shares, discussion starters, case studies. Avoid promotional content -- focus on being genuinely useful.

**Human action required:** Join the communities and post content manually. Engage authentically in discussions. Build reputation before mentioning your product. Log all activity in Attio.

### 3. Track community engagement
Log each interaction: post/comment, community name, engagement received, DMs or follows generated, any leads captured. Note which communities and content types generate the most interest.

### 4. Evaluate against threshold
Run the `threshold-engine` drill to measure against: {outcome}. If PASS, proceed to Baseline. If FAIL, try different communities or adjust your content approach."""


def gen_instructions_communities_baseline(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Set up analytics
Run the `posthog-gtm-events` drill to track community-driven traffic and conversions: `{slug}_community_post`, `{slug}_referral_visit`, `{slug}_signup_from_community`. Use UTM parameters on all shared links to attribute traffic to specific communities.

### 2. Build a content repurposing system
Run the `content-repurposing` drill to adapt your best-performing community content across multiple communities and formats. One detailed answer can become a Reddit post, a Slack thread, a blog post, and a Twitter thread.

### 3. Execute a 2-week community engagement plan
Post 2-3 times per week across your top communities. Track everything in PostHog. Focus on communities that showed traction in Smoke.

### 4. Evaluate against threshold
Measure against: {outcome}. If PASS, proceed to Scalable. If FAIL, narrow focus to fewer communities or try different content types."""


def gen_instructions_communities_scalable(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Automate community monitoring
Run the `tool-sync-workflow` drill to build n8n workflows that monitor target communities for relevant discussions, new questions matching your expertise, and mentions of competitors. Send alerts to Slack when high-opportunity threads appear.

### 2. Test engagement approaches
Run the `ab-test-orchestrator` drill to test: response formats (short vs detailed), content types (how-to vs opinion vs data), timing of engagement, and CTA approaches (soft mention vs case study link).

### 3. Scale to daily community presence
Respond to community threads daily using the monitoring alerts. Establish authority in 3-5 key communities. Track which communities drive the most qualified traffic and focus effort there.

### 4. Evaluate against threshold
Measure against: {outcome}. If PASS, proceed to Durable. If FAIL, reassess community selection or pivot to creating your own community."""


def gen_instructions_communities_durable(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Build community dashboards
Run the `dashboard-builder` drill to create a PostHog dashboard: traffic from each community, conversion rates by community, engagement trends, pipeline value attributed to community activity. Set alerts for traffic drops from key communities.

### 2. Autonomous community optimization
Configure the agent to: monitor community engagement trends, identify emerging communities in your space, flag when your reputation score drops (fewer upvotes, less engagement), and generate weekly community content briefs.

### 3. Sustain and evolve
The agent runs monthly reviews: which communities are driving the most pipeline, which are declining, what new communities should be tested. Adjust community allocation accordingly.

### 4. Evaluate sustainability
Measure against: {outcome}. This level runs continuously. If community-driven pipeline sustains, the play is durable."""


def gen_instructions_paid_smoke(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Set up ad campaign
Run the `ad-campaign-setup` drill to configure your ad platform (Google Ads, LinkedIn Ads, or Meta Ads depending on the play). Set up conversion tracking pixels. Define your target audience using the ICP from your Smoke hypothesis.

### 2. Build a landing page
Run the `landing-page-pipeline` drill to create a dedicated landing page in Webflow for this campaign. Include: clear headline matching the ad copy, social proof, single CTA, and PostHog tracking. Keep the page simple -- one message, one action.

**Human action required:** Set a small test budget ($200-500). Launch the campaign and monitor for 1 week. Do not optimize mid-flight -- let the data accumulate.

### 3. Track results
Monitor: impressions, clicks, CTR, landing page conversion rate, cost per lead, lead quality (are they ICP matches?).

### 4. Evaluate against threshold
Run the `threshold-engine` drill to measure against: {outcome}. If PASS, proceed to Baseline. If FAIL, diagnose whether the issue is targeting (wrong audience), creative (low CTR), or landing page (low conversion)."""


def gen_instructions_paid_baseline(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Optimize budget allocation
Run the `budget-allocation` drill to analyze your Smoke test data and allocate budget across ad sets, audiences, and platforms. Shift budget toward the highest-performing segments. Set daily budget caps to prevent overspend.

### 2. Set up retargeting
Run the `retargeting-setup` drill to configure retargeting audiences: website visitors who didn't convert, landing page visitors, and engaged social followers. Create retargeting ad variants with stronger CTAs.

### 3. Configure tracking pipeline
Run the `posthog-gtm-events` drill to set up end-to-end tracking: `{slug}_ad_click`, `{slug}_landing_page_view`, `{slug}_form_submit`, `{slug}_lead_qualified`. Connect ad platform data to PostHog via webhooks for unified reporting.

### 4. Run for 2 weeks at increased budget
Scale budget to $1,000-3,000 for the test period. Monitor daily: CPA trends, quality of leads entering CRM, ad fatigue indicators (declining CTR). Make weekly adjustments to targeting and creative.

### 5. Evaluate against threshold
Measure against: {outcome}. If PASS, proceed to Scalable. If FAIL, test different audiences, creatives, or platforms."""


def gen_instructions_paid_scalable(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Automate campaign management
Run the `ab-test-orchestrator` drill to set up systematic creative testing: test 3-5 ad variants per audience, automatically pause underperformers, promote winners, and launch new variants weekly.

### 2. Build tool sync workflows
Run the `tool-sync-workflow` drill to connect: ad platform conversions to Attio deals, PostHog events to ad platform audiences (for lookalike targeting), and CRM data back to ad platforms for exclusion lists (don't target existing customers).

### 3. Scale budget with guardrails
Increase budget 20-30% monthly as long as CPA stays within target. Set automated alerts for CPA increases above 20%. Build n8n workflows to pause campaigns automatically if daily spend exceeds budget by 10%.

### 4. Evaluate against threshold
Measure against: {outcome}. If PASS, proceed to Durable. If FAIL, consolidate to best-performing audiences and creatives before scaling further."""


def gen_instructions_paid_durable(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Build paid media dashboards
Run the `dashboard-builder` drill to create a PostHog dashboard: ROAS by campaign, CPA trend over time, lead quality score by source, budget utilization, creative performance decay curves. Set alerts for CPA increases and ROAS drops.

### 2. Autonomous campaign optimization
Configure the agent to: detect creative fatigue (declining CTR over 5+ days), automatically generate new creative briefs, adjust bids based on conversion data, and reallocate budget from underperforming to overperforming campaigns weekly.

### 3. Run continuous improvement
Monthly: review full-funnel attribution (ad click to closed deal), identify which audiences and creatives drive revenue (not just leads), and adjust strategy accordingly. The agent generates a monthly paid media report.

### 4. Evaluate sustainability
Measure against: {outcome}. This level runs continuously. If ROAS sustains, the play is durable. If ROAS decays, test new platforms or audiences."""


def gen_instructions_events_smoke(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Define your event ICP
Run the `icp-definition` drill to define who should attend your event. Document: target audience, what they want to learn, ideal event format (webinar, meetup, workshop), and how you will invite them.

### 2. Set up event infrastructure
Run the `webinar-pipeline` drill to configure your event: create Cal.com booking page or registration form, set up email confirmations via Loops, create an Attio list for registrants. Prepare your event content and materials.

**Human action required:** Promote the event through your channels (email, social, communities). Run the event live. The agent prepares everything but you execute the event.

### 3. Track registrations and attendance
Log all registrants in Attio. Track: registrations, attendance rate, engagement during event (questions asked, polls answered), and follow-up actions taken.

### 4. Evaluate against threshold
Run the `threshold-engine` drill to measure against: {outcome}. If PASS, proceed to Baseline. If FAIL, adjust event topic, format, promotion channels, or timing."""


def gen_instructions_events_baseline(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Build event operations
Run the `meetup-pipeline` drill to create a repeatable event process: registration page, automated email reminders (1 week, 1 day, 1 hour before), attendee tracking in Attio, and post-event follow-up sequence.

### 2. Configure event analytics
Run the `posthog-gtm-events` drill to track: `{slug}_registered`, `{slug}_attended`, `{slug}_engaged`, `{slug}_follow_up_replied`, `{slug}_meeting_booked`. Build a funnel from registration to pipeline.

### 3. Run 2-3 events over 2-4 weeks
Execute a small series to validate repeatable demand. Test different topics, times, and promotion channels. Track what drives the highest registration-to-attendance and attendance-to-pipeline rates.

### 4. Evaluate against threshold
Measure against: {outcome}. If PASS, proceed to Scalable. If FAIL, diagnose: is the problem awareness (low registrations), commitment (low attendance), or conversion (attendees don't convert)."""


def gen_instructions_events_scalable(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Automate event operations
Run the `follow-up-automation` drill to build n8n workflows: auto-send post-event follow-ups based on engagement level (active participants get a different email than passive attendees), auto-create Attio deals for qualified attendees, and auto-schedule next event invitations.

### 2. Test event variations
Run the `ab-test-orchestrator` drill to test: event formats (webinar vs workshop vs AMA), event lengths, topics, speakers, and promotion channels. Use registration and attendance data to identify winning combinations.

### 3. Scale to regular cadence
Move to bi-weekly or monthly events. Automate as much of the operations as possible. Focus your manual effort on content quality and live delivery.

### 4. Evaluate against threshold
Measure against: {outcome}. If PASS, proceed to Durable. If FAIL, reduce frequency and focus on the event format that converts best."""


def gen_instructions_events_durable(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Build event dashboards
Run the `dashboard-builder` drill to create a PostHog dashboard: registration trends, attendance rates over time, pipeline generated per event, cost per attendee, content topic performance. Set alerts for declining registration or attendance rates.

### 2. Autonomous event optimization
Configure the agent to: analyze which event topics drive the most pipeline, suggest next event topics based on ICP pain point trends, auto-generate promotion copy for upcoming events, and flag when attendance rates are declining.

### 3. Sustain and evolve
Monthly: review event ROI, test new formats, and adjust cadence. The agent generates a monthly events report with recommendations.

### 4. Evaluate sustainability
Measure against: {outcome}. This level runs continuously. If events consistently generate pipeline, the play is durable."""


def gen_instructions_partnerships_smoke(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Define partner ICP
Run the `icp-definition` drill to define your ideal partner profile: complementary products, overlapping audiences, similar company stage, and shared values. Identify 10-20 potential partners.

### 2. Build a partner prospect list
Run the `build-prospect-list` drill to research and enrich partner contacts: find the right person at each company (partnerships lead, founder, head of BD), get their email and LinkedIn, and add them to an Attio list.

**Human action required:** Reach out to 10 partners personally. Use warm intros where possible. Propose a specific, low-commitment collaboration (content swap, co-promotion, intro exchange). Log all outreach in Attio.

### 3. Track partner conversations
Log every partner interaction in Attio: outreach sent, response received, meeting booked, collaboration agreed, results generated.

### 4. Evaluate against threshold
Run the `threshold-engine` drill to measure against: {outcome}. If PASS, proceed to Baseline. If FAIL, adjust your partner ICP or value proposition."""


def gen_instructions_partnerships_baseline(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Formalize partner outreach
Run the `warm-intro-request` drill to build a systematic intro request process: identify mutual connections in your network, craft personalized intro requests, and track request-to-intro conversion rates.

### 2. Configure partnership tracking
Run the `posthog-gtm-events` drill to track: `{slug}_partner_contacted`, `{slug}_intro_received`, `{slug}_collab_launched`, `{slug}_lead_from_partner`. Attribute pipeline to specific partnerships.

### 3. Execute 5-10 partnerships over 2-4 weeks
Run the collaborations: content swaps, co-promotions, intro exchanges, or joint webinars. Track results from each partnership individually to identify which partners and formats drive the most value.

### 4. Evaluate against threshold
Measure against: {outcome}. If PASS, proceed to Scalable. If FAIL, focus on the partnership format that showed the most promise and try different partners."""


def gen_instructions_partnerships_scalable(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Automate partner workflows
Run the `follow-up-automation` drill to build n8n workflows: auto-track partner referrals via UTM parameters, auto-create Attio deals from partner-sourced leads, and auto-send partner performance reports monthly.

### 2. Build partner ecosystem
Run the `tool-sync-workflow` drill to connect: partner referral tracking to Attio deals, PostHog events to partner attribution, and Loops emails for partner nurture sequences.

### 3. Scale partnerships
Expand to 20+ active partnerships. Systematize the collaboration formats that worked. Create templates and playbooks for common partnership types.

### 4. Evaluate against threshold
Measure against: {outcome}. If PASS, proceed to Durable. If FAIL, consolidate to the top 5 highest-performing partnerships."""


def gen_instructions_partnerships_durable(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Build partnership dashboards
Run the `dashboard-builder` drill to create a PostHog dashboard: leads per partner, conversion rate by partner, pipeline value by partnership type, partner engagement trends. Set alerts for declining partner referral volume.

### 2. Autonomous partnership management
Configure the agent to: monitor partner referral quality, flag partnerships with declining returns, suggest new partnership opportunities based on ICP overlap, and generate monthly partner reports.

### 3. Sustain and optimize
Monthly: review partner ROI, retire underperforming partnerships, test new collaboration formats. The agent identifies high-potential new partners from your Attio network data.

### 4. Evaluate sustainability
Measure against: {outcome}. This level runs continuously. If partnerships consistently generate pipeline, the play is durable."""


def gen_instructions_pr_smoke(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Define your PR angle
Run the `icp-definition` drill to define your target media audience: which publications your ICP reads, which journalists cover your space, what story angles would resonate. List 10-20 target publications and journalists.

### 2. Create foundational content
Run the `blog-seo-pipeline` drill to create 2-3 high-quality content pieces that can serve as PR assets: data-driven blog posts, original research, or expert commentary. These give journalists something to reference and link to.

**Human action required:** Pitch journalists and publications directly. Personalize each pitch with why this is relevant to their beat. Offer exclusive data or quotes. Log all outreach in Attio.

### 3. Track media outreach
Log every pitch: publication, journalist, angle, status (pitched, responded, published, linked). Track resulting coverage: mentions, backlinks, referral traffic.

### 4. Evaluate against threshold
Run the `threshold-engine` drill to measure against: {outcome}. If PASS, proceed to Baseline. If FAIL, refine your angles or target different publications."""


def gen_instructions_pr_baseline(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Build a PR content machine
Run the `case-study-creation` drill to create 2-3 customer case studies that serve as PR assets. Run the `newsletter-pipeline` drill to start your own newsletter that establishes thought leadership and gives journalists a reason to follow you.

### 2. Configure PR tracking
Run the `posthog-gtm-events` drill to track: `{slug}_mention_published`, `{slug}_backlink_acquired`, `{slug}_referral_traffic`, `{slug}_lead_from_pr`. Set up Google Alerts or a media monitoring tool for brand mentions.

### 3. Execute a 4-week PR push
Pitch 10-20 publications. Submit 2-3 guest articles. Publish your case studies and promote them. Track all coverage and resulting traffic in PostHog.

### 4. Evaluate against threshold
Measure against: {outcome}. If PASS, proceed to Scalable. If FAIL, test different story angles or target tier-2 publications first to build credibility."""


def gen_instructions_pr_scalable(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Repurpose PR content
Run the `content-repurposing` drill to turn every media mention into multiple assets: social posts, email newsletter content, website social proof, and sales enablement materials.

### 2. Test PR approaches
Run the `ab-test-orchestrator` drill to test: pitch angles (data-driven vs story-driven), outreach timing, follow-up cadence, and content types (guest post vs quote vs exclusive data). Track which approaches yield the highest coverage rates.

### 3. Scale media relationships
Move from one-off pitches to ongoing relationships. Offer journalists regular access to data, experts, and customer stories. Build a media list in Attio and nurture it.

### 4. Evaluate against threshold
Measure against: {outcome}. If PASS, proceed to Durable. If FAIL, focus on the media relationships that are generating the most value."""


def gen_instructions_pr_durable(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Build PR dashboards
Run the `dashboard-builder` drill to create a PostHog dashboard: media mentions over time, referral traffic from PR, backlink growth, PR-attributed leads, share of voice vs competitors. Set alerts for mention drops.

### 2. Autonomous PR monitoring
Configure the agent to: monitor brand and competitor mentions, flag PR opportunities (industry trends, breaking news where you can comment), generate pitch drafts for time-sensitive opportunities, and track journalist relationship health.

### 3. Sustain and evolve
Monthly: review PR impact on pipeline, identify new publications to target, update story angles based on product and market changes. The agent generates a monthly PR report.

### 4. Evaluate sustainability
Measure against: {outcome}. This level runs continuously. If PR consistently drives awareness and backlinks, the play is durable."""


def gen_instructions_directories_smoke(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Identify target directories
Run the `icp-definition` drill to map where your ICP discovers products: G2, Capterra, Product Hunt, industry-specific directories, GitHub, Chrome Web Store, marketplace listings. Prioritize by relevance and traffic.

### 2. Create optimized listings
Run the `blog-seo-pipeline` drill to research keywords your ICP uses when searching directories. Use these keywords in your listing titles, descriptions, and feature lists. Write compelling copy that differentiates you from competitors on the same platform.

**Human action required:** Create or update your listings on 3-5 directories. Submit for review. Ask 5-10 existing customers to leave reviews. Log all listings in Attio.

### 3. Track listing performance
Monitor: page views, clicks to your website, reviews received, leads generated from each directory. Use UTM parameters on all listing links.

### 4. Evaluate against threshold
Run the `threshold-engine` drill to measure against: {outcome}. If PASS, proceed to Baseline. If FAIL, improve listing copy or target different directories."""


def gen_instructions_directories_baseline(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Configure tracking
Run the `posthog-gtm-events` drill to track: `{slug}_listing_view`, `{slug}_listing_click`, `{slug}_listing_signup`, `{slug}_review_submitted`. Use UTM parameters per directory for attribution.

### 2. Build landing pages for directory traffic
Run the `landing-page-pipeline` drill to create directory-specific landing pages. Match the messaging to what users expect when coming from each directory. Include social proof relevant to that directory's audience.

### 3. Scale review collection
Implement a systematic review collection process: after positive customer interactions, send a Loops email requesting a review on the relevant directory. Track review velocity in PostHog.

### 4. Evaluate against threshold
Measure against: {outcome}. If PASS, proceed to Scalable. If FAIL, focus on the directories driving the most qualified traffic."""


def gen_instructions_directories_scalable(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Test listing variations
Run the `ab-test-orchestrator` drill to test: listing headlines, feature ordering, screenshot selection, pricing presentation, and CTA copy across directories. Rotate variations monthly.

### 2. Automate review and listing management
Run the `tool-sync-workflow` drill to build n8n workflows: auto-detect new reviews and alert team, auto-respond to reviews, sync directory-sourced leads to Attio, and auto-update listings when product features change.

### 3. Expand to more directories
List on 10+ directories. Focus effort on the top 3-5 that drive real pipeline. Maintain presence on others with minimal ongoing effort.

### 4. Evaluate against threshold
Measure against: {outcome}. If PASS, proceed to Durable. If FAIL, consolidate to highest-ROI directories."""


def gen_instructions_directories_durable(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Build directory dashboards
Run the `dashboard-builder` drill to create a PostHog dashboard: traffic per directory, conversion rate per directory, review score trends, pipeline attributed to directory traffic. Set alerts for review score drops or traffic declines.

### 2. Autonomous directory management
Configure the agent to: monitor competitor listings for changes, alert when new reviews come in, suggest listing updates based on new features or positioning changes, and track directory ranking positions.

### 3. Sustain and optimize
Monthly: review directory ROI, update listing copy, request new reviews, and respond to recent reviews. The agent generates a monthly directory performance report.

### 4. Evaluate sustainability
Measure against: {outcome}. This level runs continuously. If directories consistently drive qualified traffic, the play is durable."""


def gen_instructions_leadcapture_smoke(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Define your product ICP
Run the `icp-definition` drill to define who this product experience targets: user persona, what they are trying to accomplish, what success looks like, and what would make them convert or expand.

### 2. Set up the experience
Run the `onboarding-flow` drill to configure the in-product experience: Intercom product tours, in-app messages, or Loops email sequences. Focus on the single most important user action that correlates with conversion or retention.

**Human action required:** Review the experience flows before launching. Ensure the copy is clear and the CTAs are specific. Launch to a small test group (10-50 users) and observe behavior.

### 3. Track user behavior
Log all interactions in PostHog: tour started, tour completed, CTA clicked, action taken. Note drop-off points and user feedback.

### 4. Evaluate against threshold
Run the `threshold-engine` drill to measure against: {outcome}. If PASS, proceed to Baseline. If FAIL, simplify the experience or target a different user action."""


def gen_instructions_leadcapture_baseline(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Configure event tracking
Run the `posthog-gtm-events` drill to set up detailed tracking: `{slug}_impression`, `{slug}_engaged`, `{slug}_converted`, `{slug}_retained`. Build PostHog funnels showing the complete user journey through this experience.

### 2. Set up feature announcements
Run the `feature-announcement` drill to configure Intercom in-app messages and Loops emails that guide users through the experience. Create targeted messages for different user segments based on PostHog cohorts.

### 3. Optimize activation
Run the `activation-optimization` drill to identify and improve the key activation metric. Analyze PostHog funnels to find the biggest drop-off point. Test 2-3 variations of the experience at that point.

### 4. Evaluate against threshold
Measure against: {outcome}. If PASS, proceed to Scalable. If FAIL, diagnose where users are dropping off and test fixes at that specific point."""


def gen_instructions_leadcapture_scalable(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Launch systematic testing
Run the `ab-test-orchestrator` drill to test variations of your product experience: messaging copy, timing of prompts, CTA placement, and user segments. Use PostHog feature flags to run experiments. Run each test for statistical significance.

### 2. Build churn prevention
Run the `churn-prevention` drill to configure automated interventions: detect at-risk users via PostHog cohorts (declining usage, missed milestones), trigger Intercom messages or Loops emails to re-engage them.

### 3. Set up expansion prompts
Run the `upgrade-prompt` drill to configure upgrade and expansion triggers: usage threshold notifications, feature gate messages, and team invitation prompts. Time these based on user engagement data from PostHog.

### 4. Evaluate against threshold
Measure against: {outcome}. If PASS, proceed to Durable. If FAIL, focus on the highest-impact experiment and iterate."""


def gen_instructions_leadcapture_durable(fm):
    slug = fm.get("slug", "this-play")
    outcome = fm.get("outcome", "pass threshold")
    return f"""## Instructions

### 1. Build product dashboards
Run the `dashboard-builder` drill to create a PostHog dashboard: activation rate trend, conversion funnel by cohort, churn rate trend, expansion revenue, NPS score trend, feature adoption rates. Set alerts for activation or retention drops.

### 2. Launch feedback loops
Run the `nps-feedback-loop` drill to collect and act on user feedback: deploy NPS surveys at key milestones, route feedback to the product team, trigger follow-ups based on score (promoters get referral asks, detractors get personal outreach).

### 3. Autonomous product optimization
Configure the agent to: monitor all product metrics, detect trends (positive or negative), suggest experiments based on data, and generate weekly product health reports. The agent should flag when any metric deviates from baseline by more than 15%.

### 4. Evaluate sustainability
Measure against: {outcome}. This level runs continuously. If product metrics sustain or improve, the play is durable. If metrics decay, the agent diagnoses the cause and recommends interventions."""


# =============================================================================
# Map motions to instruction generators
# =============================================================================

INSTRUCTION_GENERATORS = {
    "Outbound Founder-Led": {
        "smoke": gen_instructions_outbound_smoke,
        "baseline": gen_instructions_outbound_baseline,
        "scalable": gen_instructions_outbound_scalable,
        "durable": gen_instructions_outbound_durable,
    },
    "Founder Social Content": {
        "smoke": gen_instructions_social_smoke,
        "baseline": gen_instructions_social_baseline,
        "scalable": gen_instructions_social_scalable,
        "durable": gen_instructions_social_durable,
    },
    "Communities & Forums": {
        "smoke": gen_instructions_communities_smoke,
        "baseline": gen_instructions_communities_baseline,
        "scalable": gen_instructions_communities_scalable,
        "durable": gen_instructions_communities_durable,
    },
    "Lightweight Paid": {
        "smoke": gen_instructions_paid_smoke,
        "baseline": gen_instructions_paid_baseline,
        "scalable": gen_instructions_paid_scalable,
        "durable": gen_instructions_paid_durable,
    },
    "Micro Events": {
        "smoke": gen_instructions_events_smoke,
        "baseline": gen_instructions_events_baseline,
        "scalable": gen_instructions_events_scalable,
        "durable": gen_instructions_events_durable,
    },
    "Partnerships & Warm Intros": {
        "smoke": gen_instructions_partnerships_smoke,
        "baseline": gen_instructions_partnerships_baseline,
        "scalable": gen_instructions_partnerships_scalable,
        "durable": gen_instructions_partnerships_durable,
    },
    "PR & Earned Mentions": {
        "smoke": gen_instructions_pr_smoke,
        "baseline": gen_instructions_pr_baseline,
        "scalable": gen_instructions_pr_scalable,
        "durable": gen_instructions_pr_durable,
    },
    "Directories & Marketplaces": {
        "smoke": gen_instructions_directories_smoke,
        "baseline": gen_instructions_directories_baseline,
        "scalable": gen_instructions_directories_scalable,
        "durable": gen_instructions_directories_durable,
    },
    "Lead Capture Surface": {
        "smoke": gen_instructions_leadcapture_smoke,
        "baseline": gen_instructions_leadcapture_baseline,
        "scalable": gen_instructions_leadcapture_scalable,
        "durable": gen_instructions_leadcapture_durable,
    },
}


def level_from_filename(filename):
    """Return the level key from a filename like smoke.md, baseline.md, etc."""
    name = os.path.splitext(filename)[0]
    return name  # smoke, baseline, scalable, durable


def rewrite_play(filepath):
    """Rewrite a single play file with correct drills and agent instructions."""
    with open(filepath) as f:
        content = f.read()

    fm, body = parse_frontmatter(content)
    if not fm:
        print(f"  WARNING: Could not parse frontmatter for {filepath}")
        return False

    motion = fm.get("motion", "")
    level_key = level_from_filename(os.path.basename(filepath))
    slug = fm.get("slug", "")
    name = fm.get("name", "")
    description = fm.get("description", "")
    stage = fm.get("stage", "")
    channels = fm.get("channels", "")
    time_val = fm.get("time", "")
    outcome = fm.get("outcome", "")
    kpis = fm.get("kpis", [])
    install = fm.get("install", "")
    level_label = fm.get("level", LEVEL_META.get(level_key, {}).get("label", level_key))

    if motion not in MOTION_DRILLS:
        print(f"  WARNING: Unknown motion '{motion}' for {filepath}")
        return False

    if level_key not in MOTION_DRILLS[motion]:
        print(f"  WARNING: Unknown level '{level_key}' for motion '{motion}' in {filepath}")
        return False

    # Get correct drills for this motion+level
    drills = MOTION_DRILLS[motion][level_key]

    # Get instruction generator
    gen_fn = INSTRUCTION_GENERATORS.get(motion, {}).get(level_key)
    if not gen_fn:
        print(f"  WARNING: No instruction generator for {motion}/{level_key}")
        return False

    instructions = gen_fn(fm)

    # Build the new frontmatter
    new_fm = build_frontmatter(fm, drills)

    # Determine the display name for the heading
    display_name = description.split(".")[0] if description else name.replace("-", " ").title()
    if " — " not in display_name:
        display_name = f"{display_name} — {level_label}"

    # Build the document
    level_meta = LEVEL_META[level_key]
    next_level = level_meta["next"]

    # KPI section
    kpi_section = "\n".join(f"- {k}" for k in kpis) if isinstance(kpis, list) else kpis

    # Pass threshold section
    if next_level:
        threshold_footer = f"""If you hit this threshold, move to the **{next_level}** level.
If not, iterate on your approach and re-run this level."""
    else:
        threshold_footer = """This level runs continuously. Review monthly: what improved, what to retire, what new experiments to run."""

    new_body = f"""
# {display_name}

> **Stage:** {stage.replace(' > ', ' → ')} | **Motion:** {motion} | **Channels:** {channels}

## Overview
{description}

**Time commitment:** {time_val}
**Pass threshold:** {outcome}

---

## Budget

{_get_budget_section(fm, level_key)}

---

{instructions}

---

## KPIs to track
{kpi_section}

---

## Pass threshold
**{outcome}**

{threshold_footer}

---

## How to run this skill

1. Ensure your stack is configured: `cat ~/.gtm-config.json` (or run `npx gtm-skills init`)
2. Your CRM (`{{{{crm}}}}`) and automation platform (`{{{{automation}}}}`) will be substituted throughout
3. Follow the instructions above step by step
4. Log all outcomes in PostHog and your CRM
5. Evaluate against the pass threshold at the end of the time window

_Install this skill: `{install}`_
"""

    with open(filepath, "w") as f:
        f.write(new_fm + new_body)

    return True


def _get_budget_section(fm, level_key):
    """Generate a budget section based on level."""
    if level_key == "smoke":
        return """**Play-specific cost:** Free

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._"""
    elif level_key == "baseline":
        return """**Play-specific tools & costs**
- **Tool-specific costs:** ~$50-200/mo depending on tools required

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._"""
    elif level_key == "scalable":
        return """**Play-specific tools & costs**
- **Tool and automation costs:** ~$100-500/mo at scale

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._"""
    else:  # durable
        return """**Play-specific tools & costs**
- **Ongoing tool costs:** ~$100-500/mo
- **Agent compute costs:** Variable based on monitoring frequency

_Your CRM, PostHog, and automation platform are not included — standard stack paid once._"""


def process_motion(motion_name):
    """Process all plays for a given motion."""
    count = 0
    errors = 0

    for root, dirs, files in os.walk(SKILLS_DIR):
        for f in files:
            if not f.endswith(".md"):
                continue
            filepath = os.path.join(root, f)
            with open(filepath) as fh:
                content = fh.read()

            # Quick check if this file belongs to this motion
            if f'motion: "{motion_name}"' not in content:
                continue

            if rewrite_play(filepath):
                count += 1
            else:
                errors += 1

    return count, errors


def main():
    if len(sys.argv) > 1:
        # Process specific motion
        motion = sys.argv[1]
        if motion not in MOTION_DRILLS:
            print(f"Unknown motion: {motion}")
            print(f"Valid motions: {list(MOTION_DRILLS.keys())}")
            sys.exit(1)
        print(f"Processing motion: {motion}")
        count, errors = process_motion(motion)
        print(f"Rewrote {count} files, {errors} errors")
    else:
        # Process all motions
        total = 0
        total_errors = 0
        for motion in MOTION_DRILLS:
            print(f"\nProcessing: {motion}")
            count, errors = process_motion(motion)
            print(f"  Rewrote {count} files, {errors} errors")
            total += count
            total_errors += errors
        print(f"\nTotal: {total} files rewritten, {total_errors} errors")


if __name__ == "__main__":
    main()
