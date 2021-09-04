from exchanges.binance import BinanceClient
from strategies.indicadores import bbands, atr, rsi, personal_bbands, personal_atr

import logging

import requests

def telegram_bot_sendtext(bot_message):
    
    bot_token = '1797275370:AAHK6UumSS2FYyXDwoycxiUFr5un0b5sZak'
    bot_chatID = '886478914'
    try:
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        requests.get(send_text)
        print(bot_message)
    except:
        print(bot_message)

logger = logging.getLogger()

logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

binance = BinanceClient(False)
interaction = 1

while interaction != 0:
    print(interaction)
    coin_in_upper = dict()
    coin_in_upper["coins"] = []
    coin_in_upper["amount"] = 0
    coin_in_upper_middle = dict()
    coin_in_upper_middle["coins"] = []
    coin_in_upper_middle["amount"] = 0
    coin_in_middle_lower = dict()
    coin_in_middle_lower["coins"] = []
    coin_in_middle_lower["amount"] = 0
    coin_in_lower = dict()
    coin_in_lower["coins"] = []
    coin_in_lower["amount"] = 0

    contracts = binance.get_contracts()
    if contracts is not None:
        for contract in contracts:
            candle15 = binance.get_historical_candles(contract,"15m",100)
            upperband15, middleband15, lowerband15 = bbands(candle15,21)
            market_price = binance.market_price_symbol(contract)
            if len(upperband15)>=100 and market_price >= upperband15[99]:
                print(contract)
                print(upperband15[99])
                coin_in_upper["amount"] = coin_in_upper["amount"] + 1
                coin_in_upper["coins"].append(contract)
                candle30 = binance.get_historical_candles(contract,"30m",100)
                upperband30, middleband30, lowerband30 = bbands(candle30,21)
                if len(upperband30)>=100 and market_price >= upperband30[99]:
                    candle = binance.get_historical_candles(contract,"1h",100)
                    if len(candle["close"]) >= 100:
                        upperband, middleband, lowerband = personal_bbands(candle,21)
                        atr15 = atr(candle15,14)
                        atr60 = atr(candle,14)
                        entrada1 = upperband15[99] + atr60
                        entrada2 = upperband[99] + atr60
                        saida1 = upperband[99] - (atr15/2)
                        saida2 = upperband[99] - atr15
                        stop=0
                        if entrada1 > entrada2:
                            candle["close"].append(entrada1)
                            stop = entrada1 + atr60
                            print(entrada1)
                        else:
                            candle["close"].append(entrada2)
                            stop = entrada2 + atr60
                            print(entrada2)
                        print(rsi(candle,14))
                        print(stop)
                        if len(upperband)>=100 and market_price >= upperband[99] and rsi(candle,14) >= 80:
                            entrada1 = upperband[99] + atr15
                            entrada2 = upperband[99] + atr60
                            saida1 = upperband[99] - (atr15/2)
                            saida2 = upperband[99] - atr15
                            mensagem = "COIN IN SETUP UPPER: "+ contract + "\nENTRADAS: \n"+ str(round(entrada1,6))+"\n"+str(round(entrada2,6))+"\nSAIDAS: \n"+str(round(saida1,6))+"\n"+str(round(saida2,6))+"\nSTOP: \n"+str(stop)
                            telegram_bot_sendtext(mensagem)
            if upperband15[99] >= market_price >= middleband15[99]:
                coin_in_upper_middle["amount"] = coin_in_upper_middle["amount"] + 1
                coin_in_upper_middle["coins"].append(contract)
            if middleband15[99] >= market_price >= lowerband15[99]:
                coin_in_middle_lower["amount"] = coin_in_middle_lower["amount"] +1
                coin_in_middle_lower["coins"].append(contract)
            if lowerband15[99] >= market_price:
                coin_in_lower["amount"] = coin_in_lower["amount"] + 1
                coin_in_lower["coins"].append(contract)
        mensagem = "COINS ACIMA DA UPPER BB: "+str(coin_in_upper["amount"])+"\nCOINS ENTRE UPPER E MIDDLE BB: "+str(coin_in_upper_middle["amount"])+"\nCOINS ENTRE MIDDLE E LOWER DA BB: "+str(coin_in_middle_lower["amount"])+"\nCOINS ABAIXO DA LOWER BB: "+str(coin_in_lower["amount"])
        telegram_bot_sendtext(mensagem)
        print(coin_in_upper["coins"])
        print(coin_in_upper_middle["coins"])
        print(coin_in_middle_lower["coins"])
        print(coin_in_lower["coins"])
        interaction = interaction +1
            