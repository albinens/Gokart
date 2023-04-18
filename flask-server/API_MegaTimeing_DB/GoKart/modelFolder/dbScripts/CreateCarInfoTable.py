
from GoKart.model.dbScripts.ICreateTable import ICreateTable


class CreateCarInfoTable(ICreateTable):
    @classmethod
    def createTable(cls, cursor) -> None:
        create_script = """CREATE TABLE IF NOT EXISTS carInfo
        (bilnr   int,
        id      int PRIMARY KEY,
        time    int,
        laptimes float[],
        name    varchar(10)
        )"""
        cursor.execute(create_script)
