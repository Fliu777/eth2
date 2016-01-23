import random
class VALETrader:

    def __init__(self,connection):
        self.connection=connection

        self.curLiquidPos=0
        pass

    def sendOrder(self, isBuy, name,amount, price):
        self.counter+=1
        buy_sell_msg = {
            "type": "ADD",
            "order_id": random.randint(3000,10000000),
            "symbol": name,
            "dir": None,
            "price": price,
            "size": amount,
        }
        if isBuy:
            buy_sell_msg['dir'] = "BUY"
            self.connection.send(buy_sell_msg)
        else:
            buy_sell_msg['dir'] = "SELL"
            self.connection.send(buy_sell_msg)
    def convert(self, isBuy, name,amount):
        buy_sell_msg = {
            "type": "CONVERT",
            "order_id": random.randint(3000,10000000),
            "symbol": "VALBZ",
            "dir": None,
            "size": amount,
        }
        if isBuy:
            buy_sell_msg['dir'] = "BUY"
            self.connection.send(buy_sell_msg)
        else:
            buy_sell_msg['dir'] = "SELL"
            self.connection.send(buy_sell_msg)

    def getOrderBooks(self, book):
        liquid=book['VALBZ']
        buypriceLiquid=liquid[0][0]
        sellpriceLiquid=liquid[1][0]
        nonLiquid=book['VALE']
        buypricenonLiquid=nonLiquid[0][0]
        sellpricenonLiquid=nonLiquid[1][0]

        #liquidValue=0 # getValue('VALBZ')
        #nonLiquid=0 #getValue('VALE')
        possibleProfit=0
        cost=10
        slippage=5
        most=10-self.LiquidPos
        # valbz is the liquid one
        if sellpriceLiquid-buypricenonLiquid>0:
            diff=sellpriceLiquid-buypricenonLiquid
            if diff*most-12 > 0:
                self.sendOrder(False, "VALBZ", most, sellpriceLiquid)            #buy the non liquid
                self.sendOrder(True, "VALE", most, buypricenonLiquid)              #sell liquid
                self.convert(False, most)

        if sellpricenonLiquid-buypriceLiquid>0:
            diff=sellpricenonLiquid-buypriceLiquid
            if diff*most-12 > 0:
                self.sendOrder(True, "VALBZ", most, buypriceLiquid)            #sell non liquid
                self.sendOrder(False, "VALE", most, sellpricenonLiquid)              #buy liquid
                self.convert(True, most)
    def fillOrder(self, obj): #stock is of type STOCK
        vol=int(obj['size'])
        if obj['dir']=="BUY":
            self.LiquidPos+=vol
        else:
            self.LiquidPos-=vol





