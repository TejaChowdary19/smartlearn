from __future__ import annotations
from typing import List, Dict

def coverage(plan_text: str, required_topics: List[str]) -> float:
    plan_lower = plan_text.lower()
    hit = sum(1 for t in required_topics if t.lower() in plan_lower)
    return hit / max(1, len(required_topics))

def latency_ms(start_time: float, end_time: float) -> float:
    return max(0.0, (end_time - start_time) * 1000.0)
