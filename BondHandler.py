import random
import json

class BondHandler:


    def __init__(self, connection):
        self.connection=connection

        self.buyOrder=True
        self.sellOrder=True
        self.counter=0
        self.currentPos=0
        self.sendOrder(True, 100,999)
        self.sendOrder(False, 100,1001)
        pass


    def sendOrder(self, isBuy, amount, price):
        self.counter+=1
        buy_sell_msg = {
            "type": "add",
            "order_id": self.counter,
            "symbol": "BOND",
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

    def floodMarket(self):
    	#print ("Flooding")
        self.sendOrder(True,1,999)
        self.sendOrder(False,1,1001)

    def updatePrice(self, buyPrices=[], sellPrices=[]):
        if True:
            self.sendOrder(True,1,999)
            #buyOrder=False
        if self.buyOrder and len(sellPrices)>0 and sellPrices[0][0]>=1000:
            #sell at 1000, which is fair value
            self.sendOrder(False,1,sellPrices[0][0])
        else:
            self.sendOrder(False,1,1001)
    def handleBook(self, book, update_for):
        if update_for is not "BOND":
	    return 
        bond_book = book['BOND']
        buySide=bond_book[-1][0]
	sellSide=bond_book[-1][1]
        #clear 1ks
        for order in buySide:
            if order[0]==1000:
                if self.currentPos-order[1] >-10:
		    print ("Selling at 1000")
                    self.sendOrder(False,order[1],1000)
        for order in sellSide:
            if order[0]==1000:
                if self.currentPos+order[1] <10:
		    print ("Buying at 1000")
                    self.sendOrder(True,order[1],1000)
        #self.sendOrder(False,1,1001)
        #self.sendOrder(True,1,999)

    def fillOrder(self, obj): #stock is of type STOCK
        vol=int(obj['size'])
        if obj['dir']=="BUY":
            self.currentPos+=vol
        else:
            self.currentPos-=vol

        self.buyOrder=self.sellOrder=True
        if self.currentPos>75:
            self.sendOrder(False,self.currentPos/2,1000)
        elif self.currentPos<-75:
            self.sendOrder(True,-self.currentPos/2,1000)
        elif self.currentPos==100:
            self.buyOrder=False
        elif self.currentPos==-100:
            self.sellOrder=False
        else:
            self.updatePrice()
            #cant do anything

	if self.currentPos>0:
	    self.sendOrder(True, 100 - self.currentPos, 999)
	else:
	    self.sendOrder(True, 10, 999)

	if self.currentPos<0:
	    self.sendOrder(False, - self.currentPos + 100, 1001)
	else:
	    self.sendOrder(False, 10, 1001)
