"""
DontKenaDoxx — Photo Handler
Handles photos (direct + forwarded) and image documents sent to the bot.
"""

import logging
import time
from telegram import Update
from telegram.ext import ContextTypes

from utils.analyzer import analyze_image
from utils.formatter import format_analysis, format_error

logger = logging.getLogger(__name__)

# ─── Per-user rate limiter (in-memory) ────────────────────────────────────────
_user_cooldowns: dict[int, float] = {}
COOLDOWN_SECONDS = 30  # seconds between analyses per user

THINKING_MESSAGES = [
    "🔍 <b>DONTKENADOXX</b> is on the case...\n"
    "<i>Scanning for text, signs, architecture, vegetation...</i>",

    "🧠 <b>Cross-referencing OSINT categories...</b>\n"
    "<i>Road markings • Electrical infrastructure • Cultural markers</i>",
]

IMAGE_MIMETYPES = {
    "image/jpeg", "image/jpg", "image/png",
    "image/webp", "image/gif", "image/bmp",
}


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Main handler for photos and image documents."""
    user = update.effective_user
    user_id = user.id
    username = user.username or user.first_name or str(user_id)
    now = time.monotonic()

    # ── Rate limit check ──────────────────────────────────────────────────────
    if user_id in _user_cooldowns:
        elapsed = now - _user_cooldowns[user_id]
        if elapsed < COOLDOWN_SECONDS:
            remaining = int(COOLDOWN_SECONDS - elapsed)
            await update.message.reply_text(
                f"⏳ <b>Eh, steady lah!</b>\n"
                f"Wait <b>{remaining}s</b> more before sending another photo.",
                parse_mode="HTML",
            )
            return

    _user_cooldowns[user_id] = now
    logger.info(f"Photo received from @{username} (id={user_id})")

    # ── Resolve image source ──────────────────────────────────────────────────
    mime_type = "image/jpeg"
    photo_file = None

    if update.message.photo:
        # Standard Telegram photo (compressed)
        photo_file = await update.message.photo[-1].get_file()
        mime_type = "image/jpeg"

    elif update.message.document:
        doc = update.message.document
        if doc.mime_type and doc.mime_type.lower() in IMAGE_MIMETYPES:
            photo_file = await doc.get_file()
            mime_type = doc.mime_type.lower()
        else:
            await update.message.reply_text(
                "❌ That doesn't look like an image file leh.\n"
                "Send a JPEG, PNG, or WebP photo.",
            )
            return

    if not photo_file:
        await update.message.reply_text("❌ Cannot find any image in this message.")
        return

    # ── Send first status message ─────────────────────────────────────────────
    status_msg = await update.message.reply_text(
        THINKING_MESSAGES[0],
        parse_mode="HTML",
    )

    try:
        # ── Download image ────────────────────────────────────────────────────
        image_bytearray = await photo_file.download_as_bytearray()
        image_bytes = bytes(image_bytearray)

        if len(image_bytes) < 1024:
            await status_msg.edit_text(
                "⚠️ <b>Image too small to analyze.</b>\n"
                "Send a proper photo, not a thumbnail.",
                parse_mode="HTML",
            )
            return

        logger.info(f"Downloaded image: {len(image_bytes)} bytes, mime={mime_type}")

        # ── Update status ─────────────────────────────────────────────────────
        await status_msg.edit_text(THINKING_MESSAGES[1], parse_mode="HTML")

        # ── Call Claude Vision OSINT analyzer ────────────────────────────────
        result = await analyze_image(image_bytes, mime_type)

        # ── Format and deliver result ─────────────────────────────────────────
        formatted = format_analysis(result)
        await status_msg.edit_text(formatted, parse_mode="HTML")

        logger.info(
            f"Analysis complete for @{username}: "
            f"{result.get('best_guess', {}).get('location', '?')} "
            f"({result.get('best_guess', {}).get('confidence', 0)}%)"
        )

    except Exception as e:
        logger.error(f"Analysis failed for @{username}: {e}", exc_info=True)
        await status_msg.edit_text(format_error(str(e)), parse_mode="HTML")
