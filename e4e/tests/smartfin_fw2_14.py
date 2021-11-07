import e4e.test
import e4e.framework
import time
import datetime as dt

class SF_waterDetect40(e4e.test.Test):
    def __init__(self, fin: e4e.framework.Smartfin):
        fin.eraseRecorder()
        fin.reset()

    def test(self, fin: e4e.framework.Smartfin):
        expectedResults = {
            45: True,
            10: False,
            20: False,
            35: True,
        }

        for waterTime, deployed in expectedResults.items():
            fin.startDeployment()
            time.sleep(waterTime)
            fin.verifyEqual(
                description="Fin state after %d seconds" % (waterTime),
                actualValue=fin.getCurrentState() == e4e.framework.SMARTFIN_STATE.STATE_DEPLOYED,
                expectedValue=deployed
            )
            fin.stopDeployment()
            fin.reset()

class SF_waterDetectTiming(e4e.test.Test):
    def test(self, fin: e4e.framework.Smartfin):
        startTime = dt.datetime.now()
        fin.startDeployment()
        fin.waitForState(e4e.framework.SMARTFIN_STATE.STATE_DEPLOYED, timeout=60)
        deployTime = dt.datetime.now()
        fin.verifyLessThan(
            description="Fin deploy time",
            actualValue=(deployTime - startTime).total_seconds(),
            thresholdValue=40
        )
        fin.stopDeployment()
        fin.reset()