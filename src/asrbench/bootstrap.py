"""Cluster bootstrap for corpus error rates and paired system differences (S24, S27).

Clusters (session > speaker > item) are resampled with replacement so that correlated clips
move together. Paired comparisons reuse the same resampled clusters for both systems.
"""

from __future__ import annotations

from collections import defaultdict

import numpy as np


def _cluster_arrays(cluster_keys: list[str], errors: list[int], n_ref: list[int]):
    err, ref = defaultdict(int), defaultdict(int)
    for k, e, n in zip(cluster_keys, errors, n_ref):
        err[k] += e
        ref[k] += n
    keys = sorted(err)
    return np.array([err[k] for k in keys], float), np.array([ref[k] for k in keys], float), keys


def corpus_rate_ci(cluster_keys, errors, n_ref, n_boot=2000, alpha=0.05, seed=0) -> dict | None:
    e, n, _ = _cluster_arrays(cluster_keys, errors, n_ref)
    if len(e) == 0 or n.sum() == 0:
        return None
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(e), size=(n_boot, len(e)))
    den = n[idx].sum(1)
    rates = np.where(den > 0, e[idx].sum(1) / np.maximum(den, 1), np.nan)
    lo, hi = np.nanpercentile(rates, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return {"low": float(lo), "high": float(hi), "clusters": len(e), "n_boot": n_boot, "level": 1 - alpha}


def paired_delta_ci(cluster_keys, err_a, err_b, n_ref, n_boot=2000, alpha=0.05, seed=0) -> dict | None:
    """Delta = rate(A) - rate(B) on identical items. Negative means A has fewer errors."""
    ea, n, keys = _cluster_arrays(cluster_keys, err_a, n_ref)
    eb, _, _ = _cluster_arrays(cluster_keys, err_b, n_ref)
    if len(keys) == 0 or n.sum() == 0:
        return None
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(keys), size=(n_boot, len(keys)))
    den = np.maximum(n[idx].sum(1), 1)
    deltas = ea[idx].sum(1) / den - eb[idx].sum(1) / den
    lo, hi = np.percentile(deltas, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return {
        "delta": float(ea.sum() / n.sum() - eb.sum() / n.sum()),
        "low": float(lo),
        "high": float(hi),
        "p_a_better": float((deltas < 0).mean()),
        "clusters": len(keys),
        "n_boot": n_boot,
        "level": 1 - alpha,
    }
