---
name: social-browser-automation
description: Plan and control browser-based social research workflows for Instagram and TikTok. Use when a task requires opening social websites, searching many pages, reviewing profiles, extracting structured account data, scoring leads, handling rate limits, and exporting results to CSV/XLSX. Use for browser research and controlled collection workflows, not for high-volume mass engagement.
---

# Social Browser Automation

Use this skill to structure browser-driven research on social platforms with careful pacing, data capture, and export rules.

## Core principles

- Prefer research and structured collection before any engagement.
- Work in batches.
- Log every reviewed account.
- Avoid fast repetitive actions.
- Expect login walls, captchas, and dynamic page changes.
- Keep extraction rules consistent across platforms.

## Workflow

1. Define the target profile and output fields.
2. Build platform-specific search terms.
3. Open search results in small batches.
4. Review profile-level evidence.
5. Review recent post/video evidence.
6. Score and classify the account.
7. Export qualified rows to the lead sheet.
8. Produce a summary of why the final shortlist was selected.

## Minimum data to extract

For each account collect:
- platform
- username
- display name
- profile URL
- bio summary
- location signal
- specialty signal
- content topics
- action signals
- pricing / booking / waitlist signals
- referral-fit score
- notes with evidence

## Batch rules

- Review 10-20 candidate accounts per batch.
- Re-rank after each batch.
- Stop and save progress after every batch.
- If the site slows, shows a login wall, or starts rate-limiting, pause instead of pushing harder.

## Output rules

- Save dated files.
- Prefer one master CSV/XLSX plus a short Markdown summary.
- Keep reasoning evidence-based.
- Mark uncertainty explicitly.

## Safety and quality

Do not assume claims from one post are representative of the whole account. Verify using multiple recent posts when possible.

## Reference files

- Read `references/research-playbook.md` for cross-platform workflow.
- Read `references/scoring-rubric.md` for lead scoring.
- Use `scripts/date_naming_examples.sh` for output naming examples.
