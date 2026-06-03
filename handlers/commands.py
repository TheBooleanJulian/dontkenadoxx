"""
DontKenaDoxx — Command Handlers
/start and /help messages.
"""

from telegram import Update
from telegram.ext import ContextTypes

START_TEXT = """🗺️ <b>DontKenaDoxx</b>
<i>OSINT Geolocation Bot</i>

<b>Wah, you found me!</b> I can identify where a photo was taken using OSINT techniques — the same methods investigators and security researchers use.

<b>How to use:</b>
📤 Just send or forward me any photo
🔍 I'll analyze it across <b>10 OSINT categories</b>
📍 Get a location guess with confidence rating

<b>What I analyze:</b>
📝 Text & Signs • 🏗️ Architecture • 🛣️ Roads
🌿 Vegetation • 🚗 Vehicles • ⚡ Infrastructure
🕌 Cultural markers • ☁️ Environment • 👥 People • 🏪 Brands

<b>Best results:</b> Outdoor photos with visible signs, roads, or buildings. The more context visible, the more precise I can be.

<i>Send a photo to try it now!</i>

/help — see tips for best results"""

HELP_TEXT = """🔍 <b>DontKenaDoxx — Tips for Best Results</b>

<b>What works best:</b>
✅ Outdoor street-level photos
✅ High resolution images
✅ Photos with visible signage or text
✅ Images with distinct architectural or landscape features
✅ Forwarded photos from other chats (it analyzes those too)

<b>What doesn't work well:</b>
❌ Heavily cropped images with minimal context
❌ Very dark or blurry photos
❌ Pure indoor shots with no windows/distinctive features
❌ Abstract close-ups

<b>OSINT categories analyzed:</b>
1️⃣ Text & Signage — language, signs, license plates
2️⃣ Architecture — building style, materials, era
3️⃣ Road Infrastructure — traffic side, sign conventions
4️⃣ Vegetation & Terrain — plant species, climate indicators
5️⃣ Vehicles — car brands, plate formats
6️⃣ Electrical Infrastructure — power pole types
7️⃣ Cultural Markers — temples, flags, decorations
8️⃣ Environment — weather, humidity, sun angle
9️⃣ People — clothing, demographics
🔟 Brands — local chains, franchise adaptations

<b>Confidence levels:</b>
🟢 70–100%  High — Strong evidence
🟡 50–69%   Medium — Regional identification
🟠 30–49%   Low — Country-level guess
🔴 &lt;30%     Very Low — Hemisphere/climate zone only

<i>Send any photo to start!</i>"""


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(START_TEXT, parse_mode="HTML")


async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP_TEXT, parse_mode="HTML")
