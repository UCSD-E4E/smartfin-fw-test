import e4e.test
import e4e.framework
import IPython

class smartfin_fw2_6(e4e.test.Test):
    def __init__(self, fin:e4e.framework.Smartfin):
        fin.reset()

    def test(self, fin:e4e.framework.Smartfin):
        response = fin.sendCommand("#CLI", ">")
        print(response)
        IPython.embed()

    def cleanup(self, fin:e4e.framework.Smartfin):
        fin.reset()