# code based on EmojiSound (https://github.com/LolBaum/Emoji_Sound)
# by Luzie Ahrens and Laurin Dahm

import socket
import threading
import sys
import logging
from logging import config
import traceback

config.fileConfig("configs/loggingInfo.conf")
MAX_DATA_LENGTH = 8064  # TODO add header_len
MAX_CONNECTIONS = 30

class Server:


    def __init__(self, ip="127.0.0.1", port=5050, callback=None):
        self.ip = ip

        self.listeningPort = port
        self.addr = (self.ip, self.listeningPort)

        self.threads = []
        self.clients = []
        self.shutdown = False
        if callback:
            self.callback = callback
        else:
            self.callback = lambda x: (_ for _ in ()).throw(Warning('Callback to handle incoming messages has not been set'))

        # creating the socket
        self.listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_socket.bind(self.addr)

    def handle_client(self, conn, addr):
        logging.info(f"{addr} connected.")

        connected = True
        while connected:
            if self.shutdown:
                break
            try:
                msg = conn.recv(MAX_DATA_LENGTH)
                if msg:
                    logging.info(f"{addr} | {msg}")
                    self.callback(msg.decode('utf-8'))

            except Exception as e:
                logging.error(
                    f"connection to {addr} broke up. [ACTIVE CONNECTIONS] {threading.active_count() - 2} | {e}\n" +
                    traceback.format_exc()
                 )
                connected = False

        conn.close()
        logging.info(f"connection to ({addr}) has been closed.")

        for c in self.clients:
            if (conn, addr) == c:
                self.clients.remove(c)
                logging.info(
                    f"Client ({addr}) has removed from the list. {len(self.clients)} clients remaining"
                )

    def start(self):
        try:
            logging.info(f"Server IP: {self.ip}:{self.listeningPort}")
            self.listening_socket.listen()
            self.listening_socket.setblocking(False)
            self.listening_socket.settimeout(1)
            logging.info(f"Server is listening on {self.ip}:{self.listeningPort}")
            while True:
                if self.shutdown:
                    break
                try:
                    conn, addr = self.listening_socket.accept()
                except socket.timeout:
                    continue
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                self.threads.append(thread)
                self.clients.append((conn, addr))
                thread.deamon = True
                thread.start()
                logging.info(f"active connections: {threading.active_count() - 2}")
        except Exception as e:
            logging.error(f"Exception in main tread: {e}")
        finally:
            logging.info("Server is shutting down")
            self.end()

    def end(self):
        self.shutdown = True
        try:
            logging.info("closing all connections")
            if len(self.clients) > 0:
                for c in self.clients:
                    logging.debug(f"closing connection to {c[1]}")
                    c[0].close()
        except Exception as e:
            logging.error(f"Couldn't shut server down properly... {e}")
            sys.exit(1)
        sys.exit(0)

    def share_message(self, msg, origin=(None, None)):
        for conn, addr in self.clients:
            if addr[0] != origin[0]:
                try:
                    logging.info(f"sharing msg with {addr}")
                    conn.send(msg)
                except Exception as e:
                    logging.error(
                        f"Couldn't share '{msg}' with {addr}, closing connection | {e}"
                    )
                    conn.close()




if __name__ == "__main__":
    logging.info("Server is starting...")
    the_server = Server()
    the_server.start()
