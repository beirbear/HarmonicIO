import socketserver
from .messaging_system import MessagesQueue


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    Definition class
    """
    pass


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    """
    This class is the main class that handle with requests from clients.
    the actual mechanism that pass the data to clients.
    """

    def handle(self):
        # Receive and interpret the request data
        data = bytearray()

        """
        Discard heading for now
        data += self.request.recv(16)

        # Interpret the header for file size
        file_size = struct.unpack(">Q", data[8:16])[0]
        """

        c = True
        while c != b"":
            c = self.request.recv(2048)
            data += c

        # Then, push data messaging system.
        MessagesQueue.push_to_queue(data)
