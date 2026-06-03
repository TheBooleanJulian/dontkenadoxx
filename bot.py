"""
DontKenaDoxx — OSINT Geolocation Telegram Bot
Identifies geographic locations from photos using Claude Vision + OSINT methodology.

Usage: python bot.py
"""

import logging
import os
import sys

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from handlers.commands import handle_start, handle_help
from handlers.photo import handle_photo

# ─── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
    stream=sys.stdout,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

BANNER = """
╔══════════════════════════════════════════════╗
║   🗺️  DontKenaDoxx — OSINT Geolocation Bot   ║
║   Powered by Claude Vision + OSINT Analysis  ║
╚══════════════════════════════════════════════╝
"""


def build_app(token: str) -> Application:
    app = Application.builder().token(token).build()

    # Commands
    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(CommandHandler("help",  handle_help))

    # Photos — both compressed (PHOTO) and full-resolution (Document image)
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.Document.IMAGE, handle_photo))

    return app


def main() -> None:
    print(BANNER)

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("❌ TELEGRAM_BOT_TOKEN not set in environment.")
        sys.exit(1)

    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    if not anthropic_key:
        logger.error("❌ ANTHROPIC_API_KEY not set in environment.")
        sys.exit(1)

    model = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")
    logger.info(f"🤖 Using Claude model: {model}")
    logger.info("🗺️  Starting DontKenaDoxx bot (polling)...")

    app = build_app(token)
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        poll_interval=1.0,
    )


if __name__ == "__main__":
    main()
