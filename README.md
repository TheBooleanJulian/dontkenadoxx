<div align="center">

# DontKenaDoxx

**Telegram bot that geolocates any photo using Claude Vision and 10-category OSINT analysis.**

![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/-Telegram-26A5E4?logo=telegram&logoColor=white)
![Claude](https://img.shields.io/badge/-Claude%20API-D97757)
![Zeabur](https://img.shields.io/badge/-Zeabur-6C5CE7)
![License](https://img.shields.io/badge/license-AGPLv3%20%2B%20Commercial-00D4C8.svg)

</div>

---

## What it does

DontKenaDoxx is a Telegram bot that takes any photo and tells you where it was taken — without needing GPS metadata. It passes the image to Claude Vision with a structured OSINT prompt covering 10 categories of visual evidence (text, architecture, vehicles, vegetation, culture, and more), then returns a formatted location report with a confidence score, top 3 alternative locations, and the strongest determining clues. Built for anyone curious about geolocation tradecraft or wanting to understand how much a photo gives away.

## Features

- Handles compressed photos, full-res documents, and forwarded images
- 10-category OSINT analysis: text/signage, architecture, roads, vegetation, vehicles, infrastructure, culture, environment, people, brands
- Confidence scoring — explicit percentage, label, and color indicator
- Top 3 alternative locations with reasoning
- Key evidence summary — the 3 strongest determining clues
- Notable OSINT finds — any actionable specifics such as readable addresses or license plates
- Per-user rate limiting (30s cooldown) to prevent API burn

## Tech Stack

| Layer | Choice |
|---|---|
| Bot | python-telegram-bot (polling) |
| AI | Claude API (Anthropic) |
| Hosting | Zeabur (GitHub CI/CD, dev → main) |

## Quick Start

```bash
git clone https://github.com/TheBooleanJulian/dontkenadoxx.git
cd dontkenadoxx
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your tokens
python bot.py
```

## Configuration

| Variable | Required | Description |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | ✅ | Bot token from @BotFather |
| `ANTHROPIC_API_KEY` | ✅ | Anthropic API key |
| `CLAUDE_MODEL` | ❌ | Model to use (default: `claude-sonnet-4-6`) |

**Model options:**
- `claude-sonnet-4-6` — Fast, cost-effective (default)
- `claude-opus-4-8` — Best accuracy, higher cost — recommended for serious OSINT

## Project Structure

```
dontkenadoxx/
├── bot.py                  # Entry point, handler registration
├── handlers/
│   ├── commands.py         # /start, /help
│   └── photo.py            # Photo handler + rate limiting
├── utils/
│   ├── analyzer.py         # Claude Vision + OSINT system prompt
│   └── formatter.py        # Telegram HTML message formatting
├── .github/workflows/      # CI/CD pipeline
├── Dockerfile
└── requirements.txt
```

## Deployment

Deployed on Zeabur via GitHub Actions CI/CD. Push to `dev` triggers a smoke test, auto-merges to `main`, and Zeabur deploys from there. Set `TELEGRAM_BOT_TOKEN` and `ANTHROPIC_API_KEY` in the Zeabur dashboard environment variables.

## Screenshots

_Screenshots coming soon._

## Status / Roadmap

- [x] 10-category OSINT analysis via Claude Vision
- [x] Confidence scoring and alternative locations
- [x] Rate limiting per user
- [x] Dockerised deployment on Zeabur
- [ ] Reverse image search integration
- [ ] `/history` command to review past analyses

## Changelog

- **2026-06-03** — Initial release: full bot with Claude Vision OSINT analysis, 10-category prompt, confidence scoring, rate limiting, Dockerfile, and CI/CD pipeline. Repo rename typo fix (dontkenadobxx → dontkenadoxx).

## License

This project is dual licensed.

- Community Edition — [GNU Affero General Public License v3 (AGPLv3)](LICENSE). Free to use, modify, and self-host. If you distribute a modified version or run it as a network service, you must make the corresponding source available.
- Commercial License — for organisations that want to embed, modify, or distribute this software without AGPLv3's obligations. See [COMMERCIAL-LICENSE.md](COMMERCIAL-LICENSE.md).

---

<div align="center">
<sub>Built by <a href="https://github.com/TheBooleanJulian">@TheBooleanJulian</a></sub>
</div>