import psycopg2

from config.config import config


class DataBaseConnection():

    @classmethod
    def connect(cls):
        try:
            # read connection parameters
            params = config()
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            database = psycopg2.connect(**params)
            return database 
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    @classmethod 
    def disconnect(cls, db):
        if db is not None:
            db.close()
            print('Database connection closed.')

    # @classmethod
    # def getDataBaseConnection(cls):
    #     return cls.__database