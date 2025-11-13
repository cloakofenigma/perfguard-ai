"""
PerfGuard AI Metrics Collector
Collects real performance metrics using pytest-benchmark, memory-profiler, etc.
"""
import pytest
import subprocess
import json
import time
import psutil
import os
import sys
from typing import Dict, Any, List
from pathlib import Path
from radon.complexity import cc_visit
from radon.raw import analyze
from memory_profiler import memory_usage
from config import config
from logger import get_logger
from storage import BaselineStorage

logger = get_logger(__name__)


class MetricsCollector:
    """Collects various performance metrics"""

    def __init__(self):
        self.storage = BaselineStorage(config.BASELINE_STORAGE_PATH)

    def collect_execution_time(self, test_path: str = None) -> Dict[str, float]:
        """
        Collect execution time metrics using pytest-benchmark

        Returns dict with current execution time
        """
        logger.info("Collecting execution time metrics...")

        try:
            # Run pytest with benchmark marker
            cmd = [
                "pytest",
                "-m", config.PYTEST_MARKERS,
                "--benchmark-only",
                "--benchmark-json=benchmark_results.json",
                "-v"
            ]

            if test_path:
                cmd.append(test_path)

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )

            # Parse benchmark results
            if Path("benchmark_results.json").exists():
                with open("benchmark_results.json", 'r') as f:
                    data = json.load(f)

                benchmarks = data.get("benchmarks", [])
                if benchmarks:
                    # Use P95 (95th percentile) or mean
                    total_mean = sum(b["stats"]["mean"] for b in benchmarks) / len(benchmarks)
                    logger.info(f"Execution time (mean): {total_mean:.4f}s")
                    return {"current": total_mean}
                else:
                    logger.warning("No benchmarks found")
                    return {"current": 0.0}
            else:
                logger.warning("No benchmark results file found")
                return {"current": 0.0}

        except subprocess.TimeoutExpired:
            logger.error("Benchmark execution timed out")
            return {"current": float('inf')}
        except Exception as e:
            logger.error(f"Error collecting execution time: {e}")
            return {"current": 0.0}

    def collect_memory_usage(self, test_path: str = None) -> Dict[str, float]:
        """
        Collect memory usage metrics

        Returns dict with peak memory usage in MB
        """
        logger.info("Collecting memory usage metrics...")

        try:
            def run_tests():
                """Run tests and measure memory"""
                cmd = [
                    "pytest",
                    "-m", config.PYTEST_MARKERS,
                    "-v",
                    "--tb=short"
                ]
                if test_path:
                    cmd.append(test_path)

                subprocess.run(cmd, capture_output=True, timeout=300)

            # Measure memory usage
            mem_usage = memory_usage(
                (run_tests, ),
                interval=0.1,
                timeout=300,
                max_usage=True
            )

            # Get peak memory
            if isinstance(mem_usage, list):
                peak_memory = max(mem_usage)
            else:
                peak_memory = mem_usage

            logger.info(f"Peak memory usage: {peak_memory:.2f} MB")
            return {"current": peak_memory}

        except Exception as e:
            logger.error(f"Error collecting memory usage: {e}")
            return {"current": 0.0}

    def collect_cpu_utilization(self, test_path: str = None) -> Dict[str, float]:
        """
        Collect CPU utilization during test execution

        Returns dict with average CPU utilization percentage
        """
        logger.info("Collecting CPU utilization metrics...")

        try:
            # Start monitoring
            cpu_samples = []
            process = psutil.Process()

            # Start test in subprocess
            cmd = [
                "pytest",
                "-m", config.PYTEST_MARKERS,
                "-v",
                "--tb=short"
            ]
            if test_path:
                cmd.append(test_path)

            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Monitor CPU while test runs
            start_time = time.time()
            while proc.poll() is None and (time.time() - start_time) < 300:
                try:
                    cpu_percent = process.cpu_percent(interval=0.1)
                    cpu_samples.append(cpu_percent)
                except:
                    break
                time.sleep(0.1)

            proc.wait(timeout=10)

            # Calculate average CPU
            if cpu_samples:
                avg_cpu = sum(cpu_samples) / len(cpu_samples)
            else:
                avg_cpu = 0.0

            logger.info(f"Average CPU utilization: {avg_cpu:.2f}%")
            return {"current": avg_cpu}

        except Exception as e:
            logger.error(f"Error collecting CPU utilization: {e}")
            return {"current": 0.0}

    def collect_io_latency(self, test_path: str = None) -> Dict[str, float]:
        """
        Collect I/O latency metrics (file, network, DB operations)

        Returns dict with average I/O latency in milliseconds
        """
        logger.info("Collecting I/O latency metrics...")

        try:
            # Measure I/O operations during test execution
            process = psutil.Process()

            # Get initial I/O counters
            io_start = process.io_counters()
            start_time = time.time()

            # Run tests
            cmd = [
                "pytest",
                "-m", config.PYTEST_MARKERS,
                "-v",
                "--tb=short"
            ]
            if test_path:
                cmd.append(test_path)

            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=300
            )

            # Get final I/O counters
            end_time = time.time()
            io_end = process.io_counters()

            # Calculate I/O metrics
            total_io_ops = (
                (io_end.read_count - io_start.read_count) +
                (io_end.write_count - io_start.write_count)
            )

            elapsed_time = end_time - start_time

            if total_io_ops > 0:
                avg_latency = (elapsed_time / total_io_ops) * 1000  # Convert to ms
            else:
                avg_latency = 0.0

            logger.info(f"Average I/O latency: {avg_latency:.4f} ms")
            return {"current": avg_latency}

        except Exception as e:
            logger.error(f"Error collecting I/O latency: {e}")
            return {"current": 0.0}

    def collect_code_complexity(self, file_paths: List[str]) -> Dict[str, Any]:
        """
        Collect code complexity metrics using radon

        Args:
            file_paths: List of Python files to analyze

        Returns dict with complexity metrics
        """
        logger.info(f"Collecting code complexity for {len(file_paths)} files...")

        total_complexity = 0
        file_complexities = {}

        try:
            for file_path in file_paths:
                if not file_path.endswith('.py'):
                    continue

                if not Path(file_path).exists():
                    logger.warning(f"File not found: {file_path}")
                    continue

                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()

                # Calculate cyclomatic complexity
                try:
                    results = cc_visit(code)
                    file_total = sum(item.complexity for item in results)
                    file_complexities[file_path] = file_total
                    total_complexity += file_total
                except Exception as e:
                    logger.warning(f"Could not analyze {file_path}: {e}")

            logger.info(f"Total complexity: {total_complexity}")
            return {
                "current": total_complexity,
                "files": file_complexities
            }

        except Exception as e:
            logger.error(f"Error collecting code complexity: {e}")
            return {"current": 0, "files": {}}

    def collect_all_metrics(
        self,
        test_path: str = None,
        changed_files: List[str] = None
    ) -> Dict[str, Any]:
        """
        Collect all performance metrics

        Args:
            test_path: Optional specific test path
            changed_files: List of changed files for complexity analysis

        Returns:
            Dictionary with all metrics and baseline comparisons
        """
        logger.info("=== Starting metrics collection ===")

        metrics = {}

        # 1. Execution Time
        exec_time = self.collect_execution_time(test_path)
        exec_baseline = self.storage.get_baseline("execution_time")
        if exec_baseline:
            metrics["execution_time"] = {
                "current": exec_time["current"],
                "baseline": exec_baseline["current"],
                "change_percent": (
                    (exec_time["current"] - exec_baseline["current"]) / exec_baseline["current"] * 100
                    if exec_baseline["current"] > 0 else 0
                )
            }
        else:
            # First run - establish baseline
            self.storage.save_baseline("execution_time", exec_time)
            metrics["execution_time"] = {
                "current": exec_time["current"],
                "baseline": exec_time["current"],
                "change_percent": 0.0
            }

        # 2. Memory Usage
        memory = self.collect_memory_usage(test_path)
        mem_baseline = self.storage.get_baseline("memory_rss")
        if mem_baseline:
            metrics["memory_rss"] = {
                "current": memory["current"],
                "baseline": mem_baseline["current"],
                "change_percent": (
                    (memory["current"] - mem_baseline["current"]) / mem_baseline["current"] * 100
                    if mem_baseline["current"] > 0 else 0
                )
            }
        else:
            self.storage.save_baseline("memory_rss", memory)
            metrics["memory_rss"] = {
                "current": memory["current"],
                "baseline": memory["current"],
                "change_percent": 0.0
            }

        # 3. CPU Utilization
        cpu = self.collect_cpu_utilization(test_path)
        cpu_baseline = self.storage.get_baseline("cpu_utilization")
        if cpu_baseline:
            metrics["cpu_utilization"] = {
                "current": cpu["current"],
                "baseline": cpu_baseline["current"],
                "change_percent": (
                    (cpu["current"] - cpu_baseline["current"]) / cpu_baseline["current"] * 100
                    if cpu_baseline["current"] > 0 else 0
                )
            }
        else:
            self.storage.save_baseline("cpu_utilization", cpu)
            metrics["cpu_utilization"] = {
                "current": cpu["current"],
                "baseline": cpu["current"],
                "change_percent": 0.0
            }

        # 4. I/O Latency
        io_lat = self.collect_io_latency(test_path)
        io_baseline = self.storage.get_baseline("io_latency")
        if io_baseline:
            metrics["io_latency"] = {
                "current": io_lat["current"],
                "baseline": io_baseline["current"],
                "change_percent": (
                    (io_lat["current"] - io_baseline["current"]) / io_baseline["current"] * 100
                    if io_baseline["current"] > 0 else 0
                )
            }
        else:
            self.storage.save_baseline("io_latency", io_lat)
            metrics["io_latency"] = {
                "current": io_lat["current"],
                "baseline": io_lat["current"],
                "change_percent": 0.0
            }

        # 5. Code Complexity (if files provided)
        if changed_files:
            complexity = self.collect_code_complexity(changed_files)
            comp_baseline = self.storage.get_baseline("complexity")
            if comp_baseline:
                metrics["complexity"] = {
                    "current": complexity["current"],
                    "baseline": comp_baseline["current"],
                    "delta": complexity["current"] - comp_baseline["current"]
                }
            else:
                self.storage.save_baseline("complexity", complexity)
                metrics["complexity"] = {
                    "current": complexity["current"],
                    "baseline": complexity["current"],
                    "delta": 0
                }

        logger.info("=== Metrics collection complete ===")
        return metrics


def collect_metrics(
    suggested_benchmarks: List[str] = None,
    changed_files: List[str] = None
) -> Dict[str, Any]:
    """
    Convenience function to collect metrics

    Args:
        suggested_benchmarks: List of benchmark names (not used currently)
        changed_files: List of changed files for complexity

    Returns:
        Dictionary of collected metrics
    """
    collector = MetricsCollector()
    return collector.collect_all_metrics(
        test_path=None,
        changed_files=changed_files
    )
