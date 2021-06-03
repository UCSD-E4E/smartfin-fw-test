import e4e.test
import e4e.framework
import datetime as dt
import pytz
import time

SF_CELL_SIGNAL_TIMEOUT_MS = 300000
SF_UPLOAD_REATTEMPT_DELAY_SEC = 600
ASSERT_BOUNDARY = 15
WAIT_BOUNDARY = 60
DU_UPLOAD_MAX_REATTEMPTS = 5

class SF_NoNetworkUploadUSB(e4e.test.Test):
    def __init__(self, fin:e4e.framework.Smartfin):
        print("Disconnect the Smartfin antenna, leave USB connected")
        input()
        fin.reset()

    def test(self, fin:e4e.framework.Smartfin):
        startTime = dt.datetime.now(pytz.utc)
        fin.startDeployment()
        time.sleep(10)
        fin.stopDeployment()
        
        fin.waitForState(e4e.framework.SMARTFIN_STATE.STATE_UPLOAD)
        uploadTime = dt.datetime.now(pytz.utc)
        
        for i in range(DU_UPLOAD_MAX_REATTEMPTS):
            fin.waitForState(e4e.framework.SMARTFIN_STATE.STATE_DEEP_SLEEP, SF_CELL_SIGNAL_TIMEOUT_MS / 1000 + WAIT_BOUNDARY)
            sleepTime = dt.datetime.now(pytz.utc)
            fin.verifyWithin(SF_CELL_SIGNAL_TIMEOUT_MS / 1000, ASSERT_BOUNDARY, (sleepTime - uploadTime).total_seconds(), "Time to sleep %d" % (i + 1))

            fin.waitForState(e4e.framework.SMARTFIN_STATE.STATE_UPLOAD, SF_UPLOAD_REATTEMPT_DELAY_SEC + WAIT_BOUNDARY)
            uploadTime = dt.datetime.now(pytz.utc)
            assert(abs((uploadTime - sleepTime).total_seconds() - SF_UPLOAD_REATTEMPT_DELAY_SEC) < ASSERT_BOUNDARY)
            fin.verifyWithin(
                expectedValue=SF_UPLOAD_REATTEMPT_DELAY_SEC,
                margin=ASSERT_BOUNDARY,
                actualValue=(uploadTime - sleepTime).total_seconds(),
                description="Time to upload %d" % (i + 2)
            )

        fin.waitForState(e4e.framework.SMARTFIN_STATE.STATE_DEEP_SLEEP, SF_CELL_SIGNAL_TIMEOUT_MS / 1000 + WAIT_BOUNDARY)
        sleepTime = dt.datetime.now(pytz.utc)
        fin.verifyWithin(
            expectedValue=SF_CELL_SIGNAL_TIMEOUT_MS / 1000, 
            margin=ASSERT_BOUNDARY, 
            actualValue=(sleepTime - uploadTime).total_seconds(), 
            description="Time to sleep %d" % (DU_UPLOAD_MAX_REATTEMPTS + 1)
        )

        time.sleep(SF_UPLOAD_REATTEMPT_DELAY_SEC)
        fin.verifyEqual(
            expectedValue=e4e.framework.SMARTFIN_STATE.STATE_CHARGE,
            actualValue=fin.getCurrentState(),
            description="Ending state"
        )

    def cleanup(self, fin:e4e.framework.Smartfin):
        print("Reconnect the Smartfin antenna")
        input()
        fin.reset()