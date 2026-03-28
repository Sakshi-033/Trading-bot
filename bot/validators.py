def validate_symbol(symbol: str) -> str:
    symbol = symbol.upper().strip()
    if not symbol.endswith("USDT"):
        raise ValueError(f"Symbol must end with USDT. Got: {symbol}")
    return symbol

def validate_side(side: str) -> str:
    side = side.upper().strip()
    if side not in ["BUY", "SELL"]:
        raise ValueError(f"Side must be BUY or SELL. Got: {side}")
    return side

def validate_order_type(order_type: str) -> str:
    order_type = order_type.upper().strip()
    if order_type not in ["MARKET", "LIMIT"]:
        raise ValueError(f"Order type must be MARKET or LIMIT. Got: {order_type}")
    return order_type

def validate_quantity(quantity: str) -> float:
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValueError("Quantity must be greater than zero.")
        return qty
    except ValueError:
        raise ValueError(f"Invalid quantity: {quantity}")

def validate_price(price: str) -> float:
    try:
        p = float(price)
        if p <= 0:
            raise ValueError("Price must be greater than zero.")
        return p
    except ValueError:
        raise ValueError(f"Invalid price: {price}")