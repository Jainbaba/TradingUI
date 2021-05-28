import hashlib
import hmac
import json
import logging
import ssl
import threading
import time
from urllib.parse import urlencode

import requests
import websocket

logger = logging.getLogger()


# def get_contracts():
#     reponse_object = requests.get("https://testnet.binance.vision'/api/v3/exchangeInfo'")
#     contracts = []
#     for contract in reponse_object.json()["symbols"]:
#         contracts.append(contract['symbol'])
#     return contracts


class BinanceSpotClient:
    def __init__(self, public_key, secret_key, testnet):
        if testnet:
            self.base_url = "https://testnet.binance.vision"
            self.wss_url = 'wss://testnet.binance.vision/ws'
        else:
            self.base_url = "https://api.binance.com"
            self.wss_url = 'wss://stream.binance.com:9443/ws'

        self.public_key = public_key
        self.secret_key = secret_key

        self.header = {'X-MBX-APIKEY': self.public_key}
        self.ws = None
        self.prices = dict()
        self.id = 1
        t = threading.Thread(target=self.start_ws)
        t.start()
        logger.info("Binance Spot Client successfully initialized")

    def generate_signature(self, data):
        return hmac.new(self.secret_key.encode(), urlencode(data).encode(), hashlib.sha256).hexdigest()

    def make_request(self, method, endpoint, data):
        if method == 'GET':
            response = requests.get(self.base_url + endpoint, params=data, headers=self.header)
        elif method == 'POST':
            response = requests.post(self.base_url + endpoint, params=data, headers=self.header)
        elif method == 'DELETE':
            response = requests.delete(self.base_url + endpoint, params=data, headers=self.header)
        else:
            raise ValueError()

        if response.status_code == 200:
            return response.json()
        else:
            logger.error("Error while making %s request to %s: %s(error code %s)", method, endpoint, response.json(),
                         response.status_code)
            return None

    def get_contracts(self):
        exchange_info = self.make_request('GET', '/api/v3/exchangeInfo', None)
        contracts = dict()
        if exchange_info is not None:
            for contract_data in exchange_info["symbols"]:
                contracts[contract_data['symbol']] = contract_data
        return contracts

    def get_historical_candles(self, symbol, interval):
        data = dict()
        data['symbol'] = symbol
        data['interval'] = interval
        data['limit'] = 1000
        raw_candles = self.make_request('GET', '/api/v3/klines', data)

        candles = []

        if raw_candles is not None:
            for c in raw_candles:
                candles.append([c[0], float(c[1]), float(c[2]), float(c[3]), float(c[4]), float(c[5])])

        return candles

    def get_bid_ask(self, symbol):
        data = dict()
        data['symbol'] = symbol
        bid_ask_info = self.make_request('GET', '/api/v3/ticker/bookTicker', data)

        if bid_ask_info is not None:
            if symbol not in self.prices:
                self.prices[symbol] = {'bid': float(bid_ask_info["bidPrice"]), 'bidQty': float(bid_ask_info["bidQty"])
                    , 'ask': float(bid_ask_info["askPrice"]), 'askQty': float(bid_ask_info["askQty"])}
            else:
                self.prices[symbol]["bid"] = float(bid_ask_info["bidPrice"])
                self.prices[symbol]['bidQty'] = float(bid_ask_info["bidQty"])
                self.prices[symbol]["ask"] = float(bid_ask_info["askPrice"])
                self.prices[symbol]['askQty'] = float(bid_ask_info["askQty"])

        return self.prices

    def get_balances(self):
        data = dict()
        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self.generate_signature(data)
        balances = dict()
        account_data = self.make_request('GET', '/api/v3/account', data)

        if account_data is not None:
            for a in account_data['balances']:
                balances[a['asset']] = a
        return balances

    def place_order(self, symbol, side, quantity, order_type, price=None, tif=None):
        data = dict()
        data['symbol'] = symbol
        data['side'] = side
        data['quantity'] = quantity
        data['type'] = order_type

        if price is not None:
            data['price'] = price
        if tif is not None:
            data['timeInForce'] = tif

        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self.generate_signature(data)

        order_status = self.make_request('POST', '/api/v3/order', data)
        return order_status

    def cancel_order(self, symbol, order_id):
        data = dict()
        data['symbol'] = symbol
        data['orderId'] = order_id
        data['timestamp'] = int(time.time() * 1000)
        data['signature'] = self.generate_signature(data)

        order_status = self.make_request('DELETE', '/api/v3/order', data)
        return order_status

    def get_order_status(self, symbol, order_id):
        data = dict()
        data['timestamp'] = int(time.time() * 1000)
        data['symbol'] = symbol
        data['orderId'] = order_id
        data['signature'] = self.generate_signature(data)

        order_status = self.make_request('GET', '/api/v3/order', data)
        return order_status

    def start_ws(self):
        self.ws = websocket.WebSocketApp(self.wss_url, on_open=self.on_open, on_close=self.on_close,
                                         on_error=self.on_error, on_message=self.on_message)
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        return

    def on_open(self, ws):
        logger.info("Binance Websocket connection opened")

        self.subscribe_channel('BNBUSDT')

    def on_close(self, ws):
        logger.warning("Binance Websocket connection closed")

    def on_error(self, ws, msg):
        logger.error("Binance connection error: %s", msg)

    def on_message(self, ms, msg):
        data = json.loads(msg)
        if 'u' in data:
            symbol = data['s']

            if symbol not in self.prices:
                self.prices[symbol] = {'bid': float(data["b"]), 'bidQty': float(data["B"])
                    , 'ask': float(data["a"]), 'askQty': float(data["A"])}
            else:
                self.prices[symbol]["bid"] = float(data["b"])
                self.prices[symbol]['bidQty'] = float(data["B"])
                self.prices[symbol]["ask"] = float(data["a"])
                self.prices[symbol]['askQty'] = float(data["A"])

            print(self.prices[symbol])

    def subscribe_channel(self, symbol):
        data = dict()
        data['method'] = 'SUBSCRIBE'
        data['params'] = []
        data['params'].append(symbol.lower() + '@bookTicker')
        data['id'] = self.id
        self.ws.send(json.dumps(data))
        self.id += 1
