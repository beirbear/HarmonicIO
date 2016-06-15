import socketserver
import struct

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
        header = self.request.recv(16)

        # Interpret the header for file size
        print("t_id", struct.unpack(">Q", header[:8])[0])
        print("file_size", struct.unpack(">Q", header[8:])[0])

        data = bytearray(header)
        data += self.request.recv(struct.unpack(">Q", header[8:])[0])

        print("header", len(header), "data", struct.unpack(">Q", header[8:]), "payload", len(data))