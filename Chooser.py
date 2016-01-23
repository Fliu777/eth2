class Chooser:
    algorithms=[]
    activeTrades=[]

    def __init__(self):
        pass
    def loadAlgo(algo):
        algorithms.append(algo)
    def executeTrade():
        bestAlgo=None
        bestHistory=0
        for algo in algorithms:
            cur=algo.recent_history()
            if cur>bestHistory:
                bestAlg=algo
                bestHistory=cur
        if bestAlgo:
            bestAlgo.next_trade(activeTrades)
