import pymysql.cursors
import pandas as pd

def main():
    file = pd.read_csv('10years.csv', low_memory=False)
    crime_type = crimeType(file, 10)

    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='lucky',
                             db='network',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    file1 = open('timeseries.txt', 'w')
    try:
        with connection.cursor() as cursor:
            for crime in crime_type:
                for neighbor in getNeighbors(file, crime):
                    dayth = []
                    counts = []
                    for i in range(2005, 2016):
                        for j in range(1, 13):
                            dayth.append(str(i) + '.' + str(j))
                            counts.append(0)
                    sql = 'SELECT * FROM crimedata WHERE crime=' + crime + ' AND neighbor=' + neighbor
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    for time in result:
                        data = time["time"].split('/')[0] + '.' + time["time"].split('/')[1]
                        counts[dayth.index(data)] = counts[dayth.index(data)] + 1

                    file1.write(crime + "\t" + ','.join(str(i) for i in counts) + "\n")
    finally:
        connection.close()

    file1.close()


def crimeType(file,n):
    # count total complaints numbers by complaint type
    type_counts = file['HIERARCHYDESC'].value_counts()
    type_name = type_counts.keys()
    # return the top n crime type
    return type_name[0:n]

def getNeighbors(file, crime_type):
    # count crime numbers by different borough
    select = file['HIERARCHYDESC'] == crime_type
    crime_top = file[select]
    neighbor_counts = crime_top['INCIDENTNEIGHBORHOOD'].value_counts()
    # return all the neighbors.
    return neighbor_counts.keys()

main()
