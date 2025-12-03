# 🚀 PerfGuard AI

[![GitHub Actions](https://github.com/cloakofenigma/perfguard-ai/workflows/PerfGuard%20AI/badge.svg)](https://github.com/cloakofenigma/perfguard-ai/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **GenAI-Powered Performance Gatekeeper for Pull Requests**

Stop slow code from reaching production. PerfGuard AI automatically analyzes every Pull Request for performance issues, gives a single score (0–100), and blocks merge if the score is too low.

---

## 🎯 What is PerfGuard AI?

PerfGuard AI is a CI/CD-integrated, GenAI-powered code quality gate that:

- ✨ **Auto-generates** performance benchmarks per PR
- 🧠 **AI-powered** smart test selection using Google Gemini 2.5 Pro
- 📊 **Three-score tracking** (Previous, Current, New Code) for detailed analysis
- 🚫 **Blocks merge** if score < threshold
- ⚡ **Fully automated** in GitHub Actions
- 📱 **Interactive Dashboard** with auto-refresh and score improvement recommendations
- 🎬 **Production-ready** with sample application included
- 🛡️ **Reliable** with robust error handling and Unicode-safe processing
- 🎯 **Application-focused** analyzes only your app code, not the tool itself (configurable via `APPLICATION_PATH`)

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Application Scope](#-application-scope)
- [Sample Application](#-sample-application)
- [Interactive Dashboard](#-interactive-dashboard)
- [Performance Metrics](#-performance-metrics)
- [Scoring System](#-scoring-system)
- [Configuration](#%EF%B8%8F-configuration)
- [Usage](#-usage)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)
- [Performance Best Practices](#-performance-best-practices)
- [Security](#-security)
- [Recent Updates](#-recent-updates)
- [Resources](#-resources)
- [Contributing](#-contributing)

---

## ✨ Features

### Core Capabilities
- **AI-Driven Analysis**: Powered by Google Gemini 2.5 Pro for intelligent performance predictions
- **Three-Score Tracking**: Displays Previous, Current, and New Code scores for comprehensive analysis
- **Comprehensive Metrics**: Tracks 6 key performance indicators with real-time monitoring
- **Baseline Comparison**: Automatically establishes and compares against baselines
- **Smart Test Selection**: AI suggests which tests to run based on code changes
- **Automated Reporting**: Generates detailed markdown reports with actionable insights
- **GitHub Integration**: Seamless CI/CD workflow with PR comments and status checks
- **Interactive Dashboard**: Real-time React dashboard with auto-refresh and score improvement recommendations
- **Robust Error Handling**: Unicode-safe processing with comprehensive sanitization

### Performance Metrics Tracked
1. **Execution Time (30%)** - P95 latency, +15% threshold
2. **Memory RSS (20%)** - Peak memory usage, +20% threshold
3. **CPU Utilization (15%)** - Average CPU during tests, +25% threshold
4. **I/O Latency (15%)** - Database/network operations, +30% threshold
5. **Code Complexity (10%)** - Cyclomatic complexity delta, +2 threshold
6. **AI Risk Score (10%)** - GenAI-predicted performance risk

---

## 🏗️ Architecture

```
perfguard-ai/
├── perfguard/               # Core AI engine
│   ├── main.py             # Main orchestration & three-score tracking
│   ├── ai_analyzer.py      # Google Gemini 2.5 Pro integration
│   ├── metrics_collector.py # Performance measurement
│   ├── rules_engine.py     # Scoring calculation
│   ├── storage.py          # Baseline management
│   ├── config.py           # Configuration
│   ├── logger.py           # Structured logging
│   └── prompts.py          # AI prompts
├── sample-app/              # Demo movie application
│   ├── app.py              # Flask web app (15 movies)
│   ├── movies_data.py      # Movie database
│   ├── slow_function.py    # Intentionally slow code
│   ├── templates/          # HTML templates
│   │   ├── index.html      # Movie listing page
│   │   └── movie_detail.html # Movie details page
│   ├── static/             # CSS, JS, images
│   │   ├── css/            # Stylesheets
│   │   └── images/         # Movie posters
│   └── tests/              # Performance tests
│       └── test_perf.py    # pytest benchmarks
├── dashboard/               # React dashboard (auto-refresh)
│   ├── public/             # Static assets
│   │   └── report.json     # Performance data
│   └── src/                # Dashboard components
│       ├── App.js          # Main app (30s auto-refresh)
│       └── components/
│           ├── ScoreCard.js           # Overall score display
│           ├── MetricsCard.js         # 6 metrics breakdown
│           ├── AIAnalysisCard.js      # AI insights
│           ├── RecommendationsCard.js # Score improvement tips
│           ├── PRScoreChart.js        # Score history chart
│           └── Dashboard.js           # Main layout
├── .github/workflows/       # CI/CD pipelines
│   └── perfguard.yml       # Main workflow (analysis + dashboard deployment)
├── requirements.txt         # Python dependencies
├── pytest.ini              # Test configuration
├── perfguard_score.json    # Latest performance results
├── perfguard_report.md     # Detailed analysis report
└── README.md               # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+ (for dashboard)
- Git
- **Google API Key** (required):
  - Google API key for Gemini 2.5 Pro
- GitHub repository

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/cloakofenigma/perfguard-ai.git
cd perfguard-ai
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install dashboard dependencies**
```bash
cd dashboard
npm install
cd ..
```

4. **Set up environment variables**
```bash
# Google Gemini API key (required)
export GOOGLE_API_KEY="your-google-api-key-here"

# GitHub token (optional, for PR comments)
export GH_TOKEN="ghp-your-github-token"
```

5. **Configure GitHub Actions**

Add secrets to your repository:
- Go to Settings → Secrets and variables → Actions
- Add `GOOGLE_API_KEY` with your Google Gemini API key (required)
- GitHub token is automatically available as `GITHUB_TOKEN`

6. **Enable GitHub Pages (for dashboard)**
- Settings → Pages → Source: **Deploy from a branch**
- Branch: **gh-pages** / **(root)**
- Click **Save**
- Dashboard will auto-deploy via perfguard.yml workflow
- Note: The workflow uses peaceiris/actions-gh-pages@v3 to deploy to gh-pages branch

7. **Enable branch protection**
- Settings → Branches → Add rule
- Require status checks: "PerfGuard AI"

### 🚀 Quick Demo (2 minutes)

Want to see it in action immediately? Here's the fastest way:

**Option 1: Complete Automated Flow (Recommended)**
```bash
# 1. Clone and setup (30 seconds)
git clone https://github.com/cloakofenigma/perfguard-ai.git
cd perfguard-ai
pip install -r requirements.txt

# 2. Set API key (10 seconds)
export GOOGLE_API_KEY="your-google-api-key"

# 3. Run complete flow (90 seconds)
./perfguard_complete.sh
# Select option 1 for Full Flow (Analysis + Verify + Dashboard)
```

**Option 2: Step-by-Step**
```bash
# 1. Clone and setup
git clone https://github.com/cloakofenigma/perfguard-ai.git
cd perfguard-ai
pip install -r requirements.txt

# 2. Set API key
export GOOGLE_API_KEY="your-google-api-key"

# 3. Run verification (runs analysis + verifies output)
./verify_dashboard.sh

# 4. Start dashboard
./start_dashboard.sh
# Opens at http://localhost:3000
```

**What You'll See:**
- ✅ Three performance scores (Previous, Current, New Code) with verdict
- 📊 6 metrics analyzed (execution, memory, CPU, I/O, complexity, AI risk)
- 🤖 AI insights from Google Gemini 2.5 Pro
- 💡 Recommendations to improve your score
- 🔍 Browser console logs with `[PerfGuard]` prefix for debugging
- 📡 Server terminal logs with `[Proxy]` prefix for request monitoring

---

## 🎯 Application Scope

**IMPORTANT:** PerfGuard AI analyzes **only your application code**, not the PerfGuard tool itself.

### Current Configuration

```python
# In perfguard/config.py
APPLICATION_PATH = "sample-app"  # Only analyze this directory
```

### Why This Matters

✅ **With Scoping (Current Behavior):**
- Analyzes only files in `sample-app/` directory
- Changes to `perfguard/` or `dashboard/` are **ignored**
- Accurate results focused on your application
- No polluted metrics from tool code

❌ **Without Scoping (Old Behavior):**
- Would analyze entire repository including tool code
- Misleading scores mixing app and tool performance
- Confusing results irrelevant to your application

### What Gets Analyzed

```bash
# When you edit sample-app files
git add sample-app/app.py
git commit -m "Optimize movie search"
python perfguard/main.py
# ✅ Analyzes: sample-app/app.py changes

# When you edit PerfGuard tool files
git add perfguard/ai_analyzer.py
git commit -m "Update tool"
python perfguard/main.py
# ✅ Result: "No changes detected in sample-app/"
```

### Changing the Application Path

To analyze a different application, edit `perfguard/config.py`:

```python
# Example: Analyze your own API
APPLICATION_PATH = "my-api/src"

# Example: Analyze a web app
APPLICATION_PATH = "frontend"

# Example: Analyze a microservice
APPLICATION_PATH = "services/user-service"
```

**See [APPLICATION_SCOPE.md](APPLICATION_SCOPE.md) for detailed documentation.**

---

## 🎬 Sample Application

PerfGuard AI includes a fully-functional movie browsing application (IMDB-style) to demonstrate its capabilities.

### Running the Sample App

```bash
cd sample-app
python app.py
```

Visit `http://localhost:5000` to explore:
- **15 curated movies** with detailed information:
  - The Shawshank Redemption, The Godfather, The Dark Knight
  - Pulp Fiction, Forrest Gump, Inception
  - Fight Club, The Matrix, Goodfellas
  - The Silence of the Lambs, Interstellar, Saving Private Ryan
  - The Green Mile, Se7en, The Prestige
- **Responsive design** that works on all devices
- **Search functionality** and filters
- **Movie detail pages** with cast, crew, and plot
- **Beautiful UI** with movie posters and ratings

### Testing Performance

```bash
# Run performance tests
pytest tests/test_perf.py -m perf --benchmark-only

# Run with PerfGuard AI
cd ..
python perfguard/main.py
```

### Intentional Performance Issues

The sample app includes `slow_function.py` with common performance anti-patterns:
- **N+1 queries** - Inefficient database access
- **Memory leaks** - Unnecessary data retention
- **O(n³) algorithms** - Complex nested loops
- **String concatenation** - Inefficient string building

These demonstrate how PerfGuard AI detects and reports performance issues.

---

## 📊 Interactive Dashboard

PerfGuard AI includes a modern React dashboard with real-time monitoring and actionable insights.

### Dashboard Features

- **🔄 Auto-Refresh**: Automatically updates every 30 seconds with latest performance data
- **📈 Three-Score Display**: Visual comparison of Previous, Current, and New Code scores with trend indicators
- **📊 Metrics Breakdown**: Detailed view of all 6 performance metrics with trend indicators
- **🤖 AI Analysis**: Google Gemini 2.5 Pro insights on performance risks and critical paths
- **💡 Smart Recommendations**: Actionable suggestions to improve your score, with severity levels and impact estimates
- **📉 Score History**: Track performance trends over time with baseline comparison

### Running the Dashboard

```bash
# Development mode
cd dashboard
npm start
# Opens at http://localhost:3000

# Production build
npm run build
npm install -g serve
serve -s build
```

### Live Dashboard

After deploying to GitHub Pages, your dashboard will be available at:
```
https://[your-username].github.io/perfguard-ai/
```

### How Dashboard Deployment Works

**Automatic Deployment:**
- Dashboard builds and deploys automatically via perfguard.yml workflow
- Triggered on every PR and push to main in sample-app directory
- Uses peaceiris/actions-gh-pages@v3 action
- Deploys to gh-pages branch (force orphan - clean slate each time)
- GitHub Pages serves from gh-pages branch

**Deployment Flow:**
1. PerfGuard analysis runs and generates report.json
2. Dashboard React app builds with report.json included
3. Build artifacts copied to gh-pages branch
4. GitHub Pages picks up changes and serves updated dashboard
5. Available at: https://[username].github.io/perfguard-ai/

**Key Configuration:**
- **package.json**: `"homepage": "https://[username].github.io/perfguard-ai"`
- **App.js**: Uses `process.env.PUBLIC_URL` for asset paths
- **perfguard.yml**: Deploys to gh-pages branch on every run
- **GitHub Pages**: Configured to serve from gh-pages branch

### Dashboard Components

1. **Score Card** - Overall performance score (0-100) with color-coded verdict
   - 🟢 EXCELLENT (90-100): Ready to merge
   - 🟢 PASS (80-89): Approved for merge
   - 🟡 WARNING (70-79): Review recommended
   - 🔴 BLOCKED (0-69): Merge blocked

2. **Metrics Card** - Detailed breakdown of all 6 metrics:
   - Execution Time, Memory RSS, CPU Utilization
   - I/O Latency, Code Complexity, AI Risk Score
   - Shows current vs baseline with change percentage

3. **AI Analysis Card** - GenAI-powered insights:
   - Risk assessment and critical paths
   - Performance hotspot detection
   - Actionable recommendations

4. **Recommendations Card** - Score improvement guide:
   - Severity-based prioritization (Critical → Low)
   - Estimated point impact for each fix
   - Specific commands and code changes
   - Quick actions for common optimizations

### Updating Dashboard Data

The dashboard automatically displays data from `perfguard_score.json`. To manually update:

```bash
# Run PerfGuard analysis
python perfguard/main.py

# Copy results to dashboard
cp perfguard_score.json dashboard/public/report.json

# Refresh dashboard - auto-refresh will pick it up within 30 seconds
# Or click the "Refresh" button for immediate update
```

---

## 📊 Performance Metrics

### 1. Execution Time (Weight: 30%)
Measures P95 latency using `pytest-benchmark`.

**Threshold**: +15% from baseline

```python
@pytest.mark.perf
def test_api_performance(benchmark):
    result = benchmark(api_call)
    assert result.status_code == 200
```

### 2. Memory RSS (Weight: 20%)
Tracks peak memory usage with `memory-profiler`.

**Threshold**: +20% from baseline

### 3. CPU Utilization (Weight: 15%)
Monitors CPU usage during test execution.

**Threshold**: +25% from baseline

### 4. I/O Latency (Weight: 15%)
Measures database and network operation latency.

**Threshold**: +30% from baseline

### 5. Code Complexity (Weight: 10%)
Analyzes cyclomatic complexity with `radon`.

**Threshold**: +2 complexity points

### 6. AI Risk Score (Weight: 10%)
Claude AI predicts performance risks from code changes.

**Threshold**: >0.6 = high risk

---

## 🎯 Scoring System

### Score Calculation

```python
final_score = (
    30% × execution_time_score +
    20% × memory_score +
    15% × cpu_score +
    15% × io_score +
    10% × complexity_score +
    10% × ai_risk_score
)
```

### Score Interpretation

| Score | Verdict | Action |
|-------|---------|--------|
| 90-100 | EXCELLENT | ✅ Merge approved |
| 80-89 | PASS | ✅ Merge approved |
| 70-79 | WARNING | ⚠️ Review recommended |
| 0-69 | BLOCKED | 🚫 Merge blocked |

### Threshold Configuration

Default: **80/100** (configurable in `config.py`)

---

## ⚙️ Configuration

### Environment Variables

```bash
# AI API Key (required)
GOOGLE_API_KEY="..."            # Google Gemini 2.5 Pro

# Optional
GH_TOKEN="ghp_..."              # GitHub token for PR comments
PERFGUARD_ENV="production"      # or "development"
```

### LLM Configuration

PerfGuard AI uses Google Gemini 2.5 Pro for AI-powered analysis:

- **Model**: Google Gemini 2.5 Pro (`gemini-2.5-pro`)
- **Purpose**: Intelligent performance risk prediction and code analysis
- **Features**: Advanced code understanding, performance impact assessment, actionable recommendations

### Config File (`perfguard/config.py`)

```python
# LLM Configuration
GEMINI_MODEL = "gemini-2.5-pro"  # Google's latest model
MAX_TOKENS = 2048

# Performance thresholds
THRESHOLDS = {
    "execution_time": 0.15,    # +15%
    "memory_rss": 0.20,         # +20%
    "cpu_utilization": 0.25,    # +25%
    "io_latency": 0.30,         # +30%
    "complexity_delta": 2,      # +2 points
    "ai_risk_threshold": 0.6    # 0-1 scale
}

# Scoring weights (must sum to 100)
WEIGHTS = {
    "execution_time": 30,
    "memory_rss": 20,
    "cpu_utilization": 15,
    "io_latency": 15,
    "complexity": 10,
    "ai_risk": 10
}

# Passing score
MIN_PASSING_SCORE = 80

# Retry Configuration
API_RETRY_ATTEMPTS = 3
API_RETRY_DELAY = 2  # seconds
API_TIMEOUT = 30  # seconds
```

---

## 💻 Usage

### Complete Workflow (Automated)

**🎯 Master Script** - Menu-driven interface for all operations:
```bash
export GOOGLE_API_KEY="your-api-key"
./perfguard_complete.sh

# Options:
# 1) Run Analysis + Verify + Start Dashboard (Full Flow)
# 2) Run Analysis Only
# 3) Verify Existing Reports
# 4) Start Dashboard (requires existing report)
# 5) Clean All Reports and Start Fresh
```

### Local Testing

**Option 1: Full Verification Flow (Recommended)**
```bash
export GOOGLE_API_KEY="your-api-key"

# Run complete verification (cleans old reports, runs analysis, verifies)
./verify_dashboard.sh

# Start dashboard with pre-flight checks
./start_dashboard.sh
```

**Option 2: Manual Steps**
```bash
# Run PerfGuard on current changes
export GOOGLE_API_KEY="your-api-key"
python perfguard/main.py

# Files are automatically saved to both:
#   - perfguard_score.json (root)
#   - dashboard/public/report.json (dashboard)

# View results in terminal
cat perfguard_report.md

# Start dashboard
cd dashboard && npm start
```

### Dashboard Usage

```bash
# Quick start (recommended - checks if report exists first)
./start_dashboard.sh

# Or manual start
cd dashboard
npm start

# Features:
# - Auto-refresh enabled by default (30s interval)
# - Manual refresh button for immediate updates
# - Toggle auto-refresh on/off as needed
# - View at: http://localhost:3000
# - Browser console shows [PerfGuard] logs
# - Server terminal shows [Proxy] logs
```

### Debugging

**Browser Console (F12):**
```
[PerfGuard] Fetching report.json...
[PerfGuard] Response status: 200
[PerfGuard] Report data loaded: {previous_score: 66.2, current_score: 79.3, ...}
[PerfGuard] Dashboard updated successfully!
```

**Server Terminal:**
```
[Proxy] Request for /report.json
[Proxy] File found, size: 3656 bytes
[Proxy] Serving scores: { previous: 66.2, current: 79.3, delta: 76.0 }
```

**Troubleshooting:**
```bash
# Verify everything is working
./verify_dashboard.sh

# Check current scores
jq '{previous_score, current_score, delta_score}' dashboard/public/report.json

# Clean and restart
rm -f dashboard/public/report.json perfguard_score.json
python perfguard/main.py
./start_dashboard.sh
```

### In Pull Requests

1. Create a branch with changes
2. Open a pull request
3. PerfGuard AI runs automatically via GitHub Actions
4. Review the PR comment with performance report
5. Check the dashboard for detailed insights
6. Fix issues if score < 80 (use recommendations card)
7. Merge when score is ≥80 and approved

### Manual Test Execution

```bash
# Run all performance tests
pytest -m perf

# Run specific test
pytest sample-app/tests/test_perf.py::test_api_performance -v

# With benchmarking
pytest -m perf --benchmark-only

# Update dashboard with results (automatic save to both locations)
python perfguard/main.py
# Files saved to:
#   - perfguard_score.json (root)
#   - dashboard/public/report.json (dashboard)
```

### CI/CD Integration

PerfGuard automatically runs on:
- Pull requests (opened, synchronized, reopened) - only for sample-app/** changes
- Pushes to main branch - only for sample-app/** changes
- Manual workflow dispatch

Results are:
- Posted as PR comments with detailed analysis
- Uploaded as artifacts (30-day retention)
- **Dashboard deployed to gh-pages branch on EVERY run (including PRs)**
- Dashboard accessible at: https://[username].github.io/perfguard-ai/
- Workflow status used for merge blocking (score < 80)
- Both report.json and baseline_score.json deployed automatically

---

## 🛠️ Development

### Project Structure

```
perfguard/
├── main.py              # Entry point
├── ai_analyzer.py       # AI integration (retry logic, error handling)
├── metrics_collector.py # Metrics collection (all 6 metrics)
├── rules_engine.py      # Score calculation
├── storage.py           # Baseline management
├── config.py            # Centralized config
├── logger.py            # Structured logging
└── prompts.py           # AI prompt templates
```

### Adding New Metrics

1. Update `config.py` with new metric
2. Add collection logic in `metrics_collector.py`
3. Update scoring in `rules_engine.py`
4. Adjust weights to sum to 100

### Testing Locally

```bash
# Install dev dependencies
pip install pytest pytest-flask pytest-benchmark

# Run unit tests
pytest tests/

# Run with coverage
pytest --cov=perfguard tests/
```

### Code Quality

```bash
# Format code
black perfguard/ sample-app/

# Lint code
ruff check perfguard/

# Security scan
bandit -r perfguard/

# Dependency audit
safety check
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "No changes detected"
**Cause**: No git diff found
**Solution**: Ensure you have committed changes or use proper base branch

#### 2. API Key Issues
**Problem**: "ANTHROPIC_API_KEY not set" or API rate limits
**Solution**:
- Ensure at least one API key is set (Anthropic or Google)
- Add both keys for automatic fallback
- Check API credits/quotas
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="..."  # Fallback
```

#### 3. "Benchmark results not found"
**Cause**: No tests with `@pytest.mark.perf`
**Solution**: Add performance test markers to your test functions
```python
@pytest.mark.perf
def test_performance(benchmark):
    result = benchmark(function_to_test)
```

#### 4. "Score always 100"
**Cause**: No baseline established
**Solution**: Run tests once to create baseline
```bash
python perfguard/main.py  # Creates perfguard_baselines.json
```

#### 5. Dashboard Not Updating
**Cause**: Stale data or missing report.json
**Solution**:
```bash
# Copy latest results
cp perfguard_score.json dashboard/public/report.json

# Check auto-refresh is enabled (should update within 30s)
# Or click the manual refresh button

# Clear browser cache if needed
Ctrl+Shift+R (Chrome/Firefox)
```

#### 6. Unicode/Encoding Errors
**Problem**: "'ascii' codec can't encode character"
**Solution**: Already handled! The system automatically sanitizes all text to ASCII-safe format. If you encounter this, it's a bug - please report it.

#### 7. "Import errors" or "Module not found"
**Cause**: Missing dependencies
**Solution**:
```bash
pip install -r requirements.txt  # Python deps
cd dashboard && npm install      # Dashboard deps
```

#### 8. Dashboard Build Fails
**Problem**: npm build errors
**Solution**:
```bash
cd dashboard
rm -rf node_modules package-lock.json
npm install
npm run build
```

#### 9. GitHub Actions Failing
**Problem**: Workflow errors
**Solution**:
- Check secrets are properly set (ANTHROPIC_API_KEY, GOOGLE_API_KEY)
- Verify GitHub Pages is enabled
- Check workflow logs for specific errors
- Ensure branch protection is configured correctly

#### 10. Dashboard Shows "Report Load Failed: HTTP 404"
**Problem**: Dashboard can't find report.json despite file existing
**Root Cause**: Incorrect path configuration for GitHub Pages deployment

**Solution:**
1. Verify PUBLIC_URL is used in App.js:
   ```javascript
   const url = `${process.env.PUBLIC_URL}/report.json?t=${Date.now()}`;
   ```
2. Check package.json has correct homepage:
   ```json
   "homepage": "https://[username].github.io/perfguard-ai"
   ```
3. Clear browser cache completely (Ctrl+Shift+Delete → All Time)
4. Wait 5-10 minutes for CDN propagation after new deployment
5. Verify file exists: `curl https://[username].github.io/perfguard-ai/report.json`

**Note**: If you see this error on a fresh browser, check that:
- GitHub Pages is set to gh-pages branch (not GitHub Actions)
- Latest workflow completed successfully
- No github-pages environment exists (check Settings → Environments)

### Debug Mode

```bash
# Enable verbose logging
export PERFGUARD_ENV=development

# Run with Python debugger
python -m pdb perfguard/main.py
```

### Logs

```bash
# View GitHub Actions logs
# Go to Actions → Latest run → PerfGuard AI → View logs

# Local logs
python perfguard/main.py 2>&1 | tee perfguard.log
```

---

## 📈 Performance Best Practices

### DO ✅
- Tag performance-critical tests with `@pytest.mark.perf`
- Establish baselines before making comparisons
- Review AI suggestions carefully
- Fix high-risk issues first
- Monitor trends over time

### DON'T ❌
- Don't ignore WARNING verdicts
- Don't bypass checks without review
- Don't set thresholds too loose
- Don't skip security scans
- Don't commit sensitive data

---

## 🔐 Security

### API Keys
- **Never** commit API keys to git
- Use GitHub Secrets for CI/CD
- Rotate keys regularly
- Use environment-specific keys

### Sanitization
- All AI outputs are sanitized before display
- Input validation on user data
- No script injection in reports

### Dependency Security
```bash
# Check for vulnerabilities
safety check

# Security audit
bandit -r perfguard/
```

---

## 🎉 Recent Updates

### Version 3.1 Features (Latest - December 2025)

#### GitHub Pages Deployment Fix
- **PUBLIC_URL Path Resolution**: Fixed report.json loading on GitHub Pages
  - Changed from absolute path `/report.json` to `${process.env.PUBLIC_URL}/report.json`
  - Resolves to `/perfguard-ai/report.json` on GitHub Pages
  - Works correctly in both local dev and production
- **Simplified Workflow**: Removed conflicting deploy-dashboard.yml
  - Single workflow (perfguard.yml) handles both analysis and dashboard deployment
  - Uses peaceiris/actions-gh-pages@v3 for reliable gh-pages branch deployment
- **Environment Cleanup**: Removed github-pages environment to prevent deployment conflicts
  - GitHub Pages now correctly uses gh-pages branch (legacy mode)
  - No more README.md showing instead of dashboard

### Version 3.0 Features (November 2025)

#### Gemini-Only Architecture
- **Simplified LLM Stack**: Removed Anthropic dependency, using only Google Gemini 2.5 Pro
- **Enhanced Safety Settings**: Configured BLOCK_NONE for all categories to enable code analysis
- **Finish Reason Handling**: Robust handling of API completion states
- **Smart Diff Truncation**: Reduces 55MB+ diffs to ~5KB of meaningful changes
- **Optimized Git Diff**: Using `--no-color`, `--no-ext-diff`, `--unified=2` flags

#### Three-Score Tracking System
- **Previous Score**: Overall app performance before code changes
- **Current Score**: Overall app performance after code changes
- **Delta Score**: Performance score specifically for new code changes
- **Baseline Persistence**: Automatic storage in `dashboard/public/baseline_score.json`
- **AI-Powered Delta Calculation**: Considers risk score, critical paths, and file count

#### Automatic File Management
- **Dual-Location Saves**: Outputs automatically saved to both:
  - `perfguard_score.json` (root directory for backward compatibility)
  - `dashboard/public/report.json` (dashboard consumption)
- **No Manual Copy-Paste**: Eliminates need for `cp` commands
- **GitHub Actions Compatible**: Works seamlessly in CI/CD environments

#### Dashboard Reliability Enhancements
- **Custom Proxy Server**: `setupProxy.js` for reliable JSON serving with proper headers
- **Client-Side Logging**: `[PerfGuard]` prefix logs in browser console
- **Server-Side Logging**: `[Proxy]` prefix logs in terminal
- **Enhanced Error Handling**: No fallback to mock data - shows real errors with troubleshooting steps
- **Aggressive Cache-Busting**: Both client-side (query params) and server-side (headers)
- **Enriched Metrics**: Metrics object now includes score fields for all categories

#### Automation Scripts
- **`perfguard_complete.sh`**: Master menu-driven script with 5 workflow options
- **`verify_dashboard.sh`**: Complete 10-step verification (clean → analyze → verify → compare)
- **`start_dashboard.sh`**: Quick dashboard startup with pre-flight checks
- **Comprehensive Documentation**: `DASHBOARD_FIX_COMPLETE.md` with debugging guide

### Version 2.0 Features (Previous)

#### Interactive Dashboard Features
- **Auto-Refresh**: Updates every 30 seconds automatically
- **Manual Refresh**: Instant update button
- **Last Updated Indicator**: Shows when data was last fetched
- **Recommendations Card**: Actionable score improvement tips with severity levels
  - Critical, High, Medium, Low prioritization
  - Estimated point impact for each fix
  - Specific commands and code examples

#### Reliability Features
- **Unicode Sanitization**: Comprehensive ASCII-only text processing
- **Error Recovery**: Graceful handling of API failures
- **Retry Logic**: Configurable retry attempts with exponential backoff
- **Better Logging**: Structured logging with sanitized output

#### CI/CD Features
- **GitHub Pages Deployment**: Automatic dashboard deployment workflow
- **Artifact Management**: 30-day retention for performance results
- **Better PR Comments**: Updated or created intelligently
- **Score Thresholds**: Configurable pass/fail criteria

### What's Next

- Historical trend analysis with charts
- Performance regression detection
- Custom metric plugins
- Slack/Teams notifications
- Multi-repository support

---

## 📚 Resources

- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [pytest-benchmark Guide](https://pytest-benchmark.readthedocs.io/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [React Documentation](https://react.dev/)
- [Performance Testing Best Practices](https://martinfowler.com/articles/performance-testing.html)
- [PerfGuard AI Dashboard Fix Guide](DASHBOARD_FIX_COMPLETE.md)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

---

## 👥 Authors

- **Your Name** - *Initial work* - [cloakofenigma](https://github.com/cloakofenigma)

---

## 🙏 Acknowledgments

- Anthropic for Claude AI
- pytest-benchmark team
- Open source community

---

## 📞 Support

- 🐛 [Report a bug](https://github.com/cloakofenigma/perfguard-ai/issues)
- 💡 [Request a feature](https://github.com/cloakofenigma/perfguard-ai/issues)
- 💬 [Discussions](https://github.com/cloakofenigma/perfguard-ai/discussions)
- 📖 [Documentation](https://github.com/cloakofenigma/perfguard-ai/wiki)

### FAQ

**Q: Which AI provider should I use?**
A: Google Gemini 2.5 Pro is the primary and only LLM used. Simplified architecture with robust error handling.

**Q: How much do API calls cost?**
A: Minimal. Each analysis uses ~2K tokens (~$0.01 per run with Claude, even less with Gemini).

**Q: Can I use this with private repositories?**
A: Yes! GitHub Actions secrets keep your API keys secure.

**Q: Does it work with monorepos?**
A: Yes, PerfGuard analyzes the entire repository and all changed files.

**Q: How do I exclude files from analysis?**
A: Configure in `config.py` or use `.perfguardignore` file (coming soon).

---

## 🎯 Project Status

- ✅ **Production Ready**: Fully functional with sample application
- ✅ **CI/CD Integration**: GitHub Actions workflows configured
- ✅ **Interactive Dashboard**: React dashboard with auto-refresh
- ✅ **Multi-LLM Support**: Claude + Gemini fallback
- ✅ **Comprehensive Testing**: Sample app with performance tests
- 🚧 **Active Development**: New features added regularly

**Latest Version**: 3.1
**Last Updated**: December 2025

---

<div align="center">

**Made with ❤️ by H347h3n5, for developers and testers**

⭐ Star us on GitHub if PerfGuard AI helps your team!

[Report Issues](https://github.com/cloakofenigma/perfguard-ai/issues) • [View Dashboard Demo](https://cloakofenigma.github.io/perfguard-ai/) • [Read Docs](https://github.com/cloakofenigma/perfguard-ai/wiki)

</div>
