#!/usr/bin/env python3

import asyncio
import datetime
import sys
import os
import random

PORT = int(sys.argv[1])
rightNow = str(datetime.datetime.now())
answerList = ['Your guess is as good as mine', 'You need a vacation.', 'It\'s Trump\'s fault!', 'I don\'t know. What do you think?',
             'Nobody ever said it would be easy, they only said it would be worth it.', 'You really expect me to answer that?',
             'You\'re going to get what you deserve.', 'That depends on how much you\'re willing to pay.']
qAndaDict = {}

def randomNumberGenerator():
    return random.randint(0,7)

async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    fileList = [f for f in os.listdir('.') if os.path.isfile(f)]
    if message == '__EXIT__':
        loop.stop()
        print('Server Closed: Exit Message Recieved')
    connectionStr = "Connection from {0}".format(addr)
    if message not in qAndaDict.keys():
        ResponseData = answerList[randomNumberGenerator()]
        qAndaDict[message] = ResponseData
    else:
        ResponseData = qAndaDict[message]
    data = message + '{' + ResponseData
    data = data.encode('utf-8')
    writer.write(data)
    await writer.drain()

    fileNum = 1
    if message != '__EXIT__':
        if '8ball_message_1.txt' in fileList:
            while ('8ball_message_%d.txt' % fileNum) in fileList:
                fileNum += 1
                newFileName = ('8ball_message_%d.txt' % fileNum)
            with open(newFileName, 'w') as f:
                f.write(rightNow + '\n' + message + '\n' + ResponseData)
        else:
            with open('8ball_message_1.txt', 'w') as f:
                f.write(rightNow + '\n' + message + '\n' + ResponseData)
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
