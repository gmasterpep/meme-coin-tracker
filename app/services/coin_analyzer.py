from __future__ import annotations


def analyze_token(token: dict) -> dict:
    """Low-fi token evaluator using basic heuristics for memecoin screening."""
    liquidity = float(token.get("liquidity_usd") or 0)
    market_cap = float(token.get("market_cap_usd") or 0)
    holder_concentration = float(token.get("holder_concentration_pct") or 0)
    launch_age_minutes = int(token.get("launch_age_minutes") or 0)
    red_flags = list(token.get("red_flags") or [])
    green_flags = list(token.get("green_flags") or [])

    risk_score = 0
    if holder_concentration > 40:
        risk_score += 20
    if liquidity < 100000:
        risk_score += 25
    if market_cap < 500000:
        risk_score += 15
    if red_flags:
        risk_score += min(30, len(red_flags) * 10)

    short_term_score = 50
    long_term_score = 40

    if liquidity > 400000:
        short_term_score += 18
    if market_cap > 1000000:
        long_term_score += 20
    if launch_age_minutes < 45:
        short_term_score += 12
    if holder_concentration < 30:
        long_term_score += 12
    if green_flags:
        long_term_score += min(20, len(green_flags) * 5)

    short_term_score = max(0, min(100, short_term_score - risk_score))
    long_term_score = max(0, min(100, long_term_score - risk_score))

    total_score = (short_term_score * 0.55) + (long_term_score * 0.45)

    return {
        "risk_score": min(100, risk_score),
        "short_term_score": short_term_score,
        "long_term_score": long_term_score,
        "total_score": total_score,
        "red_flags": red_flags,
        "green_flags": green_flags,
    }
