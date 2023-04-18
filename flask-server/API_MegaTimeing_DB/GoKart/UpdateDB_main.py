
#from GoKart.model.Model import Model
from modelFolder.Modeldb import ModelDB
from modelFolder.TableInsertions.clearTable import TimedFunctionsDB
from modelFolder.DataBaseConnection import DataBaseConnection
import schedule
import time


class DB_Main():
    def __init__(self) -> None:
        self.__model = ModelDB()
        self.db = DataBaseConnection()
    def UpdateDB(self):
        db = self.db.connect()
        self.__model.run(db,0)
        db.close()


if __name__ == "__main__":
    main = DB_Main()
    main.UpdateDB()
