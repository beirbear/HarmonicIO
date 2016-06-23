from datetime import datetime
from general.definition import CStatus


class EngineChannel(object):
    def __init__(self, addr, port, status=CStatus.AVAILABLE):
        self.addr = addr
        self.port = port
        self.status = status
        self.last_seen = datetime.now()

    def __str__(self):
        return self.addr + str(self.port)

    def get_channel(self):
        return (self.addr, self.port)


class PEChannels(object):
    __channels = {}
    __available_channels = []

    @staticmethod
    def __get_channel_identity(addr, port):
        return addr + str(port)

    @staticmethod
    def register_channel(addr, port, status):

        identity = PEChannels.__get_channel_identity(addr, port)
        if identity not in PEChannels.__channels:
            PEChannels.__channels[identity] = EngineChannel(addr, port, status)
        else:
            PEChannels.__channels[identity].status = status
            PEChannels.__channels[identity].last_seen = datetime.now()

        if PEChannels.__channels[identity].status == CStatus.AVAILABLE:
            PEChannels.__available_channels.append(identity)

    @staticmethod
    def get_available_channel(group=None):
        """
        This method get channel by the order of registration.
        :return:
        """

        if not group:
            # No group define
            if len(PEChannels.__available_channels) == 0:
                return None

            c_identity = PEChannels.__available_channels.pop(0)
            PEChannels.__channels[c_identity].status = CStatus.BUSY
            return PEChannels.__channels[c_identity].get_channel()

        if group == "optimize":
            # Optimize group, utilize the cluster number into minimum
            if len(PEChannels.__available_channels) == 0:
                return None

            if len(PEChannels.__available_channels) == 1: pass
            else: PEChannels.__available_channels = sorted(PEChannels.__available_channels)

            c_identity = PEChannels.__available_channels.pop(0)
            PEChannels.__channels[c_identity].status = CStatus.BUSY
            return PEChannels.__channels[c_identity].get_channel()

    @staticmethod
    def view_available_channel():
        return [item for item in PEChannels.__available_channels]

