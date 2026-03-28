from bot.client import send_request
from bot.logging_config import logger

def place_order(symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> dict:
    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }

    if order_type == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"

    logger.info(f"Placing {order_type} {side} order for {quantity} {symbol}")

    response = send_request("POST", "/fapi/v1/order", params)

    if "orderId" in response:
        logger.info(f"Order successful! ID: {response['orderId']} | Status: {response['status']}")
    else:
        logger.error(f"Order failed: {response}")

    return response