class BondHandler:
    connection=None
    buyOrder=False
    sellOrder=False
    counter=0
    def __init__(self, connection):
        BondHandler.connection=connection
        self.sendOrder(True,100,999)
        self.sendOrder(False, 100,1001)
        pass
    def sendOrder(self, isBuy, amount, price):
        if isBuy:
            BondHandler.counter+=1
            return "ADD "+str(BondHandler.counter)+" BOND BUY "+str(amount)+" "+str(price)
        else:
            BondHandler.counter+=1
            return "ADD "+str(BondHandler.counter)+" BOND SELL "+str(amount)+" "+str(price)
        pass
    def updatePrice(self, stock, buyPrices=[], sellPrices=[]):
        if BondHandler.buyOrder:
            self.sendOrder(True,100,999)
            #buyOrder=False
        if BondHandler.buyOrder and len(sellPrices)>0 and sellPrices[0][0]>=1000:
            #sell at 1000, which is fair value
            self.sendOrder(False,100,sellPrices[0][0])
        elif BondHandler.sellOrder:
            self.sendOrder(False,100,1001)

    def fillOrder(self, stock, orderbook): #stock is of type STOCK
        if stock.volume>0:
            #buy order executed
            BondHandler.buyOrder=False
        else:
            BondHandler.sellOrder=False
