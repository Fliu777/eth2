class Chooser:
    algorithms=[]
    activeTrades=[]

    def __init__(self):
        pass
    def loadAlgo(self, algo):
        Chooser.algorithms.append(algo)
    def executeTrade(self):
        bestAlgo=None
        bestHistory=0
        for algo in Chooser.algorithms:
            cur=algo.recent_history()
            if cur>bestHistory:
                bestAlg=algo
                bestHistory=cur
        if bestAlgo:
            bestAlgo.next_trade(Chooser.activeTrades)