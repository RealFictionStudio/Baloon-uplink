import atexit
import time

from ..modules_debug import ModuleDebuger
from .icm40609lib import ICM40609


class ICM40609IMUSensor:
    def __init__(self, debug: bool = False) -> None:
        self.mpu = ICM40609()
        self.debuger = ModuleDebuger(debug)
        self.DEBUG = self.debuger.DEBUG
        atexit.register(self.close)

        self.name = "IMU_ICM40609"

    def close(self):
        self.mpu.close()
        self.mpu = None

    def check_availability(self):
        self.DEBUG(f"IMU id: {self.mpu.check_availability()}", 0, force=True)

    def make_measure(self) -> dict:
        try:
            accel_g = self.mpu.read_accel_data().values()
            accel_rec = {
                "accl_x": accel_g[0],
                "accl_y": accel_g[1],
                "accl_z": accel_g[2],
            }
            gyro_g = self.mpu.read_gyro_data().values()
            gyro_rec = {"gyro_x": gyro_g[0], "gyro_y": gyro_g[1], "gyro_z": gyro_g[2]}
            temp = [(self.mpu.read_temp_data() / 132.48) + 25]
            timestamp = [time.time()]

            res = {"time": timestamp, "temp": temp}
            res.update(accel_rec)
            res.update(gyro_rec)

            return res
        except Exception as e:
            self.DEBUG(str(e), 2, self.name, force=True)
