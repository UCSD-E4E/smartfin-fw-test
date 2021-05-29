from abc import ABC, abstractmethod
import e4e.framework
class Test(ABC):
    @abstractmethod
    def __init__(self, fin:e4e.framework.Smartfin):

        return
    @abstractmethod
    def test(self, fin:e4e.framework.Smartfin):
        return

    @abstractmethod
    def cleanup(self, fin:e4e.framework.Smartfin):
        return