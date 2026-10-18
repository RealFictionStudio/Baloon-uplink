class ModuleDebuger:
    def __init__(self, debug: bool = False) -> None:
        self.debug = self.config_debug(debug)

    def config_debug(self, value: bool) -> bool:
        if type(value) != bool:
            self.DEBUG("Inaproperiate debug config value", 1)
            return False

        self.debug = value
        return True

    def DEBUG(
        self, text: str = "", dtype: int = 0, name: str = "Module", force: bool = False
    ) -> None:
        if text.strip() == "":
            return
        if self.debug or force:
            match dtype:
                case 0:
                    # Info
                    print(f"{name}: [?] {text}")
                case 1:
                    # Warning
                    print(f"{name}: [*] {text}")
                case 2:
                    # Error
                    print(f"{name}: [!] {text}")
                case _:
                    name = "Annonymous" if name.strip() == "" else name
                    print(f"{name}: [?] {text}")
