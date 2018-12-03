#!/usr/bin/env python3

import asyncio
import datetime
import sys
import os
import random

PORT = 25252

async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    connectionStr = "Connection from {0}".format(addr)
    if message == '__EXIT__,0':
        loop.stop()
        print('Server Closed: Exit Message Recieved')
    print(message)
    writer.write(data)
    await writer.drain()
    writer.close()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', PORT, loop=loop)
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
