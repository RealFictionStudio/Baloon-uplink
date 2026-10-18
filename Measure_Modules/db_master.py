import sqlite3

from .modules_debug import ModuleDebuger


class DBMaster:
    def __init__(self, db_path: str = "airdata.db") -> None:
        self.db_path = db_path

        self.DEBUG = ModuleDebuger()
        self.name = "DBMaster"

        self.init_db()

    def init_db(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def init_table(self, table_name: str, test_record: dict) -> bool:
        if table_name.strip() == "":
            raise Exception("Table name not set. Unable to init table")
        if type(test_record) != dict:
            raise Exception("Test record need to be type dictionary")

        query = []
        # Temporary all records will be REAL
        for key in test_record.keys():
            query.append(f"{key} REAL")
        try:
            self.cursor.execute(
                f""" 
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        {",\n".join(query)}
                    )
                """
            )
        except Exception as e:
            self.DEBUG.DEBUG(str(e), 2, self.name, True)

        self.db_update()

        return True

    def insert_record(self, module_name: str, record: dict):
        if module_name.strip() == "":
            raise Exception("Table name not set. Unable to init table")
        if type(record) != dict:
            raise Exception("Test record need to be type dictionary")
        if module_name not in self.get_all_tables():
            self.init_table(module_name, record)
        try:
            self.cursor.execute(
                "INSERT INTO bme280table(time, temperature, humidity, pressure) VALUES (?, ?, ?, ?)",
                tuple(record.values()),
            )
        except Exception as e:
            self.DEBUG.DEBUG(str(e), 2, self.name, True)

        self.db_update()

    def get_all_tables(self) -> list[str]:
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        res = []
        for table in self.cursor.fetchall():
            res.append(table[0])

        return res

    def db_update(self):
        self.conn.commit()

    def close_db(self) -> None:
        self.db_update()
        self.conn.close()
