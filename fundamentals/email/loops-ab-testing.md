---
name: loops-ab-testing
description: Run A/B tests on email subject lines and content in Loops
tool: Loops
difficulty: Intermediate
---

# A/B Test Emails in Loops

## Prerequisites
- Loops audience large enough for statistical significance (minimum 500 contacts per variant)
- Baseline metrics from previous sends to compare against

## Steps

1. **Choose what to test.** Test one variable at a time. High-impact variables in order: Subject line (biggest impact on open rate), CTA text and placement (biggest impact on click rate), Send time (impacts open rate), Email length (impacts engagement). Never test multiple variables simultaneously -- you will not know what caused the difference.

2. **Create variants.** For subject line tests in broadcasts, create two versions of your email with different subject lines but identical body content. Make the variants meaningfully different -- "New Feature: AI Reports" vs "Your reports just got smarter" tests framing, not just word choice.

3. **Set the test split.** Send variant A to 25% of the segment and variant B to 25%. Hold the remaining 50% to receive the winning variant after results are in. This maximizes the impact of your test.

4. **Define your success metric.** Before launching, decide what wins: open rate (for subject line tests), click rate (for content tests), or reply rate (for sales-oriented emails). Write down your hypothesis: "I believe the question subject line will have 10% higher open rate than the statement."

5. **Wait for statistical significance.** Let the test run for 24-48 hours before declaring a winner. You need at least 100 opens per variant for a subject line test to be meaningful. Small differences (less than 5%) may not be statistically significant.

6. **Document and compound learnings.** Record every test result in a shared doc: what was tested, hypothesis, result, and takeaway. Over time, you build a library of proven patterns for your specific audience. Apply winning patterns to your automated sequences.
