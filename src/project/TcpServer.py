import socket

LOCALHOST_ADDRESS = "127.0.0.1"
DEFAULT_PORT = 8888
BUFFER_SIZE = 1024
BACKLOG = 5


class TCPServer:
    def __init__(self, host=LOCALHOST_ADDRESS, port=DEFAULT_PORT):
        self.host = host
        self.port = port

    def start(self):
        """Method for starting the server."""

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            self._setup_socket(server_socket)
            print("Listening at", server_socket.getsockname())

            while True:
                conn, addr = server_socket.accept()
                print("Connected by", addr)

                data = conn.recv(BUFFER_SIZE)

                response = self.handle_request(data)

                conn.sendall(response)
                conn.close()

    def handle_request(self, raw_request: bytes):
        """Handles incoming data and returns a response.
        Override this in subclass.
        """
        return raw_request

    def _setup_socket(self, server_socket):
        """Sets up the socket for listening."""
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(BACKLOG)
