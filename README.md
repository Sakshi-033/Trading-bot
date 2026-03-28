# Binance Futures Trading Bot

A Python CLI app to place orders on Binance Futures Testnet (USDT-M).

## Setup

1. Clone the repo
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate`
4. Install: `pip install -r requirements.txt`
5. Create `.env` file with your API keys:
   - BINANCE_API_KEY=your_key
   - BINANCE_SECRET_KEY=your_secret

## How to Run

Market order:
`python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002`

Limit order:
`python -m bot.cli --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.002 --price 70000`

Interactive mode:
`python -m bot.cli`

## Project Structure

- `bot/client.py` — Binance API client
- `bot/orders.py` — Order placement
- `bot/validators.py` — Input validation
- `bot/logging_config.py` — Logging setup
- `bot/cli.py` — CLI entry point

## Assumptions

- Uses Binance Futures Testnet only
- Minimum order value is 100 USDT
- LIMIT orders require --price argument