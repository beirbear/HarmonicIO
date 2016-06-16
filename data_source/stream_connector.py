"""
This module contain information about the master node and its connector
"""
from .services import Services
from .configuration import Definition, Setting
import urllib3
import json
import time
import socket
import struct


class StreamConnector(object):
    def __init__(self):
        from .configuration import Setting
        self.__master_addr = Setting.get_server_addr()
        self.__master_port = Setting.get_server_port()
        self.__connector = urllib3.PoolManager()

    def is_master_alive(self):
        try:
            response = self.__connector.request('GET', Definition.Server.get_str_check_master())
            if response.status == 200:
                return True
        except:
            return False

    def __get_stream_end_point(self):
        response = self.__connector.request('GET', Definition.Server.get_str_push_req())

        if response.status != 200:
            return False
        try:
            content = json.loads(response.data.decode('utf-8'))

            return (content['c_addr'], int(content['c_port']), int(content['t_id']), )

        except:
            Services.t_print("JSON content error from the master!\n" + response.data.decode('utf-8'))


    def __push_stream_end_point(self, target, data):
        # Create a client socket to connect to server

        s = None
        for res in socket.getaddrinfo(target[0], target[1], socket.AF_UNSPEC, socket.SOCK_STREAM):
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
            Services.e_print("Cannot connect to " + target[0] + ":" + str(target[1]))
            return False

        with s:
            """
            Discard heading for now
            data[0:8] = struct.pack(">Q", target[2])
            data[8:16] = struct.pack(">Q", len(data))
            """

            s.sendall(data)
            s.sendall(b'')
            s.close()

        return True

    def send_data(self, data):
        # The data must be byte array
        if not isinstance(data, bytearray):
            Services.t_print("Data type must by byte array in send_data method in StreamConnector")

        c_target = self.__get_stream_end_point()
        while not c_target:
            time.sleep(Setting.get_std_idle_time())
            c_target = self.__get_stream_end_point()

        while not self.__push_stream_end_point(c_target, data):
            time.sleep(Setting.get_std_idle_time())
