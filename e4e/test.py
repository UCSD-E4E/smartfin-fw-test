from abc import ABC, abstractmethod
import e4e.framework


class Test(ABC):
    def __init__(self, fin: e4e.framework.Smartfin) -> None:
        fin.reset()

    @abstractmethod
    def test(self, fin: e4e.framework.Smartfin) -> None:
        pass

    def cleanup(self, fin: e4e.framework.Smartfin) -> None:
        fin.reset()
