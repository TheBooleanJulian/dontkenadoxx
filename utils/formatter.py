"""
DontKenaDoxx — Telegram Message Formatter
Produces rich HTML-formatted Telegram messages from OSINT analysis JSON.
"""

# ─── Singlish flavour text by confidence tier ─────────────────────────────────
CONFIDENCE_FLAVOUR = {
    "very_high": "Confirm plus chop, this one is",
    "high": "Very likely this place lah —",
    "medium": "Probably somewhere around",
    "low": "Best guess nia, don't quote me —",
    "very_low": "Aiyah, very hard to tell, but maybe",
}

CONFIDENCE_EMOJIS = {
    "very_high": "🟢",
    "high": "🟢",
    "medium": "🟡",
    "low": "🟠",
    "very_low": "🔴",
}

CLUE_MAP = [
    ("text_signage",      "📝", "Text & Signage"),
    ("architecture",      "🏗️", "Architecture"),
    ("road_infrastructure","🛣️","Road & Transport"),
    ("vegetation",        "🌿", "Vegetation & Terrain"),
    ("vehicles",          "🚗", "Vehicles"),
    ("electrical",        "⚡", "Infrastructure"),
    ("cultural",          "🕌", "Cultural Markers"),
    ("environment",       "☁️", "Environment"),
    ("people",            "👥", "People"),
    ("brands",            "🏪", "Brands"),
]

SKIP_VALUES = {"none visible", "none", "n/a", "not visible", "not applicable", "", "not determinable"}


def _tier(confidence: int) -> str:
    if confidence >= 90: return "very_high"
    if confidence >= 70: return "high"
    if confidence >= 50: return "medium"
    if confidence >= 30: return "low"
    return "very_low"


def _confidence_bar(pct: int, length: int = 12) -> str:
    filled = max(0, min(length, round((pct / 100) * length)))
    return "█" * filled + "░" * (length - filled)


def _escape(text: str) -> str:
    """Minimal HTML escape for Telegram HTML parse mode."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def format_analysis(data: dict) -> str:
    """Convert OSINT analysis dict into a rich Telegram HTML message."""

    bg          = data.get("best_guess", {})
    location    = _escape(bg.get("location", "Unknown"))
    confidence  = int(bg.get("confidence", 0))
    conf_label  = _escape(bg.get("confidence_label", "Unknown"))
    clues       = data.get("clues", {})
    reasoning   = _escape(data.get("reasoning", "No reasoning provided."))
    alternatives= data.get("alternative_locations", [])
    key_evidence= data.get("key_evidence", [])
    notable     = _escape(data.get("notable_finds", ""))
    privacy_tip = _escape(data.get("privacy_tip", ""))

    tier      = _tier(confidence)
    bar       = _confidence_bar(confidence)
    c_emoji   = CONFIDENCE_EMOJIS[tier]
    flavour   = CONFIDENCE_FLAVOUR[tier]

    lines = [
        "🗺️ <b>DONTKENADOXX ANALYSIS</b>",
        "",
        "📍 <b>LOCATION IDENTIFIED</b>",
        f"<code>{location}</code>",
        f"{c_emoji} <code>{bar}</code> <b>{confidence}% — {conf_label}</b>",
        f"<i>{flavour} {location}</i>",
        "",
        "━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
        "🔍 <b>OSINT CLUES DETECTED</b>",
    ]

    has_clues = False
    for key, emoji, label in CLUE_MAP:
        val = clues.get(key, "").strip()
        if val.lower() not in SKIP_VALUES and val:
            lines.append(f"\n{emoji} <b>{label}</b>")
            lines.append(_escape(val))
            has_clues = True

    if not has_clues:
        lines.append("<i>No specific clues extracted.</i>")

    lines += [
        "",
        "━━━━━━━━━━━━━━━━━━━━━━━━━",
        "",
        "🧠 <b>REASONING</b>",
        reasoning,
    ]

    if key_evidence:
        lines += [
            "",
            "━━━━━━━━━━━━━━━━━━━━━━━━━",
            "",
            "🏆 <b>KEY EVIDENCE</b>",
        ]
        for ev in key_evidence:
            lines.append(f"• {_escape(ev)}")

    if alternatives:
        lines += [
            "",
            "━━━━━━━━━━━━━━━━━━━━━━━━━",
            "",
            "📊 <b>ALTERNATIVE LOCATIONS</b>",
        ]
        medals = ["🥈", "🥉", "🔸"]
        for i, alt in enumerate(alternatives[:3]):
            medal     = medals[i] if i < len(medals) else "•"
            alt_loc   = _escape(alt.get("location", "Unknown"))
            alt_conf  = int(alt.get("confidence", 0))
            alt_bar   = _confidence_bar(alt_conf, 8)
            alt_reason= _escape(alt.get("reason", ""))
            lines.append(f"{medal} <b>{alt_loc}</b>  <code>{alt_bar}</code> {alt_conf}%")
            if alt_reason:
                lines.append(f"   <i>{alt_reason}</i>")

    if notable and notable.lower() not in SKIP_VALUES:
        lines += [
            "",
            "━━━━━━━━━━━━━━━━━━━━━━━━━",
            "",
            "🔎 <b>NOTABLE OSINT FINDS</b>",
            notable,
        ]

    if privacy_tip and privacy_tip.lower() not in SKIP_VALUES:
        lines += [
            "",
            "━━━━━━━━━━━━━━━━━━━━━━━━━",
            "",
            "🛡️ <b>PRIVACY TIP</b>",
            f"<i>The strongest clue in this photo:</i>",
            f"<b>{privacy_tip}</b>",
        ]

    lines += [
        "",
        "━━━━━━━━━━━━━━━━━━━━━━━━━",
        "<i>🤫 DontKenaDoxx • OSINT Geolocation Bot</i>",
    ]

    return "\n".join(lines)


def format_error(error_msg: str) -> str:
    return (
        "❌ <b>Analysis Failed</b>\n\n"
        f"<code>{_escape(error_msg[:300])}</code>\n\n"
        "Try sending a clearer, higher-resolution image lah."
    )


def format_low_quality_warning() -> str:
    return (
        "⚠️ <b>Image quality too low</b>\n\n"
        "Send a higher-resolution image for better OSINT results.\n"
        "Blurry, dark, or very small images cannot be analyzed properly."
    )
