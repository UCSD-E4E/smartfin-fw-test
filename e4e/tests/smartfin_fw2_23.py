import e4e.test
import e4e.framework
import datetime as dt
import pytz
import IPython
import time
import e4e.decoder

class SF_checkForFWVersion(e4e.test.Test):
    def __init__(self, fin:e4e.framework.Smartfin):
        fin.eraseRecorder()

        fin.sendCommand('#CLI', '>', 10)
        fin.sendCommand('*\r', '>', 10)
        response = fin.sendCommand('9\r', '>', 10).decode(errors='ignore')
        versionLine = response.splitlines()[2]
        self.version = tuple([int(x) for x in versionLine.split()[2].strip('v').split('.')])
        fin.reset()
    
    def test(self, fin:e4e.framework.Smartfin):
        startTime = dt.datetime.now(pytz.utc)
        fin.startDeployment()
        time.sleep(10)
        fin.stopDeployment()
        fin.waitForState(e4e.framework.SMARTFIN_STATE.STATE_DEEP_SLEEP)
        df = fin.getSerialData()
        fin.saveSerialData(df)
        data = []
        for record in df:
            data.extend(e4e.decoder.decodeRecord(record))
        textEns = [ens for ens in data if ens['dataType'] == 0x0F]
        fin.verifyEqual(
            expectedValue=('FW%d.%d.%d.%d' % self.version),
            actualValue=textEns[0]['text'],
            description="Firmware version message"
        )
        
    def cleanup(self, fin: e4e.framework.Smartfin):
        pass