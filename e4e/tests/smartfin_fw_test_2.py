import e4e.test
import e4e.framework
import time
import e4e.dataEndpoint
import datetime as dt
import pytz
import e4e.decoder
import pandas as pd
import traceback
import IPython

class smartfin_fw_test_2(e4e.test.Test):
    def __init__(self, fin:e4e.framework.Smartfin):
        pass

    def test(self, fin:e4e.framework.Smartfin):
        SESSION_LEN_S = 120

        startTime = dt.datetime.now(pytz.utc)
        fin.startDeployment()
        time.sleep(SESSION_LEN_S)
        fin.stopDeployment()

        fin.waitForMatch('Next State: STATE_DEEP_SLEEP', 6000)
        df = fin.getDeploymentData('credentials.json')
        data = fin.getSerialData()
        cloudData = list(df['data'])
        differences = []
        try:
            for i in range(len(data)):
                for j in range(len(cloudData[i])):
                    if cloudData[i][j] != data[i][j]:
                        differences.append((i, j))
            print(differences)
        except Exception as e:
            IPython.embed()

    def cleanup(self, fin:e4e.framework.Smartfin):
        pass