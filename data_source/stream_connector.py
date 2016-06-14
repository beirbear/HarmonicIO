"""
This module contain information about the master node and its connector
"""
from .services import Services
from .configuration import Definition
import urllib3


class StreamConnector(object):
    def __init__(self):
        from .configuration import Setting
        self.__master_addr = Setting.get_server_addr()
        self.__master_port = Setting.get_server_port()
        self.__connector = urllib3.PoolManager()

        # Test communication
        if self.is_master_alive():
            print("Testing connection to master: successful.")
        else:
            Services.e_print("Testing connection to master: fail.")

    def is_master_alive(self):
        response = self.__connector.request('GET', Definition.Server.get_str_check_master())
        if response.status == 200:
            return True

        return False

    def __get_stream_end_point(self):
        pass

    def __put_stream_end_point(self):
        pass

    def send_data(self, data):
        # The data must be byte array
        if not isinstance(data, bytearray):
            Services.t_print("Data type must by byte array in send_data method in StreamConnector")

