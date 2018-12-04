#!/usr/bin/env python3

import asyncio
import datetime
import sys
import os

HOST = '127.0.0.1'
PORT = 25252


from random import randint

from scapy.all import *
from scapy.modules.nmap import *


# Packets for nmap os tests


def get_random_test(target, port1, port2):
    tcpopt = [("WScale", 10),
              ("NOP", None),
              ("MSS", 256),
              ("Timestamp", (123, 0))]
    tests = [
        IP(dst=target, id=1) /
        TCP(seq=1, sport=5001 + i, dport=port1 if i < 4 else port2,
            options=tcpopt, flags=flags)
        for i, flags in enumerate(["CS", "", "SFUP", "A", "S", "A", "FPU"])
    ]
    tests.append(IP(dst=target) / UDP(sport=5008, dport=1) / (300 * "i"))
    return tests[randint(0, 7)]


# returns the the random test packet response
def test_fp(host, port1, port2):
    fingerprint = {}
    src = get_random_test(host, port1, port2)
    res = sr1(src, timeout=2)
    if src.sport == 5008:
        fingerprint["PU"] = (src, res)
        fingerprint["number"] = 8
    else:
        test = "T%i" % (src.sport - 5000)
        if res is not None and ICMP in res:
            warning("Test %s answered by an ICMP", test)
            res = None
        fingerprint[test] = res
        fingerprint["number"] = src.sport - 5000
        fingerprint['host'] = host
    return fingerprint



nmapResult = test_fp(HOST, PORT, 80)
nmapResult = str(nmapResult)


async def tcp_echo_client(message, loop):

    reader, writer = await asyncio.open_connection(HOST, PORT, loop=loop)
    # while serverResStop <= 5:
    #    nmapResult = test_fp(HOST, PORT, 80)
    #    nmapResult = str(nmapResult)
    #    serverResStop += 1
    writer.write(message.encode())
    data = await reader.read(100)
    writer.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(nmapResult, loop))
loop.close()
