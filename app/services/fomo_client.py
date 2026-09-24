from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.config import settings


@dataclass
class FomoProfile:
    name: str
    wallet: str
    score: float = 0.0
    win_rate: float = 0.0
    avg_return_pct: float = 0.0
    recent_activity: list[str] = field(default_factory=list)


class FomoClient:
    """Interface for Fomo data retrieval. Replace with real API or blockchain indexing integration."""

    def __init__(self, base_url: str | None = None, api_key: str | None = None):
        self.base_url = base_url or settings.fomo_api_base_url
        self.api_key = api_key or settings.fomo_api_key

    async def get_top_profiles(self) -> list[FomoProfile]:
        """Return top Fomo profiles. Replace this placeholder with a real data source."""
        return [
            FomoProfile(
                name="pyro",
                wallet="0x0000000000000000000000000000000000000000",
                score=88.0,
                win_rate=0.73,
                avg_return_pct=14.5,
                recent_activity=["bought token A", "sold token B", "bought token C"],
            ),
            FomoProfile(
                name="meme-lord",
                wallet="0x1111111111111111111111111111111111111111",
                score=82.0,
                win_rate=0.68,
                avg_return_pct=11.1,
                recent_activity=["bought token X", "traded token Y"],
            ),
        ]

    async def get_wallet_activity(self, wallet_address: str) -> list[dict[str, Any]]:
        """Return recent token buys/sells for a wallet."""
        return [
            {
                "wallet": wallet_address,
                "token_symbol": "ABC",
                "token_address": "0xabc",
                "buy_time": "2026-09-24T14:02:00Z",
                "price_usd": 0.00034,
                "quantity": 1500,
                "direction": "buy",
            }
        ]

    async def get_token_metadata(self, token_address: str) -> dict[str, Any]:
        """Return current metadata for a token. Replace with real blockchain or indexer data."""
        return {
            "symbol": "ABC",
            "address": token_address,
            "chain": "Solana",
            "liquidity_usd": 350000,
            "market_cap_usd": 2400000,
            "launch_age_minutes": 19,
            "holder_concentration_pct": 31.0,
            "top_wallets": ["0xaaa", "0xbbb"],
            "red_flags": [],
            "green_flags": ["active community", "adequate liquidity", "fresh launch"],
        }
