import e4e.test
import e4e.framework
import time
import e4e.dataEndpoint
import datetime as dt
import pytz
import e4e.decoder
import pandas as pd
import os

class SF_DeployCycle(e4e.test.Test):
    def __init__(self, fin:e4e.framework.Smartfin):
        pass

    def test(self, fin:e4e.framework.Smartfin):
        DEPLOYMENT_TIME = 180
        for trial in range(20):
            startTime = dt.datetime.now(pytz.utc)
            fin.startDeployment()
            time.sleep(DEPLOYMENT_TIME)
            fin.stopDeployment()
            assert(fin.waitForMatch('Next State: STATE_DEEP_SLEEP', 6000))
            df = e4e.dataEndpoint.getData('credentials.json')
            thisDeploymentData = df[df['Publish Timestamp'] > startTime]
            assert(len(thisDeploymentData) < 11)

            sessionTimeStr = startTime.strftime("%Y.%m.%d.%H.%M.%S.%f")
            sessionFileName = "Sfin-%s-%s.log" % (fin.sfid, sessionTimeStr)
            with open(os.path.join(fin.results_dir, sessionFileName), 'w') as dataFile:
                for record in thisDeploymentData['data']:
                    dataFile.write(record)
                    dataFile.write('\n')
                    
            data = []
            for record in thisDeploymentData['data']:
                assert(record and record != None)
                ensembleList = e4e.decoder.decodeRecord(record)
                data.extend(ensembleList)

            df = pd.DataFrame(data)

            # Check that the logged data is within 10 seconds of the actual deployment time
            assert(abs((max(df['timestamp']) - min(df['timestamp'])) - DEPLOYMENT_TIME) < 10)

    def cleanup(self, fin:e4e.framework.Smartfin):
        pass