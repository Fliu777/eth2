import random
class VALETrader:
    def __init__(self,connection):
        print("wtf")
        self.connection=connection
        self.VALEcurLiquidPos=0
        self.VALBZcurLiquidPos=0

        print ("starting?")

    def sendOrder(self, isBuy, name,amount, price):
        buy_sell_msg = {
            "type": "add",
            "order_id": random.randint(10000,1000000),
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
    def convert(self, isBuy,amount):
        #return
        buy_sell_msg = {
            "type": "convert",
            "order_id": random.randint(10000,1000000),
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
        if 'VALBZ' not in book or 'VALE' not in book:
            return
        liquid=book['VALBZ']
        nonLiquid=book['VALE']
        if len(liquid[-1][0]) == 0 or len(liquid[-1][1]) == 0 or len(nonLiquid[-1][0]) == 0 or len(nonLiquid[-1][1]) == 0:
            return

        #print (liquid[-1])
        buypriceLiquid=liquid[-1][0][0][0]
        sellpriceLiquid=liquid[-1][1][0][0]

        #print (nonLiquid)
        buypricenonLiquid=nonLiquid[-1][0][0][0]
        sellpricenonLiquid=nonLiquid[-1][1][0][0]
        print (self.VALEcurLiquidPos)
        print (self.VALBZcurLiquidPos)
        if self.VALEcurLiquidPos>0:
            self.sendOrder(False, "VALE", self.VALEcurLiquidPos, sellpricenonLiquid)
            print("dump extra VALE")
        elif self.VALEcurLiquidPos<0:
            self.sendOrder(True, "VALE", self.VALEcurLiquidPos, buypricenonLiquid)
            print("dump extra VALE")

        if self.VALBZcurLiquidPos>0:
            self.sendOrder(False, "VALBZ", self.VALBZcurLiquidPos, sellpriceLiquid)
            print("dump extra VALBZ")

        elif self.VALBZcurLiquidPos<0:
            self.sendOrder(True, "VALBZ", self.VALBZcurLiquidPos, buypriceLiquid)
            print("dump extra VALBZ")

        #print(buypricenonLiquid)
        #print(buypriceLiquid)

        #liquidValue=0 # getValue('VALBZ')
        #nonLiquid=0 #getValue('VALE')
        possibleProfit=0
        cost=10
        slippage=5
        most=3
        # valbz is the liquid one
        if buypriceLiquid-buypricenonLiquid>0:
            diff=buypriceLiquid-sellpricenonLiquid
            if diff*most-10 > 0:
                self.sendOrder(False, "VALBZ", most, buypriceLiquid )            #buy the non liquid
                self.sendOrder(True, "VALE", most, buypricenonLiquid)              #sell liquid
                self.convert(False, most)
                print("doing smth")

        if buypricenonLiquid-buypriceLiquid>0:
            diff=buypricenonLiquid-sellpriceLiquid
            if diff*most-10 > 0:
                self.sendOrder(True, "VALBZ", most, buypricenonLiquid )            #buy the non liquid
                self.sendOrder(False, "VALE", most, buypriceLiquid)              #sell liquid
                self.convert(True, most)
                print("doing smth")

    def fillOrder(self, obj): #stock is of type STOCK
        vol=int(obj['size'])
        print("filled ")
        print(obj)
        if obj['symbol']=='VALE':

            if obj['dir']=="BUY":
                self.VALEcurLiquidPos+=vol
            else:
                self.VALEcurLiquidPos-=vol
        else:
            if obj['dir']=="BUY":
                self.VALBZcurLiquidPos+=vol
            else:
                self.VALBZcurLiquidPos-=vol





