#!/usr/bin/env python3

import asyncio
import random

from nmap_server import *
import ast

PORT = 25252

hosts = {}
known = {}
ants = []


async def signal_ants(ant_list, host, guess):
    resp = dict()
    resp['ip'] = host
    resp['guess'] = guess
    msg = str(resp)
    for i in ant_list:
        reader, writer = await asyncio.open_connection(
            i, 8888)
        writer.write(msg.encode())
        writer.close()
        await writer.wait_closed()

def ant_signal_parser(message):
    message = message.replace('<', '{ ', 1)
    message = message.replace('>', '} ', 1)
    message = message.replace('<', '')
    message = message.replace('>', '')
    message = message.replace('|', '')
    message = message.replace('(', '')
    message = message.replace(')', '')
    message = message.replace('IP  version', 'IP_Version')
    message = message.replace('IP  frag', 'IP_Frag')
    message = message.replace('TCP  sport', 'TCP_Sport')
    message = message.replace('UDP  sport', 'UDP_Sport')
    message = message.replace('UDPerror  sport', 'UDPerror_Sport')
    message = message.replace('Raw  load=', '\'Raw_Load\' : ')
    message = message.replace('ICMP  type', 'ICMP_Type')
    message = message.replace('IPerror  version', 'IPerror_Version')
    message = message.replace('Padding  load=', '\'Padding_Load\' : ')
    messageList = message.split()
    i = 0
    #if 'IPerror_Version' not in message:
    while i < (len(messageList) - 1):
        if '=' in messageList[i] and 'Padding_Load' not in messageList[i] and 'Raw_Load' not in messageList[i]:
            messageList[i] = messageList[i].replace('=', "\' : \'")
            messageList[i] = "\'" + messageList[i] + "\', "
        i += 1
    return messageList


async def handle_ants(reader, writer):

    data = await reader.read(8192)
    message = data.decode()

    addr = writer.get_extra_info('peername')
    ants.append(addr)
    if message == '__EXIT__':
        loop.stop()
        print('Server Closed: Exit Message Received')
    #print(message)
    '''
    messageList = ant_signal_parser(message)
    dictTranslate = ''.join(messageList)
    print(dictTranslate)
    '''
    fp = ast.literal_eval(message)
    host = fp['host']
    del fp['host']
    if host not in hosts:
        hosts[host] = {}
    guess = add_fingerprint(host, fp, hosts)
    if guess is not None:
    #     await signal_ants(ants, host, guess)
        if host not in known:
            known[host]=1
            print(host+':  '+str(guess))
        elif known[host] == 1:
            known[host] = 2
            ending = random.randint(140, 190)
            print('192.198.58.'+ str(ending)+':  '+str(guess))

    writer.close()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_ants, '192.168.58.129', PORT, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass


# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
