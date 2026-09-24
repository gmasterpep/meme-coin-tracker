from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    telegram_token: str = Field(default="", alias="TELEGRAM_TOKEN")
    telegram_chat_id: str = Field(default="", alias="TELEGRAM_CHAT_ID")
    fomo_api_base_url: str = Field(default="https://example.com", alias="FOMO_API_BASE_URL")
    fomo_api_key: str = Field(default="", alias="FOMO_API_KEY")
    paper_trading_enabled: bool = Field(default=True, alias="PAPER_TRADING_ENABLED")
    max_position_pct: float = Field(default=0.5, alias="MAX_POSITION_PCT")
    max_daily_loss_pct: float = Field(default=2.5, alias="MAX_DAILY_LOSS_PCT")
    top_wallet_limit: int = Field(default=15, alias="TOP_WALLET_LIMIT")
    ranked_opportunity_limit: int = Field(default=10, alias="RANKED_OPPORTUNITY_LIMIT")

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore",
    }


settings = Settings()


@dataclass
class WalletWatch:
    address: str
    label: str = ""
    enabled: bool = True
    notes: str = ""


@dataclass
class WalletSignal:
    wallet: str
    token_symbol: str
    token_address: str
    buy_time: str
    quantity: float | None = None
    price_usd: float | None = None
    confidence: float = 0.0
    reason: str = ""


@dataclass
class TokenOpportunity:
    symbol: str
    address: str
    chain: str
    score: float = 0.0
    risk_score: float = 0.0
    short_term_score: float = 0.0
    long_term_score: float = 0.0
    buy_recommendation: str = "avoid"
    summary: str = ""
    liquidity_usd: float | None = None
    market_cap_usd: float | None = None
    launch_age_minutes: int | None = None
    holder_concentration_pct: float | None = None
    top_wallets: list[str] = field(default_factory=list)
    red_flags: list[str] = field(default_factory=list)
    green_flags: list[str] = field(default_factory=list)
    recommended_entry: str = "n/a"
    stop_loss: str = "n/a"
    target_exit: str = "n/a"


@dataclass
class WalletPerformance:
    wallet: str
    scoring: float = 0.0
    win_rate: float = 0.0
    avg_return_pct: float = 0.0
    avg_holding_hours: float = 0.0
    sample_size: int = 0
    recent_quality: float = 0.0
