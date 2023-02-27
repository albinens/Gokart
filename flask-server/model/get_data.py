from model.dbConnect import DataBaseConnection
import time
import psycopg2
import requests
import json


class get_data():

    @classmethod
    def read_table(self, nr, time):
        try:
            print(time, "---------------")
            data = []
            db = DataBaseConnection.connect()
            cursor = db.cursor()

            if time == None:
                sentence = ""
            else:
                # First check so that time is a string and NOT an int
                if type(time) == int:
                    time = str(time)
                sentence = " AND TIME > "+time
                print(sentence)
            cursorRequest = "SELECT * FROM bilinfo WHERE bilnr = " + \
                str(nr)+sentence
            print(cursorRequest)
            cursor.execute(cursorRequest)

            # Retrieve the results of the query
            rows = cursor.fetchall()

            # Print the rows
            for row in rows:

                data.append(row)
            print("Successful SELECT from table")
            # print(data)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            cursor.close()

            return data
