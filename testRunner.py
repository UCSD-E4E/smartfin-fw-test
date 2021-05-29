#!/usr/bin/env python3
import pkgutil
from e4e.tests import *
import e4e.test
import os
import IPython
import importlib
import yaml
import e4e.framework
import traceback
import datetime as dt

TEST_RESULTS_DIR_FMT = "{name}_{test}_{timestamp}"

if __name__ == "__main__":
    with open(os.path.join('.', 'settings.yaml'), 'r') as stream:
        settings = yaml.safe_load(stream)
    if not os.path.exists(settings['testResults']):
        os.mkdir(settings['testResults'])

    with open(os.path.join('.', 'e4e', 'tests', 'devices.yaml'), 'r') as stream:
        devices = yaml.safe_load(stream)
    with open(os.path.join(".", "e4e", "tests", "tests.yaml"), 'r') as stream:
        testClasses = yaml.safe_load(stream)
    tests = {path.split('.')[-1]:path for path in testClasses}
    testNames = [path.split('.')[-1] for path in testClasses]
    


    
    while True:
        for i in range(len(devices)):
            print("%4d: %s" % (i, sorted(devices.keys())[i]))
        print("%4d: %s" % (i + 1, "Exit"))
        selectedDeviceIdx = int(input())
        
        assert(selectedDeviceIdx <= len(devices))
        if selectedDeviceIdx == len(devices):
            break

        selectedDevice = sorted(devices.keys())[selectedDeviceIdx]

        for i in range(len(tests)):
            print("%4d: %s" % (i, testNames[i]))
        print("%4d: %s" % (i + 1, "Exit"))
        
        selectedTestIdx = int(input())
        
        assert(selectedTestIdx <= len(tests))
        if selectedTestIdx == len(tests):
            break

        try:
            selectedTestModule = tests[testNames[selectedTestIdx]]
            testPath = '.'.join(selectedTestModule.split('.')[:-1])
            modulesource = importlib.import_module(testPath)
            importlib.reload(modulesource)
            testResultsDir = os.path.join(settings['testResults'], TEST_RESULTS_DIR_FMT.format(
                name=selectedDevice,
                test=testNames[selectedTestIdx],
                timestamp=dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            ))
            os.mkdir(testResultsDir)
            with e4e.framework.Smartfin(port=devices[selectedDevice]['port'], 
                results_dir=testResultsDir, name=selectedDevice, 
                sfid=devices[selectedDevice]['sfid']) as fin:
                testClass = getattr(modulesource, testNames[selectedTestIdx])
                testInstance = testClass(fin)
                testInstance.test(fin)
                testInstance.cleanup(fin)
                print("%s completed" % (selectedTestModule))
        except Exception as e:
            print(e)
            traceback.print_exc()