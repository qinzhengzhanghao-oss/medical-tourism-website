---
name: dentist-lead-sheet-manager
description: Build and maintain structured lead sheets for dental outreach. Use when converting Instagram or TikTok research into a spreadsheet or CSV; when standardizing fields for US dental prospects; when scoring fit, tracking follow-up status, and keeping outreach records for referral-partner prospecting.
---

# Dentist Lead Sheet Manager

Use this skill to turn raw social-platform research into a clean, comparable lead sheet for outreach and follow-up.

## Workflow

1. Normalize one row per target account.
2. Fill required identity, content, and fit columns.
3. Score the lead consistently.
4. Add outreach status fields.
5. Keep notes factual and brief.

## Required columns

### Identity
- platform
- username
- display_name
- profile_url
- bio_summary
- us_location
- language
- specialty
- age_signal
- follower_count_band
- contact_info
- website

### Content tags
- posts_treatment_cases
- posts_experience_sharing
- posts_dental_surgery
- posts_implant_or_artificial_teeth_price
- posts_before_after
- mentions_booking_or_reserve
- mentions_queue_or_waitlist

### Action tags
- selfie_explanation
- product_or_tool_display
- action_demo
- teeth_display
- surgery_action_display

### Business fit
- us_based
- english_speaking
- young_professional_brand
- likely_private_practice
- affordability_topic_present
- wait_time_topic_present
- cross_border_referral_fit
- referral_potential_score
- priority_level

### Outreach tracking
- followed
- commented
- dm_prepared
- dm_sent
- replied
- interested
- follow_up_needed
- last_contact_date
- next_action
- notes

## Sheet rules

- Use lowercase snake_case for headers.
- Keep booleans as yes/no.
- Keep scores numeric when possible.
- Keep notes evidence-based; avoid assumptions stated as facts.
- If a field is unknown, leave blank instead of guessing.

## Output formats

Prefer:
- CSV for portability
- XLSX when the user explicitly wants Excel
- Markdown table only for small previews

## Reference files

- Read `references/field-definitions.md` for field meanings.
- Use `assets/dentist_lead_sheet_template.csv` as the starter template.
