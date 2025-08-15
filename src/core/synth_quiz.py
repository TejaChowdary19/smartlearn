from __future__ import annotations
from typing import List, Dict, Tuple

def grade_mcq_batch(items: List[Dict]) -> Tuple[float, List[Dict]]:
    correct = 0
    results = []
    for item in items:
        user = item.get("user_answer")
        ans = item.get("answer")
        ok = (user == ans)
        correct += 1 if ok else 0
        results.append({"q": item.get("q"), "correct": ok, "expected": ans, "user": user, "explanation": item.get("explanation")})
    score = correct / len(items) if items else 0.0
    return score, results

def adapt_difficulty(current: int, score: float) -> int:
    if score >= 0.85 and current < 3: return current + 1
    if score < 0.5 and current > 1: return current - 1
    return current
