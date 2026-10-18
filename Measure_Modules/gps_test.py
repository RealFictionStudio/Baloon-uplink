import multiprocessing
from time import sleep, time

import smbus2

BME280_PORT = 1
BME280_ADDRESS = 0x76
SENSOR_LOOP_INTERVAL = 3


class InternalSystemsManager(multiprocessing.Process):
    def __init__(self):
        super().__init__()
        self.running = True

        self.bme280_port = BME280_PORT
        self.bme280_address = BME280_ADDRESS
        self.I2C_ADDR = 0x42
        self.BUFFER_SIZE = 32
        self.REG_DATA = 0xFF
        self.data_packet = {
            "time": time(),
            "lat": 0.0,
            "lon": 0.0,
            "alt": 0.0,
            "temp": 0.0,
            "hum": 0.0,
            "pres": 0.0,
        }

    def gps_step(self):
        try:
            raw_data = self.read_gps_data()
            if raw_data:
                for line in raw_data.split("\r\n"):
                    self.parse_nmea(line)
        except Exception as e:
            print(f"Error in gps_step: {e}")

    def read_gps_data(self):
        data = b""
        try:
            with smbus2.SMBus(self.bme280_port) as bus:
                for _ in range(5):
                    chunk = bus.read_i2c_block_data(
                        self.I2C_ADDR, self.REG_DATA, self.BUFFER_SIZE
                    )
                    data += bytes(chunk)
                    sleep(0.1)

            raw_text = data.decode(errors="ignore").strip()
            return raw_text if raw_text else None
        except Exception as e:
            print(f"Error reading GPS: {e}")
            return None

    def nmea_to_decimal(self, coord, direction):
        try:
            if not coord:
                return None
            deg_length = 3 if direction in ["E", "W"] else 2
            degrees = float(coord[:deg_length])
            minutes = float(coord[deg_length:]) / 60
            decimal = degrees + minutes
            if direction in ["S", "W"]:
                decimal *= -1
            return round(decimal, 6)
        except Exception as e:
            print(f"Error converting NMEA to decimal: {e}")
            return None

    def parse_nmea(self, sentence):
        try:
            parts = sentence.split(",")
            if sentence.startswith("$GNRMC") and len(parts) > 6:
                status = parts[2]
                if status == "A":
                    lat = self.nmea_to_decimal(parts[3], parts[4])
                    lon = self.nmea_to_decimal(parts[5], parts[6])

                    self.data_packet["timestamp"] = time()
                    self.data_packet["lat"] = lat
                    self.data_packet["lon"] = lon
                    print(f"GPS FIX: Lat {lat}, Lon {lon}")
                else:
                    print("No GPS fix")
            elif sentence.startswith("$GNGGA") and len(parts) > 9:
                altitude = parts[9]
                self.data_packet["time"] = time()
                self.data_packet["alt"] = altitude
                print(f"Altitude: {altitude} m")
        except Exception as e:
            print(f"Error parsing NMEA: {e}")


if __name__ == "__main__":
    im = InternalSystemsManager()
    print("GPS TEST 1")
    im.gps_step()
