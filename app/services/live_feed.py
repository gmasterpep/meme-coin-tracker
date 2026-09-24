from __future__ import annotations

import asyncio
import logging
from typing import Any

from telegram import Bot

from app.config import settings
from app.services.alert_router import rank_opportunity
from app.services.fomo_client import FomoClient, normalize_event

logger = logging.getLogger(__name__)


class LiveFeedService:
    def __init__(self, bot: Bot, client: FomoClient | None = None):
        self.bot = bot
        self.client = client or FomoClient()
        self.seen: set[tuple[str, str]] = set()

    async def run_forever(self) -> None:
        if not settings.telegram_chat_id:
            raise ValueError("TELEGRAM_CHAT_ID is missing")
        delay = 2
        while True:
            try:
                async for message in self.client.stream_events():
                    event = normalize_event(message)
                    if not event:
                        continue
                    key = (str(event["token_address"]), str(event["trader"]))
                    if key in self.seen:
                        continue
                    self.seen.add(key)
                    await self.handle_event(event)
                delay = 2
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception("Fomo stream failed; reconnecting")
                await asyncio.sleep(delay)
                delay = min(delay * 2, 60)

    async def handle_event(self, event: dict[str, Any]) -> None:
        metadata = await self.client.get_token_metadata(str(event["token_address"]))
        # Until complete token-market data is available, this is a transparent
        # screening alert rather than a buy instruction or automated trade.
        result = rank_opportunity(50.0, metadata)
        flags = ", ".join(result["red_flags"]) or "none reported"
        message = (
            "🔎 *Fomo event detected*\n"
            f"Token: `{event['symbol']}`\n"
            f"Address: `{event['token_address']}`\n"
            f"Trader: `{event['trader']}`\n"
            f"Event: {event['direction']}\n"
            f"Opportunity score: {result['opportunity_score']}/100\n"
            f"Risk score: {result['risk_score']}/100\n"
            f"Recommendation: {result['recommendation']}\n"
            f"Red flags: {flags}\n\n"
            "Paper-trading only. This is not financial advice; no live order was placed."
        )
        await self.bot.send_message(chat_id=settings.telegram_chat_id, text=message, parse_mode="Markdown")
