import time

from ..modules_debug import ModuleDebuger
from .gy271compass import Compass


class GY271Sensor:
    def __init__(self, delay: int = 1, debug: bool = False) -> None:
        self.sensor = Compass()
        self.debuger = ModuleDebuger(debug)
        self.DEBUG = self.debuger.DEBUG
        self.config_debug = self.debuger.config_debug

        self.name = "GY271"

    def run_measurement(self) -> dict:
        try:
            angle = self.sensor.get_bearing()
            axis = self.sensor.get_axis()
            for i in range(len(axis)):
                axis[i] = axis[i] / 10000
            temp = self.sensor.read_temp()
            timestamp = time.time()
            return {"time": timestamp, "angle": angle, "X": axis[0], "Y": axis[1], "Z": axis[2], "temp": temp}

        # print("Heading Angle = {}°".format(angle))
        # print("Temperature = {:.1f}°C".format(temp))

        except Exception as e:
            self.DEBUG(str(e), 2, self.name, True)
            time.sleep(10)
            return False
