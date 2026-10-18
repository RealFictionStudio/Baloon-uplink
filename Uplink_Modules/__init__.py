version = "0.1"
author = ""
organization = ""

__modules_loaded__ = []
__modules_classes__ = []

DEBUG = True
if DEBUG:
    print("DEBUG ENABLED")

from typing import Any

from .uplink_master import UplinkMaster

default_uplink_master = UplinkMaster()

try:
    from .lora_wan.lora_com import LoRACom

    class LoRA(LoRACom):
        def __init__(
            self,
            brate: int,
            port: str,
            timeout: int,
            verbose: bool = False,
            endflag: bytes = b"\n",
            readbuf: int = 1024,
        ) -> None:
            super().__init__(brate, port, timeout, verbose, endflag, readbuf)

        def listen(self):
            return self.read_mode()

        def send(self, data: Any):
            try:
                self.send_message(data)
            except Exception as e:
                self.DEBUG(str(e), 2, self.name, force=True)

    __modules_loaded__.append("LoRA")
    __modules_classes__.append(LoRA)
    default_uplink_master.add_com_module(LoRA(9600, "ttyUSB0", 5))

except Exception as e:
    if DEBUG:
        print("[LoRA] LOADING ERROR: ", str(e))

__all__ = [version, __modules_loaded__, __modules_classes__, UplinkMaster]

print(
    f"Uplink modules package initialised in version {version}\nCreated by {author} for {organization}"
)
print(f"Loaded modules:")
for module in __modules_loaded__:
    print("\t- " + module)
