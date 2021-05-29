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

WET_DRY_PIN = 37

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

    def __enter__(self):
        self._handler = logging.FileHandler(os.path.join(self.results_dir, self.name + ".log"))
        self._handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
        self._handler.setFormatter(formatter)
        self.logger.addHandler(self._handler)
        self.__match = None

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
                line = self._port.readline()
                self.logger.info("Serial - %s" % (line))
                if self.__match:
                    matches = re.findall(self.__match, line.decode(errors='ignore'))
                    if len(matches) > 0:
                        self.__match = None
                        self.__matchEvent.set()

    def waitForMatch(self, regex, timeout:float = None):
        self.__match = regex
        retval = self.__matchEvent.wait(timeout)
        self.__matchEvent.clear()

    def getDeploymentData(self, credentials:str, startTime:dt.datetime = None) -> pd.DataFrame:
        df = e4e.dataEndpoint.getData(credentials)
        if startTime is None:
            return df[df['Publish Timestamp'] > self.__deploymentStartTime]
        else:
            return df[df['Publish Timestamp'] > startTime]

    def saveDeploymentData(self, df:pd.DataFrame):
        sessionTimeStr = self.__deploymentStartTime.strftime("%Y.%m.%d.%H.%M.%S.%f")
        sessionFileName = "Sfin-%s-%s.csv" % (self.sfid, sessionTimeStr)
        df.to_csv(os.path.join(self.results_dir, sessionFileName))
        sessionFileName = "Sfin-%s-%s.log" % (self.sfid, sessionTimeStr)
        with open(os.path.join(self.results_dir, sessionFileName), 'w') as dataFile:
            for record in df['data']:
                dataFile.write(record)
                dataFile.write('\n')