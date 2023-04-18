import time
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from model.Model import Model
from model.dbConnect import DataBaseConnection
from model.get_data import get_data
from model.calculations import Calculations
from API_MegaTimeing_DB.GoKart.modelFolder.Modeldb import ModelDB

# För att starta:
# Kör denna pythonfilen. Öppnar port 5000. (http://localhost:5000/api/members)
# Sedan öppna ny terminal gå till my-app och kör 'npm start'. Då öppnas (http://localhost:3000/)

# Multiselect option: Ifall valt är >=2 ska en färdig normalfördelningskurva visas
# med "DOTS" som representerar vart de valda bilarna ligger generellt!
# Väljs 1bil görs en bellcurve för bara den bilen. INGA DOTS

# Tjo brorn nu är allt på git

# Define för FlaskBackend
app = Flask(__name__)

# STOPPAR CORS ERROR FÖR FRONTEND
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# Class Main kör kör och uppdaterar backend


class Main():
    def __init__(self) -> None:
        self.__model = Model()
        self.timeStart = time.time()
        self.unix_time = 10000000000
        self.db = DataBaseConnection.connect()
        # Raden nedan är en konstruktor som skapar variabeln __UpdateModelDB som
        # ger oss lättare åtkomst till classens functioner. Tex "run"
        self.__UpdateModelDB = ModelDB

    def get_update_modelDB(self):
        # Funktionen returnerar den konstruerade variabeln som motsvarar klassfunktionen
        return self.__UpdateModelDB.run(self)

    def main(self):
        self.__model.run()
        # Raden nedan kör och uppdaterar databasen med värden från de 3 senaste racing-månaderna
        # self.__UpdateModelDB.run()

    def getTimeStart(self):
        print(self.timeStart, "TIME START ---------------------")
        return self.timeStart

    def getUnixTime(self):
        return self.unix_time

    def setUnixTime(self, newUnixTime):
        self.unix_time = newUnixTime

    def checkDBUpdate(x):
        myModel = ModelDB()
        myModel.run(2)
        print(time.time(), "TIMENOW----------------")

    # Skapar backend på routen nedan

    @app.route("/api/laps/<id>", methods=["GET"])
    @cross_origin()
    def lapsOfCar(id):
        # TANKE: CONNECT HÄR
        database = main.db
        # ID kan även vara stringen "UPDATE" som ska skicka en updatePuls till functionen __UpdateModelDB
        if id == "UPDATE":

            unix_time = main.getUnixTime()
            startTime = main.getTimeStart()
            if startTime - 120 <= time.time():  # DENNA KOMMER SKE FÖRSTA GÅNGEN
                main.checkDBUpdate()
                main.setUnixTime(time.time())
                main.timeStart = 10000000000
                print(unix_time, "UNIX TIME--------------")
                return jsonify("UPDATED")

            elif (unix_time) <= (time.time()-120):  # OM DET HAR GÅTT MER ÄN 120SEK FRÅN SENAST
                main.checkDBUpdate()
                main.setUnixTime(time.time())
                return jsonify("UPDATED")

            elif (unix_time + 120) >= (time.time()):  # OM DET INTE GÅTT 120SEK FRÅN SENAST
                TimeLeft = str(int(unix_time+120-time.time()))
                print(TimeLeft)
                print(unix_time, "UNIX TIME --------")
                print(time.time(), "TIME NOW-----------")
                return (jsonify(TimeLeft))
            # Main.get_update_modelDB()  # PROBLEM MED ATT KÖRA FUNKTIONEN
            # ModelDB.run()
            print("------------UPDATE--------------")
            return (jsonify("UPDATED"))
        # ID kan vara csv. Filtering sker här:
        wantedId = []
        values = []
        if "," in id:
            values = id.split(",")
            if len(values[-1]) > 2:
                Time = values[-1]
                print('HÄR ÄR TID - ', Time)
                wantedId = values[:-1]
            else:
                wantedId = values
                Time = 1
        else:
            wantedId.append(id)
            Time = 1
        averageList = []

        for id in wantedId:
            try:
                # DataBaseConnection.disconnect(database)
                print("TIME __----------------", Time)
                laps = get_data.read_table(database, id, Time)
                averageList.append([id, Calculations.average(
                    laps, 10, 70), Calculations.low(laps, 52)])

            except:
                # wantedId.remove(id)
                pass

            # return jsonify(laps),

        print("-------------AVERAGELIST", averageList)
        # OCH DISCONNECT HÄR. PRÖVA

        return jsonify(averageList)


if __name__ == "__main__":
    main = Main()
    main.main()
    app.run(debug=True)
