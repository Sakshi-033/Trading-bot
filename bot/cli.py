import argparse
from bot.validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price
from bot.orders import place_order
from bot.logging_config import logger

def interactive_mode():
    print("\nWelcome to Binance Futures Trading Bot!")
    print("==========================================\n")

    symbol = input("Enter symbol (e.g. BTCUSDT): ").strip()
    side = input("Enter side (BUY or SELL): ").strip()
    order_type = input("Enter order type (MARKET or LIMIT): ").strip()
    quantity = input("Enter quantity (e.g. 0.002): ").strip()

    price = None
    if order_type.upper() == "LIMIT":
        price = input("Enter price: ").strip()

    try:
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        order_type = validate_order_type(order_type)
        quantity = validate_quantity(quantity)
        if price:
            price = validate_price(price)

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
        print(f"Error: {e}")
    except Exception as e:
        print(f"Something went wrong: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        interactive_mode()
    else:
        main()