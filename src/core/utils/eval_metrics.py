"""Retrieval evaluation metric helpers."""

from __future__ import annotations

from typing import List


def recall_at_k(relevant: List[str], retrieved: List[str], k: int) -> float:
    """Compute Recall@K for lists of item identifiers."""
    if not relevant:
        return 0.0
    top_k = retrieved[:k]
    return len(set(relevant) & set(top_k)) / len(relevant)


def evaluate_retrieval(answers: List[List[str]], predictions: List[List[str]], k: int = 1) -> float:
    """Return average Recall@K over multiple queries."""
    scores = [recall_at_k(a, p, k) for a, p in zip(answers, predictions)]
    return sum(scores) / len(scores) if scores else 0.0
