#!/usr/bin/env python3
from typing import List, Dict
def getNextEvent(schedule:List[Dict[str, int]])->Dict[str,int]:
    earliestExecute = 0
    for event in schedule:
        if event['lastExecute'] == 0:
            timeToCompare = event['delay_ms'] + 1
        else:
            if event['interval_ms'] != -1:
                timeToCompare = event['lastExecute'] + event['interval_ms']
            else:
                continue
        
        if earliestExecute == 0:
            earliestExecute = timeToCompare
            earliestEvent = event

        if timeToCompare < earliestExecute:
            earliestExecute = timeToCompare
            earliestEvent = event
    
    return earliestExecute, earliestEvent


if __name__ == "__main__":
    schedule = [
        {
            'ensType':10,
            'delay_ms':0,
            'interval_ms':1000,
            'ensSize':23,
            'lastExecute': 0
        },
        {
            'ensType':7,
            'delay_ms':0,
            'interval_ms':10000,
            'ensSize':5,
            'lastExecute': 0
        }
    ]

    MAX_BUFFER = 496
    DEPLOYMENT_TIME_ms = 500000
    ensSequence = []

    nextTime = 0
    while True:
        nextTime, nextEvent = getNextEvent(schedule)
        if nextTime < DEPLOYMENT_TIME_ms:
            nextEvent['lastExecute'] = nextTime
            ensSequence.append((nextEvent['ensType'], nextEvent['ensSize'], nextTime))
        else:
            break

    recordedSize = 0
    for ens in ensSequence:
        if ens[1] > MAX_BUFFER - (recordedSize % MAX_BUFFER):
            recordedSize += MAX_BUFFER - (recordedSize % MAX_BUFFER)
        recordedSize += ens[1]
    print("Recorded %d bytes" % recordedSize)
    print("Recorded %d Packets" % (recordedSize / MAX_BUFFER + 1))
    print(ensSequence)
