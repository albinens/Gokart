
from API_MegaTimeing_DB.GoKart.modelFolder.ApiConnections import ApiConnections
from API_MegaTimeing_DB.GoKart.modelFolder.DataBaseConnection import DataBaseConnection
from API_MegaTimeing_DB.GoKart.modelFolder.HeatParser import HeatParser
from API_MegaTimeing_DB.GoKart.modelFolder.TableInsertions.InsertIntoCarInfoTable import InsertIntoCarInfoTable


class ModelDB():
    def __init__(self) -> None:
        self.__apiConnecter = ApiConnections()
        self.__dbConnecter = DataBaseConnection()
        self.__inserter = InsertIntoCarInfoTable()

    def run(self, updateOptimize) -> None:
        db = self.__dbConnecter.connect()
        ##
        # Här ska en forloop köras för x-antal månader.
        ##
        # Här ska en forloop köras för alla heats i en specifik månad
        ##
        # for self.__apiConnecter.connect_to_dropin(11).

        # Denna raden printar alla heatIDS för månad 11
        lastSeasonsMonths = (ApiConnections.get_months(self)[
                             (-3)+updateOptimize:])
        for heatID in self.__apiConnecter.get_heatIDs(lastSeasonsMonths):
            print(heatID)
            self.__apiConnecter.connect_to_dropin_heat(heatID)  # test value
            heatParserObj = HeatParser()
            racerList = heatParserObj.parse(
                self.__apiConnecter.get_active_connection())
            cursor = db.cursor()
            self.__inserter.insertIntoTable(racerList, cursor)
            db.commit()

            print(racerList)

        self.__dbConnecter.disconnect(db)
