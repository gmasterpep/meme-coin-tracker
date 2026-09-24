from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncIterator
from typing import Any

import aiohttp

from app.config import settings
from app.models import WalletPerformance

logger = logging.getLogger(__name__)


class FomoClient:
    """Read-only client for the public PooTracker Fomo-compatible API.

    The hosted stream currently documents live thesis events, not a guaranteed
    complete trade stream. The adapter deliberately normalizes only fields it
    can observe and never executes trades.
    """

    def __init__(self, base_url: str | None = None, stream_url: str | None = None):
        self.base_url = (base_url or settings.fomo_api_base_url).rstrip("/")
        self.stream_url = stream_url or settings.fomo_stream_url

    async def _get(self, path: str, **params: Any) -> Any:
        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(f"{self.base_url}{path}", params=params) as response:
                response.raise_for_status()
                return await response.json()

    async def get_top_profiles(self) -> list[dict[str, Any]]:
        data = await self._get("/v2/leaderboards/traders")
        return data.get("items", data if isinstance(data, list) else [])

    async def get_token_metadata(self, token_address: str) -> dict[str, Any]:
        data = await self._get(f"/v2/tokens/{token_address}/theses")
        if isinstance(data, dict):
            return {"address": token_address, **data}
        return {"address": token_address}

    async def stream_events(self) -> AsyncIterator[dict[str, Any]]:
        timeout = aiohttp.ClientTimeout(total=None)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.ws_connect(self.stream_url, heartbeat=25) as socket:
                await socket.send_json({"type": "subscribe", "subscription": {"type": "all"}})
                async for message in socket:
                    if message.type == aiohttp.WSMsgType.TEXT:
                        yield message.json()
                    elif message.type in {aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR}:
                        raise ConnectionError("Fomo stream closed")


def normalize_event(message: dict[str, Any]) -> dict[str, Any] | None:
    """Extract a token event from a documented stream frame when available."""
    if message.get("type") != "thesis":
        return None
    data = message.get("data") or {}
    if not isinstance(data, dict):
        return None
    token = data.get("token") or data.get("tokenAddress") or data.get("address")
    if isinstance(token, dict):
        token_address = token.get("address") or token.get("tokenAddress")
        symbol = token.get("symbol") or token.get("name") or "UNKNOWN"
    else:
        token_address, symbol = token, data.get("symbol") or data.get("tokenSymbol") or "UNKNOWN"
    if not token_address:
        return None
    return {
        "token_address": token_address,
        "symbol": symbol,
        "direction": str(data.get("direction") or data.get("side") or "signal").lower(),
        "trader": data.get("user") or data.get("handle") or data.get("username") or "unknown",
        "raw": data,
    }
