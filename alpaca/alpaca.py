import os
import requests, json
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
ORDERS_URL = "{}/v2/orders".format(BASE_URL)

# Function to get account information
def get_account():
    r = requests.get(ACCOUNT_URL, headers={'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY})
    return json.loads(r.content)

# Function to create an order
def create_order(symbol, qty, side, type, time_in_force):
    # Define the order data
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": type,
        "time_in_force": time_in_force
    }
    r = requests.post(ORDERS_URL, json=data, headers={'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY})
    print(r.content)
    return json.loads(r.content)

# response = create_order('AAPL', 1, 'buy', 'market', 'gtc')
# print(response)