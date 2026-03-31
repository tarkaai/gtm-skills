#!/usr/bin/env bash
set -euo pipefail

REPO="/Users/dan/Projects/tarka/gtm-skills"
DRILLS="$REPO/drills"
FUNDIES="$REPO/fundamentals"
DRY_RUN="${1:-}"

log() { echo "[migrate] $*"; }
move_drill() {
    local src="$1" dest_cat="$2"
    local filename=$(basename "$src")
    local dest_dir="$DRILLS/$dest_cat"
    local dest="$dest_dir/$filename"
    
    if [ "$src" = "$dest" ]; then return; fi
    
    mkdir -p "$dest_dir"
    if [ -n "$DRY_RUN" ]; then
        echo "  WOULD MOVE: $src -> $dest"
    else
        mv "$src" "$dest"
    fi
}

move_fundamental_to_drill() {
    local src="$1" dest_cat="$2"
    local filename=$(basename "$src")
    local dest_dir="$DRILLS/$dest_cat"
    local dest="$dest_dir/$filename"
    
    mkdir -p "$dest_dir"
    if [ -n "$DRY_RUN" ]; then
        echo "  WOULD MOVE FUND->DRILL: $src -> $dest"
    else
        mv "$src" "$dest"
    fi
}

update_category() {
    local file="$1" new_cat="$2"
    if [ -n "$DRY_RUN" ]; then
        echo "  WOULD UPDATE category in $(basename "$file") -> $new_cat"
    else
        # Update the category: line in frontmatter
        sed -i '' "s/^category:.*/category: $new_cat/" "$file"
    fi
}

# ==============================================================
# STEP 1: FUNDAMENTALS — move multi-tool orchestrations to drills
# ==============================================================
log "=== STEP 1: Move orchestration fundamentals to drills ==="

# The call-transcript-* fundamentals are Fireflies + Claude orchestrations -> drills
# They belong in a "transcript-analysis" or "discovery" drill category
for f in "$FUNDIES"/sales/call-transcript-*.md; do
    [ -f "$f" ] && move_fundamental_to_drill "$f" "discovery"
done

# competitor-changelog-monitoring is Clay + n8n orchestration -> drills  
[ -f "$FUNDIES/research/competitor-changelog-monitoring.md" ] && \
    move_fundamental_to_drill "$FUNDIES/research/competitor-changelog-monitoring.md" "research"

# ==============================================================
# STEP 2: DRILLS — reclassify from stage-based to capability-based
# ==============================================================
log "=== STEP 2: Reclassify drills ==="

# --- PRODUCT (214) -> split into ~10 capability categories ---

# ONBOARDING (all user onboarding and activation drills)
for name in \
    onboarding-flow onboarding-personalization onboarding-sequence-design \
    onboarding-sequence-automation onboarding-experiment-orchestration \
    onboarding-persona-scaling onboarding-health-monitor \
    onboarding-call-script onboarding-call-routing onboarding-call-follow-up \
    onboarding-call-performance-monitor \
    signup-funnel-audit signup-friction-reduction signup-flow-personalization \
    signup-funnel-health-monitor \
    admin-user-role-routing workspace-setup-flow \
    quick-start-content-pipeline \
    empty-state-design empty-state-scaling empty-state-health-monitor \
    sample-data-seeding sample-data-engagement-monitor \
    template-gallery-setup \
    wizard-step-builder wizard-completion-monitor \
    integration-wizard-build integration-health-monitor \
    activation-optimization activation-health-monitor \
    ttv-health-monitor; do
    [ -f "$DRILLS/product/$name.md" ] && move_drill "$DRILLS/product/$name.md" "onboarding"
done

# RETENTION (churn prevention, health scoring, winback, engagement)
for name in \
    churn-signal-extraction churn-risk-scoring churn-prevention \
    churn-intervention-routing churn-model-health-monitor \
    winback-campaign winback-offer-personalization winback-campaign-health-monitor \
    at-risk-intervention-health-monitor \
    health-score-model-design health-score-alerting \
    engagement-score-computation engagement-score-weight-tuning engagement-alert-routing \
    usage-drop-detection usage-alert-delivery usage-alert-health-monitor \
    cohort-retention-extraction cohort-retention-health-monitor cohort-insight-generation \
    milestone-retention-monitor \
    inactive-reengagement-health-monitor \
    support-churn-correlation support-health-monitor support-ticket-analysis \
    nps-feedback-loop nps-response-routing nps-health-monitor nps-segment-scaling \
    commitment-health-monitor \
    cs-playbook-health-monitor; do
    [ -f "$DRILLS/product/$name.md" ] && move_drill "$DRILLS/product/$name.md" "retention"
