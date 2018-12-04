#!/usr/bin/env python3

import asyncio

from nmap_server import *

PORT = 25252

hosts = {}
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


async def handle_ants(reader, writer):
    data = await reader.read(100)
    message = data.decode()

    addr = writer.get_extra_info('peername')
    ants.append(addr)
    if message == '__EXIT__':
        loop.stop()
        print('Server Closed: Exit Message Received')
    fp = dict(message)
    host = fp['host']
    del fp['host']
    if host not in hosts:
        hosts[host] = {}
    guess = add_fingerprint(host, fp, hosts)
    if guess is not None:
        await signal_ants(ants, host, guess)
    writer.close()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_ants, '127.0.0.1', PORT, loop=loop)
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
