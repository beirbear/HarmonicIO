import socket
import struct
from concurrent.futures import ProcessPoolExecutor
from general.definition import Definition


class MessagingConfiguration(object):
    __queue_threshold = 4
    __max_in_memory_msg = 500

    @staticmethod
    def get_queue_threshold():
        return MessagingConfiguration.__queue_threshold

    @staticmethod
    def get_max_in_memory_msg():
        return  MessagingConfiguration.__max_in_memory_msg


class MessagesQueue(object):
    __msg_queue = []
    __pool = ProcessPoolExecutor()

    @staticmethod
    def push_to_queue(item):
        if not isinstance(item, bytearray):
            raise Exception("Invalid implementation! requires byte array but got something else.")

        MessagesQueue.__msg_queue.append([item])
        MessagesQueue.__check_for_scale()

    @staticmethod
    def get_queue_length():
        return len(MessagesQueue.__msg_queue)

    @staticmethod
    def pop_queue(index):
        return MessagesQueue.__msg_queue.pop(index)

    @staticmethod
    def is_queue_available():
        if MessagesQueue.get_queue_length() < MessagingConfiguration.get_max_in_memory_msg():
            return True

        return False

    @staticmethod
    def __check_for_scale():
        print("There are {0} tuples in queues.".format(MessagesQueue.get_queue_length()))

    @staticmethod
    async def stream_to_batch(c_addr, c_port):

        data = MessagesQueue.pop_queue(0)[0]

        def __push_stream_end_point(c_addr, c_port, data):
            # Create a client socket to connect to server

            s = None
            for res in socket.getaddrinfo(c_addr, c_port, socket.AF_UNSPEC, socket.SOCK_STREAM):
                af, socktype, proto, canonname, sa = res
                try:
                    s = socket.socket(af, socktype, proto)
                except OSError as msg:
                    s = None
                    continue
                try:
                    s.connect(sa)
                except OSError as msg:
                    s.close()
                    s = None
                    continue
                break
            if s is None:
                print('could not open socket')
                return False

            with s:
                s.sendall(data)
                s.sendall(b'')
                s.close()

            return True

        MessagesQueue.__pool.map(__push_stream_end_point(c_addr, c_port, data))
        # while not __push_stream_end_point(c_target, data): pass


class MessagingServices(object):
    __msg_id = 0

    @staticmethod
    def get_new_msg_id():
        MessagingServices.__msg_id += 1
        return MessagingServices.__msg_id

    @staticmethod
    def get_current_id():
        return MessagingServices.__msg_id
