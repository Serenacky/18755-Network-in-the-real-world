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

    rate = [6.1, 6.2, 5.9, 4.9, 5.1, 5.4, 5.4, 5.1, 4.7, 4.5, 4.8, 4.6, 5.5, 5.4, 5.0, 4.5, 4.7, 5.1, 5.1, 4.9, 4.2, 3.9,
           4.2, 4.1, 5.1, 4.9, 4.3, 3.8, 4.1, 4.5, 4.7, 4.6, 4.0, 3.9, 4.1, 4.5, 5.4, 5.3, 5.0, 4.1, 4.7, 5.1, 5.3, 5.4,
           4.7, 4.8, 5.3, 5.9, 7.3, 7.5, 7.4, 6.7, 7.2, 7.6, 7.8, 7.7, 7.1, 7.1, 7.1, 7.4, 9.1, 9.5, 8.8, 7.8, 8.1, 8.0,
           8.1, 7.9, 7.1, 7.0, 7.3, 7.3, 8.2, 7.9, 7.5, 6.7, 7.2, 7.9, 7.9, 7.8, 7.0, 6.8, 6.7, 6.8, 7.8, 7.6, 7.3, 6.4,
           7.0, 7.6, 8.0, 7.7, 6.8, 6.7, 6.5, 7.0, 8.4, 7.7, 7.2, 6.4, 6.7, 7.2, 7.3, 7.0, 6.2, 6.2, 5.9, 5.8, 6.7, 6.6,
           6.4, 5.1, 5.6, 5.8, 6.3, 5.9, 4.9, 4.8, 4.8, 4.8, 6.0, 5.7, 5.6, 4.8, 5.4, 5.5, 5.8, 5.4, 4.9, 4.8, 4.8, 4.9]

    file = open("unemployment.csv", 'w')
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
                    rn = rate[k * 12:(k * 12 + 12)];
                    rn = [r / max(rn) for r in rn];

                    ln = line[k * 12:(k * 12 + 12)];
                    ln = [q / max(ln) for q in ln];

                    c = crosscorrelate(pd.Series(rn),
                                       (pd.Series(ln)))
                    index = findMax(c)
                    if len(index) != 24:
                        maxn = 0
                        for m in index:
                            if abs(m) > abs(maxn):
                                maxn = m
                        if maxn < 0:
                            file.write("unemployment" + "," + type + "," +
                                       str(c[int(maxn + 11.5)]) + "," + str(k + 2005) + "\n")
                        if maxn > 0:
                            file.write(type + "," + "unemployment" + "," +
                                       str(c[int(maxn + 11.5)]) + "," + str(k + 2005) + "\n")
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


