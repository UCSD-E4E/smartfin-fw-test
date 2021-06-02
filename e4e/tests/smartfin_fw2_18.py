import e4e.test
import e4e.framework
import time
import datetime as dt
import pytz
import IPython

class smartfin_fw2_18_test1(e4e.test.Test):
    def __init__(self, fin:e4e.framework.Smartfin):
        fin.reset()

    def test(self, fin:e4e.framework.Smartfin):
        sessionTimes = [5*60, 10*60, 15*60, 20*60]
        data = {}
        for sessionTime in sessionTimes:
            fin.reset()
            startTime = dt.datetime.now(pytz.utc)
            fin.startDeployment()
            time.sleep(sessionTime)
            fin.stopDeployment()
            fin.waitForMatch('Next State: STATE_DEEP_SLEEP', 6000)

            df = fin.getDeploymentData('credentials.json')
            fin.saveDeploymentData(df)
            eventNames = set(['-'.join(event.split('-')[:-1]) for event in df['event']])
            eventName = eventNames.pop()
            dateStr = eventName.split('-')[2]
            timeStr = eventName.split('-')[3]
            timezone = pytz.timezone('UTC')
            sessionStart = dt.datetime.strptime('-'.join([dateStr, timeStr]), '%Y%m%d-%H%M%S')
            sessionStart = timezone.localize(sessionStart)
            data[sessionTime] = (startTime, sessionStart)
        IPython.embed()


    def cleanup(self, fin:e4e.framework.Smartfin):
        fin.reset()