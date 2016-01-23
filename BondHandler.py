import random

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

    def send(self):
        BondHandler.BondHandler(client)
        

    def sendOrder(self, isBuy, amount, price):
        if isBuy:
            BondHandler.counter+=1
            self.send(str(BondHandler.counter),str(price), str(amount))
            #BondHandler.connection.send("ADD "+str(BondHandler.counter)+" BOND BUY "+str(price)+" "+str(amount))
        else:
            BondHandler.counter+=1
            self.send(str(BondHandler.counter),str(price), str(amount))
            
            #BondHandler.connection.send("ADD "+str(BondHandler.counter)+" BOND SELL "+str(price)+" "+str(amount))
        pass
    def updatePrice(self, buyPrices=[], sellPrices=[]):
        if BondHandler.buyOrder:
            self.sendOrder(True,1,999)
            #buyOrder=False
        if BondHandler.buyOrder and len(sellPrices)>0 and sellPrices[0][0]>=1000:
            #sell at 1000, which is fair value
            self.sendOrder(False,1,sellPrices[0][0])
        elif BondHandler.sellOrder:
            self.sendOrder(False,1,1001)

    def fillOrder(self, obj): #stock is of type STOCK
        vol=int(obj['size'])
        if obj['dir']=="BUY":
            BondHandler.currentPos+=vol
        else:
            BondHandler.currentPos-=vol
        BondHandler.buyOrder=BondHandler.sellOrder=True
        if BondHandler.currentPos>75:
            BondHandler.sendOrder(False,BondHandler.currentPos,1000)
        elif BondHandler.currentPos<-75:
            BondHandler.sendOrder(True,BondHandler.currentPos,1000)
        elif BondHandler.currentPos==100:
            BondHandler.buyOrder=False
        elif BondHandler.currentPos==-100:
            BondHandler.sellOrder=False
        else:
            BondHandler.updatePrice()
            #cant do anything

