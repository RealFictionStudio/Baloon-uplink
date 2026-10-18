import atexit
import time

import serial


class LoRACom:
    def __init__(
        self,
        brate: int,
        port: str,
        timeout: int,
        verbose: bool = False,
        endflag: bytes = b"\n",
        readbuf: int = 1024,
    ) -> None:
        # PUBLIC
        self.brate = brate
        self.port = port
        self.verbose = verbose
        self.timeout = timeout
        self.endflag = endflag
        self.readbuf = readbuf
        self.name = "LoRA"

        # PRIVATE
        self.reading = False

    def init(self) -> None:
        self.ser = serial.Serial()
        self.ser.baudrate = self.brate
        self.ser.port = self.port
        self.ser.timeout = self.timeout
        self.DEBUG("Initiating device at", self.ser.name)

        # Clear before exit
        atexit.register(self.close)

    def close(self):
        self.ser.close()
        self.DEBUG("LoRA Closed")
        del self

    def DEBUG(self, *text):
        if self.verbose:
            print(" ".join(text))

    def open_port(self) -> bool:
        try:
            self.ser.open()
            if self.ser.is_open:
                self.DEBUG("Port opened")
            else:
                self.DEBUG("[!] Failed to open port")
        except Exception as e:
            self.DEBUG(e)
        return self.ser.is_open

    def send_message(self, msg):
        msgt = type(msg)
        if msgt != bytes:
            if msgt == str:
                to_send = msg.encode()
            elif msgt == int:
                to_send = str(msg).encode()
            elif msgt == float:
                to_send = str(msg).encode()
            elif msgt == bool:
                to_send = str(int(msg)).encode()
            else:
                self.DEBUG(
                    "Unsupported message type, no guarantee it'll be sent propertly"
                )
                to_send = str(msg).encode()

        else:
            to_send = msg

        self.ser.write(to_send)
        self.DEBUG("Message sent")

    def config_readmode(self, rbuf: int, endflag: str):
        if type(rbuf) != int:
            self.DEBUG(f"Incorrect type of rbuf: expected 'int' got {type(rbuf)}")
            return False
        if type(endflag) != str:
            self.DEBUG(f"Incorrect type of endflag: expected 'str' got {type(endflag)}")
            return False

        self.readbuf = rbuf
        self.endflag = endflag

        return True

    def read_mode(self):
        self.reading = True
        while self.reading:
            try:
                ser_bytes = self.ser.read_until(self.endflag, self.readbuf)
                decoded_bytes = float(ser_bytes[0 : len(ser_bytes) - 2].decode("utf-8"))
                print(decoded_bytes)
            except:
                self.DEBUG("Reading Interrupt")
                break


if __name__ == "__main__":
    l = LoRA(9600, "/dev/ttyUSB0", 1000, True)
    l.init()
    l.open_port()
    l.send_message(b"hello")


"""
while True:
    try:
        ser_bytes = ser.readline()
        decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        print(decoded_bytes)
    except:
        print("Keyboard Interrupt")
        break

"""
