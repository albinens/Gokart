from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from model.Model import Model
from model.dbConnect import DataBaseConnection
from model.get_data import get_data
from model.calculations import Calculations


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

    def main(self):
        self.__model.run()

    # Skapar backend på routen nedan

    @app.route("/api/laps/<id>", methods=["GET"])
    @cross_origin()
    def lapsOfCar(id):
        # ID kan vara csv. Filtering sker här:
        wantedId = []
        values = []
        if "," in id:

            values = id.split(",")
            if len(values[-1]) > 3:
                time = values[-1]

                print('HÄR ÄR TID - ', time)
                wantedId = values[:-1]
            else:
                wantedId = values
                time = 1

        else:
            wantedId.append(id)
            time = 1

        averageList = []
        for id in wantedId:
            print("TIME __----------------", time)
            laps = get_data.read_table(id, time)
            averageList.append(Calculations.average(laps, 10, 100))
            # return jsonify(laps),
        return jsonify(averageList)


if __name__ == "__main__":
    main = Main()
    main.main()
    app.run(debug=True)
