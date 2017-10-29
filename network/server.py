import socket
import select
import threading
import logging


class Server:
    def __init__(self, port: int, response_timeout: int, max_connections: int=7):
        self._port = port
        self._response_timeout = response_timeout  # seconds
        self._max_connections = max_connections
        self._clients = []
        self._client_buffers = []
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._thread = threading.Thread(target=self._connection_handler)
        self._lock = threading.Lock()
        self._running = False
        logging.basicConfig(format='%(levelname)s: %(message)s')

    def start(self):
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind(('', self._port))
        self._socket.listen(self._max_connections)
        self._running = True
        self._thread.start()

    def stop(self):
        self._running = False
        self._thread.join()
        for client in self._clients:
            client.close()
        self._clients = []
        self._client_buffers = []
        self._socket.close()

    def _connection_handler(self):
        timeout = 0.05  # seconds
        while self._running:
            interesting_sockets = [self._socket] + self._clients
            rlist, wlist, xlist = select.select(interesting_sockets, [], [], timeout)
            with self._lock:
                for incoming in rlist:
                    if incoming == self._socket:
                        # accept incoming connections
                        client, address = incoming.accept()
                        self._clients.append(client)
                        self._client_buffers.append(bytearray())
                    else:
                        # check if client sockets are sending data or got disconnected
                        received_data = incoming.recv(2048)
                        if len(received_data) > 0:
                            self._client_buffers[self._clients.index(incoming)] = received_data
                        else:
                            del self._client_buffers[self._clients.index(incoming)]
                            self._clients.remove(incoming)
                            logging.warning('Client disconnected: %s', incoming.getsockname())

    def broadcast_data(self, data: bytes):
        for client in self._clients:
            try:
                client.sendall(data)
            except:
                logging.error('Failed broadcast to: %s', client.getsockname())

    def send_to_client(self, data: bytes, client_id: int):
        if len(self._clients) > client_id:
            client = self._clients[client_id]
            try:
                client.sendall(data)
            except:
                logging.error('Failed sending to client: %d @ %s', client_id, client.getsockname())
        else:
            logging.error('Client does not exist: %d', client_id)

    def read_client_data(self, client_id: int) -> bytes:
        data = bytearray()
        if len(self._clients) > client_id:
            with self._lock:
                data = self._client_buffers[client_id]
                self._client_buffers[client_id] = bytearray()
        else:
            logging.error('Client does not exist: %d', client_id)
        return data

    def get_connected_clients(self):
        return self._clients

    def is_running(self):
        return self._running

####################################################################################################

server = Server(4000, 2)
server.start()
while True:
    import time
    time.sleep(2)
    server.send_to_client('kaj ima\n'.encode(), 0)
    server.broadcast_data('lima\n'.encode())
    response = server.read_client_data(0)
    if response:
        print(response)
    else:
        print('jbg')
