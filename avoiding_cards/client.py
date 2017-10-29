import socket
import threading
import logging


frame_splitter = b'\x7D\x7D\x7D\x7D'


class ClientMessageHandler:
    def handle(self, this_client, data: bytes):
        pass


class Client:
    def __init__(self, server_address: str, server_port: int, handler: ClientMessageHandler):
        self._server_address = server_address
        self._server_port = server_port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._handler = handler
        self._thread = threading.Thread(target=self._receive_messages)
        self._running = False
        logging.basicConfig(format='%(levelname)s: %(message)s')

    def start(self):
        self._socket.connect((self._server_address, self._server_port))
        self._running = True
        self._thread.start()

    def stop(self):
        self._running = False
        self._thread.join()
        self._socket.close()

    def send_data(self, data: bytes):
        data = data + frame_splitter
        try:
            self._socket.sendall(data)
        except:
            logging.error('Failed sending data to server')

    def _receive_messages(self):
        while self._running:
            received_data = self._socket.recv(2048)
            if len(received_data) > 0:
                frames = received_data.split(frame_splitter)
                for frame in frames:
                    if len(frame) > 0:
                        self._handler.handle(self, frame)
            else:
                self._running = False
                self._socket.close()
                logging.error('Server closed the connection, client stopped')

    def is_running(self):
        return self._running


####################################################################################################

# class DefaultHandler(MessageHandler):
#     def handle(self, data: bytes):
#         print('server said: {}'.format(data))
#
# dh = DefaultHandler()
#
# client = Client('localhost', 4000, dh)
# client.start()
# while True:
#     import time
#     from avoiding_cards import messages
#     import pickle
#     time.sleep(2)
#     client.send_data(pickle.dumps(messages.PlayerNameMessage('ZZZ')))
#     if not client.is_running():
#         break
