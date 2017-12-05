import pymysql.cursors
import pandas as pd
import numpy as np


def main():

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='lucky',
                                 db='network',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM allplace"
            cursor.execute(sql)
            result = cursor.fetchall()
            writefile(result, cursor)

    finally:
        connection.close()


def writefile(result, cursor):
    file = open('global_to_local.txt', 'w')
    for glob in result:
        sql = "SELECT * FROM timeseries WHERE crime ='" + glob["crime"] + "'"
        cursor.execute(sql)
        res = cursor.fetchall()
        for local in res:
            globalline = glob['timeline'].split(",")
            localline = local['timeline'].split(",")
            line1 = [int(a) for a in globalline]
            line2 = [int(a) for a in localline]

            for k in range(11):
                series1 = line1[k * 12:(k * 12 + 12)];
                series2 = line2[k * 12:(k * 12 + 12)];
                if max(series1) != 0:
                    series1 = [q / max(series1) for q in series1]
                if max(series2) != 0:
                    series2 = [q / max(series2) for q in series2]

                c = autocorrelate(pd.Series(series1),
                                  (pd.Series(series2)))

                index = findMax(c)
                if len(index) != 24:
                    maxn = 0
                    for m in index:
                        if abs(m) > abs(maxn):
                            maxn = m
                    if maxn < 0:
                        file.write(local["crime"] + "\t" + local["neighbor"] + "\t" +
                                   str(c[int(maxn + 11.5)]) + "\t" + str(k + 2005) + "\n")
    file.close()

def autocorrelate(x, y):
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
