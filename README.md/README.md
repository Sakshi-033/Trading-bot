# Binance Futures Trading Bot

A Python CLI app to place orders on Binance Futures Testnet (USDT-M).

## Setup

1. Clone the repo
2. Create a virtual environment:
   python -m venv venv
   venv\Scripts\activate
3. Install dependencies:
   pip install -r requirements.txt
4. Create a .env file with your API keys:
   BINANCE_API_KEY=your_key_here
   BINANCE_SECRET_KEY=your_secret_here

## How to Run

Market order:
   python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002

Limit order:
   python -m bot.cli --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.002 --price 70000

## Project Structure

   bot/
     client.py        # Binance API client, signing, requests
     orders.py        # Order placement logic
     validators.py    # Input validation
     logging_config.py # Logging setup
     cli.py           # CLI entry point

## Assumptions

- Uses Binance Futures Testnet only
- Minimum order value is 100 USDT
- LIMIT orders require --price argument