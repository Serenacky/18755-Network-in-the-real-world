import pymysql.cursors

connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='luckyday',
                                 db='network',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
file1 = open("interedge.csv",'w')
file2 = open("internode.csv",'w')
# file.write('Source,Target,Type,Weight,Id,start,end');


try:
    with connection.cursor() as cursor:
        node = []
        sql = "SELECT * FROM interCrime"
        cursor.execute(sql)
        result = cursor.fetchall()
        for data in result:
            count = 0
            if float(data["cor"]) > 3.5:
                file1.write(data["source"].replace(",", " ") + "," + data["target"].replace(",", " ") + ",Directed," + data["cor"] + "," + data["year"]
                            + "," + str(0.8 + float(data["year"])) + "\n")
                if data["source"] not in node:
                    file2.write(data["source"].replace(",", " ") + "," + data["source"].split(",")[0] + "," + data["source"].split(",")[1] + "\n")
                    node.append(data["source"])
                if data["target"] not in node:
                    file2.write(data["target"].replace(",", " ") + "," + data["target"].split(",")[0] + "," + data["target"].split(",")[1] + "\n")
                    node.append(data["target"])

finally:
        connection.close()

file1.close()
file2.close()
