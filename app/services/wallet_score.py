from __future__ import annotations

from statistics import mean


def score_wallet_performance(history: list[dict]) -> dict:
    """Compute a wallet-quality score from recent trade history."""
    if not history:
        return {
            "scoring": 0.0,
            "win_rate": 0.0,
            "avg_return_pct": 0.0,
            "avg_holding_hours": 0.0,
            "sample_size": 0,
            "recent_quality": 0.0,
        }

    returns = [float(item.get("pnl_pct", 0.0)) for item in history]
    avg_return = mean(returns) if returns else 0.0
    win_rate = sum(1 for r in returns if r > 0) / len(returns)
    avg_holding_hours = mean([float(item.get("holding_hours", 0.0)) for item in history])

    scoring = min(100.0, max(0.0, (avg_return * 2.5) + (win_rate * 55) + 10.0))
    recent_quality = min(100.0, max(0.0, scoring * 0.9))

    return {
        "scoring": round(scoring, 2),
        "win_rate": round(win_rate, 3),
        "avg_return_pct": round(avg_return, 2),
        "avg_holding_hours": round(avg_holding_hours, 2),
        "sample_size": len(history),
        "recent_quality": round(recent_quality, 2),
    }


def classify_trade_risk(opportunity_score: float, risk_score: float) -> str:
    if risk_score > 70 or opportunity_score < 35:
        return "avoid"
    if opportunity_score >= 70 and risk_score <= 45:
        return "strong-buy"
    if opportunity_score >= 55 and risk_score <= 60:
        return "watch"
    if opportunity_score >= 45:
        return "short-term-speculative"
    return "avoid"
