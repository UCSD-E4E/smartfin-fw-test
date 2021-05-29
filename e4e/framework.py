#!/usr/bin/env python3
import RPi.GPIO as GPIO
import serial
import logging
import os
import threading

WET_DRY_PIN = 37

class Smartfin:
    def __init__(self, port:str, results_dir:str, name:str, sfid=str):
        self._portName = port
        self._results_dir = results_dir
        self._name = name
        self._sfid = sfid
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self._runSerialMonitor = True

    def __enter__(self):
        self._handler = logging.FileHandler(os.path.join(self._results_dir, self._name + ".log"))
        self._handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
        self._handler.setFormatter(formatter)
        self.logger.addHandler(self._handler)

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

    def stopDeployment(self):
        GPIO.output(WET_DRY_PIN, GPIO.LOW)
        self.logger.info("Wet/Dry Sensor LOW")

    def serialMonitor(self):
        while self._runSerialMonitor:
            if self._port.inWaiting():
                line = self._port.readline()
                self.logger.info("Serial - %s" % (line))