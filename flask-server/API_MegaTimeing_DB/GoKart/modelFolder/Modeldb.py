
from API_MegaTimeing_DB.GoKart.modelFolder.ApiConnections import ApiConnections
from API_MegaTimeing_DB.GoKart.modelFolder.DataBaseConnection import DataBaseConnection
from API_MegaTimeing_DB.GoKart.modelFolder.HeatParser import HeatParser
from API_MegaTimeing_DB.GoKart.modelFolder.TableInsertions.InsertIntoCarInfoTable import InsertIntoCarInfoTable


class ModelDB():
    def __init__(self) -> None:
        self.__apiConnecter = ApiConnections()
        self.__dbConnecter = DataBaseConnection()
        self.__inserter = InsertIntoCarInfoTable()
        self.__lastReadId = self.__apiConnecter.get_heatIDs(
            self.__apiConnecter.get_months()[-1])

    def run(self, updateOptimize) -> None:
        db = self.__dbConnecter.connect()
        # Här används inte 0 så att om inga nya varv hittas ska inte en rom lista returneras från koden nedan
        lastReadId = self.__lastReadId[1]
        ##

        # Denna raden printar alla heatIDS för månad 11
        lastSeasonsMonths = (ApiConnections.get_months(self)[
                             (-3)+updateOptimize:])
        for heatID in self.__apiConnecter.get_heatIDs(lastSeasonsMonths):
            if heatID > lastReadId:

                print(heatID)
                self.__apiConnecter.connect_to_dropin_heat(
                    heatID)  # test value
                heatParserObj = HeatParser()
                racerList = heatParserObj.parse(
                    self.__apiConnecter.get_active_connection())
                cursor = db.cursor()
                self.__inserter.insertIntoTable(racerList, cursor)
                db.commit()

                print(racerList)

        self.__dbConnecter.disconnect(db)
