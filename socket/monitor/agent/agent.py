# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
import Queue
import socket
import logging
import threading

import moniItems


def readn(sock):
    while True:
        data = sock.recv(4096)
        if len(data) == 0:
            break
        return data

class porterThread(threading.Thread):
    def __init__(self, name, q, trans, interval):
        super(porterThread, self).__init__()
        self.name = name
        self.q = q
        self.trans = trans
        self.interval = interval
        self.socket = None

    def run(self):
        if self.name == 'collect':
            self.collectLoop()
        elif self.name == 'sendjson':
            self.sendLoop()

    def collectLoop(self):
        items = moniItems.runAllGet()
        logging.debug('items:%s' % items)
        self.q.put(items)

    def sendLoop(self):
        while True:
            if not self.q.empty():
                data = self.q.get()
                self.sendjson(data)
            time.sleep(self.interval)

    def connect(self, addr):
        i = 0.1
        while True:
            try:
                self.sock = socket.create_connection(addr)
                return
            except Exception as e:
                logging.error('connect error:%s, try again' % e)
                time.sleep(i)
                i = i * 2
                if i > 30:
                    i = 30

    def sendjson(self, data):
        if self.socket == None:
            self.connect(self.trans)

        cnt = 1
        while cnt < 3:
            try:
                self.sock.send('%10d%s' % (len(data), data))
                body = readn(self.sock)
                logging.debug('body:%s' % body)
                return
            except Exception as e:
                logging.error('send error:%s' % e)
                self.sock.close()
                self.connect(self.trans)
                cnt += 1


def main():
    trans = ('127.0.0.1', 9000)
    q = Queue.Queue(10)

    collect = porterThread('collect', q, trans, interval=10)
    collect.setDaemon(True)
    collect.start()
    logging.debug('collect thread running.')

    time.sleep(1)
    sendjson = porterThread('sendjson', q, trans, interval=3)
    sendjson.setDaemon(True)
    sendjson.start()
    logging.debug('sendjson thread running.')

    collect.join()
    sendjson.join()

if __name__ == '__main__':
    FORMAT = '%(asctime)-15s %(filename)s line:%(lineno)d %(levelname)s %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    main()