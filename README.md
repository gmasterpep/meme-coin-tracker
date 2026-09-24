# Meme Coin Tracker

This repository is a starter framework for a Telegram-based crypto intelligence agent focused on Fomo-style wallet activity and new memecoin discovery.

It is designed to help you:
- monitor any configured Fomo wallets or profiles
- detect new coin buys and token launches
- analyze wallet quality and coin risk
- rank opportunities by expected profit potential
- send alerts through Telegram
- start with paper trading before enabling live strategy execution

Key idea:
- Fomo notifications are the trigger
- the agent independently evaluates both the wallet and the token before recommending action
- this reduces the risk of blindly copying hype-driven buys

## Architecture

- `app/bot.py` – Telegram bot entry point, commands, and message handling
- `app/config.py` – environment configuration and secrets
- `app/models.py` – structured objects used across the app
- `app/services/fomo_client.py` – interface for Fomo wallet/profile retrieval
- `app/services/wallet_score.py` – wallet quality and historical performance scoring
- `app/services/coin_analyzer.py` – token risk, utility, and opportunity analysis
- `app/services/alert_router.py` – combines wallet + token evaluation into a ranked signal
- `main.py` – app bootstrap

## Recommended rollout

1. Configure a Telegram bot and chat ID
2. Add a list of watchers (wallet addresses or Fomo profile names)
3. Start from paper-trade mode and Telegram alerts
4. Review the opportunity rankings
5. Add trade approval workflow
6. Only later enable limited live execution with strict risk caps

## Environment setup

1. Create a virtual environment
2. Install dependencies
3. Copy `.env.example` to `.env`
4. Fill in your bot token and config values

## Example commands

- `/start` – show the bot status
- `/watch add 0xabc...` – add a wallet to the watchlist
- `/watch list` – show tracked wallets
- `/status` – show the current system status
- `/rank` – show top ranked opportunities
- `/paper` – toggle paper-trading mode

## Important note

This repository is intentionally structured as a starter project and does not assume an official Fomo API exists. The Fomo integration layer is implemented as a clean interface so you can plug in whichever data source is available to you (official API, blockchain indexing, or webhook-based triggers), without rewriting the core logic.

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

## Disclaimer

This software is for research and analysis only. It does not guarantee profit, and memecoin trading is high risk. Use strict risk controls and paper trade before live execution.
