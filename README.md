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
- 🧠 **AI-powered** smart test selection with dual LLM support (Claude + Gemini)
- 📊 **Single score** (0–100) for easy decision making
- 🚫 **Blocks merge** if score < threshold
- ⚡ **Fully automated** in GitHub Actions
- 📱 **Interactive Dashboard** with auto-refresh and score improvement recommendations
- 🎬 **Production-ready** with sample application included
- 🛡️ **Reliable** with fallback providers and robust error handling

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
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
- **AI-Driven Analysis**: Uses Claude 3.5 Sonnet with Google Gemini 2.5 Pro as fallback for intelligent performance predictions
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
│   ├── main.py             # Main orchestration
│   ├── ai_analyzer.py      # Multi-LLM integration (Claude + Gemini)
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
│   ├── perfguard.yml       # Main PerfGuard workflow
│   └── deploy-dashboard.yml # GitHub Pages deployment
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
- **AI API Keys** (at least one required):
  - Anthropic API key (Claude 3.5 Sonnet) - Primary
  - Google API key (Gemini 2.5 Pro) - Fallback
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
# Primary LLM (recommended)
export ANTHROPIC_API_KEY="sk-ant-your-api-key-here"

# Backup LLM (optional but recommended)
export GOOGLE_API_KEY="your-google-api-key-here"

# GitHub token (optional, for PR comments)
export GH_TOKEN="ghp-your-github-token"
```

5. **Configure GitHub Actions**

Add secrets to your repository:
- Go to Settings → Secrets and variables → Actions
- Add `ANTHROPIC_API_KEY` with your Claude API key
- Add `GOOGLE_API_KEY` with your Gemini API key (recommended)
- GitHub token is automatically available as `GITHUB_TOKEN`

6. **Enable GitHub Pages (for dashboard)**
- Settings → Pages → Source: GitHub Actions

7. **Enable branch protection**
- Settings → Branches → Add rule
- Require status checks: "PerfGuard AI"

### 🚀 Quick Demo (2 minutes)

Want to see it in action immediately? Here's the fastest way:

```bash
# 1. Clone and setup (30 seconds)
git clone https://github.com/cloakofenigma/perfguard-ai.git
cd perfguard-ai
pip install -r requirements.txt

# 2. Set API key (10 seconds)
export ANTHROPIC_API_KEY="sk-ant-your-key"  # or GOOGLE_API_KEY

# 3. Run PerfGuard on sample app (60 seconds)
python perfguard/main.py

# 4. View results (20 seconds)
cat perfguard_report.md
cp perfguard_score.json dashboard/public/report.json
cd dashboard && npm install && npm start
# Opens dashboard at http://localhost:3000
```

You'll see:
- ✅ Performance score with verdict
- 📊 6 metrics analyzed (execution, memory, CPU, I/O, complexity, AI risk)
- 🤖 AI insights from Claude/Gemini
- 💡 Recommendations to improve your score

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
- **📈 Score Visualization**: Large, color-coded score display with verdict status
- **📊 Metrics Breakdown**: Detailed view of all 6 performance metrics with trend indicators
- **🤖 AI Analysis**: Claude/Gemini insights on performance risks and critical paths
- **💡 Smart Recommendations**: Actionable suggestions to improve your score, with severity levels and impact estimates
- **📉 Score History**: Track performance trends over time

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
# AI API Keys (at least one required)
ANTHROPIC_API_KEY="sk-ant-..."  # Primary: Claude 3.5 Sonnet
GOOGLE_API_KEY="..."            # Fallback: Gemini 2.5 Pro

# Optional
GH_TOKEN="ghp_..."              # GitHub token for PR comments
PERFGUARD_ENV="production"      # or "development"
```

### LLM Fallback Strategy

PerfGuard AI uses a multi-provider approach for reliability:

1. **Primary**: Anthropic Claude 3.5 Sonnet (`claude-3-5-sonnet-20241022`)
2. **Fallback**: Google Gemini 2.5 Pro (`gemini-2.5-pro`)

If the primary provider fails (rate limits, API issues), it automatically switches to the backup.

### Config File (`perfguard/config.py`)

```python
# LLM Configuration
CLAUDE_MODEL = "claude-3-5-sonnet-20241022"  # Latest model
GEMINI_MODEL = "gemini-2.5-pro"              # Backup model (Google's latest)
MAX_TOKENS = 2048

# LLM Priority (tries in order)
LLM_PROVIDERS = ["anthropic", "gemini"]

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

### Local Testing

```bash
# Run PerfGuard on current changes
python perfguard/main.py

# View results in terminal
cat perfguard_report.md

# Or view in dashboard
cp perfguard_score.json dashboard/public/report.json
cd dashboard && npm start
```

### Dashboard Usage

```bash
# Start the dashboard
cd dashboard
npm start

# Auto-refresh is enabled by default (30s interval)
# Use the refresh button for immediate updates
# Toggle auto-refresh on/off as needed

# View at: http://localhost:3000
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

# Update dashboard with results
python perfguard/main.py
cp perfguard_score.json dashboard/public/report.json
```

### CI/CD Integration

PerfGuard automatically runs on:
- Pull requests (opened, synchronized, reopened)
- Pushes to main branch
- Manual workflow dispatch

Results are:
- Posted as PR comments
- Uploaded as artifacts (30-day retention)
- Deployed to dashboard (on main branch)
- Used for merge blocking (score < 80)

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

### Version 2.0 Features (Latest)

#### Multi-LLM Support
- **Google Gemini 2.5 Pro** integration as fallback provider
- Automatic failover from Claude to Gemini on API issues
- Configurable provider priority
- Robust error handling and retry logic

#### Interactive Dashboard Enhancements
- **Auto-Refresh**: Updates every 30 seconds automatically
- **Manual Refresh**: Instant update button
- **Last Updated Indicator**: Shows when data was last fetched
- **Cache-Busting**: Prevents browser caching with timestamp queries
- **Recommendations Card**: New component with actionable score improvement tips
  - Severity-based prioritization (Critical, High, Medium, Low)
  - Estimated point impact for each fix
  - Specific commands and code examples
  - Quick actions for common optimizations

#### Reliability Improvements
- **Unicode Sanitization**: Comprehensive ASCII-only text processing
- **Error Recovery**: Graceful handling of API failures
- **Retry Logic**: Configurable retry attempts with exponential backoff
- **Better Logging**: Structured logging with sanitized output

#### CI/CD Enhancements
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

- [Claude AI Documentation](https://docs.anthropic.com/)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [pytest-benchmark Guide](https://pytest-benchmark.readthedocs.io/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [React Dashboard Guide](https://react.dev/)
- [Performance Testing Best Practices](https://martinfowler.com/articles/performance-testing.html)

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
A: Use both! Anthropic Claude 3.5 Sonnet is primary, Google Gemini 2.5 Pro is fallback for reliability.

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

**Latest Version**: 2.0
**Last Updated**: November 2024

---

<div align="center">

**Made with ❤️ by developers, for developers**

⭐ Star us on GitHub if PerfGuard AI helps your team!

[Report Issues](https://github.com/cloakofenigma/perfguard-ai/issues) • [View Dashboard Demo](https://cloakofenigma.github.io/perfguard-ai/) • [Read Docs](https://github.com/cloakofenigma/perfguard-ai/wiki)

</div>
