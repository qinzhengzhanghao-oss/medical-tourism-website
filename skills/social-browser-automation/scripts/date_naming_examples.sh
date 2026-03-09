#!/usr/bin/env bash
set -euo pipefail
DATE="${1:-$(date +%F)}"
echo "${DATE}_instagram_dentist_shortlist.csv"
echo "${DATE}_tiktok_dentist_shortlist.csv"
echo "${DATE}_social_dentist_summary.md"
