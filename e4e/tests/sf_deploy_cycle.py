import e4e.test
import e4e.framework
import time

class SF_DeployCycle(e4e.test.Test):
    def __init__(self, fin:e4e.framework.Smartfin):
        print("Init")

    def test(self, fin:e4e.framework.Smartfin):
        fin.startDeployment()
        time.sleep(15)
        fin.stopDeployment()

    def cleanup(self, fin:e4e.framework.Smartfin):
        print("Cleanup")