import pymysql.cursors

file = open('weathergephi.csv','w')
connection = pymysql.connect(host='localhost',
                            user='root',
                            password='luckyday',
                            db='network',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        sql = 'SELECT max(cor) FROM weather'
        cursor.execute(sql)
        maxcor = float(cursor.fetchone()["max(cor)"])

        sql = 'SELECT * FROM weather'
        cursor.execute(sql)
        weather = cursor.fetchall()
        for data in weather:
            if float(data["cor"])/maxcor > 0.6:
                sql = 'SELECT max(cor) FROM global_to_local'
                cursor.execute(sql)
                maxglobaltolocal = float(cursor.fetchone()["max(cor)"])
                sql = "SELECT * FROM global_to_local WHERE crime='" + data["target"] + "'"
                cursor.execute(sql)
                result = cursor.fetchall()
                for get in result:
                    if float(get["cor"])/maxglobaltolocal > 0.6:
                        file.write(data["source"] + "," + get["crime"] + " " + get["neighbor"] + ",Directed,"
                                   + str((float(get["cor"])/maxglobaltolocal)*(float(data["cor"])/maxcor)) + "," + get["year"]
                                   + "," + str(0.8 + float(get["year"])) + "\n")

finally:
    connection.close()