done

# CONVERSION (upgrade, pricing, trial, freemium, PLG, downgrade)
for name in \
    upgrade-prompt upgrade-prompt-health-monitor \
    pricing-experiment-runner pricing-page-conversion-monitor pricing-health-monitor \
    trial-activation-scoring trial-intervention-orchestration trial-conversion-health-monitor \
    freemium-conversion-health-report free-to-paid-funnel-health-monitor \
    gate-conversion-health-report \
    plg-conversion-health-monitor plg-sales-routing \
    downgrade-intent-detection downgrade-intercept-flow downgrade-intervention-health-monitor \
    auto-upgrade-execution \
    annual-conversion-health-monitor \
    usage-threshold-detection usage-pricing-model-analysis usage-revenue-optimization-report \
    multiyear-offer-engine; do
    [ -f "$DRILLS/product/$name.md" ] && move_drill "$DRILLS/product/$name.md" "conversion"
done
# Also move the existing conversion/ drills (brand/cta stuff stays)
# They're already in conversion/, so just leave them

# ADVOCACY (referrals, viral, UGC, case studies, testimonials, champions, reviews)  
for name in \
    referral-program referral-health-monitor referral-funnel-monitor \
    referral-channel-scaling referral-segment-scaling referral-fulfillment-automation \
    viral-mechanic-design viral-loop-instrumentation viral-coefficient-monitor \
    invite-flow-setup invite-acceptance-optimization invite-viral-loop invite-health-monitor \
    social-share-surface-build social-share-health-monitor \
    share-content-generator public-share-health-monitor \
    ugc-prompt-design ugc-collection-automation ugc-incentive-scaling ugc-health-monitor \
    testimonial-request-pipeline testimonial-health-monitor \
    case-study-candidate-pipeline case-study-recruitment-health-monitor \
    review-request-health-monitor \
    advocacy-program-design advocacy-activation-pipeline advocacy-health-monitor \
    champion-identification-scoring champion-recognition-pipeline \
    champion-co-marketing-pipeline champion-program-health-monitor \
    power-user-scoring; do
    [ -f "$DRILLS/product/$name.md" ] && move_drill "$DRILLS/product/$name.md" "advocacy"
done

# REVENUE-OPS (billing, dunning, seat expansion, NDR, add-ons, cross-sell)
for name in \
    dunning-sequence-automation \
    payment-failure-detection payment-recovery-health-monitor \
    proactive-card-expiry-detection \
    seat-growth-signal-detection seat-expansion-prompt-delivery seat-expansion-health-monitor \
    ndr-baseline-measurement ndr-cohort-tracking ndr-health-monitor \
    addon-discovery-surface-build addon-cross-sell-health-monitor \
    cross-sell-catalog-mapping cross-sell-segment-scaling; do
    [ -f "$DRILLS/product/$name.md" ] && move_drill "$DRILLS/product/$name.md" "revenue-ops"
done

# ENABLEMENT (gamification, certification, best practices, AI coaching, recommendations, tooltips, workflows)
for name in \
    gamification-system-design gamification-event-tracking gamification-reward-delivery \
    gamification-leaderboard-pipeline gamification-personalization gamification-health-monitor \
    certification-curriculum-design certification-delivery-automation \
    certification-scaling-pipeline certification-health-monitor \
    best-practices-content-pipeline best-practices-delivery-automation \
    best-practices-personalization best-practices-health-report \
    ai-coach-conversation-design ai-coach-health-monitor \
    ai-chatbot-deployment chatbot-knowledge-pipeline chatbot-escalation-routing chatbot-resolution-monitor \
    recommendation-engine-prototype recommendation-personalization-pipeline recommendation-health-monitor \
    tooltip-targeting-automation tooltip-performance-monitor \
    shortcut-discovery-promotion shortcut-adoption-monitor \
    spotlight-series-health-monitor \
    workflow-suggestion-personalization workflow-suggestion-delivery \
    workflow-behavior-analysis workflow-optimization-health-monitor \
    usage-milestone-rewards usage-analytics-surface-build usage-analytics-engagement-monitor \
    ai-content-prompt-optimization ai-content-usage-health-monitor; do
    [ -f "$DRILLS/product/$name.md" ] && move_drill "$DRILLS/product/$name.md" "enablement"
