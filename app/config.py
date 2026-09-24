from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    telegram_token: str = Field(default="", alias="TELEGRAM_TOKEN")
    telegram_chat_id: str = Field(default="", alias="TELEGRAM_CHAT_ID")
    fomo_api_base_url: str = Field(
        default="https://fomo-public.pootracker.app", alias="FOMO_API_BASE_URL"
    )
    fomo_stream_url: str = Field(
        default="wss://fomo-public.pootracker.app/v2/stream", alias="FOMO_STREAM_URL"
    )
    fomo_api_key: str = Field(default="", alias="FOMO_API_KEY")
    paper_trading_enabled: bool = Field(default=True, alias="PAPER_TRADING_ENABLED")
    max_position_pct: float = Field(default=0.5, alias="MAX_POSITION_PCT")
    max_daily_loss_pct: float = Field(default=2.5, alias="MAX_DAILY_LOSS_PCT")
    top_wallet_limit: int = Field(default=15, alias="TOP_WALLET_LIMIT")
    ranked_opportunity_limit: int = Field(default=10, alias="RANKED_OPPORTUNITY_LIMIT")

    model_config = {"env_file": ".env", "case_sensitive": False, "extra": "ignore"}


settings = Settings()
