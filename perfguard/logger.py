"""
PerfGuard AI Logging Infrastructure
Structured logging with appropriate levels and formatting
"""
import logging
import sys
from typing import Optional
from pathlib import Path

class PerfGuardLogger:
    """Custom logger for PerfGuard AI with structured output"""

    _instance: Optional[logging.Logger] = None

    @classmethod
    def get_logger(cls, name: str = "perfguard") -> logging.Logger:
        """Get or create logger instance"""
        if cls._instance is None:
            cls._instance = cls._setup_logger(name)
        return cls._instance

    @classmethod
    def _setup_logger(cls, name: str) -> logging.Logger:
        """Setup logger with appropriate handlers and formatters"""
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # Avoid duplicate handlers
        if logger.handlers:
            return logger

        # Console handler with UTF-8 encoding
        import io
        # Wrap stdout to ensure UTF-8 encoding
        if hasattr(sys.stdout, 'buffer'):
            utf8_stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        else:
            utf8_stdout = sys.stdout

        console_handler = logging.StreamHandler(utf8_stdout)
        console_handler.setLevel(logging.INFO)

        # Formatter with timestamp, level, and message
        formatter = logging.Formatter(
            fmt='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

        return logger

    @classmethod
    def set_level(cls, level: str):
        """Set logging level dynamically"""
        if cls._instance:
            numeric_level = getattr(logging, level.upper(), logging.INFO)
            cls._instance.setLevel(numeric_level)


# Convenience function to get logger
def get_logger(name: str = "perfguard") -> logging.Logger:
    """Get logger instance"""
    return PerfGuardLogger.get_logger(name)