done

# IN-APP-MESSAGING (push, in-app messages, announcements, email subjects, feature announcements)
for name in \
    push-notification-setup push-notification-campaign \
    push-notification-segmentation push-notification-health-monitor \
    feature-announcement announcement-health-monitor \
    in-app-message-health-monitor \
    email-subject-test-pipeline email-subject-performance-monitor; do
    [ -f "$DRILLS/product/$name.md" ] && move_drill "$DRILLS/product/$name.md" "messaging"
done

# EXPERIMENTATION (A/B testing, MVT, feature flags, personalization experiments, funnel optimization)
for name in \
    mvt-experiment-design mvt-results-analysis mvt-experiment-health-monitor \
    layout-variant-builder \
    flag-lifecycle-automation flag-rollout-health-monitor \
    feature-readiness-gating feature-adoption-monitor \
    funnel-drop-off-diagnosis funnel-optimization-health-monitor funnel-segment-scaling \
    session-recording-friction-analysis \
    struggle-signal-detection \
    ux-experiment-health-monitor \
    personalization-rule-engine personalization-scaling-pipeline personalization-health-monitor \
    segment-personalization-routing segment-drift-monitor \
    behavior-segmentation-pipeline user-behavior-segmentation \
    adoption-campaign-health-report adoption-campaign-segment-scaling; do
    [ -f "$DRILLS/product/$name.md" ] && move_drill "$DRILLS/product/$name.md" "experimentation"
done

# SUPPORT (proactive outreach, chatbot — some already moved to enablement, keep support-specific ones)
for name in \
    proactive-outreach-pipeline proactive-outreach-health-monitor; do
    [ -f "$DRILLS/product/$name.md" ] && move_drill "$DRILLS/product/$name.md" "support"
done

# Remaining product drills that didn't get categorized:
# deprecation-*, video-tutorial-*, collaboration-*, onboarding-call-*
for name in \
    deprecation-communication-setup deprecation-impact-assessment \
    deprecation-migration-tracker deprecation-segment-routing deprecation-health-monitor; do
    [ -f "$DRILLS/product/$name.md" ] && move_drill "$DRILLS/product/$name.md" "product-ops"
done

for name in \
    video-tutorial-personalization video-tutorial-engagement-tracking video-tutorial-health-monitor; do
    [ -f "$DRILLS/product/$name.md" ] && move_drill "$DRILLS/product/$name.md" "enablement"
done

for name in \
    collaboration-instrumentation collaboration-adoption-monitor collaboration-network-effects; do
    [ -f "$DRILLS/product/$name.md" ] && move_drill "$DRILLS/product/$name.md" "advocacy"
done

# --- SALES (125) -> split into capability categories ---

# DISCOVERY (all discovery calls, question banks, call preps)
for name in \
    bant-discovery-call meddic-discovery-call pain-discovery-call \
    need-discovery-call risk-discovery-call authority-discovery-call \
    timing-discovery-call competitive-discovery-call stakeholder-discovery-call \
    technical-discovery-call tech-stack-discovery \
    pain-discovery-call-prep risk-discovery-call-prep change-objection-call-prep \
    discovery-question-bank \
    call-brief-feedback-loop account-research-brief; do
    [ -f "$DRILLS/sales/$name.md" ] && move_drill "$DRILLS/sales/$name.md" "discovery"
done

# QUALIFICATION (scorecards, auto-scoring, reporting for BANT/MEDDIC/need/timing)
for name in \
    bant-scorecard-setup bant-auto-scoring bant-qualification-reporting \
    meddic-scorecard-setup meddic-auto-scoring meddic-qualification-reporting meddic-deal-health-monitor \
    need-scorecard-setup need-auto-scoring need-assessment-reporting \
    timing-scorecard-setup timing-auto-scoring timing-qualification-reporting \
    lead-score-model-setup lead-score-automation scoring-model-performance-monitor \
    change-readiness-scoring technical-fit-scoring; do
    [ -f "$DRILLS/sales/$name.md" ] && move_drill "$DRILLS/sales/$name.md" "qualification"
