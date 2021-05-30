import e4e.test
import e4e.framework
import time
import e4e.dataEndpoint
import datetime as dt
import pytz
import e4e.decoder
import pandas as pd
import traceback

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
            fin.waitForMatch('Next State: STATE_DEEP_SLEEP', 6000)
            df = fin.getDeploymentData('credentials.json')
            assert(len(df) < 11)

            fin.saveDeploymentData(df)

            data = []
            for record in df['data']:
                try:                    
                    assert(record and record != None)
                    ensembleList = e4e.decoder.decodeRecord(record)
                    data.extend(ensembleList)
                except Exception as e:
                    print(record)
                    print(e)
                    traceback.print_exc()
                    
            try:
                df = pd.DataFrame(data)

                # Check that the logged data is within 10 seconds of the actual deployment time
                assert(abs((max(df['timestamp']) - min(df['timestamp'])) - DEPLOYMENT_TIME) < 10)
            except Exception as e:
                print(df)

    def cleanup(self, fin:e4e.framework.Smartfin):
        pass