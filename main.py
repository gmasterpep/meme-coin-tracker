from __future__ import annotations

import logging
from typing import Any

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from app.config import settings

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Meme Coin Tracker is online.\n"
        "Commands:\n"
        "- /start\n"
        "- /watch add <wallet>\n"
        "- /watch list\n"
        "- /status\n"
        "- /rank\n"
        "- /paper\n"
    )


async def watch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text or ""
    parts = text.split()

    if len(parts) < 3 or parts[1] != "add":
        await update.message.reply_text("Usage: /watch add <wallet_address>")
        return

    wallet = parts[2]
    await update.message.reply_text(f"Added wallet to watchlist: {wallet}")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"Telegram token configured: {'yes' if settings.telegram_token else 'no'}\n"
        f"Paper trading enabled: {'yes' if settings.paper_trading_enabled else 'no'}\n"
        f"Max position: {settings.max_position_pct}%\n"
        f"Max daily loss: {settings.max_daily_loss_pct}%"
    )


async def rank(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Sample ranked opportunity feed:\n"
        "1. Token ABC | Short-term speculative | Score 76\n"
        "2. Token DEF | Watch | Score 63\n"
        "3. Token GHI | Avoid | Score 32"
    )


async def paper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    settings.paper_trading_enabled = not settings.paper_trading_enabled
    await update.message.reply_text(
        f"Paper trading set to: {'enabled' if settings.paper_trading_enabled else 'disabled'}"
    )


async def build_bot() -> Application:
    if not settings.telegram_token:
        raise ValueError("TELEGRAM_TOKEN missing. Copy .env.example to .env and add your token.")

    app = Application.builder().token(settings.telegram_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("watch", watch))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("rank", rank))
    app.add_handler(CommandHandler("paper", paper))
    return app
