# Luzie Ahrens and Laurin Dahm
# 22.09.2021

import sys
import threading
import time
import socket
import logging
from logging import config

config.fileConfig("configs/loggingInfo.conf")


class Client:
    def __init__(self, ip="127.0.0.1", port=5050):
        self.ip = ip
        self.port = port

        self.is_running = False
        self.thread = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (ip, port)

    def start(self, ip=None, port=None):
        if ip:
            self.ip = ip
        if port:
            self.port = port
        self.addr = (self.ip, self.port)
        self.socket.connect(self.addr)
        self.is_running = True

    def send(self, msg):
        self.socket.send(msg.encode('utf-8'))

    def disconnect(self):
        self.socket.close()


if __name__ == '__main__':
    client = Client()
    client.run()
