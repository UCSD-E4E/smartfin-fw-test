import e4e.test
import e4e.framework
import IPython

class smartfin_fw2_6(e4e.test.Test):
    def __init__(self, fin:e4e.framework.Smartfin):
        fin.reset()

    def test(self, fin:e4e.framework.Smartfin):
        for i in range(100):
            fin.reset()
            fin.sendCommand("#CLI", ">", 10)
            assert(fin.getCurrentState() == e4e.framework.SMARTFIN_STATE.STATE_CLI)

    def cleanup(self, fin:e4e.framework.Smartfin):
        fin.reset()