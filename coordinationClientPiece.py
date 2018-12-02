#!/usr/bin/env python3

import asyncio
import datetime
import sys
import os

HOST = '127.0.0.1'
PORT = int(sys.argv[1])
QUESTION = (sys.argv[2])
rightNow = str(datetime.datetime.now())

async def tcp_echo_client(message, loop):
    reader, writer = await asyncio.open_connection(HOST, PORT, loop=loop)
    fileList = [f for f in os.listdir('.') if os.path.isfile(f)]
    writer.write(message.encode())
    data = await reader.read(100)
    data = data.decode()
    data = data.split('{')
    questionData = data[0]
    responseData = data[1]
    fileNum = 1
    if questionData != '__EXIT__':
        if '8ball_response_1.txt' in fileList:
            while ('8ball_response_%d.txt' % fileNum) in fileList:
                fileNum += 1
                newFileName = ('8ball_response_%d.txt' % fileNum)
            with open(newFileName, 'w') as f:
                f.write(rightNow + '\n' + questionData + '\n' + responseData)
        else:
            with open('8ball_response_1.txt', 'w') as f:
                f.write(rightNow + '\n' + questionData + '\n' + responseData)
    writer.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(QUESTION, loop))
loop.close()
