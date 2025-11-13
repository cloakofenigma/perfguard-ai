# PerfGuard AI

GenAI-Driven Performance Model Suggestor for PRs. Automatically enforces performance standards on every code change.

## Features
- AI-powered test selection & benchmarking
- Single Performance Score (0-100)
- Blocks merges if score < 80
- React dashboard for trends

## Quick Start
1. Fork/clone this repo.
2. Add secrets: `ANTHROPIC_API_KEY` (Claude API).
3. Enable branch protection: Require "PerfGuard AI" check.
4. Open a PR → Watch it run!

## Tech Stack
- Python + pytest-benchmark + memory-profiler
- Claude 3.5 Sonnet (via Anthropic SDK)
- GitHub Actions
- React + Chart.js (dashboard)

## Usage
- Push to PR: Triggers workflow.
- Score posted as PR comment.
- Dashboard: `npm start` in `/dashboard`.
