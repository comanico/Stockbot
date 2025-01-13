import os
import json
import threading
from spender import Spender
from discordObserver import discordObserver
from alpacaObserver import alpacaObserver

def process_data(data):
    
    side = data['message'][0].lower() if data['message'][0] == "Buy" or data['message'][0] == "Sell" else data['message'][0]
    
    # Start subject which is Spender
    spender = Spender()

    # Start Discord Observer
    discord = discordObserver()
    alpaca = alpacaObserver(data['ticker'][0], 1, side, "market", "gtc")

    # Start Alpaca Observer
    spender.attach(alpaca)
    spender.attach(discord)

    if side == "buy":
        spender.buy()
    elif side == "sell":
        spender.sell()
    else:
        spender.detach(alpaca)


def main():
    files = os.listdir('public')
    all_json_data = []

    for file_name in files:
        file_path = os.path.join('public', file_name)
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            all_json_data.append(json_data)

    threads = []
    for data in all_json_data:
        thread = threading.Thread(target=process_data, args=(data,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()