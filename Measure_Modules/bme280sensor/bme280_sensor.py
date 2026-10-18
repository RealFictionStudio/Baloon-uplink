import os
import time

import bme280
import smbus2

from ..modules_debug import ModuleDebuger


class BME280Sensor:
    def __init__(
        self,
        addr: int = 0x76,
        busid: int = 1,
        delay: float = 5,
        timezone: str = "Europe/Warsaw",
        debug: bool = False,
    ) -> None:
        self.addr = addr
        self.busid = busid
        self.delay = delay
        self.timezone = timezone
        self.debuger = ModuleDebuger(debug)
        self.DEBUG = self.debuger.DEBUG
        self.config_debug = self.debuger.config_debug
        self.bus = smbus2.SMBus(self.busid)
        self.calibration_params = bme280.load_calibration_params(self.bus, self.addr)

        self.name = "BME280"

    def run_measurement(self) -> dict:
        try:
            data = bme280.sample(self.bus, self.addr, self.calibration_params)
            temperature_celsius = data.temperature
            humidity = data.humidity
            pressure = data.pressure
            timestamp = time.time()  # data.timestamp

            return {
                "time": timestamp,
                "temp": temperature_celsius,
                "humidity": humidity,
                "pressure": pressure,
            }
            """print(
                    str(timestamp)
                    + " Temp={0:0.1f}ºC, Temp={1:0.1f}ºF, Humidity={2:0.1f}%, Pressure={3:0.2f}hPa".format(
                        temperature_celsius, temperature_fahrenheit, humidity, pressure
                    )
                )"""

            time.sleep(self.delay)
        except Exception as e:
            self.DEBUG(str(e), 2, self.name, True)
            time.sleep(10)
            return False
