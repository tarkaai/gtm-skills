#!/usr/bin/env python3
"""
Verify all references in the GTM Skills repo:
1. Every drill's fundamentals: list only contains slugs that exist in fundamentals/
2. Every play level's drills: list only contains slugs that exist in drills/
3. No fundamental has "click", "navigate to", or "go to" in its instructions
4. Count: how many play levels reference at least 1 drill
"""
import os, re, glob, sys

REPO = "/Users/dan/Projects/tarka/gtm-skills"
FUNDAMENTALS_DIR = os.path.join(REPO, "fundamentals")
DRILLS_DIR = os.path.join(REPO, "drills")
SKILLS_DIR = os.path.join(REPO, "skills")

errors = []
warnings = []

# Build valid slug sets
valid_fundamental_slugs = set()
for f in glob.glob(os.path.join(FUNDAMENTALS_DIR, "**/*.md"), recursive=True):
    slug = os.path.splitext(os.path.basename(f))[0]
    valid_fundamental_slugs.add(slug)

valid_drill_slugs = set()
for f in glob.glob(os.path.join(DRILLS_DIR, "**/*.md"), recursive=True):
    slug = os.path.splitext(os.path.basename(f))[0]
    valid_drill_slugs.add(slug)

print(f"Found {len(valid_fundamental_slugs)} fundamentals and {len(valid_drill_slugs)} drills\n")

# --- Check 1: Drill fundamental references ---
print("=" * 60)
print("CHECK 1: Drill fundamental references")
print("=" * 60)
drill_errors = 0
for f in glob.glob(os.path.join(DRILLS_DIR, "**/*.md"), recursive=True):
    with open(f, "r") as fh:
        content = fh.read()
    if not content.strip():
        continue
    
    # Extract fundamentals from frontmatter
    in_fundamentals = False
    for line in content.split("\n"):
        if line.strip() == "fundamentals:":
            in_fundamentals = True
            continue
        if in_fundamentals:
            if line.strip().startswith("- "):
                slug = line.strip()[2:].strip()
                if slug not in valid_fundamental_slugs:
                    drill_name = os.path.splitext(os.path.basename(f))[0]
                    errors.append(f"Drill '{drill_name}' references non-existent fundamental '{slug}'")
                    drill_errors += 1
            elif line.strip() and not line.startswith(" "):
                in_fundamentals = False

if drill_errors == 0:
    print("PASS: All drill fundamental references are valid")
else:
    print(f"FAIL: {drill_errors} invalid fundamental references in drills")

# --- Check 2: Play drill references ---
print("\n" + "=" * 60)
print("CHECK 2: Play drill references")
print("=" * 60)
play_errors = 0
play_files_with_drills = 0
play_files_total = 0
for f in glob.glob(os.path.join(SKILLS_DIR, "**/*.md"), recursive=True):
    with open(f, "r") as fh:
        content = fh.read()
    if not content.strip():
        continue
    
    play_files_total += 1
    has_drills = False
    in_drills = False
    for line in content.split("\n"):
        if line.strip() == "drills:":
            in_drills = True
            continue
        if in_drills:
            if line.strip().startswith("- "):
                slug = line.strip()[2:].strip()
                has_drills = True
                if slug not in valid_drill_slugs:
                    play_name = os.path.relpath(f, SKILLS_DIR)
                    errors.append(f"Play '{play_name}' references non-existent drill '{slug}'")
                    play_errors += 1
            elif line.strip() and not line.startswith(" "):
                in_drills = False
    
    if has_drills:
        play_files_with_drills += 1

if play_errors == 0:
    print("PASS: All play drill references are valid")
else:
    print(f"FAIL: {play_errors} invalid drill references in plays")
print(f"  {play_files_with_drills} of {play_files_total} play files reference at least 1 drill")

# --- Check 3: Agent-hostile language in fundamentals ---
print("\n" + "=" * 60)
print("CHECK 3: Agent-hostile language in fundamentals")
print("=" * 60)
hostile_patterns = [
    (r"(?i)navigate to", "navigate to"),
    (r"(?i)click on\b", "click on"),
    (r"(?i)click '", "click '"),
    (r"(?i)\bgo to (?!your|the API|the PostHog|cal\.com|a )", "go to (UI navigation)"),
]
hostile_count = 0
for f in glob.glob(os.path.join(FUNDAMENTALS_DIR, "**/*.md"), recursive=True):
    with open(f, "r") as fh:
        content = fh.read()
    
    # Skip frontmatter
    parts = content.split("---", 2)
    if len(parts) >= 3:
        body = parts[2]
    else:
        body = content
    
    fname = os.path.relpath(f, FUNDAMENTALS_DIR)
    for pattern, label in hostile_patterns:
        matches = re.findall(pattern, body)
        if matches:
            for m in matches:
                warnings.append(f"Fundamental '{fname}' contains agent-hostile language: '{m}'")
                hostile_count += 1

if hostile_count == 0:
    print("PASS: No agent-hostile language found in fundamentals")
else:
    print(f"WARNING: {hostile_count} instances of potentially agent-hostile language")
    for w in warnings[:10]:
        print(f"  - {w}")
    if len(warnings) > 10:
        print(f"  ... and {len(warnings) - 10} more")

# --- Summary ---
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Fundamentals: {len(valid_fundamental_slugs)}")
print(f"Drills: {len(valid_drill_slugs)}")
print(f"Play files total: {play_files_total}")
print(f"Play files with drill references: {play_files_with_drills} ({play_files_with_drills*100//play_files_total}%)")
print(f"Errors: {len(errors)}")
print(f"Warnings: {len(warnings)}")

if errors:
    print("\nERRORS:")
    for e in errors:
        print(f"  - {e}")

sys.exit(1 if errors else 0)
