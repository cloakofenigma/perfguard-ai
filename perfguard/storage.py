"""
PerfGuard AI Storage and Baseline Management
Handles baseline metrics storage and comparison
"""
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime
from logger import get_logger

logger = get_logger(__name__)


class BaselineStorage:
    """Manages baseline metrics storage and retrieval"""

    def __init__(self, storage_path: str = "perfguard_baselines.json"):
        self.storage_path = Path(storage_path)
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        """Create storage file if it doesn't exist"""
        if not self.storage_path.exists():
            self.storage_path.write_text(json.dumps({"baselines": {}, "metadata": {}}))
            logger.info(f"Created baseline storage at {self.storage_path}")

    def load_baselines(self) -> Dict[str, Any]:
        """Load all baselines from storage"""
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
            logger.info(f"Loaded {len(data.get('baselines', {}))} baselines")
            return data.get("baselines", {})
        except Exception as e:
            logger.error(f"Failed to load baselines: {e}")
            return {}

    def save_baseline(self, test_name: str, metrics: Dict[str, Any]):
        """Save or update baseline for a specific test"""
        try:
            # Load existing data
            with open(self.storage_path, 'r') as f:
                data = json.load(f)

            # Update baseline
            data["baselines"][test_name] = {
                "metrics": metrics,
                "timestamp": datetime.now().isoformat(),
                "version": data.get("metadata", {}).get("version", 1)
            }

            # Update metadata
            if "metadata" not in data:
                data["metadata"] = {}
            data["metadata"]["last_updated"] = datetime.now().isoformat()
            data["metadata"]["total_baselines"] = len(data["baselines"])

            # Save back
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)

            logger.info(f"Saved baseline for {test_name}")
        except Exception as e:
            logger.error(f"Failed to save baseline: {e}")
            raise

    def get_baseline(self, test_name: str) -> Optional[Dict[str, Any]]:
        """Get baseline for a specific test"""
        baselines = self.load_baselines()
        baseline = baselines.get(test_name)

        if baseline:
            logger.info(f"Retrieved baseline for {test_name}")
            return baseline.get("metrics")
        else:
            logger.warning(f"No baseline found for {test_name}")
            return None

    def compare_with_baseline(
        self,
        test_name: str,
        current_metrics: Dict[str, float]
    ) -> Dict[str, Any]:
        """Compare current metrics with baseline"""
        baseline = self.get_baseline(test_name)

        if not baseline:
            logger.info(f"No baseline for {test_name}, establishing new baseline")
            self.save_baseline(test_name, current_metrics)
            return {
                "is_first_run": True,
                "baseline_established": True,
                "changes": {}
            }

        # Calculate percentage changes
        changes = {}
        for metric, current_value in current_metrics.items():
            baseline_value = baseline.get(metric, 0)
            if baseline_value == 0:
                changes[metric] = {
                    "baseline": baseline_value,
                    "current": current_value,
                    "change_percent": 0,
                    "regression": False
                }
            else:
                change_percent = ((current_value - baseline_value) / baseline_value) * 100
                changes[metric] = {
                    "baseline": baseline_value,
                    "current": current_value,
                    "change_percent": round(change_percent, 2),
                    "regression": change_percent > 0  # Assuming higher is worse
                }

        return {
            "is_first_run": False,
            "baseline_established": False,
            "changes": changes
        }

    def clear_baselines(self):
        """Clear all baselines (use with caution)"""
        self.storage_path.write_text(json.dumps({"baselines": {}, "metadata": {}}))
        logger.warning("All baselines cleared")

    def export_baselines(self, export_path: str):
        """Export baselines to a different file"""
        with open(self.storage_path, 'r') as f:
            data = json.load(f)
        with open(export_path, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Baselines exported to {export_path}")
