from __future__ import annotations

from app.services.coin_analyzer import analyze_token
from app.services.wallet_score import classify_trade_risk


def rank_opportunity(wallet_score: float, token_metadata: dict) -> dict:
    """Combine wallet quality and token evaluation into an opportunity ranking."""
    token_analysis = analyze_token(token_metadata)

    opportunity_score = (
        wallet_score * 0.55 + token_analysis["total_score"] * 0.45
    )
    risk_score = token_analysis["risk_score"] + max(0, 50 - wallet_score / 2)
    recommendation = classify_trade_risk(opportunity_score, risk_score)

    summary = (
        f"Opportunity score {opportunity_score:.1f}/100 | "
        f"risk {risk_score:.1f}/100 | recommendation={recommendation}"
    )

    result = {
        "opportunity_score": round(opportunity_score, 2),
        "risk_score": round(risk_score, 2),
        "recommendation": recommendation,
        "summary": summary,
        "short_term_score": token_analysis["short_term_score"],
        "long_term_score": token_analysis["long_term_score"],
        "red_flags": token_analysis["red_flags"],
        "green_flags": token_analysis["green_flags"],
    }
    return result
