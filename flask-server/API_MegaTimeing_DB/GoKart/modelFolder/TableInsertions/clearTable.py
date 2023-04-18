import psycopg2

#Tanken är att databasen töms helt och hållet 1 gång i månaden.

class TimedFunctionsDB():
    @classmethod
    def clearAll(cursor):
        try:
            cursor.execute('TRUNCATE "bilinfo"') 

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            cursor.close()

    