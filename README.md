# 🗺️ DontKenaDoxx — OSINT Geolocation Telegram Bot

> *"Don't kena doxxed — but here's how your photo gives away your location anyway."*

A Telegram bot that identifies the geographic location of any photo using Claude Vision and systematic OSINT methodology. Analyzes 10 categories of visual evidence and returns a structured location report with confidence rating.

---

## ✨ Features

- 📸 **Handles all photo types** — compressed, full-res documents, forwarded photos
- 🔍 **10-category OSINT analysis** — text, architecture, roads, vegetation, vehicles, infrastructure, culture, environment, people, brands
- 🎯 **Confidence scoring** — explicit percentage + label + color indicator
- 📊 **Alternative locations** — top 3 possibilities with reasoning
- 🏆 **Key evidence summary** — the 3 strongest determining clues
- 🔎 **Notable OSINT finds** — any actionable specifics (readable signs, addresses, etc.)
- ⏳ **Rate limiting** — 30s per user cooldown to prevent API burn

---

## 🛠️ Setup

### Prerequisites
- Python 3.12+
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- Anthropic API key

### Local Development

```bash
# 1. Clone the repo
git clone https://github.com/TheBooleanJulian/dontkenadoxx.git
cd dontkenadoxx

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
cp .env.example .env
# Edit .env with your actual tokens

# 4. Run
python bot.py
```

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | ✅ | Bot token from @BotFather |
| `ANTHROPIC_API_KEY` | ✅ | Anthropic API key |
| `CLAUDE_MODEL` | ❌ | Model to use (default: `claude-sonnet-4-6`) |

**Model options:**
- `claude-sonnet-4-6` — Fast, cost-effective (default)
- `claude-opus-4-8` — Best accuracy, higher cost — recommended for serious OSINT

---

## 🚀 Deployment (Zeabur)

1. Push to GitHub
2. Create new Zeabur project → deploy from GitHub repo
3. Set environment variables in Zeabur dashboard
4. Done — Zeabur auto-deploys on `main` branch push

**CI/CD pipeline:** `git push origin dev` → GitHub Actions smoke test → auto-merge to `main` → Zeabur deploys

---

## 🏗️ Architecture

```
dontkenadoxx/
├── bot.py                     # Entry point, handler registration
├── handlers/
│   ├── commands.py            # /start, /help
│   └── photo.py              # Photo handler + rate limiting
├── utils/
│   ├── analyzer.py           # Claude Vision + OSINT system prompt
│   └── formatter.py          # Telegram HTML message formatting
├── .github/workflows/ci.yml  # CI/CD pipeline
├── Dockerfile                # Container deployment
└── requirements.txt
```

### OSINT Analysis Flow

```
User sends photo
       │
       ▼
Download image bytes
       │
       ▼
Claude Vision API (10-category OSINT prompt)
       │
       ▼
Parse JSON response
       │
       ▼
Format → Telegram HTML message
       │
       ▼
Edit status message with result
```

---

## 🔍 OSINT Categories

| # | Category | What it detects |
|---|---|---|
| 1 | 📝 Text & Signage | Language, scripts, business names, license plates |
| 2 | 🏗️ Architecture | Style, materials, era, HDB vs private |
| 3 | 🛣️ Road Infrastructure | LHD/RHD traffic, sign conventions, road markings |
| 4 | 🌿 Vegetation | Plant species, terrain, climate zone |
| 5 | 🚗 Vehicles | Car brands, plate formats, transport types |
| 6 | ⚡ Infrastructure | Power poles, cabling, street lights |
| 7 | 🕌 Cultural | Temples, mosques, flags, hawker centers |
| 8 | ☁️ Environment | Weather, humidity, sun angle, season |
| 9 | 👥 People | Ethnicity, clothing, cultural dress |
| 10 | 🏪 Brands | Local chains, franchise adaptations |

---

## 📄 License

MIT — use freely, credit appreciated.

---

*Built by [@TheBooleanJulian](https://t.me/TheBooleanJulian) • Part of the Miku bot fleet 🎤*
