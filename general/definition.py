class BatchErrorCode:
    SUCCESS = 0
    CREATE_SOCKET_ERROR = 1
    PROCESSING_ERROR = 2


class CStatus:
    AVAILABLE = 0
    BUSY = 1


class Definition(object):
    @staticmethod
    def get_str_node_name():
        return "node_name"

    @staticmethod
    def get_str_node_addr():
        return "node_addr"

    @staticmethod
    def get_str_server_addr():
        return "server_addr"

    @staticmethod
    def get_str_server_port():
        return "server_port"

    @staticmethod
    def get_str_node_port():
        return "node_port"

    @staticmethod
    def get_str_idle_time():
        return "std_idle_time"

    @staticmethod
    def get_str_data_port_range():
        return "node_data_port_range"

    @staticmethod
    def get_str_idle_time():
        return "std_idle_time"

    @staticmethod
    def get_str_token():
        return "token"

    @staticmethod
    def get_str_load1():
        return "load1"

    @staticmethod
    def get_str_load5():
        return "load5"

    @staticmethod
    def get_str_load15():
        return "load15"

    @staticmethod
    def get_cpu_load_command():
        return ['uptime', '|', 'awk', '{ print $8 $9 $10}']

    class Server(object):
        @staticmethod
        def get_str_check_master(addr, port, token):
            return "http://" + addr + ":" + str(port) + "/" + Definition.REST.get_str_status() + "?" + \
                   Definition.REST.get_str_token() + "=" + token

        @staticmethod
        def get_str_push_req(addr, port, token):
            return "http://" + addr + ":" + str(port) + "/" + Definition.REST.get_str_stream_req() + "?" + \
                   Definition.REST.get_str_token() + "=" + token

    class REST(object):
        @staticmethod
        def get_str_status():
            return "status"

        @staticmethod
        def get_str_stream_req():
            return "streamRequest"

        @staticmethod
        def get_str_token():
            return "token"
