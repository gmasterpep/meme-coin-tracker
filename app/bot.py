from __future__ import annotations

from typing import Any

from app.config import settings
from app.models import TokenOpportunity


class AlertRouter:
    def format_opportunity(self, opportunity: TokenOpportunity) -> str:
        if opportunity.buy_recommendation == "avoid":
            status = "AVOID"
        elif opportunity.buy_recommendation in {"strong-buy", "short-term-speculative"}:
            status = "BUY / WATCH"
        else:
            status = "WATCH"

        return (
            f"*{status}*\n"
            f"Token: {opportunity.symbol}\n"
            f"Chain: {opportunity.chain}\n"
            f"Score: {opportunity.score:.1f}/100\n"
            f"Risk: {opportunity.risk_score:.1f}/100\n"
            f"Short-term: {opportunity.short_term_score:.1f}\n"
            f"Long-term: {opportunity.long_term_score:.1f}\n"
            f"Entry: {opportunity.recommended_entry}\n"
            f"Stop: {opportunity.stop_loss}\n"
            f"Target: {opportunity.target_exit}\n"
            f"Summary: {opportunity.summary}\n"
            f"Green flags: {', '.join(opportunity.green_flags) if opportunity.green_flags else 'n/a'}\n"
            f"Red flags: {', '.join(opportunity.red_flags) if opportunity.red_flags else 'n/a'}"
        )

    def get_risk_cap_for_position(self, score: float) -> float:
        return min(settings.max_position_pct, max(0.1, score / 100.0))
