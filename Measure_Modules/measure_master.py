import time

from .db_master import DBMaster
from .modules_debug import ModuleDebuger


class MeasureMaster:
    def __init__(self, delay: float = 0.2, multithread: bool = True) -> None:
        self.multithread = multithread
        self.measure_mods = []
        self.md = ModuleDebuger()
        self.db_master = DBMaster()
        self.delay = delay

    def add_mod(self, mod_inst) -> None:
        self.measure_mods.append(mod_inst)

    def make_measures(self) -> list:
        res = []
        for mod in self.measure_mods:
            mres = mod.run()
            if mres:
                res.append(mres)
                self.db_master.insert_record(mod.name, mres)
            else:
                res.append([])
            time.sleep(self.delay)

        return res

    def start(self) -> None:
        while True:
            try:
                res = self.make_measures()
                for i, v in enumerate(res):
                    print(f"<{i}> {v}")
            except Exception as e:
                self.md.DEBUG(f"Critical error {e}", 2, "MeasureMaster", True)
                time.sleep(5)
