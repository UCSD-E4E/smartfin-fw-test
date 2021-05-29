import e4e.test
import e4e.framework
import datetime as dt
import pytz
import time
import IPython
import e4e.dataEndpoint

class smartfin_fw2_10(e4e.test.Test):
    def __init__(self, fin:e4e.framework.Smartfin):
        pass

    def test(self, fin:e4e.framework.Smartfin):
        startTime = dt.datetime.now(pytz.utc)
        fin.startDeployment()
        for i in range(15):
            fin.waitForMatch('Flushing', 180)
        fin.stopDeployment()
        fin.waitForMatch('Initializing State STATE_UPLOAD', 60)

        fin.startDeployment()
        fin.waitForMatch('Flushing', 180)
        fin.stopDeployment()
        fin.waitForMatch('Next State: STATE_DEEP_SLEEP', 6000)

        df = fin.getDeploymentData('credentials.json', startTime=startTime)
        fin.saveDeploymentData(df)

        eventNames = set(['-'.join(event.split('-')[:-1]) for event in df['event']])
        assert(len(eventNames) == 2)
        # eventName = eventNames.pop()
        # dateStr = eventName.split('-')[2]
        # timeStr = eventName.split('-')[3]
        # timezone = pytz.timezone('UTC')
        # sessionStart = dt.datetime.strptime('-'.join([dateStr, timeStr]), '%Y%m%d-%H%M%S')
        # sessionStart = timezone.localize(sessionStart)
        # assert(abs((sessionStart - startTime).total_seconds()) < 10)


    def cleanup(self, fin:e4e.framework.Smartfin):
        pass