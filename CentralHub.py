import socket
from threading import Thread

import pymysql


def db_init(database, table_name):
    connection = pymysql.connect(host='localhost', user='root', password='')
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS "+database)
    connection.select_db(database)
    sql_create = "CREATE TABLE IF NOT EXISTS "+table_name+"( ID INT NOT NULL AUTO_INCREMENT primary key, MsgID INT " \
                                                          "NOT NULL , IP VARCHAR(30) NOT NULL , Result INT NOT NULL );"
    cursor.execute(sql_create)
    connection.commit()
    return connection


def listen(connection, table_name, addresses):
    # Create a listener socket for ants to relay info
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 10000)
    sock.bind(server_address)
    # Loop to process ant info
    while True:
        data, address = sock.recvfrom(4096)
        addresses.add(address)
        if data:
            data_list = data.split(",")
            cursor = connection.cursor()
            insert = "INSERT into %s VALUES %s,'%s', %s"
            cursor.execute(insert, table_name, data_list[0], data_list[1], data_list[2])
            connection.commit()


dbConnect = db_init("Ants", "Hosts")
# set to contain all of the ant IPs
address_list = set(())

listener = Thread(target=listen, args=[dbConnect, "Hosts", address_list])
listener.start()

# Logic for processing the data will go here

dbConnect.close()