done

# DEMOS (demo prep, execution, follow-up, POC, sandbox)
for name in \
    demo-prep-automation demo-recap-assembly demo-follow-up-automation \
    demo-follow-up-cadence demo-follow-up-intelligence demo-performance-monitor \
    exec-demo-prep exec-demo-performance-monitor \
    story-matched-demo-prep technical-demo-content-assembly technical-proof-library \
    poc-scoping-workshop poc-governance-automation poc-health-monitoring \
    poc-intelligence-reporting \
    sandbox-auto-provisioning sandbox-provisioning-workflow \
    sandbox-usage-monitoring sandbox-intelligence-reporting; do
    [ -f "$DRILLS/sales/$name.md" ] && move_drill "$DRILLS/sales/$name.md" "demos"
done

# COMPETITIVE (battlecards, objection handling, win/loss, competitive intel)
for name in \
    competitive-battlecard-assembly competitive-detection-automation \
    competitive-intelligence-automation \
    competitive-intelligence-monitor competitive-objection-response \
    competitive-win-loss-reporting \
    objection-detection-automation objection-follow-up-sequence objection-intelligence-monitor \
    change-objection-extraction change-objection-response-automation change-objection-intelligence-monitor \
    timing-objection-detection-automation timing-objection-follow-up-sequence timing-objection-response \
    technical-objection-intelligence-monitor \
    budget-objection-response price-objection-response; do
    [ -f "$DRILLS/sales/$name.md" ] && move_drill "$DRILLS/sales/$name.md" "competitive"
done

# VALUE-ENGINEERING (business cases, ROI, success criteria, stories)
for name in \
    business-case-assembly business-case-effectiveness-monitor pain-based-business-case \
    roi-auto-generation roi-calculator-build roi-prediction-accuracy roi-skepticism-intelligence-monitor \
    success-criteria-workshop success-criteria-intelligence success-criteria-reporting \
    story-library-curation story-intelligence-reporting \
    technical-collateral-matching technical-gap-assessment technical-intelligence-monitor; do
    [ -f "$DRILLS/sales/$name.md" ] && move_drill "$DRILLS/sales/$name.md" "value-engineering"
done

# DEAL-MANAGEMENT (stakeholders, champions, pricing, negotiation, expansion, multi-year)
for name in \
    stakeholder-map-assembly stakeholder-engagement-orchestration \
    stakeholder-consensus-tracker stakeholder-intelligence-reporting \
    map-auto-generation map-template-creation map-milestone-tracking map-risk-scoring \
    champion-profiling champion-recruitment-sequence champion-enablement-delivery \
    champion-multi-thread-expansion champion-health-monitoring champion-program-reporting \
    pricing-proposal-assembly pricing-outcome-tracking pricing-intelligence-monitor \
    deal-negotiation-tracking deal-negotiation-intelligence-monitor deal-term-ab-testing \
    multi-year-deal-modeling multi-year-proposal-automation multi-year-pipeline-scaling \
    expansion-scoring-pipeline expansion-outreach-sequence expansion-signal-qualification \
    expansion-upsell-health-monitor \
    budget-detection-automation budget-follow-up-sequence budget-intelligence-monitor \
    authority-verification-reporting \
    pain-pattern-analysis pain-intelligence-reporting \
    risk-pattern-analysis risk-intelligence-monitor risk-mitigation-delivery \
    timing-intelligence-monitor \
    follow-up-ab-testing; do
    [ -f "$DRILLS/sales/$name.md" ] && move_drill "$DRILLS/sales/$name.md" "deal-management"
done

# --- MEASUREMENT (29) -> split between experimentation and analytics ---
# Experiment-related ones go to experimentation, monitoring/dashboard stay in measurement
for name in \
    experiment-hypothesis-design experiment-impact-reporting \
    experiment-learnings-database experiment-pipeline-automation \
    experiment-portfolio-health-monitor \
    holdout-group-setup holdout-integrity-monitor holdout-lift-measurement; do
    [ -f "$DRILLS/measurement/$name.md" ] && move_drill "$DRILLS/measurement/$name.md" "experimentation"
