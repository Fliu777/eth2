import random
import json

class BondHandler:
    connection=None
    buyOrder=True
    sellOrder=True
    counter=0
    currentPos=0

    def __init__(self, connection):
        BondHandler.connection=connection
        self.sendOrder(True, 100,999)
        self.sendOrder(False, 100,1001)
        pass


    def sendOrder(self, isBuy, amount, price):
        BondHandler.counter+=1
        buy_sell_msg = {
            "type": "add",
            "order_id": BondHandler.counter,
            "symbol": "BOND",
            "dir": None,
            "price": price,
            "size": amount,
        }
        if isBuy:
	        buy_sell_msg['dir'] = "BUY"
	        BondHandler.connection.send(json.dumps(buy_sell_msg))
        else:
	        buy_sell_msg['dir'] = "SELL"
	        BondHandler.connection.send(json.dumps(buy_sell_msg))

    def updatePrice(self, buyPrices=[], sellPrices=[]):
        if BondHandler.buyOrder:
            self.sendOrder(True,100,999)
            #buyOrder=False
        if BondHandler.buyOrder and len(sellPrices)>0 and sellPrices[0][0]>=1000:
            #sell at 1000, which is fair value
            self.sendOrder(False,1,sellPrices[0][0])
        elif BondHandler.sellOrder:
            self.sendOrder(False,1,1001)
    def handleBook(self, book):
        last=book[-1]
        buySide=last[0]
        sellSide=last[1]
        #clear 1ks
        for order in buySide:
            if order[0]==1000:
                if BondHandler.currentPos-order[1] <-90:
                    BondHandler.sendOrder(False,order[0],1000)
        for order in sellSide:
            if order[0]==1000:
                if BondHandler.currentPos+order[1] >90:
                    BondHandler.sendOrder(True,order[0],1000)
        if BondHandler.counter%10==0:
            BondHandler.sendOrder(False,1,1001)
            BondHandler.sendOrder(True,1,999)

    def fillOrder(self, obj): #stock is of type STOCK
        vol=int(obj['size'])
        if obj['dir']=="BUY":
            BondHandler.currentPos+=vol
        else:
            BondHandler.currentPos-=vol

        BondHandler.buyOrder=BondHandler.sellOrder=True
        if BondHandler.currentPos>75:
            BondHandler.sendOrder(False,BondHandler.currentPos/2,1000)
        elif BondHandler.currentPos<-75:
            BondHandler.sendOrder(True,-BondHandler.currentPos/2,1000)
        elif BondHandler.currentPos==100:
            BondHandler.buyOrder=False
        elif BondHandler.currentPos==-100:
            BondHandler.sellOrder=False
        else:
            BondHandler.updatePrice()
            #cant do anything

