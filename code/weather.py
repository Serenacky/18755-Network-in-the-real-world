import pymysql.cursors
import pandas as pd
import numpy as np

def main():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='luckyday',
                                 db='network',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    weather = [29.7, 32.4, 35.3, 52.3, 56.3, 71.7, 75.1, 73.7, 67.3, 53.4, 44.0, 27.6, 38.1, 30.4, 38.2, 53.7, 58.8, 66.2,
               73.4, 72.9, 61.0, 50.8, 45.2, 38.8, 32.5, 20.9, 43.3, 47.5, 63.8, 69.5, 70.6, 74.0, 66.7, 59.3, 41.8, 34.5,
               31.4, 29.4, 37.1, 53.9, 57.1, 70.0, 72.6, 69.7, 65.9, 51.1, 40.1, 31.3, 22.0, 31.2, 42.3, 52.1, 61.2, 68.2,
               69.4, 71.8, 64.9, 50.7, 47.2, 31.1, 25.9, 26,4, 43.3, 55.4, 63.6, 70.8, 75.6, 74.4, 65.7, 53.4, 42.3, 25.6,
               24.2, 31.8, 39.2, 53.5, 62.9, 70.0, 76.9, 72.8, 65.4, 52.8, 46.9, 37.5, 32.8, 35.4, 51.5, 50.4, 67.0, 70.1,
               76.8, 71.5, 63.6, 53.5, 39.6, 38.1, 31.5, 28.7, 35.9, 52.4, 62.5, 69.4, 73.4, 70.7, 64.0, 56.3, 39.4, 34.2,
               22.1, 25.7, 34.5, 52.2, 62.0, 70.6, 70.5, 70.0, 64.1, 53.7, 38.8, 35.5, 25.3, 18.3, 35.8, 52.9, 66.1, 70.4,
               73.3, 71.3, 69.6, 53.9, 48.6, 44.5]

    hotmask = [0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0]
    coldmask = [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
    file = open("weather.csv", 'w')

    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM allplace"
            cursor.execute(sql)
            result = cursor.fetchall()
            for i in range(len(result)):
                type = result[i]['crime']
                timeline = result[i]['timeline'].split(",")
                line = [int(a) for a in timeline]
                for k in range(11):
                    wn = weather[k * 12:(k * 12 + 12)]
                    wn = [r / max(wn) for r in wn]

                    ln = line[k * 12:(k * 12 + 12)]
                    ln = [q / max(ln) for q in ln]

                    hotTemp = [a*b for a,b in zip(wn,hotmask)]
                    hotLine = [a*b for a,b in zip(ln,hotmask)]
                    hotc = crosscorrelate(pd.Series(hotTemp),
                                       (pd.Series(hotLine)))

                    coldTemp = [a*b for a,b in zip(wn,coldmask)]
                    coldLine = [a*b for a,b in zip(ln,coldmask)]

                    coldc = crosscorrelate(pd.Series(coldTemp),
                                       (pd.Series(coldLine)))

                    index1 = findMax(hotc)
                    index2 = findMax(coldc)
                    if len(index1) != 24:
                        maxn = 0
                        for m in index1:
                            if abs(m) > abs(maxn):
                                maxn = m
                            if maxn < 0:
                                file.write("HotWeather" + "," + type + "," +
                                       str(hotc[int(maxn + 11.5)]) + "," + str(k + 2005) + "\n")

                    if len(index2) != 24:
                        maxn = 0
                        for m in index2:
                            if abs(m) > abs(maxn):
                                 maxn = m
                            if maxn < 0:
                                file.write("ColdWeather" + "," + type + "," +
                                   str(coldc[int(maxn + 11.5)]) + "," + str(k + 2005) + "\n")
    finally:
        connection.close()

    file.close()

def crosscorrelate(x, y):
    sz = x.shape[0]
    out = np.zeros(sz * 2)
    x1 = np.zeros(sz * 2)
    y1 = np.zeros(sz * 2)
    x1[:sz] = x
    y1[:sz] = y
    for step in range(sz * 2):
        out[step] = np.correlate(np.roll(x1, step), y1)
    return out


def findMax(c):
    index = []
    for i in range(len(c)):
        if c[i] == max(c):
            j = i - 11.5
            index.append(j)
    return index


main()


