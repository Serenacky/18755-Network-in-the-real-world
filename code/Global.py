import pymysql.cursors
import pandas as pd

def main():
    file = pd.read_csv('10years.csv', low_memory=False)
    crime_type = crimeType(file, 10)

    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Wishmeluck0715',
                             db='network',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    file1 = open('allcrime_for_eachtype.txt', 'w')
    try:
        with connection.cursor() as cursor:
            for crime in crime_type:
                counts = []
                for i in range(132):
                    counts.append(0)
                sql = 'SELECT timeline FROM timeseries WHERE crime="' + crime + '"'
                cursor.execute(sql)
                result = cursor.fetchall()
                for time in result:
                    data = time['timeline'].split(',')
                    counts = [counts[i]+int(data[i]) for i in range(len(counts))]

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

main()
