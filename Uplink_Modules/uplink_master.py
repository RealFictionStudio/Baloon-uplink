from .modules_debug import ModuleDebuger


class UplinkMaster:
    def __init__(self, debug: bool = False) -> None:
        # PUBLIC
        self.debuger = ModuleDebuger(debug=debug)
        self.DEBUG = self.debuger.DEBUG
        self.com_modules = dict()

        self.name = "UplinkMaster"

        # PRIVATE

    def add_com_module(self, com_mod):
        if com_mod.name is not None:
            if com_mod.name in self.com_modules.keys():
                cnt = len(
                    list(
                        map(
                            lambda x: x.startswith(com_mod.name),
                            list(self.com_modules.keys()),
                        )
                    )
                )
                self.com_modules[f"{com_mod.name}{cnt+1}"] = com_mod
            else:
                self.com_modules[com_mod.name] = com_mod

        else:
            cnt = len(
                list(
                    map(
                        lambda x: x.startswith("Unknown"), list(self.com_modules.keys())
                    )
                )
            )
            self.com_modules[f"Unknown{cnt+1}"] = com_mod

    def listen_with(self, mod_name: str):
        if mod_name not in self.com_modules.keys():
            self.DEBUG(
                f"Unable to listen with {mod_name}, module not found",
                2,
                self.name,
                force=True,
            )
            return

        try:
            return self.com_modules[mod_name].listen()
        except Exception as e:
            self.DEBUG(str(e), 2, self.name, force=True)
