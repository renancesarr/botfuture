import logging
import requests
from requests.sessions import TooManyRedirects


logger = logging.getLogger()

class BinanceClient:
    def __init__(self, testnet):
        if testnet:
            self.base_url = "https://testnet.binancefuture.com"
            connect = self.make_request("GET", "/fapi/v1/ping", None)
        
            if connect is not None:
                logger.info("Cliente inicializado no modo de teste")
        else:
            self.base_url = "https://fapi.binance.com"
            connect = self.make_request("GET", "/fapi/v1/ping", None)
        
            if connect is not None:
                logger.info("Cliente inicializado no modo real")
            
            
    def make_request(self, method, endpoint, data):
        if method == "GET":
            try:
                response = requests.get(self.base_url+endpoint, params=data)
            except ConnectionError :
                logger.error("Verifique a conexâo.")
            except TimeoutError :
                logger.error("O servidor demorou muito para responder")
            except TooManyRedirects:
                logger.error("O servidor demorou muito para responder")
            else:
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.error("Erro % enquanto tentava fazer get no endpoint: %s", response.status_code, endpoint)
                    return None
        else:
            raise ValueError
        
    
    def get_contracts(self):
        exchange_info = self.make_request("GET", "/fapi/v1/exchangeInfo", None)
        
        contracts = []
        
        if exchange_info is not None:
            for contract_data in exchange_info['symbols']:
                if contract_data["contractType"] == "PERPETUAL" and contract_data["quoteAsset"] == "USDT":
                    contracts.append(contract_data['pair'])
            return contracts
        else:
            return None
            
    def get_historical_candles(self, symbol, interval, limit):
        data = dict()
        data['symbol'] = symbol
        data['interval']=interval
        data['limit'] = limit
        raw_candles = self.make_request("GET", "/fapi/v1/markPriceKlines", data)
        
        candles = dict()
        candles['openTime'] = []
        candles['open'] = []
        candles['high'] = []
        candles['low'] = []
        candles['close'] = []
        
        if raw_candles is not None:
            for c in raw_candles:
                candles["openTime"].append(c[0])
                candles["open"].append(float(c[1]))
                candles["high"].append(float(c[2]))
                candles["low"].append(float(c[3]))
                candles["close"].append(float(c[4]))
            return candles
        else:
            return None
        
    def market_price_symbol(self, symbol):
        data = dict()
        data['symbol'] = symbol
        
        ob_data = self.make_request("GET", "/fapi/v1/premiumIndex", data)
        if ob_data is not None:
            price = float(ob_data['markPrice'])
            return price
        else:
            return None
                
        
        