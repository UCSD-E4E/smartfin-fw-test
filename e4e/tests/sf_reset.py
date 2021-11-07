import e4e.test
import e4e.framework

class SF_HW_Reset(e4e.test.Test):
    def __init__(self, fin: e4e.framework.Smartfin) -> None:
        super().__init__(fin)

    def test(self, fin: e4e.framework.Smartfin) -> None:
        super().test(fin)
        fin.reset()


    def cleanup(self, fin: e4e.framework.Smartfin) -> None:
        return super().cleanup(fin)
