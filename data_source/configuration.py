class Setting(object):
    __node_addr = None
    __node_port = None
    __node_name = None
    __server_addr = None
    __server_port = None
    __token = "None"
    is_running = False
    __std_idle_time = None

    @staticmethod
    def set_node_addr(addr=None):
        if addr:
            Setting.__node_addr = addr
        else:
            import socket
            from general.services import Services
            Setting.__node_addr = socket.gethostname()

            # if addr is valid
            if Services.is_valid_ipv4(Setting.__node_addr) or Services.is_valid_ipv6(Setting.__node_addr):
                return None

            # if addr is not valid
            Setting.__node_addr = Services.get_host_name_i()
            if Services.is_valid_ipv4(Setting.__node_addr) or Services.is_valid_ipv6(Setting.__node_addr):
                return None

            Services.t_print("Cannot get node ip address!")

    @staticmethod
    def get_node_name():
        return Setting.__node_name

    @staticmethod
    def get_node_addr():
        return Setting.__node_addr

    @staticmethod
    def get_node_port():
        return Setting.__node_port

    @staticmethod
    def get_server_addr():
        return Setting.__server_addr

    @staticmethod
    def get_server_port():
        return Setting.__server_port

    @staticmethod
    def get_token():
        return Setting.__token

    @staticmethod
    def get_std_idle_time():
        return Setting.__std_idle_time

    @staticmethod
    def read_cfg_from_file():
        from general.services import Services
        if not Services.is_file_exist('data_source/configuration.json'):
            Services.t_print('data_source/configuration.json does not exist')
        else:
            with open('data_source/configuration.json', 'rt') as t:
                try:
                    import json
                    cfg = json.loads(t.read())

                    from general.definition import Definition
                    # Check for the json structure
                    if  Definition.get_str_node_name() in cfg and \
                        Definition.get_str_server_addr() in cfg and \
                        Definition.get_str_server_port() in cfg and \
                        Definition.get_str_node_port() in cfg and \
                        Definition.get_str_idle_time() in cfg:
                        # Check port number is int or not
                        if not isinstance(cfg[Definition.get_str_server_port()], int):
                            Services.t_print("Server port must be integer")
                        elif not isinstance(cfg[Definition.get_str_node_port()], int):
                            Services.t_print("Node port must be integer")
                        elif not isinstance(cfg[Definition.get_str_idle_time()], int):
                            Services.t_print("Node port must be integer")
                        else:

                            Setting.set_node_addr()
                            Setting.__node_name = cfg[Definition.get_str_node_name()].strip()
                            Setting.__server_addr = cfg[Definition.get_str_server_addr()].strip()
                            Setting.__server_port = cfg[Definition.get_str_server_port()]
                            Setting.__node_port = cfg[Definition.get_str_node_port()]
                            Setting.__std_idle_time = cfg[Definition.get_str_idle_time()]
                            print("Load setting successful")
                except:
                    Services.t_print("Invalid setting in configuration file.")

"""
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
        def get_str_check_master():
            return "http://" + Setting.get_server_addr() + ":" + str(Setting.get_server_port()) + "/status?token=" + Setting.get_token()

        @staticmethod
        def get_str_push_req():
            return "http://" + Setting.get_server_addr() + ":" + str(Setting.get_server_port()) + "/streamRequest?token=" + Setting.get_token()

    class REST(object):
        @staticmethod
        def get_str_status():
            return "status"
"""