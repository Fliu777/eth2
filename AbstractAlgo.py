class AbstractAlgorithm:
    def next_trade(): #can be null
        raise NotImplementedError("Class %s doesn't implement next_trade()" % (self.__class__.__name__))
    def get_cur_profit():
        raise NotImplementedError("Class %s doesn't implement get_cur_profit()" % (self.__class__.__name__))
    def recent_history():
        raise NotImplementedError("Class %s doesn't implement recent_history()" % (self.__class__.__name__))