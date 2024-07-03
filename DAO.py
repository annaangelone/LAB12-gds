from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDDCountry():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor()
        query = ("""SELECT DISTINCT Country
                    FROM go_retailers""")
        cursor.execute(query, )

        for row in cursor:
            result.append(row[0])
            # equivale a creare il costruttore lungo con tutte le righe con i rispettivi attributi

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getRetailersByCountry(country):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("""SELECT *
                        FROM go_retailers
                        WHERE Country = %s""")
        cursor.execute(query, (country,))

        for row in cursor:
            result.append(Retailer(row["Retailer_code"], row["Retailer_name"], row["Type"], row["Country"], 0))
            # equivale a creare il costruttore lungo con tutte le righe con i rispettivi attributi

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getRetailers():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("""SELECT *
                    FROM go_retailers""")
        cursor.execute(query,)

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(anno, r1: Retailer, r2: Retailer):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor()
        query = ("""SELECT COUNT(DISTINCT gds1.Product_number) as peso
                    FROM go_daily_sales gds1, go_daily_sales gds2
                    WHERE YEAR(gds1.Date) = %s AND YEAR(gds1.Date) = YEAR(gds2.Date) AND
                    gds1.Retailer_code = %s AND gds2.Retailer_code = %s
                    AND gds1.Product_number = gds2.Product_number""")

        cursor.execute(query, (anno, r1.Retailer_code, r2.Retailer_code, ))

        for row in cursor:
            result.append(row[0])
            # equivale a creare il costruttore lungo con tutte le righe con i rispettivi attributi

        cursor.close()
        conn.close()
        return result