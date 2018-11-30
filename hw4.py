import socket
import time
from threading import Thread


def socket_init(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', port)
    sock.bind(server_address)
    return sock


def device_thread(name, port, upstream, rate):
    sock = socket_init(port)
    sockOut = socket_init(port+10)
    power_lvl = 0
    expected_power = 0
    initial_time = time.time()
    while True:
        current_time = time.time()
        if current_time > initial_time + 3:
            initial_time = current_time
            if abs(3-expected_power) > 1:
                print(name+str(expected_power))
                print(name+'\'s downstream neighbor is compromised')
            expected_power = 0
        time.sleep(rate)
        sockOut.sendto('status is normal '+name, ('localhost', upstream))
        power_lvl += 1
        data = sock.recv(4096)
        print(data)
        power_lvl += 1
        expected_power += 1
        if name != 'hub':
            sock.sendto(data, ('localhost', upstream))
            power_lvl += 1


profiler = Thread(target=device_thread, args=['hub', 10000, 0, 1])
profiler1 = Thread(target=device_thread, args=['hrm', 10001, 10000, 1])
profiler2 = Thread(target=device_thread, args=['pulseOx', 10002, 10001, 1])
profiler3 = Thread(target=device_thread, args=['sensor', 10003, 10002, 1])
profiler4 = Thread(target=device_thread, args=['accelerometer', 10004, 10003, 1])

profiler.start()
profiler1.start()
profiler2.start()
profiler3.start()
profiler4.start()

newsock = socket_init(20000)
'''for x in range(0, 12):
    newsock.sendto("hello", ('localhost', 10004))'''
