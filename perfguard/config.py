"""
PerfGuard AI Configuration Management
Centralized configuration for thresholds, weights, and settings
"""
import os
from typing import Dict, Any

class Config:
    """Main configuration class for PerfGuard AI"""

    # API Configuration
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GITHUB_TOKEN = os.getenv("GH_TOKEN")

    # LLM Configuration
    CLAUDE_MODEL = "claude-3-5-sonnet-20241022"  # Latest model
    GEMINI_MODEL = "gemini-1.5-pro"  # Backup model
    MAX_TOKENS = 2048

    # LLM Priority (tries in order: anthropic -> gemini)
    LLM_PROVIDERS = ["anthropic", "gemini"]

    # Performance Thresholds (as per spec)
    THRESHOLDS = {
        "execution_time": 0.15,      # +15% vs baseline
        "memory_rss": 0.20,           # +20% vs baseline
        "cpu_utilization": 0.25,      # +25%
        "io_latency": 0.30,           # +30%
        "complexity_delta": 2,        # +2 cyclomatic complexity
        "ai_risk_threshold": 0.6      # >0.6 = high risk
    }

    # Metric Weights (must sum to 100)
    WEIGHTS = {
        "execution_time": 30,
        "memory_rss": 20,
        "cpu_utilization": 15,
        "io_latency": 15,
        "complexity": 10,
        "ai_risk": 10
    }

    # Scoring Configuration
    MIN_PASSING_SCORE = 80
    SCORE_PRECISION = 1  # Decimal places

    # Storage Configuration
    BASELINE_STORAGE_PATH = "perfguard_baselines.json"
    RESULTS_PATH = "perfguard_score.json"
    REPORT_PATH = "perfguard_report.md"

    # Test Configuration
    PYTEST_MARKERS = "perf"
    BENCHMARK_ROUNDS = 5
    MEMORY_PRECISION = 3

    # Retry Configuration
    API_RETRY_ATTEMPTS = 3
    API_RETRY_DELAY = 2  # seconds
    API_TIMEOUT = 30  # seconds

    # Git Configuration
    DEFAULT_BASE_BRANCH = "main"
    DIFF_CONTEXT_LINES = 3

    # Dashboard Configuration
    DASHBOARD_PORT = 3000
    API_PORT = 5000

    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        if not cls.ANTHROPIC_API_KEY and not cls.GOOGLE_API_KEY:
            raise ValueError("At least one AI API key (ANTHROPIC_API_KEY or GOOGLE_API_KEY) is required")

        # Validate weights sum to 100
        total_weight = sum(cls.WEIGHTS.values())
        if total_weight != 100:
            raise ValueError(f"Weights must sum to 100, got {total_weight}")

        return True

    @classmethod
    def get_threshold(cls, metric: str) -> float:
        """Get threshold for a specific metric"""
        return cls.THRESHOLDS.get(metric, 0.0)

    @classmethod
    def get_weight(cls, metric: str) -> int:
        """Get weight for a specific metric"""
        return cls.WEIGHTS.get(metric, 0)

    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "thresholds": cls.THRESHOLDS,
            "weights": cls.WEIGHTS,
            "min_passing_score": cls.MIN_PASSING_SCORE,
            "model": cls.CLAUDE_MODEL
        }


# Development/Test configuration
class DevConfig(Config):
    """Development configuration with relaxed thresholds"""
    MIN_PASSING_SCORE = 70
    API_RETRY_ATTEMPTS = 1


# Production configuration
class ProdConfig(Config):
    """Production configuration with strict thresholds"""
    MIN_PASSING_SCORE = 85
    API_RETRY_ATTEMPTS = 5


# Select configuration based on environment
ENV = os.getenv("PERFGUARD_ENV", "production")
if ENV == "development":
    config = DevConfig()
elif ENV == "test":
    config = DevConfig()
else:
    config = Config()
