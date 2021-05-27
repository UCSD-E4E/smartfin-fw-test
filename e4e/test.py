from abc import ABC, abstractmethod

class Test(ABC):
    @abstractmethod
    def __init__(self):

        return
    @abstractmethod
    def test(self):
        return

    @abstractmethod
    def cleanup(self):
        return