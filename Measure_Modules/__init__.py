version = "0.1"
author = ""
organization = ""

__modules_loaded__ = []
__modules_classes__ = []

DEBUG = True
if DEBUG:
    print("DEBUG ENABLED")

import re

from .measure_master import MeasureMaster

default_measure_master = MeasureMaster()

try:
    from .bme280sensor.bme280_sensor import BME280Sensor

    class BME280(BME280Sensor):
        def __init__(
            self,
            addr: int = 118,
            busid: int = 1,
            delay: float = 5,
            timezone: str = "Europe/Warsaw",
            debug: bool = False,
        ) -> None:
            super().__init__(addr, busid, delay, timezone, debug)

        def run(self) -> list[float]:
            res = self.run_measurement()
            if res:
                return res
            else:
                self.DEBUG("Measurment failed", 2, self.name, force=True)
                return False

    __modules_loaded__.append("BME280")
    __modules_classes__.append(BME280)
    default_measure_master.add_mod(BME280())
except Exception as e:
    if DEBUG:
        print("[BME280] LOADING ERROR: " + str(e))

try:
    from .gy271compass.gy271 import GY271Sensor

    class GY271(GY271Sensor):
        def __init__(self, delay: int = 1, debug: bool = False) -> None:
            super().__init__(delay, debug)

        def run(self) -> list[float]:
            res = self.run_measurement()
            if res:
                return res
            else:
                self.DEBUG("Measurment failed", 2, self.name, force=True)
                return False

    __modules_loaded__.append("GY271")
    __modules_classes__.append(GY271)
    default_measure_master.add_mod(GY271())
except Exception as e:
    if DEBUG:
        print("[GY271] LOADING ERROR: " + str(e))

try:
    from .ICM40609_IMU.icm40609 import ICM40609IMUSensor

    class ICM40609(ICM40609IMUSensor):
        def __init__(self, debug: bool = False) -> None:
            super().__init__(debug)

        def run(self) -> list[float]:
            res = self.make_measure()
            if res:
                return res
            else:
                self.DEBUG("Measurment failed", 2, self.name, force=True)
                return False

    __modules_loaded__.append("ICM40609")
    __modules_classes__.append(ICM40609)
    default_measure_master.add_mod(ICM40609())
except Exception as e:
    if DEBUG:
        print("ICM40609 LOADING ERROR: " + str(e))

__all__ = [version, __modules_loaded__, __modules_classes__, MeasureMaster]

print(
    f"Measure Modules package initialised in version {version}\nCreated by {author} for {organization}"
)
print(f"Loaded modules:")
for module in __modules_loaded__:
    print("\t- " + module)