done

# The rest of measurement stays as "analytics"
for name in \
    ab-test-orchestrator autonomous-optimization dashboard-builder \
    posthog-gtm-events threshold-engine \
    analyst-briefing-monitor booking-conversion-monitor \
    breakup-reengagement-monitor brief-quality-monitor \
    champion-outbound-reporting devrel-performance-monitor \
    engagement-performance-reporting intent-signal-health-monitor \
    interactive-tool-performance-monitor newsletter-performance-monitor \
    report-performance-monitor research-effectiveness-monitor \
    social-content-performance-monitor stakeholder-engagement-scoring \
    stakeholder-intelligence-monitor value-asset-performance-monitor; do
    [ -f "$DRILLS/measurement/$name.md" ] && move_drill "$DRILLS/measurement/$name.md" "analytics"
done

# --- EVENTS (47) -> split into event subtypes ---
# Keep events/ but slim it down; move series-automation to operations
# Actually, events is reasonably sized at 47, and the sub-types are too small alone
# Let's split into events-live/ and events-virtual/ ? No, let's keep events unified.
# Events stays as-is. 47 is high but they are all genuinely event drills.

# --- OPERATIONS (10) stays as-is, good size ---
# --- OUTREACH (24) stays as-is, good size ---
# --- PROSPECTING (11) stays as-is, good size ---
# --- CONTENT (29) stays as-is, good size ---
# --- PARTNERSHIPS (24) stays as-is, good size ---
# --- PAID (32) stays as-is, good size ---
# --- COMMUNITY (13) stays as-is, good size ---
# --- SEO (14) stays as-is, good size ---
# --- RESEARCH (8) stays as-is ---
# Smaller categories stay as-is: podcast, sdk, github, marketplaces, partner-marketplaces,
# qa-platforms, directories, gifting, sms, direct-mail, chrome-web-store, influencer,
# media, docs, field, youtube, thought-leadership, awards

# ==============================================================
# STEP 3: Update category: fields in all moved drills
# ==============================================================
log "=== STEP 3: Update category fields ==="

update_cat_dir() {
    local cat="$1" cat_name="$2"
    if [ -d "$DRILLS/$cat" ]; then
        for f in "$DRILLS/$cat"/*.md; do
            [ -f "$f" ] && update_category "$f" "$cat_name"
        done
    fi
}

update_cat_dir "onboarding" "Onboarding"
update_cat_dir "retention" "Retention"
update_cat_dir "conversion" "Conversion"
update_cat_dir "advocacy" "Advocacy"
update_cat_dir "revenue-ops" "Revenue Ops"
update_cat_dir "enablement" "Enablement"
update_cat_dir "messaging" "Messaging"
update_cat_dir "experimentation" "Experimentation"
update_cat_dir "product-ops" "Product Ops"
update_cat_dir "support" "Support"
update_cat_dir "discovery" "Discovery"
update_cat_dir "qualification" "Qualification"
update_cat_dir "demos" "Demos"
update_cat_dir "competitive" "Competitive"
update_cat_dir "value-engineering" "Value Engineering"
update_cat_dir "deal-management" "Deal Management"
update_cat_dir "analytics" "Analytics"

# ==============================================================
# STEP 4: Clean up empty directories
# ==============================================================
log "=== STEP 4: Clean up empty directories ==="

for dir in "$DRILLS"/product "$DRILLS"/sales "$DRILLS"/measurement; do
    if [ -d "$dir" ]; then
        remaining=$(find "$dir" -name "*.md" | wc -l)
        if [ "$remaining" -eq 0 ]; then
            if [ -n "$DRY_RUN" ]; then
                echo "  WOULD REMOVE empty dir: $dir"
            else
                rmdir "$dir" 2>/dev/null || true
            fi
        else
            log "  $dir still has $remaining files"
        fi
    fi
done

log "=== Migration complete ==="

# Report final counts
log "=== Final drill distribution ==="
for dir in "$DRILLS"/*/; do
    count=$(find "$dir" -name "*.md" 2>/dev/null | wc -l)
    echo "  $(basename "$dir"): $count"
done | sort -t: -k2 -rn

