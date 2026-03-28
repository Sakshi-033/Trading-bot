import hmac
import hashlib
import time
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = "https://testnet.binancefuture.com"

api_key = os.getenv("BINANCE_API_KEY")
secret_key = os.getenv("BINANCE_SECRET_KEY")

def sign(params: dict) -> str:
    query_string = urlencode(params)
    signature = hmac.new(
        secret_key.encode("utf-8"),
        query_string.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    return signature

def send_request(method: str, endpoint: str, params: dict) -> dict:
    params["timestamp"] = int(time.time() * 1000)
    params["signature"] = sign(params)
    headers = {"X-MBX-APIKEY": api_key}
    url = BASE_URL + endpoint
    if method == "POST":
        response = requests.post(url, headers=headers, params=params)
    else:
        response = requests.get(url, headers=headers, params=params)
    return response.json()