from __future__ import annotations

import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from app.config import settings

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Meme Coin Tracker is online.\n"
        "Live Fomo feed: connected by the worker when deployed.\n\n"
        "Commands:\n/start\n/status\n/rank\n/paper"
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"Paper trading: {'enabled' if settings.paper_trading_enabled else 'disabled'}\n"
        f"Fomo feed: {settings.fomo_stream_url}\n"
        f"Max position: {settings.max_position_pct}%\n"
        "Live execution: disabled"
    )


async def rank(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Rankings are produced from incoming Fomo events. No live event has been ranked yet."
    )


async def paper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    settings.paper_trading_enabled = not settings.paper_trading_enabled
    await update.message.reply_text(
        f"Paper trading set to: {'enabled' if settings.paper_trading_enabled else 'disabled'}"
    )


async def build_bot() -> Application:
    if not settings.telegram_token:
        raise ValueError("TELEGRAM_TOKEN is missing")
    app = Application.builder().token(settings.telegram_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("rank", rank))
    app.add_handler(CommandHandler("paper", paper))
    return app
