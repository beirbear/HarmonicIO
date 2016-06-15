from datetime import datetime

class CStatus:
    AVAILABLE = 0
    BUSY = 1


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

        if PEChannels[identity] == CStatus.AVAILABLE:
            PEChannels.__available_channels.append(identity)

    @staticmethod
    def get_available_channel():
        if len(PEChannels.__available_channels) == 0:
            return None

        c_identity = PEChannels.__available_channels.pop(0)
        PEChannels.__channels[c_identity].status = CStatus.BUSY
        return PEChannels.__channels[c_identity].get_channel()
