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
- 🧠 **AI-powered** smart test selection (no full test suite needed)
- 📊 **Single score** (0–100) for easy decision making
- 🚫 **Blocks merge** if score < threshold
- ⚡ **Fully automated** in GitHub Actions
- 🎬 **Production-ready** with sample application included

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Sample Application](#-sample-application)
- [Performance Metrics](#-performance-metrics)
- [Scoring System](#-scoring-system)
- [Configuration](#%EF%B8%8F-configuration)
- [Usage](#-usage)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## ✨ Features

### Core Capabilities
- **AI-Driven Analysis**: Uses Claude 3.5 Sonnet to predict performance hotspots
- **Comprehensive Metrics**: Tracks 6 key performance indicators
- **Baseline Comparison**: Automatically establishes and compares against baselines
- **Smart Test Selection**: AI suggests which tests to run based on code changes
- **Automated Reporting**: Generates detailed markdown reports with actionable insights
- **GitHub Integration**: Seamless CI/CD workflow with PR comments

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
│   ├── ai_analyzer.py      # Claude AI integration
│   ├── metrics_collector.py # Performance measurement
│   ├── rules_engine.py     # Scoring calculation
│   ├── storage.py          # Baseline management
│   ├── config.py           # Configuration
│   ├── logger.py           # Structured logging
│   └── prompts.py          # AI prompts
├── sample-app/              # Demo movie application
│   ├── app.py              # Flask web app
│   ├── movies_data.py      # Movie database
│   ├── slow_function.py    # Intentionally slow code
│   ├── templates/          # HTML templates
│   ├── static/             # CSS, JS, images
│   └── tests/              # Performance tests
├── dashboard/               # React dashboard
│   └── src/                # Dashboard components
├── .github/workflows/       # CI/CD pipeline
│   └── perfguard.yml       # GitHub Actions workflow
├── requirements.txt         # Python dependencies
├── pytest.ini              # Test configuration
└── README.md               # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Git
- Anthropic API key (Claude 3.5 Sonnet)
- GitHub repository

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/cloakofenigma/perfguard-ai.git
cd perfguard-ai
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
export GH_TOKEN="your-github-token"  # Optional
```

4. **Configure GitHub Actions**

Add secrets to your repository:
- Go to Settings → Secrets and variables → Actions
- Add `ANTHROPIC_API_KEY` with your Claude API key

5. **Enable branch protection**
- Settings → Branches → Add rule
- Require status checks: "PerfGuard AI"

---

## 🎬 Sample Application

PerfGuard AI includes a fully-functional movie browsing application to demonstrate its capabilities.

### Running the Sample App

```bash
cd sample-app
python app.py
```

Visit `http://localhost:5000` to explore:
- **15 curated movies** with detailed information
- **Responsive design** that works on all devices
- **Search functionality** and filters
- **Movie detail pages** with cast, crew, and plot

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
# Required
ANTHROPIC_API_KEY="sk-ant-..."

# Optional
GH_TOKEN="ghp_..."
PERFGUARD_ENV="production"  # or "development"
```

### Config File (`perfguard/config.py`)

```python
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
```

---

## 💻 Usage

### Local Testing

```bash
# Run PerfGuard on current changes
python perfguard/main.py

# View results
cat perfguard_report.md
```

### In Pull Requests

1. Create a branch with changes
2. Open a pull request
3. PerfGuard AI runs automatically
4. Review the comment and score
5. Fix issues if score < 80
6. Merge when approved

### Manual Test Execution

```bash
# Run all performance tests
pytest -m perf

# Run specific test
pytest sample-app/tests/test_perf.py::test_api_performance -v

# With benchmarking
pytest -m perf --benchmark-only
```

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

#### 2. "ANTHROPIC_API_KEY not set"
**Cause**: Missing API key
**Solution**: Add API key to environment or GitHub secrets

#### 3. "Benchmark results not found"
**Cause**: No tests with `@pytest.mark.perf`
**Solution**: Add performance test markers

#### 4. "Score always 100"
**Cause**: No baseline established
**Solution**: Run tests once to create baseline

#### 5. "Import errors"
**Cause**: Missing dependencies
**Solution**: `pip install -r requirements.txt`

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

## 📚 Resources

- [Claude AI Documentation](https://docs.anthropic.com/)
- [pytest-benchmark Guide](https://pytest-benchmark.readthedocs.io/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
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
- 📧 Email: support@perfguard.ai

---

<div align="center">

**Made with ❤️ by developers, for developers**

⭐ Star us on GitHub if PerfGuard AI helps your team!

</div>
