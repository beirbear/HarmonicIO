class Setting(object):
    import socket
    import multiprocessing
    __node_name = None
    __node_addr = socket.gethostbyname(socket.gethostname())
    __node_port = None
    __node_data_port_start = None
    __node_data_port_stop = None
    __std_idle_time = None
    __token = "None"
    __max_workers = multiprocessing.cpu_count()
    __ext_process = None

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
    def get_data_port_start():
        return Setting.__node_data_port_start

    @staticmethod
    def get_data_port_stop():
        return Setting.__node_data_port_stop

    @staticmethod
    def get_std_idle_time():
        return Setting.__std_idle_time

    @staticmethod
    def get_token():
        return Setting.__token

    @staticmethod
    def get_max_worker():
        return Setting.__max_workers

    @staticmethod
    def get_external_process():
        return Setting.__ext_process

    @staticmethod
    def read_cfg_from_file():
        from .services import Services
        if not Services.is_file_exist('worker/configuration.json'):
            Services.t_print('worker/configuration.json does not exist')
        else:
            with open('worker/configuration.json', 'rt') as t:
                import json
                cfg = json.loads(t.read())

                try:
                    # Check for the json structure
                    if  Definition.get_str_node_name() in cfg and \
                        Definition.get_str_node_port() in cfg and \
                        Definition.get_str_data_port_range() in cfg and \
                        Definition.get_str_idle_time() in cfg and \
                        Definition.get_str_ext_process() in cfg:
                        # Check port number is int or not
                        if not isinstance(cfg[Definition.get_str_node_port()], int):
                            Services.t_print("Node port must be integer")
                        elif not isinstance(cfg[Definition.get_str_data_port_range()], list):
                            Services.t_print("Port range must be list")
                        elif not (isinstance(cfg[Definition.get_str_data_port_range()][0], int) and \
                                  isinstance(cfg[Definition.get_str_data_port_range()][1], int)):
                            Services.t_print("Port range must be integer")
                        elif len(cfg[Definition.get_str_data_port_range()]) != 2:
                            Services.t_print("Port range must compost of two elements: start, stop")
                        elif not isinstance(cfg[Definition.get_str_idle_time()], int):
                            Services.t_print("Idle time must be integer")
                        elif cfg[Definition.get_str_data_port_range()][0] > \
                             cfg[Definition.get_str_data_port_range()][1]:
                            Services.t_print("Start port range must greater than stop port range")
                        else:
                            Setting.__node_name = cfg[Definition.get_str_node_name()].strip()
                            Setting.__node_port = cfg[Definition.get_str_node_port()]
                            Setting.__node_data_port_start = cfg[Definition.get_str_data_port_range()][0]
                            Setting.__node_data_port_stop = cfg[Definition.get_str_data_port_range()][1]
                            Setting.__std_idle_time = cfg[Definition.get_str_idle_time()]
                            Setting.__ext_process = cfg[Definition.get_str_ext_process()].strip()
                            print("Load setting successful")
                except:
                    Services.t_print("Invalid data in configuration file.")


class Definition(object):
    @staticmethod
    def get_str_node_name():
        return "node_name"

    @staticmethod
    def get_str_node_port():
        return "node_port"

    @staticmethod
    def get_str_node_addr():
        return "node_addr"

    @staticmethod
    def get_str_data_port_range():
        return "node_data_port_range"

    @staticmethod
    def get_str_idle_time():
        return "std_idle_time"

    @staticmethod
    def get_str_ext_process():
        return "ext_process"

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

    class REST(object):
        @staticmethod
        def get_str_status():
            return "status"
