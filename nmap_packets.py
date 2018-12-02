
from scapy.layers.inet import *

#Packets for nmap os tests

def send_t2(hostname):
    ant = IP(dst=hostname) / TCP(sport=9090, dport=80, options=[('Timestamp', (0xFFFFFFFF, 0L)), ('MSS', 265),
    ('NOP', ()), ('SAckOK', ''), ('WScale', 10)])
    ant[IP].flags = 'DF'
    ant[TCP].flags = ''
    ant.window = 128
    scan = sr1(ant, timeout=1)
    return process_t_scan(scan, ant)


def send_t3(hostname):
    ant = IP(dst=hostname) / TCP(sport=9091, dport=80, options=[('Timestamp', (0xFFFFFFFF, 0L)), ('MSS', 265),
    ('NOP', ()), ('SAckOK', ''), ('WScale', 10)])
    ant[TCP].flags = 'SFPU'
    ant.window = 256
    scan = sr1(ant, timeout=1)
    return process_t_scan(scan, ant)


def send_t4(hostname):
    ant = IP(dst=hostname) / TCP(sport=9092, dport=80, options=[('Timestamp', (0xFFFFFFFF, 0L)), ('MSS', 265),
    ('NOP', ()), ('SAckOK', ''), ('WScale', 10)])
    ant[IP].flags = 'DF'
    ant[TCP].flags = 'A'
    ant.window = 1024
    scan = sr1(ant, timeout=1)
    return process_t_scan(scan, ant)


def send_t5(hostname):
    ant = IP(dst=hostname) / TCP(sport=9093, dport=23, options=[('Timestamp', (0xFFFFFFFF, 0L)), ('MSS', 265),
    ('NOP', ()), ('SAckOK', ''), ('WScale', 10)])
    ant[TCP].flags = 'S'
    ant.window = 31337
    scan = sr1(ant, timeout=1)
    return process_t_scan(scan, ant)


def send_t6(hostname):
    ant = IP(dst=hostname) / TCP(sport=9094, dport=23, options=[('Timestamp', (0xFFFFFFFF, 0L)), ('MSS', 265),
    ('NOP', ()), ('SAckOK', ''), ('WScale', 10)])
    ant[IP].flags = 'DF'
    ant[TCP].flags = 'A'
    ant.window = 32768
    scan = sr1(ant, timeout=1)
    return process_t_scan(scan, ant)


def send_t7(hostname):
    ant = IP(dst=hostname) / TCP(sport=9095, dport=23, options=[('Timestamp', (0xFFFFFFFF, 0L)), ('MSS', 265),
    ('NOP', ()), ('SAckOK', ''), ('WScale', 15)])
    ant[TCP].flags = 'FPU'
    ant.window = 65535
    scan = sr1(ant, timeout=2)
    return process_t_scan(scan, ant)


def df_test(fingerprint, packet):
    if packet[IP].frag == 1:
        fingerprint['DF'] = 'Y'
    else:
        fingerprint['DF'] = 'N'
    return fingerprint


def tg_test(fingerprint, packet):
    if packet[IP].ttl > 128:
        fingerprint['TG'] = 255
    elif packet[IP].ttl > 64:
        fingerprint['TG'] = 128
    elif packet[IP].ttl > 32:
        fingerprint['TG'] = 64
    else:
        fingerprint['TG'] = 32
    return fingerprint


def s_test(fingerprint, scan, old):
    if scan[TCP].seq == 0:
        fingerprint['S'] = 'Z'
    elif scan[TCP].seq == old[TCP].seq:
        fingerprint['S'] = 'S'
    elif scan[TCP].seq == old[TCP].seq:
        fingerprint['S'] = 'S+'
    else:
        fingerprint['S'] = 'O'


def a_test(fingerprint, scan, old):
    if scan[TCP].ack == 0:
        fingerprint['A'] = 'A'
    elif scan[TCP].ack == old[TCP].ack:
        fingerprint['A'] = 'A'
    elif scan[TCP].ack == old[TCP].ack:
        fingerprint['A'] = 'A+'
    else:
        fingerprint['A'] = 'O'


def f_test(fingerprint, scan):
    fingerprint['F'] = str(scan[TCP].flags)


def w_test(fingerpront, scan):
    fingerpront['W'] = scan[TCP].window


def process_t_scan(scan, old):
    fingerprint = {}
    if scan is None:
        fingerprint['R'] = 'N'
    else:
        fingerprint['R'] = 'Y'
        df_test(fingerprint, scan)
        tg_test(fingerprint, scan)
        a_test(fingerprint, scan, old)
        s_test(fingerprint, scan, old)
        w_test(fingerprint, scan)
    return fingerprint

