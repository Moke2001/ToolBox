from abc import abstractmethod


class Group:
    def __init__(self,N):
        self.N = N

    @abstractmethod
    def __mul__(self,other):
        pass

    @abstractmethod
    def __rmul__(self,other):
        pass

    @abstractmethod
    def __eq__(self,other):
        pass

    @abstractmethod
    def commuter(self,other):
        pass

    @abstractmethod
    def dag(self):
        pass

