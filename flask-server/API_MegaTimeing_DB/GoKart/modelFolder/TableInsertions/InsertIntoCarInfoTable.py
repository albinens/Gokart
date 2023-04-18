import psycopg2

from API_MegaTimeing_DB.GoKart.modelFolder.TableInsertions.ITableInsertion import ITableInsertion


class InsertIntoCarInfoTable(ITableInsertion):
    @classmethod
    def insertIntoTable(cls, data: list, cursor) -> None:
        try:

            insert_script = 'INSERT INTO "bilinfo" (bilnr, id, time, laptimes, name) VALUES(%s,%s,%s,%s,%s)'
            for race in data:
                insert_value = (
                    race["nr"], race["id"], race["date"], race["laptimes"], str(race["name"]))
                # print(insert_value)
                cursor.execute(insert_script, insert_value)
            print("Successful insertion into Bilinfo")

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            cursor.close()
