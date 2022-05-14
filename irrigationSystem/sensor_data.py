import serial
import pymysql
import time
device='/dev/ttyS0'

arduino= serial.Serial(device,9600)


while True:
    data= arduino.readline()
    time.sleep(1)
    data1= arduino.readline()
    time.sleep(1)
    data2= arduino.readline()
    time.sleep(1)
    data3= arduino.readline()
    time.sleep(1)
    data = int (data)
    data1= str (data1)
    data2= str (data2)
    data3 = str (data3)
    time.sleep(1)
    print(data)
    print(data1)
    print(data2)
    print(data3)
    if (data< 350):
        arduino.write(b"1")
    elif (data > 350):
        arduino.write(b"2")
    
    dbConn = pymysql.connect("localhost","pi","","irrigationSystem_db") or die("could not connect to database")
    print(dbConn)

    with dbConn:
        cursor= dbConn.cursor()
        cursor.execute("INSERT INTO sensorsData(waterLevel,photoRes,humidity,temperature) VALUES(%d,%s,%s,%s)" %(data, data1, data2, data3))
        dbConn.commit
        cursor.close()

# 