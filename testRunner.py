#!/usr/bin/env python3
import pkgutil
import e4e.test
import os
import importlib
import yaml
import e4e.framework
import traceback
import datetime as dt
from e4e import tests
from typing import Type, Set
import inspect

TEST_RESULTS_DIR_FMT = "{name}_{timestamp}_{test}"

def __all_subclasses(cls: Type[object]) -> Set[Type[object]]:
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in __all_subclasses(c)]
    )

def iter_namespaces(ns_pkg):
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def load_plugins():
    for _, name, _ in iter_namespaces(tests):
        try:
            importlib.import_module(name)
        except:
            print(f'Failed to import {name}')

if __name__ == "__main__":
    with open(os.path.join('.', 'settings.yaml'), 'r') as stream:
        settings = yaml.safe_load(stream)
    if not os.path.exists(settings['testResults']):
        os.mkdir(settings['testResults'])

    with open(os.path.join('.', 'e4e', 'tests', 'devices.yaml'), 'r') as stream:
        devices = yaml.safe_load(stream)
    load_plugins()
    test_classes = list(__all_subclasses(e4e.test.Test))
    


    
    while True:
        for i in range(len(devices)):
            print("%4d: %s" % (i, sorted(devices.keys())[i]))
        print("%4d: %s" % (i + 1, "Exit"))
        selectedDeviceIdx = int(input())
        
        assert(selectedDeviceIdx <= len(devices))
        if selectedDeviceIdx == len(devices):
            break

        selectedDevice = sorted(devices.keys())[selectedDeviceIdx]

        for i in range(len(test_classes)):
            print("%4d: %s" % (i, test_classes[i].__name__))
        print("%4d: %s" % (i + 1, "Exit"))
        
        selectedTestIdx = int(input())
        
        assert(selectedTestIdx <= len(test_classes))
        if selectedTestIdx == len(test_classes):
            break

        try:
            selectedTestModule = test_classes[selectedTestIdx]
            testResultsDir = os.path.join(settings['testResults'], TEST_RESULTS_DIR_FMT.format(
                name=selectedDevice,
                test=test_classes[selectedTestIdx].__name__,
                timestamp=dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            ))
            os.mkdir(testResultsDir)
            with e4e.framework.Smartfin(port=devices[selectedDevice]['port'], 
                results_dir=testResultsDir, name=selectedDevice, 
                sfid=devices[selectedDevice]['sfid']) as fin:
                assert(issubclass(selectedTestModule, e4e.test.Test))
                assert(not inspect.isabstract(selectedTestModule))
                testInstance: e4e.test.Test = selectedTestModule(fin)
                try:
                    testInstance.test(fin)
                    print("%s completed" % (selectedTestModule.__name__))
                except Exception as e:
                    print("%s failed" % (selectedTestModule.__name__))
                    raise e
                finally:
                    testInstance.cleanup(fin)
        except Exception as e:
            print(e)
            traceback.print_exc()