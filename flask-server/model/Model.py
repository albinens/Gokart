from model.dbConnect import DataBaseConnection
from model.get_data import get_data
from model.calculations import Calculations


class Model():
    def __init__(self) -> None:
        #self.__apiConnecter = ApiConnections()
        self.__dbConnecter = DataBaseConnection()
        self.__getdata = get_data()
        self.__Calculations = Calculations()

    def run(self) -> None:
        db = self.__dbConnecter.connect()
        cursor = db.cursor()
        min, max = (40, 70)

        # DENNA RETURNERAR DATA ENDAST. FUNKAR? JA
        data = self.__getdata.read_table(db,13, "0")
        self.__Calculations.average(data, min, max)
        self.__Calculations.laps(data, min, max)
        self.__Calculations.high(data, max)
        self.__Calculations.low(data, min)
        self.__dbConnecter.disconnect(db)
