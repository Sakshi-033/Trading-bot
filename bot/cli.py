import argparse
from bot.validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price
from bot.orders import place_order
from bot.logging_config import logger

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Trading Bot")
    parser.add_argument("--symbol", required=True, help="Trading pair e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--type", dest="order_type", required=True, help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, help="Order quantity e.g. 0.001")
    parser.add_argument("--price", required=False, help="Price for LIMIT orders")

    args = parser.parse_args()

    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity = validate_quantity(args.quantity)

        price = None
        if order_type == "LIMIT":
            if not args.price:
                raise ValueError("Price is required for LIMIT orders.")
            price = validate_price(args.price)

        print(f"\n--- Order Request ---")
        print(f"Symbol   : {symbol}")
        print(f"Side     : {side}")
        print(f"Type     : {order_type}")
        print(f"Quantity : {quantity}")
        if price:
            print(f"Price    : {price}")
        print("---------------------\n")

        response = place_order(symbol, side, order_type, quantity, price)

        print(f"\n--- Order Response ---")
        print(f"Order ID    : {response.get('orderId', 'N/A')}")
        print(f"Status      : {response.get('status', 'N/A')}")
        print(f"Executed Qty: {response.get('executedQty', 'N/A')}")
        print(f"Avg Price   : {response.get('avgPrice', 'N/A')}")
        print("----------------------\n")

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        print(f"Error: {e}")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"Something went wrong: {e}")

if __name__ == "__main__":
    main()