import e4e.test
import e4e.framework
import time

class SF_Calibrate(e4e.test.Test):
    def __init__(self, fin: e4e.framework.Smartfin):
        super().__init__(fin)

    def test(self, fin: e4e.framework.Smartfin) -> None:
        NUM_CYCLES = 3
        CYCLE_TIME = 15
        MEASUREMENT_TIME = 5

        super().test(fin)
        fin.enterCLI()
        response = fin.sendCommand('C\r\n', ':', 10)
        assert(response.decode().find('Please enter the number of temp cycles') != -1)
        response = fin.sendCommand(f'{NUM_CYCLES}\r\n', ':', 10)
        assert(response.decode().find('Please enter the cycle time in seconds (total time between each temp measurement)') != -1)
        response = fin.sendCommand(f'{CYCLE_TIME}\r\n', ':', 10)
        assert(response.decode().find('Please enter the measurement time in seconds (total time taking measurements each cycle):') != -1)
        response = fin.sendCommand(f'{MEASUREMENT_TIME}\r\n', responsePattern='next power cycle',timeout=10)
        assert(response.decode().find('System will boot into calibration mode upon next power cycle') != -1)
        fin.reset()
        time.sleep(NUM_CYCLES * CYCLE_TIME)
        return

    def cleanup(self, fin: e4e.framework.Smartfin) -> None:
        super().cleanup(fin)