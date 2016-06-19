import concurrent.futures
from .configuration import Setting
from general.definition import CStatus
import socket
import subprocess
from .services import Services
from general.definition import BatchErrorCode


class ChannelStatus(object):
    def __init__(self, port):
        self.port = port
        if self.is_port_open():
            self.status = CStatus.BUSY
        else:
            self.status = CStatus.AVAILABLE

    def is_port_open(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', self.port))
        sock.close()

        if result == 0:
            return True

        return False


class PEsMaster(object):
    def __init__(self):
        self.__pe_pool = concurrent.futures.ProcessPoolExecutor(max_workers=Setting.get_max_worker())
        self.__ports = []

        # Define port status
        for port_num in range(Setting.get_data_port_start(), Setting.get_data_port_stop()):
            self.__ports += [ChannelStatus(port_num)]

        # Check number of available port
        available_port = 0
        for item in self.__ports:
            if item.status == CStatus.AVAILABLE:
                available_port += 1

        if available_port < Setting.get_max_worker():
            Services.e_print("Important: Port number that can be used is less than the number of workers!")

        self.__available_port = available_port

    def __get_available_port(self):
        for item in self.__ports:
            if item.status == CStatus.AVAILABLE:
                item.status = CStatus.BUSY
                return item.port

        return None

    def run_pe(self):

        for i in range(Setting.get_max_worker()):
            port = self.__get_available_port()

            if not port:
                Services.e_print("Important: no more port available.")
                break

            batch_name = Setting.get_node_addr() + "_" + port

            self.__pe_pool.map(run_microbatch, (batch_name, port, Setting.get_master_addr(), Setting.get_master_port(), Setting.get_std_idle_time()))


def run_microbatch(info):

    # External process call
    def call_ext_process():

        cmd = Setting.get_external_process() + list(info)

        if subprocess.call(cmd) != BatchErrorCode.SUCCESS:
            return False

        return True

    while not call_ext_process():
        # If the process error, call it again without delay
        pass
