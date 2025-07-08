"""Simple utilities for performance monitoring."""

from __future__ import annotations

import time
import psutil


class PerfTracker:
    """Track execution time and memory usage."""

    def __init__(self):
        self.process = psutil.Process()
        self.start = time.time()

    def snapshot(self, label: str = "") -> dict:
        return {
            "label": label,
            "duration": time.time() - self.start,
            "rss": self.process.memory_info().rss,
        }

    def reset(self):
        self.start = time.time()
