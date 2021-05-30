#!/usr/bin/env python3
import RPi.GPIO as GPIO
import serial
import logging
import os
import threading
import re
import datetime as dt
import pytz
import e4e.dataEndpoint
import pandas as pd
import enum
from typing import List
import html
import time

WET_DRY_PIN = 37

class SMARTFIN_STATE(enum.Enum):
    STATE_NULL=0
    STATE_DEEP_SLEEP=1
    STATE_SESSION_INIT=2
    STATE_DEPLOYED=3
    STATE_UPLOAD=4
    STATE_CLI=5
    STATE_MFG_TEST=6
    STATE_TMP_CAL=7
    STATE_CHARGE=8

SMARTFIN_STATE_strMap = {
    SMARTFIN_STATE.STATE_NULL: "UNKNOWN",
    SMARTFIN_STATE.STATE_DEEP_SLEEP: 'STATE_DEEP_SLEEP',
    SMARTFIN_STATE.STATE_SESSION_INIT: 'STATE_SESSION_INIT',
    SMARTFIN_STATE.STATE_DEPLOYED: 'STATE_DEPLOYED',
    SMARTFIN_STATE.STATE_UPLOAD: 'STATE_UPLOAD',
    SMARTFIN_STATE.STATE_CLI: 'STATE_CLI',
    SMARTFIN_STATE.STATE_MFG_TEST: 'STATE_MFG_TEST',
    SMARTFIN_STATE.STATE_TMP_CAL: 'STATE_TMP_CAL',
    SMARTFIN_STATE.STATE_CHARGE: 'STATE_CHARGE'
}

SMARTFIN_STATE_stateMap = {value: key for key, value in SMARTFIN_STATE_strMap.items()}

class Smartfin:
    def __init__(self, port:str, results_dir:str, name:str, sfid=str):
        self._portName = port
        self.results_dir = results_dir
        self.name = name
        self.sfid = sfid
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self._runSerialMonitor = True
        self.__match = None
        self.__matchEvent = threading.Event()
        self.__deploymentStartTime = None
        self.__matches = []
        self.__currentState = SMARTFIN_STATE.STATE_NULL
        self.__data = []
        self.__response = b''
        self.__recordResponse = False

    def __enter__(self):
        self._handler = logging.FileHandler(os.path.join(self.results_dir, self.name + ".log"))
        self._handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
        self._handler.setFormatter(formatter)
        self.logger.addHandler(self._handler)
        self.__match = None
        self.__currentState = SMARTFIN_STATE.STATE_NULL
        self.__data = []
        self.__response = b''
        self.__recordResponse = False

        self._port = serial.Serial(self._portName, baudrate=115200)
        self._port.timeout = 1
        self.logger.info("%s opened" % (self._portName))
        self._runSerialMonitor = True

        self._serialMonitorThread = threading.Thread(target=self.serialMonitor)
        self._serialMonitorThread.start()


        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(WET_DRY_PIN, GPIO.OUT)
        GPIO.output(WET_DRY_PIN, GPIO.LOW)
        self.logger.info("Wet/Dry Sensor LOW")
        return self

    def __exit__(self, exc_type, esc_val, exc_tb):
        self._runSerialMonitor = False
        self._serialMonitorThread.join()
        self.logger.info("Stopping test")
        self._handler.close()
        self.logger.removeHandler(self._handler)
        self._port.close()
        GPIO.cleanup()

    def reset(self):
        self._runSerialMonitor = False
        self._serialMonitorThread.join()
        self.logger.info("Stopping serial monitor")
        self._port.close()

        # reset - currently not supported
        print("Manually Reset Smartfin")
        input()

        self._port.open()
        self.logger.info("Starting serial monitor")
        self._runSerialMonitor = True
        self._serialMonitorThread = threading.Thread(target=self.serialMonitor)
        self._serialMonitorThread.start()

    def startDeployment(self):
        GPIO.output(WET_DRY_PIN, GPIO.HIGH)
        self.logger.info("Wet/Dry Sensor HIGH")
        self.__deploymentStartTime = dt.datetime.now(pytz.utc)

    def stopDeployment(self):
        GPIO.output(WET_DRY_PIN, GPIO.LOW)
        self.logger.info("Wet/Dry Sensor LOW")

    def serialMonitor(self):
        while self._runSerialMonitor:
            if self._port.inWaiting():
                data = self._port.readline()
                line = data.decode(errors='ignore')
                self.logger.info("Serial Rx - %s" % (line.strip()))
                if self.__match:
                    matches = re.findall(self.__match, line)
                    if len(matches) > 0:
                        self.__match = None
                        self.__matches.extend(matches)
                        self.__matchEvent.set()

                stateMatch = re.findall('Initializing State.*', line)
                if len(stateMatch) == 1:
                    self.__currentState = SMARTFIN_STATE_stateMap[line.split()[-1].strip()]
                
                if self.__currentState == SMARTFIN_STATE.STATE_UPLOAD:
                    uploadDataMatch = re.findall('Uploaded record', line)
                    if len(uploadDataMatch) > 0:
                        self.__data.append(line.strip('Uploaded record').strip())

                if self.__recordResponse:
                    self.__response += data

    def sendCommand(self, command:str, responsePattern:str="", timeout:float=None)->bytes:
        self.__match = responsePattern
        self.__response = b''
        self.__recordResponse = True
        self.logger.info("Serial Tx - %s" % (command))
        self._port.write(command.encode())
        assert(self.__matchEvent.wait(timeout))
        self.__matchEvent.clear()
        return self.__response

    def getSerialData(self)->List[str]:
        return self.__data

    def getCurrentState(self)->SMARTFIN_STATE:
        return self.__currentState

    def waitForMatch(self, regex, timeout:float = None):
        self.__match = regex
        retval = self.__matchEvent.wait(timeout)
        self.__matchEvent.clear()
        return retval

    def waitForGetMatch(self, regex, timeout:float=None):
        self.__match = regex
        self.__matches = []
        assert(self.__matchEvent.wait(timeout))
        self.__matchEvent.clear()
        return self.__matches

    def getDeploymentData(self, credentials:str, startTime:dt.datetime = None) -> pd.DataFrame:
        df = e4e.dataEndpoint.getData(credentials)
        if startTime is None:
            startTime = self.__deploymentStartTime

        df = df[df['Publish Timestamp'] > startTime]
        df['data'] = [html.unescape(s) for s in df['data']]
        return df

    def saveDeploymentData(self, df:pd.DataFrame):
        sessionTimeStr = self.__deploymentStartTime.strftime("%Y.%m.%d.%H.%M.%S.%f")
        sessionFileName = "Sfin-%s-%s.csv" % (self.sfid, sessionTimeStr)
        df.to_csv(os.path.join(self.results_dir, sessionFileName))
        sessionFileName = "Sfin-%s-%s.log" % (self.sfid, sessionTimeStr)
        with open(os.path.join(self.results_dir, sessionFileName), 'w') as dataFile:
            for record in df['data']:
                dataFile.write(record)
                dataFile.write('\n')