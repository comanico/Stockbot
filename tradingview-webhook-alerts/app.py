import requests, json
from chalice import Chalice

app = Chalice(app_name='tradingview-webhook-alerts')

API_KEY = 'PKCM8E23C7YRW0WZ4BT1'
SECRET_KEY = 'dsUthApfflZ56lv0IpzHmbFEP9T5XgjUntnV2Y7L'
BASE_URL = "https://paper-api.alpaca.markets"
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}


@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/buy_stock', methods=['POST'])
def buy_stock():
    request = app.current_request
    webhook_message = request.json_body
    data = {
        "symbol": webhook_message['ticker'],
        "qty": 1,
        "side": "buy",
        "type": "limit",
        "limit_price": webhook_message['close'], 
        "time_in_force": "gtc",
        "order_class": "bracket",
        "take_profit": {
            "limit_price": webhook_message['close'] * 1.1
        },
        "stop_loss": {
            "stop_price": webhook_message['close'] * 0.98,
        }
    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)
    response = json.loads(r.content)

    print(response)
    print(response.keys())   

    return {'message': 'Buy stock',
            'webhook_message': webhook_message}