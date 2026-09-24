from __future__ import annotations

import asyncio
import logging

from app.bot import build_bot
from app.services.live_feed import LiveFeedService

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    app = await build_bot()
    await app.initialize()
    await app.start()
    await app.updater.start_polling()  # type: ignore[union-attr]
    feed_task = asyncio.create_task(LiveFeedService(app.bot).run_forever())
    logging.info("Telegram bot and read-only Fomo feed started")
    try:
        await asyncio.Event().wait()
    finally:
        feed_task.cancel()
        await app.updater.stop()  # type: ignore[union-attr]
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
