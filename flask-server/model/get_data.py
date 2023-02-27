from model.dbConnect import DataBaseConnection
import time
import psycopg2
import requests
import json


class get_data():

    @classmethod
    def read_table(self, nr):
        try:

            data = []
            db = DataBaseConnection.connect()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM bilinfo WHERE bilnr ="+str(nr))

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
