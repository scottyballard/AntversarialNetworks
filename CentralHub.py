import json
import socket
from threading import Thread

import pymysql


def db_init(database, table_name, table_name2):
    connection = pymysql.connect(host='localhost', user='root', password='')
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS "+database)
    connection.select_db(database)
    sql_create = "CREATE TABLE IF NOT EXISTS "+table_name+"( ID INT NOT NULL AUTO_INCREMENT primary key, MsgID INT " \
                                                          "NOT NULL , IP VARCHAR(30) NOT NULL , Result INT NOT NULL );"
    sql_create1 = "CREATE TABLE IF NOT EXISTS "+table_name2+"( ID INT NOT NULL AUTO_INCREMENT primary key, " \
                                                            "IP VARCHAR(30) NOT NULL , Port INT NOT NULL );"
    cursor.execute(sql_create)
    cursor.execute(sql_create1)
    connection.commit()
    return connection


def socket_init(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', port)
    sock.bind(server_address)
    return sock


def profile(connection, table_name):
    # Create a listener socket for ants to relay info
    sock = socket_init(10000)
    # Loop to process ant info
    while True:
        data, address = sock.recvfrom(4096)
        if data:
            data_json = json.loads(data)
            cursor = connection.cursor()
            insert = "INSERT into %s VALUES %s,'%s', %s"
            cursor.execute(insert, table_name, data_json.get("msgid"), data_json.get("ip"), data_json.get("result"))
            connection.commit()
            # TODO: Add function to make profile determinations


def monitor(connection, table_name, addresses):
    # Create a listener socket for ants to relay info
    sock = socket_init(10001)
    # Loop to process ant info
    while True:
        data, address = sock.recvfrom(4096)
        addresses.add(address) # Add to running tally of active ants
        if data:
            data_json = json.loads(data)
            cursor = connection.cursor()
            insert = "INSERT into %s VALUES '%s', %s"
            cursor.execute(insert, table_name, data_json.get("ip"), data_json.get("port"))
            connection.commit()
            if is_adversary(connection, table_name, data_json.get("ip")):
                notify_ants(address, data_json.get("ip"))


def is_adversary(connection, table_name, address):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM %s WHERE IP='%s'", table_name, address)
    rows = cursor.fetchall()
    sus_queries = 0
    for row in rows:
        ++sus_queries
    if sus_queries > 5:
        return True
    else:
        return False

def notify_ants(ants, bad_ip):
    s


dbConnect = db_init("Ants", "Profiles", "Monitor")
# set to contain all of the ant IPs
address_list = set(())

profiler = Thread(target=profile, args=[dbConnect, "Profiles"])
profiler.start()
monitoring = Thread(target=monitor, args=[dbConnect, "Monitor", address_list])

# Logic for processing the data will go here

dbConnect.close()

